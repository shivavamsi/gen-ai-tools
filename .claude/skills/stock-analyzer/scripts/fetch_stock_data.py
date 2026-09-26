# /// script
# requires-python = ">=3.10"
# dependencies = ["yfinance>=0.2.54"]
# ///
"""Fetch hard numbers for stocks and ETFs from Yahoo Finance (via yfinance) as JSON.

Usage: uv run fetch_stock_data.py [--brief] TICKER [TICKER ...]
       e.g. uv run fetch_stock_data.py AAPL RELIANCE.NS VOO

--brief skips annual statements, headlines, earnings dates and fund holdings: faster and
shorter output for screening long candidate lists.

Exit codes: 0 = at least one ticker fetched, 1 = every ticker failed, 2 = usage error.
Yahoo data is unofficial and may be delayed; the skill cross-checks it with web sources.
"""
# yfinance raises many undocumented exception types; each field degrades to null instead of aborting.
# ruff: noqa: BLE001

from __future__ import annotations

import json
import logging
import math
import sys
from datetime import datetime, timezone

import pandas as pd
import yfinance as yf

# Failures are reported in the JSON "errors" field; keep yfinance's own logging off stderr.
logging.getLogger("yfinance").setLevel(logging.CRITICAL)

# Exchange suffix -> benchmark index for the relative 1-year return.
BENCHMARKS = {
    "": "^GSPC",  # United States
    ".TO": "^GSPTSE",  # Canada
    ".V": "^GSPTSE",  # Canada (TSX Venture)
    ".L": "^FTSE",  # United Kingdom
    ".DE": "^GDAXI",  # Germany
    ".PA": "^FCHI",  # France
    ".AS": "^AEX",  # Netherlands
    ".SW": "^SSMI",  # Switzerland
    ".T": "^N225",  # Japan
    ".HK": "^HSI",  # Hong Kong
    ".SS": "000001.SS",  # Shanghai
    ".SZ": "399001.SZ",  # Shenzhen
    ".NS": "^NSEI",  # India NSE
    ".BO": "^BSESN",  # India BSE
    ".AX": "^AXJO",  # Australia
    ".KS": "^KS11",  # South Korea
    ".TW": "^TWII",  # Taiwan
    ".SI": "^STI",  # Singapore
    ".SA": "^BVSP",  # Brazil
    ".MX": "^MXX",  # Mexico
}
FALLBACK_BENCHMARK = "ACWI"  # iShares MSCI All Country World ETF

VALUATION = {
    "pe": ("trailingPE",),
    "forward_pe": ("forwardPE",),
    "peg": ("trailingPegRatio", "pegRatio"),
    "price_to_book": ("priceToBook",),
    "price_to_sales": ("priceToSalesTrailing12Months",),
    "ev_to_ebitda": ("enterpriseToEbitda",),
}
HEALTH = {
    "revenue_growth_yoy": ("revenueGrowth",),
    "earnings_growth_yoy": ("earningsGrowth",),
    "gross_margin": ("grossMargins",),
    "operating_margin": ("operatingMargins",),
    "net_margin": ("profitMargins",),
    "roe": ("returnOnEquity",),
    "roa": ("returnOnAssets",),
    "debt_to_equity_pct": ("debtToEquity",),
    "current_ratio": ("currentRatio",),
    "total_cash": ("totalCash",),
    "total_debt": ("totalDebt",),
    "free_cash_flow": ("freeCashflow",),
    "operating_cash_flow": ("operatingCashflow",),
    "payout_ratio": ("payoutRatio",),
}
OWNERSHIP = {
    "insiders_pct": ("heldPercentInsiders",),
    "institutions_pct": ("heldPercentInstitutions",),
    "short_pct_float": ("shortPercentOfFloat",),
    "beta": ("beta",),
}
ANALYSTS = {
    "rating": ("recommendationKey",),
    "rating_mean_1_buy_5_sell": ("recommendationMean",),
    "analyst_count": ("numberOfAnalystOpinions",),
    "target_mean": ("targetMeanPrice",),
    "target_low": ("targetLowPrice",),
    "target_high": ("targetHighPrice",),
}
FUND = {
    "category": ("category",),
    "fund_family": ("fundFamily",),
    "total_assets": ("totalAssets",),
    "yield": ("yield",),
    "three_year_avg_return": ("threeYearAverageReturn",),
    "five_year_avg_return": ("fiveYearAverageReturn",),
}
ANNUAL_ROWS = {
    "revenue": ("income", "Total Revenue"),
    "net_income": ("income", "Net Income"),
    "diluted_shares": ("income", "Diluted Average Shares"),
    "free_cash_flow": ("cashflow", "Free Cash Flow"),
}


def clean(value):
    """Convert numpy/pandas scalars to JSON-safe values; NaN and inf become None."""
    if value is None:
        return None
    if hasattr(value, "item"):
        value = value.item()
    if isinstance(value, float):
        return None if math.isnan(value) or math.isinf(value) else round(value, 4)
    return value


def pick(info: dict, fields: dict) -> dict:
    """Map output names to the first non-empty Yahoo info key listed for each."""
    out = {}
    for name, keys in fields.items():
        out[name] = next((clean(info[k]) for k in keys if clean(info.get(k)) is not None), None)
    return out


def ratio(numerator, denominator):
    if numerator is None or not denominator:
        return None
    return round(numerator / denominator, 4)


def cagr(values: list):
    """Compound annual growth between the first and last positive values."""
    points = [v for v in values if v is not None]
    if len(points) < 2 or points[0] <= 0 or points[-1] <= 0:
        return None
    return round((points[-1] / points[0]) ** (1 / (len(points) - 1)) - 1, 4)


def benchmark_for(symbol: str) -> str:
    suffix = "." + symbol.rsplit(".", 1)[1] if "." in symbol else ""
    return BENCHMARKS.get(suffix, FALLBACK_BENCHMARK)


def one_year_return(close: pd.Series):
    year = close[close.index >= close.index[-1] - pd.Timedelta(days=365)]
    return ratio(year.iloc[-1] - year.iloc[0], year.iloc[0]) if len(year) > 1 else None


def benchmark_return(symbol: str, cache: dict):
    if symbol not in cache:
        try:
            close = yf.Ticker(symbol).history(period="1y")["Close"].dropna()
            cache[symbol] = one_year_return(close) if not close.empty else None
        except Exception:
            cache[symbol] = None
    return cache[symbol]


def rsi14(close: pd.Series):
    delta = close.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / 14, adjust=False).mean().iloc[-1]
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / 14, adjust=False).mean().iloc[-1]
    return 100.0 if loss == 0 else round(100 - 100 / (1 + gain / loss), 1)


def trend(close: pd.Series, price, bench_symbol: str, cache: dict) -> dict:
    sma50 = clean(close.tail(50).mean()) if len(close) >= 50 else None
    sma200 = clean(close.tail(200).mean()) if len(close) >= 200 else None
    ret_1y = one_year_return(close)
    bench_1y = benchmark_return(bench_symbol, cache)
    return {
        "sma50": sma50,
        "sma200": sma200,
        "pct_vs_sma200": ratio(price - sma200, sma200) if price and sma200 else None,
        "rsi14": rsi14(close) if len(close) > 15 else None,
        "return_1y": ret_1y,
        "benchmark": bench_symbol,
        "benchmark_return_1y": bench_1y,
        "excess_return_1y": round(ret_1y - bench_1y, 4) if ret_1y is not None and bench_1y is not None else None,
    }


def annual(ticker: yf.Ticker) -> dict:
    """Up to four fiscal years of revenue, profit, FCF and share count, oldest first."""
    frames = {}
    for name, attr in (("income", "income_stmt"), ("cashflow", "cashflow")):
        try:
            frames[name] = getattr(ticker, attr)
        except Exception:
            frames[name] = pd.DataFrame()
    income = frames["income"]
    if income is None or income.empty:
        return {}
    years = sorted(income.columns)[-4:]
    out = {"fiscal_years": [y.strftime("%Y-%m") for y in years]}
    for name, (frame_name, row) in ANNUAL_ROWS.items():
        frame = frames[frame_name]
        if frame is None or row not in frame.index:
            out[name] = None
            continue
        out[name] = [clean(frame.at[row, y]) if y in frame.columns else None for y in years]
    out["revenue_cagr"] = cagr(out["revenue"] or [])
    out["diluted_shares_change_per_year"] = cagr(out["diluted_shares"] or [])
    return out


def fund_details(ticker: yf.Ticker, info: dict) -> dict:
    out = pick(info, FUND)
    try:
        funds = ticker.funds_data
        ops = funds.fund_operations
        if "Annual Report Expense Ratio" in ops.index:
            out["expense_ratio"] = clean(ops.loc["Annual Report Expense Ratio"].iloc[0])
        holdings = funds.top_holdings
        out["top_holdings"] = [
            {"symbol": sym, "name": row.get("Name"), "weight": clean(row.get("Holding Percent"))}
            for sym, row in holdings.head(10).iterrows()
        ]
        out["top10_weight"] = clean(holdings.head(10)["Holding Percent"].sum())
        out["sector_weights"] = {k: clean(v) for k, v in funds.sector_weightings.items() if v}
    except Exception as exc:
        out["funds_data_error"] = f"{type(exc).__name__}: {exc}"
    return out


def next_earnings(ticker: yf.Ticker):
    try:
        dates = (ticker.calendar or {}).get("Earnings Date") or []
        return str(dates[0]) if dates else None
    except Exception:
        return None


def headlines(ticker: yf.Ticker, limit: int = 5) -> list:
    try:
        items = ticker.news or []
    except Exception:
        return []
    out = []
    for item in items[:limit]:
        content = item.get("content", item)
        provider = content.get("provider") or {}
        published = content.get("pubDate") or content.get("providerPublishTime")
        if isinstance(published, (int, float)):
            published = datetime.fromtimestamp(published, timezone.utc).isoformat()
        out.append(
            {
                "title": content.get("title"),
                "publisher": provider.get("displayName") or content.get("publisher"),
                "published": published,
            }
        )
    return out


def analyze(symbol: str, cache: dict, brief: bool = False) -> dict:
    ticker = yf.Ticker(symbol)
    try:
        info = ticker.info or {}
    except Exception:
        info = {}
    close = ticker.history(period="2y")["Close"].dropna()
    price = clean(info.get("currentPrice") or info.get("regularMarketPrice"))
    if price is None and not close.empty:
        price = clean(close.iloc[-1])
    if price is None:
        raise ValueError("no data returned; check the symbol and exchange suffix (e.g. RELIANCE.NS, BRK-B)")

    currency = info.get("currency")
    financial_currency = info.get("financialCurrency") or currency
    kind = info.get("quoteType", "UNKNOWN")
    data = {
        "name": info.get("longName") or info.get("shortName"),
        "type": kind,
        "exchange": info.get("exchange"),
        "currency": currency,
        "financial_currency": financial_currency,
        "country": info.get("country"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "price": price,
        "market_cap": clean(info.get("marketCap")),
        "week52_high": clean(info.get("fiftyTwoWeekHigh")),
        "week52_low": clean(info.get("fiftyTwoWeekLow")),
        "trend": trend(close, price, benchmark_for(symbol), cache) if not close.empty else {},
    }
    if not brief:
        data["next_earnings"] = next_earnings(ticker)
        data["headlines"] = headlines(ticker)
    high = data["week52_high"]
    data["pct_below_52w_high"] = ratio(price - high, high) if high else None

    if kind in ("ETF", "MUTUALFUND"):
        data["fund"] = pick(info, FUND) if brief else fund_details(ticker, info)
        return data

    data["valuation"] = pick(info, VALUATION)
    data["health"] = pick(info, HEALTH)
    data["ownership"] = pick(info, OWNERSHIP)
    data["analysts"] = pick(info, ANALYSTS)
    data["annual"] = {} if brief else annual(ticker)
    data["notes"] = []
    health, yearly = data["health"], data["annual"]
    # Yahoo's dividendYield is a percentage and, unlike the trailing field, stays correct for ADRs.
    dividend_pct = clean(info.get("dividendYield"))
    health["dividend_yield"] = round(dividend_pct / 100, 4) if dividend_pct is not None else None
    cash, debt = health["total_cash"], health["total_debt"]
    health["net_cash"] = cash - debt if cash is not None and debt is not None else None

    if health["free_cash_flow"] is None and (yearly.get("free_cash_flow") or [None])[-1] is not None:
        health["free_cash_flow"] = yearly["free_cash_flow"][-1]
        data["notes"].append("free_cash_flow is the latest fiscal year, not trailing 12 months")
    if data["market_cap"] is None and (yearly.get("diluted_shares") or [None])[-1] is not None:
        data["market_cap"] = round(price * yearly["diluted_shares"][-1])
        data["notes"].append("market_cap estimated as price x latest diluted shares")
    # Market cap is in the quote currency; only compare it with statements in the same currency.
    if financial_currency == currency:
        data["valuation"]["fcf_yield"] = ratio(health["free_cash_flow"], data["market_cap"])
    else:
        data["valuation"]["fcf_yield"] = None
        data["notes"].append(f"statements in {financial_currency}, quote in {currency}: convert before comparing")
    return data


def main(argv: list[str]) -> int:
    # Accept "AAPL MSFT", "AAPL,MSFT" or one quoted string holding several tickers.
    args = " ".join(argv).replace(",", " ").split()
    brief = "--brief" in args
    symbols = list(dict.fromkeys(s.upper() for s in args if not s.startswith("--")))
    if not symbols:
        print(__doc__, file=sys.stderr)
        return 2
    result = {
        "as_of": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "Yahoo Finance via yfinance (unofficial; prices may be delayed ~15 min)",
        "units": [
            "Margins, growth, returns, yields, ownership and fcf_yield are fractions (0.25 = 25%).",
            "debt_to_equity_pct is a percentage (150 = 1.5x).",
            "Prices, averages and targets use currency (GBp = pence; divide by 100 for GBP; market_cap is then in GBP).",
            "Cash, debt, free cash flow and the annual figures use financial_currency.",
            "Trend returns use dividend-adjusted closes. fcf_yield is null when the two currencies differ.",
        ],
        "tickers": {},
        "errors": {},
    }
    cache: dict = {}
    for symbol in symbols:
        try:
            result["tickers"][symbol] = analyze(symbol, cache, brief)
        except Exception as exc:
            result["errors"][symbol] = f"{type(exc).__name__}: {exc}"
    print(json.dumps(result, indent=2, default=str))
    return 0 if result["tickers"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
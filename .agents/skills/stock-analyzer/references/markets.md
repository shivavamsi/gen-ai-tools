# Global Markets Reference

Use this to pick the right macro indicators, primary filings, and local sentiment sources for each ticker. Judge macro where the company **earns** its revenue. A US-listed ADR of a Taiwanese chipmaker needs both Taiwan and US conditions.

## Ticker Conventions (Yahoo Finance)

- Share classes use a hyphen: `BRK-B`, not `BRK.B`.
- Suffix = exchange: `RELIANCE.NS`, `SHEL.L`, `7203.T`, `0700.HK`, `005930.KS`, `2330.TW`, `600519.SS`.
- Japan, Hong Kong, China, Korea and Taiwan use numeric codes. Search "<company> Yahoo Finance ticker" when unsure.
- A company listed in several places: default to the primary home listing unless the user names one. Mention the ADR when it is how most readers can buy it.
- **ADRs** (TSM, BABA, INFY, ASML, NVO): the quote is in USD but statements may be in the home currency (see the script's `notes`). Check the ADR ratio before any per-share math.

## Listing, Benchmark & Macro

| Region | Suffix | Currency | Benchmark (script) | Central bank | Key macro to check |
|:--|:--|:--|:--|:--|:--|
| United States | *(none)* | USD | S&P 500 `^GSPC` | Federal Reserve | CPI/PCE, jobs report, ISM PMI, GDP, 10-yr Treasury yield, rate expectations (CME FedWatch) |
| Canada | `.TO`, `.V` | CAD | TSX `^GSPTSE` | Bank of Canada | CPI, jobs, oil, housing, US trade |
| United Kingdom | `.L` | GBp (pence) | FTSE 100 `^FTSE` | Bank of England | CPI, wage growth, GDP, gilt yields, GBP |
| Germany / France / Netherlands | `.DE` / `.PA` / `.AS` | EUR | DAX `^GDAXI` / CAC 40 `^FCHI` / AEX `^AEX` | ECB | HICP inflation, PMI, GDP, Bund yields, EUR/USD, energy prices |
| Other Eurozone (`.MI`, `.MC`, …) | varies | EUR | ACWI fallback | ECB | Same as above plus national fiscal and spread risk |
| Switzerland | `.SW` | CHF | SMI `^SSMI` | SNB | CPI, CHF strength (hurts exporters) |
| Japan | `.T` | JPY | Nikkei 225 `^N225` | Bank of Japan | CPI, wage talks (shunto), JGB yields and BoJ policy, JPY, Tankan survey |
| China A-shares | `.SS` / `.SZ` | CNY | `000001.SS` / `399001.SZ` | PBoC | NBS and Caixin PMI, CPI/PPI, credit growth, property sales, stimulus, US–China trade and export controls |
| Hong Kong | `.HK` | HKD | Hang Seng `^HSI` | HKMA (USD peg, follows the Fed) + PBoC | Mainland China data, US rates, capital flows |
| India | `.NS` / `.BO` | INR | Nifty 50 `^NSEI` / Sensex `^BSESN` | RBI | CPI, repo rate, GDP, INR, crude oil, FII/DII flows, monsoon, budget policy |
| Australia | `.AX` | AUD | ASX 200 `^AXJO` | RBA | CPI, jobs, iron ore, China demand, housing |
| South Korea | `.KS` (`.KQ` → ACWI) | KRW | KOSPI `^KS11` | Bank of Korea | Exports (especially chips), KRW, CPI |
| Taiwan | `.TW` | TWD | TAIEX `^TWII` | Central Bank (CBC) | Exports, semiconductor cycle, TWD, cross-strait risk |
| Singapore | `.SI` | SGD | STI `^STI` | MAS (policy through the exchange rate) | Trade, rates, property |
| Brazil | `.SA` | BRL | Ibovespa `^BVSP` | Banco Central (Selic) | IPCA inflation, Selic rate, BRL, commodities, fiscal |
| Mexico | `.MX` | MXN | IPC `^MXX` | Banxico | US trade and nearshoring, remittances, MXN |
| Anything else | other | local | ACWI fallback | Local central bank | IMF/World Bank outlook, local CPI, rates, currency |

Global cross-checks for any region: IMF World Economic Outlook, OECD outlook, oil (Brent), the US dollar index, the US 10-year yield, and major geopolitical events.

## Primary Sources & Local Sentiment

| Region | Filings / primary sources | Local sentiment (plus Reddit, X, StockTwits for all) |
|:--|:--|:--|
| United States | SEC EDGAR (10-K, 10-Q, 8-K, Form 4 insider trades), company IR | r/stocks, r/investing, r/wallstreetbets, r/ValueInvesting, StockTwits |
| Canada | SEDAR+ | r/CanadianInvestor, Stockhouse |
| United Kingdom | RNS announcements (London Stock Exchange site), Companies House | r/UKInvesting, lse.co.uk forums, ADVFN |
| Europe | Company IR sites, national regulators (BaFin, AMF, AFM, CONSOB, CNMV) | r/eupersonalfinance, r/mauerstrassenwetten (DE), Boursorama forums (FR) |
| Switzerland | SIX Swiss Exchange | r/SwissPersonalFinance |
| Japan | EDINET, TDnet | Yahoo! Finance Japan message boards (掲示板), Kabutan, Minkabu |
| China / Hong Kong | CNINFO, SSE/SZSE, HKEXnews | Xueqiu (Snowball), Eastmoney Guba, AAStocks |
| India | NSE/BSE corporate announcements, annual reports, Screener.in | r/IndiaInvestments, r/IndianStreetBets, r/StockMarketIndia, ValuePickr, Moneycontrol boards |
| Australia | ASX announcements | HotCopper, r/ASX_Bets, r/AusFinance |
| South Korea | DART | Naver Finance discussion boards |
| Taiwan | MOPS | PTT Stock board |
| Singapore | SGX announcements | r/singaporefi, HardwareZone forums |
| Brazil / Mexico | CVM / BMV | r/investimentos (BR) |

Non-English forums: search in the local language when possible (e.g. the company name in Japanese or Chinese). Summarize the tone in English and treat automatic translation as approximate.
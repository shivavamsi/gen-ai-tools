# Analysis Framework (Long-Term, 1–5 Years)

How to turn data into a verdict. Score five pillars from 1 (weak) to 5 (strong), apply red-flag gates, then use timing only to choose between BUY now and WAIT.

The rubric guides judgment; it is not a formula. If you override it, say why in one line of the report.

---

## Pillar 1 — Business Strength (weight 35%)

Is this a good business that will be bigger and more profitable in 5 years?

| Check | Strong | Weak |
|:--|:--|:--|
| Revenue growth (3–4 yr `revenue_cagr`) | > 10%/yr, steady | Shrinking or erratic |
| Profitability (`operating_margin`, `net_margin`) | Above industry peers, stable or rising | Losses, or margins falling |
| Returns (ROE / ROA / ROIC) | ROE > 15% with modest debt | ROE < 8% |
| Cash (`free_cash_flow`, annual trend) | Positive and growing | Negative for years, funded by debt or new shares |
| Balance sheet (`net_cash`, `debt_to_equity_pct`, current ratio) | Net cash, or debt < 2× EBITDA | Debt > 4× EBITDA, or near-term maturities larger than cash |
| Share count (`diluted_shares_change_per_year`) | Falling (buybacks) | Rising > 3%/yr (dilution) |
| Moat | Clear edge: brand, network effects, switching costs, cost advantage, patents, licences | Commodity product, no pricing power |
| Management | Consistent guidance, sensible capital allocation, insiders own shares | Missed guidance, empire-building deals, heavy insider selling |

Scoring: **5** = durable moat, 3+ years of growing revenue and cash flow, strong balance sheet. **3** = solid but average, cyclical, or mixed. **1** = shrinking, burning cash, or overloaded with debt or dilution.

Adjust for sector. Generic ratios mislead here:

- **Banks**: use P/B, ROE, capital ratio (CET1), bad-loan ratio (NPL), deposit trends. Ignore debt/equity and FCF.
- **Insurers**: combined ratio (< 100% = underwriting profit), P/B, reserve adequacy.
- **REITs**: FFO/AFFO per share, occupancy, loan-to-value, P/FFO. Ignore net income and P/E.
- **Utilities and telecoms**: regulated returns, dividend coverage, debt maturity schedule.
- **Companies with a captive finance arm** (automakers, equipment makers): consolidated FCF and debt include the lending book. Judge the industrial business on its own.
- **Cyclicals and commodities** (energy, mining, chemicals, autos, semis): judge on mid-cycle earnings. A low P/E at the peak of the cycle is often a trap.
- **Unprofitable growth** (young tech, biotech): revenue growth, gross margin, cash runway (cash ÷ yearly burn), and a credible path to profit. Runway under 18 months is a soft red flag.
- **Buyback-heavy firms**: a very high ROE (> 100%) can come from shrunken equity. Use ROA and margins instead.

---

## Pillar 2 — Price vs Value (weight 25%)

Is the price fair for what you get?

1. Compare the multiples (`pe`, `forward_pe`, `ev_to_ebitda`, `price_to_sales`, `price_to_book`, `fcf_yield`) with three references: the stock's own 5-year average (search for it), its closest peers, and the local market index.
2. Rules of thumb (sector context overrides them):
   - PEG: < 1 cheap · 1–2 fair · > 2 pricey (only meaningful for steady growers)
   - FCF yield (mature firms): > 6% cheap · 3–6% fair · < 2% pricey
   - P/S > 15 with no profits: priced for perfection
3. **Estimate a fair-value range with at least two methods**:
   - Earnings: forward EPS × a justified P/E (the peer median or the stock's own 5-year median, adjusted for growth).
   - Cash flow: FCF per share ÷ a target FCF yield (e.g. 4–5% for quality compounders, 6–8% for average firms).
   - Analyst mean target: use it as a cross-check only, never on its own.
   Report a range (low–high), rounded. Say it is rough.

Scoring: **5** = price below the low end of the fair range · **4** = lower half of the range · **3** = near the middle · **2** = upper half, or up to 10% above the high end · **1** = more than 10% above the high end, or valuation that needs everything to go right.

---

## Pillar 3 — Industry & Competition (micro) (weight 15%)

- Is the industry growing, flat, or shrinking? What drives it (tailwinds and headwinds)?
- Is market share rising or falling against the 2–3 main competitors?
- Pricing power: can it raise prices without losing customers?
- Concentration: any customer or supplier above 20% of revenue?
- Disruption and regulation: new technology, antitrust, price controls, licence changes, subsidies ending.

Scoring: **5** = a leader in a growing industry with rising share · **3** = a stable position in a mature industry · **1** = losing share in a shrinking or disrupted industry.

---

## Pillar 4 — Economy (macro) (weight 15%)

Judge the economy where the company **earns** its money, not only where it is listed. See [markets.md](markets.md) for each region's central bank, key data, and index.

- **Interest rates**: the direction of the next moves. Rising rates hurt high-valuation growth stocks, REITs, utilities, and heavy borrowers. Banks gain from moderately higher rates.
- **Inflation**: does the company have pricing power, or will its costs rise faster than its prices?
- **Growth**: GDP, PMI, jobs. Cyclicals (industrials, materials, discretionary, semis) need growth. Defensives (staples, healthcare, utilities) hold up in slowdowns.
- **Currency**: a strong home currency hurts exporters and helps importers. For foreign stocks, the investor's own currency affects their return.
- **Commodities**: oil for energy and airlines, metals for miners, and input costs for manufacturers.
- **Policy and geopolitics**: tariffs, sanctions, export controls, elections, wars, taxes and subsidies.

Scoring: **5** = clear tailwinds for this business · **3** = neutral or mixed · **1** = strong headwinds.

---

## Pillar 5 — Crowd Mood (sentiment) (weight 10%)

What are investors saying and doing? Collect signals from these sources:

| Source | What to look for |
|:--|:--|
| Reddit (r/stocks, r/investing, r/wallstreetbets, regional subs in [markets.md](markets.md)) | Tone, volume of posts, quality of arguments |
| StockTwits, X (Twitter) | Bull/bear ratio, trending status, hype language |
| News headlines (last 30–90 days) | Tone and topic: earnings, lawsuits, deals, management changes |
| Analyst revisions (last 90 days) | Estimates and targets moving up or down, upgrades and downgrades |
| Insider trades | Clusters of open-market *buying* are meaningful; routine planned selling is not |
| Short interest (`short_pct_float`) | > 10% of float = many bettors against it |

Label the mood **Positive / Neutral / Negative / Mixed** and the heat **Quiet / Normal / Hyped**.

Rules:
- Smart-money signals (insider buying, estimate revisions, institutional flows) count more than retail chatter.
- Contrarian extremes: heavy hype plus a stretched valuation → lower the score. Heavy pessimism plus strong fundamentals can be an opportunity, so do not penalize it.
- Pump warning: a small cap, sudden volume, promotional posts, and no real company news → hard red flag.
- Mood never overrides fundamentals for a long-term verdict. It adjusts conviction and timing.

Scoring: **5** = positive with smart money agreeing · **3** = neutral or mixed · **1** = negative with smart money leaving.

---

## Red-Flag Gates (check before scoring)

**Hard flags** mean the verdict is **SELL** if the business is broken, or **AVOID** for new money. The overall score does not matter:
- Going-concern warning, or bankruptcy risk (debt due in 12 months is larger than cash plus expected FCF, with no financing)
- Credible accounting-fraud allegations, a restatement, or an auditor resignation
- Trading halt, delisting notice, or sanctions blocking ownership
- Pump-and-dump pattern (see Pillar 5)
- Leveraged or inverse ETF (2×, 3×, −1×) or single-stock ETF held long term: daily resets erode value over time

**Soft flags** cap the verdict at **HOLD** or **WAIT** and set conviction to Low:
- Share count rising > 5%/yr
- Negative FCF for 3+ years with < 18 months of cash runway
- CEO or CFO left suddenly, or a major lawsuit or regulatory action is pending
- One customer > 30% of revenue
- Structural risk for foreign listings (e.g. China VIE structures, ADR delisting risk, capital controls)
- Binary event ahead (drug trial result, court ruling, licence decision) that could move the price ±30%

---

## Weighted Score → Verdict

`Score = 0.35×Business + 0.25×Value + 0.15×Industry + 0.15×Macro + 0.10×Mood` (range 1–5)

| Condition (after the red-flag gates) | Verdict |
|:--|:--|
| Score ≥ 3.8 and Value ≥ 3 | **BUY** (use the timing check below) |
| Score ≥ 3.8 and Value ≤ 2 | **WAIT**: good business, high price. Give a buy-below price. |
| Score 3.0–3.7 and Value ≥ 4 | **BUY**, conviction Medium or lower |
| Score 3.0–3.7 otherwise | **HOLD**: fine to keep, not compelling to buy |
| Score 2.3–2.9 | **AVOID**: weak case; better options likely exist |
| Score < 2.3 | **SELL** |

**Timing check (entry only; it never turns a weak stock into a BUY):**
- Overheated means RSI14 > 70, *or* price more than 25% above its 200-day average (`pct_vs_sma200` > 0.25), *or* price above the fair-value high. If a BUY is overheated, change it to **WAIT** and give the buy-below level.
- Earnings due within 14 days: keep BUY, but suggest buying in 2–3 parts.
- Downtrend (price below a falling 200-day average) with good fundamentals: keep BUY, but suggest buying in parts. Do not try to catch the exact bottom.

**Price levels to report:**
- *Buy-below*: the low-to-mid part of the fair-value range. Round it.
- *Consider trimming above*: about 15–20% above the fair-value high.

**Conviction:**
- **High**: pillars agree, data is complete and recent (script plus 2 or more sources), no soft flags.
- **Medium**: some pillars disagree, or there are minor data gaps.
- **Low**: important data is missing, signals conflict, soft flags are present, less than 2 years of history, or a binary event is ahead.

---

## Personalizing (only when the user gives position details)

Inputs: shares held, average cost, share of portfolio (%), and risk tolerance.

- Compute unrealized gain or loss: `(price − avg cost) ÷ avg cost`.
- **The purchase price does not change what the stock is worth now.** Decide from today's facts, not from breaking even.
- **ADD**: the generic verdict is BUY and the position is below the concentration limit.
- **HOLD**: the thesis is intact and the price is within or near the fair range.
- **TRIM** (sell part): the price is above the "consider trimming" level, *or* the position is above the concentration limit (about 10% of the portfolio for a conservative investor, 15% moderate, 20–25% aggressive).
- **SELL**: a hard red flag, or the long-term thesis is broken, whatever the gain or loss.
- Mention taxes once, briefly, when a sale would realize a large gain ("check the tax impact before selling"). Give no specific tax advice.
- Risk tolerance: for conservative investors, treat volatile names (beta > 1.5, unprofitable, binary events) one notch more cautiously.

---

## ETF Framework

Replace Pillars 1–3 with these checks. Keep Macro and Mood, applied to the fund's exposure.

| Check | Good | Concern |
|:--|:--|:--|
| Cost (`expense_ratio`) | Broad index ≤ 0.10%; sector/international ≤ 0.40% | Passive fund > 0.50%; active/thematic > 0.75% |
| Diversification (`top10_weight`, `sector_weights`) | Top 10 < 35%, no sector > 40% | Top 10 > 50%, or one theme |
| What's inside | Quality holdings at reasonable aggregate valuation | Holdings priced for perfection; many unprofitable firms |
| Size & trading (`total_assets`) | > $1B, tight spreads | < $100M (closure risk), thin trading |
| Track record (`three_year_avg_return`, `five_year_avg_return`, `excess_return_1y`) | Tracks its index closely, beats category peers | Lags its index or category persistently |
| Fit | Core holding (broad market, total bond) | Narrow or hype-driven theme bought after a big run |

Special cases:
- **Leveraged, inverse, or single-stock ETFs**: hard flag, **AVOID** for long-term holding. Explain daily-reset decay in one line.
- **Covered-call / income ETFs**: upside is capped and NAV can erode. The high yield is not free money.
- **Bond ETFs**: say how sensitive the price is to interest rates (duration) and what the credit quality is.
- **Crypto or commodity ETFs**: there are no fundamentals to score. Use Macro, Mood, and cost; conviction is Low; suggest a small position size.

Verdict for ETFs: use the same scale (BUY / WAIT / HOLD / AVOID / SELL). For broad, cheap index funds, the question is usually *when and how much*, not *whether*. Default to BUY, or WAIT when valuations are stretched, and suggest regular fixed-amount buying (dollar-cost averaging).
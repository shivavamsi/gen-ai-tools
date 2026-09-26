# Report Templates & Examples

All examples use **fictional** companies (ACME, BOLT, CRUX). They show shape and tone only; never reuse their numbers.

## Writing Rules

- **Lead with the verdict.** The reader should know what to do from the first two lines.
- **Plain words, short sentences** (≤ 20 words), with no unexplained jargon. When a term is needed, explain it in a few words:
  - P/E → "price vs profit (P/E 24)"
  - Free cash flow → "cash left after running the business"
  - Moat → "competitive edge"
  - Dilution → "company issuing new shares, shrinking your slice"
  - 200-day average → "long-term price trend"
  - RSI > 70 → "price ran up fast (overheated)"
- **At most about 6 numbers per stock** outside the table. Round them ($84, not $84.1732). Every number needs a meaning ("sales up 14% a year", not "revenue CAGR 0.1403").
- **Length**: one stock ≤ about 25 lines. Several stocks: comparison table plus at most 2 lines per stock.
- **Never invent a number.** If a figure is unknown, write "n/a" in the table and don't mention it in the prose.
- Only when the data script failed, add this line under the header: `⚠️ Live data tool unavailable. Numbers are from web sources (dated) and may be less exact.`
- End every report with the sources line and the disclaimer line.

## Verdict Badges

| Badge | Meaning in plain words |
|:--|:--|
| 🟢 **BUY** | Good business at a fair or cheap price. Buy now (in parts is fine). |
| ⏳ **WAIT** | Good business, but the price is too high or it just ran up. Buy below the stated price. |
| 🟡 **HOLD** | Fine to keep. Not a strong reason to buy more or to sell. |
| ⛔ **AVOID** | Weak case. Don't start a position. Better options likely exist. |
| 🔴 **SELL** | Business or story is broken, or there's a serious red flag. Get out and stay out. |
| ➕ **ADD** / 🟠 **TRIM** | Personalized only: buy more, or sell part of your position. |

Ratings in tables: Business and Industry → 🟢 Strong · 🟡 OK · 🔴 Weak. Value → 🟢 Cheap/Fair · 🟡 Full · 🔴 Pricey. Mood → 🟢 Positive · 🟡 Mixed/Neutral · 🔴 Negative, plus "· Hyped" when the heat is extreme. Trend → 🟢 Up · 🟡 Sideways · 🔴 Down, plus "(overheated)" when it applies.

---

## Template A — Single Stock or ETF

```markdown
## {{badge}} {{VERDICT}} — {{Company}} ({{TICKER}})
**{{price}}** · Fair value ≈ {{low}}–{{high}} · Conviction: **{{High|Medium|Low}}** · Data as of {{YYYY-MM-DD}}

**In short:** {{1–2 plain sentences: what the business is like and whether the price is right}}

- **If you don't own it:** {{action + price level}}
- **If you own it:** {{action + trim/sell level}}

| Check | Rating | In plain words |
|:--|:--|:--|
| Business strength | {{rating}} | {{one line}} |
| Price vs value | {{rating}} | {{one line}} |
| Industry & competition | {{rating}} | {{one line}} |
| Economy | {{rating}} | {{one line}} |
| Crowd mood | {{rating · heat}} | {{one line: social + news + analysts}} |
| Price trend | {{rating}} | {{one line: entry timing only}} |

**Biggest risk:** {{one line}}
**What would change this call:** {{one concrete trigger → new verdict}}

*Sources: {{3–6 short named links}} · Educational analysis, not financial advice. Prices move; check before trading.*
```

For an ETF, rename the first three rows **Cost & size**, **What's inside**, and **Diversification**.

### Example A — Single stock, generic

Input: `/stock-analyzer ACME`

```markdown
## 🟢 BUY — Acme Robotics (ACME)
**$84** · Fair value ≈ $90–105 · Conviction: **Medium** · Data as of 2026-09-26

**In short:** A strong, growing business at a fair price. A good buy to hold for 3–5 years.

- **If you don't own it:** Buy now, ideally in 2–3 parts. It's still good value up to about $95.
- **If you own it:** Hold. Consider trimming above $125.

| Check | Rating | In plain words |
|:--|:--|:--|
| Business strength | 🟢 Strong | Sales up 14% a year; keeps 22¢ profit from each $1 of sales; more cash than debt |
| Price vs value | 🟢 Fair | Price vs profit (P/E 24) is below its usual 29 |
| Industry & competition | 🟢 Strong | Factory automation is growing, and Acme is winning share |
| Economy | 🟡 OK | Lower rates help; new tariffs on parts hurt a little |
| Crowd mood | 🟡 Mixed · Quiet | Analysts raising targets; Reddit worried about one slow quarter |
| Price trend | 🟢 Up | Above its long-term trend, not overheated |

**Biggest risk:** If factories cut spending, orders could fall by about a fifth.
**What would change this call:** Two quarters in a row of falling orders → HOLD.

*Sources: ACME Q2 results (Aug 2026), Yahoo Finance, Reuters, r/stocks · Educational analysis, not financial advice. Prices move; check before trading.*
```

---

## Template B — Comparison (2–4 tickers: tickers as columns)

```markdown
## Stock Comparison: {{T1}} vs {{T2}} vs {{T3}} · Data as of {{YYYY-MM-DD}}

**Quick answer:** {{one or two sentences: best pick for new money, what to wait on, what to skip}}

| | {{T1}} | {{T2}} | {{T3}} |
|:--|:--|:--|:--|
| **Verdict** | {{badge VERDICT}} | … | … |
| Conviction | | | |
| Price → fair value | | | |
| Buy below | | | |
| Business strength | | | |
| Price vs value | | | |
| Industry | | | |
| Economy | | | |
| Crowd mood | | | |
| Price trend | | | |
| Sales growth (per yr) | | | |
| Profit margin | | | |
| 1-yr return vs its index | | | |
| Biggest risk | | | |

**Why:**
- **{{T1}} — {{VERDICT}}.** {{≤ 2 plain sentences, with a price level}}
- …

**Ranking for new money:** 1. … · 2. … · 3. …

*Sources: … · Educational analysis, not financial advice. Prices move; check before trading.*
```

- **5–8 tickers**: flip the table so tickers are rows. Keep only Verdict, Conviction, Price → fair value, Business, Value, Mood, and Biggest risk.
- **Stocks mixed with ETFs**: add a `Cost per year` row (ETF expense ratio, "—" for stocks). Use "—" wherever a row doesn't apply.
- **Different currencies**: show each price in its own currency and compare using percentages, never raw prices.

### Example B — Comparison

Input: `/stock-analyzer ACME BOLT CRUX`

```markdown
## Stock Comparison: ACME vs BOLT vs CRUX · Data as of 2026-09-26

**Quick answer:** ACME is the best buy today. BOLT is the best business but too pricey right now, so wait. Skip CRUX.

| | ACME | BOLT | CRUX |
|:--|:--|:--|:--|
| **Verdict** | 🟢 **BUY** | ⏳ **WAIT** | ⛔ **AVOID** |
| Conviction | Medium | High | Medium |
| Price → fair value | $84 → $90–105 | $310 → $220–260 | $12 → $8–11 |
| Buy below | $95 | $240 | — |
| Business strength | 🟢 Strong | 🟢 Strong | 🔴 Weak |
| Price vs value | 🟢 Fair | 🔴 Pricey | 🔴 Pricey |
| Industry | 🟢 Strong | 🟢 Strong | 🟡 OK |
| Economy | 🟡 OK | 🟡 OK | 🔴 Weak |
| Crowd mood | 🟡 Mixed | 🟢 Positive · Hyped | 🔴 Negative |
| Price trend | 🟢 Up | 🟢 Up (overheated) | 🔴 Down |
| Sales growth (per yr) | 14% | 31% | −6% |
| Profit margin | 22% | 35% | −4% |
| 1-yr return vs its index | +9% | +48% | −31% |
| Biggest risk | Factory slowdown | Priced for perfection | Cash running low |

**Why:**
- **ACME — BUY.** A solid grower at a fair price. Buy in parts; still good value up to $95.
- **BOLT — WAIT.** Great business, but today's price assumes years of perfect growth. Buy below $240.
- **CRUX — AVOID.** Sales are shrinking and cash lasts about a year. If you own it, sell into bounces.

**Ranking for new money:** 1. ACME · 2. BOLT (at a lower price) · 3. CRUX

*Sources: company Q2 results, Yahoo Finance, Reuters, StockTwits, r/investing · Educational analysis, not financial advice. Prices move; check before trading.*
```

---

## Personalized Add-On

When the user gives position details, replace the two "If you…" bullets (or add under each ticker in a comparison) with:

```markdown
**Your position:** {{shares}} shares at {{avg cost}} → {{+/−X%}} ({{gain/loss amount}}). {{Portfolio weight vs limit, if given}}.
**What to do:** {{badge ADD|HOLD|TRIM|SELL}} — {{one or two plain sentences with a concrete level}}
```

### Example C — Personalized

Input: `Should I keep BOLT? I have 40 shares at $150, about 30% of my portfolio. Moderate risk.`

```markdown
**Your position:** 40 shares at $150 → +107% (about +$6,400). BOLT is ~30% of your portfolio, twice the ~15% limit for moderate risk.
**What to do:** 🟠 **TRIM** — Sell about half to bring BOLT near 15%. Keep the rest; the business is strong. Check the tax impact before selling.
```
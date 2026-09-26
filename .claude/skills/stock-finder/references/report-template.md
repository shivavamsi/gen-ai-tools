# Stock-Finder Report Template

Apply the **writing rules, verdict badges, and rating labels** from stock-analyzer's `report-template.md`: plain words, short sentences, explained jargon, rounded numbers, and no invented figures. The example below uses **fictional** companies and tickers. It shows shape and tone only; never reuse its numbers.

Target length: about 40 lines or fewer.

## Template

```markdown
## 🔎 {{Theme}}: best stocks to buy now · Data as of {{YYYY-MM-DD}}

**What it is:** {{one plain sentence}}
**Right now:** {{stage emoji + stage}}. {{one plain line on current circumstances}}
**How I picked:** Screened {{N}} {{US-listed}} companies → {{M}} made the shortlist → analyzed each in depth.

## 🏆 Best buy now: {{Company}} ({{TICKER}}) — {{badge VERDICT}}
**{{price}}** · Fair value ≈ {{low}}–{{high}} · {{Good value up to | Buy below}} {{level}} · Conviction: **{{High|Medium|Low}}**

- **{{Reason 1 label}}:** {{position in the theme}}
- **{{Reason 2 label}}:** {{financial strength}}
- **{{Reason 3 label}}:** {{price vs value}}

**Main risk:** {{one line}}

**Other ways to play it:**
- 🛡️ **Play it safer: {{TICKER}} ({{Company}}), {{badge VERDICT}}.** {{one line, with the exposure level if Indirect}}
- 🚀 **More upside, more risk: {{TICKER}} ({{Company}}), {{badge VERDICT}}.** {{one line on why it's riskier + a level}}
- 🧺 **Simpler option: {{ETF TICKER}} ETF, {{badge VERDICT}}.** {{number of holdings, yearly cost}}

| Rank | Stock | Verdict | Exposure | Business | Value | Mood | Risk | Buy below |
|:--|:--|:--|:--|:--|:--|:--|:--|:--|
| 1 | … | … | Pure-play / Significant / Indirect | … | … | … | Low / Medium / High | … |

**Left out:** {{up to 4 notable names with a 2–4 word reason: too small (under $2B), little real exposure, red flag}}

*Sources: {{3–6 short named sources}} · Educational analysis, not financial advice. Prices move; check before trading.*
```

Stage emoji: 🌱 Early · 🔥 Hype · 🟢 Growth · 🏛️ Mature · 🧊 Bust.

**Variants**
- **Global expansion triggered**: add this line under "How I picked": `🌍 No US-listed stock met the bar, so non-US stocks were included.` After each non-US ticker, add a short access note, e.g. "(US ADR: XXXX)" or "(needs international trading access)".
- **No BUY anywhere, but a top WAIT exists**: change the header to `## 🏆 Best pick (wait for a better price): {{Company}} ({{TICKER}}) — ⏳ WAIT` and give the buy-below level in the first line.
- **Nothing qualifies**: change the header to `## 🏆 No clear buy right now`. Explain why in 1–2 lines, then show the table as a watchlist with buy-below levels.
- **Personal details given**: mark owned stocks "(you own)" in the table, and add one line under the best pick on how it fits their risk level or holdings.
- Leave out any "Other ways" bullet that has no qualifying candidate. Never repeat a ticker across slots.

---

## Example (fictional companies)

Input: `/stock-finder warehouse robotics`

```markdown
## 🔎 Warehouse Robotics: best stocks to buy now · Data as of 2026-09-26

**What it is:** Robots and software that move, pick, and pack goods in warehouses.
**Right now:** 🟢 Growth. Orders are rising as labor costs climb. The leaders make money, but a few already look pricey.
**How I picked:** Screened 14 US-listed companies → 5 made the shortlist → analyzed each in depth.

## 🏆 Best buy now: Acme Robotics (ACME) — 🟢 BUY
**$84** · Fair value ≈ $90–105 · Good value up to $95 · Conviction: **Medium**

- **A leader:** #2 in warehouse robots, winning customers from older rivals.
- **Healthy:** Sales up 14% a year, profitable, more cash than debt.
- **Fair price:** Price vs profit (P/E 24) is below its usual 29.

**Main risk:** A slowdown in retail spending could delay new warehouse orders.

**Other ways to play it:**
- 🛡️ **Play it safer: BOLT (Bolt Industrial), 🟡 HOLD.** Huge, steady, and pays a dividend. Robots are only ~20% of sales (indirect), so there's less upside.
- 🚀 **More upside, more risk: CRUX (Crux Automation), ⏳ WAIT.** Almost pure robots, with sales up 40% a year, but it barely makes a profit and is pricey. Buy below $48.
- 🧺 **Simpler option: ROBF ETF, 🟢 BUY.** 45 robotics stocks in one fund; costs 0.55% a year.

| Rank | Stock | Verdict | Exposure | Business | Value | Mood | Risk | Buy below |
|:--|:--|:--|:--|:--|:--|:--|:--|:--|
| 1 | ACME | 🟢 BUY | Significant | 🟢 Strong | 🟢 Fair | 🟡 Mixed | Medium | $95 |
| 2 | CRUX | ⏳ WAIT | Pure-play | 🟡 OK | 🔴 Pricey | 🟢 Positive · Hyped | High | $48 |
| 3 | BOLT | 🟡 HOLD | Indirect | 🟢 Strong | 🟡 Full | 🟢 Positive | Low | $140 |
| 4 | DYNX | ⛔ AVOID | Significant | 🔴 Weak | 🟡 Full | 🔴 Negative | High | — |

**Left out:** GRIP (too small, under $2B) · HAUL (robots under 5% of sales) · KNOT (accounting restatement)

*Sources: company Q2 results, IFR robotics report, Yahoo Finance, Reuters, r/stocks · Educational analysis, not financial advice. Prices move; check before trading.*
```
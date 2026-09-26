# Discovery Playbook

How to go from a theme ("humanoid robots", "GLP-1 drugs", "grid batteries") to a scored shortlist. Scoring and verdicts come from stock-analyzer's `analysis-framework.md`. This file covers only what is specific to finding stocks.

---

## 1. Map the Theme

Write down, before any stock search:

- **Definition**: one plain sentence saying what the field is and what it is not. Pin down vague words: "batteries" could mean cell makers, materials, grid storage, or EVs.
- **Value chain**: 3–4 layers, each with the kind of company that earns money there:
  - *Picks & shovels*: tools, chips, materials, equipment everyone in the field needs
  - *Core builders*: companies whose main product *is* the theme
  - *Platforms & integrators*: large firms bundling the theme into wider offerings
  - *Adopters*: customers who benefit (usually a weak way to invest in the theme; include only if they are the clearest winners)
- **Growth drivers and blockers**: demand, costs, regulation, subsidies, technology hurdles.
- **Market size**: one dated estimate from a credible source, labeled as an estimate.

Too broad (e.g. "tech", "healthcare")? Ask the user to pick one of 3 suggested sub-themes. Otherwise, choose the layers with the clearest profit pools and say which ones you picked.

---

## 2. Read the Current Circumstances

The user wants the best buy *now*. Classify the theme's stage using this evidence:

| Stage | Signs | What it means for picks |
|:--|:--|:--|
| **Early** | Little real revenue, big promises, winners unclear | Favor diversified leaders or an ETF; cap conviction at Medium |
| **Hype** | Theme stocks/ETF up > 50% in a year, extreme valuations, IPO/SPAC wave, mainstream buzz | Favor WAIT with buy-below levels; demand real profits |
| **Growth** | Revenue growing fast and broadly, leaders emerging, margins improving | Favor the leaders at fair prices |
| **Mature** | Slower growth, consolidation, price competition | Favor cash flow, dividends, low valuations; watch the cycle |
| **Bust** | Prices down > 40% from peak, gloom, weak players failing | Favor the strongest balance sheets; opportunity if fundamentals hold |

Evidence to collect: the 1-year return of the main thematic ETF against the S&P 500; average valuation of the leaders against the market; news and social volume; capital raising (IPOs, secondary offerings); and whether reported revenue is actually growing. Also note theme-specific policy (subsidies, tariffs, export controls, approvals) and how interest rates affect long-duration growth stocks.

Summarize it all in one plain line for the report, e.g. "Demand is booming, but prices already assume years of it."

---

## 3. Build the Long List (8–20 companies)

**Discovery sources** (use several; ask each "who makes money here?"):
- **Thematic ETF holdings.** Find 1–3 ETFs for the theme by web search, then run the data script *without* `--brief` on them to get their top holdings. This is the best seed list.
- **Competitor sections of annual reports** (10-K "Competition"; investor presentations) of the first names you find.
- **Industry and market-research coverage**: trade press, industry associations, government or agency reports.
- **"Best <theme> stocks <month year>" articles**: use them as leads only. They are often promotional, outdated, or paid.
- **News**: recent contracts, product launches, funding rounds, partnerships.

For each company, record the ticker, the listing, a rough market cap, and its **theme exposure**:

| Exposure | Test |
|:--|:--|
| **Pure-play** | > 50% of revenue, or of expected growth, comes from the theme |
| **Significant** | 20–50% of revenue, or the theme is management's stated main growth driver with material revenue |
| **Indirect** | 5–20% of revenue, or a strategic program with little revenue yet |
| **Token** | < 5% and not a growth driver. Exclude it as "theme-washing" (buzzwords without business). |

Base exposure on evidence: segment reporting, investor presentations, earnings-call remarks. In pre-revenue fields, use backlog, contracts, R&D spend, and management's stated priority as proxies, and mark the exposure "early-stage".

---

## 4. Screen to a Shortlist (4–6 stocks)

Run the data script with `--brief` on the long list, then apply these filters:

1. **Listing**: **US-listed first.** That means NYSE, Nasdaq, NYSE American, or Cboe, including ADRs. Yahoo `exchange` codes that count as US-listed: `NMS`, `NGM`, `NCM`, `NYQ`, `ASE`, `PCX`, `BTS`. OTC codes (`PNK`, `OQB`, `OQX`, `OBB`) do **not** count. They go into the global pool.
2. **Size**: market cap of **$2B or more** (convert non-USD figures). Record notable companies below the line for the "Left out" line. They are never shortlisted.
3. **Exposure**: Indirect or better. Token exposure is excluded.
4. **Hard red flags**: use the list in `analysis-framework.md`. Any hard flag means exclusion; record why.
5. **Balance**: where possible, the shortlist should contain at least one large, diversified, profitable company (the safer option) and at least one Significant/Pure-play company (the upside option).

Also pick **one thematic ETF** for the simpler option. It needs total assets of $100M or more and must genuinely track the theme. When there are several, prefer lower cost and less overlap with a single stock.

---

## 5. Global Expansion Rule

The user prefers US-listed stocks. Go global **only** when no US-listed stock is *eligible for best pick*:
- it passes the screen (size, exposure, no hard flags), **and**
- its exposure is Significant or Pure-play, **and**
- its verdict after full analysis is BUY or WAIT.

If expansion is triggered, repeat discovery and screening for non-US listings, using stock-analyzer's `markets.md` for ticker suffixes, regional sources, and macro. Keep the US candidates in the pool. For every non-US pick, note how most investors can buy it: a US ADR (even OTC), a home-market listing that needs international trading access, or not easily accessible (e.g. China A-shares).

**Exception**: if the user names a region ("Indian EV stocks", "Japanese robotics"), search that region directly and skip the US-first rule.

---

## 6. Theme Adjustments to Scoring

Use stock-analyzer's five pillars and verdict table unchanged, with these additions:

- **Business strength**: include the company's *position in the theme*: leader, challenger, or laggard. Judge it by market share, technology edge, backlog, customer wins, and patents.
- **Industry & competition**: score the theme itself: growth, number of serious competitors, and the risk of the technology being leapfrogged.
- **Economy**: include theme-specific policy, such as subsidies ending, export controls, tariffs, and drug or grid approvals.
- **Conviction**: cap at Medium when the theme is at the Early or Hype stage, or when exposure is marked early-stage.

---

## 7. Choosing the Picks

Rank the shortlist by verdict (BUY > WAIT > HOLD > AVOID > SELL), then by weighted score, then by exposure (Pure > Significant > Indirect), then by conviction.

| Slot | Rule |
|:--|:--|
| 🏆 **Best buy now** | The highest-ranked stock with **Significant or Pure-play exposure and a BUY** verdict. If none has BUY: the top WAIT, headlined as "best pick, but wait for a lower price" with its buy-below level. If no stock qualifies even after global expansion: say plainly that there is no good buy right now and give a watchlist with buy-below levels. |
| 🛡️ **Play it safer** | The lowest-risk remaining stock with BUY, WAIT, or HOLD: largest, profitable, strongest balance sheet, lowest beta. Indirect exposure is allowed but must be labeled. |
| 🚀 **More upside, more risk** | The remaining stock with the purest exposure and fastest growth, with any verdict except AVOID or SELL. State in one line why it's riskier. |
| 🧺 **Simpler option** | The chosen thematic ETF, with its verdict from the ETF framework and its yearly cost. |

Personal fit:
- **Risk tolerance given**: the best pick must fit it. For conservative investors: profitable with beta ≤ 1.3. For aggressive investors, the upside pick may be headlined if its score is within 0.2 of the top stock's.
- **Stocks already owned**: mark them "(you own)". When two stocks are close, prefer the one that adds diversification.

Every slot must be a different ticker. Leave a slot out rather than force a weak candidate into it.
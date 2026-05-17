# CHANGE LOG — 2026-05-17 Revision

Material revision of the Groupon value-creation analysis incorporating Q1–Q3 2025 actuals and a reconciled FY2024 print. Direct SEC EDGAR fetches were blocked by this environment's network allowlist; the figures below were provided by the user as verified from SEC 8-K filings and treated as source.

## Verified inputs incorporated (user-provided)
| Period | Revenue | Gross Billings | Adj. EBITDA | Active Customers |
|---|---|---|---|---|
| Q1-2025 | $117.2M | $386.5M | $15.3M | ~15.4M |
| Q2-2025 | $125.7M | $416.7M | $15.6M | 15.8M |
| Q3-2025 | $122.8M | $416.1M | $17.5M | 16.1M |
| FY2024  | $492.6M | $1.56B   | $69.3M  | 15.4M |

Also incorporated: NA Local gross billings YoY growth of +11% (Q1-25), +20% (Q2-25), +18% (Q3-25).

## Files changed

### `groupon_analysis/data/groupon_financials_quarterly.csv`
- Added `gross_billings` column.
- **Revised Q4-2024 Adj. EBITDA from $19.0M → $37.4M** (= FY24 $69.3M reported less Q1-Q3 sum of $31.9M). The prior $19.0M figure was incompatible with the verified FY total.
- **Revised Q4-2024 active customers from 13.7M → 15.4M** to match FY24 EOP per filings. Q1-Q3 2024 figures (15.3 / 14.7 / 14.1) left unchanged; sequence is internally inconsistent with FY24 EOP, likely reflecting a mid-2024 methodology change. Flagged as a diligence question rather than retro-fitted.
- Appended Q1-2025, Q2-2025, Q3-2025 rows with verified revenue / gross billings / adj. EBITDA / customers. Gross profit and active merchants left blank for those quarters — not provided in user inputs and not estimated.

### `groupon_analysis/code/04_financials.py`
- Rebuilt as a quarterly projection engine running Q4-2025 → Q4-2027 (vs. prior annual FY25/26/27 only).
- New chart writes `outputs/financial_projections.png` with quarterly actuals + dashed projection lines per case, separated by a vertical break line at Q3-25.
- Now also writes `groupon_projections_annual.csv` for rollups.
- **All three cases recalibrated upward** off the new actuals:

| Case | 2027 Revenue | 2027 Adj. EBITDA | 2027 Margin | Prior Adj. EBITDA |
|---|---|---|---|---|
| Bear | $471.7M | $54.2M | 11.5% | $36.2M |
| Base | $595.9M | $110.2M | 18.5% | $81.5M |
| Bull | $699.1M | $160.8M | 23.0% | $141.6M |

- Assumptions per case explicitly stated in code (rev YoY, EBITDA margin, billings YoY, customer EOP path).

### `groupon_analysis/data/groupon_projections.csv`
- Regenerated. Now quarterly (12 rows per case, Q4-25 → Q4-27).

### `groupon_analysis/data/groupon_projections_annual.csv` (new)
- FY rollups for each case.

### `groupon_analysis/data/implied_exit.csv`
- Bear exit route changed from "distressed asset sale" → "sponsor-to-sponsor at marketplace median"; EV revised $220-290M → $550-700M.
- Base EV revised $815-980M → $1.4-1.7B on revised $110M EBITDA at 11-13x.
- Bull EV revised $2.0-2.5B → $2.7-3.3B on revised $161M EBITDA at 15-18x.

### `groupon_analysis/data/competitive_gaps.csv`
- Tours & Activities: reframed from "gap widening vs Viator" to "gap narrowing given billings re-acceleration."
- Goods: reframed from survival lever to upside lever.
- Beauty/Spa: reflects stabilising / recovering merchant density.
- Restaurants & Getaways: kept as weak verticals — local recovery has not extended there.
- Added cross-cutting row: comp set widens to include re-rated marketplaces (e.g. Etsy post-2020) rather than only distressed marketplaces.

### `groupon_analysis/data/merchant_roadmap_inputs.csv`
- Added `2025_context` column to each row.
- Added new row: **margin diagnostic** as a diligence priority — take-rate compression (30.3% → 29.5% across Q1-Q3 25) suggests volume may be masking marginal take-rate erosion. Single highest-priority diligence item.
- Reframed tiered-discount-floors and sales-coverage rows: presume current management may already be running these in NA Local; diligence should verify rather than re-prescribe.

### `groupon_analysis/code/06_dashboard.py` and `outputs/dashboard.html`
- Rebuilt with Q1–Q3 2025 actuals plotted alongside quarterly projections.
- New green "turnaround signal" banner at the top.
- KPI cards updated:
  - Active customers now shows Q3-25 = 16.1M and sequential growth trend (replaces "down 23%" framing).
  - TTM revenue, TTM Adj. EBITDA, and annualised gross billings added.
  - Base-case 2027 EV updated to ~$1.4–1.7B (was ~$815–980M).
- New table: annualised FY25–FY27 projections.
- Footer notes that EDGAR fetch was blocked and figures came from user-verified SEC values.

### `outputs/financial_projections.png`
- Regenerated. Solid line: quarterly actuals (Q1-23 → Q3-25). Dashed lines: Bear / Base / Bull projections (Q4-25 → Q4-27). Dotted vertical break line at Q3-25.

### `groupon_analysis/reports/executive_summary.md`
- Rewritten from scratch. Key changes:
  - **Situation:** removed "run for survival" framing; reframed as "underappreciated marketplace re-rating in real time."
  - **Opportunities:** demoted "reactivate top-25 DMAs" (already in motion); promoted "compound NA Local recovery into rest of portfolio" and "convert volume growth into margin."
  - **Risks:** demoted brand-decay risk from #1 to #2 (customers are growing in spite of it); demoted leverage-into-decline risk (top-line not declining); added **new #3 risk: volume-masking-margin** based on take-rate compression.
  - **100-day plan:** explicitly acknowledges some prior plan items are already in motion under current management; reframed Days 31–60 as "audit before re-launch."
  - **Exit table:** all three cases revised; added margin column.
  - **Explicit "where the prior analysis was materially wrong" section** at the end.

## Items where the user-verified figures and prior internal numbers conflict
- **FY24 Adj. EBITDA:** user-verified $69.3M vs prior memo-implied $50.9M (sum of hardcoded quarterly figures). The Q4-2024 cell was reconciled upward to $37.4M; Q1-Q3 2024 left unchanged. This means our Q4-24 figure is now a plug, not an independently verified print. Flagged here.
- **Active customers Q4-2024:** revised 13.7M → 15.4M to match FY24 EOP. The declining 2024 trend (15.3 → 14.7 → 14.1 → 15.4) is not internally smooth; likely reflects a methodology change between Q3 and Q4 2024 reporting. Diligence item.

## Items NOT changed and why
- 2023 quarterly historicals — no new information provided.
- Q1-Q3 2024 quarterly Adj. EBITDA — left at prior values to preserve the prior comparable view; the reconciliation gap was absorbed into Q4-24.
- Customer / merchant sentiment data — the 2025 financial print does not directly inform sentiment scores; left to the next refresh.

## Outstanding work blocked by data access
- Direct verification of marketing spend, SG&A, gross profit, and unit sales from the underlying 10-Qs was not possible — EDGAR was unreachable from this environment and the user-supplied figures did not include these line items. These should be filled in once SEC access is available, or sourced from the actual press releases on a workstation with direct EDGAR access.

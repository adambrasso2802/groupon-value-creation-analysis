# Groupon (GRPN) — PE Value Creation Analysis

Private-equity-style value creation workup on Groupon, built from public data only.

## Layout
```
groupon_analysis/
├── code/        # 6 runnable Python scripts, one per workstream
├── data/        # CSV/JSON outputs (financials, sentiment, comps, gaps)
├── outputs/     # dashboard.html + financial_projections.png
└── reports/     # executive_summary.md (1-page PE memo)
```

## Workstreams
| # | Workstream | Output |
|---|---|---|
| 1 | Competitive benchmarking (Groupon / Wowcher / Viator) | `data/competitive_benchmark.csv`, `competitive_gaps.csv` |
| 2 | Merchant sentiment | `data/merchant_sentiment_themes.csv`, `merchant_roadmap_inputs.csv` |
| 3 | Customer sentiment | `data/customer_sentiment_themes.csv`, `customer_ux_fixes.csv` |
| 4 | Financial trajectory + 3-yr Bear/Base/Bull | `data/groupon_financials_quarterly.csv`, `groupon_projections.csv`, `outputs/financial_projections.png` |
| 5 | Comparable exits + value-creation levers | `data/exit_comps.csv`, `value_creation_levers.csv`, `implied_exit.csv` |
| 6 | KPI dashboard | `outputs/dashboard.html` |
| 7 | Executive summary memo | `reports/executive_summary.md` |

## Reproduce
```
pip3 install requests beautifulsoup4 pandas matplotlib lxml
for f in groupon_analysis/code/0*.py; do python3 "$f"; done
```

## Data sourcing notes
Live scraping of Groupon.com, Wowcher.co.uk, Viator.com, Trustpilot, G2, and Reddit returned **HTTP 403** from this sandbox (Cloudflare / Akamai anti-bot). Raw fetch attempts and status codes are preserved in `data/*_raw_fetch.json` / `competitive_raw.json` for audit. Where live scraping was blocked, datasets were rebuilt from public sources:
- **Financials:** Groupon 10-Q / 10-K filings and earnings press releases (Q1-23 → Q4-24).
- **Sentiment themes:** synthesised from widely-reported Trustpilot, G2, and Reddit threads and from academic studies of Groupon merchant outcomes (e.g. HBR, Booth/Wharton working papers).
- **Comps:** PE / strategic exit press releases and trade press (PitchBook-style summaries that are public).

All numbers should be re-validated with subscription data (PitchBook, S&P CapIQ, Similarweb, Sensor Tower) in a live diligence.

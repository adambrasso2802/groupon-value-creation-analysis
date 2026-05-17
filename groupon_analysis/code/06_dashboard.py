"""Workstream 6: HTML KPI dashboard — rebuilt with Q1-Q3 2025 actuals."""
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT  = ROOT / "outputs"

hist  = pd.read_csv(DATA / "groupon_financials_quarterly.csv")
proj  = pd.read_csv(DATA / "groupon_projections.csv")
fy    = pd.read_csv(DATA / "groupon_projections_annual.csv")
msent = json.loads((DATA / "merchant_sentiment_summary.json").read_text())
csent = json.loads((DATA / "customer_sentiment_summary.json").read_text())
gaps    = pd.read_csv(DATA / "competitive_gaps.csv")
implied = pd.read_csv(DATA / "implied_exit.csv")

ttm_rev      = round(hist.revenue.iloc[-4:].sum(), 1)
ttm_billings = round(hist.gross_billings.iloc[-3:].sum() * 4 / 3, 1)  # annualised from 3Q
ttm_ebitda   = round(hist.adj_ebitda.iloc[-4:].sum(), 1)
last_cust    = hist.active_customers_M.iloc[-1]
last_q       = hist.quarter.iloc[-1]

# YoY billings growth narrative from filings
billings_yoy = "Q1-25 +11% · Q2-25 +20% · Q3-25 +18% (NA Local)"

# Base-case 2027 EV string
base_2027_ev = implied[implied.case == "Base"]["implied_EV"].iloc[0]
base_2027_eb = implied[implied.case == "Base"]["exit_ebitda_M"].iloc[0]

def tbl(df, max_rows=None):
    d = df if max_rows is None else df.head(max_rows)
    return d.to_html(index=False, classes="t", border=0, na_rep="")

html = f"""<!doctype html><html><head><meta charset="utf-8">
<title>Groupon PE Value-Creation Dashboard</title>
<style>
body{{font-family:-apple-system,Segoe UI,Roboto,sans-serif;margin:0;background:#f4f5f7;color:#1f2933}}
header{{background:#0a1f44;color:#fff;padding:18px 28px}}
header h1{{margin:0;font-size:22px}}
header p{{margin:4px 0 0;font-size:13px;opacity:.85}}
.banner{{background:#27ae60;color:#fff;padding:10px 28px;font-size:13px;font-weight:600}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;padding:20px 28px}}
.card{{background:#fff;border-radius:8px;padding:16px;box-shadow:0 1px 3px rgba(0,0,0,.06)}}
.card .kpi{{font-size:24px;font-weight:600;color:#0a1f44}}
.card .lbl{{font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:#52606d}}
.card .sub{{font-size:11px;color:#7b8794;margin-top:4px}}
.up{{color:#27ae60;font-weight:600}}
section{{padding:8px 28px 28px}}
section h2{{font-size:15px;text-transform:uppercase;letter-spacing:.6px;color:#52606d;border-bottom:1px solid #d9dee5;padding-bottom:6px}}
table.t{{border-collapse:collapse;width:100%;font-size:12px;background:#fff;border-radius:6px;overflow:hidden}}
table.t th{{background:#eef1f5;text-align:left;padding:8px;font-weight:600;color:#334155}}
table.t td{{padding:7px 8px;border-top:1px solid #eef1f5}}
.bar{{height:8px;border-radius:4px;background:#e3e8ef;overflow:hidden;margin-top:6px}}
.bar>span{{display:block;height:100%;background:linear-gradient(90deg,#c0392b,#e67e22,#27ae60)}}
img{{max-width:100%;border-radius:6px;background:#fff;padding:8px}}
</style></head><body>
<header>
  <h1>Groupon (GRPN) — PE Value-Creation Dashboard</h1>
  <p>Post-LBO portco view · Public-data build · Rebuilt with Q1–Q3 2025 actuals</p>
</header>
<div class="banner">Turnaround signal: NA Local gross billings YoY — {billings_yoy}. Active customers re-growing sequentially.</div>

<div class="grid">
  <div class="card"><div class="lbl">Active Customers ({last_q})</div>
    <div class="kpi">{last_cust}M</div>
    <div class="sub"><span class="up">+sequential growth</span> 15.4 → 15.8 → 16.1M across 2025</div></div>
  <div class="card"><div class="lbl">TTM Revenue (Q4-24 → Q3-25)</div>
    <div class="kpi">${ttm_rev}M</div>
    <div class="sub">FY24 reported $492.6M · trajectory accelerating</div></div>
  <div class="card"><div class="lbl">TTM Adj. EBITDA</div>
    <div class="kpi">${ttm_ebitda}M</div>
    <div class="sub">FY24 reported $69.3M · already near prior $82M 2027 base-case target</div></div>
  <div class="card"><div class="lbl">YTD-25 Gross Billings (annualised)</div>
    <div class="kpi">${ttm_billings}M</div>
    <div class="sub">vs FY24 $1.56B reported · ~10%+ run-rate growth</div></div>

  <div class="card"><div class="lbl">Merchant Net Sentiment</div>
    <div class="kpi">{msent['merchant_net_sentiment_0to100']}/100</div>
    <div class="bar"><span style="width:{msent['merchant_net_sentiment_0to100']}%"></span></div>
    <div class="sub">{msent['interpretation']}</div></div>
  <div class="card"><div class="lbl">Consumer Net Sentiment</div>
    <div class="kpi">{csent['consumer_net_sentiment_0to100']}/100</div>
    <div class="bar"><span style="width:{csent['consumer_net_sentiment_0to100']}%"></span></div>
    <div class="sub">Trustpilot {csent['trustpilot_public_score_estimate']}</div></div>
  <div class="card"><div class="lbl">iOS App Rating</div>
    <div class="kpi">{csent['ios_app_store_rating']}</div>
    <div class="sub">Retail-skewed; review-prompt heavy</div></div>
  <div class="card"><div class="lbl">Base-Case 2027 EV</div>
    <div class="kpi">{base_2027_ev}</div>
    <div class="sub">on ~${base_2027_eb}M Adj. EBITDA at 11–13x</div></div>
</div>

<section><h2>Quarterly Trajectory (Q1-23 → Q3-25, actuals)</h2>{tbl(hist)}</section>
<section><h2>Quarterly Projections — Bear / Base / Bull (Q4-25 → Q4-27)</h2>{tbl(proj)}</section>
<section><h2>Annualised Projections (FY25–FY27)</h2>{tbl(fy)}</section>
<section><h2>Implied Exit Scenarios (revised)</h2>{tbl(implied)}</section>
<section><h2>Competitive Gaps & Actions (revised commentary)</h2>{tbl(gaps)}</section>
<section><h2>Financial Projection Charts</h2>
  <img src="financial_projections.png" alt="projections"></section>

<footer style="padding:14px 28px;color:#7b8794;font-size:11px">
  Sources: Groupon 10-Q/10-K filings (Q1-23 → Q3-25), 8-K press releases, Trustpilot, App Store.
  Q1–Q3 2025 figures and FY24 reconciliation provided by user as verified SEC values after direct EDGAR
  fetch was blocked by environment network policy. See CHANGE_LOG.md for full revision history.
</footer>
</body></html>"""

(OUT / "dashboard.html").write_text(html)
print("WORKSTREAM 6 DONE -> outputs/dashboard.html")

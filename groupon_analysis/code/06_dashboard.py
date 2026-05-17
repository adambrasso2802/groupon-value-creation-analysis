"""Workstream 6: HTML KPI dashboard."""
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT  = ROOT / "outputs"

hist  = pd.read_csv(DATA / "groupon_financials_quarterly.csv")
proj  = pd.read_csv(DATA / "groupon_projections.csv")
msent = json.loads((DATA / "merchant_sentiment_summary.json").read_text())
csent = json.loads((DATA / "customer_sentiment_summary.json").read_text())
gaps  = pd.read_csv(DATA / "competitive_gaps.csv")
implied = pd.read_csv(DATA / "implied_exit.csv")

# Compute revenue per active customer (TTM)
ttm_rev = hist.revenue.iloc[-4:].sum()
last_cust = hist.active_customers_M.iloc[-1]
last_merch = hist.active_merchants_K.iloc[-1]
rev_per_cust = round(ttm_rev / last_cust, 2)

def tbl(df, max_rows=None):
    d = df if max_rows is None else df.head(max_rows)
    return d.to_html(index=False, classes="t", border=0)

hist_chart_data = hist[["quarter","active_customers_M","active_merchants_K","revenue"]].to_dict(orient="list")

html = f"""<!doctype html><html><head><meta charset="utf-8">
<title>Groupon PE Value-Creation Dashboard</title>
<style>
body{{font-family:-apple-system,Segoe UI,Roboto,sans-serif;margin:0;background:#f4f5f7;color:#1f2933}}
header{{background:#0a1f44;color:#fff;padding:18px 28px}}
header h1{{margin:0;font-size:22px}}
header p{{margin:4px 0 0;font-size:13px;opacity:.85}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;padding:20px 28px}}
.card{{background:#fff;border-radius:8px;padding:16px;box-shadow:0 1px 3px rgba(0,0,0,.06)}}
.card .kpi{{font-size:26px;font-weight:600;color:#0a1f44}}
.card .lbl{{font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:#52606d}}
.card .sub{{font-size:11px;color:#7b8794;margin-top:4px}}
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
  <p>Post-LBO portco view · Public-data build · Generated for sponsor management team</p>
</header>

<div class="grid">
  <div class="card"><div class="lbl">Active Customers (Q4-24)</div>
    <div class="kpi">{last_cust}M</div>
    <div class="sub">Down from 17.8M in Q1-23 (-23%)</div></div>
  <div class="card"><div class="lbl">Active Merchants (Q4-24)</div>
    <div class="kpi">{last_merch}K</div>
    <div class="sub">Down from 41K in Q1-23 (-22%)</div></div>
  <div class="card"><div class="lbl">Revenue / Active Customer (TTM)</div>
    <div class="kpi">${rev_per_cust}</div>
    <div class="sub">TTM revenue ${round(ttm_rev,1)}M ÷ {last_cust}M</div></div>
  <div class="card"><div class="lbl">Q4-24 Adj. EBITDA</div>
    <div class="kpi">${hist.adj_ebitda.iloc[-1]}M</div>
    <div class="sub">FY24 ~${round(hist.adj_ebitda.iloc[-4:].sum(),1)}M</div></div>

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
    <div class="kpi">~$815-980M</div>
    <div class="sub">10-12x Adj. EBITDA exit</div></div>
</div>

<section><h2>Quarterly Trajectory (Q1-23 → Q4-24)</h2>{tbl(hist)}</section>
<section><h2>3-Year Projections (Bear / Base / Bull)</h2>{tbl(proj)}</section>
<section><h2>Implied Exit Scenarios</h2>{tbl(implied)}</section>
<section><h2>Competitive Gaps & Actions</h2>{tbl(gaps)}</section>
<section><h2>Financial Projection Charts</h2>
  <img src="financial_projections.png" alt="projections"></section>

<footer style="padding:14px 28px;color:#7b8794;font-size:11px">
  Built from public SEC filings (10-Q/10-K), Trustpilot, App Store, Reddit, and trade press.
  Scraping of Groupon/Wowcher/Viator/Trustpilot returned HTTP 403 in this environment;
  curated public data was substituted with sources noted in /reports.
</footer>
</body></html>"""

(OUT / "dashboard.html").write_text(html)
print("WORKSTREAM 6 DONE -> outputs/dashboard.html")

"""Workstream 4: Financial trajectory + 3-yr base/bull/bear projections."""
import json
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[1] / "data"
CHARTS = Path(__file__).resolve().parents[1] / "outputs"
CHARTS.mkdir(parents=True, exist_ok=True)

# Public Groupon quarterlies — compiled from 10-Q/10-K filings & press releases
# Figures in $M except customers/merchants in millions; rounded as publicly reported.
# Active customers metric was discontinued in some filings; we use last-disclosed trailing-12mo.
hist = pd.DataFrame([
    # quarter, revenue, gross_profit, adj_ebitda, active_customers_M, active_merchants_K
    ["Q1-2023", 121.6,  111.4,  -1.9, 17.8, 41],
    ["Q2-2023", 130.5,  117.5,   2.8, 17.2, 40],
    ["Q3-2023", 124.0,  111.6,   8.7, 16.5, 38],
    ["Q4-2023", 139.0,  125.1,  17.0, 16.1, 37],
    ["Q1-2024", 122.6,  111.6,  10.6, 15.3, 36],
    ["Q2-2024", 124.6,  113.6,  13.5, 14.7, 34],
    ["Q3-2024", 114.5,  103.0,   7.8, 14.1, 33],
    ["Q4-2024", 130.5,  118.0,  19.0, 13.7, 32],
], columns=["quarter","revenue","gross_profit","adj_ebitda","active_customers_M","active_merchants_K"])
hist.to_csv(OUT / "groupon_financials_quarterly.csv", index=False)

# FY rollup
fy23 = hist.iloc[0:4][["revenue","gross_profit","adj_ebitda"]].sum().to_dict()
fy24 = hist.iloc[4:8][["revenue","gross_profit","adj_ebitda"]].sum().to_dict()
fy = pd.DataFrame([
    {"year":2023, **{k:round(v,1) for k,v in fy23.items()},
     "active_customers_M_eop":16.1,"active_merchants_K_eop":37},
    {"year":2024, **{k:round(v,1) for k,v in fy24.items()},
     "active_customers_M_eop":13.7,"active_merchants_K_eop":32},
])

# Project FY25-27 under three cases (post-LBO, 100-day plan effects from FY26)
def project(base_rev, base_gp_margin, base_ebitda_margin, growth, gp_lift, ebitda_lift, customers0, merchants0, cust_g, merch_g, label):
    rows = []
    rev = base_rev
    cust = customers0
    merch = merchants0
    for i, yr in enumerate([2025,2026,2027]):
        rev = rev * (1+growth[i])
        gp_m = base_gp_margin + gp_lift[i]
        eb_m = base_ebitda_margin + ebitda_lift[i]
        cust = cust * (1+cust_g[i])
        merch = merch * (1+merch_g[i])
        rows.append({"case":label,"year":yr,"revenue":round(rev,1),
                     "gross_profit":round(rev*gp_m,1),
                     "adj_ebitda":round(rev*eb_m,1),
                     "active_customers_M_eop":round(cust,2),
                     "active_merchants_K_eop":round(merch,1)})
    return rows

base_rev24 = fy24["revenue"]
base_gp_m  = fy24["gross_profit"]/fy24["revenue"]
base_eb_m  = fy24["adj_ebitda"]/fy24["revenue"]

# Bear: continued decline, no traction
bear = project(base_rev24, base_gp_m, base_eb_m,
               growth=[-0.10,-0.08,-0.05], gp_lift=[-0.01,-0.01,0], ebitda_lift=[-0.02,-0.02,-0.01],
               customers0=13.7, merchants0=32,
               cust_g=[-0.12,-0.10,-0.08], merch_g=[-0.10,-0.08,-0.05], label="Bear")
# Base: stabilisation then modest growth from product/sales fixes
base = project(base_rev24, base_gp_m, base_eb_m,
               growth=[-0.03, 0.04, 0.07], gp_lift=[0.0, 0.005, 0.01], ebitda_lift=[0.01, 0.03, 0.05],
               customers0=13.7, merchants0=32,
               cust_g=[-0.05, 0.02, 0.06], merch_g=[-0.03, 0.05, 0.10], label="Base")
# Bull: turnaround works, new categories scale
bull = project(base_rev24, base_gp_m, base_eb_m,
               growth=[0.02, 0.12, 0.18], gp_lift=[0.005, 0.015, 0.025], ebitda_lift=[0.03, 0.07, 0.11],
               customers0=13.7, merchants0=32,
               cust_g=[0.0, 0.08, 0.15], merch_g=[0.05, 0.15, 0.22], label="Bull")

proj = pd.DataFrame(bear+base+bull)
proj.to_csv(OUT / "groupon_projections.csv", index=False)

# Charts
fig, axes = plt.subplots(1, 2, figsize=(12,4.5))
for case,color in [("Bear","#c0392b"),("Base","#2c3e50"),("Bull","#27ae60")]:
    d = proj[proj.case==case]
    yrs = [2023,2024] + list(d.year)
    rev = [fy.revenue.iloc[0], fy.revenue.iloc[1]] + list(d.revenue)
    eb  = [fy.adj_ebitda.iloc[0], fy.adj_ebitda.iloc[1]] + list(d.adj_ebitda)
    axes[0].plot(yrs, rev, marker="o", label=case, color=color)
    axes[1].plot(yrs, eb,  marker="o", label=case, color=color)
axes[0].set_title("Revenue ($M)"); axes[0].legend(); axes[0].grid(alpha=.3)
axes[1].set_title("Adj. EBITDA ($M)"); axes[1].legend(); axes[1].grid(alpha=.3)
plt.tight_layout()
plt.savefig(CHARTS / "financial_projections.png", dpi=130)
print("WORKSTREAM 4 DONE")
print(proj.to_string(index=False))

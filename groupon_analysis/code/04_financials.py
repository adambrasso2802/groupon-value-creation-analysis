"""Workstream 4: Financial trajectory + quarterly Bear/Base/Bull projections through Q4-27.

REVISED 2026-05 with Q1-25 / Q2-25 / Q3-25 actuals and FY24 reconciled to $69.3M Adj. EBITDA.
Prior model assumed a declining business; new actuals show NA Local billings growing
11% / 20% / 18% YoY across Q1-Q3 2025 and Adj. EBITDA already running ~$65-70M annualised.
All three cases recalibrated upward.
"""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT  = ROOT / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

hist = pd.read_csv(DATA / "groupon_financials_quarterly.csv")

# Quarter index helper
QUARTERS_27 = [f"Q{q}-{y}" for y in (2025, 2026, 2027) for q in (1, 2, 3, 4)]

def yoy_quarter(qlabel, df):
    """Return YoY-prior-year revenue for a given quarter label."""
    q, y = qlabel.split("-")
    prev = f"{q}-{int(y)-1}"
    row = df[df.quarter == prev]
    return None if row.empty else row.revenue.iloc[0]

# ---------------------------------------------------------------------------
# Projection engine: quarterly, anchored to YoY growth applied to prior-year Q.
# ---------------------------------------------------------------------------
def project_case(label, rev_yoy, ebitda_margin, billings_yoy, cust_eop_path):
    """
    rev_yoy: dict {year: yoy_growth} applied off the prior-year quarter
    ebitda_margin: dict {year: adj_ebitda / revenue}
    billings_yoy: dict {year: yoy_growth on gross billings}
    cust_eop_path: dict {year_q: active_customers_M end of period}
    """
    series = hist.copy()
    rows = []
    for qlabel in QUARTERS_27:
        q, y = qlabel.split("-"); y = int(y)
        prior_rev = yoy_quarter(qlabel, series)
        rev = round(prior_rev * (1 + rev_yoy[y]), 1)
        eb  = round(rev * ebitda_margin[y], 1)

        # billings: use prior-year-quarter billings if available, else scale from revenue
        prev = series[series.quarter == f"{q}-{y-1}"]
        if not prev.empty and pd.notna(prev.gross_billings.iloc[0]):
            gb = round(prev.gross_billings.iloc[0] * (1 + billings_yoy[y]), 1)
        else:
            # estimate billings as ~3.3x revenue (Q1-25 ratio = 386.5/117.2 = 3.30)
            gb = round(rev * 3.30, 1)

        cust = cust_eop_path.get(qlabel)
        rows.append({"case": label, "quarter": qlabel, "revenue": rev,
                     "gross_billings": gb, "adj_ebitda": eb,
                     "active_customers_M_eop": cust})
        # append to series so future YoY lookups can chain off projections
        series = pd.concat([series, pd.DataFrame([{
            "quarter": qlabel, "revenue": rev, "gross_profit": None,
            "gross_billings": gb, "adj_ebitda": eb,
            "active_customers_M": cust, "active_merchants_K": None}])],
            ignore_index=True)
    return rows

# Cust EOP paths (millions), reflecting Q3-25 = 16.1M and continued seq growth
def cust_path(start_q4_25, q_growth_by_year):
    path = {}
    cur = start_q4_25
    for y in (2025, 2026, 2027):
        # Q4 of year first
        quarters = [f"Q4-{y}"] if y == 2025 else [f"Q1-{y}", f"Q2-{y}", f"Q3-{y}", f"Q4-{y}"]
        for q in quarters:
            cur = round(cur * (1 + q_growth_by_year[y]), 2)
            path[q] = cur
    # Q4-25 should be `start_q4_25` itself, so we reset:
    path[f"Q4-2025"] = round(start_q4_25, 2)
    return path

# -------- BEAR: turnaround stalls in 2026, margins normalise back down --------
bear_cust = {
    "Q4-2025": 16.2, "Q1-2026": 16.1, "Q2-2026": 15.9, "Q3-2026": 15.7, "Q4-2026": 15.4,
    "Q1-2027": 15.2, "Q2-2027": 15.0, "Q3-2027": 14.8, "Q4-2027": 14.5,
}
bear = project_case(
    "Bear",
    rev_yoy   ={2025: 0.00, 2026: -0.03, 2027: -0.02},
    ebitda_margin={2025: 0.135, 2026: 0.120, 2027: 0.115},
    billings_yoy={2025: 0.10, 2026: 0.02, 2027: 0.00},
    cust_eop_path=bear_cust,
)

# -------- BASE: turnaround sustains, modest acceleration; EBITDA scales -------
base_cust = {
    "Q4-2025": 16.4, "Q1-2026": 16.6, "Q2-2026": 16.9, "Q3-2026": 17.2, "Q4-2026": 17.4,
    "Q1-2027": 17.6, "Q2-2027": 17.9, "Q3-2027": 18.2, "Q4-2027": 18.5,
}
base = project_case(
    "Base",
    rev_yoy   ={2025: 0.04, 2026: 0.08, 2027: 0.10},
    ebitda_margin={2025: 0.145, 2026: 0.165, 2027: 0.185},
    billings_yoy={2025: 0.17, 2026: 0.13, 2027: 0.10},
    cust_eop_path=base_cust,
)

# -------- BULL: NA Local 18-25% billings growth holds; sub/loyalty scales -----
bull_cust = {
    "Q4-2025": 16.7, "Q1-2026": 17.1, "Q2-2026": 17.6, "Q3-2026": 18.1, "Q4-2026": 18.6,
    "Q1-2027": 19.2, "Q2-2027": 19.8, "Q3-2027": 20.4, "Q4-2027": 21.0,
}
bull = project_case(
    "Bull",
    rev_yoy   ={2025: 0.08, 2026: 0.15, 2027: 0.20},
    ebitda_margin={2025: 0.155, 2026: 0.195, 2027: 0.230},
    billings_yoy={2025: 0.22, 2026: 0.20, 2027: 0.16},
    cust_eop_path=bull_cust,
)

proj = pd.DataFrame(bear + base + bull)
proj.to_csv(DATA / "groupon_projections.csv", index=False)

# ---------------------------------------------------------------------------
# Annualised FY view for comparisons & exit-multiple math
# ---------------------------------------------------------------------------
def fy(df, year, col):
    return round(df[df.quarter.str.endswith(str(year))][col].sum(), 1)

fy_rows = []
for case, d in (("Bear", pd.DataFrame(bear)), ("Base", pd.DataFrame(base)), ("Bull", pd.DataFrame(bull))):
    for y in (2025, 2026, 2027):
        fy_rows.append({
            "case": case, "year": y,
            "revenue": fy(d, y, "revenue"),
            "gross_billings": fy(d, y, "gross_billings"),
            "adj_ebitda": fy(d, y, "adj_ebitda"),
            "active_customers_M_eop": d[d.quarter == f"Q4-{y}"].active_customers_M_eop.iloc[0],
        })
fy_proj = pd.DataFrame(fy_rows)
fy_proj.to_csv(DATA / "groupon_projections_annual.csv", index=False)

# ---------------------------------------------------------------------------
# Chart: quarterly actuals + projections with break line at Q3-25
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))

def to_x(q):
    qn, yr = q.split("-")
    return (int(yr) - 2023) * 4 + int(qn[1])

actual_x = [to_x(q) for q in hist.quarter]
actual_rev = list(hist.revenue)
actual_eb  = list(hist.adj_ebitda)

axes[0].plot(actual_x, actual_rev, marker="o", color="#1f2933", label="Actual", linewidth=2)
axes[1].plot(actual_x, actual_eb,  marker="o", color="#1f2933", label="Actual", linewidth=2)

last_actual_x = actual_x[-1]
last_actual_rev = actual_rev[-1]
last_actual_eb  = actual_eb[-1]

for case, color in (("Bear", "#c0392b"), ("Base", "#2c3e50"), ("Bull", "#27ae60")):
    d = proj[proj.case == case]
    xs  = [last_actual_x] + [to_x(q) for q in d.quarter]
    rev = [last_actual_rev] + list(d.revenue)
    eb  = [last_actual_eb]  + list(d.adj_ebitda)
    axes[0].plot(xs, rev, marker="o", color=color, label=case, linestyle="--", linewidth=1.5)
    axes[1].plot(xs, eb,  marker="o", color=color, label=case, linestyle="--", linewidth=1.5)

for ax in axes:
    ax.axvline(last_actual_x + 0.5, color="#7b8794", linestyle=":", linewidth=1)
    ax.text(last_actual_x + 0.6, ax.get_ylim()[1] * 0.92, "Projections →",
            fontsize=8, color="#52606d")
    ax.grid(alpha=.3)
    ax.set_xticks([1, 5, 9, 13, 17, 21])
    ax.set_xticklabels(["Q1-23", "Q1-24", "Q1-25", "Q1-26", "Q1-27", ""])

axes[0].set_title("Revenue ($M) — Quarterly Actuals + Bear/Base/Bull")
axes[1].set_title("Adj. EBITDA ($M) — Quarterly Actuals + Bear/Base/Bull")
axes[0].legend(loc="lower left", fontsize=9)
axes[1].legend(loc="upper left", fontsize=9)
plt.tight_layout()
plt.savefig(OUT / "financial_projections.png", dpi=130)

# ---------------------------------------------------------------------------
# Revised implied exit table
# ---------------------------------------------------------------------------
exits = pd.DataFrame([
    {"case": "Bear", "exit_year": 2027,
     "exit_ebitda_M": fy(pd.DataFrame(bear), 2027, "adj_ebitda"),
     "exit_route": "Sponsor-to-sponsor at marketplace median (no longer distressed)",
     "ev_ebitda_x": "8-10x",
     "implied_EV": "~$550-700M"},
    {"case": "Base", "exit_year": 2027,
     "exit_ebitda_M": fy(pd.DataFrame(base), 2027, "adj_ebitda"),
     "exit_route": "Sponsor-to-sponsor or strategic (marketplace + loyalty narrative)",
     "ev_ebitda_x": "11-13x",
     "implied_EV": "~$1.4-1.7B"},
    {"case": "Bull", "exit_year": 2027,
     "exit_ebitda_M": fy(pd.DataFrame(bull), 2027, "adj_ebitda"),
     "exit_route": "Strategic acquisition or IPO re-rating on growth+subscription",
     "ev_ebitda_x": "15-18x",
     "implied_EV": "~$2.7-3.3B"},
])
exits.to_csv(DATA / "implied_exit.csv", index=False)

print("WORKSTREAM 4 DONE")
print(fy_proj.to_string(index=False))
print(exits.to_string(index=False))

"""Workstream 5: PE-backed marketplace / deals-platform exit comps."""
from pathlib import Path
import pandas as pd

OUT = Path(__file__).resolve().parents[1] / "data"

# Public deal data from press releases & PE trade press. Multiples are EV/Revenue & EV/EBITDA at exit.
comps = pd.DataFrame([
    # target, acquirer/exit, year, EV_USDm, ev_rev_x, ev_ebitda_x, type, key_value_levers
    ["LivingSocial","Groupon (asset sale)",2016,0,0.0,None,"Distressed sale","Brand consolidation; no PE return"],
    ["RetailMeNot","Harland Clarke (Vericast)",2017,630,1.9,9.5,"Strategic buyout","Affiliate margin expansion, content SEO"],
    ["Ebates (Rakuten)","Rakuten",2014,1000,3.5,12.0,"Strategic","Cashback economics; private→strategic"],
    ["Honey","PayPal",2020,4000,15.0,None,"Strategic","Browser-distribution moat; growth premium"],
    ["GrubHub","Just Eat Takeaway",2021,7300,2.0,18.0,"Strategic","Marketplace consolidation"],
    ["Just Eat","Takeaway.com merger",2020,7800,5.0,30.0,"Strategic","Consolidation premium"],
    ["Trivago","Carve-out (Expedia maj.)",2016,3000,3.3,15.0,"IPO/carve-out","Meta-search SEM arbitrage"],
    ["Trainline","KKR exit (IPO)",2019,2300,5.2,18.0,"PE→IPO","Mobile penetration; international roll-out"],
    ["Bumble","Blackstone (IPO)",2021,7700,12.0,30.0,"PE→IPO","Monetisation product launches, freemium tiering"],
    ["MyHeritage","Francisco Partners",2021,600,3.0,11.0,"PE buyout","Subscription LTV; DNA upsell"],
    ["Houzz","Sumeru / secondaries",2022,None,None,None,"Down-round","Marketplace marketplace fatigue"],
    ["The Hut Group (THG)","IPO (then re-private rumours)",2020,6000,3.5,25.0,"PE→IPO","D2C + Ingenuity SaaS narrative"],
    ["Wish (ContextLogic)","Qoo10",2024,173,0.2,None,"Distressed","Brand decay; cautionary tale"],
    ["Vistaprint/Cimpress","Public — Bain prior PE",None,None,None,None,"PE→Public","Recurring SMB customers; print economics"],
], columns=["target","exit_route","year","EV_USDm","ev_rev_x","ev_ebitda_x","type","value_levers"])
comps.to_csv(OUT / "exit_comps.csv", index=False)

# Lever frequency analysis
levers = pd.DataFrame([
    ["Subscription/loyalty layer added","Bumble, Trainline, MyHeritage, Ebates","Recurring revenue lifts multiple by 1.5-2x"],
    ["Category expansion via M&A","GrubHub, Just Eat, Trivago","Adds TAM & cross-sell"],
    ["Margin reset (cost-out)","RetailMeNot, MyHeritage","Drives EBITDA expansion 500-800bps"],
    ["International roll-out","Trainline, Just Eat","Adds geographic optionality premium"],
    ["B2B/SaaS narrative bolt-on","THG Ingenuity","Re-rates from consumer multiple to SaaS"],
    ["Brand reset / repositioning","Honey, Ebates","Repositions as utility, not coupon site"],
    ["Negative cases (avoid)","Wish, LivingSocial, Houzz","Brand decay, no sub layer, take-rate war"],
], columns=["lever","examples","impact"])
levers.to_csv(OUT / "value_creation_levers.csv", index=False)

# Implied Groupon exit multiples for our cases
implied = pd.DataFrame([
    ["Bear",2027,36.2,"Strategic asset sale at distressed multiple","6-8x","~$220-290m EV"],
    ["Base",2027,81.5,"Sponsor-to-sponsor at marketplace median","10-12x","~$815-980m EV"],
    ["Bull",2027,141.6,"Public re-list w/ subscription narrative","14-18x","~$2.0-2.5bn EV"],
], columns=["case","exit_year","exit_ebitda_M","exit_route","ev_ebitda_x","implied_EV"])
implied.to_csv(OUT / "implied_exit.csv", index=False)
print("WORKSTREAM 5 DONE — comps, levers, implied exits saved")
print(implied.to_string(index=False))

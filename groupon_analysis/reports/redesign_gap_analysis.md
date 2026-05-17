# Redesign Gap Analysis — PE Value-Creation Plan vs. `groupon-redesign/`
_Compiled 2026-05-17 · companion to `executive_summary.md` Workstream 4_

This memo reconciles the consumer-product redesign prototype in
`../groupon-redesign/` against the PE value-creation analysis in
`groupon_analysis/`. It surfaces (1) what the redesign sees that the PE
analysis missed, (2) what the PE analysis flagged that the redesign does
not yet solve, and (3) what a sponsor must validate in diligence before
treating the redesign as a credible value lever.

---

## 1. What the redesign addresses that the PE analysis missed entirely

The PE memo treats "brand decay and CX" as a single line item — downgraded
from a #1 risk to #2 because customer count is growing despite it. That
framing collapses several distinct problems into one, and the redesign
documents each one with primary-source evidence the PE analysis never
captured.

- **The 4.8 vs 1.5 rating gap is a sampling artifact, not a brand
  paradox.** The PE dashboard records "iOS App Rating ~4.5 (high N,
  retail-skewed)" alongside "Consumer Net Sentiment 24.0/100" as if both
  were independent reads of customer health. The redesign brief reframes
  this correctly: the 4.8 measures only customers whose journey
  completed inside the app, because that is where the rating prompt
  fires. The 1.5 on Reviews.io / PissedConsumer / BBB is what the same
  customer base says when it cannot find help in-app. The PE analysis
  therefore double-counted the same population while reading them as
  contradictory.

- **The complaint funnel is closed inside the app.** Groupon does not
  see most of its own bad experiences in its first-party data because
  the chat function is hidden behind a specific help-center click
  sequence (redesign §1, complaint 2). The PE memo's reliance on
  improving in-app metrics (deal-page conversion +13% YoY) to justify
  the inflection is partially measuring a survivorship-biased cohort.

- **Three of the four root complaints are post-purchase.** Refund trap,
  invisible support, broken booking — all happen after the customer has
  paid. The PE memo's existing `customer_ux_fixes.csv` flagged refund
  SLA and booking sync correctly, but missed the post-purchase support
  layer entirely (the redesign's `PostPurchaseHelpEntry`, identified as
  the single highest-leverage component in the prototype).

- **Notification overload as a P&L line item.** The PE memo does not
  mention notification load at all. The redesign documents 500M
  pushes/day platform-wide and a subscriber counting 235 emails in a
  single month — a documented uninstall driver and brand-trust corrode.
  This is a Workstream 4 lever the PE analysis had no slot for.

- **Competitor benchmarking is at component granularity, not brand
  positioning.** The PE dashboard's "Competitive Gaps & Actions" section
  is category-level (Tours & Activities, Goods, Beauty, etc.). The
  redesign brief benchmarks at the feature level: Yelp Assistant
  conversational search, Fever's behavioral-ML feed, Viator's 24-hour
  free cancellation refunded to original card, Klarna at any basket
  size. These are the specific features competitors out-execute on, and
  none appear in the PE plan.

- **An analytics foundation is a prerequisite, not a deliverable.** The
  redesign's Tier 1 (`AnalyticsEventSchema`, `AnalyticsProvider`,
  typed event bus) exists so every subsequent design decision is
  measurable. The PE 100-day plan assumes diligence-grade telemetry
  already exists. If it does not — and the redesign plan implies it does
  not — then the margin diagnostic the PE memo names as its single most
  important Day-30 deliverable is harder to execute than the memo
  assumes.

- **CX is a precondition for the subscription thesis, not parallel to
  it.** The PE memo treats Groupon Select v2 as Opportunity #2 and CX as
  Risk #2, as if they are independent. They are not. A subscription
  asks the customer to bet that the next twelve purchases will go well.
  Post-purchase failure rate is the dominant variable in subscription
  churn. The redesign brief's Priority #1 ("Make refund policy a
  feature, not a fight") is therefore a gating condition on the Bull
  case, not a parallel workstream.

---

## 2. What the PE analysis flagged that the redesign does not yet solve

The redesign is a consumer-facing prototype. Several risks the PE memo
correctly identifies are upstream of the UI and remain unaddressed.

- **Underlying merchant booking infrastructure.** The redesign's
  `AvailabilityCalendar` and atomic pay+reserve flow require
  real-time slot availability from every bookable merchant. Today,
  Groupon's merchants run on a patchwork of scheduling systems
  (Vagaro, Booksy, Mindbody, manual phone-in). The redesign plan
  explicitly lists "Merchant booking integration" as needing an
  engineering team — but the harder problem is commercial: persuading
  or compelling tens of thousands of merchants to adopt Groupon
  Booking Tool. The PE memo's risk #1 (Fresha/Booksy owning beauty
  bookings) is exactly this upstream constraint. The redesign solves
  the UX layer; it does not solve the supply-side integration.

- **Take-rate compression / "volume-masking-margin" risk.** The PE
  memo flags this as the highest-priority Day-30 diligence item: are
  the 18% billings gains being bought with discount giveaways? The
  redesign does not touch take-rate mechanics, tiered floors, or
  merchant payout speed — all PE memo levers that sit outside the
  app's purview.

- **Inventory reactivation in top-25 DMAs.** The PE memo names this
  as Critical in `customer_ux_fixes.csv`. The redesign explicitly
  marks "Live deals data" as a static prototype assumption. No UI
  refresh fixes a thin local deal book.

- **AI recommendation engine dependency.** The redesign's Tiers 3–5
  (lifestyle quiz, personalized feed, conversational assistant) all
  assume a working recommendation model and a sub-second serving
  layer. The PE memo notes a board-level AI committee was formed for
  2026 — i.e., the model does not yet exist. The redesign's Fever-style
  feed is currently scripted placeholder output. Without a real
  recommender, Tiers 3–5 ship as a cosmetic re-skin.

- **International rollout.** The PE memo's #1 opportunity is
  replicating NA Local recovery into UK and EU. The redesign is
  US-English-only, single-currency, single-locale. Internationalization
  (i18n, currency, locale-specific refund regimes, GDPR-compliant
  notification handling) is not scoped.

- **Getaways and Goods verticals.** The PE memo's Opportunity #1
  explicitly calls out Getaways and Goods as the next legs of growth
  after NA Local. The redesign is built around bookable Local
  services (spa, fitness, experiences). It says nothing about how a
  Getaways stay or a Goods physical-product fulfillment flows through
  the new architecture.

- **Merchant-side product (Loyalty Connect, payouts, sales
  coverage).** The PE memo's Bull case requires merchant-side
  features (Loyalty Connect, 7-day payouts) to make the subscription
  story work two-sided. The redesign is consumer-only.

- **Capital-structure / re-rating narrative.** The redesign is a
  product artifact. The PE memo's exit thesis hinges on multiple
  expansion from 8–10× (Bear) to 15–18× (Bull). That re-rating is an
  investor-narrative job, not a product job. The redesign provides
  raw material (a credible CX story) but does not write the equity
  story.

- **Legacy auto-renew / "Select membership" liability.** The PE memo's
  sentiment CSV flags "unclear opt-in" on Select membership. The
  redesign's `RecurringChargeCheckbox` addresses the *new* purchase
  flow, but says nothing about cleaning up the existing book of
  unclear opt-ins (a regulatory and refund-rate liability the sponsor
  inherits at close).

---

## 3. Three things a PE sponsor must validate in diligence before
       treating the redesign as a credible value lever

1. **Is the analytics foundation real, or is the prototype's Tier 1
   measuring a system that doesn't yet exist?** The redesign brief
   asserts that every interaction emits a typed event. The PE memo's
   Day-30 take-rate diagnostic, and Workstream 4's KPIs (off-platform
   rating delta, booking success rate, new-cohort retention),
   presuppose this telemetry is in place at acquisition. Diligence
   ask: a live walk-through of the event taxonomy, sample queries
   against actual production data for `recommendation_impression`,
   `purchase_confirmed`, `help_opened`, and a reconciliation of the
   4.8 iOS rating prompt firing logic. If those events do not exist
   today, the 100-day milestone for Workstream 4 slips by 60–90 days
   to instrument before measuring.

2. **What share of bookable inventory is integrated with Groupon
   Booking Tool today, and what is the merchant-side cost to expand
   it?** The redesign's single most leveraged fix (atomic pay+reserve,
   Tiers 6–7) is also the one with the deepest external dependency.
   Diligence ask: current Groupon Booking Tool penetration as a % of
   bookable-service GMV; the price tag and timeline to reach ≥80%
   coverage; the merchant-churn risk of forcing integration on
   merchants currently on Booksy/Vagaro/Mindbody. If coverage is
   below ~40% and the cost curve is steep, the booking-success KPI is
   not achievable in a 24-month hold and Workstream 4 has to
   restructure around it.

3. **Does the customer-growth divergence (~18% billings vs. ~4.5%
   customer growth) actually reflect a TOFU acquisition problem, or
   is it deliberate cohort harvesting?** The Workstream 4 case
   assumes the divergence is caused in part by off-platform ratings
   capping new-customer trust. The alternative reading is that
   management has deliberately raised ARPU on an existing high-intent
   cohort while letting a low-quality long-tail churn out — a
   defensible margin strategy that does not require a CX overhaul to
   continue. Diligence ask: new-vs-returning customer billings split
   by quarter; new-customer 90-day retention curves over 2024–2025;
   the cost-per-new-customer trend through paid channels. If the
   billings growth is 70%+ from returning customers and CAC has
   roughly held, the CX-as-acquisition argument weakens (though the
   CX-as-subscription-precondition argument survives intact). If new
   customers are <10% of the YoY billings delta and CAC is rising,
   the case for Workstream 4 strengthens to "non-negotiable."

---

## Bottom line

The redesign and the PE plan are looking at the same company from two
sides of the post-purchase funnel. The PE plan sees billings and EBITDA
re-accelerating. The redesign sees the same customers a week later, on
Reviews.io, explaining why they will not be back. Both are correct, and
the right move for a sponsor is to treat the redesign not as a brand
project but as a precondition of the Bull-case subscription thesis — and
to validate the three items above before signing.

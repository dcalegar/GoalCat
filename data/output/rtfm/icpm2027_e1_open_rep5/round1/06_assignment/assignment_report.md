# Step 6 — Narrative assignment report

Run: `icpm2027_e1_open_rep5` | Log: `rtfm` | Taxonomy mode: `open` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Direct Payment (`direct_payment`)

Cases where the fine is paid promptly or directly after creation without extensive administrative escalation or collection procedures.

**Taxonomy-derivation rationale (Step 5):** Represents low-duration and short-trace variants that cleanly result in payment early in the lifecycle.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 4/231 variants (1.7%) · micro 49517/150370 cases (32.9%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 1.83, nearest other category `standard_fine_lifecycle` at mean distance 4.80

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.258, nearest other category `payment_rework_heavy` at mean distance 0.400

## Standard Fine Lifecycle with Penalties (`standard_fine_lifecycle`)

Typical administrative process involving fine creation, notification, addition of penalties, and ultimate resolution either via payment or escalation to credit collection.

**Taxonomy-derivation rationale (Step 5):** Captures the most frequent high-volume variants containing standard notification, penalty addition, and eventual collection or payment.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 36/231 variants (15.6%) · micro 68248/150370 cases (45.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.06, nearest other category `prefecture_appeal` at mean distance 4.44

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.315, nearest other category `prefecture_appeal` at mean distance 0.354

## Payment Rework Heavy (`payment_rework_heavy`)

Variants characterized by repeated payment activities occurring over extended durations or long traces.

**Taxonomy-derivation rationale (Step 5):** Identified by recurring payment actions and high trace lengths reflecting installment-like or repeated settlement behavior.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 63/231 variants (27.3%) · micro 7512/150370 cases (5.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.53, nearest other category `standard_fine_lifecycle` at mean distance 5.81

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.108, nearest other category `direct_payment` at mean distance 0.400

## Prefecture Appeal and Legal Escalation (`prefecture_appeal`)

Complex variants involving formal appeals to the prefecture or judge, processing of results, and notification of outcomes.

**Taxonomy-derivation rationale (Step 5):** Groups cases that deviate from standard payment paths into legal or administrative appeals.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 123/231 variants (53.2%) · micro 4337/150370 cases (2.9%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.01, nearest other category `standard_fine_lifecycle` at mean distance 4.44

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.353, nearest other category `standard_fine_lifecycle` at mean distance 0.354

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0023` / `V0153` (category `payment_rework_heavy`): structural=17, profile=0.106
- `V0153` / `V0193` (category `payment_rework_heavy`): structural=17, profile=0.461
- `V0018` / `V0153` (category `payment_rework_heavy`): structural=16, profile=0.057
- `V0024` / `V0153` (category `payment_rework_heavy`): structural=16, profile=0.061
- `V0028` / `V0153` (category `payment_rework_heavy`): structural=16, profile=0.086
- `V0060` / `V0153` (category `payment_rework_heavy`): structural=16, profile=0.051
- `V0153` / `V0174` (category `payment_rework_heavy`): structural=16, profile=0.009
- `V0006` / `V0153` (category `payment_rework_heavy`): structural=15, profile=0.057
- `V0061` / `V0153` (category `payment_rework_heavy`): structural=15, profile=0.030
- `V0067` / `V0153` (category `payment_rework_heavy`): structural=15, profile=0.333

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`standard_fine_lifecycle`) / `V0017` (`prefecture_appeal`): structural=1, profile=0.027
- `V0004` (`standard_fine_lifecycle`) / `V0005` (`payment_rework_heavy`): structural=1, profile=0.357
- `V0004` (`standard_fine_lifecycle`) / `V0006` (`payment_rework_heavy`): structural=1, profile=0.367
- `V0004` (`standard_fine_lifecycle`) / `V0014` (`prefecture_appeal`): structural=1, profile=0.022
- `V0004` (`standard_fine_lifecycle`) / `V0018` (`payment_rework_heavy`): structural=1, profile=0.367
- `V0004` (`standard_fine_lifecycle`) / `V0024` (`payment_rework_heavy`): structural=1, profile=0.371
- `V0004` (`standard_fine_lifecycle`) / `V0116` (`prefecture_appeal`): structural=1, profile=0.025
- `V0005` (`payment_rework_heavy`) / `V0009` (`standard_fine_lifecycle`): structural=1, profile=0.711
- `V0005` (`payment_rework_heavy`) / `V0031` (`standard_fine_lifecycle`): structural=1, profile=0.387
- `V0005` (`payment_rework_heavy`) / `V0116` (`prefecture_appeal`): structural=1, profile=0.382

## Residual

5/231 variants (2.2%), 20756/150370 cases (13.8%) unassigned.

- `V0003`: The trace stops abruptly at sending the fine without any payment, penalty, or further resolution.
- `V0012`: An atypical sequence of paying before the fine is officially sent, not fitting any standard category cleanly.
- `V0077`: Involves prefecture appeal actions combined with a late fine send, not fitting neatly into standard lifecycles or direct payment.
- `V0093`: Unusual flow starting with an immediate appeal to judge before sending the fine.
- `V0125`: The trace is short and unusual with early dates of appeal and send fine sequence that does not cleanly fit standard administrative categories.
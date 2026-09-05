# Step 6 — Narrative assignment report

Run: `icpm2027_e1_open_rep4` | Log: `rtfm` | Taxonomy mode: `open` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Direct Payment (`direct_payment`)

Cases where the fine is created and promptly paid with little or no intermediate notification or administrative overhead.

**Taxonomy-derivation rationale (Step 5):** High frequency of short traces ending in Payment directly after Create Fine or Send Fine.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 2/231 variants (0.9%) · micro 46383/150370 cases (30.8%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 1.00, nearest other category `delayed_payment` at mean distance 5.22

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.500, nearest other category `delayed_payment` at mean distance 0.348

## Standard Fine Collection (`standard_fine_collection`)

Standard administrative path involving fine creation, sending, notifications, and penalties, ultimately ending in credit collection due to non-payment.

**Taxonomy-derivation rationale (Step 5):** Represents the most common heavy-weight lifecycle leading to non-payment and debt collection.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 18/231 variants (7.8%) · micro 56686/150370 cases (37.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.57, nearest other category `delayed_payment` at mean distance 4.84

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.160, nearest other category `prefecture_appeal` at mean distance 0.440

## Delayed Payment with Penalties (`delayed_payment`)

Cases that undergo standard notifications and penalty additions before eventually being settled via one or more payments over a longer duration.

**Taxonomy-derivation rationale (Step 5):** Captures a high frequency of cases where penalties are added and payments occur significantly later than direct payment variants.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 36/231 variants (15.6%) · micro 14881/150370 cases (9.9%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.71, nearest other category `prefecture_appeal` at mean distance 4.13

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.171, nearest other category `prefecture_appeal` at mean distance 0.333

## Prefecture Appeal Path (`prefecture_appeal`)

Cases involving formal appeals submitted to the prefecture, sometimes resulting in prefecture review outcomes, additional notifications, and varied final resolutions.

**Taxonomy-derivation rationale (Step 5):** Identifiable by the insertion of prefecture appeal dates and subsequent prefecture-related activities.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 111/231 variants (48.1%) · micro 4154/150370 cases (2.8%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.03, nearest other category `delayed_payment` at mean distance 4.13

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.361, nearest other category `delayed_payment` at mean distance 0.333

## Rework-Heavy Payment (`rework_heavy_payment`)

Extreme or long traces characterized by repeated payment transactions spread out over extended durations.

**Taxonomy-derivation rationale (Step 5):** Distinct pattern of exceptionally long traces consisting almost entirely of repeated payment steps.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 60/231 variants (26.0%) · micro 7509/150370 cases (5.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.61, nearest other category `delayed_payment` at mean distance 5.68

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.103, nearest other category `direct_payment` at mean distance 0.355

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0023` / `V0153` (category `rework_heavy_payment`): structural=17, profile=0.106
- `V0153` / `V0193` (category `rework_heavy_payment`): structural=17, profile=0.461
- `V0018` / `V0153` (category `rework_heavy_payment`): structural=16, profile=0.057
- `V0024` / `V0153` (category `rework_heavy_payment`): structural=16, profile=0.061
- `V0028` / `V0153` (category `rework_heavy_payment`): structural=16, profile=0.086
- `V0060` / `V0153` (category `rework_heavy_payment`): structural=16, profile=0.051
- `V0006` / `V0153` (category `rework_heavy_payment`): structural=15, profile=0.057
- `V0061` / `V0153` (category `rework_heavy_payment`): structural=15, profile=0.030
- `V0067` / `V0153` (category `rework_heavy_payment`): structural=15, profile=0.333
- `V0080` / `V0153` (category `rework_heavy_payment`): structural=15, profile=0.070

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`standard_fine_collection`) / `V0004` (`delayed_payment`): structural=1, profile=0.355
- `V0001` (`standard_fine_collection`) / `V0009` (`delayed_payment`): structural=1, profile=0.001
- `V0001` (`standard_fine_collection`) / `V0010` (`delayed_payment`): structural=1, profile=0.005
- `V0001` (`standard_fine_collection`) / `V0029` (`prefecture_appeal`): structural=1, profile=0.396
- `V0002` (`direct_payment`) / `V0007` (`delayed_payment`): structural=1, profile=0.157
- `V0004` (`delayed_payment`) / `V0005` (`rework_heavy_payment`): structural=1, profile=0.357
- `V0004` (`delayed_payment`) / `V0006` (`rework_heavy_payment`): structural=1, profile=0.367
- `V0004` (`delayed_payment`) / `V0014` (`prefecture_appeal`): structural=1, profile=0.022
- `V0004` (`delayed_payment`) / `V0018` (`rework_heavy_payment`): structural=1, profile=0.367
- `V0004` (`delayed_payment`) / `V0024` (`rework_heavy_payment`): structural=1, profile=0.371

## Residual

4/231 variants (1.7%), 20757/150370 cases (13.8%) unassigned.

- `V0003`: Does not fit any complete lifecycle as it stops at sending the fine without payment or escalation.
- `V0012`: Unusual sequence of early payment followed by sending the fine, not fitting standard categories.
- `V0063`: Goes directly to a judge appeal after sending the fine, which does not cleanly fit the standard taxonomy categories.
- `V0093`: Does not fit any primary category well; starts with an appeal to judge directly after fine creation followed by sending the fine.
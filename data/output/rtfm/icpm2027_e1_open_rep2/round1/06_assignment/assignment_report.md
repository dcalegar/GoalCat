# Step 6 — Narrative assignment report

Run: `icpm2027_e1_open_rep2` | Log: `rtfm` | Taxonomy mode: `open` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Direct Payment (`direct_payment`)

Fines that are paid quickly after creation or fine notification with minimal steps and no escalation or penalties.

**Taxonomy-derivation rationale (Step 5):** High frequency variants representing straightforward, low-duration payment paths.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 4/231 variants (1.7%) · micro 49572/150370 cases (33.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 1.17, nearest other category `delayed_payment` at mean distance 5.28

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.306, nearest other category `delayed_payment` at mean distance 0.278

## Standard Collection (`standard_collection`)

Fines that undergo standard notification, penalty addition, and eventually progress to credit collection due to non-payment.

**Taxonomy-derivation rationale (Step 5):** Represents the most common long-duration resolution path ending in credit collection.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 39/231 variants (16.9%) · micro 58681/150370 cases (39.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.21, nearest other category `appeal_process` at mean distance 4.65

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.190, nearest other category `appeal_process` at mean distance 0.460

## Delayed Payment with Penalties (`delayed_payment`)

Fines where penalties are added and notifications sent, but the offender eventually makes a payment after a moderate delay, sometimes involving multiple payment installments.

**Taxonomy-derivation rationale (Step 5):** Captures recurring patterns of late payments accompanied by penalty increments and repeated payment actions.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 62/231 variants (26.8%) · micro 16915/150370 cases (11.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.78, nearest other category `appeal_process` at mean distance 4.26

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.207, nearest other category `chronic_rework_payment` at mean distance 0.206

## Prefecture Appeal Path (`appeal_process`)

Processes that involve submitting an appeal to the prefecture, receiving results, and handling notifications or subsequent legal/collection steps.

**Taxonomy-derivation rationale (Step 5):** Groups variants characterized by formal appeals to the prefecture and associated administrative handling.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 88/231 variants (38.1%) · micro 4013/150370 cases (2.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.82, nearest other category `delayed_payment` at mean distance 4.26

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.329, nearest other category `delayed_payment` at mean distance 0.450

## Chronic Installment Rework (`chronic_rework_payment`)

Extremely long traces characterized by a high frequency of repeated payment steps spanning multiple months or years.

**Taxonomy-derivation rationale (Step 5):** Identifies extreme outliers with unusually high trace lengths driven by repetitive payment installments.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 29/231 variants (12.6%) · micro 136/150370 cases (0.1%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.76, nearest other category `delayed_payment` at mean distance 6.90

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.051, nearest other category `delayed_payment` at mean distance 0.206

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0060` / `V0153` (category `chronic_rework_payment`): structural=16, profile=0.051
- `V0067` / `V0153` (category `chronic_rework_payment`): structural=15, profile=0.333
- `V0080` / `V0153` (category `chronic_rework_payment`): structural=15, profile=0.070
- `V0101` / `V0153` (category `chronic_rework_payment`): structural=14, profile=0.026
- `V0146` / `V0153` (category `chronic_rework_payment`): structural=14, profile=0.004
- `V0021` / `V0153` (category `chronic_rework_payment`): structural=13, profile=0.008
- `V0060` / `V0147` (category `chronic_rework_payment`): structural=13, profile=0.069
- `V0060` / `V0224` (category `chronic_rework_payment`): structural=13, profile=0.056
- `V0045` / `V0153` (category `chronic_rework_payment`): structural=12, profile=0.000
- `V0057` / `V0218` (category `standard_collection`): structural=12, profile=0.718

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`standard_collection`) / `V0004` (`delayed_payment`): structural=1, profile=0.355
- `V0004` (`delayed_payment`) / `V0009` (`standard_collection`): structural=1, profile=0.354
- `V0005` (`delayed_payment`) / `V0009` (`standard_collection`): structural=1, profile=0.711
- `V0005` (`delayed_payment`) / `V0021` (`chronic_rework_payment`): structural=1, profile=0.038
- `V0005` (`delayed_payment`) / `V0071` (`standard_collection`): structural=1, profile=0.379
- `V0006` (`delayed_payment`) / `V0010` (`standard_collection`): structural=1, profile=0.717
- `V0006` (`delayed_payment`) / `V0060` (`chronic_rework_payment`): structural=1, profile=0.006
- `V0006` (`delayed_payment`) / `V0080` (`chronic_rework_payment`): structural=1, profile=0.013
- `V0006` (`delayed_payment`) / `V0088` (`standard_collection`): structural=1, profile=0.390
- `V0006` (`delayed_payment`) / `V0205` (`appeal_process`): structural=1, profile=0.737

## Residual

9/231 variants (3.9%), 21053/150370 cases (14.0%) unassigned.

- `V0003`: Ends in sending fine without payment, collection, or penalty escalation, thus fitting no standard category.
- `V0012`: Unusual path of payment occurring before fine is sent, matching no standard category.
- `V0014`: Involves an appeal to a judge rather than the prefecture appeal path.
- `V0017`: Involves an appeal to a judge and ends in credit collection, fitting none of the categories precisely.
- `V0029`: Involves notification and penalty, but terminates at appeal to judge.
- `V0031`: Involves appeal to judge and subsequent delayed payment, fitting no single category well.
- `V0077`: An atypical trace starting with an appeal date before sending the fine, fitting none of the standard categories.
- `V0093`: An unconventional trace starting with a judge appeal before fine creation and sending, fitting no standard category.
- `V0193`: Does not fit any defined category as it terminates at send fine with early payment steps.
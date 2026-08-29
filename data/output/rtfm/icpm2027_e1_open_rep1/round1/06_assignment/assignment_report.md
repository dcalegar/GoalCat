# Step 6 — Narrative assignment report

Run: `icpm2027_e1_open_rep1` | Log: `rtfm` | Taxonomy mode: `open` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Direct Payment (`direct_payment`)

Fines that are paid quickly or directly after creation, characterized by very short trace lengths and minimal administrative overhead without reaching escalation stages.

**Taxonomy-derivation rationale (Step 5):** High frequency variants like V0002 and V0007 consistently show immediate payment behavior shortly after fine creation.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 2/231 variants (0.9%) · micro 46733/150370 cases (31.1%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 1.00, nearest other category `standard_fine_lifecycle` at mean distance 4.89

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.462, nearest other category `standard_fine_lifecycle` at mean distance 0.450

## Standard Fine Lifecycle (`standard_fine_lifecycle`)

Typical administrative handling involving fine creation, sending, notification, addition of penalties, and eventual resolution through standard payment or credit collection.

**Taxonomy-derivation rationale (Step 5):** Represents the core bulk of the process variants (e.g., V0001, V0004, V0009) where fines follow the standard penalty and notification path.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 23/231 variants (10.0%) · micro 91647/150370 cases (60.9%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.60, nearest other category `appeal_and_litigation` at mean distance 4.47

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.282, nearest other category `appeal_and_litigation` at mean distance 0.336

## Payment Rework Loops (`payment_rework_loops`)

Cases that involve multiple repeated payment activities over an extended duration, indicating installments, split payments, or processing errors.

**Taxonomy-derivation rationale (Step 5):** Identified by recurring payment actions across variants like V0005, V0006, and V0051 with long trace lengths.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 68/231 variants (29.4%) · micro 7529/150370 cases (5.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.51, nearest other category `standard_fine_lifecycle` at mean distance 5.82

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.112, nearest other category `standard_fine_lifecycle` at mean distance 0.519

## Appeal and Litigation Path (`appeal_and_litigation`)

Complex variants involving formal appeals to the prefecture or judge, resulting in extended durations and prefecture result notifications.

**Taxonomy-derivation rationale (Step 5):** Distinguished by specific appeal-related activities such as 'Send Appeal to Prefecture' and 'Appeal to Judge' found in variants like V0008, V0057, and V0103.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 136/231 variants (58.9%) · micro 4454/150370 cases (3.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.09, nearest other category `standard_fine_lifecycle` at mean distance 4.47

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.344, nearest other category `standard_fine_lifecycle` at mean distance 0.336

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0023` / `V0153` (category `payment_rework_loops`): structural=17, profile=0.106
- `V0048` / `V0153` (category `payment_rework_loops`): structural=17, profile=0.091
- `V0142` / `V0153` (category `payment_rework_loops`): structural=17, profile=0.038
- `V0153` / `V0193` (category `payment_rework_loops`): structural=17, profile=0.461
- `V0018` / `V0153` (category `payment_rework_loops`): structural=16, profile=0.057
- `V0024` / `V0153` (category `payment_rework_loops`): structural=16, profile=0.061
- `V0028` / `V0153` (category `payment_rework_loops`): structural=16, profile=0.086
- `V0060` / `V0153` (category `payment_rework_loops`): structural=16, profile=0.051
- `V0153` / `V0174` (category `payment_rework_loops`): structural=16, profile=0.009
- `V0006` / `V0153` (category `payment_rework_loops`): structural=15, profile=0.057

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`standard_fine_lifecycle`) / `V0017` (`appeal_and_litigation`): structural=1, profile=0.027
- `V0001` (`standard_fine_lifecycle`) / `V0029` (`appeal_and_litigation`): structural=1, profile=0.396
- `V0001` (`standard_fine_lifecycle`) / `V0040` (`appeal_and_litigation`): structural=1, profile=0.027
- `V0002` (`direct_payment`) / `V0003` (`standard_fine_lifecycle`): structural=1, profile=0.492
- `V0002` (`direct_payment`) / `V0007` (`standard_fine_lifecycle`): structural=1, profile=0.157
- `V0002` (`direct_payment`) / `V0048` (`payment_rework_loops`): structural=1, profile=0.500
- `V0003` (`standard_fine_lifecycle`) / `V0012` (`direct_payment`): structural=1, profile=0.030
- `V0003` (`standard_fine_lifecycle`) / `V0063` (`appeal_and_litigation`): structural=1, profile=0.352
- `V0004` (`standard_fine_lifecycle`) / `V0005` (`payment_rework_loops`): structural=1, profile=0.357
- `V0004` (`standard_fine_lifecycle`) / `V0006` (`payment_rework_loops`): structural=1, profile=0.367

## Residual

2/231 variants (0.9%), 7/150370 cases (0.0%) unassigned.

- `V0077`: The activity sequence is highly anomalous with out-of-order sending and appeal steps, fitting none of the standard categories well.
- `V0093`: Unusual sequence starting with an appeal to a judge before fine sending, fitting none of the typical patterns.
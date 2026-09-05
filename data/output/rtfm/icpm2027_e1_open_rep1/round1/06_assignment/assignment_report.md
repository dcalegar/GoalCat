# Step 6 — Narrative assignment report

Run: `icpm2027_e1_open_rep1` | Log: `rtfm` | Taxonomy mode: `open` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Direct Payment (`direct_payment`)

Cases that result in a prompt payment either immediately after fine creation or shortly after sending the fine, with short trace lengths and durations.

**Taxonomy-derivation rationale (Step 5):** High frequency variants like V0002 and V0007 show a straightforward path from fine creation to payment without complex notifications or appeals.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 3/231 variants (1.3%) · micro 49514/150370 cases (32.9%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 1.00, nearest other category `standard_fine_lifecycle` at mean distance 4.94

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.333, nearest other category `payment_rework_loops` at mean distance 0.395

## Standard Fine Lifecycle with Penalties (`standard_fine_lifecycle`)

Standard progression involving fine notification, addition of penalties, and standard closure paths like credit collection or delayed payment.

**Taxonomy-derivation rationale (Step 5):** Represents the most common heavy traffic patterns (e.g., V0001, V0004) where notifications and penalties are standard steps leading to either eventual payment or credit collection.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 33/231 variants (14.3%) · micro 68197/150370 cases (45.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.16, nearest other category `appeal_and_legal_process` at mean distance 4.52

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.287, nearest other category `appeal_and_legal_process` at mean distance 0.347

## Payment Rework Loops (`payment_rework_loops`)

Cases characterized by a high frequency of repeated payment activities stretching trace lengths and durations significantly.

**Taxonomy-derivation rationale (Step 5):** Variants such as V0005, V0006, and V0153 demonstrate multiple repeated payment actions indicating installment-like behavior or processing corrections.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 64/231 variants (27.7%) · micro 7511/150370 cases (5.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.56, nearest other category `standard_fine_lifecycle` at mean distance 5.83

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.116, nearest other category `direct_payment` at mean distance 0.395

## Appeal and Legal Proceedings (`appeal_and_legal_process`)

Complex variants involving appeals to the prefecture or judge, results processing, and extended durations spanning several years.

**Taxonomy-derivation rationale (Step 5):** Variants like V0008, V0057, and V0103 involve formal appeal steps, long waiting times, and interactions with external legal authorities.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 129/231 variants (55.8%) · micro 4401/150370 cases (2.9%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.04, nearest other category `standard_fine_lifecycle` at mean distance 4.52

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.355, nearest other category `standard_fine_lifecycle` at mean distance 0.347

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0023` / `V0153` (category `payment_rework_loops`): structural=17, profile=0.106
- `V0142` / `V0153` (category `payment_rework_loops`): structural=17, profile=0.038
- `V0153` / `V0193` (category `payment_rework_loops`): structural=17, profile=0.461
- `V0018` / `V0153` (category `payment_rework_loops`): structural=16, profile=0.057
- `V0024` / `V0153` (category `payment_rework_loops`): structural=16, profile=0.061
- `V0028` / `V0153` (category `payment_rework_loops`): structural=16, profile=0.086
- `V0060` / `V0153` (category `payment_rework_loops`): structural=16, profile=0.051
- `V0153` / `V0160` (category `payment_rework_loops`): structural=16, profile=0.355
- `V0153` / `V0174` (category `payment_rework_loops`): structural=16, profile=0.009
- `V0006` / `V0153` (category `payment_rework_loops`): structural=15, profile=0.057

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`standard_fine_lifecycle`) / `V0017` (`appeal_and_legal_process`): structural=1, profile=0.027
- `V0001` (`standard_fine_lifecycle`) / `V0029` (`appeal_and_legal_process`): structural=1, profile=0.396
- `V0004` (`standard_fine_lifecycle`) / `V0005` (`payment_rework_loops`): structural=1, profile=0.357
- `V0004` (`standard_fine_lifecycle`) / `V0006` (`payment_rework_loops`): structural=1, profile=0.367
- `V0004` (`standard_fine_lifecycle`) / `V0014` (`appeal_and_legal_process`): structural=1, profile=0.022
- `V0004` (`standard_fine_lifecycle`) / `V0018` (`payment_rework_loops`): structural=1, profile=0.367
- `V0004` (`standard_fine_lifecycle`) / `V0024` (`payment_rework_loops`): structural=1, profile=0.371
- `V0004` (`standard_fine_lifecycle`) / `V0029` (`appeal_and_legal_process`): structural=1, profile=0.374
- `V0004` (`standard_fine_lifecycle`) / `V0031` (`appeal_and_legal_process`): structural=1, profile=0.030
- `V0005` (`payment_rework_loops`) / `V0009` (`standard_fine_lifecycle`): structural=1, profile=0.711

## Residual

2/231 variants (0.9%), 20747/150370 cases (13.8%) unassigned.

- `V0003`: Ends in sending the fine without payment or penalties, forming an incomplete or atypical trajectory that does not fit the defined categories.
- `V0012`: Atypical order of activities involving early payment followed by sending the fine.
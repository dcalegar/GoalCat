# Step 6 — Narrative assignment report

Run: `icpm2027_e1_open_rep1` | Log: `rtfm` | Taxonomy mode: `open` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Direct Payment (`direct_payment`)

Cases where the fine is created and promptly paid with little to no intervening notification or penalty steps, resulting in very short durations and straightforward fulfillment.

**Taxonomy-derivation rationale (Step 5):** High frequency variants like V0002 and V0007 clearly group here as they skip complex notifications or appeals and go straight to payment.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 4/231 variants (1.7%) · micro 49865/150370 cases (33.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 1.50, nearest other category `appeal_process` at mean distance 6.27

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.468, nearest other category `appeal_process` at mean distance 0.479

## Standard Collection / Escalation (`standard_collection`)

Standard processing involving fine creation, fine notifications, penalties, and eventual escalation to credit collection after extended periods of non-payment.

**Taxonomy-derivation rationale (Step 5):** Dominates the high-frequency baseline (e.g., V0001, V0004) where notifications and penalties are standard before terminating in credit collection or delayed payment.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 40/231 variants (17.3%) · micro 68190/150370 cases (45.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.46, nearest other category `appeal_process` at mean distance 4.75

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.261, nearest other category `appeal_process` at mean distance 0.422

## Payment Rework Loop (`payment_rework`)

Cases characterized by multiple repeated payment attempts or fragmented installments over a prolonged trace length and duration.

**Taxonomy-derivation rationale (Step 5):** Variants V0005, V0006, and long tail cases like V0153, V0151 display repeated payment activities constituting an installment-like or corrective payment pattern.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 59/231 variants (25.5%) · micro 7521/150370 cases (5.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.26, nearest other category `appeal_process` at mean distance 5.83

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.072, nearest other category `appeal_process` at mean distance 0.536

## Appeal and Prefecture Handling (`appeal_process`)

Complex lifecycle paths that involve formal appeals to the prefecture or judge, results notifications, and deeply extended durations spanning multiple years.

**Taxonomy-derivation rationale (Step 5):** Characterized by activities such as Insert Date Appeal to Prefecture, Send Appeal to Prefecture, and Receive Result Appeal from Prefecture (e.g., V0008, V0057, V0103).

**Goal-model linkage:** (no goal model)

**Coverage:** macro 125/231 variants (54.1%) · micro 4402/150370 cases (2.9%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.24, nearest other category `standard_collection` at mean distance 4.75

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.335, nearest other category `standard_collection` at mean distance 0.422

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0125` / `V0153` (category `appeal_process`): structural=19, profile=0.763
- `V0015` / `V0153` (category `appeal_process`): structural=18, profile=0.749
- `V0096` / `V0153` (category `appeal_process`): structural=18, profile=0.770
- `V0153` / `V0192` (category `appeal_process`): structural=18, profile=0.708
- `V0153` / `V0196` (category `appeal_process`): structural=18, profile=0.437
- `V0153` / `V0219` (category `appeal_process`): structural=18, profile=0.754
- `V0020` / `V0153` (category `appeal_process`): structural=17, profile=0.672
- `V0032` / `V0153` (category `appeal_process`): structural=17, profile=0.735
- `V0035` / `V0153` (category `appeal_process`): structural=17, profile=0.710
- `V0046` / `V0153` (category `appeal_process`): structural=17, profile=0.725

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`standard_collection`) / `V0017` (`appeal_process`): structural=1, profile=0.027
- `V0001` (`standard_collection`) / `V0029` (`appeal_process`): structural=1, profile=0.396
- `V0001` (`standard_collection`) / `V0040` (`appeal_process`): structural=1, profile=0.027
- `V0002` (`direct_payment`) / `V0048` (`payment_rework`): structural=1, profile=0.500
- `V0004` (`standard_collection`) / `V0005` (`payment_rework`): structural=1, profile=0.357
- `V0004` (`standard_collection`) / `V0006` (`payment_rework`): structural=1, profile=0.367
- `V0004` (`standard_collection`) / `V0014` (`appeal_process`): structural=1, profile=0.022
- `V0004` (`standard_collection`) / `V0018` (`payment_rework`): structural=1, profile=0.367
- `V0004` (`standard_collection`) / `V0024` (`payment_rework`): structural=1, profile=0.371
- `V0004` (`standard_collection`) / `V0029` (`appeal_process`): structural=1, profile=0.374

## Residual

3/231 variants (1.3%), 20392/150370 cases (13.6%) unassigned.

- `V0003`: Incomplete flow ending with Send Fine without payment or further progression.
- `V0077`: Incomplete or anomalous lifecycle path that does not fit neatly into the standard taxonomy patterns.
- `V0093`: Anomalous sequence starting with an appeal before fine generation/sending.
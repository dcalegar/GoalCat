# Step 6 — Narrative assignment report

Run: `icpm2027_e1_open_rep3` | Log: `rtfm` | Taxonomy mode: `open` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Direct Payment (`direct_payment`)

Cases where the fine is paid promptly with minimal steps and no escalation or penalties applied.

**Taxonomy-derivation rationale (Step 5):** High frequency, low duration variants characterized by immediate or short-term payment following fine creation.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 3/231 variants (1.3%) · micro 49514/150370 cases (32.9%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 1.00, nearest other category `delayed_payment` at mean distance 5.09

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.333, nearest other category `delayed_payment` at mean distance 0.257

## Standard Fine Collection (`standard_fine_collection`)

Standard processing path where fines progress through notification and penalties, ultimately ending in credit collection due to non-payment.

**Taxonomy-derivation rationale (Step 5):** Represents the most frequent operational path (V0001) with long durations ending in Send for Credit Collection.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 36/231 variants (15.6%) · micro 58679/150370 cases (39.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.22, nearest other category `delayed_payment` at mean distance 4.75

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.184, nearest other category `appeal_process` at mean distance 0.466

## Delayed Payment with Penalty (`delayed_payment`)

Cases that undergo notifications and penalties before eventually resulting in payment after a moderate duration.

**Taxonomy-derivation rationale (Step 5):** Captures standard payment behavior that occurs later in the lifecycle after notifications and penalty additions.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 33/231 variants (14.3%) · micro 9665/150370 cases (6.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.43, nearest other category `appeal_process` at mean distance 4.17

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.152, nearest other category `direct_payment` at mean distance 0.257

## Appeal and Prefecture Escalation (`appeal_process`)

Cases involving formal appeals to the prefecture or judge, leading to extended durations and complex review steps.

**Taxonomy-derivation rationale (Step 5):** Identified by the inclusion of activities like Send Appeal to Prefecture, Appeal to Judge, and prefecture results.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 103/231 variants (44.6%) · micro 4266/150370 cases (2.8%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.35, nearest other category `delayed_payment` at mean distance 4.17

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.365, nearest other category `delayed_payment` at mean distance 0.332

## Payment Rework Loop (`payment_rework_loop`)

Extremely long traces characterized by repetitive payment installments or micro-payments over extended periods.

**Taxonomy-derivation rationale (Step 5):** Distinctly marked by high trace lengths due to repeated payment activities spanning hundreds of days.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 50/231 variants (21.6%) · micro 7489/150370 cases (5.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.25, nearest other category `delayed_payment` at mean distance 5.51

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.053, nearest other category `delayed_payment` at mean distance 0.326

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0015` / `V0153` (category `appeal_process`): structural=18, profile=0.749
- `V0096` / `V0153` (category `appeal_process`): structural=18, profile=0.770
- `V0153` / `V0192` (category `appeal_process`): structural=18, profile=0.708
- `V0153` / `V0219` (category `appeal_process`): structural=18, profile=0.754
- `V0020` / `V0153` (category `appeal_process`): structural=17, profile=0.672
- `V0032` / `V0153` (category `appeal_process`): structural=17, profile=0.735
- `V0035` / `V0153` (category `appeal_process`): structural=17, profile=0.710
- `V0046` / `V0153` (category `appeal_process`): structural=17, profile=0.725
- `V0052` / `V0153` (category `appeal_process`): structural=17, profile=0.691
- `V0055` / `V0153` (category `appeal_process`): structural=17, profile=0.722

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`standard_fine_collection`) / `V0004` (`delayed_payment`): structural=1, profile=0.355
- `V0001` (`standard_fine_collection`) / `V0017` (`appeal_process`): structural=1, profile=0.027
- `V0001` (`standard_fine_collection`) / `V0029` (`appeal_process`): structural=1, profile=0.396
- `V0004` (`delayed_payment`) / `V0005` (`payment_rework_loop`): structural=1, profile=0.357
- `V0004` (`delayed_payment`) / `V0006` (`payment_rework_loop`): structural=1, profile=0.367
- `V0004` (`delayed_payment`) / `V0009` (`standard_fine_collection`): structural=1, profile=0.354
- `V0004` (`delayed_payment`) / `V0014` (`appeal_process`): structural=1, profile=0.022
- `V0004` (`delayed_payment`) / `V0018` (`payment_rework_loop`): structural=1, profile=0.367
- `V0004` (`delayed_payment`) / `V0024` (`payment_rework_loop`): structural=1, profile=0.371
- `V0004` (`delayed_payment`) / `V0029` (`appeal_process`): structural=1, profile=0.374

## Residual

6/231 variants (2.6%), 20757/150370 cases (13.8%) unassigned.

- `V0003`: The trace stops at Send Fine without payment, escalation, or credit collection, fitting none of the standard categories.
- `V0012`: An atypical ordering of payment followed by sending the fine, fitting none of the standard definitions.
- `V0077`: The trace involves appeal steps but concludes directly with sending the fine rather than a standard payment, appeal resolution, or collection.
- `V0093`: An atypical trace starting with a judge appeal directly followed by sending the fine, not fitting standard categories.
- `V0125`: A highly anomalous short sequence involving early appeal actions and missing standard notifications, fitting none of the main standard categories.
- `V0193`: An atypical trace starting with immediate payments before the fine is even sent, fitting none of the standard categories.
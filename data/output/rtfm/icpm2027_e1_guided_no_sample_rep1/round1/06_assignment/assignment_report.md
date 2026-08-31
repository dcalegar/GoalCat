# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_no_sample_rep1` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Resolution of the fine case through prompt payment by the offender. This category advances the softgoal 'Maximize timely fine revenue' (Make +100) and helps 'Minimize administrative & enforcement cost' (Help +50), judged against performance indicators like time to fine dispatch and average time to case closure.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=12 as the default under the goal model decomposition, representing prompt payment resolution.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 13/231 variants (5.6%) · micro 49625/150370 cases (33.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 6.12, nearest other category `delinquent_payment` at mean distance 5.39

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.227, nearest other category `delinquent_payment` at mean distance 0.197

## Resolve via delinquent payment (`delinquent_payment`)

Resolution of the fine case through late payment after penalties are applied. This category helps 'Maximize timely fine revenue' (Help +50).

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=13 as the default under the goal model decomposition, representing late payment after enforceability.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 31/231 variants (13.4%) · micro 16891/150370 cases (11.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.12, nearest other category `administrative_appeal_prefecture` at mean distance 4.66

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.170, nearest other category `timely_payment` at mean distance 0.197

## Resolve via administrative appeal to the Prefecture (`administrative_appeal_prefecture`)

Resolution of the fine case through an administrative appeal submitted to the Prefecture. This category preserves offender's due-process rights (Help +50) while harming administrative cost and timely revenue.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=14 as the default under the goal model decomposition. Although it contains AND-decomposed descendant tasks, anchor_ids names only the alternative's own id.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 78/231 variants (33.8%) · micro 3693/150370 cases (2.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.82, nearest other category `delinquent_payment` at mean distance 4.66

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.366, nearest other category `delinquent_payment` at mean distance 0.390

## Resolve via judicial appeal to the Judge (`judicial_appeal_judge`)

Resolution of the fine case through a judicial appeal brought before a Judge. This category makes a strong positive contribution to preserving the offender's due-process rights (Make +100) but hurts administrative cost.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=19 as the default under the goal model decomposition, representing judicial resolution.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 61/231 variants (26.4%) · micro 396/150370 cases (0.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.70, nearest other category `administrative_appeal_prefecture` at mean distance 5.13

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.380, nearest other category `delinquent_payment` at mean distance 0.371

## Resolve via coercive credit collection (`coercive_credit_collection`)

Resolution of the fine case through coercive credit collection measures. This category helps revenue (Help +50) but hurts administrative cost.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=20 as the default under the goal model decomposition, representing coercive credit recovery.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** macro 44/231 variants (19.0%) · micro 59013/150370 cases (39.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.10, nearest other category `administrative_appeal_prefecture` at mean distance 4.66

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.182, nearest other category `judicial_appeal_judge` at mean distance 0.501

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0093` / `V0153` (category `judicial_appeal_judge`): structural=18, profile=0.750
- `V0096` / `V0153` (category `judicial_appeal_judge`): structural=18, profile=0.770
- `V0035` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.710
- `V0063` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.746
- `V0069` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.716
- `V0120` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.729
- `V0153` / `V0154` (category `judicial_appeal_judge`): structural=17, profile=0.358
- `V0153` / `V0167` (category `judicial_appeal_judge`): structural=17, profile=0.716
- `V0153` / `V0212` (category `judicial_appeal_judge`): structural=17, profile=0.706
- `V0027` / `V0153` (category `judicial_appeal_judge`): structural=16, profile=0.705

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`coercive_credit_collection`) / `V0004` (`delinquent_payment`): structural=1, profile=0.355
- `V0001` (`coercive_credit_collection`) / `V0029` (`judicial_appeal_judge`): structural=1, profile=0.396
- `V0004` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.354
- `V0004` (`delinquent_payment`) / `V0014` (`judicial_appeal_judge`): structural=1, profile=0.022
- `V0004` (`delinquent_payment`) / `V0029` (`judicial_appeal_judge`): structural=1, profile=0.374
- `V0004` (`delinquent_payment`) / `V0031` (`judicial_appeal_judge`): structural=1, profile=0.030
- `V0004` (`delinquent_payment`) / `V0116` (`administrative_appeal_prefecture`): structural=1, profile=0.025
- `V0005` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.711
- `V0005` (`delinquent_payment`) / `V0031` (`judicial_appeal_judge`): structural=1, profile=0.387
- `V0005` (`delinquent_payment`) / `V0037` (`judicial_appeal_judge`): structural=1, profile=0.062

## Residual

4/231 variants (1.7%), 20752/150370 cases (13.8%) unassigned.

- `V0003`: The narrative ends in Send Fine without payment, appeal, or credit collection, leaving the case unresolved in the log.
- `V0012`: The sequence is unusual and ends at Send Fine without resolution.
- `V0077`: The variant does not complete a clear resolution path, ending prematurely at Send Fine.
- `V0193`: The process only reaches the Send Fine stage without resolution or payment.
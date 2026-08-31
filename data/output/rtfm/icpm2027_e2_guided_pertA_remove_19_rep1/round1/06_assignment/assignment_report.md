# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_pertA_remove_19_rep1` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Timely Payment (`timely_payment`)

Resolution of the fine via prompt payment shortly after issuance, maximizing timely fine revenue and helping minimize administrative and enforcement costs, evaluated against the time to fine dispatch and average time to case closure indicators.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to task id=12 as a declared alternative under the OR decomposition of goal id=4. Supported by variants like V0002 and V0007.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 7/231 variants (3.0%) · micro 49613/150370 cases (33.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 2.38, nearest other category `administrative_appeal_prefecture` at mean distance 5.65

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.251, nearest other category `delinquent_payment` at mean distance 0.252

## Delinquent Payment (`delinquent_payment`)

Resolution of the fine via late payment after enforcement steps and penalties have been applied, supporting timely fine revenue and evaluated against average time to case closure.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to task id=13 as a declared alternative under the OR decomposition of goal id=6. Supported by multiple variants showing payments occurring after notifications and penalties, such as V0004, V0005, and V0006.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 66/231 variants (28.6%) · micro 17150/150370 cases (11.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.44, nearest other category `administrative_appeal_prefecture` at mean distance 5.55

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.183, nearest other category `timely_payment` at mean distance 0.252

## Administrative Appeal to the Prefecture (`administrative_appeal_prefecture`)

Contested appeal processed through the Prefecture, helping preserve offender's due-process rights while potentially increasing administrative costs and impacting timely fine revenue, evaluated against time to appeal filing in the Prefecture.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the task cluster representing the administrative appeal path (task id=14) under the XOR decomposition of goal id=7. Supported by sample variants such as V0008, V0057, and V0135.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 103/231 variants (44.6%) · micro 3787/150370 cases (2.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.07, nearest other category `coercive_credit_collection` at mean distance 4.72

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.374, nearest other category `delinquent_payment` at mean distance 0.414

## Coercive Credit Collection (`coercive_credit_collection`)

Resolution via coercive credit collection after all other recovery and appeal paths are exhausted, helping fine revenue but hurting administrative costs and offender due-process rights, evaluated against average time to case closure.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to task id=20 as a declared alternative under the OR decomposition of goal id=6. Supported by frequent and extreme variants ending in credit collection, such as V0001.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** macro 44/231 variants (19.0%) · micro 59013/150370 cases (39.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.10, nearest other category `administrative_appeal_prefecture` at mean distance 4.72

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.182, nearest other category `administrative_appeal_prefecture` at mean distance 0.494

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0142` / `V0153` (category `delinquent_payment`): structural=17, profile=0.038
- `V0153` / `V0154` (category `delinquent_payment`): structural=17, profile=0.358
- `V0153` / `V0207` (category `delinquent_payment`): structural=17, profile=0.344
- `V0153` / `V0208` (category `delinquent_payment`): structural=17, profile=0.360
- `V0018` / `V0153` (category `delinquent_payment`): structural=16, profile=0.057
- `V0024` / `V0153` (category `delinquent_payment`): structural=16, profile=0.061
- `V0056` / `V0153` (category `delinquent_payment`): structural=16, profile=0.339
- `V0060` / `V0153` (category `delinquent_payment`): structural=16, profile=0.051
- `V0065` / `V0153` (category `delinquent_payment`): structural=16, profile=0.377
- `V0085` / `V0153` (category `delinquent_payment`): structural=16, profile=0.350

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`coercive_credit_collection`) / `V0004` (`delinquent_payment`): structural=1, profile=0.355
- `V0004` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.354
- `V0005` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.711
- `V0005` (`delinquent_payment`) / `V0071` (`coercive_credit_collection`): structural=1, profile=0.379
- `V0006` (`delinquent_payment`) / `V0010` (`coercive_credit_collection`): structural=1, profile=0.717
- `V0006` (`delinquent_payment`) / `V0080` (`timely_payment`): structural=1, profile=0.013
- `V0006` (`delinquent_payment`) / `V0088` (`coercive_credit_collection`): structural=1, profile=0.390
- `V0007` (`timely_payment`) / `V0154` (`delinquent_payment`): structural=1, profile=0.075
- `V0008` (`administrative_appeal_prefecture`) / `V0054` (`delinquent_payment`): structural=1, profile=0.361
- `V0008` (`administrative_appeal_prefecture`) / `V0062` (`delinquent_payment`): structural=1, profile=0.354

## Residual

11/231 variants (4.8%), 20807/150370 cases (13.8%) unassigned.

- `V0003`: The case ends after Send Fine without payment or further enforcement/appeal steps, so it does not fit any definitive resolution category.
- `V0012`: The case contains payment followed by sending the fine, which does not cleanly map to the standard lifecycle categories.
- `V0029`: Ends directly with an appeal to a judge after penalty, not fitting standard payment, prefecture appeal, or credit collection.
- `V0063`: The process deviates into a judicial appeal pathway without falling neatly into timely payment, delinquent payment, prefecture appeal, or credit collection.
- `V0069`: The narrative concludes with a judicial appeal after the prefecture appeal process, falling outside standard administrative categories.
- `V0077`: The sequence is atypical with out-of-order fine dispatch and appeal steps, fitting none of the standard categories well.
- `V0093`: The unusual sequence starts with a judicial appeal before fine dispatch, fitting none of the standard definitions.
- `V0096`: The process focuses heavily on an early judicial appeal rather than administrative resolution or standard payment.
- `V0097`: The trajectory involves a mix of judicial appeal and prefecture appeal without reaching a standard payment or enforcement outcome.
- `V0193`: Does not fit any defined category as it terminates prematurely at sending the fine with early abnormal payment.
- `V0205`: The primary focus is an appeal to a judge following penalties and early payment without completing standard administrative appeal or full recovery tracks.
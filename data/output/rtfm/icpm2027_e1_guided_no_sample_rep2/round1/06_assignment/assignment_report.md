# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_no_sample_rep2` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Cases resolved through prompt payment of the fine, advancing the softgoal Maximize timely fine revenue and helping Minimize administrative and enforcement cost, judged against Indicator 114 Average time to case closure.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative id=12 as authorized by the goal model decomposition under id=4.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 8/231 variants (3.5%) · micro 49628/150370 cases (33.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.29, nearest other category `administrative_appeal` at mean distance 5.47

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.393, nearest other category `delinquent_payment` at mean distance 0.323

## Resolve via delinquent payment (`delinquent_payment`)

Cases resolved via payment after penalties have been added, helping Maximize timely fine revenue, judged against Indicator 114 Average time to case closure.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative id=13 as authorized by the goal model decomposition under id=4.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 50/231 variants (21.6%) · micro 16925/150370 cases (11.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.97, nearest other category `administrative_appeal` at mean distance 5.14

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.192, nearest other category `timely_payment` at mean distance 0.323

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Cases resolved through an administrative appeal process to the Prefecture, preserving due process rights while impacting administrative costs and revenue, judged against Indicator 113.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative id=14 as authorized by the goal model decomposition under id=4.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 73/231 variants (31.6%) · micro 3664/150370 cases (2.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.99, nearest other category `coercive_credit_collection` at mean distance 4.72

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.362, nearest other category `judicial_appeal` at mean distance 0.404

## Resolve via judicial appeal to the Judge (`judicial_appeal`)

Cases resolved through a judicial appeal to the Judge, strongly supporting offender's due process rights while hurting enforcement costs, judged against Indicator 175.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative id=19 as authorized by the goal model decomposition under id=4.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 56/231 variants (24.2%) · micro 514/150370 cases (0.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.35, nearest other category `administrative_appeal` at mean distance 4.99

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.380, nearest other category `delinquent_payment` at mean distance 0.379

## Resolve via coercive credit collection (`coercive_credit_collection`)

Cases resolved through coercive credit collection measures, helping revenue but hurting administrative costs, judged against Indicator 114.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative id=20 as authorized by the goal model decomposition under id=4.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** macro 39/231 variants (16.9%) · micro 58881/150370 cases (39.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.10, nearest other category `administrative_appeal` at mean distance 4.72

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.181, nearest other category `judicial_appeal` at mean distance 0.478

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0096` / `V0153` (category `judicial_appeal`): structural=18, profile=0.770
- `V0035` / `V0153` (category `judicial_appeal`): structural=17, profile=0.710
- `V0063` / `V0153` (category `judicial_appeal`): structural=17, profile=0.746
- `V0069` / `V0153` (category `judicial_appeal`): structural=17, profile=0.716
- `V0097` / `V0153` (category `judicial_appeal`): structural=17, profile=0.762
- `V0120` / `V0153` (category `judicial_appeal`): structural=17, profile=0.729
- `V0153` / `V0154` (category `judicial_appeal`): structural=17, profile=0.358
- `V0153` / `V0212` (category `judicial_appeal`): structural=17, profile=0.706
- `V0027` / `V0153` (category `judicial_appeal`): structural=16, profile=0.705
- `V0029` / `V0153` (category `judicial_appeal`): structural=16, profile=0.730

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`coercive_credit_collection`) / `V0004` (`delinquent_payment`): structural=1, profile=0.355
- `V0001` (`coercive_credit_collection`) / `V0017` (`judicial_appeal`): structural=1, profile=0.027
- `V0001` (`coercive_credit_collection`) / `V0029` (`judicial_appeal`): structural=1, profile=0.396
- `V0001` (`coercive_credit_collection`) / `V0040` (`judicial_appeal`): structural=1, profile=0.027
- `V0004` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.354
- `V0004` (`delinquent_payment`) / `V0014` (`judicial_appeal`): structural=1, profile=0.022
- `V0004` (`delinquent_payment`) / `V0029` (`judicial_appeal`): structural=1, profile=0.374
- `V0004` (`delinquent_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.030
- `V0004` (`delinquent_payment`) / `V0116` (`administrative_appeal`): structural=1, profile=0.025
- `V0005` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.711

## Residual

5/231 variants (2.2%), 20758/150370 cases (13.8%) unassigned.

- `V0003`: The case ends with Send Fine without any payment, appeal, or credit collection, so it does not fit any of the resolution categories.
- `V0012`: The case ends with Send Fine after an initial payment, which does not fit any defined resolution category.
- `V0077`: The narrative only involves creating the fine, appeal steps, and sending the fine, without a final resolution like payment or collection.
- `V0083`: The variant's outcome is Send Appeal to Prefecture, which does not represent a final resolution of the case.
- `V0093`: The outcome is Send Fine after an appeal to the judge, lacking a final resolution category.
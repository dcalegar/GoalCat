# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_no_sample_rep2` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Cases resolved through prompt payment of the fine, advancing the softgoal Maximize timely fine revenue and helping Minimize administrative and enforcement cost, judged against Indicator 114 Average time to case closure.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared OR alternative id=12 as the baseline path for fast resolution.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 8/231 variants (3.5%) · micro 49620/150370 cases (33.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 2.68, nearest other category `delinquent_payment` at mean distance 5.21

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.239, nearest other category `delinquent_payment` at mean distance 0.224

## Resolve via delinquent payment (`delinquent_payment`)

Cases resolved via payment after penalties are applied, helping Maximize timely fine revenue, judged against Indicator 114 Average time to case closure.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared OR alternative id=13 representing late payments after enforcement notification.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 37/231 variants (16.0%) · micro 16937/150370 cases (11.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.63, nearest other category `administrative_appeal` at mean distance 5.16

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.157, nearest other category `timely_payment` at mean distance 0.224

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Cases involving an administrative appeal lodged with the Prefecture, balancing the preservation of due-process rights against administrative costs, judged by Indicator 113 Time to appeal filing, Prefecture.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared OR alternative id=14 representing the administrative appeal path.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 86/231 variants (37.2%) · micro 3701/150370 cases (2.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.88, nearest other category `coercive_credit_collection` at mean distance 4.62

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.367, nearest other category `judicial_appeal` at mean distance 0.406

## Resolve via judicial appeal to the Judge (`judicial_appeal`)

Cases involving a judicial appeal to a judge, strongly making Preserve offender's due-process rights while hurting cost-efficiency, judged against Indicator 175 Time to appeal filing, Judge.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared OR alternative id=19 representing judicial appeals.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 62/231 variants (26.8%) · micro 372/150370 cases (0.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.77, nearest other category `administrative_appeal` at mean distance 5.18

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.401, nearest other category `delinquent_payment` at mean distance 0.398

## Resolve via coercive credit collection (`coercive_credit_collection`)

Cases resolved through forced credit collection measures, helping revenue but hurting enforcement costs and due-process rights, judged against Indicator 114 Average time to case closure.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared OR alternative id=20 representing coercive recovery actions.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** macro 34/231 variants (14.7%) · micro 58988/150370 cases (39.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.11, nearest other category `administrative_appeal` at mean distance 4.62

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.188, nearest other category `judicial_appeal` at mean distance 0.473

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0093` / `V0153` (category `judicial_appeal`): structural=18, profile=0.750
- `V0096` / `V0153` (category `judicial_appeal`): structural=18, profile=0.770
- `V0035` / `V0153` (category `judicial_appeal`): structural=17, profile=0.710
- `V0063` / `V0153` (category `judicial_appeal`): structural=17, profile=0.746
- `V0069` / `V0153` (category `judicial_appeal`): structural=17, profile=0.716
- `V0082` / `V0153` (category `judicial_appeal`): structural=17, profile=0.698
- `V0097` / `V0153` (category `judicial_appeal`): structural=17, profile=0.762
- `V0120` / `V0153` (category `judicial_appeal`): structural=17, profile=0.729
- `V0153` / `V0154` (category `judicial_appeal`): structural=17, profile=0.358
- `V0153` / `V0212` (category `judicial_appeal`): structural=17, profile=0.706

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`coercive_credit_collection`) / `V0004` (`delinquent_payment`): structural=1, profile=0.355
- `V0001` (`coercive_credit_collection`) / `V0029` (`judicial_appeal`): structural=1, profile=0.396
- `V0004` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.354
- `V0004` (`delinquent_payment`) / `V0014` (`judicial_appeal`): structural=1, profile=0.022
- `V0004` (`delinquent_payment`) / `V0029` (`judicial_appeal`): structural=1, profile=0.374
- `V0004` (`delinquent_payment`) / `V0116` (`administrative_appeal`): structural=1, profile=0.025
- `V0005` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.711
- `V0005` (`delinquent_payment`) / `V0071` (`coercive_credit_collection`): structural=1, profile=0.379
- `V0005` (`delinquent_payment`) / `V0116` (`administrative_appeal`): structural=1, profile=0.382
- `V0005` (`delinquent_payment`) / `V0130` (`administrative_appeal`): structural=1, profile=0.019

## Residual

4/231 variants (1.7%), 20752/150370 cases (13.8%) unassigned.

- `V0003`: The case ends at Send Fine without any payment, appeal, or enforcement action.
- `V0012`: Involves early payment followed by sending the fine, but remains unclosed in terms of final resolution categories.
- `V0077`: Incomplete or irregular flow ending in Send Fine after appeal actions; does not fit standard lifecycle.
- `V0193`: Incomplete or non-standard sequence ending in Send Fine without clear payment or appeal resolution.
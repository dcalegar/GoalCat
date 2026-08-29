# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_no_sample_rep2` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Resolution of the fine case through prompt voluntary payment by the offender, advancing the softgoal to maximize timely fine revenue and helping to minimize administrative and enforcement cost.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=12 based on the goal model decomposition under goal id=4.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 35/231 variants (15.2%) · micro 49653/150370 cases (33.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.98, nearest other category `delinquent_payment` at mean distance 5.09

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.218, nearest other category `delinquent_payment` at mean distance 0.196

## Resolve via delinquent payment (`delinquent_payment`)

Resolution of the fine case through payment after penalties have been added and the fine becomes enforceable, helping to maximize timely fine revenue.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=13 under the enforced case closure options of goal id=6.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 37/231 variants (16.0%) · micro 16963/150370 cases (11.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.04, nearest other category `administrative_appeal` at mean distance 4.51

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.178, nearest other category `timely_payment` at mean distance 0.196

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Resolution of the fine case through an administrative appeal process directed to the Prefecture, preserving offender's due-process rights while impacting administrative cost and revenue.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=14 under the mutually exclusive contested appeal options of goal id=7.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 52/231 variants (22.5%) · micro 3637/150370 cases (2.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.80, nearest other category `delinquent_payment` at mean distance 4.51

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.353, nearest other category `judicial_appeal` at mean distance 0.402

## Resolve via judicial appeal toometr to the Judge (`judicial_appeal`)

Resolution of the fine case through a judicial appeal brought before a judge, strongly making the softgoal to preserve offender's due-process rights while hurting administrative cost and revenue.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=19 under the mutually exclusive contested appeal options of goal id=7.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 51/231 variants (22.1%) · micro 342/150370 cases (0.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.55, nearest other category `administrative_appeal` at mean distance 5.08

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.384, nearest other category `timely_payment` at mean distance 0.397

## Resolve via coercive credit collection (`coercive_credit_collection`)

Resolution of the fine case through coercive credit collection procedures, helping fine revenue but hurting enforcement costs.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=20 under the enforced case closure options of goal id=6.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** macro 43/231 variants (18.6%) · micro 59012/150370 cases (39.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.10, nearest other category `administrative_appeal` at mean distance 4.69

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.186, nearest other category `judicial_appeal` at mean distance 0.487

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0093` / `V0153` (category `judicial_appeal`): structural=18, profile=0.750
- `V0096` / `V0153` (category `judicial_appeal`): structural=18, profile=0.770
- `V0035` / `V0153` (category `judicial_appeal`): structural=17, profile=0.710
- `V0063` / `V0153` (category `judicial_appeal`): structural=17, profile=0.746
- `V0069` / `V0153` (category `judicial_appeal`): structural=17, profile=0.716
- `V0120` / `V0153` (category `judicial_appeal`): structural=17, profile=0.729
- `V0153` / `V0154` (category `judicial_appeal`): structural=17, profile=0.358
- `V0153` / `V0206` (category `judicial_appeal`): structural=17, profile=0.718
- `V0153` / `V0212` (category `judicial_appeal`): structural=17, profile=0.706
- `V0153` / `V0214` (category `judicial_appeal`): structural=17, profile=0.688

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`coercive_credit_collection`) / `V0004` (`delinquent_payment`): structural=1, profile=0.355
- `V0001` (`coercive_credit_collection`) / `V0029` (`judicial_appeal`): structural=1, profile=0.396
- `V0004` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.354
- `V0004` (`delinquent_payment`) / `V0014` (`judicial_appeal`): structural=1, profile=0.022
- `V0004` (`delinquent_payment`) / `V0029` (`judicial_appeal`): structural=1, profile=0.374
- `V0004` (`delinquent_payment`) / `V0116` (`timely_payment`): structural=1, profile=0.025
- `V0005` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.711
- `V0005` (`delinquent_payment`) / `V0071` (`coercive_credit_collection`): structural=1, profile=0.379
- `V0005` (`delinquent_payment`) / `V0116` (`timely_payment`): structural=1, profile=0.382
- `V0005` (`delinquent_payment`) / `V0130` (`timely_payment`): structural=1, profile=0.019

## Residual

13/231 variants (5.6%), 20763/150370 cases (13.8%) unassigned.

- `V0003`: The process stops at Send Fine without any payment, appeal, or enforcement action.
- `V0012`: The case involves an early payment followed by sending the fine, but lacks a complete resolution fitting the standard taxonomy flow.
- `V0077`: Incomplete or anomalous flow starting with fine creation and ending with sending fine out of order; does not clearly resolve into any category.
- `V0104`: The variant ends with notifying the result of the appeal to the offender without a final resolution like payment or coercive collection.
- `V0115`: The process ends at notifying the result to the offender without reaching a resolution state.
- `V0137`: The process stops at notifying the appeal result without any terminal resolution.
- `V0167`: The process terminates with notifying the result of the appeal, without reaching a definitive resolution category like payment or collection.
- `V0175`: Terminates at notifying the result of the appeal without a final resolution.
- `V0179`: Ends with notifying the result of the administrative appeal rather than a final resolution.
- `V0191`: Ends at receiving the result of the appeal without a final resolution.
- `V0192`: Terminates with receiving the appeal result from the Prefecture.
- `V0193`: Terminates at sending the fine with no final resolution achieved.
- `V0194`: Terminates at sending an appeal to the Prefecture without a final resolution.
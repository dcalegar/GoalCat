# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_rep4` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Resolution of the fine case through early payment before penalties or enforcement actions, advancing the softgoal to maximize timely fine revenue and helping minimize administrative and enforcement cost, judged against the indicator for time to fine dispatch.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=12, supported by frequent variants such as V0002 where payment occurs promptly after fine creation.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 7/231 variants (3.0%) · micro 49629/150370 cases (33.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 2.38, nearest other category `delinquent_payment` at mean distance 5.33

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.254, nearest other category `delinquent_payment` at mean distance 0.254

## Resolve via delinquent payment (`delinquent_payment`)

Resolution of the fine case through delayed payment occurring after notifications and penalties have been applied, contributing to maximizing timely fine revenue, judged against average time to case closure.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=13, supported by variants such as V0004, V0005, and V0006 where payments happen subsequent to notification and penalty addition steps.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 75/231 variants (32.5%) · micro 17004/150370 cases (11.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.51, nearest other category `administrative_appeal` at mean distance 4.90

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.205, nearest other category `timely_payment` at mean distance 0.254

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Resolution of the fine case via an administrative appeal submitted to the Prefecture, preserving the offender's due-process rights while impacting administrative costs and fine revenue, judged against the time to appeal filing indicator for the Prefecture.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=14, supported by variants such as V0008, V0057, and V0135 involving the inclusion of date appeals and sending appeals to the Prefecture.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 53/231 variants (22.9%) · micro 3595/150370 cases (2.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.21, nearest other category `coercive_credit_collection` at mean distance 4.84

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.353, nearest other category `judicial_appeal` at mean distance 0.397

## Resolve via judicial appeal to the Judge (`judicial_appeal`)

Resolution of the fine case via a judicial appeal submitted to a Judge, heavily advancing the offender's due-process rights while hurting administrative and enforcement costs, judged against the time to appeal filing indicator for the Judge.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=19, backed by variants such as V0103 and V0176 where appeals to the Judge are explicitly recorded.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 36/231 variants (15.6%) · micro 463/150370 cases (0.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.99, nearest other category `administrative_appeal` at mean distance 5.36

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.352, nearest other category `administrative_appeal` at mean distance 0.397

## Resolve via coercive credit collection (`coercive_credit_collection`)

Resolution of the fine case through coercive credit collection measures after all other options fail, helping maximize revenue but hurting administrative costs, judged against the average time to case closure indicator.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=20, supported by frequent variants like V0001 where cases culminate in credit collection routing.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** macro 43/231 variants (18.6%) · micro 58905/150370 cases (39.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.11, nearest other category `administrative_appeal` at mean distance 4.84

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.186, nearest other category `judicial_appeal` at mean distance 0.483

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0096` / `V0153` (category `judicial_appeal`): structural=18, profile=0.770
- `V0035` / `V0153` (category `judicial_appeal`): structural=17, profile=0.710
- `V0063` / `V0153` (category `judicial_appeal`): structural=17, profile=0.746
- `V0069` / `V0153` (category `judicial_appeal`): structural=17, profile=0.716
- `V0120` / `V0153` (category `judicial_appeal`): structural=17, profile=0.729
- `V0153` / `V0154` (category `judicial_appeal`): structural=17, profile=0.358
- `V0153` / `V0212` (category `judicial_appeal`): structural=17, profile=0.706
- `V0027` / `V0153` (category `judicial_appeal`): structural=16, profile=0.705
- `V0029` / `V0153` (category `judicial_appeal`): structural=16, profile=0.730
- `V0047` / `V0153` (category `judicial_appeal`): structural=16, profile=0.706

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`coercive_credit_collection`) / `V0004` (`delinquent_payment`): structural=1, profile=0.355
- `V0001` (`coercive_credit_collection`) / `V0017` (`judicial_appeal`): structural=1, profile=0.027
- `V0001` (`coercive_credit_collection`) / `V0029` (`judicial_appeal`): structural=1, profile=0.396
- `V0004` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.354
- `V0004` (`delinquent_payment`) / `V0014` (`judicial_appeal`): structural=1, profile=0.022
- `V0004` (`delinquent_payment`) / `V0029` (`judicial_appeal`): structural=1, profile=0.374
- `V0004` (`delinquent_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.030
- `V0005` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.711
- `V0005` (`delinquent_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.387
- `V0005` (`delinquent_payment`) / `V0037` (`judicial_appeal`): structural=1, profile=0.062

## Residual

17/231 variants (7.4%), 20774/150370 cases (13.8%) unassigned.

- `V0003`: The case ends after Send Fine without payment or further enforcement, so it does not fit any resolution category.
- `V0012`: Ends with Send Fine after an early payment step, which does not fit standard closure categories.
- `V0077`: The case concludes with Send Fine after an appeal process, but does not reach a final resolution like payment or credit collection.
- `V0093`: The case ends with Send Fine following an appeal to the judge, with no final resolution like payment or collection.
- `V0103`: The narrative ends inconclusively with Send Appeal to Prefecture without reaching a final resolution or payment.
- `V0104`: The variant ends at Notify Result Appeal to Offender without resolving through payment, credit collection, or an active appeal.
- `V0115`: The variant ends with Notify Result Appeal to Offender without final resolution or closure.
- `V0118`: The process ends at Send Appeal to Prefecture without a terminal resolution.
- `V0119`: The narrative ends with Send Appeal to Prefecture.
- `V0124`: The variant ends at Send Appeal to Prefecture with an irregular early payment event.
- `V0125`: The sequence terminates at Send Appeal to Prefecture without completion.
- `V0137`: The process concludes with notifying the result of an appeal to the offender without resolving via payment, appeal outcome, or collection.
- `V0144`: The process stops at sending an appeal to the Prefecture without completing a resolution path.
- `V0145`: The process stops after sending an appeal to the Prefecture without reaching a final resolution category.
- `V0193`: The narrative has an irregular flow where payment occurs before the fine is officially sent, fitting no standard category.
- `V0194`: Payment occurs early in the sequence before administrative appeal steps are processed, making it a residual case.
- `V0196`: The sequence involves out-of-order steps like appealing before sending the fine, falling into the residual.
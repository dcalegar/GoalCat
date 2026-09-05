# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_pertC_distractor_6_187_rep4` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Cases resolved through prompt payment by the offender, advancing timely fine revenue and minimizing administrative and enforcement costs, judged against time-to-closure indicators.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative 12, evidenced by frequent variants such as V0002 showing direct payment.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 7/231 variants (3.0%) · micro 49581/150370 cases (33.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 2.48, nearest other category `delinquent_payment` at mean distance 5.51

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.352, nearest other category `delinquent_payment` at mean distance 0.296

## Resolve via delinquent payment (`delinquent_payment`)

Cases resolved via payment after penalties or enforcement steps have been applied, contributing to timely fine revenue while balancing due-process concerns.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative 13, supported by variants like V0004, V0005, and V0006 where payments occur after penalty addition.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 60/231 variants (26.0%) · micro 16988/150370 cases (11.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.25, nearest other category `administrative_appeal` at mean distance 4.75

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.185, nearest other category `timely_payment` at mean distance 0.296

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Cases involving an administrative appeal process directed to the Prefecture, preserving offender due-process rights while potentially impacting enforcement costs and revenue, measured against appeal filing time indicators.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative 14, evidenced in variants such as V0008, V0057, and V00137 detailing Prefecture appeal steps.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 65/231 variants (28.1%) · micro 3655/150370 cases (2.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.38, nearest other category `delinquent_payment` at mean distance 4.75

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.362, nearest other category `judicial_appeal` at mean distance 0.414

## Resolve via judicial appeal to the Judge (`judicial_appeal`)

Cases involving judicial review by a judge, strongly prioritizing the preservation of due-process rights at the expense of enforcement costs and revenue timing.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative 19, backed by variants like V0103, V0176, and V0140 that include judicial appeal activities.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 55/231 variants (23.8%) · micro 492/150370 cases (0.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.79, nearest other category `delinquent_payment` at mean distance 5.37

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.390, nearest other category `delinquent_payment` at mean distance 0.382

## Resolve via coercive credit collection (`coercive_credit_collection`)

Cases escalated to coercive credit collection procedures due to non-payment or unresolved status, aiming to recover revenue while incurring higher enforcement costs.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative 20, substantiated by frequent variants ending in credit collection like V0001.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** macro 41/231 variants (17.7%) · micro 58903/150370 cases (39.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.10, nearest other category `administrative_appeal` at mean distance 4.90

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.191, nearest other category `judicial_appeal` at mean distance 0.483

## Resolve via fine annulment (`fine_annulment`)

Cases where the fine is formally annulled or dismissed, concluding the process without collection.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative 187, maintaining structural completeness for the OR decomposition.

**Goal-model linkage:** 187 (Task): Resolve via fine annulment

**Coverage:** macro 0/231 variants (0.0%) · micro 0/150370 cases (0.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a, nearest other category `None` at mean distance n/a

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a, nearest other category `None` at mean distance n/a

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0093` / `V0153` (category `judicial_appeal`): structural=18, profile=0.750
- `V0096` / `V0153` (category `judicial_appeal`): structural=18, profile=0.770
- `V0035` / `V0153` (category `judicial_appeal`): structural=17, profile=0.710
- `V0063` / `V0153` (category `judicial_appeal`): structural=17, profile=0.746
- `V0069` / `V0153` (category `judicial_appeal`): structural=17, profile=0.716
- `V0097` / `V0153` (category `judicial_appeal`): structural=17, profile=0.762
- `V0120` / `V0153` (category `judicial_appeal`): structural=17, profile=0.729
- `V0134` / `V0153` (category `judicial_appeal`): structural=17, profile=0.706
- `V0153` / `V0154` (category `judicial_appeal`): structural=17, profile=0.358
- `V0153` / `V0212` (category `judicial_appeal`): structural=17, profile=0.706

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

3/231 variants (1.3%), 20751/150370 cases (13.8%) unassigned.

- `V0003`: The process ends at Send Fine without any payment, appeal, or enforcement closure.
- `V0012`: The case involves an early payment followed by sending the fine, leaving the process incomplete.
- `V0077`: The process ends with 'Send Fine' after an administrative appeal is initiated, without concluding payment, resolution, or formal escalation.
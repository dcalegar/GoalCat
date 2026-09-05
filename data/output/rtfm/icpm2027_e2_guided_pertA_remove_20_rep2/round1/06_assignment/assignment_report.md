# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_pertA_remove_20_rep2` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Cases resolved through prompt payment of the fine, advancing the softgoal to maximize timely fine revenue and helping to minimize administrative and enforcement cost. Evaluated against indicator 'Time to fine dispatch (days)' and 'Average time to case closure (days)'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=12 as observed in frequent variants such as V0002.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 10/231 variants (4.3%) · micro 50004/150370 cases (33.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 2.64, nearest other category `delinquent_payment` at mean distance 5.16

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.356, nearest other category `delinquent_payment` at mean distance 0.377

## Resolve via delinquent payment (`delinquent_payment`)

Cases resolved via payment after penalties or enforcement steps have been initiated, helping to maximize timely fine revenue. Judged against indicator 'Average time to case closure (days)'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=13, evidenced by variants like V0004 and V0009 where payments occur after notification and penalty additions.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 51/231 variants (22.1%) · micro 75424/150370 cases (50.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.56, nearest other category `administrative_appeal_prefecture` at mean distance 5.10

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.298, nearest other category `timely_payment` at mean distance 0.377

## Resolve via administrative appeal to the Prefecture (`administrative_appeal_prefecture`)

Cases involving an administrative appeal submitted to the Prefecture, preserving the offender's due-process rights while incurring trade-offs on administrative cost and revenue. Judged against 'Time to appeal filing, Prefecture (days)'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=14, supported by variants showing activities such as Insert Date Appeal to Prefecture and Send Appeal to Prefecture.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 101/231 variants (43.7%) · micro 3971/150370 cases (2.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.16, nearest other category `delinquent_payment` at mean distance 5.10

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.384, nearest other category `judicial_appeal_judge` at mean distance 0.409

## Resolve via judicial appeal to the Judge (`judicial_appeal_judge`)

Cases involving a judicial appeal to the Judge, making a strong contribution to preserving the offender's due-process rights while hurting administrative costs. Judged against 'Time to appeal filing, Judge (days)'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=19, observed in complex or contested variants where judicial appeals are recorded.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 67/231 variants (29.0%) · micro 541/150370 cases (0.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.70, nearest other category `administrative_appeal_prefecture` at mean distance 5.21

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.407, nearest other category `administrative_appeal_prefecture` at mean distance 0.409

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0093` / `V0153` (category `judicial_appeal_judge`): structural=18, profile=0.750
- `V0096` / `V0153` (category `judicial_appeal_judge`): structural=18, profile=0.770
- `V0035` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.710
- `V0063` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.746
- `V0069` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.716
- `V0082` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.698
- `V0097` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.762
- `V0120` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.729
- `V0134` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.706
- `V0153` / `V0154` (category `judicial_appeal_judge`): structural=17, profile=0.358

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`delinquent_payment`) / `V0017` (`judicial_appeal_judge`): structural=1, profile=0.027
- `V0001` (`delinquent_payment`) / `V0029` (`judicial_appeal_judge`): structural=1, profile=0.396
- `V0001` (`delinquent_payment`) / `V0040` (`judicial_appeal_judge`): structural=1, profile=0.027
- `V0004` (`delinquent_payment`) / `V0014` (`judicial_appeal_judge`): structural=1, profile=0.022
- `V0004` (`delinquent_payment`) / `V0029` (`judicial_appeal_judge`): structural=1, profile=0.374
- `V0004` (`delinquent_payment`) / `V0031` (`judicial_appeal_judge`): structural=1, profile=0.030
- `V0005` (`delinquent_payment`) / `V0031` (`judicial_appeal_judge`): structural=1, profile=0.387
- `V0005` (`delinquent_payment`) / `V0037` (`judicial_appeal_judge`): structural=1, profile=0.062
- `V0005` (`delinquent_payment`) / `V0044` (`timely_payment`): structural=1, profile=0.001
- `V0005` (`delinquent_payment`) / `V0130` (`administrative_appeal_prefecture`): structural=1, profile=0.019

## Residual

2/231 variants (0.9%), 20430/150370 cases (13.6%) unassigned.

- `V0003`: The process ends with Send Fine and lacks payment, appeal, or collection steps, making it incomplete regarding final resolution.
- `V0026`: The case ends with credit collection after a penalty was added, representing an unresolved delinquent process rather than a successful payment or appeal resolution.
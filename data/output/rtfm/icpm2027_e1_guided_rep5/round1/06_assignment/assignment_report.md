# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_rep5` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Resolution of the fine case through early or timely payment by the offender, advancing the softgoal 'Maximize timely fine revenue' and helping 'Minimize administrative & enforcement cost', evaluated against indicator 'Time to fine dispatch (days)' and 'Average time to case closure (days)'.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative id=12 as evidenced by frequent fast payments in variants such as V0002.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 9/231 variants (3.9%) · micro 50062/150370 cases (33.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 2.33, nearest other category `administrative_appeal_prefecture` at mean distance 5.63

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.356, nearest other category `delinquent_payment` at mean distance 0.309

## Resolve via delinquent payment (`delinquent_payment`)

Resolution of the fine case through payment occurring after penalties or notifications have been applied, helping maximize timely fine revenue, evaluated against indicator 'Average time to case closure (days)'.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative id=13, evidenced by variants where payment occurs after penalty application such as V0004, V0005, and V0006.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 51/231 variants (22.1%) · micro 16820/150370 cases (11.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.07, nearest other category `administrative_appeal_prefecture` at mean distance 5.23

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.176, nearest other category `timely_payment` at mean distance 0.309

## Resolve via administrative appeal to the Prefecture (`administrative_appeal_prefecture`)

Resolution of the fine case through an administrative appeal process directed to the Prefecture, preserving offender's due-process rights while potentially increasing administrative costs, evaluated against indicator 'Time to appeal filing, Prefecture (days)' and 'Average time to case closure (days)'.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative id=14, supported by variants containing steps like 'Insert Date Appeal to Prefecture', 'Send Appeal to Prefecture', and 'Receive Result Appeal from Prefecture' (e.g., V0008, V0057).

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 79/231 variants (34.2%) · micro 3710/150370 cases (2.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.97, nearest other category `coercive_credit_collection` at mean distance 4.69

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.369, nearest other category `judicial_appeal_judge` at mean distance 0.412

## Resolve via judicial appeal to the Judge (`judicial_appeal_judge`)

Resolution of the fine case through a judicial appeal to a Judge, making a strong contribution to preserving offender's due-process rights while hurting administrative & enforcement cost minimization, evaluated against indicator 'Time to appeal filing, Judge (days)'.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative id=19, supported by variants explicitly logging judicial appeals such as V0103, V0176, and V0140.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 54/231 variants (23.4%) · micro 392/150370 cases (0.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.50, nearest other category `administrative_appeal_prefecture` at mean distance 5.07

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.393, nearest other category `delinquent_payment` at mean distance 0.387

## Resolve via coercive credit collection (`coercive_credit_collection`)

Resolution of the fine case through coercive credit collection measures, helping maximize fine revenue while hurting cost minimization, evaluated against indicator 'Average time to case closure (days)'.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative id=20, backed by variants concluding with credit collection actions such as V0001, V0009, and V0134.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** macro 37/231 variants (16.0%) · micro 59001/150370 cases (39.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.10, nearest other category `administrative_appeal_prefecture` at mean distance 4.69

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.178, nearest other category `judicial_appeal_judge` at mean distance 0.482

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0093` / `V0153` (category `judicial_appeal_judge`): structural=18, profile=0.750
- `V0096` / `V0153` (category `judicial_appeal_judge`): structural=18, profile=0.770
- `V0035` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.710
- `V0063` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.746
- `V0069` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.716
- `V0097` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.762
- `V0120` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.729
- `V0153` / `V0154` (category `judicial_appeal_judge`): structural=17, profile=0.358
- `V0153` / `V0212` (category `judicial_appeal_judge`): structural=17, profile=0.706
- `V0027` / `V0153` (category `judicial_appeal_judge`): structural=16, profile=0.705

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`coercive_credit_collection`) / `V0004` (`delinquent_payment`): structural=1, profile=0.355
- `V0001` (`coercive_credit_collection`) / `V0029` (`judicial_appeal_judge`): structural=1, profile=0.396
- `V0004` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.354
- `V0004` (`delinquent_payment`) / `V0014` (`judicial_appeal_judge`): structural=1, profile=0.022
- `V0004` (`delinquent_payment`) / `V0018` (`timely_payment`): structural=1, profile=0.367
- `V0004` (`delinquent_payment`) / `V0029` (`judicial_appeal_judge`): structural=1, profile=0.374
- `V0004` (`delinquent_payment`) / `V0031` (`judicial_appeal_judge`): structural=1, profile=0.030
- `V0005` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.711
- `V0005` (`delinquent_payment`) / `V0031` (`judicial_appeal_judge`): structural=1, profile=0.387
- `V0005` (`delinquent_payment`) / `V0037` (`judicial_appeal_judge`): structural=1, profile=0.062

## Residual

1/231 variants (0.4%), 20385/150370 cases (13.6%) unassigned.

- `V0003`: The narrative only shows fine creation and sending without reaching a final resolution such as payment or appeal.
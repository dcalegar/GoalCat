# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_pertC_distractor_6_187_rep2` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Cases resolved through prompt payment of the fine, advancing the softgoal 'Maximize timely fine revenue' and helping 'Minimize administrative & enforcement cost', judged against indicator 'Average time to case closure'.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative id=12, supported by frequent variants such as V0002 and V0007 where payment concludes the case early.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 7/231 variants (3.0%) · micro 49608/150370 cases (33.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 1.81, nearest other category `delinquent_payment` at mean distance 5.82

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.342, nearest other category `delinquent_payment` at mean distance 0.299

## Resolve via delinquent payment (`delinquent_payment`)

Cases resolved through payment made after penalties have been added and notifications sent, helping 'Maximize timely fine revenue', judged against indicator 'Average time to case closure'.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative id=13, supported by variants like V0004, V0005, and V0006 where payments occur subsequent to notification and penalty steps.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 46/231 variants (19.9%) · micro 16957/150370 cases (11.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.85, nearest other category `administrative_appeal` at mean distance 5.06

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.189, nearest other category `timely_payment` at mean distance 0.299

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Cases involving an administrative appeal process directed to the Prefecture, preserving offender's due-process rights while potentially increasing costs and delaying revenue, judged against 'Time to appeal filing, Prefecture'.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative id=14, evidenced by variants containing appeal insertion and transmission steps such as V0008, V0057, and V0135.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 76/231 variants (32.9%) · micro 3650/150370 cases (2.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.38, nearest other category `coercive_credit_collection` at mean distance 4.86

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.387, nearest other category `delinquent_payment` at mean distance 0.384

## Resolve via judicial appeal to the Judge (`judicial_appeal`)

Cases involving judicial appeal to a judge, strongly making 'Preserve offender's due-process rights' while hurting cost minimization, judged against 'Time to appeal filing, Judge'.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative id=19, supported by variants showing 'Appeal to Judge' actions such as V0103, V0140, and V0176.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 60/231 variants (26.0%) · micro 511/150370 cases (0.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.27, nearest other category `administrative_appeal` at mean distance 5.06

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.394, nearest other category `delinquent_payment` at mean distance 0.390

## Resolve via coercive credit collection (`coercive_credit_collection`)

Cases escalated and resolved through coercive credit collection measures, helping revenue maximization but hurting cost minimization, judged against 'Average time to case closure'.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative id=20, evidenced by variants culminating in 'Send for Credit Collection' like V0001, V0009, and V0134.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** macro 40/231 variants (17.3%) · micro 58897/150370 cases (39.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.07, nearest other category `administrative_appeal` at mean distance 4.86

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.179, nearest other category `judicial_appeal` at mean distance 0.482

## Resolve via fine annulment (`fine_annulment`)

Cases resulting in the annulment of the fine.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative id=187 as declared in the goal model decomposition.

**Goal-model linkage:** 187 (Task): Resolve via fine annulment

**Coverage:** macro 0/231 variants (0.0%) · micro 0/150370 cases (0.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a, nearest other category `None` at mean distance n/a

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a, nearest other category `None` at mean distance n/a

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0153` / `V0207` (category `delinquent_payment`): structural=17, profile=0.344
- `V0153` / `V0208` (category `delinquent_payment`): structural=17, profile=0.360
- `V0018` / `V0153` (category `delinquent_payment`): structural=16, profile=0.057
- `V0024` / `V0153` (category `delinquent_payment`): structural=16, profile=0.061
- `V0039` / `V0153` (category `delinquent_payment`): structural=16, profile=0.359
- `V0041` / `V0153` (category `delinquent_payment`): structural=16, profile=0.380
- `V0050` / `V0153` (category `delinquent_payment`): structural=16, profile=0.381
- `V0060` / `V0153` (category `delinquent_payment`): structural=16, profile=0.051
- `V0085` / `V0153` (category `delinquent_payment`): structural=16, profile=0.350
- `V0153` / `V0164` (category `delinquent_payment`): structural=16, profile=0.391

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`coercive_credit_collection`) / `V0004` (`delinquent_payment`): structural=1, profile=0.355
- `V0001` (`coercive_credit_collection`) / `V0017` (`judicial_appeal`): structural=1, profile=0.027
- `V0001` (`coercive_credit_collection`) / `V0029` (`judicial_appeal`): structural=1, profile=0.396
- `V0004` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.354
- `V0004` (`delinquent_payment`) / `V0014` (`judicial_appeal`): structural=1, profile=0.022
- `V0004` (`delinquent_payment`) / `V0029` (`judicial_appeal`): structural=1, profile=0.374
- `V0004` (`delinquent_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.030
- `V0004` (`delinquent_payment`) / `V0116` (`administrative_appeal`): structural=1, profile=0.025
- `V0005` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.711
- `V0005` (`delinquent_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.387

## Residual

2/231 variants (0.9%), 20747/150370 cases (13.8%) unassigned.

- `V0003`: The case ends after sending the fine without resulting in payment, appeal, or credit collection, falling into the residual.
- `V0012`: Unusual sequence starting with payment and then sending fine, falling into the residual.
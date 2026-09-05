# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_rep5` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Resolution of the fine case through early or timely payment by the offender. Advances the softgoal 'Maximize timely fine revenue' (Make +100) and 'Minimize administrative & enforcement cost' (Help +50), and performance is judged against indicator 'Time to fine dispatch (days)' and 'Average time to case closure (days)'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=12. Supported by frequent narrative variants such as V0002 and V0007 where payment occurs directly after fine creation or sending.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 24/231 variants (10.4%) · micro 49602/150370 cases (33.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.83, nearest other category `administrative_appeal` at mean distance 4.77

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.261, nearest other category `delinquent_payment` at mean distance 0.216

## Resolve via delinquent payment (`delinquent_payment`)

Resolution of the fine case through payment occurring after penalties or enforcement steps have been initiated. Advances 'Maximize timely fine revenue' (Help +50) and is judged against 'Average time to case closure (days)'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=13. Supported by narrative variants such as V0004, V0005, and V0006 where payment follows fine notification and penalty addition.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 45/231 variants (19.5%) · micro 16969/150370 cases (11.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.43, nearest other category `timely_payment` at mean distance 4.79

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.169, nearest other category `timely_payment` at mean distance 0.216

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Resolution of the fine case through an administrative appeal process directed to the Prefecture. Preserves offender's due-process rights (Help +50) while incurring administrative costs, and is judged against 'Time to appeal filing, Prefecture (days)'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=14. Supported by variants such as V0008 and V0057 showing activities inserting appeal dates and sending appeals to the Prefecture.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 55/231 variants (23.8%) · micro 3645/150370 cases (2.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.90, nearest other category `coercive_credit_collection` at mean distance 4.71

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.334, nearest other category `judicial_appeal` at mean distance 0.407

## Resolve via judicial appeal to the Judge (`judicial_appeal`)

Resolution of the fine case through a judicial appeal brought before a Judge. Strongly preserves due-process rights (Make +100) but hurts administrative and enforcement costs, and is judged against 'Time to appeal filing, Judge (days)'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=19. Supported by variants such as V0103, V0176, and V0140 demonstrating formal appeal steps directed to the Judge.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 65/231 variants (28.1%) · micro 409/150370 cases (0.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.67, nearest other category `administrative_appeal` at mean distance 5.19

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.399, nearest other category `delinquent_payment` at mean distance 0.401

## Resolve via coercive credit collection (`coercive_credit_collection`)

Resolution of the fine case through coercive credit collection measures after all other recourse or timeouts have elapsed. Helps maximize timely fine revenue but hurts minimization of administrative costs, judged against 'Average time to case closure (days)'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=20. Supported by frequent variants like V0001 and V0009 ending with credit collection dispatch after prolonged durations.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** macro 40/231 variants (17.3%) · micro 58998/150370 cases (39.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.09, nearest other category `administrative_appeal` at mean distance 4.71

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.194, nearest other category `judicial_appeal` at mean distance 0.480

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
- `V0153` / `V0167` (category `judicial_appeal`): structural=17, profile=0.716

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`coercive_credit_collection`) / `V0004` (`delinquent_payment`): structural=1, profile=0.355
- `V0001` (`coercive_credit_collection`) / `V0029` (`judicial_appeal`): structural=1, profile=0.396
- `V0004` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.354
- `V0004` (`delinquent_payment`) / `V0014` (`judicial_appeal`): structural=1, profile=0.022
- `V0004` (`delinquent_payment`) / `V0029` (`judicial_appeal`): structural=1, profile=0.374
- `V0004` (`delinquent_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.030
- `V0004` (`delinquent_payment`) / `V0116` (`timely_payment`): structural=1, profile=0.025
- `V0005` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.711
- `V0005` (`delinquent_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.387
- `V0005` (`delinquent_payment`) / `V0037` (`judicial_appeal`): structural=1, profile=0.062

## Residual

2/231 variants (0.9%), 20747/150370 cases (13.8%) unassigned.

- `V0003`: The case ends with Send Fine and has no final payment, appeal, or collection step, thus remaining in the residual category.
- `V0012`: The case concludes with Send Fine after an initial payment, which does not fit standard fine resolution categories cleanly.
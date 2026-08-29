# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_rep1` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Resolution of the fine case through early payment by the offender. Advances the 'Maximize timely fine revenue' softgoal and helps 'Minimize administrative & enforcement cost'. Measured against indicator 'Time to fine dispatch (days)' and 'Average time to case closure (days)'.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative task 12 as observed in frequent variants such as V0002.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 10/231 variants (4.3%) · micro 49619/150370 cases (33.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.84, nearest other category `administrative_appeal` at mean distance 4.76

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.245, nearest other category `delinquent_payment` at mean distance 0.243

## Resolve via delinquent payment (`delinquent_payment`)

Resolution of the fine case through payment after notifications and penalties have been applied. Helps 'Maximize timely fine revenue'. Measured against indicator 'Average time to case closure (days)'.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative task 13 as seen in variants where payment occurs after penalty addition such as V0004 and V0006.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 50/231 variants (21.6%) · micro 16947/150370 cases (11.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.63, nearest other category `administrative_appeal` at mean distance 4.79

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.175, nearest other category `timely_payment` at mean distance 0.243

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Resolution path involving administrative appeal to the Prefecture. Preserves offender's due-process rights while impacting enforcement costs and revenue. Measured against indicator 'Time to appeal filing, Prefecture (days)'.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative task 14 representing administrative appeals observed in variants like V0008 and V0057.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 61/231 variants (26.4%) · micro 3645/150370 cases (2.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.81, nearest other category `coercive_credit_collection` at mean distance 4.63

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.360, nearest other category `timely_payment` at mean distance 0.390

## Resolve via judicial appeal to the Judge (`judicial_appeal`)

Resolution path involving judicial appeal to the Judge. Strongly preserves due-process rights but hurts enforcement cost and revenue. Measured against indicator 'Time to appeal filing, Judge (days)'.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative task 19 representing judicial appeals found in variants like V0103 and V0140.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 65/231 variants (28.1%) · micro 397/150370 cases (0.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.69, nearest other category `administrative_appeal` at mean distance 5.16

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.406, nearest other category `delinquent_payment` at mean distance 0.383

## Resolve via coercive credit collection (`coercive_credit_collection`)

Resolution path via coercive credit collection for unpaid or unresolved fines. Helps revenue but hurts cost and due-process softgoals. Measured against indicator 'Average time to case closure (days)'.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative task 20 representing credit collection endpoints observed in high-duration variants like V0001 and V0009.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** macro 41/231 variants (17.7%) · micro 59010/150370 cases (39.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.07, nearest other category `administrative_appeal` at mean distance 4.63

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.166, nearest other category `judicial_appeal` at mean distance 0.492

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
- `V0153` / `V0154` (category `judicial_appeal`): structural=17, profile=0.358
- `V0153` / `V0167` (category `judicial_appeal`): structural=17, profile=0.716
- `V0153` / `V0206` (category `judicial_appeal`): structural=17, profile=0.718

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`coercive_credit_collection`) / `V0004` (`delinquent_payment`): structural=1, profile=0.355
- `V0001` (`coercive_credit_collection`) / `V0029` (`judicial_appeal`): structural=1, profile=0.396
- `V0004` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.354
- `V0004` (`delinquent_payment`) / `V0014` (`judicial_appeal`): structural=1, profile=0.022
- `V0004` (`delinquent_payment`) / `V0029` (`judicial_appeal`): structural=1, profile=0.374
- `V0004` (`delinquent_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.030
- `V0005` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.711
- `V0005` (`delinquent_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.387
- `V0005` (`delinquent_payment`) / `V0037` (`judicial_appeal`): structural=1, profile=0.062
- `V0005` (`delinquent_payment`) / `V0071` (`coercive_credit_collection`): structural=1, profile=0.379

## Residual

4/231 variants (1.7%), 20752/150370 cases (13.8%) unassigned.

- `V0003`: The case ends at Send Fine without payment or further action, thus it does not resolve the case.
- `V0012`: The case concludes with Send Fine after an initial payment, remaining unresolved.
- `V0077`: An incomplete or abnormal sequence where sending the fine occurs after appeal steps, fitting none of the standard resolution paths.
- `V0193`: Incomplete case progression ending prematurely at 'Send Fine' without resolution or payment categories fitting.
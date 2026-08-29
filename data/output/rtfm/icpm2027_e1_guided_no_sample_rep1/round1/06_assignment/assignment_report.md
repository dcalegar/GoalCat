# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_no_sample_rep1` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Resolution of the fine case through prompt voluntary payment, advancing 'Maximize timely fine revenue' (Make +100) and 'Minimize administrative & enforcement cost' (Help +50), judged against 'Average time to case closure' (Indicator 114).

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared OR alternative 12, as instructed by the default rule.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 35/231 variants (15.2%) · micro 49662/150370 cases (33.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.87, nearest other category `delinquent_payment` at mean distance 5.05

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.213, nearest other category `delinquent_payment` at mean distance 0.193

## Resolve via delinquent payment (`delinquent_payment`)

Resolution of the fine case through late payment after penalties are added, supporting 'Maximize timely fine revenue' (Help +50), judged against 'Average time to case closure' (Indicator 114).

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared OR alternative 13 under the default mapping rule.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 35/231 variants (15.2%) · micro 16912/150370 cases (11.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.23, nearest other category `administrative_appeal` at mean distance 4.60

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.181, nearest other category `timely_payment` at mean distance 0.193

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Resolution of the case through an administrative appeal lodged with the Prefecture, preserving offender's due-process rights (Help +50) while impacting costs and revenue (SomeNegative -25), judged against indicator 113.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared XOR alternative 14, following the default rule.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 50/231 variants (21.6%) · micro 3631/150370 cases (2.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.79, nearest other category `delinquent_payment` at mean distance 4.60

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.351, nearest other category `judicial_appeal` at mean distance 0.403

## Resolve via judicial appeal to the Judge (`judicial_appeal`)

Resolution of the case through a judicial appeal to the Judge, making a strong contribution to due-process rights (Make +100) but hurting administrative costs (Hurt -50), judged against indicator 175.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared XOR alternative 19 under the default rule.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 57/231 variants (24.7%) · micro 392/150370 cases (0.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.46, nearest other category `administrative_appeal` at mean distance 4.97

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.406, nearest other category `delinquent_payment` at mean distance 0.402

## Resolve via coercive credit collection (`coercive_credit_collection`)

Resolution of the case through coercive credit collection measures, helping timely revenue (Help +50) but hurting enforcement costs (Hurt -50), judged against indicator 114.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared OR alternative 20, following the default rule.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** macro 40/231 variants (17.3%) · micro 59004/150370 cases (39.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.07, nearest other category `administrative_appeal` at mean distance 4.63

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.169, nearest other category `judicial_appeal` at mean distance 0.479

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
- `V0004` (`delinquent_payment`) / `V0116` (`timely_payment`): structural=1, profile=0.025
- `V0005` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.711
- `V0005` (`delinquent_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.387
- `V0005` (`delinquent_payment`) / `V0037` (`judicial_appeal`): structural=1, profile=0.062

## Residual

14/231 variants (6.1%), 20769/150370 cases (13.8%) unassigned.

- `V0003`: The case ends with 'Send Fine' and remains unresolved with no payment, appeal, or credit collection.
- `V0012`: The narrative concludes with 'Send Fine' without resolution.
- `V0077`: An incomplete or irregular sequence where activities are ordered out of the standard lifecycle.
- `V0103`: The case ends with Send Appeal to Prefecture without resolving into payment, collection, or a final appeal outcome.
- `V0104`: The final activity is Notify Result Appeal to Offender, leaving the case unresolved regarding payment or credit collection.
- `V0115`: The process stops at Notify Result Appeal to Offender without reaching payment or collection.
- `V0118`: The variant ends at Send Appeal to Prefecture with no final resolution.
- `V0119`: The variant terminates at Send Appeal to Prefecture.
- `V0124`: The variant ends at Send Appeal to Prefecture without a final closure.
- `V0125`: The variant terminates at Send Appeal to Prefecture.
- `V0137`: The process stops at Notify Result Appeal to Offender without final resolution.
- `V0144`: The variant stops at Send Appeal to Prefecture.
- `V0145`: The variant ends at Send Appeal to Prefecture.
- `V0193`: Case ends prematurely at Send Fine without resolution or payment, leaving it unclassified.
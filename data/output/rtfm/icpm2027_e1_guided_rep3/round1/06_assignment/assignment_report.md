# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_rep3` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Cases resolved through prompt payment by the offender, advancing the softgoal to maximize timely fine revenue and helping minimize administrative and enforcement costs, judged against indicator 112 (Time to fine dispatch) and 114 (Average time to case closure).

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=12, supported by frequent variants such as V0002 and V0007 where payment occurs shortly after fine creation or sending.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 6/231 variants (2.6%) · micro 49580/150370 cases (33.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 2.27, nearest other category `delinquent_payment` at mean distance 5.59

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.365, nearest other category `delinquent_payment` at mean distance 0.289

## Resolve via delinquent payment (`delinquent_payment`)

Cases resolved via payment after notification or penalty addition, advancing the softgoal to maximize timely fine revenue, judged against indicator 114 (Average time to case closure).

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=13, evidenced by variants like V0004, V0005, and V0006 where payments happen after fine notifications and penalties.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 53/231 variants (22.9%) · micro 16945/150370 cases (11.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.53, nearest other category `administrative_appeal` at mean distance 4.82

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.167, nearest other category `timely_payment` at mean distance 0.289

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Cases involving an administrative appeal process directed to the Prefecture, preserving offender due-process rights (softgoal id=113) while impacting administrative costs and revenue, measured against indicator 113.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=14, observed in variants such as V0008, V0057, and V0035 which contain dates, send events, and results related to the Prefecture appeal.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 69/231 variants (29.9%) · micro 3694/150370 cases (2.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.86, nearest other category `coercive_credit_collection` at mean distance 4.69

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.336, nearest other category `judicial_appeal` at mean distance 0.396

## Resolve via judicial appeal to the Judge (`judicial_appeal`)

Cases involving a judicial appeal to a judge, strongly making the case for preserving offender due-process rights while hurting administrative costs, measured via indicator 175.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=19, identified in variants such as V0103, V0140, and V0176 which explicitly log appeals directed to the Judge.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 59/231 variants (25.5%) · micro 506/150370 cases (0.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.81, nearest other category `administrative_appeal` at mean distance 5.21

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.393, nearest other category `administrative_appeal` at mean distance 0.396

## Resolve via coercive credit collection (`coercive_credit_collection`)

Cases resolved by sending uncollected or disputed fines for coercive credit collection, helping maximize revenue but hurting enforcement costs, evaluated against indicator 114.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=20, supported by frequent long-running variants like V0001, V0009, and V0057 ending with credit collection dispatch.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** macro 41/231 variants (17.7%) · micro 58894/150370 cases (39.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.13, nearest other category `administrative_appeal` at mean distance 4.69

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.192, nearest other category `judicial_appeal` at mean distance 0.484

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
- `V0153` / `V0212` (category `judicial_appeal`): structural=17, profile=0.706
- `V0027` / `V0153` (category `judicial_appeal`): structural=16, profile=0.705

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

- `V0003`: The case only reaches Send Fine and remains open or unclosed in this variant sequence, so it does not fit any of the resolution categories.
- `V0012`: The process sequence concludes with Send Fine after a payment, leaving the final case resolution ambiguous or incomplete under the defined taxonomy categories.
- `V0077`: The narrative ends with Send Fine and lacks final resolution via payment, appeal, or credit collection.
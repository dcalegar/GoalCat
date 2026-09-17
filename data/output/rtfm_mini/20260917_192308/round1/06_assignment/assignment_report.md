# Step 6 — Narrative assignment report

Run: `20260917_192308` | Log: `rtfm_mini` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

8 variants, 8 cases total.

## Resolve via timely payment (`timely_payment`)

Resolution of the fine through timely payment, advancing Maximize timely fine revenue and minimizing administrative and enforcement costs.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative task 12 as evidenced by variant V0004 where payment occurs directly after fine creation.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 1/8 variants (12.5%) · micro 1/8 cases (12.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `delinquent_payment` at mean distance 3.67

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `delinquent_payment` at mean distance 0.498

## Resolve via delinquent payment (`delinquent_payment`)

Resolution of the case through payment after notification and penalty have been applied, contributing to timely fine revenue.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative task 13, evidenced by variants V0003, V0007, and V0008 where payment follows enforcement steps.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 3/8 variants (37.5%) · micro 3/8 cases (37.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 1.33, nearest other category `coercive_credit_collection` at mean distance 1.67

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.253, nearest other category `timely_payment` at mean distance 0.498

## Resolve via administrative appeal to the Prefecture (`administrative_appeal_prefecture`)

Resolution via an administrative appeal process directed to the Prefecture, preserving due-process rights.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative task 14, supported by variant V0006 showing appeal insertion and sending.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 1/8 variants (12.5%) · micro 1/8 cases (12.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `coercive_credit_collection` at mean distance 3.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `judicial_appeal_judge` at mean distance 0.360

## Resolve via judicial appeal to the Judge (`judicial_appeal_judge`)

Resolution through a judicial appeal brought before a judge, strongly making offender's due-process rights.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative task 19, supported by variant V0005 culminating in an appeal to the judge.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 1/8 variants (12.5%) · micro 1/8 cases (12.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `coercive_credit_collection` at mean distance 1.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `administrative_appeal_prefecture` at mean distance 0.360

## Resolve via coercive credit collection (`coercive_credit_collection`)

Resolution of the fine via coercive credit collection procedures, helping fine revenue while hurting administrative costs.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative task 20, evidenced by variant V0002 ending with credit collection.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** macro 1/8 variants (12.5%) · micro 1/8 cases (12.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `judicial_appeal_judge` at mean distance 1.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `judicial_appeal_judge` at mean distance 0.429

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0007` / `V0008` (category `delinquent_payment`): structural=2, profile=0.004
- `V0003` / `V0007` (category `delinquent_payment`): structural=1, profile=0.377
- `V0003` / `V0008` (category `delinquent_payment`): structural=1, profile=0.380

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0002` (`coercive_credit_collection`) / `V0003` (`delinquent_payment`): structural=1, profile=0.361
- `V0002` (`coercive_credit_collection`) / `V0005` (`judicial_appeal_judge`): structural=1, profile=0.429
- `V0003` (`delinquent_payment`) / `V0005` (`judicial_appeal_judge`): structural=1, profile=0.401
- `V0002` (`coercive_credit_collection`) / `V0007` (`delinquent_payment`): structural=2, profile=0.738
- `V0002` (`coercive_credit_collection`) / `V0008` (`delinquent_payment`): structural=2, profile=0.741
- `V0005` (`judicial_appeal_judge`) / `V0007` (`delinquent_payment`): structural=2, profile=0.691
- `V0005` (`judicial_appeal_judge`) / `V0008` (`delinquent_payment`): structural=2, profile=0.687
- `V0002` (`coercive_credit_collection`) / `V0006` (`administrative_appeal_prefecture`): structural=3, profile=0.456
- `V0003` (`delinquent_payment`) / `V0004` (`timely_payment`): structural=3, profile=0.306
- `V0003` (`delinquent_payment`) / `V0006` (`administrative_appeal_prefecture`): structural=3, profile=0.428

## Residual

1/8 variants (12.5%), 1/8 cases (12.5%) unassigned.

- `V0001`: The narrative ends with Send Fine and has no payment or appeal resolution, so it does not fit any completed resolution category.
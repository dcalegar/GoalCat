# Step 6 — Narrative assignment report

Run: `20260820_102718` | Log: `rtfm_mini` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

6 variants, 6 cases total.

## Resolve via timely payment (`timely_payment`)

Resolution of the fine via timely payment directly after issuance.

**Taxonomy-derivation rationale (Step 5):** Sample variant V0004 shows a direct path from fine creation to payment, mapping 1:1 to task 12.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 1/6 variants (16.7%) · micro 1/6 cases (16.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `delinquent_payment` at mean distance 3.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `delinquent_payment` at mean distance 0.306

## Resolve via delinquent payment (`delinquent_payment`)

Resolution of the fine via payment after notification and added penalty.

**Taxonomy-derivation rationale (Step 5):** Sample variant V0003 demonstrates fine creation, communication, notification, penalty addition, and final payment.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 1/6 variants (16.7%) · micro 1/6 cases (16.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `coercive_credit_collection` at mean distance 1.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `timely_payment` at mean distance 0.306

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Resolution through administrative appeal steps involving the Prefecture.

**Taxonomy-derivation rationale (Step 5):** Sample variant V0006 shows execution of appeal steps toward the Prefecture alongside penalty enforcement.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture; 15 (Task): Insert Date Appeal to Prefecture; 16 (Task): Send Appeal to Prefecture; 17 (Task): Receive Result Appeal from Prefecture; 18 (Task): Notify Result Appeal to Offender

**Coverage:** macro 1/6 variants (16.7%) · micro 1/6 cases (16.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `coercive_credit_collection` at mean distance 3.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `judicial_appeal` at mean distance 0.360

## Resolve via judicial appeal to the Judge (`judicial_appeal`)

Resolution via an appeal brought before a judge.

**Taxonomy-derivation rationale (Step 5):** Sample variant V0005 shows fine creation, notification, penalty, and an appeal to the judge.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 1/6 variants (16.7%) · micro 1/6 cases (16.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `coercive_credit_collection` at mean distance 1.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `administrative_appeal` at mean distance 0.360

## Resolve via coercive credit collection (`coercive_credit_collection`)

Resolution through coercive credit collection measures after penalties are applied.

**Taxonomy-derivation rationale (Step 5):** Sample variant V0002 records fine creation, communication, notification, penalty, and final routing to credit collection.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** macro 1/6 variants (16.7%) · micro 1/6 cases (16.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `delinquent_payment` at mean distance 1.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `delinquent_payment` at mean distance 0.361

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- none

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0002` (`coercive_credit_collection`) / `V0003` (`delinquent_payment`): structural=1, profile=0.361
- `V0002` (`coercive_credit_collection`) / `V0005` (`judicial_appeal`): structural=1, profile=0.429
- `V0003` (`delinquent_payment`) / `V0005` (`judicial_appeal`): structural=1, profile=0.401
- `V0002` (`coercive_credit_collection`) / `V0006` (`administrative_appeal`): structural=3, profile=0.456
- `V0003` (`delinquent_payment`) / `V0004` (`timely_payment`): structural=3, profile=0.306
- `V0003` (`delinquent_payment`) / `V0006` (`administrative_appeal`): structural=3, profile=0.428
- `V0005` (`judicial_appeal`) / `V0006` (`administrative_appeal`): structural=3, profile=0.360
- `V0002` (`coercive_credit_collection`) / `V0004` (`timely_payment`): structural=4, profile=0.667
- `V0004` (`timely_payment`) / `V0005` (`judicial_appeal`): structural=4, profile=0.571
- `V0004` (`timely_payment`) / `V0006` (`administrative_appeal`): structural=6, profile=0.544

## Residual

1/6 variants (16.7%), 1/6 cases (16.7%) unassigned.

- `V0001`: The narrative only involves creating and sending the fine without any payment, appeal, or collection steps, so it does not resolve the fine.
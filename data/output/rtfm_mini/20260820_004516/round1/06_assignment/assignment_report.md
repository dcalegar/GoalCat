# Step 6 — Narrative assignment report

Run: `20260820_004516` | Log: `rtfm_mini` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

6 variants, 6 cases total.

## Resolve via timely payment (`timely_payment`)

Fine is resolved directly through early payment by the offender.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared task id=12 as observed in variant V0004.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 1/6 variants (16.7%) · micro 1/6 cases (16.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `delinquent_payment` at mean distance 3.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `delinquent_payment` at mean distance 0.306

## Resolve via delinquent payment (`delinquent_payment`)

Fine is resolved via payment after notification and penalty addition.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared task id=13 as observed in variant V0003.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 1/6 variants (16.7%) · micro 1/6 cases (16.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `coercive_credit_collection` at mean distance 1.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `timely_payment` at mean distance 0.306

## Resolve via administrative appeal to the Prefecture (`administrative_appeal_prefecture`)

Fine case involves an administrative appeal process directed to the Prefecture.

**Taxonomy-derivation rationale (Step 5):** Maps to the declared administrative appeal goal and tasks (id=14 to 18) as observed in variant V0006.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture; 15 (Task): Insert Date Appeal to Prefecture; 16 (Task): Send Appeal to Prefecture; 17 (Task): Receive Result Appeal from Prefecture; 18 (Task): Notify Result Appeal to Offender

**Coverage:** macro 1/6 variants (16.7%) · micro 1/6 cases (16.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `coercive_credit_collection` at mean distance 3.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `judicial_appeal_judge` at mean distance 0.360

## Resolve via judicial appeal to the Judge (`judicial_appeal_judge`)

Fine case is contested via a judicial appeal to the Judge.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared task id=19 as observed in variant V0005.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 1/6 variants (16.7%) · micro 1/6 cases (16.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `coercive_credit_collection` at mean distance 1.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `administrative_appeal_prefecture` at mean distance 0.360

## Resolve via coercive credit collection (`coercive_credit_collection`)

Fine enforcement escalates to coercive credit collection after penalties are added.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared task id=20 as observed in variant V0002.

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
- `V0002` (`coercive_credit_collection`) / `V0005` (`judicial_appeal_judge`): structural=1, profile=0.429
- `V0003` (`delinquent_payment`) / `V0005` (`judicial_appeal_judge`): structural=1, profile=0.401
- `V0002` (`coercive_credit_collection`) / `V0006` (`administrative_appeal_prefecture`): structural=3, profile=0.456
- `V0003` (`delinquent_payment`) / `V0004` (`timely_payment`): structural=3, profile=0.306
- `V0003` (`delinquent_payment`) / `V0006` (`administrative_appeal_prefecture`): structural=3, profile=0.428
- `V0005` (`judicial_appeal_judge`) / `V0006` (`administrative_appeal_prefecture`): structural=3, profile=0.360
- `V0002` (`coercive_credit_collection`) / `V0004` (`timely_payment`): structural=4, profile=0.667
- `V0004` (`timely_payment`) / `V0005` (`judicial_appeal_judge`): structural=4, profile=0.571
- `V0004` (`timely_payment`) / `V0006` (`administrative_appeal_prefecture`): structural=6, profile=0.544

## Residual

1/6 variants (16.7%), 1/6 cases (16.7%) unassigned.

- `V0001`: The process ends with Send Fine without any payment, appeal, or credit collection action, making it incomplete or residual.
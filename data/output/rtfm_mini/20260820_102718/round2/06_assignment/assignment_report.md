# Step 6 — Narrative assignment report

Run: `20260820_102718` | Log: `rtfm_mini` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

6 variants, 6 cases total.

## Resolve via payment (`payment`)

Resolution of the fine via payment, either timely after issuance or delinquent after notification and penalty.

**Taxonomy-derivation rationale (Step 5):** Merged timely_payment and delinquent_payment categories per reviewer request, encompassing both direct payments and payments following notification and penalties.

**Goal-model linkage:** 12 (Task): Resolve via timely payment; 13 (Task): Resolve via delinquent payment

**Coverage:** macro 2/6 variants (33.3%) · micro 2/6 cases (33.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.00, nearest other category `coercive_credit_collection` at mean distance 2.50

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.306, nearest other category `administrative_appeal` at mean distance 0.486

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

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `judicial_appeal` at mean distance 1.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `judicial_appeal` at mean distance 0.429

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0003` / `V0004` (category `payment`): structural=3, profile=0.306

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0002` (`coercive_credit_collection`) / `V0003` (`payment`): structural=1, profile=0.361
- `V0002` (`coercive_credit_collection`) / `V0005` (`judicial_appeal`): structural=1, profile=0.429
- `V0003` (`payment`) / `V0005` (`judicial_appeal`): structural=1, profile=0.401
- `V0002` (`coercive_credit_collection`) / `V0006` (`administrative_appeal`): structural=3, profile=0.456
- `V0003` (`payment`) / `V0006` (`administrative_appeal`): structural=3, profile=0.428
- `V0005` (`judicial_appeal`) / `V0006` (`administrative_appeal`): structural=3, profile=0.360
- `V0002` (`coercive_credit_collection`) / `V0004` (`payment`): structural=4, profile=0.667
- `V0004` (`payment`) / `V0005` (`judicial_appeal`): structural=4, profile=0.571
- `V0004` (`payment`) / `V0006` (`administrative_appeal`): structural=6, profile=0.544

## Residual

1/6 variants (16.7%), 1/6 cases (16.7%) unassigned.

- `V0001`: The process variant ends simply after sending the fine, without a final resolution such as payment, appeal, or coercive collection.
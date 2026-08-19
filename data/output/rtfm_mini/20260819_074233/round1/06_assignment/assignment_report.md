# Step 6 — Narrative assignment report

Run: `20260819_074233` | Log: `rtfm_mini` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

6 variants, 6 cases total.

## Resolve via timely payment (`timely_payment`)

Fines resolved through prompt payment before formal enforcement and penalties.

**Taxonomy-derivation rationale (Step 5):** Directly maps to the timely payment task realizing fast revenue recovery without formal notification or penalties.

**Goal-model linkage:** TP (Task): Resolve via timely payment

**Coverage:** macro 1/6 variants (16.7%) · micro 1/6 cases (16.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `delinquent_payment` at mean distance 3.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `delinquent_payment` at mean distance 0.306

## Resolve via delinquent payment (`delinquent_payment`)

Fines resolved through payment occurring after formal notification and added penalties.

**Taxonomy-derivation rationale (Step 5):** Maps to delinquent payment following the enforcement path with notification and penalty surcharge.

**Goal-model linkage:** TA (Task): Resolve via delinquent payment

**Coverage:** macro 1/6 variants (16.7%) · micro 1/6 cases (16.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `coercive_collection` at mean distance 1.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `timely_payment` at mean distance 0.306

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Fines contested through the administrative appeal channel directed to the Prefecture.

**Taxonomy-derivation rationale (Step 5):** Traces to administrative appeal handling steps including filing, transmission, and ruling from the Prefecture.

**Goal-model linkage:** TB (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 1/6 variants (16.7%) · micro 1/6 cases (16.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `coercive_collection` at mean distance 3.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `judicial_appeal` at mean distance 0.360

## Resolve via judicial appeal to the Judge (`judicial_appeal`)

Fines contested through the judicial appeal channel directed to a Judge.

**Taxonomy-derivation rationale (Step 5):** Maps directly to the judicial appeal alternative providing independent review.

**Goal-model linkage:** TC (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 1/6 variants (16.7%) · micro 1/6 cases (16.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `coercive_collection` at mean distance 1.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `administrative_appeal` at mean distance 0.360

## Resolve via coercive credit collection (`coercive_collection`)

Fines recovered through coercive credit collection procedures following unfulfilled enforcement.

**Taxonomy-derivation rationale (Step 5):** Traces to the coercive credit collection task used when voluntary or non-appeal resolutions are absent.

**Goal-model linkage:** TD (Task): Resolve via coercive credit collection

**Coverage:** macro 1/6 variants (16.7%) · micro 1/6 cases (16.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `delinquent_payment` at mean distance 1.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `delinquent_payment` at mean distance 0.361

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- none

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0002` (`coercive_collection`) / `V0003` (`delinquent_payment`): structural=1, profile=0.361
- `V0002` (`coercive_collection`) / `V0005` (`judicial_appeal`): structural=1, profile=0.429
- `V0003` (`delinquent_payment`) / `V0005` (`judicial_appeal`): structural=1, profile=0.401
- `V0002` (`coercive_collection`) / `V0006` (`administrative_appeal`): structural=3, profile=0.456
- `V0003` (`delinquent_payment`) / `V0004` (`timely_payment`): structural=3, profile=0.306
- `V0003` (`delinquent_payment`) / `V0006` (`administrative_appeal`): structural=3, profile=0.428
- `V0005` (`judicial_appeal`) / `V0006` (`administrative_appeal`): structural=3, profile=0.360
- `V0002` (`coercive_collection`) / `V0004` (`timely_payment`): structural=4, profile=0.667
- `V0004` (`timely_payment`) / `V0005` (`judicial_appeal`): structural=4, profile=0.571
- `V0004` (`timely_payment`) / `V0006` (`administrative_appeal`): structural=6, profile=0.544

## Residual

1/6 variants (16.7%), 1/6 cases (16.7%) unassigned.

- `V0001`: The narrative ends in Send Fine without any payment, appeal, or enforcement action.
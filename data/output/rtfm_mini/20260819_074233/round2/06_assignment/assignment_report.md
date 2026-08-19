# Step 6 — Narrative assignment report

Run: `20260819_074233` | Log: `rtfm_mini` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

6 variants, 6 cases total.

## Resolve via payment (`payment_resolution`)

Fines resolved through payment, encompassing both prompt payments before formal enforcement and delinquent payments following formal notification and added penalties.

**Taxonomy-derivation rationale (Step 5):** Merged timely_payment and delinquent_payment categories per the reviewer's requested script rework-loop demonstration, combining both payment-related resolution paths.

**Goal-model linkage:** TP (Task): Resolve via timely payment; TA (Task): Resolve via delinquent payment

**Coverage:** macro 2/6 variants (33.3%) · micro 2/6 cases (33.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.00, nearest other category `coercive_collection` at mean distance 2.50

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.306, nearest other category `administrative_appeal` at mean distance 0.486

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

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `judicial_appeal` at mean distance 1.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `judicial_appeal` at mean distance 0.429

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0003` / `V0004` (category `payment_resolution`): structural=3, profile=0.306

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0002` (`coercive_collection`) / `V0003` (`payment_resolution`): structural=1, profile=0.361
- `V0002` (`coercive_collection`) / `V0005` (`judicial_appeal`): structural=1, profile=0.429
- `V0003` (`payment_resolution`) / `V0005` (`judicial_appeal`): structural=1, profile=0.401
- `V0002` (`coercive_collection`) / `V0006` (`administrative_appeal`): structural=3, profile=0.456
- `V0003` (`payment_resolution`) / `V0006` (`administrative_appeal`): structural=3, profile=0.428
- `V0005` (`judicial_appeal`) / `V0006` (`administrative_appeal`): structural=3, profile=0.360
- `V0002` (`coercive_collection`) / `V0004` (`payment_resolution`): structural=4, profile=0.667
- `V0004` (`payment_resolution`) / `V0005` (`judicial_appeal`): structural=4, profile=0.571
- `V0004` (`payment_resolution`) / `V0006` (`administrative_appeal`): structural=6, profile=0.544

## Residual

1/6 variants (16.7%), 1/6 cases (16.7%) unassigned.

- `V0001`: The process ends at Send Fine without any payment, appeal, or credit collection action completed.
# Step 6 — Narrative assignment report

Run: `20260818_203957` | Log: `rtfm_mini` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

6 variants, 6 cases total.

## Resolve via payment (`payment`)

Fine is settled by the offender either promptly without enforcement or later following formal notification and penalty addition.

**Taxonomy-derivation rationale (Step 5):** Merged timely_payment and delinquent_payment categories per reviewer request to exercise the revision path.

**Goal-model linkage:** TP (Task): Resolve via timely payment; TA (Task): Resolve via delinquent payment

**Coverage:** macro 2/6 variants (33.3%) · micro 2/6 cases (33.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.00, nearest other category `coercive_collection` at mean distance 2.50

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.306, nearest other category `administrative_appeal` at mean distance 0.486

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Case involves an administrative appeal process directed to the Prefecture following fine enforcement.

**Taxonomy-derivation rationale (Step 5):** Traced to variant V0006 which includes appeal steps submitted to the Prefecture and a subsequent result ruling.

**Goal-model linkage:** TB (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 1/6 variants (16.7%) · micro 1/6 cases (16.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `coercive_collection` at mean distance 3.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `judicial_appeal` at mean distance 0.360

## Resolve via judicial appeal to the Judge (`judicial_appeal`)

Case involves an appeal brought before a judicial judge after standard enforcement steps.

**Taxonomy-derivation rationale (Step 5):** Traced to variant V0005 where the trace ends with an appeal to the judge following notification and penalties.

**Goal-model linkage:** TC (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 1/6 variants (16.7%) · micro 1/6 cases (16.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `coercive_collection` at mean distance 1.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `administrative_appeal` at mean distance 0.360

## Resolve via coercive credit collection (`coercive_collection`)

Unresolved enforced fine is forwarded to a credit collection agent for coercive recovery.

**Taxonomy-derivation rationale (Step 5):** Traced to variant V0002 which concludes with sending the case for credit collection after all penalties and notifications.

**Goal-model linkage:** TD (Task): Resolve via coercive credit collection

**Coverage:** macro 1/6 variants (16.7%) · micro 1/6 cases (16.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `judicial_appeal` at mean distance 1.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `judicial_appeal` at mean distance 0.429

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0003` / `V0004` (category `payment`): structural=3, profile=0.306

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0002` (`coercive_collection`) / `V0003` (`payment`): structural=1, profile=0.361
- `V0002` (`coercive_collection`) / `V0005` (`judicial_appeal`): structural=1, profile=0.429
- `V0003` (`payment`) / `V0005` (`judicial_appeal`): structural=1, profile=0.401
- `V0002` (`coercive_collection`) / `V0006` (`administrative_appeal`): structural=3, profile=0.456
- `V0003` (`payment`) / `V0006` (`administrative_appeal`): structural=3, profile=0.428
- `V0005` (`judicial_appeal`) / `V0006` (`administrative_appeal`): structural=3, profile=0.360
- `V0002` (`coercive_collection`) / `V0004` (`payment`): structural=4, profile=0.667
- `V0004` (`payment`) / `V0005` (`judicial_appeal`): structural=4, profile=0.571
- `V0004` (`payment`) / `V0006` (`administrative_appeal`): structural=6, profile=0.544

## Residual

1/6 variants (16.7%), 1/6 cases (16.7%) unassigned.

- `V0001`: The narrative only describes the creation and sending of the fine, without any resolution steps such as payment, administrative appeal, judicial appeal, or coercive collection.
# Step 6 — Narrative assignment report

Run: `20260828_171553` | Log: `rtfm_mini` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

6 variants, 6 cases total.

## Resolve via payment (`payment_resolution`)

Resolution of the fine case through offender payment, either timely or after penalties have been applied, helping maximize timely fine revenue and minimize administrative and enforcement costs, evaluated against average time to case closure.

**Taxonomy-derivation rationale (Step 5):** Merged timely_payment and delinquent_payment per the reviewer's requested revision, encompassing both payment variants V0003 and V0004.

**Goal-model linkage:** 12 (Task): Resolve via timely payment; 13 (Task): Resolve via delinquent payment

**Coverage:** macro 2/6 variants (33.3%) · micro 2/6 cases (33.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.00, nearest other category `coercive_credit_collection` at mean distance 2.50

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.306, nearest other category `administrative_appeal_prefecture` at mean distance 0.486

## Resolve via administrative appeal to the Prefecture (`administrative_appeal_prefecture`)

Resolution via an administrative appeal submitted to the Prefecture, preserving due-process rights while impacting administrative cost and fine revenue, measured against 'Time to appeal filing, Prefecture'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative 14, observed in variant V0006 involving appeal insertion, sending, and receiving results.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 1/6 variants (16.7%) · micro 1/6 cases (16.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `coercive_credit_collection` at mean distance 3.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `judicial_appeal_judge` at mean distance 0.360

## Resolve via judicial appeal to the Judge (`judicial_appeal_judge`)

Resolution via a judicial appeal brought before a judge, strongly preserving offender due-process rights while hurting administrative cost, measured against 'Time to appeal filing, Judge'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative 19, evidenced by variant V0005 ending in an appeal to the judge.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 1/6 variants (16.7%) · micro 1/6 cases (16.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `coercive_credit_collection` at mean distance 1.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `administrative_appeal_prefecture` at mean distance 0.360

## Resolve via coercive credit collection (`coercive_credit_collection`)

Resolution of the fine case through coercive credit collection steps after penalties are added, helping fine revenue and hurting administrative costs.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative 20, evidenced by variant V0002 which results in sending the case for credit collection.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** macro 1/6 variants (16.7%) · micro 1/6 cases (16.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `judicial_appeal_judge` at mean distance 1.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `judicial_appeal_judge` at mean distance 0.429

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0003` / `V0004` (category `payment_resolution`): structural=3, profile=0.306

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0002` (`coercive_credit_collection`) / `V0003` (`payment_resolution`): structural=1, profile=0.361
- `V0002` (`coercive_credit_collection`) / `V0005` (`judicial_appeal_judge`): structural=1, profile=0.429
- `V0003` (`payment_resolution`) / `V0005` (`judicial_appeal_judge`): structural=1, profile=0.401
- `V0002` (`coercive_credit_collection`) / `V0006` (`administrative_appeal_prefecture`): structural=3, profile=0.456
- `V0003` (`payment_resolution`) / `V0006` (`administrative_appeal_prefecture`): structural=3, profile=0.428
- `V0005` (`judicial_appeal_judge`) / `V0006` (`administrative_appeal_prefecture`): structural=3, profile=0.360
- `V0002` (`coercive_credit_collection`) / `V0004` (`payment_resolution`): structural=4, profile=0.667
- `V0004` (`payment_resolution`) / `V0005` (`judicial_appeal_judge`): structural=4, profile=0.571
- `V0004` (`payment_resolution`) / `V0006` (`administrative_appeal_prefecture`): structural=6, profile=0.544

## Residual

1/6 variants (16.7%), 1/6 cases (16.7%) unassigned.

- `V0001`: The narrative ends with Send Fine and shows no completion, payment, appeal, or collection steps, so it does not realize any of the defined resolution categories.
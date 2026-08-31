# Step 6 — Narrative assignment report

Run: `20260831_064805` | Log: `rtfm_mini` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

8 variants, 8 cases total.

## Resolve via timely or delinquent payment (`resolve_via_timely_or_delinquent_payment`)

Represents the resolution of a fine via either timely or delinquent payment, advancing Maximize timely fine revenue and minimizing administrative and enforcement costs, evaluated against Average time to case closure.

**Taxonomy-derivation rationale (Step 5):** Merged per reviewer request to exercise Step 9 revise path, combining timely payment (id 12) and delinquent payment (id 13) as observed across variants V0003, V0004, V0007, and V0008.

**Goal-model linkage:** 12 (Task): Resolve via timely payment; 13 (Task): Resolve via delinquent payment

**Coverage:** macro 4/8 variants (50.0%) · micro 4/8 cases (50.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 2.50, nearest other category `resolve_via_coercive_credit_collection` at mean distance 2.25

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.376, nearest other category `resolve_via_judicial_appeal_to_the_judge` at mean distance 0.588

## Resolve via administrative appeal to the Prefecture (`resolve_via_administrative_appeal_to_the_prefecture`)

Represents handling the case through an administrative appeal to the Prefecture, preserving due-process rights while impacting administrative costs and revenue.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative id 14, observed in variant V0006 through insertion and sending of the appeal.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 1/8 variants (12.5%) · micro 1/8 cases (12.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `resolve_via_coercive_credit_collection` at mean distance 3.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `resolve_via_judicial_appeal_to_the_judge` at mean distance 0.360

## Resolve via judicial appeal to the Judge (`resolve_via_judicial_appeal_to_the_judge`)

Represents contesting the fine via a judicial appeal to the Judge, strongly supporting due-process rights but hurting administrative cost efficiency.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative id 19, supported by variant V0005 ending in an appeal to the Judge.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 1/8 variants (12.5%) · micro 1/8 cases (12.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `resolve_via_coercive_credit_collection` at mean distance 1.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `resolve_via_administrative_appeal_to_the_prefecture` at mean distance 0.360

## Resolve via coercive credit collection (`resolve_via_coercive_credit_collection`)

Represents resolving an enforceable fine through coercive credit collection, helping revenue but hurting administrative costs.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative id 20, evidenced by variant V0002 terminating with Send for Credit Collection.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** macro 1/8 variants (12.5%) · micro 1/8 cases (12.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `resolve_via_judicial_appeal_to_the_judge` at mean distance 1.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `resolve_via_judicial_appeal_to_the_judge` at mean distance 0.429

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0004` / `V0007` (category `resolve_via_timely_or_delinquent_payment`): structural=4, profile=0.596
- `V0004` / `V0008` (category `resolve_via_timely_or_delinquent_payment`): structural=4, profile=0.592
- `V0003` / `V0004` (category `resolve_via_timely_or_delinquent_payment`): structural=3, profile=0.306
- `V0007` / `V0008` (category `resolve_via_timely_or_delinquent_payment`): structural=2, profile=0.004
- `V0003` / `V0007` (category `resolve_via_timely_or_delinquent_payment`): structural=1, profile=0.377
- `V0003` / `V0008` (category `resolve_via_timely_or_delinquent_payment`): structural=1, profile=0.380

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0002` (`resolve_via_coercive_credit_collection`) / `V0003` (`resolve_via_timely_or_delinquent_payment`): structural=1, profile=0.361
- `V0002` (`resolve_via_coercive_credit_collection`) / `V0005` (`resolve_via_judicial_appeal_to_the_judge`): structural=1, profile=0.429
- `V0003` (`resolve_via_timely_or_delinquent_payment`) / `V0005` (`resolve_via_judicial_appeal_to_the_judge`): structural=1, profile=0.401
- `V0002` (`resolve_via_coercive_credit_collection`) / `V0007` (`resolve_via_timely_or_delinquent_payment`): structural=2, profile=0.738
- `V0002` (`resolve_via_coercive_credit_collection`) / `V0008` (`resolve_via_timely_or_delinquent_payment`): structural=2, profile=0.741
- `V0005` (`resolve_via_judicial_appeal_to_the_judge`) / `V0007` (`resolve_via_timely_or_delinquent_payment`): structural=2, profile=0.691
- `V0005` (`resolve_via_judicial_appeal_to_the_judge`) / `V0008` (`resolve_via_timely_or_delinquent_payment`): structural=2, profile=0.687
- `V0002` (`resolve_via_coercive_credit_collection`) / `V0006` (`resolve_via_administrative_appeal_to_the_prefecture`): structural=3, profile=0.456
- `V0003` (`resolve_via_timely_or_delinquent_payment`) / `V0006` (`resolve_via_administrative_appeal_to_the_prefecture`): structural=3, profile=0.428
- `V0005` (`resolve_via_judicial_appeal_to_the_judge`) / `V0006` (`resolve_via_administrative_appeal_to_the_prefecture`): structural=3, profile=0.360

## Residual

1/8 variants (12.5%), 1/8 cases (12.5%) unassigned.

- `V0001`: The narrative ends with Send Fine and does not complete payment, appeal, or credit collection.
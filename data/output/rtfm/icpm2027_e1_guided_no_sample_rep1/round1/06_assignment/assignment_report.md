# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_no_sample_rep1` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`resolve_timely_payment`)

Resolution of the fine case through prompt payment by the offender. Advances the softgoal Maximize timely fine revenue (Make +100) and helps Minimize administrative and enforcement cost (Help +50), judged against performance indicators like Average time to case closure.

**Taxonomy-derivation rationale (Step 5):** Traced 1:1 to declared alternative id=12 as a primary path of fine case resolution.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 26/231 variants (11.3%) · micro 49726/150370 cases (33.1%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 6.46, nearest other category `resolve_delinquent_payment` at mean distance 5.68

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.232, nearest other category `resolve_delinquent_payment` at mean distance 0.209

## Resolve via delinquent payment (`resolve_delinquent_payment`)

Resolution of the fine case through delayed payment after penalties are applied. Helps maximize timely fine revenue (Help +50).

**Taxonomy-derivation rationale (Step 5):** Traced 1:1 to declared alternative id=13 representing resolution after penalty application.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 48/231 variants (20.8%) · micro 16848/150370 cases (11.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.72, nearest other category `resolve_administrative_appeal_prefecture` at mean distance 4.91

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.191, nearest other category `resolve_timely_payment` at mean distance 0.209

## Resolve via administrative appeal to the Prefecture (`resolve_administrative_appeal_prefecture`)

Resolution of the case through an administrative appeal lodged with the Prefecture. Preserves offender's due-process rights (Help +50) while incurring administrative costs and impacting revenue.

**Taxonomy-derivation rationale (Step 5):** Traced 1:1 to declared alternative id=14 representing administrative review paths.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 60/231 variants (26.0%) · micro 3641/150370 cases (2.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.01, nearest other category `resolve_judicial_appeal_judge` at mean distance 4.70

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.365, nearest other category `resolve_judicial_appeal_judge` at mean distance 0.404

## Resolve via judicial appeal to the Judge (`resolve_judicial_appeal_judge`)

Resolution of the case through a judicial appeal brought before a Judge. Strongly preserves offender's due-process rights (Make +100) but hurts minimization of administrative and enforcement costs.

**Taxonomy-derivation rationale (Step 5):** Traced 1:1 to declared alternative id=19 representing judicial review paths.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 43/231 variants (18.6%) · micro 389/150370 cases (0.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.68, nearest other category `resolve_administrative_appeal_prefecture` at mean distance 4.70

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.373, nearest other category `resolve_delinquent_payment` at mean distance 0.392

## Resolve via coercive credit collection (`resolve_coercive_credit_collection`)

Resolution of the case through enforced coercive credit collection procedures. Helps maximize revenue (Help +50) but hurts administrative cost minimization and due-process preservation.

**Taxonomy-derivation rationale (Step 5):** Traced 1:1 to declared alternative id=20 representing coercive closure paths.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** macro 42/231 variants (18.2%) · micro 58991/150370 cases (39.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.13, nearest other category `resolve_administrative_appeal_prefecture` at mean distance 4.76

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.189, nearest other category `resolve_judicial_appeal_judge` at mean distance 0.473

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0153` / `V0207` (category `resolve_delinquent_payment`): structural=17, profile=0.344
- `V0153` / `V0208` (category `resolve_delinquent_payment`): structural=17, profile=0.360
- `V0024` / `V0153` (category `resolve_delinquent_payment`): structural=16, profile=0.061
- `V0039` / `V0153` (category `resolve_delinquent_payment`): structural=16, profile=0.359
- `V0065` / `V0153` (category `resolve_delinquent_payment`): structural=16, profile=0.377
- `V0085` / `V0153` (category `resolve_delinquent_payment`): structural=16, profile=0.350
- `V0113` / `V0153` (category `resolve_delinquent_payment`): structural=16, profile=0.377
- `V0153` / `V0164` (category `resolve_delinquent_payment`): structural=16, profile=0.391
- `V0153` / `V0174` (category `resolve_delinquent_payment`): structural=16, profile=0.009
- `V0002` / `V0147` (category `resolve_timely_payment`): structural=15, profile=0.608

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`resolve_coercive_credit_collection`) / `V0004` (`resolve_delinquent_payment`): structural=1, profile=0.355
- `V0001` (`resolve_coercive_credit_collection`) / `V0029` (`resolve_judicial_appeal_judge`): structural=1, profile=0.396
- `V0001` (`resolve_coercive_credit_collection`) / `V0040` (`resolve_judicial_appeal_judge`): structural=1, profile=0.027
- `V0004` (`resolve_delinquent_payment`) / `V0009` (`resolve_coercive_credit_collection`): structural=1, profile=0.354
- `V0004` (`resolve_delinquent_payment`) / `V0014` (`resolve_judicial_appeal_judge`): structural=1, profile=0.022
- `V0004` (`resolve_delinquent_payment`) / `V0018` (`resolve_timely_payment`): structural=1, profile=0.367
- `V0004` (`resolve_delinquent_payment`) / `V0029` (`resolve_judicial_appeal_judge`): structural=1, profile=0.374
- `V0004` (`resolve_delinquent_payment`) / `V0031` (`resolve_judicial_appeal_judge`): structural=1, profile=0.030
- `V0005` (`resolve_delinquent_payment`) / `V0009` (`resolve_coercive_credit_collection`): structural=1, profile=0.711
- `V0005` (`resolve_delinquent_payment`) / `V0031` (`resolve_judicial_appeal_judge`): structural=1, profile=0.387

## Residual

12/231 variants (5.2%), 20775/150370 cases (13.8%) unassigned.

- `V0003`: The case ends with Send Fine and remains unresolved without payment or appeal completion.
- `V0012`: The case involves payment followed by sending fine, which is an incomplete or anomalous resolution path.
- `V0077`: The case ends inconclusively at Send Fine without payment or final appeal resolution.
- `V0083`: The process terminates at Send Appeal to Prefecture without a final resolution.
- `V0086`: The variant ends at Send Appeal to Prefecture without completing the full lifecycle.
- `V0093`: The sequence stops at Send Fine after a judge appeal without conclusion.
- `V0096`: The process ends at Appeal to Judge without reaching case resolution.
- `V0097`: The variant ends at Send Appeal to Prefecture without a final outcome.
- `V0098`: The process terminates at Notify Result Appeal to Offender without final resolution.
- `V0099`: The variant stops at Notify Result Appeal to Offender.
- `V0167`: The outcome is notification of the appeal result rather than final payment, appeal resolution, or credit collection.
- `V0175`: The variant terminates at notification of the appeal result, meaning it does not reach a final payment or collection outcome.
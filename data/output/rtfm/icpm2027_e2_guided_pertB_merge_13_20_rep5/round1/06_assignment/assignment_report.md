# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_pertB_merge_13_20_rep5` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Resolution of the fine case through payment realization, advancing the softgoal to maximize timely fine revenue and helping minimize administrative and enforcement cost, judged against time-to-closure indicators.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative id=12. Supported by frequent variants like V0002 and V0004 where payment successfully closes the fine case.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 61/231 variants (26.4%) · micro 66527/150370 cases (44.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.75, nearest other category `merged_closure` at mean distance 4.96

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.237, nearest other category `merged_closure` at mean distance 0.401

## Merged resolution (`merged_closure`)

Resolution via merged tasks (id=13), helping maximize timely fine revenue while hurting administrative cost and preserving due-process rights.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative id=13. Represented in cases leading to credit collection and direct case completions.

**Goal-model linkage:** 13 (Task): Merged 13+20

**Coverage:** macro 9/231 variants (3.9%) · micro 55/150370 cases (0.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.86, nearest other category `timely_payment` at mean distance 4.96

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.494, nearest other category `timely_payment` at mean distance 0.401

## Resolve via administrative appeal to the Prefecture (`administrative_appeal_prefecture`)

Resolution path involving administrative appeals submitted to the Prefecture, advancing the offender's due-process rights while potentially increasing administrative costs and reducing timely revenue.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative id=14. Evidenced in variants involving 'Insert Date Appeal to Prefecture', 'Send Appeal to Prefecture', and subsequent prefecture responses.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 83/231 variants (35.9%) · micro 3711/150370 cases (2.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.34, nearest other category `timely_payment` at mean distance 5.04

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.387, nearest other category `judicial_appeal_judge` at mean distance 0.413

## Resolve via judicial appeal to the Judge (`judicial_appeal_judge`)

Resolution path involving judicial appeals to the Judge, making a strong positive contribution to preserving the offender's due-process rights while hurting administrative costs and timely revenue.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative id=19. Evidenced in variants containing 'Appeal to Judge' activities.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 64/231 variants (27.7%) · micro 529/150370 cases (0.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.65, nearest other category `administrative_appeal_prefecture` at mean distance 5.26

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.410, nearest other category `administrative_appeal_prefecture` at mean distance 0.413

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0093` / `V0153` (category `judicial_appeal_judge`): structural=18, profile=0.750
- `V0096` / `V0153` (category `judicial_appeal_judge`): structural=18, profile=0.770
- `V0035` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.710
- `V0063` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.746
- `V0069` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.716
- `V0082` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.698
- `V0097` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.762
- `V0120` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.729
- `V0134` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.706
- `V0153` / `V0154` (category `judicial_appeal_judge`): structural=17, profile=0.358

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0002` (`timely_payment`) / `V0048` (`merged_closure`): structural=1, profile=0.500
- `V0004` (`timely_payment`) / `V0014` (`judicial_appeal_judge`): structural=1, profile=0.022
- `V0004` (`timely_payment`) / `V0029` (`judicial_appeal_judge`): structural=1, profile=0.374
- `V0004` (`timely_payment`) / `V0031` (`judicial_appeal_judge`): structural=1, profile=0.030
- `V0005` (`timely_payment`) / `V0031` (`judicial_appeal_judge`): structural=1, profile=0.387
- `V0005` (`timely_payment`) / `V0037` (`judicial_appeal_judge`): structural=1, profile=0.062
- `V0005` (`timely_payment`) / `V0044` (`merged_closure`): structural=1, profile=0.001
- `V0005` (`timely_payment`) / `V0071` (`merged_closure`): structural=1, profile=0.379
- `V0005` (`timely_payment`) / `V0130` (`administrative_appeal_prefecture`): structural=1, profile=0.019
- `V0005` (`timely_payment`) / `V0204` (`judicial_appeal_judge`): structural=1, profile=0.036

## Residual

14/231 variants (6.1%), 79548/150370 cases (52.9%) unassigned.

- `V0001`: The case results in Send for Credit Collection without payment or appeal resolution, falling outside the defined taxonomy categories.
- `V0003`: The narrative ends at Send Fine without any payment or appeal conclusion, so it does not fit the taxonomy categories.
- `V0009`: Despite a partial payment, the case ultimately ends up sent for credit collection, failing to resolve successfully via payment or appeal.
- `V0010`: The case ends with Send for Credit Collection, which does not fit any successful resolution category.
- `V0012`: The sequence involves payment followed by sending the fine, which does not map cleanly to standard resolution paths.
- `V0019`: Although an administrative appeal to the Prefecture is processed, the case ultimately ends in credit collection rather than resolution.
- `V0020`: The case undergoes an administrative appeal to the Prefecture but ultimately results in credit collection.
- `V0025`: The case includes an administrative appeal to the Prefecture but ends with credit collection.
- `V0026`: The narrative ends with Send for Credit Collection, which does not fit timely payment, merged closure, administrative appeal to the prefecture, or judicial appeal to the judge.
- `V0051`: The case involves an administrative appeal to the prefecture and concludes with credit collection rather than timely payment or resolved appeal.
- `V0106`: The case ends with Send for Credit Collection, which does not match any primary resolution category.
- `V0108`: The case concludes with Send for Credit Collection despite intermediate payment and appeal steps.
- `V0111`: The case terminates with Send for Credit Collection.
- `V0123`: The case ends with Send for Credit Collection.
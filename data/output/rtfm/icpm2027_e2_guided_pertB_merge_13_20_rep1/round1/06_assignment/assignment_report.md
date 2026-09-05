# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_pertB_merge_13_20_rep1` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Resolution of the fine case through prompt payment by the offender, advancing the softgoal to maximize timely fine revenue and helping minimize administrative and enforcement costs, evaluated against indicators such as time to fine dispatch and average time to case closure.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative id=12, supported by frequent variants such as V0002 and V0007 where payment successfully closes the case without further appeals.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 56/231 variants (24.2%) · micro 66364/150370 cases (44.1%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.76, nearest other category `merged_closure` at mean distance 4.52

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.265, nearest other category `merged_closure` at mean distance 0.395

## Merged Resolution and Closure (`merged_closure`)

Resolution via merged closure pathways, helping maximize timely fine revenue while hurting the minimization of administrative and enforcement costs and preserving due-process rights, evaluated against average time to case closure.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative id=13 as specified in the goal model, representing cases processed via the merged path.

**Goal-model linkage:** 13 (Task): Merged 13+20

**Coverage:** macro 13/231 variants (5.6%) · micro 583/150370 cases (0.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.72, nearest other category `timely_payment` at mean distance 4.52

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.465, nearest other category `timely_payment` at mean distance 0.395

## Resolve via administrative appeal to the Prefecture (`administrative_appeal_prefecture`)

Resolution of the fine case through an administrative appeal submitted to the Prefecture, preserving the offender's due-process rights while negatively impacting timely fine revenue and enforcement cost minimization, evaluated against the time to appeal filing, Prefecture indicator.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative id=14, evidenced by variants like V0008, V0057, and V0135 that incorporate activities such as Insert Date Appeal to Prefecture and Send Appeal to Prefecture.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 92/231 variants (39.8%) · micro 3733/150370 cases (2.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.52, nearest other category `merged_closure` at mean distance 4.84

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.396, nearest other category `judicial_appeal_judge` at mean distance 0.420

## Resolve via judicial appeal to the Judge (`judicial_appeal_judge`)

Resolution of the fine case through a judicial appeal to the Judge, making a strong positive contribution to preserving the offender's due-process rights while hurting administrative costs and revenue, evaluated against time to appeal filing, Judge.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative id=19, supported by variants such as V0103, V0176, and V0140 containing the Appeal to Judge activity.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 60/231 variants (26.0%) · micro 414/150370 cases (0.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.77, nearest other category `administrative_appeal_prefecture` at mean distance 5.40

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.410, nearest other category `administrative_appeal_prefecture` at mean distance 0.420

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0093` / `V0153` (category `judicial_appeal_judge`): structural=18, profile=0.750
- `V0096` / `V0153` (category `judicial_appeal_judge`): structural=18, profile=0.770
- `V0035` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.710
- `V0063` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.746
- `V0069` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.716
- `V0097` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.762
- `V0120` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.729
- `V0134` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.706
- `V0153` / `V0154` (category `judicial_appeal_judge`): structural=17, profile=0.358
- `V0153` / `V0206` (category `judicial_appeal_judge`): structural=17, profile=0.718

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0002` (`timely_payment`) / `V0012` (`merged_closure`): structural=1, profile=0.462
- `V0004` (`timely_payment`) / `V0014` (`judicial_appeal_judge`): structural=1, profile=0.022
- `V0004` (`timely_payment`) / `V0018` (`merged_closure`): structural=1, profile=0.367
- `V0004` (`timely_payment`) / `V0029` (`judicial_appeal_judge`): structural=1, profile=0.374
- `V0004` (`timely_payment`) / `V0031` (`judicial_appeal_judge`): structural=1, profile=0.030
- `V0004` (`timely_payment`) / `V0085` (`merged_closure`): structural=1, profile=0.006
- `V0005` (`timely_payment`) / `V0031` (`judicial_appeal_judge`): structural=1, profile=0.387
- `V0005` (`timely_payment`) / `V0037` (`judicial_appeal_judge`): structural=1, profile=0.062
- `V0005` (`timely_payment`) / `V0044` (`merged_closure`): structural=1, profile=0.001
- `V0005` (`timely_payment`) / `V0071` (`merged_closure`): structural=1, profile=0.379

## Residual

10/231 variants (4.3%), 79276/150370 cases (52.7%) unassigned.

- `V0001`: The case ends with Send for Credit Collection without payment or appeal resolution, so it does not fit any of the resolution categories.
- `V0003`: The case ends with Send Fine and is incomplete in terms of final resolution.
- `V0009`: Despite an intermediate payment, the case ultimately proceeds to Send for Credit Collection.
- `V0010`: The case terminates with Send for Credit Collection after an intermediate payment.
- `V0017`: The case includes a judicial appeal to the Judge but ultimately results in Send for Credit Collection rather than a positive resolution.
- `V0019`: Although an administrative appeal to the Prefecture is processed, the case ultimately ends in Send for Credit Collection.
- `V0020`: Despite an administrative appeal to the Prefecture, the case terminates in Send for Credit Collection.
- `V0025`: The case processes an administrative appeal to the Prefecture but ultimately ends with Send for Credit Collection.
- `V0026`: The narrative ends with Send for Credit Collection, which does not fit timely payment, merged closure, administrative appeal, or judicial appeal.
- `V0160`: The case ends with credit collection after multiple payments and does not cleanly fit standard resolution pathways.
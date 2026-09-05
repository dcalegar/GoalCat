# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_pertB_merge_13_20_rep2` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Resolution of the fine case through payment realization, advancing the softgoal to maximize timely fine revenue and helping minimize administrative and enforcement cost, judged against time-to-closure indicators.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative id=12 in the goal model. Supported by frequent narrative variants like V0002 and V0007 showing direct payment after fine creation.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 63/231 variants (27.3%) · micro 66539/150370 cases (44.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.66, nearest other category `merged_closure` at mean distance 4.24

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.240, nearest other category `merged_closure` at mean distance 0.309

## Merged case resolution (`merged_closure`)

Resolution of cases through merged enforcement paths (Task 13+20), helping maximize timely fine revenue while hurting administrative cost and preserving due process, judged against average case closure time indicators.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative id=13. Evidenced in various credit collection and closure pathways in the event log.

**Goal-model linkage:** 13 (Task): Merged 13+20

**Coverage:** macro 1/231 variants (0.4%) · micro 1/150370 cases (0.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `administrative_appeal` at mean distance 3.40

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `administrative_appeal` at mean distance 0.280

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Resolution through an administrative appeal process directed to the Prefecture, helping preserve offender due-process rights while impacting revenue and enforcement costs, evaluated against Prefecture appeal timing indicators.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative id=14. Supported by narrative traces containing appeal insertion, sending, and receiving results from the Prefecture (e.g., V0008, V0057).

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 78/231 variants (33.8%) · micro 671/150370 cases (0.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.27, nearest other category `merged_closure` at mean distance 3.40

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.376, nearest other category `merged_closure` at mean distance 0.280

## Resolve via judicial appeal to the Judge (`judicial_appeal`)

Resolution through a judicial appeal to the Judge, making a strong positive contribution to preserving offender due-process rights while hurting administrative costs, judged against Judge appeal timing indicators.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative id=19. Supported by narrative variants showing direct or subsequent judge appeal activities (e.g., V0103, V0176).

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 67/231 variants (29.0%) · micro 415/150370 cases (0.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.67, nearest other category `merged_closure` at mean distance 4.57

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.405, nearest other category `merged_closure` at mean distance 0.296

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0093` / `V0153` (category `judicial_appeal`): structural=18, profile=0.750
- `V0096` / `V0153` (category `judicial_appeal`): structural=18, profile=0.770
- `V0035` / `V0153` (category `judicial_appeal`): structural=17, profile=0.710
- `V0063` / `V0153` (category `judicial_appeal`): structural=17, profile=0.746
- `V0069` / `V0153` (category `judicial_appeal`): structural=17, profile=0.716
- `V0082` / `V0153` (category `judicial_appeal`): structural=17, profile=0.698
- `V0097` / `V0153` (category `judicial_appeal`): structural=17, profile=0.762
- `V0120` / `V0153` (category `judicial_appeal`): structural=17, profile=0.729
- `V0134` / `V0153` (category `judicial_appeal`): structural=17, profile=0.706
- `V0153` / `V0154` (category `judicial_appeal`): structural=17, profile=0.358

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0004` (`timely_payment`) / `V0014` (`judicial_appeal`): structural=1, profile=0.022
- `V0004` (`timely_payment`) / `V0029` (`judicial_appeal`): structural=1, profile=0.374
- `V0004` (`timely_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.030
- `V0005` (`timely_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.387
- `V0005` (`timely_payment`) / `V0037` (`judicial_appeal`): structural=1, profile=0.062
- `V0005` (`timely_payment`) / `V0184` (`judicial_appeal`): structural=1, profile=0.060
- `V0006` (`timely_payment`) / `V0014` (`judicial_appeal`): structural=1, profile=0.390
- `V0006` (`timely_payment`) / `V0205` (`judicial_appeal`): structural=1, profile=0.737
- `V0007` (`timely_payment`) / `V0063` (`judicial_appeal`): structural=1, profile=0.354
- `V0007` (`timely_payment`) / `V0154` (`judicial_appeal`): structural=1, profile=0.075

## Residual

22/231 variants (9.5%), 82744/150370 cases (55.0%) unassigned.

- `V0001`: The case ends with Send for Credit Collection without payment or appeal resolution, meaning it does not fit any of the resolution categories.
- `V0003`: The case ends with Send Fine and lacks payment or appeal outcomes, making it part of the residual.
- `V0008`: The case ends with Send Appeal to Prefecture without a final resolution, so it does not fit any completed resolution category.
- `V0009`: Despite a partial payment, the case ultimately ends with Send for Credit Collection rather than successful resolution.
- `V0010`: The case concludes with Send for Credit Collection, bypassing normal payment or appeal resolution.
- `V0011`: The variant ends by sending an appeal to the Prefecture without reaching a final closure.
- `V0012`: The case finishes after sending the fine, with no payment or appeal resolution.
- `V0015`: The case terminates at Send Appeal to Prefecture without reaching a final outcome.
- `V0017`: The case involves a judicial appeal but ultimately concludes with Send for Credit Collection rather than resolution.
- `V0019`: Despite undergoing an administrative appeal, the case ultimately ends with Send for Credit Collection.
- `V0020`: The case features an administrative appeal but concludes uncollected via Send for Credit Collection.
- `V0025`: The case features an administrative appeal but ultimately results in Send for Credit Collection.
- `V0026`: The narrative ends with Send for Credit Collection, which does not match timely payment, administrative appeal, judicial appeal, or merged closure.
- `V0040`: The narrative culminates in Send for Credit Collection, which does not fit any of the resolution categories.
- `V0043`: The case ends with Send for Credit Collection, which does not realize any of the defined resolution goals.
- `V0106`: The case ends with Send for Credit Collection, which does not fit any of the four defined categories.
- `V0108`: The process concludes by sending the case for credit collection, making it part of the residual.
- `V0111`: The process terminates with Send for Credit Collection, which falls outside the specific categories.
- `V0123`: The narrative ends with credit collection actions rather than a defined category resolution.
- `V0160`: The case ends in credit collection rather than timely payment or a recognized appeal resolution.
- `V0169`: The narrative involves multiple payments but ultimately ends in credit collection rather than timely resolution.
- `V0173`: The narrative ends in credit collection without completing successful payment or appeal resolution.
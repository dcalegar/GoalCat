# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_pertB_merge_13_20_rep1` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Resolution of the fine case through payment realization, advancing the 'Maximize timely fine revenue' softgoal and helping 'Minimize administrative & enforcement cost'. Judged against indicator id=114 (Average time to case closure).

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative id=12 as supported by variants like V0002 and V0007.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 78/231 variants (33.8%) · micro 66574/150370 cases (44.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.06, nearest other category `administrative_appeal` at mean distance 5.11

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.227, nearest other category `judicial_appeal` at mean distance 0.428

## Merged 13+20 (`merged_closure`)

Resolution through merged enforcement and credit collection procedures, helping 'Maximize timely fine revenue' while hurting 'Minimize administrative & enforcement cost' and preserving due-process rights. Judged against indicator id=114.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative id=13 as observed in variants like V0001.

**Goal-model linkage:** 13 (Task): Merged 13+20

**Coverage:** macro 7/231 variants (3.0%) · micro 18/150370 cases (0.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.29, nearest other category `administrative_appeal` at mean distance 5.43

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.169, nearest other category `timely_payment` at mean distance 0.508

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Resolution via administrative appeal processes, preserving the offender's due-process rights (softgoal id=14) while impacting administration costs and revenue. Judged against indicator id=113.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative id=14 as reflected in variants such as V0008.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 68/231 variants (29.4%) · micro 3904/150370 cases (2.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.89, nearest other category `judicial_appeal` at mean distance 4.99

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.366, nearest other category `judicial_appeal` at mean distance 0.417

## Resolve via judicial appeal to the Judge (`judicial_appeal`)

Resolution through judicial appeals to the Judge, making a strong positive contribution to preserving offender's due-process rights while hurting cost and revenue softgoals. Judged against indicator id=175.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative id=19, observed in variants such as V0103 and V0140.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 61/231 variants (26.4%) · micro 531/150370 cases (0.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.39, nearest other category `administrative_appeal` at mean distance 4.99

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.403, nearest other category `administrative_appeal` at mean distance 0.417

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
- `V0153` / `V0154` (category `judicial_appeal`): structural=17, profile=0.358
- `V0153` / `V0167` (category `judicial_appeal`): structural=17, profile=0.716

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0004` (`timely_payment`) / `V0014` (`judicial_appeal`): structural=1, profile=0.022
- `V0004` (`timely_payment`) / `V0029` (`judicial_appeal`): structural=1, profile=0.374
- `V0004` (`timely_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.030
- `V0005` (`timely_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.387
- `V0005` (`timely_payment`) / `V0037` (`judicial_appeal`): structural=1, profile=0.062
- `V0005` (`timely_payment`) / `V0071` (`merged_closure`): structural=1, profile=0.379
- `V0005` (`timely_payment`) / `V0184` (`judicial_appeal`): structural=1, profile=0.060
- `V0006` (`timely_payment`) / `V0014` (`judicial_appeal`): structural=1, profile=0.390
- `V0006` (`timely_payment`) / `V0088` (`merged_closure`): structural=1, profile=0.390
- `V0006` (`timely_payment`) / `V0205` (`judicial_appeal`): structural=1, profile=0.737

## Residual

17/231 variants (7.4%), 79343/150370 cases (52.8%) unassigned.

- `V0001`: The variant ends with Send for Credit Collection, which does not directly realize timely payment, merged closure, or any appeal process.
- `V0003`: The variant ends with Send Fine and lacks payment or appeal resolution.
- `V0009`: Despite an intermediate payment, the case ultimately ends with Send for Credit Collection.
- `V0010`: The case ultimately results in Send for Credit Collection.
- `V0012`: The case ends with Send Fine following a payment and does not match the target resolution outcomes.
- `V0026`: The case ends with Send for Credit Collection.
- `V0043`: The case ultimately ends with Send for Credit Collection.
- `V0077`: The process sequence is incomplete or atypical, ending abruptly without a clear resolution category.
- `V0106`: The final outcome is sending for credit collection, which does not fit timely payment or appeals directly.
- `V0108`: The case involves both payment and a final step of sending for credit collection.
- `V0111`: The case ends by being sent for credit collection.
- `V0123`: The case finishes with credit collection procedures.
- `V0129`: The outcome is sending for credit collection.
- `V0133`: The final activity is sending for credit collection.
- `V0134`: The narrative finishes by sending the case for credit collection.
- `V0135`: The process terminates with credit collection.
- `V0138`: The final step is sending for credit collection.
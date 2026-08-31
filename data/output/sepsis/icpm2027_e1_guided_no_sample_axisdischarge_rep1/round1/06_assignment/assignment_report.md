# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_no_sample_axisdischarge_rep1` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Release A (`release_a`)

Patient discharge via Release A pathway. This pathway helps avoid post-discharge deterioration and is evaluated against post-discharge ER return metrics.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release A (id 17) under the OR-decomposition of goal 6. Helps avoid post-discharge deterioration.

**Goal-model linkage:** 17 (Task): Release A

**Coverage:** macro 623/846 variants (73.6%) · micro 671/1050 cases (63.9%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.43, nearest other category `release_b` at mean distance 15.10

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.352, nearest other category `release_d` at mean distance 0.438

## Release B (`release_b`)

Patient discharge via Release B pathway. This pathway helps avoid post-discharge deterioration and is evaluated against post-discharge ER return metrics.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release B (id 18) under the OR-decomposition of goal 6. Helps avoid post-discharge deterioration.

**Goal-model linkage:** 18 (Task): Release B

**Coverage:** macro 55/846 variants (6.5%) · micro 56/1050 cases (5.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 16.61, nearest other category `release_a` at mean distance 15.10

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.248, nearest other category `release_d` at mean distance 0.546

## Release C (`release_c`)

Patient discharge via Release C pathway.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release C (id 19) under the OR-decomposition of goal 6.

**Goal-model linkage:** 19 (Task): Release C

**Coverage:** macro 25/846 variants (3.0%) · micro 25/1050 cases (2.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 22.70, nearest other category `release_a` at mean distance 18.12

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.268, nearest other category `release_d` at mean distance 0.433

## Release D (`release_d`)

Patient discharge via Release D pathway.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release D (id 20) under the OR-decomposition of goal 6.

**Goal-model linkage:** 20 (Task): Release D

**Coverage:** macro 24/846 variants (2.8%) · micro 24/1050 cases (2.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 19.12, nearest other category `release_a` at mean distance 17.06

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.300, nearest other category `release_c` at mean distance 0.433

## Release E (`release_e`)

Patient discharge via Release E pathway.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release E (id 21) under the OR-decomposition of goal 6.

**Goal-model linkage:** 21 (Task): Release E

**Coverage:** macro 6/846 variants (0.7%) · micro 6/1050 cases (0.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 17.67, nearest other category `release_a` at mean distance 16.38

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.253, nearest other category `release_d` at mean distance 0.440

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0274` / `V0710` (category `release_c`): structural=177, profile=0.390
- `V0084` / `V0710` (category `release_c`): structural=174, profile=0.253
- `V0615` / `V0710` (category `release_c`): structural=174, profile=0.504
- `V0138` / `V0710` (category `release_c`): structural=173, profile=0.253
- `V0313` / `V0710` (category `release_c`): structural=173, profile=0.165
- `V0314` / `V0710` (category `release_c`): structural=173, profile=0.148
- `V0427` / `V0710` (category `release_c`): structural=173, profile=0.418
- `V0433` / `V0710` (category `release_c`): structural=173, profile=0.313
- `V0601` / `V0710` (category `release_c`): structural=173, profile=0.248
- `V0710` / `V0747` (category `release_c`): structural=173, profile=0.049

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0022` (`release_a`) / `V0274` (`release_c`): structural=1, profile=0.374
- `V0037` (`release_b`) / `V0706` (`release_a`): structural=1, profile=0.359
- `V0100` (`release_a`) / `V0586` (`release_b`): structural=1, profile=0.339
- `V0396` (`release_a`) / `V0410` (`release_d`): structural=1, profile=0.334
- `V0008` (`release_a`) / `V0037` (`release_b`): structural=2, profile=0.337
- `V0014` (`release_a`) / `V0691` (`release_b`): structural=2, profile=0.388
- `V0014` (`release_a`) / `V0725` (`release_d`): structural=2, profile=0.674
- `V0028` (`release_a`) / `V0586` (`release_b`): structural=2, profile=0.414
- `V0035` (`release_a`) / `V0426` (`release_c`): structural=2, profile=0.445
- `V0037` (`release_b`) / `V0209` (`release_a`): structural=2, profile=0.339

## Residual

113/846 variants (13.4%), 268/1050 cases (25.5%) unassigned.

- `V0001`: The narrative ends at ER Sepsis Triage and does not involve any patient discharge pathway.
- `V0002`: The narrative ends at CRP and does not involve any patient discharge pathway.
- `V0003`: The narrative ends at Leucocytes and does not involve any patient discharge pathway.
- `V0004`: The narrative ends at IV Antibiotics and does not involve any patient discharge pathway.
- `V0005`: The narrative ends at LacticAcid and does not involve any patient discharge pathway.
- `V0006`: The narrative ends at IV Antibiotics and does not involve any patient discharge pathway.
- `V0007`: The narrative ends at IV Antibiotics and does not involve any patient discharge pathway.
- `V0009`: The narrative ends at IV Antibiotics and does not involve any patient discharge pathway.
- `V0010`: The narrative ends at ER Sepsis Triage and does not involve any patient discharge pathway.
- `V0011`: The narrative ends at IV Antibiotics and does not involve any patient discharge pathway.
- `V0012`: The narrative ends at IV Antibiotics and does not involve any patient discharge pathway.
- `V0013`: The narrative ends at Leucocytes and does not involve any patient discharge pathway.
- `V0017`: The narrative ends at ER Sepsis Triage and does not involve any patient discharge pathway.
- `V0019`: The narrative ends at IV Antibiotics and does not involve any patient discharge pathway.
- `V0020`: The narrative ends at CRP and does not involve any patient discharge pathway.
- `V0024`: The narrative ends at Admission NC and does not involve any patient discharge pathway.
- `V0025`: The narrative ends at IV Antibiotics and does not involve any patient discharge pathway.
- `V0027`: The narrative ends at IV Antibiotics and does not involve any patient discharge pathway.
- `V0029`: The narrative ends at Leucocytes and does not involve any patient discharge pathway.
- `V0031`: The narrative ends at LacticAcid and does not involve any patient discharge pathway.
- `V0034`: The narrative ends at IV Liquid and does not involve any patient discharge pathway.
- `V0036`: The narrative ends at CRP and does not involve any patient discharge pathway.
- `V0038`: The narrative ends at IV Antibiotics and does not involve any patient discharge pathway.
- `V0040`: The narrative ends at Admission NC and does not involve any patient discharge pathway.
- `V0043`: The narrative ends at LacticAcid and does not involve any patient discharge pathway.
- `V0050`: The narrative ends at CRP and does not involve any patient discharge pathway.
- `V0056`: The narrative ends with IV Antibiotics and does not reach any patient discharge category.
- `V0062`: The narrative ends with IV Antibiotics and does not reach any patient discharge category.
- `V0081`: The narrative ends with IV Liquid and does not reach any patient discharge category.
- `V0088`: The narrative ends with IV Antibiotics and does not reach any patient discharge category.
- `V0092`: The narrative ends with LacticAcid and does not reach any patient discharge category.
- `V0111`: The outcome is Admission NC, which does not match any discharge pathway category.
- `V0127`: The outcome is LacticAcid, which does not match any discharge pathway category.
- `V0132`: The outcome is IV Antibiotics, which does not match any discharge pathway category.
- `V0133`: The outcome is IV Antibiotics, which does not match any discharge pathway category.
- `V0137`: The outcome is LacticAcid, which does not match any discharge pathway category.
- `V0146`: The outcome is Leucocytes, which does not match any discharge pathway category.
- `V0148`: The outcome is IV Antibiotics, which does not match any discharge pathway category.
- `V0187`: Incomplete path ending in CRP without any release pathway.
- `V0197`: Incomplete path ending in Leucocytes without any release pathway.
- `V0217`: The outcome is IV Antibiotics, which does not match any release category.
- `V0219`: The outcome is Leucocytes, which does not match any release category.
- `V0232`: The outcome is IV Antibiotics, which does not match any release category.
- `V0234`: The outcome is Leucocytes, which does not match any release category.
- `V0260`: Outcome is IV Antibiotics; does not reach any release pathway.
- `V0268`: Outcome is Leucocytes; does not reach any release pathway.
- `V0287`: Outcome is CRP; does not reach any release pathway.
- `V0292`: Outcome is Leucocytes; does not reach any release pathway.
- `V0295`: Outcome is IV Antibiotics; does not reach any release pathway.
- `V0302`: The narrative does not reach a discharge pathway and ends at ER Sepsis Triage.
- `V0305`: The narrative ends with IV Antibiotics and does not reach any release pathway.
- `V0322`: The narrative ends at IV Antibiotics without reaching a discharge category.
- `V0325`: The narrative ends at IV Antibiotics and does not reach a discharge category.
- `V0330`: The narrative ends at IV Liquid without reaching a discharge category.
- `V0336`: The narrative ends at CRP without reaching a discharge category.
- `V0342`: The narrative ends at CRP without reaching a discharge category.
- `V0349`: The narrative ends at ER Sepsis Triage without reaching a discharge category.
- `V0365`: The narrative ends with Leucocytes and does not contain any discharge pathway activity.
- `V0368`: The narrative ends with Admission NC and does not reach any discharge category.
- `V0374`: The narrative ends with Leucocytes and lacks any discharge pathway activity.
- `V0378`: The narrative stops at IV Antibiotics and does not realize any discharge pathway.
- `V0379`: The narrative ends with IV Antibiotics without reaching a discharge category.
- `V0415`: The narrative ends with Admission NC and does not reach any discharge category.
- `V0417`: The narrative ends with ER Triage and does not complete a patient discharge pathway.
- `V0429`: The narrative ends with IV Antibiotics and does not reach any discharge category.
- `V0462`: The narrative ends with CRP and does not reach any discharge category.
- `V0488`: The narrative stops at IV Liquid and does not reach a discharge category.
- `V0492`: The narrative terminates at IV Liquid without reaching discharge.
- `V0495`: The narrative stops at IV Antibiotics without reaching a discharge category.
- `V0501`: The narrative ends with IV Liquid and does not reach any of the specified release pathways.
- `V0502`: The narrative ends with Admission NC and does not conclude with a release pathway.
- `V0507`: The narrative terminates at IV Antibiotics and does not reach a discharge category.
- `V0510`: The narrative ends with IV Antibiotics and lacks a release activity.
- `V0516`: The narrative ends with Leucocytes and does not reach any release pathway.
- `V0517`: The narrative terminates at ER Triage without any discharge event.
- `V0549`: The narrative ends with IV Liquid and does not realize any release category.
- `V0565`: The variant outcome is Admission NC, which does not match any of the release taxonomy categories.
- `V0575`: The variant outcome is Leucocytes, which does not match any of the release taxonomy categories.
- `V0580`: The variant outcome is CRP, which does not match any of the release taxonomy categories.
- `V0584`: The variant outcome is IV Liquid, which does not match any of the release taxonomy categories.
- `V0585`: The variant outcome is LacticAcid, which does not match any of the release taxonomy categories.
- `V0587`: The variant outcome is CRP, which does not match any of the release taxonomy categories.
- `V0592`: The variant outcome is IV Antibiotics, which does not match any of the release taxonomy categories.
- `V0636`: The outcome is LacticAcid, which does not correspond to any known release pathway in the taxonomy.
- `V0644`: The outcome is CRP, which does not correspond to any known release pathway in the taxonomy.
- `V0645`: The outcome is LacticAcid, which does not correspond to any known release pathway in the taxonomy.
- `V0654`: The variant does not end with any release pathway matching the taxonomy categories.
- `V0663`: The variant ends with Admission NC and does not reach any release pathway.
- `V0664`: The variant ends with IV Liquid and does not reach any release pathway.
- `V0676`: The variant ends with IV Antibiotics and does not reach any release pathway.
- `V0679`: The variant ends with IV Antibiotics and does not reach any release pathway.
- `V0685`: The variant ends with IV Antibiotics and does not reach any release pathway.
- `V0689`: The variant ends with IV Antibiotics and does not reach any release pathway.
- `V0694`: The variant ends with ER Sepsis Triage and does not reach any release pathway.
- `V0703`: The narrative terminates at IV Liquid rather than any of the discharge pathways.
- `V0707`: The narrative terminates at Admission NC without completing a discharge pathway.
- `V0708`: The narrative terminates at IV Antibiotics without completing a discharge pathway.
- `V0713`: The narrative terminates at IV Antibiotics without completing a discharge pathway.
- `V0742`: The narrative terminates at LacticAcid without completing a discharge pathway.
- `V0750`: The narrative terminates at IV Antibiotics without completing a discharge pathway.
- `V0759`: The narrative ends with IV Antibiotics and does not realize any of the discharge release pathways.
- `V0764`: The process terminates at ER Sepsis Triage and does not discharge the patient.
- `V0772`: The narrative terminates at CRP and does not include any release category.
- `V0774`: The process terminates at ER Sepsis Triage without any discharge event.
- `V0775`: The process terminates at CRP without reaching a release pathway.
- `V0777`: The process terminates at Leucocytes without reaching a release pathway.
- `V0778`: The process terminates at Leucocytes without reaching a release pathway.
- `V0791`: The process terminates at IV Antibiotics without reaching a release category.
- `V0816`: The narrative ends with 'IV Antibiotics' and does not complete any discharge pathway.
- `V0820`: The narrative ends with 'LacticAcid' and does not complete any discharge pathway.
- `V0826`: The narrative ends with 'Admission NC' and does not complete any discharge pathway.
- `V0832`: The narrative ends with 'IV Antibiotics' and does not complete any discharge pathway.
- `V0843`: The narrative ends with 'IV Liquid' and does not complete any discharge pathway.
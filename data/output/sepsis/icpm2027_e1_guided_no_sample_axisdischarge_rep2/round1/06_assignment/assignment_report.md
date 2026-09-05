# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_no_sample_axisdischarge_rep2` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Release A discharge (`release_a`)

Discharge via Release A, advancing the softgoal Avoid post-discharge deterioration and measured against Post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative Release A (id=17) under the OR decomposition of goal id=6.

**Goal-model linkage:** 17 (Task): Release A

**Coverage:** macro 598/846 variants (70.7%) · micro 646/1050 cases (61.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.43, nearest other category `release_b` at mean distance 15.09

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.348, nearest other category `release_d` at mean distance 0.444

## Release B discharge (`release_b`)

Discharge via Release B, advancing the softgoal Avoid post-discharge deterioration and measured against Post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative Release B (id=18) under the OR decomposition of goal id=6.

**Goal-model linkage:** 18 (Task): Release B

**Coverage:** macro 55/846 variants (6.5%) · micro 56/1050 cases (5.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 16.61, nearest other category `release_a` at mean distance 15.09

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.248, nearest other category `release_d` at mean distance 0.545

## Release C discharge (`release_c`)

Discharge via Release C under the OR decomposition of goal id=6.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative Release C (id=19) under the OR decomposition of goal id=6.

**Goal-model linkage:** 19 (Task): Release C

**Coverage:** macro 24/846 variants (2.8%) · micro 24/1050 cases (2.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 23.33, nearest other category `release_a` at mean distance 18.49

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.255, nearest other category `release_d` at mean distance 0.437

## Release D discharge (`release_d`)

Discharge via Release D under the OR decomposition of goal id=6.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative Release D (id=20) under the OR decomposition of goal id=6.

**Goal-model linkage:** 20 (Task): Release D

**Coverage:** macro 23/846 variants (2.7%) · micro 23/1050 cases (2.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 19.17, nearest other category `release_a` at mean distance 16.94

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.296, nearest other category `release_c` at mean distance 0.437

## Release E discharge (`release_e`)

Discharge via Release E under the OR decomposition of goal id=6.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative Release E (id=21) under the OR decomposition of goal id=6.

**Goal-model linkage:** 21 (Task): Release E

**Coverage:** macro 6/846 variants (0.7%) · micro 6/1050 cases (0.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 17.67, nearest other category `release_a` at mean distance 16.38

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.253, nearest other category `release_d` at mean distance 0.443

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0274` / `V0710` (category `release_c`): structural=177, profile=0.390
- `V0084` / `V0710` (category `release_c`): structural=174, profile=0.253
- `V0138` / `V0710` (category `release_c`): structural=173, profile=0.253
- `V0313` / `V0710` (category `release_c`): structural=173, profile=0.165
- `V0314` / `V0710` (category `release_c`): structural=173, profile=0.148
- `V0427` / `V0710` (category `release_c`): structural=173, profile=0.418
- `V0433` / `V0710` (category `release_c`): structural=173, profile=0.313
- `V0601` / `V0710` (category `release_c`): structural=173, profile=0.248
- `V0710` / `V0747` (category `release_c`): structural=173, profile=0.049
- `V0423` / `V0710` (category `release_c`): structural=172, profile=0.126

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

140/846 variants (16.5%), 295/1050 cases (28.1%) unassigned.

- `V0001`: This narrative ends in ER Sepsis Triage and does not reach any discharge activity.
- `V0002`: This narrative ends in CRP testing and does not reach any discharge activity.
- `V0003`: This narrative ends in Leucocytes testing and does not reach any discharge activity.
- `V0004`: This narrative ends in IV Antibiotics and does not reach any discharge activity.
- `V0005`: This narrative ends in LacticAcid testing and does not reach any discharge activity.
- `V0006`: This narrative ends in IV Antibiotics and does not reach any discharge activity.
- `V0007`: This narrative ends in IV Antibiotics and does not reach any discharge activity.
- `V0009`: This narrative ends in IV Antibiotics and does not reach any discharge activity.
- `V0010`: This narrative ends in ER Sepsis Triage and does not reach any discharge activity.
- `V0011`: This narrative ends in IV Antibiotics and does not reach any discharge activity.
- `V0012`: This narrative ends in IV Antibiotics and does not reach any discharge activity.
- `V0013`: This narrative ends in Leucocytes testing and does not reach any discharge activity.
- `V0017`: This narrative ends in ER Sepsis Triage and does not reach any discharge activity.
- `V0019`: This narrative ends in IV Antibiotics and does not reach any discharge activity.
- `V0020`: This narrative ends in CRP testing and does not reach any discharge activity.
- `V0024`: This narrative ends in Admission NC and does not reach any specific discharge category.
- `V0025`: This narrative ends in IV Antibiotics and does not reach any discharge activity.
- `V0027`: The narrative ends prematurely with IV Antibiotics and does not reach any discharge category.
- `V0029`: The narrative ends with Leucocytes and does not reach any discharge category.
- `V0031`: The narrative ends with LacticAcid and does not reach any discharge category.
- `V0034`: The narrative ends with IV Liquid and does not reach any discharge category.
- `V0036`: The narrative ends with CRP and does not reach any discharge category.
- `V0038`: The narrative ends with IV Antibiotics and does not reach any discharge category.
- `V0040`: The narrative ends with Admission NC and does not reach any discharge category.
- `V0043`: The narrative ends with LacticAcid and does not reach any discharge category.
- `V0050`: The narrative ends with CRP and does not reach any discharge category.
- `V0056`: The narrative ends with IV Antibiotics and does not reach any discharge category.
- `V0062`: The narrative ends with IV Antibiotics and does not reach any discharge category.
- `V0081`: The narrative ends with IV Liquid and does not reach any discharge category.
- `V0088`: The narrative ends with IV Antibiotics and does not reach any discharge category.
- `V0092`: The narrative ends with LacticAcid and does not reach any discharge category.
- `V0111`: The outcome is Admission NC, with no final discharge activity corresponding to the taxonomy categories.
- `V0127`: The variant terminates at LacticAcid without completing any of the specified release activities.
- `V0132`: The variant ends at IV Antibiotics and does not reach any discharge activity.
- `V0133`: The variant terminates at IV Antibiotics without performing a release activity.
- `V0137`: The variant ends at LacticAcid and does not include any discharge actions.
- `V0146`: The variant ends at Leucocytes without reaching a release activity.
- `V0148`: The variant terminates at IV Antibiotics without performing a discharge step.
- `V0151`: The narrative ends with Release D, but does not specify the goal ID=6 OR decomposition context properly or lacks sufficient matching markers for release categories A-E in a recognizable way, or corresponds to residual.
- `V0187`: The narrative does not conclude with any recognized discharge activity.
- `V0197`: The narrative does not conclude with any recognized discharge activity.
- `V0217`: The narrative ends with IV Antibiotics and does not reach any discharge activity.
- `V0219`: The narrative ends with Leucocytes and does not reach any discharge activity.
- `V0232`: The outcome is IV Antibiotics, which does not match any release category.
- `V0234`: The outcome is Leucocytes, which does not match any release category.
- `V0260`: The narrative ends at IV Antibiotics and does not reach any discharge category.
- `V0268`: The narrative ends at Leucocytes and does not culminate in any discharge category.
- `V0287`: The process terminates at CRP and does not reach any discharge category.
- `V0292`: The narrative ends at Leucocytes without reaching any discharge milestone.
- `V0295`: The process stops at IV Antibiotics and does not reach a discharge category.
- `V0302`: The process terminates at ER Sepsis Triage and does not reach a discharge activity.
- `V0305`: The process terminates at IV Antibiotics without reaching any discharge milestone.
- `V0322`: The process terminates at IV Antibiotics without reaching a discharge activity.
- `V0325`: The process terminates at IV Antibiotics without reaching a discharge activity.
- `V0330`: The outcome is IV Liquid, which does not match any of the release discharge categories.
- `V0336`: The outcome is CRP, which does not match any of the release categories.
- `V0342`: The outcome is CRP, which does not match any of the release categories.
- `V0349`: The outcome is ER Sepsis Triage, which does not match any of the release categories.
- `V0365`: The narrative ends with Leucocytes and does not culminate in any of the specified release types.
- `V0368`: The narrative terminates at Admission NC and does not reach a release category.
- `V0374`: The narrative ends with Leucocytes and does not reach any release category.
- `V0378`: The narrative ends with IV Antibiotics and does not reach a discharge category.
- `V0379`: The narrative ends with IV Antibiotics and does not reach a discharge category.
- `V0415`: The narrative ends at Admission NC without any discharge event.
- `V0417`: The narrative ends at ER Triage without any discharge event.
- `V0429`: The narrative ends with IV Antibiotics and does not reach any discharge category.
- `V0462`: The narrative outcome is CRP rather than a recognized release category.
- `V0488`: The narrative ends with IV Liquid and does not reach any discharge category.
- `V0492`: The narrative ends with IV Liquid and does not reach any discharge category.
- `V0495`: The narrative ends with IV Antibiotics and does not reach any discharge category.
- `V0501`: The narrative ends with IV Liquid and does not reach a discharge or release activity.
- `V0502`: The narrative ends with Admission NC and does not reach a discharge or release activity.
- `V0504`: The narrative ends with Return ER after Release A, so it does not fit a standard release category.
- `V0505`: The narrative ends with Return ER after Release A, so it does not fit a standard release category.
- `V0507`: The narrative ends with IV Antibiotics and does not reach a discharge or release activity.
- `V0508`: The narrative ends with Return ER after Release A, so it does not fit a standard release category.
- `V0510`: The narrative ends with IV Antibiotics and does not reach a discharge or release activity.
- `V0515`: The narrative ends with Return ER after Release A, so it does not fit a standard release category.
- `V0516`: The narrative ends with Leucocytes and does not reach a discharge or release activity.
- `V0517`: The narrative ends with ER Triage and does not reach a discharge or release activity.
- `V0519`: The narrative ends with Return ER after Release A, so it does not fit a standard release category.
- `V0520`: The narrative ends with Return ER after Release A, so it does not fit a standard release category.
- `V0549`: The narrative ends in IV Liquid and does not reach a discharge category.
- `V0556`: The narrative outcome is Return ER after a Release A, which does not cleanly match any final release goal category due to the post-discharge return.
- `V0558`: The narrative outcome is Return ER after a Release A, which does not cleanly match any final release goal category due to the post-discharge return.
- `V0559`: The narrative outcome is Return ER after a Release A, which does not cleanly match any final release goal category due to the post-discharge return.
- `V0560`: The narrative outcome is Return ER after a Release A, which does not cleanly match any final release goal category due to the post-discharge return.
- `V0564`: The narrative outcome is Return ER after a Release A, which does not cleanly match any final release goal category due to the post-discharge return.
- `V0565`: The narrative terminates at Admission NC, meaning no discharge category is realized.
- `V0567`: The narrative outcome is Return ER after a Release A, which does not cleanly match any final release goal category due to the post-discharge return.
- `V0573`: The narrative outcome is Return ER after a Release A, which does not cleanly match any final release goal category due to the post-discharge return.
- `V0575`: The narrative terminates early at Leucocytes, meaning no discharge category is realized.
- `V0580`: The process terminates at CRP and does not reach any discharge activity.
- `V0584`: The process terminates at IV Liquid and does not reach a discharge category.
- `V0585`: The process terminates at LacticAcid without completing any discharge.
- `V0587`: The process terminates at CRP without any discharge event.
- `V0592`: The process terminates at IV Antibiotics without any discharge outcome.
- `V0605`: Although it ends with Release A before a return, the ultimate outcome is Return ER, rendering the discharge tracking for post-discharge deterrence unsuccessful or outside standard successful discharge categories.
- `V0614`: The narrative leads to Return ER after Release A, therefore not fulfilling the long-term non-deterioration goal successfully.
- `V0615`: Despite containing Release C, the case culminates in Return ER, making it fall into the residual.
- `V0625`: The case ends with Return ER following Release A, meaning it does not fulfill the successful avoidance of post-discharge deterioration.
- `V0636`: The narrative ends in LacticAcid without any discharge or release activity, fitting none of the discharge categories.
- `V0644`: The narrative ends in CRP without any discharge or release activity, fitting none of the discharge categories.
- `V0645`: The narrative ends in LacticAcid without any discharge or release activity, fitting none of the discharge categories.
- `V0654`: The narrative ends with Leucocytes rather than any discharge category.
- `V0663`: The narrative ends with Admission NC and does not reach any discharge category.
- `V0664`: The process terminates with IV Liquid and does not reach a discharge category.
- `V0676`: The narrative ends with IV Antibiotics and does not reach a discharge activity.
- `V0679`: The narrative ends with IV Antibiotics without reaching a discharge activity.
- `V0685`: The narrative ends with IV Antibiotics and does not reach a discharge activity.
- `V0689`: The narrative terminates at IV Antibiotics without a discharge event.
- `V0694`: The narrative stops at ER Sepsis Triage and does not reach any discharge category.
- `V0703`: The narrative ends with IV Liquid and does not reach any discharge category.
- `V0707`: The narrative terminates at Admission NC without reaching any discharge outcome.
- `V0708`: The narrative terminates at IV Antibiotics and does not reach a discharge category.
- `V0713`: The narrative terminates at IV Antibiotics and does not reach a discharge category.
- `V0742`: The outcome is LacticAcid, which does not match any discharge category in the taxonomy.
- `V0750`: The outcome is IV Antibiotics, which does not match any discharge category in the taxonomy.
- `V0759`: The narrative ends with IV Antibiotics and does not reach any discharge event.
- `V0764`: The narrative terminates early at ER Sepsis Triage and does not reach discharge.
- `V0772`: The narrative concludes with CRP and does not reach a discharge event.
- `V0774`: The narrative terminates at ER Sepsis Triage and does not reach discharge.
- `V0775`: The narrative ends with CRP and does not reach a discharge event.
- `V0777`: The process terminates at Leucocytes without reaching any discharge activity, so no release category is realized.
- `V0778`: The process terminates at Leucocytes and does not conclude with a discharge activity.
- `V0791`: The process terminates at IV Antibiotics without reaching a discharge activity.
- `V0804`: The outcome is Return ER, so it does not realize any discharge category.
- `V0806`: The outcome is Return ER, so it does not realize any discharge category.
- `V0808`: The outcome is Return ER, so it does not realize any discharge category.
- `V0812`: The outcome is Return ER, so it does not realize any discharge category.
- `V0815`: The outcome is Return ER, so it does not realize any discharge category.
- `V0816`: The outcome is IV Antibiotics, which is not a discharge category.
- `V0820`: The outcome is LacticAcid, which is not a discharge category.
- `V0821`: The outcome is Return ER, so it does not realize any discharge category.
- `V0822`: The outcome is Return ER, so it does not realize any discharge category.
- `V0823`: The outcome is Return ER, so it does not realize any discharge category.
- `V0825`: The outcome is Return ER, so it does not realize any discharge category.
- `V0826`: The narrative ends with Admission NC and does not reach any discharge activity.
- `V0832`: The narrative terminates at IV Antibiotics and does not reach a discharge activity.
- `V0843`: The narrative terminates at IV Liquid and does not reach any discharge activity.
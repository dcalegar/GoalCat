# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_axisdischarge_pertC_distractor_6_112_rep1` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Release A (`release_a`)

Standard discharge pathway corresponding to Task Release A, measured by Avoid post-discharge deterioration and Post-discharge ER return indicators, contributing positively to avoiding post-discharge deterioration.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release A (id=17), supported by frequent and rare variants such as V0008, V0065, and V0070.

**Goal-model linkage:** 17 (Task): Release A

**Coverage:** macro 580/846 variants (68.6%) · micro 628/1050 cases (59.8%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.28, nearest other category `release_b` at mean distance 15.03

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.345, nearest other category `release_d` at mean distance 0.447

## Release B (`release_b`)

Discharge pathway corresponding to Task Release B, measured by Avoid post-discharge deterioration, contributing positively to avoiding post-discharge deterioration.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release B (id=18), supported by variants such as V0068 and V0145.

**Goal-model linkage:** 18 (Task): Release B

**Coverage:** macro 55/846 variants (6.5%) · micro 56/1050 cases (5.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 16.61, nearest other category `release_a` at mean distance 15.03

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.248, nearest other category `release_d` at mean distance 0.545

## Release C (`release_c`)

Discharge pathway corresponding to Task Release C, measured against post-discharge indicators.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release C (id=19), supported by long-running variant V0710.

**Goal-model linkage:** 19 (Task): Release C

**Coverage:** macro 24/846 variants (2.8%) · micro 24/1050 cases (2.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 23.33, nearest other category `release_a` at mean distance 18.45

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.255, nearest other category `release_d` at mean distance 0.437

## Release D (`release_d`)

Discharge pathway corresponding to Task Release D, measured against post-discharge indicators.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release D (id=20), supported by variant V0273.

**Goal-model linkage:** 20 (Task): Release D

**Coverage:** macro 23/846 variants (2.7%) · micro 23/1050 cases (2.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 19.17, nearest other category `release_a` at mean distance 16.92

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.296, nearest other category `release_c` at mean distance 0.437

## Release E (`release_e`)

Discharge pathway corresponding to Task Release E, measured against post-discharge indicators.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release E (id=21) based on the goal model decomposition, with no separate divergence found in the sample.

**Goal-model linkage:** 21 (Task): Release E

**Coverage:** macro 6/846 variants (0.7%) · micro 6/1050 cases (0.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 17.67, nearest other category `release_a` at mean distance 16.37

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.253, nearest other category `release_d` at mean distance 0.443

## Release F (`release_f`)

Discharge pathway corresponding to Task Release F, measured against post-discharge indicators.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release F (id=112) based on the goal model decomposition.

**Goal-model linkage:** 112 (Task): Release F

**Coverage:** macro 0/846 variants (0.0%) · micro 0/1050 cases (0.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a, nearest other category `None` at mean distance n/a

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a, nearest other category `None` at mean distance n/a

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

158/846 variants (18.7%), 313/1050 cases (29.8%) unassigned.

- `V0001`: The process terminates at ER Sepsis Triage and does not reach a discharge pathway.
- `V0002`: The process ends at CRP without completing any discharge pathway.
- `V0003`: The process ends at Leucocytes without reaching a discharge pathway.
- `V0004`: The process ends at IV Antibiotics and does not conclude with a release task.
- `V0005`: The process terminates at LacticAcid without any discharge pathway.
- `V0006`: The process ends at IV Antibiotics without reaching a release task.
- `V0007`: The process terminates at IV Antibiotics without a discharge pathway.
- `V0009`: The process ends at IV Antibiotics without concluding with a release task.
- `V0010`: The process ends at ER Sepsis Triage without reaching a discharge pathway.
- `V0011`: The process terminates at IV Antibiotics without a release task.
- `V0012`: The process ends at IV Antibiotics without reaching a discharge pathway.
- `V0013`: The process terminates at Leucocytes without reaching a discharge pathway.
- `V0017`: The process terminates at ER Sepsis Triage without reaching a discharge pathway.
- `V0019`: The process ends at IV Antibiotics without reaching a discharge pathway.
- `V0020`: The process terminates at CRP without reaching a discharge pathway.
- `V0024`: The process ends at Admission NC without reaching a release task.
- `V0025`: The process terminates at IV Antibiotics without reaching a discharge pathway.
- `V0027`: The narrative ends with IV Antibiotics and does not reach a discharge task.
- `V0029`: The narrative terminates at Leucocytes without reaching any release pathway.
- `V0031`: The narrative ends with LacticAcid and does not contain a discharge event.
- `V0034`: The narrative terminates at IV Liquid and has no discharge task.
- `V0036`: The narrative ends at CRP without a discharge pathway.
- `V0038`: The narrative terminates at IV Antibiotics and lacks a discharge activity.
- `V0040`: The narrative ends with Admission NC and does not reach any release task.
- `V0043`: The narrative ends at LacticAcid and contains no discharge process.
- `V0050`: The narrative terminates at CRP without reaching any release category.
- `V0056`: The narrative terminates at IV Antibiotics and does not reach a discharge pathway category.
- `V0062`: The narrative terminates at IV Antibiotics without reaching a discharge pathway.
- `V0081`: The narrative ends with IV Liquid and does not reach any discharge pathway category.
- `V0088`: The narrative terminates at IV Antibiotics and does not reach a discharge pathway category.
- `V0092`: The narrative ends with LacticAcid and does not reach a discharge pathway category.
- `V0111`: The outcome is Admission NC without any discharge task, so no release category applies.
- `V0127`: The narrative ends in LacticAcid without any discharge pathway.
- `V0132`: The narrative ends with IV Antibiotics and does not reach a discharge category.
- `V0133`: The outcome is IV Antibiotics without a discharge event.
- `V0137`: The narrative ends in LacticAcid without completing a discharge path.
- `V0146`: The narrative ends in Leucocytes without reaching any release task.
- `V0148`: The variant ends with IV Antibiotics and lacks a discharge activity.
- `V0151`: The narrative ends with Return ER after Release D, which does not match the specific discharge outcomes for Release A or Release B.
- `V0154`: The patient returns to the ER after discharge, invalidating the positive discharge criteria of Release A and Release B.
- `V0155`: The patient returns to the ER following a Release A event, failing the positive avoidance of post-discharge return.
- `V0157`: The process terminates with a return to the ER after Release A.
- `V0160`: The narrative includes a subsequent return to the ER.
- `V0161`: The case involves a return to the ER following Release A.
- `V0163`: The patient experienced a post-discharge ER return after Release A.
- `V0164`: The narrative records an ER return following discharge.
- `V0168`: The narrative includes a return to the ER after Release A.
- `V0171`: The patient returns to the ER after discharge.
- `V0172`: The case involves an ER return following Release A.
- `V0174`: The patient returns to the ER after the Release A event.
- `V0181`: The outcome is Leucocytes and does not reach a recognized release task endpoint.
- `V0187`: The variant ends prematurely at CRP without reaching any release pathway.
- `V0197`: The sequence ends at Leucocytes without reaching a release category.
- `V0217`: The narrative ends with IV Antibiotics rather than a discharge pathway task.
- `V0219`: The narrative ends with Leucocytes rather than a discharge pathway task.
- `V0232`: The narrative terminates at IV Antibiotics and does not reach any release pathway.
- `V0234`: The process ends at Leucocytes without reaching any discharge task.
- `V0260`: The narrative does not reach any discharge pathway and ends at IV Antibiotics.
- `V0268`: The narrative does not reach any discharge pathway and ends at Leucocytes.
- `V0287`: The narrative terminates at CRP and does not complete a discharge task, making it part of the residual.
- `V0292`: The process terminates prematurely at Leucocytes without reaching a discharge task.
- `V0295`: The process ends at IV Antibiotics and does not reach any designated release category.
- `V0302`: The narrative ends prematurely at ER Sepsis Triage and does not reach any discharge pathway.
- `V0305`: The trace terminates at IV Antibiotics and does not reach a discharge category.
- `V0322`: The trace stops at IV Antibiotics without reaching any defined release category.
- `V0325`: The process instance ends at IV Antibiotics and does not reach a discharge category.
- `V0330`: The narrative terminates at IV Liquid and does not reach a recognized release task.
- `V0336`: The variant ends prematurely at CRP without a discharge task.
- `V0342`: The variant halts at CRP without reaching any release pathway.
- `V0349`: The variant stops at ER Sepsis Triage and does not reach a discharge pathway.
- `V0365`: The narrative does not conclude with any release activity, thus does not fit any of the discharge categories.
- `V0368`: The process terminates at Admission NC without reaching any release task.
- `V0374`: The variant terminates at Leucocytes and does not reach a discharge category.
- `V0378`: The narrative ends with IV Antibiotics rather than a recognized release pathway.
- `V0379`: The narrative terminates at IV Antibiotics without reaching any discharge category.
- `V0382`: Although it includes Release A, the final outcome is Return ER, indicating a post-discharge return that falls outside positive avoidance criteria.
- `V0385`: The process concludes with Return ER after an interim Release A, failing to maintain positive post-discharge status.
- `V0386`: The final outcome is Return ER following Release A, meaning it does not fit the successful avoidance criteria.
- `V0398`: The process ends with Return ER after Release A, failing the post-discharge avoidance criteria.
- `V0415`: The narrative ends with Admission NC and does not complete a discharge pathway.
- `V0417`: The narrative terminates at ER Triage and does not realize any discharge pathway.
- `V0429`: The variant ends with IV Antibiotics and does not reach any discharge pathway.
- `V0462`: The narrative ends in an interim lab activity (CRP) rather than a complete discharge pathway, so it does not fit any release category.
- `V0488`: The process terminates at IV Liquid without reaching any release pathway category.
- `V0492`: The process terminates at IV Liquid and does not reach a discharge pathway category.
- `V0495`: The process ends at IV Antibiotics without reaching a discharge pathway.
- `V0501`: The narrative ends with IV Liquid and does not reach any standard discharge pathway like Release A or B.
- `V0502`: The narrative ends with Admission NC and does not complete a discharge pathway.
- `V0507`: The variant terminates at IV Antibiotics without reaching a discharge pathway.
- `V0510`: The process terminates at IV Antibiotics and does not complete a discharge.
- `V0516`: The process terminates prematurely at Leucocytes without reaching a discharge pathway.
- `V0517`: The process ends at ER Triage and does not complete a discharge pathway.
- `V0549`: The narrative terminates at IV Liquid and does not reach a recognized release pathway.
- `V0556`: The narrative concludes with Return ER, which does not map to any of the standard release categories.
- `V0558`: The outcome is Return ER following Release A, meaning it does not cleanly realize a pure release pathway category without return.
- `V0559`: The process ends with Return ER after an initial Release A.
- `V0560`: The process results in Return ER.
- `V0564`: The narrative ends in Return ER.
- `V0565`: The narrative ends with Admission NC, which is incomplete relative to the release categories.
- `V0567`: The narrative ends with Return ER.
- `V0573`: The narrative ends with Return ER.
- `V0575`: The process stops at Leucocytes and does not reach a discharge/release outcome.
- `V0580`: The process terminates at CRP without reaching any release pathway.
- `V0584`: The process terminates at IV Liquid without reaching a discharge pathway.
- `V0585`: The process terminates at LacticAcid without completing any discharge pathway.
- `V0587`: The process ends at CRP without a corresponding release pathway.
- `V0592`: The process ends at IV Antibiotics without reaching a discharge outcome.
- `V0605`: Although the narrative ends in Release A, it resulted in a post-discharge ER return, violating the positive contribution indicator of avoiding post-discharge deterioration for Release A.
- `V0614`: Although the narrative indicates Release A, it resulted in an ER return, failing the indicator to avoid post-discharge deterioration.
- `V0615`: Although the narrative indicates Release C, it resulted in an ER return, which falls outside the successful fulfillment of standard pathways without adverse return.
- `V0625`: Although the narrative indicates Release A, it resulted in an ER return, failing the indicator to avoid post-discharge deterioration.
- `V0636`: The narrative does not conclude with a standard discharge category from the taxonomy.
- `V0644`: The narrative terminates at CRP without reaching any designated release category.
- `V0645`: The narrative terminates at LacticAcid without realizing a release pathway.
- `V0646`: The variant ends with LacticAcid and does not clearly fit any release category.
- `V0654`: The narrative does not culminate in any discharge pathway category, ending instead at Leucocytes.
- `V0663`: The process terminates at Admission NC without reaching any release pathway.
- `V0664`: The process terminates at IV Liquid without reaching a release pathway.
- `V0670`: The narrative concludes with Leucocytes rather than any discharge category.
- `V0676`: The narrative ends with IV Antibiotics and does not reach a discharge pathway.
- `V0679`: The narrative terminates at IV Antibiotics without reaching a discharge pathway.
- `V0685`: The narrative ends with IV Antibiotics and does not reach any release category.
- `V0689`: The narrative terminates at IV Antibiotics without a discharge event.
- `V0694`: The narrative ends at ER Sepsis Triage and does not reach any discharge pathway.
- `V0703`: The narrative ends with IV Liquid and does not reach a discharge pathway category.
- `V0705`: The narrative results in a Return ER outcome after Release A, failing to maintain the avoidance of post-discharge deterioration.
- `V0707`: The narrative terminates at Admission NC without reaching a final discharge pathway.
- `V0708`: The narrative stops at IV Antibiotics without completing a discharge pathway.
- `V0712`: The narrative leads to a Return ER event after Release A, reflecting a post-discharge return.
- `V0713`: The narrative terminates at IV Antibiotics without concluding in a release category.
- `V0719`: The narrative leads to a Return ER following Release A.
- `V0720`: The narrative results in a Return ER after Release A.
- `V0721`: The narrative ends with a Return ER following Release A.
- `V0724`: The narrative terminates with a Return ER after Release A.
- `V0742`: The narrative ends with LacticAcid rather than a discharge pathway, so no category fits.
- `V0750`: The outcome is IV Antibiotics rather than a discharge pathway, so no category applies.
- `V0759`: The outcome is IV Antibiotics rather than a discharge pathway.
- `V0764`: The outcome is ER Sepsis Triage, so no release pathway is realized.
- `V0772`: The outcome is CRP, meaning no release pathway was completed.
- `V0774`: The outcome is ER Sepsis Triage without reaching any discharge category.
- `V0775`: The outcome is CRP, failing to realize a release pathway.
- `V0777`: The narrative does not reach any discharge pathway and ends at Leucocytes.
- `V0778`: The narrative terminates at Leucocytes without reaching a discharge activity.
- `V0791`: The process terminates at IV Antibiotics without reaching a discharge pathway.
- `V0804`: The narrative ends with Return ER after Release A, so it does not fit cleanly into a standard successful discharge pathway category.
- `V0806`: The narrative ends with Return ER following Release A.
- `V0808`: The narrative results in a Return ER outcome.
- `V0812`: The narrative ends with Return ER after Release A.
- `V0815`: The narrative terminates with Return ER.
- `V0816`: The variant ends with IV Antibiotics, which is an intermediate stage and not a discharge pathway category.
- `V0820`: The narrative terminates at LacticAcid, which is an intermediate diagnostic activity rather than a discharge pathway.
- `V0821`: The narrative ends with Return ER.
- `V0822`: The narrative ends with Return ER.
- `V0823`: The narrative ultimately results in a Return ER outcome.
- `V0825`: The narrative ends with Return ER.
- `V0826`: The variant ends with Admission NC and does not complete a release task or match any specific discharge pathway category.
- `V0832`: The variant ends at IV Antibiotics without reaching any discharge pathway category.
- `V0843`: The variant terminates at IV Liquid and does not execute any release task.
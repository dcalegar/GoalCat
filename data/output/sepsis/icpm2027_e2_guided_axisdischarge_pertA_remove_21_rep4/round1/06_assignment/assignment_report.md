# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_axisdischarge_pertA_remove_21_rep4` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Release A (`release_a`)

Patient discharge via Release A path, helping avoid post-discharge deterioration as measured by post-discharge ER return indicator.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative Release A (id=17) from the goal model, observed as a standard discharge outcome in variants such as V0008.

**Goal-model linkage:** 17 (Task): Release A

**Coverage:** macro 536/846 variants (63.4%) · micro 580/1050 cases (55.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.23, nearest other category `release_b` at mean distance 13.95

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.336, nearest other category `release_d` at mean distance 0.463

## Release B (`release_b`)

Patient discharge via Release B path, helping avoid post-discharge deterioration as measured by post-discharge ER return indicator.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative Release B (id=18) from the goal model, observed as a distinct discharge outcome in variants such as V0068 and V0145.

**Goal-model linkage:** 18 (Task): Release B

**Coverage:** macro 82/846 variants (9.7%) · micro 87/1050 cases (8.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 15.69, nearest other category `release_a` at mean distance 13.95

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.380, nearest other category `release_d` at mean distance 0.490

## Release C (`release_c`)

Patient discharge via Release C path, associated with captured discharge outcomes.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative Release C (id=19) from the goal model, observed as the final outcome in variant V0710.

**Goal-model linkage:** 19 (Task): Release C

**Coverage:** macro 22/846 variants (2.6%) · micro 22/1050 cases (2.1%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 24.46, nearest other category `release_a` at mean distance 19.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.221, nearest other category `release_d` at mean distance 0.446

## Release D (`release_d`)

Patient discharge via Release D path, associated with captured discharge outcomes.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative Release D (id=20) from the goal model, observed as the final outcome in variant V0273.

**Goal-model linkage:** 20 (Task): Release D

**Coverage:** macro 19/846 variants (2.2%) · micro 19/1050 cases (1.8%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 17.08, nearest other category `release_a` at mean distance 15.25

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.253, nearest other category `release_c` at mean distance 0.446

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0274` / `V0710` (category `release_c`): structural=177, profile=0.390
- `V0084` / `V0710` (category `release_c`): structural=174, profile=0.253
- `V0138` / `V0710` (category `release_c`): structural=173, profile=0.253
- `V0313` / `V0710` (category `release_c`): structural=173, profile=0.165
- `V0314` / `V0710` (category `release_c`): structural=173, profile=0.148
- `V0433` / `V0710` (category `release_c`): structural=173, profile=0.313
- `V0601` / `V0710` (category `release_c`): structural=173, profile=0.248
- `V0710` / `V0747` (category `release_c`): structural=173, profile=0.049
- `V0423` / `V0710` (category `release_c`): structural=172, profile=0.126
- `V0426` / `V0710` (category `release_c`): structural=172, profile=0.161

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0016` (`release_a`) / `V0052` (`release_b`): structural=1, profile=0.429
- `V0022` (`release_a`) / `V0274` (`release_c`): structural=1, profile=0.374
- `V0026` (`release_a`) / `V0052` (`release_b`): structural=1, profile=0.219
- `V0033` (`release_a`) / `V0054` (`release_b`): structural=1, profile=0.210
- `V0037` (`release_b`) / `V0706` (`release_a`): structural=1, profile=0.359
- `V0041` (`release_a`) / `V0055` (`release_b`): structural=1, profile=0.417
- `V0044` (`release_a`) / `V0754` (`release_b`): structural=1, profile=0.378
- `V0054` (`release_b`) / `V0231` (`release_a`): structural=1, profile=0.150
- `V0054` (`release_b`) / `V0265` (`release_a`): structural=1, profile=0.172
- `V0054` (`release_b`) / `V0509` (`release_a`): structural=1, profile=0.394

## Residual

187/846 variants (22.1%), 342/1050 cases (32.6%) unassigned.

- `V0001`: The narrative ends at ER Sepsis Triage and does not reach any discharge path.
- `V0002`: The narrative ends at CRP and does not reach any discharge path.
- `V0003`: The narrative ends at Leucocytes and does not reach any discharge path.
- `V0004`: The narrative ends at IV Antibiotics and does not reach any discharge path.
- `V0005`: The narrative ends at LacticAcid and does not reach any discharge path.
- `V0006`: The narrative ends at IV Antibiotics and does not reach any discharge path.
- `V0007`: The narrative ends at IV Antibiotics and does not reach any discharge path.
- `V0009`: The narrative ends at IV Antibiotics and does not reach any discharge path.
- `V0010`: The narrative ends at ER Sepsis Triage and does not reach any discharge path.
- `V0011`: The narrative ends at IV Antibiotics and does not reach any discharge path.
- `V0012`: The narrative ends at IV Antibiotics and does not reach any discharge path.
- `V0013`: The narrative ends at Leucocytes and does not reach any discharge path.
- `V0017`: The narrative ends at ER Sepsis Triage and does not reach any discharge path.
- `V0019`: The narrative ends at IV Antibiotics and does not reach any discharge path.
- `V0020`: The narrative ends at CRP and does not reach any discharge path.
- `V0024`: The narrative ends at Admission NC and does not reach any release category.
- `V0025`: The narrative ends at IV Antibiotics and does not reach any discharge path.
- `V0027`: The narrative ends with IV Antibiotics and does not reach any discharge path.
- `V0029`: The narrative ends with Leucocytes and does not reach any discharge path.
- `V0031`: The narrative ends with LacticAcid and does not reach any discharge path.
- `V0034`: The narrative ends with IV Liquid and does not reach any discharge path.
- `V0036`: The narrative ends with CRP and does not reach any discharge path.
- `V0038`: The narrative ends with IV Antibiotics and does not reach any discharge path.
- `V0040`: The narrative ends with Admission NC and does not reach any discharge path.
- `V0043`: The narrative ends with LacticAcid and does not reach any discharge path.
- `V0050`: The narrative ends with CRP and does not reach any discharge path.
- `V0056`: The process ends with IV Antibiotics rather than a patient discharge outcome, so none of the release categories fit.
- `V0062`: The process ends with IV Antibiotics rather than a patient discharge outcome, so no release category fits.
- `V0081`: The narrative outcome is IV Liquid, meaning the patient was not discharged under any release category.
- `V0088`: The narrative outcome is IV Antibiotics, meaning the patient was not discharged.
- `V0092`: The narrative outcome is LacticAcid, meaning the patient was not discharged.
- `V0111`: The variant ends with Admission NC and does not realize any of the discharge categories.
- `V0127`: The narrative ends with LacticAcid instead of a discharge path.
- `V0132`: The narrative ends with IV Antibiotics rather than a discharge pathway.
- `V0133`: The narrative terminates at IV Antibiotics, not a discharge category.
- `V0137`: The narrative ends with LacticAcid instead of a discharge category.
- `V0146`: The narrative ends with Leucocytes rather than a discharge path.
- `V0148`: The narrative terminates at IV Antibiotics.
- `V0151`: The narrative ends with Return ER following Release D, which does not cleanly map to the discharge paths defined in Release A, B, or C, and lacks specific outcome capture criteria for Release D without prior alignment.
- `V0154`: The narrative shows a final outcome of Return ER after a Release A event, meaning it does not fulfill the successful avoidance of post-discharge deterioration as measured by post-discharge ER return.
- `V0155`: The narrative results in a Return ER event following discharge, failing to avoid post-discharge deterioration.
- `V0157`: The narrative concludes with a Return ER event, indicating post-discharge deterioration.
- `V0160`: The narrative ends with a Return ER event after Release A, indicating it did not avoid post-discharge deterioration.
- `V0161`: The narrative ends with a Return ER event, negating the avoidance of post-discharge deterioration.
- `V0163`: The narrative ends in a Return ER event, indicating post-discharge deterioration occurred despite Release A.
- `V0164`: The narrative includes a Return ER outcome following release, failing the criteria for post-discharge deterioration avoidance.
- `V0168`: The narrative concludes with a Return ER event, showing post-discharge deterioration.
- `V0171`: The narrative leads to a Return ER event after Release A, failing to avoid post-discharge deterioration.
- `V0172`: The narrative results in a Return ER event following release, indicating post-discharge deterioration.
- `V0174`: The narrative ends with a Return ER event, indicating post-discharge deterioration.
- `V0181`: The outcome is Leucocytes rather than a valid discharge path.
- `V0187`: The outcome is CRP and lacks a valid discharge classification.
- `V0196`: The narrative ends with Release E, which does not match any of the defined categories A, B, C, or D.
- `V0197`: The outcome is Leucocytes, lacking any valid discharge path.
- `V0217`: The narrative terminates at IV Antibiotics without any discharge activity, so none of the release categories fit.
- `V0219`: The narrative terminates at Leucocytes without any discharge activity, so none of the release categories fit.
- `V0232`: The narrative ends with IV Antibiotics and does not reach any discharge category.
- `V0234`: The narrative ends with Leucocytes and does not reach any discharge category.
- `V0260`: The narrative terminates at IV Antibiotics without any discharge activity.
- `V0268`: The narrative terminates at Leucocytes without any discharge event.
- `V0287`: The narrative ends at CRP without reaching any patient discharge path.
- `V0292`: The narrative terminates at Leucocytes and does not reach a discharge destination.
- `V0295`: The narrative ends with IV Antibiotics and does not realize any discharge path.
- `V0302`: The narrative ends with ER Sepsis Triage and does not represent a discharge path.
- `V0305`: The narrative terminates at IV Antibiotics and does not reach a discharge outcome.
- `V0309`: The narrative ends with Admission NC and includes an intermediate Release B step rather than a terminal discharge type matching the listed categories.
- `V0316`: The narrative ends with Release E, which is not part of the defined taxonomy categories (release_a, release_b, release_c, release_d).
- `V0322`: The narrative terminates at IV Antibiotics and does not reach a discharge destination.
- `V0325`: The narrative terminates at IV Antibiotics and does not reach any discharge category.
- `V0327`: The narrative ends with Return ER, which indicates post-discharge deterioration, meaning it does not successfully realize the goal of avoiding ER return for Release A or Release B.
- `V0328`: The narrative ends with Return ER, representing post-discharge deterioration and failing the criteria for Release A or Release B.
- `V0330`: The narrative terminates at IV Liquid rather than a patient discharge pathway, so it does not realize any of the release categories.
- `V0334`: The narrative ends with Return ER, indicating post-discharge deterioration which violates the avoidance condition for release paths.
- `V0335`: Although it features Release A, the narrative ultimately results in a Return ER, indicating post-discharge deterioration.
- `V0336`: The outcome is CRP, meaning the patient was not discharged via any of the release pathways.
- `V0339`: The narrative concludes with Return ER, indicating a failure to avoid post-discharge deterioration.
- `V0342`: The outcome activity is CRP, so no discharge pathway is realized.
- `V0346`: The narrative terminates with Return ER, reflecting post-discharge deterioration.
- `V0347`: The narrative ends with Return ER, demonstrating post-discharge deterioration.
- `V0348`: Despite passing through Release A, the case eventually leads to Return ER, indicating post-discharge deterioration.
- `V0349`: The outcome is ER Sepsis Triage, meaning the patient was not discharged via a release category.
- `V0350`: The narrative ultimately ends with Return ER after Release A, failing the avoidance of post-discharge deterioration.
- `V0365`: The narrative outcome is Leucocytes rather than any recognized release path, so it does not fit any of the categories.
- `V0368`: The narrative outcome is Admission NC rather than any recognized release path, so it does not fit any category.
- `V0374`: The narrative outcome is Leucocytes rather than any recognized release path, so it does not fit any of the categories.
- `V0378`: The narrative ends with IV Antibiotics rather than any of the specified release outcomes.
- `V0379`: The narrative ends with IV Antibiotics rather than any of the specified release outcomes.
- `V0382`: Although it passes through Release A, the final outcome is Return ER, indicating post-discharge deterioration rather than successful avoidance.
- `V0385`: The final outcome is Return ER, indicating post-discharge deterioration.
- `V0386`: The final outcome is Return ER, reflecting post-discharge deterioration.
- `V0398`: The final outcome is Return ER, indicating post-discharge deterioration.
- `V0415`: The outcome is Admission NC rather than any of the specified release paths.
- `V0417`: The process ends at ER Triage without reaching any release category.
- `V0427`: The outcome is Return ER, which does not realize any of the specified discharge paths.
- `V0429`: The narrative ends with IV Antibiotics and does not reach a discharge outcome category.
- `V0435`: Although it passes through Release A, the final outcome is Return ER, making it a non-realizing path for successful discharge categories.
- `V0437`: The final outcome is Return ER, which does not realize any of the successful discharge paths.
- `V0440`: The final outcome is Return ER, thus it does not realize a successful release path.
- `V0441`: The final outcome is Return ER.
- `V0442`: The final outcome is Return ER.
- `V0443`: The final outcome is Return ER.
- `V0447`: The final outcome is Return ER.
- `V0448`: The final outcome is Return ER.
- `V0449`: The final outcome is Return ER.
- `V0462`: The narrative ends with CRP rather than a release path.
- `V0488`: The narrative does not conclude with a discharge event, so it does not fit any of the release categories.
- `V0492`: The narrative does not conclude with a discharge event, so it does not fit any of the release categories.
- `V0495`: The narrative does not conclude with a discharge event, so it does not fit any of the release categories.
- `V0501`: The narrative ends with IV Liquid and does not reach any discharge path.
- `V0502`: The narrative ends with Admission NC and does not reach any discharge path.
- `V0507`: The narrative ends with IV Antibiotics and does not reach a discharge category.
- `V0510`: The narrative ends with IV Antibiotics and does not reach a discharge category.
- `V0516`: The narrative terminates at Leucocytes and does not reach any discharge path.
- `V0517`: The narrative terminates at ER Triage and does not reach any discharge path.
- `V0549`: The narrative does not end with a release category, terminating at IV Liquid.
- `V0553`: The variant ends with Release E, which does not correspond to any of the defined release categories (A, B, C, or D).
- `V0556`: Although it contains Release A earlier, the final outcome is Return ER, which does not fit standard discharge definitions.
- `V0558`: The variant results in a Return ER outcome after Release A, so it does not fit the persistent avoidance goal.
- `V0559`: The variant results in a Return ER outcome after Release A.
- `V0560`: The variant results in a Return ER outcome after Release A.
- `V0564`: The variant results in a Return ER outcome after Release A.
- `V0565`: The variant ends with Admission NC and has no release outcome.
- `V0567`: The variant results in a Return ER outcome after Release A.
- `V0573`: The variant results in a Return ER outcome after Release A.
- `V0575`: The variant ends with Leucocytes and has no release outcome.
- `V0580`: The narrative ends with CRP and does not reach any release pathway.
- `V0584`: The narrative ends with IV Liquid and does not reach any release pathway.
- `V0585`: The narrative ends with LacticAcid and does not reach any release pathway.
- `V0587`: The narrative ends with CRP and does not reach any release pathway.
- `V0592`: The narrative ends with IV Antibiotics and does not reach any release pathway.
- `V0598`: The narrative ends with Release E, which is not part of the taxonomy.
- `V0603`: The narrative results in Release E, which does not match any of the defined taxonomy categories (Release A, B, C, or D).
- `V0605`: Although it ends with Release A initially, it leads to a Return ER event, reflecting post-discharge deterioration rather than successful avoidance.
- `V0614`: Although it ends with Release A, it results in a Return ER event, indicating post-discharge deterioration.
- `V0615`: Although it ends with Release C initially, it results in a Return ER event.
- `V0625`: Although it ends with Release A initially, it results in a Return ER event, indicating post-discharge deterioration.
- `V0629`: The outcome is Release E, which does not match any of the defined categories (release_a, release_b, release_c, release_d).
- `V0636`: The outcome is LacticAcid, which does not match any discharge path categories.
- `V0644`: The outcome activity is CRP, which does not correspond to any valid discharge category.
- `V0645`: The outcome activity is LacticAcid, lacking a matching discharge category.
- `V0654`: The variant ends with Leucocytes rather than any discharge category, so it does not realize any of the release paths.
- `V0663`: The variant ends with Admission NC and does not reach any release or discharge outcome.
- `V0664`: The variant stops at IV Liquid and does not reach a discharge category.
- `V0670`: The variant ends with Leucocytes after an ER return, meaning it does not cleanly realize any of the release paths.
- `V0676`: The narrative ends in IV Antibiotics without any discharge activity or post-discharge outcomes.
- `V0679`: The narrative terminates at IV Antibiotics without reaching a discharge path.
- `V0685`: The process terminates at IV Antibiotics and does not involve any release path.
- `V0689`: The process ends at IV Antibiotics without a discharge step.
- `V0694`: The process ends early at ER Sepsis Triage.
- `V0703`: The narrative ends with IV Liquid rather than a recognized discharge category.
- `V0705`: Although it ends with Release A initially, there is a subsequent Return ER event, so it does not successfully avoid post-discharge deterioration.
- `V0707`: The narrative terminates at Admission NC and does not reach any release destination.
- `V0708`: The narrative terminates at IV Antibiotics and does not reach any release destination.
- `V0712`: Although it concludes with Release A, it is followed by Return ER, failing the avoidance of post-discharge deterioration.
- `V0713`: The narrative terminates at IV Antibiotics without any discharge outcome.
- `V0718`: The narrative ends with Release D followed by Return ER, meaning it does not avoid post-discharge deterioration.
- `V0719`: Ends with Release A followed by Return ER, thus failing the no-deterioration condition.
- `V0720`: Ends with Release A followed by Return ER, failing the criteria for release_a.
- `V0721`: Ends with Release A followed by Return ER, failing the criteria for release_a.
- `V0724`: Ends with Release A followed by Return ER, failing the criteria for release_a.
- `V0727`: Although it features Release A, the patient experienced a Return ER outcome, disqualifying it from being considered a successful realization of the avoidance goal.
- `V0734`: The narrative terminates with Return ER, meaning it does not fulfill the successful avoidance criteria of Release A.
- `V0742`: The outcome is LacticAcid, which does not match any of the defined discharge categories.
- `V0744`: Although Release A is mentioned, the final outcome is Return ER, failing the avoidance goal.
- `V0745`: The final outcome is Return ER, disqualifying it from the target avoidance category.
- `V0746`: The final outcome is Return ER, failing the avoidance criteria.
- `V0748`: The final outcome is Return ER, disqualifying it from the successful avoidance criteria.
- `V0750`: The outcome is IV Antibiotics, which does not map to any release categories.
- `V0759`: The narrative ends at IV Antibiotics and does not reach any discharge path or capture outcomes.
- `V0764`: The sequence terminates prematurely at ER Sepsis Triage and does not involve any patient discharge or outcomes.
- `V0772`: The narrative stops at CRP and does not reach a discharge destination.
- `V0774`: The process terminates at ER Sepsis Triage without reaching any discharge outcome.
- `V0775`: The sequence ends at CRP and does not include any discharge pathways or outcomes.
- `V0777`: The narrative does not culminate in any discharge outcome category.
- `V0778`: The narrative ends with Leucocytes rather than a recognized release outcome.
- `V0779`: The process ends in Return ER rather than any discharge category.
- `V0785`: Although it passes through Release A, the final outcome is Return ER.
- `V0787`: The process ends with Return ER.
- `V0791`: The variant ends with IV Antibiotics and does not reach a discharge category.
- `V0794`: The process ultimately ends with Return ER.
- `V0797`: The process ends in Return ER.
- `V0798`: The process ends in Return ER.
- `V0816`: The narrative terminates at IV Antibiotics and does not reach any discharge category.
- `V0820`: The narrative terminates at LacticAcid and does not reach any discharge category.
- `V0826`: The narrative ends in Admission NC without any release activity or captured discharge outcomes.
- `V0832`: The process terminates at IV Antibiotics without reaching a discharge or release state.
- `V0843`: The process terminates at IV Liquid without reaching a discharge or release state.
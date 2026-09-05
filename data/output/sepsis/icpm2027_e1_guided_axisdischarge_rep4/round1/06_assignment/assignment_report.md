# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_axisdischarge_rep4` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Release A (`release_a`)

Represents the discharge of an admitted patient under pathway A, contributing positively to avoiding post-discharge deterioration and measured against post-discharge ER returns.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release A (id=17) as observed in the sample variants such as V0008, supporting avoidance of post-discharge deterioration.

**Goal-model linkage:** 17 (Task): Release A

**Coverage:** macro 563/846 variants (66.5%) · micro 607/1050 cases (57.8%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.31, nearest other category `release_b` at mean distance 15.03

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.342, nearest other category `release_d` at mean distance 0.449

## Release B (`release_b`)

Represents the discharge of an admitted patient under pathway B, helping to avoid post-discharge deterioration and evaluated against post-discharge ER return indicators.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release B (id=18) as seen in sample variants like V0068 and V0145, helping avoid post-discharge deterioration.

**Goal-model linkage:** 18 (Task): Release B

**Coverage:** macro 55/846 variants (6.5%) · micro 56/1050 cases (5.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 16.61, nearest other category `release_a` at mean distance 15.03

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.248, nearest other category `release_c` at mean distance 0.543

## Release C (`release_c`)

Represents the discharge of an admitted patient under pathway C, contributing to the overall patient disposition goal and measured against post-discharge ER returns.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release C (id=19) as evidenced by sample variant V0710.

**Goal-model linkage:** 19 (Task): Release C

**Coverage:** macro 21/846 variants (2.5%) · micro 21/1050 cases (2.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 25.08, nearest other category `release_a` at mean distance 19.28

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.201, nearest other category `release_d` at mean distance 0.452

## Release D (`release_d`)

Represents the discharge of an admitted patient under pathway D, reaching a captured discharge and monitored via post-discharge ER return indicators.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release D (id=20) as observed in sample variant V0273.

**Goal-model linkage:** 20 (Task): Release D

**Coverage:** macro 23/846 variants (2.7%) · micro 23/1050 cases (2.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 19.17, nearest other category `release_a` at mean distance 16.92

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.296, nearest other category `release_e` at mean distance 0.443

## Release E (`release_e`)

Represents the discharge of an admitted patient under pathway E, concluding the patient journey towards a documented disposition.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release E (id=21) based on the goal model decomposition for captured discharges.

**Goal-model linkage:** 21 (Task): Release E

**Coverage:** macro 6/846 variants (0.7%) · micro 6/1050 cases (0.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 17.67, nearest other category `release_a` at mean distance 16.36

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.253, nearest other category `release_d` at mean distance 0.443

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

178/846 variants (21.0%), 337/1050 cases (32.1%) unassigned.

- `V0001`: This narrative ends in ER Sepsis Triage and does not reach any release pathway.
- `V0002`: This variant terminates at CRP testing without reaching a discharge or release pathway.
- `V0003`: The process ends at Leucocytes testing and does not represent a patient discharge.
- `V0004`: This variant concludes with IV Antibiotics and does not involve any patient release.
- `V0005`: The process ends at LacticAcid and does not result in a discharge.
- `V0006`: This narrative finishes with IV Antibiotics rather than patient release.
- `V0007`: This variant terminates with IV Antibiotics and lacks a discharge event.
- `V0009`: The sequence ends at IV Antibiotics without proceeding to a release state.
- `V0010`: This variant terminates at ER Sepsis Triage and does not reach a discharge goal.
- `V0011`: The process ends with IV Antibiotics, omitting any release activity.
- `V0012`: This narrative finishes at IV Antibiotics and does not reach patient discharge.
- `V0013`: The variant ends at Leucocytes testing without achieving discharge.
- `V0017`: The sequence ends at ER Sepsis Triage and does not represent a discharge.
- `V0019`: This narrative stops at IV Antibiotics and does not reach a release outcome.
- `V0020`: The process ends with CRP testing and lacks a discharge activity.
- `V0021`: Although it includes Release A, the final outcome is Return ER, which does not cleanly fit the standard discharge pathway definitions in this context.
- `V0023`: The final outcome is Return ER following Release A, making it part of the residual rather than a standard clean release category.
- `V0024`: This variant ends at Admission NC rather than a final discharge/release category.
- `V0025`: The sequence ends with IV Antibiotics and does not involve a patient release.
- `V0027`: The variant ends with IV Antibiotics and does not conclude with a patient discharge or disposition matching any release pathway.
- `V0029`: The variant terminates at Leucocytes without reaching a patient release or disposition category.
- `V0031`: The variant ends at LacticAcid and does not represent a discharge event.
- `V0034`: The variant ends with IV Liquid and lacks any patient discharge activity.
- `V0036`: The variant ends with CRP and does not reach a discharge milestone.
- `V0038`: The variant terminates at IV Antibiotics without involving a patient release.
- `V0040`: The variant terminates with Admission NC and does not reach a discharge status.
- `V0043`: The variant ends at LacticAcid and does not include any release activity.
- `V0050`: The variant ends with CRP and does not contain a discharge event.
- `V0056`: The outcome is IV Antibiotics, which does not represent a patient discharge or any defined release pathway.
- `V0062`: The outcome is IV Antibiotics, representing treatment rather than a final discharge pathway.
- `V0078`: The outcome is Return ER following Release A, which does not exclusively represent a clean discharge path category realization.
- `V0080`: The narrative ends with Return ER after Release A, so it does not fit standard successful discharge categories.
- `V0081`: The process ends with IV Liquid and does not reach a discharge disposition.
- `V0083`: The narrative results in a Return ER event following Release A.
- `V0085`: The narrative ends with Return ER after Release A.
- `V0088`: The process terminates at IV Antibiotics without reaching a discharge destination.
- `V0089`: The narrative ends with Return ER after Release A.
- `V0092`: The process terminates at LacticAcid without completing a discharge.
- `V0094`: The narrative results in a Return ER after Release A.
- `V0098`: The narrative concludes with Return ER after Release A.
- `V0111`: The narrative ends with Admission NC rather than a recognized release category.
- `V0127`: The narrative outcome is LacticAcid, which does not represent a patient discharge or release event.
- `V0132`: The process concludes with IV Antibiotics, which is not a discharge or disposition category.
- `V0133`: The outcome is IV Antibiotics, representing treatment rather than patient discharge.
- `V0137`: The sequence ends with LacticAcid, lacking any discharge event.
- `V0146`: The sequence terminates at Leucocytes, which does not correspond to any discharge category.
- `V0148`: The outcome is IV Antibiotics, which represents treatment rather than a release event.
- `V0151`: The narrative ends with Return ER, which does not match any of the release categories (release_a, release_b, release_c, release_d, release_e) as a terminal outcome.
- `V0154`: The narrative ends with Return ER, meaning it does not conclude under any specified release category.
- `V0155`: The narrative ends with Return ER, failing to achieve a final release category.
- `V0157`: The narrative ends with Return ER, which disqualifies it from matching any release category.
- `V0160`: The narrative ends with Return ER, so it does not fit any of the release categories.
- `V0161`: The narrative ends with Return ER, which is not represented among the release categories.
- `V0163`: The narrative ends with Return ER, meaning it does not conclude in a release category.
- `V0164`: The narrative ends with Return ER, failing to meet the criteria for any release category.
- `V0168`: The narrative ends with Return ER, so it does not fit any release category.
- `V0171`: The narrative ends with Return ER, disqualifying it from any release category.
- `V0172`: The narrative ends with Return ER, which is not a release category.
- `V0174`: The narrative ends with Return ER, failing to conclude under a release category.
- `V0181`: The narrative ends with Leucocytes and does not reach a discharge category.
- `V0187`: The narrative ends with CRP and does not reach a discharge event.
- `V0197`: The narrative ends with Leucocytes and does not reach any discharge category.
- `V0217`: The narrative outcome is IV Antibiotics, which does not represent any of the defined release pathways.
- `V0219`: The narrative ends with Leucocytes and does not reach a discharge or release state.
- `V0232`: The narrative ends at IV Antibiotics without reaching any discharge disposition, so no category fits.
- `V0234`: The narrative ends at Leucocytes without reaching any discharge disposition, so no category fits.
- `V0260`: The variant concludes with IV Antibiotics and does not reach a patient release or disposition event matching any of the pathways.
- `V0268`: The variant concludes with Leucocytes and does not reach any discharge or disposition event.
- `V0287`: The narrative terminates at CRP and does not reach a discharge disposition.
- `V0292`: The narrative terminates at Leucocytes and does not reach a discharge disposition.
- `V0295`: The narrative terminates at IV Antibiotics and does not reach a discharge disposition.
- `V0302`: The patient journey terminates at ER Sepsis Triage without reaching a discharge or disposition pathway.
- `V0305`: Terminates at IV Antibiotics inside the ER phase, without reaching a discharge disposition.
- `V0322`: Stops at IV Antibiotics without reaching a discharge category.
- `V0325`: Ends abruptly at IV Antibiotics without completing a discharge pathway.
- `V0330`: The outcome is IV Liquid rather than a patient discharge disposition.
- `V0336`: The outcome is CRP and does not represent a discharge disposition.
- `V0342`: The final activity is CRP, lacking a discharge disposition.
- `V0349`: The final activity is ER Sepsis Triage, not a discharge event.
- `V0365`: The narrative outcome is Leucocytes, not a discharge category from the taxonomy.
- `V0368`: The narrative outcome is Admission NC, lacking a discharge realization.
- `V0374`: The narrative outcome is Leucocytes, not a discharge category.
- `V0378`: The narrative ends with IV Antibiotics and does not reach a discharge or disposition event.
- `V0379`: The narrative ends with IV Antibiotics and does not reach a discharge or disposition event.
- `V0415`: The narrative concludes with Admission NC and does not reach any release category.
- `V0417`: The narrative concludes with ER Triage and does not reach a release category.
- `V0427`: The narrative outcome is Return ER rather than a recognized release category.
- `V0429`: The narrative ends with IV Antibiotics and does not reach a discharge disposition.
- `V0435`: The narrative outcome is Return ER following Release A, representing a post-discharge ER return.
- `V0440`: The narrative outcome is Return ER after Release A.
- `V0441`: The narrative outcome is Return ER after Release A.
- `V0442`: The narrative outcome is Return ER after Release A.
- `V0443`: The narrative outcome is Return ER after Release A.
- `V0447`: The narrative outcome is Return ER after Release C.
- `V0448`: The narrative outcome is Return ER after Release A.
- `V0449`: The narrative outcome is Return ER after Release A.
- `V0462`: The narrative does not conclude with a recognized release pathway activity.
- `V0488`: The narrative ends with IV Liquid and does not reach a discharge disposition category.
- `V0492`: The narrative ends with IV Liquid and does not reach a discharge disposition category.
- `V0495`: The narrative ends with IV Antibiotics and does not reach a discharge disposition category.
- `V0501`: The variant ends with IV Liquid and does not conclude with any of the discharge pathways corresponding to categories A through E.
- `V0502`: The variant terminates at Admission NC without reaching a discharge or disposition category.
- `V0507`: The variant ends with IV Antibiotics and does not reach a patient discharge event.
- `V0510`: The variant finishes at IV Antibiotics without reaching any discharge or disposition outcome.
- `V0516`: The variant terminates at Leucocytes without reaching a discharge or disposition category.
- `V0517`: The variant ends at ER Triage and does not represent a patient discharge.
- `V0549`: The narrative ends with IV Liquid rather than any discharge category, so it does not fit the taxonomy.
- `V0556`: The outcome is Return ER, which falls into the residual category as it does not match any of the release pathways.
- `V0558`: The outcome is Return ER, which falls into the residual category.
- `V0559`: The outcome is Return ER, which falls into the residual category.
- `V0560`: The outcome is Return ER, which falls into the residual category.
- `V0564`: The outcome is Return ER, which falls into the residual category.
- `V0565`: The outcome is Admission NC, which is not one of the release pathways.
- `V0567`: The outcome is Return ER, which falls into the residual category.
- `V0573`: The outcome is Return ER, which falls into the residual category.
- `V0575`: The outcome is Leucocytes, which is not one of the release pathways.
- `V0580`: The variant ends in CRP without reaching a formal patient discharge disposition.
- `V0584`: The narrative terminates at IV Liquid and does not reach a discharge disposition.
- `V0585`: The narrative terminates at LacticAcid without achieving patient release.
- `V0587`: The narrative ends with CRP and does not complete a patient release.
- `V0592`: The process variant ends at IV Antibiotics without concluding the patient journey.
- `V0605`: Although it ends with Release A, the subsequent Return ER indicates post-discharge deterioration that falls outside standard successful pathway completion.
- `V0614`: Although it ends with Release A initially, the subsequent Return ER indicates post-discharge deterioration.
- `V0615`: Although it ends with Release C initially, the subsequent Return ER indicates post-discharge deterioration.
- `V0625`: Although it ends with Release A initially, the subsequent Return ER indicates post-discharge deterioration.
- `V0636`: The process terminates at LacticAcid without any discharge or release activity, so no release category applies.
- `V0644`: The process concludes at CRP without reaching a discharge or release event.
- `V0645`: The process ends at LacticAcid and does not realize any release category.
- `V0654`: The variant ends with Leucocytes and does not culminate in any recognized discharge disposition.
- `V0663`: The process terminates at Admission NC without achieving a final discharge category.
- `V0664`: The variant terminates at IV Liquid and lacks any discharge outcome.
- `V0670`: Although Release A appears midway, the variant ultimately finishes with Leucocytes following an ER return.
- `V0676`: The narrative ends with IV Antibiotics and does not reach a discharge or disposition event corresponding to any release category.
- `V0679`: The process terminates at IV Antibiotics without any discharge outcome.
- `V0685`: The trace stops at IV Antibiotics and contains no release or discharge activity.
- `V0689`: The process ends at IV Antibiotics with no recorded patient disposition.
- `V0694`: The activity sequence stops at ER Sepsis Triage and does not contain a discharge event.
- `V0703`: The variant ends in IV Liquid and does not reach any discharge category.
- `V0705`: The narrative concludes with Return ER after Release A, so it does not fit standard successful release categories due to the ER return.
- `V0707`: The variant terminates at Admission NC and does not reach a discharge disposition.
- `V0708`: The variant terminates at IV Antibiotics and does not reach a discharge disposition.
- `V0712`: The narrative concludes with Return ER following a discharge, leaving the primary pathway.
- `V0713`: The variant terminates at IV Antibiotics and does not reach a discharge disposition.
- `V0719`: The narrative ends with a Return ER event after Release A.
- `V0720`: The narrative ends with a Return ER event after Release A.
- `V0721`: The narrative ends with a Return ER event after Release A.
- `V0724`: The narrative ends with a Return ER event following Release A.
- `V0742`: The outcome is LacticAcid, which does not correspond to any of the release pathways.
- `V0750`: The outcome is IV Antibiotics, which does not correspond to any discharge release category.
- `V0759`: The process terminates at IV Antibiotics and does not reach any discharge category.
- `V0764`: The variant stops at ER Sepsis Triage and does not reach a discharge disposition.
- `V0772`: The narrative ends with CRP and does not complete a discharge pathway.
- `V0774`: The variant ends prematurely at ER Sepsis Triage without reaching a discharge disposition.
- `V0775`: The narrative terminates at CRP and does not realize any discharge category.
- `V0777`: The process terminates at Leucocytes without reaching any discharge activity.
- `V0778`: The process terminates at Leucocytes without reaching a valid patient discharge outcome.
- `V0779`: The outcome is Return ER following an initial Release A, which does not map cleanly into a standalone category definition.
- `V0785`: The variant ends in Return ER after Release A, outside the scope of simple discharge categories.
- `V0787`: The final outcome is Return ER after Release A, so it does not fit a single positive discharge category.
- `V0791`: The process stops at IV Antibiotics without completing a discharge.
- `V0794`: The process terminates with Return ER after Release A.
- `V0797`: The final state is Return ER following Release A.
- `V0798`: The final state is Return ER following Release A.
- `V0804`: The narrative outcome is Return ER following Release A, meaning it does not solely fit the successful discharge goal category without post-discharge return context.
- `V0806`: The narrative ends with Return ER, meaning it does not fit the standard discharge categorization.
- `V0808`: The narrative ends with Return ER after Release A, so it does not represent a clean category realization.
- `V0812`: The narrative ends with Return ER following Release A, meaning it does not fit the clean release categories.
- `V0815`: The narrative ends with Return ER following Release A.
- `V0816`: The outcome is IV Antibiotics, which does not represent a patient discharge.
- `V0817`: Although it contains Release C, the final outcome is Return ER, making it fall into the residual.
- `V0820`: The outcome is LacticAcid, which does not represent a final patient discharge.
- `V0821`: The final outcome is Return ER following Release A.
- `V0822`: The final outcome is Return ER following Release A.
- `V0823`: The final outcome is Return ER following Release A.
- `V0825`: The final outcome is Return ER following Release A.
- `V0826`: The narrative ends with Admission NC and does not conclude with a discharge activity representing any of the defined pathways.
- `V0832`: The narrative ends with IV Antibiotics and does not reach a patient discharge or disposition outcome.
- `V0843`: The narrative ends with IV Liquid and does not conclude with a discharge activity.
# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_axisdischarge_pertC_distractor_6_112_rep5` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Release A (`release_a`)

Standard release pathway supporting discharge for admitted cases, contributing to avoiding post-discharge deterioration and measured against post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release A (id=17), supported by variants such as V0008, V0070, and V0071.

**Goal-model linkage:** 17 (Task): Release A

**Coverage:** macro 591/846 variants (69.9%) · micro 639/1050 cases (60.9%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.42, nearest other category `release_b` at mean distance 15.09

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.347, nearest other category `release_d` at mean distance 0.445

## Release B (`release_b`)

Alternative discharge pathway for admitted cases, contributing to avoiding post-discharge deterioration and evaluated against post-discharge ER return rates.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release B (id=18), evidenced in variants like V0068 and V0145.

**Goal-model linkage:** 18 (Task): Release B

**Coverage:** macro 55/846 variants (6.5%) · micro 56/1050 cases (5.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 16.61, nearest other category `release_a` at mean distance 15.09

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.248, nearest other category `release_d` at mean distance 0.545

## Release C (`release_c`)

Specialized release pathway for long-stay or complex admitted cases, aligned with avoiding post-discharge deterioration.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release C (id=19), evidenced by long-running variant V0710.

**Goal-model linkage:** 19 (Task): Release C

**Coverage:** macro 25/846 variants (3.0%) · micro 25/1050 cases (2.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 22.84, nearest other category `release_a` at mean distance 18.16

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.271, nearest other category `release_d` at mean distance 0.435

## Release D (`release_d`)

Alternative discharge routing for inpatient cases to prevent post-discharge deterioration.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release D (id=20), observed in variant V0273.

**Goal-model linkage:** 20 (Task): Release D

**Coverage:** macro 23/846 variants (2.7%) · micro 23/1050 cases (2.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 19.17, nearest other category `release_a` at mean distance 16.95

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.296, nearest other category `release_c` at mean distance 0.435

## Release E (`release_e`)

Designated discharge alternative for specific inpatient disposition scenarios.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative Release E (id=21).

**Goal-model linkage:** 21 (Task): Release E

**Coverage:** macro 6/846 variants (0.7%) · micro 6/1050 cases (0.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 17.67, nearest other category `release_a` at mean distance 16.40

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.253, nearest other category `release_d` at mean distance 0.443

## Release F (`release_f`)

Alternative discharge routing option for concluding an admitted patient stay.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative Release F (id=112).

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

146/846 variants (17.3%), 301/1050 cases (28.7%) unassigned.

- `V0001`: This narrative ends at ER Sepsis Triage without any admission or discharge pathway, so it does not realize any of the release categories.
- `V0002`: This narrative terminates at CRP testing in the ER without reaching an inpatient admission or discharge pathway.
- `V0003`: This narrative ends with Leucocytes testing in the ER and does not involve admission or release.
- `V0004`: This variant concludes with IV Antibiotics administration in the ER without proceeding to admission or discharge.
- `V0005`: This narrative terminates with LacticAcid testing in the emergency department and does not involve admission or release.
- `V0006`: The process ends with IV Antibiotics in the ER and does not progress to an inpatient admission and subsequent release.
- `V0007`: This narrative stops at IV Antibiotics in the emergency department without any admission or release activities.
- `V0009`: This narrative concludes with IV Antibiotics in the ER and does not include an admission or release outcome.
- `V0010`: This variant loops back to ER Sepsis Triage and does not result in an inpatient admission or release.
- `V0011`: The process finishes with IV Antibiotics in the ER without progressing to admission or discharge steps.
- `V0012`: This narrative concludes with IV Antibiotics in the emergency department and lacks admission or release events.
- `V0013`: This variant ends at Leucocytes in the ER and does not reach an admission or discharge pathway.
- `V0017`: This narrative ends at ER Sepsis Triage and does not involve any admission or discharge activities.
- `V0019`: This process concludes with IV Antibiotics in the ER without proceeding to admission or discharge.
- `V0020`: This narrative ends with CRP testing in the ER and lacks admission or release events.
- `V0024`: This narrative terminates at Admission NC and does not reach a discharge/release activity.
- `V0025`: This variant ends with IV Antibiotics in the emergency department without any admission or release events.
- `V0027`: The narrative ends at IV Antibiotics without reaching a discharge pathway.
- `V0029`: The narrative terminates at Leucocytes without reaching a discharge event.
- `V0031`: The narrative terminates at LacticAcid without an admission or discharge event.
- `V0034`: The narrative ends at IV Liquid without reaching a discharge pathway.
- `V0036`: The narrative terminates at CRP without reaching a discharge pathway.
- `V0038`: The narrative ends at IV Antibiotics and does not reach a discharge event.
- `V0040`: The narrative terminates at Admission NC without reaching a discharge outcome.
- `V0043`: The narrative terminates at LacticAcid without any admission or release activities.
- `V0050`: The narrative ends at CRP without reaching an admission or discharge pathway.
- `V0056`: Variant ends in IV Antibiotics, not a release outcome.
- `V0062`: Variant terminates at IV Antibiotics without a release activity.
- `V0081`: The narrative ends with IV Liquid and does not reach any release or discharge category.
- `V0088`: The narrative concludes with IV Antibiotics and does not reach any release or discharge outcome.
- `V0092`: The narrative ends with LacticAcid and does not reach a discharge or release category.
- `V0111`: The narrative terminates at Admission NC and does not reach any release or discharge outcome.
- `V0127`: The process ends with LacticAcid rather than a discharge or release event, so no release category applies.
- `V0132`: The narrative terminates at IV Antibiotics without any discharge or release event.
- `V0133`: The process ends at IV Antibiotics and does not reach any release category.
- `V0137`: The variant ends at LacticAcid without proceeding to any discharge or release activity.
- `V0146`: The process ends at Leucocytes without reaching any discharge or release activity.
- `V0148`: The narrative ends at IV Antibiotics without any release event.
- `V0151`: The narrative concludes with Release D, which does not match any of the standard release categories A, B, C, E, or F.
- `V0187`: The narrative ends abruptly at CRP without any discharge or release activity.
- `V0197`: The narrative terminates at Leucocytes without featuring a release or discharge event.
- `V0217`: The narrative terminates at IV Antibiotics without reaching any discharge or release category.
- `V0219`: The trace stops at Leucocytes and does not conclude with a release activity.
- `V0232`: The process terminates at IV Antibiotics without reaching any release or discharge activity.
- `V0234`: The process stops at Leucocytes and does not conclude with a release pathway.
- `V0260`: The narrative terminates at IV Antibiotics without reaching a discharge or release activity.
- `V0268`: The narrative ends abruptly at Leucocytes without reaching a release or discharge activity.
- `V0287`: The narrative does not conclude with any release activity, but stops at CRP.
- `V0292`: The process stops at Leucocytes without reaching any release or discharge activity.
- `V0295`: The variant terminates at IV Antibiotics without concluding the stay with a release activity.
- `V0302`: The variant ends at ER Sepsis Triage and does not represent a release pathway.
- `V0305`: The variant ends at IV Antibiotics and does not reach a discharge or release activity.
- `V0322`: The variant ends at IV Antibiotics and does not reach a release activity.
- `V0325`: The variant ends at IV Antibiotics and does not reach a release activity.
- `V0330`: The narrative ends with IV Liquid and does not conclude with a release pathway.
- `V0336`: The narrative ends with CRP and does not complete a release pathway.
- `V0342`: The narrative ends with CRP and does not complete a release pathway.
- `V0349`: The narrative terminates at ER Sepsis Triage and does not complete a release.
- `V0365`: The narrative does not conclude with a release activity, so no release category applies.
- `V0368`: The narrative terminates at Admission NC and does not feature a release event.
- `V0374`: The narrative terminates at Leucocytes and lacks any release activity.
- `V0378`: The narrative ends with IV Antibiotics rather than a release outcome, so none of the release categories fit.
- `V0379`: The narrative concludes with IV Antibiotics instead of a discharge event.
- `V0382`: The patient returns to the ER after Release A, so the final outcome is Return ER which does not fit any release category.
- `V0385`: The narrative ends with Return ER following Release A, meaning it does not cleanly realize a final release category.
- `V0386`: The final activity is Return ER, rendering the category inapplicable.
- `V0398`: The case ends with Return ER, which does not fit any of the release categories.
- `V0411`: The final activity is Leucocytes and does not conclude with a recognized release pathway event.
- `V0415`: The process stops at Admission NC and does not complete a release pathway.
- `V0417`: The process loops back and ends with ER Triage without reaching a release category.
- `V0429`: The narrative stops at IV Antibiotics and does not conclude with a discharge or release event matching the taxonomy.
- `V0462`: The variant ends in CRP and does not complete a release or discharge activity.
- `V0488`: The narrative does not conclude with a release pathway, ending in IV Liquid instead.
- `V0492`: The narrative does not conclude with a release pathway, ending in IV Liquid instead.
- `V0495`: The narrative does not conclude with a release pathway, ending in IV Antibiotics instead.
- `V0501`: The outcome is IV Liquid, meaning the patient was not discharged through a release pathway.
- `V0502`: The outcome is Admission NC, which is an intermediate admission step rather than a release pathway.
- `V0507`: The outcome is IV Antibiotics, which represents ongoing treatment rather than discharge.
- `V0510`: The outcome is IV Antibiotics, which is an in-hospital treatment step, not a release pathway.
- `V0516`: The outcome is Leucocytes, which is a diagnostic lab test, not a discharge pathway.
- `V0517`: The outcome is ER Triage, which is an early diagnostic/triage step, not a release pathway.
- `V0549`: The narrative terminates at IV Liquid without reaching any discharge or release category.
- `V0556`: The narrative ends with Return ER after an initial Release A, which does not map cleanly to any single release category's successful outcome criteria without returning.
- `V0558`: The narrative results in a Return ER outcome after Release A, representing a post-discharge ER return.
- `V0559`: The narrative concludes with a Return ER outcome following Release A.
- `V0560`: The narrative results in a Return ER outcome following Release A.
- `V0564`: The narrative ends with a Return ER outcome after Release A.
- `V0565`: The narrative ends with Admission NC, failing to reach any final discharge or release state.
- `V0567`: The narrative results in a Return ER outcome after Release A.
- `V0573`: The narrative ends with a Return ER outcome following Release A.
- `V0575`: The narrative ends with Leucocytes and does not reach any release or discharge outcome.
- `V0580`: The process variant terminates at CRP without reaching any discharge or release activity.
- `V0584`: The process variant terminates at IV Liquid without reaching a discharge disposition.
- `V0585`: The process variant terminates at LacticAcid without reaching a release activity.
- `V0587`: The process variant terminates at CRP without any release or discharge action.
- `V0592`: The process variant terminates at IV Antibiotics without reaching a discharge destination.
- `V0605`: Although the patient was initially released via Release A, the variant resulted in a Return ER, so it does not fit standard successful release categories.
- `V0614`: The narrative results in a Return ER after Release A, therefore falling outside the standard pathway evaluated successfully.
- `V0615`: The narrative ends with a Return ER following Release C, preventing it from fitting cleanly into standard successful discharge outcomes.
- `V0625`: The narrative results in a Return ER following Release A, meaning it does not fit standard successful release categories.
- `V0636`: The variant does not end with a recognized release outcome, terminating instead at LacticAcid.
- `V0644`: The variant terminates at CRP without reaching any recognized release category.
- `V0645`: The process variant terminates at LacticAcid without a proper release outcome.
- `V0654`: The variant terminates in Leucocytes without reaching a release pathway.
- `V0663`: The narrative terminates at Admission NC without concluding with a release activity.
- `V0664`: The process ends at IV Liquid and does not reach a discharge category.
- `V0670`: The process ends with Leucocytes following an unsuccessful discharge attempt.
- `V0676`: The narrative ends with IV Antibiotics and does not conclude with a release activity.
- `V0679`: The narrative ends with IV Antibiotics and does not conclude with a release activity.
- `V0685`: The narrative ends with IV Antibiotics and does not conclude with a release activity.
- `V0689`: The narrative ends with IV Antibiotics and does not conclude with a release activity.
- `V0694`: The narrative ends with ER Sepsis Triage and does not conclude with a release activity.
- `V0703`: The narrative ends with IV Liquid rather than a discharge event, so it does not realize any of the release categories.
- `V0707`: The narrative ends with Admission NC and does not complete a release pathway.
- `V0708`: The narrative ends with IV Antibiotics and does not reach a discharge event.
- `V0713`: The narrative ends with IV Antibiotics and does not realize any release category.
- `V0742`: The narrative does not conclude with a release activity (outcome is LacticAcid).
- `V0750`: The narrative does not result in a release outcome, terminating at IV Antibiotics.
- `V0759`: The narrative terminates at IV Antibiotics and does not conclude with a release pathway.
- `V0764`: The narrative stops at ER Sepsis Triage and does not represent a discharge pathway.
- `V0772`: The process terminates at CRP and does not complete a discharge pathway.
- `V0774`: The sequence ends at ER Sepsis Triage without reaching any release activity.
- `V0775`: The narrative concludes at CRP and does not contain any discharge or release event.
- `V0777`: The narrative does not conclude with an admitted case release pathway, terminating at Leucocytes.
- `V0778`: The process terminates at Leucocytes without reaching a discharge or release activity.
- `V0779`: The process outcome is Return ER following Release A, which does not fit standard categorization cleanly or terminates in an ER return.
- `V0785`: The ultimate outcome is Return ER after a release, falling outside the basic release taxonomy.
- `V0787`: The outcome is Return ER, rendering standard discharge categorization inapplicable.
- `V0791`: Terminates at IV Antibiotics without concluding an admitted stay.
- `V0794`: Ends with Return ER following Release A, outside standard successful release categories.
- `V0797`: Terminates in Return ER after a brief release.
- `V0798`: Terminates in Return ER.
- `V0804`: The narrative results in a Return ER outcome after Release A, so it does not cleanly realize a sole release category without subsequent return.
- `V0806`: The narrative results in a Return ER outcome after Release A, indicating post-discharge ER return rather than just a completed release category.
- `V0808`: The narrative concludes with Return ER after Release A.
- `V0812`: The narrative results in a Return ER outcome.
- `V0815`: The narrative concludes with Return ER.
- `V0816`: The narrative stops at IV Antibiotics without reaching a discharge or release category.
- `V0820`: The narrative terminates at LacticAcid without any discharge or release event.
- `V0821`: The narrative concludes with a Return ER outcome.
- `V0822`: The narrative concludes with a Return ER outcome.
- `V0823`: The narrative concludes with a Return ER outcome.
- `V0825`: The narrative concludes with a Return ER outcome.
- `V0826`: The narrative ends with Admission NC and does not feature a release or discharge activity, so no release category applies.
- `V0832`: The process terminates at IV Antibiotics without any discharge or release activity.
- `V0843`: The process concludes at IV Liquid without reaching a release or discharge step.
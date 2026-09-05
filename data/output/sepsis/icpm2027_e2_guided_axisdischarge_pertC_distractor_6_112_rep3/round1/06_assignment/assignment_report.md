# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_axisdischarge_pertC_distractor_6_112_rep3` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Release A (`release_a`)

Standard patient release path from an inpatient ward, contributing to avoiding post-discharge deterioration and measured against post-discharge ER returns.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release A (id=17), observed frequently in the narrative sample (e.g. V0008, V0065, V0070) culminating in normal discharge.

**Goal-model linkage:** 17 (Task): Release A

**Coverage:** macro 589/846 variants (69.6%) · micro 633/1050 cases (60.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.33, nearest other category `release_b` at mean distance 15.11

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.346, nearest other category `release_d` at mean distance 0.443

## Release B (`release_b`)

Alternative inpatient release path B, contributing to avoiding post-discharge deterioration and measured against post-discharge ER returns.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release B (id=18), explicitly observed in rare variants such as V0068 and V0145.

**Goal-model linkage:** 18 (Task): Release B

**Coverage:** macro 54/846 variants (6.4%) · micro 55/1050 cases (5.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 16.68, nearest other category `release_a` at mean distance 15.11

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.230, nearest other category `release_c` at mean distance 0.539

## Release C (`release_c`)

Alternative inpatient release path C, contributing to avoiding post-discharge deterioration and measured against post-discharge ER returns.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release C (id=19), observed in long-running complex variants like V0710.

**Goal-model linkage:** 19 (Task): Release C

**Coverage:** macro 22/846 variants (2.6%) · micro 22/1050 cases (2.1%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 24.46, nearest other category `release_a` at mean distance 19.03

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.221, nearest other category `release_d` at mean distance 0.446

## Release D (`release_d`)

Alternative inpatient release path D, contributing to avoiding post-discharge deterioration and measured against post-discharge ER returns.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release D (id=20), observed in variant V0273.

**Goal-model linkage:** 20 (Task): Release D

**Coverage:** macro 24/846 variants (2.8%) · micro 24/1050 cases (2.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 19.12, nearest other category `release_a` at mean distance 17.04

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.300, nearest other category `release_e` at mean distance 0.440

## Release E (`release_e`)

Alternative inpatient release path E, contributing to avoiding post-discharge deterioration and measured against post-discharge ER returns.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release E (id=21) as defined in the goal model decomposition for id=6.

**Goal-model linkage:** 21 (Task): Release E

**Coverage:** macro 6/846 variants (0.7%) · micro 6/1050 cases (0.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 17.67, nearest other category `release_a` at mean distance 16.36

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.253, nearest other category `release_d` at mean distance 0.440

## Release F (`release_f`)

Alternative inpatient release path F, contributing to avoiding post-discharge deterioration and measured against post-discharge ER returns.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release F (id=112) as defined in the goal model decomposition for id=6.

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

151/846 variants (17.8%), 310/1050 cases (29.5%) unassigned.

- `V0001`: This narrative ends at ER Sepsis Triage and does not involve any patient release path from an inpatient ward.
- `V0002`: This narrative ends at CRP testing during the ER phase and does not reach inpatient admission or release.
- `V0003`: This narrative terminates at Leucocytes testing in the ER and does not represent an inpatient release path.
- `V0004`: This narrative ends with IV Antibiotics administration in the ER and does not include inpatient admission and release.
- `V0005`: This narrative concludes with LacticAcid testing in the ER and does not proceed to an inpatient ward or release.
- `V0006`: This narrative finishes with IV Antibiotics in the ER without any subsequent inpatient admission or release path.
- `V0007`: This narrative ends at IV Antibiotics in the ER and lacks inpatient admission and release stages.
- `V0009`: This sequence ends with IV Antibiotics in the ER and does not involve inpatient admission or release.
- `V0010`: This narrative finishes with ER Sepsis Triage and does not represent an inpatient release pathway.
- `V0011`: This process variant terminates upon administering IV Antibiotics in the ER, without proceeding to inpatient care.
- `V0012`: This narrative concludes with IV Antibiotics in the emergency setting and does not reach an inpatient ward.
- `V0013`: This narrative terminates at Leucocytes testing in the ER and does not include inpatient release.
- `V0017`: This narrative ends at ER Sepsis Triage and does not feature inpatient admission or release.
- `V0019`: This narrative concludes with IV Antibiotics in the ER and does not reach inpatient release paths.
- `V0020`: This narrative ends at CRP testing in the ER and lacks inpatient admission and release.
- `V0021`: Although the patient is admitted and receives Release A, the final outcome of this variant is a return to the ER, placing it outside a standard successful release category.
- `V0023`: Although Release A occurs, the variant concludes with Return ER, indicating a return to the emergency room rather than a successful standard release path outcome.
- `V0024`: This narrative terminates at Admission NC and does not complete an inpatient release path.
- `V0025`: This narrative ends with IV Antibiotics in the emergency department without inpatient admission or release.
- `V0027`: The process ends at 'IV Antibiotics' without a release activity.
- `V0029`: The process ends at 'Leucocytes' without any release event.
- `V0031`: The process ends at 'LacticAcid' without reaching a release phase.
- `V0034`: The process terminates at 'IV Liquid' before any inpatient release.
- `V0036`: The sequence ends at 'CRP' without a release step.
- `V0038`: The variant ends at 'IV Antibiotics' without an inpatient release.
- `V0040`: The process stops at 'Admission NC' without a subsequent release path.
- `V0043`: The process ends at 'LacticAcid' without reaching a release.
- `V0050`: The process ends at 'CRP' without any release activity.
- `V0056`: The process terminates at IV Antibiotics without reaching a release category.
- `V0062`: The process terminates at IV Antibiotics without reaching any release category.
- `V0081`: The narrative ends at IV Liquid without reaching any patient release path, so no release category fits.
- `V0088`: The narrative ends at IV Antibiotics without reaching any patient release path, so no release category fits.
- `V0092`: The narrative ends at LacticAcid without reaching any patient release path, so no release category fits.
- `V0111`: The narrative outcome is Admission NC, so it does not realize any of the release paths.
- `V0127`: The variant ends with LacticAcid and does not show an inpatient release activity.
- `V0132`: The variant stops at IV Antibiotics without reaching a release activity.
- `V0133`: The process terminates at IV Antibiotics without any discharge or release event.
- `V0137`: The process stops at LacticAcid and does not contain a release step.
- `V0146`: The process ends at Leucocytes without reaching a release category.
- `V0148`: The variant stops at IV Antibiotics without an inpatient release.
- `V0187`: The narrative does not reach any release activity, terminating at CRP without fulfilling any release path.
- `V0197`: The narrative terminates at Leucocytes without reaching any release category.
- `V0217`: The narrative ends with IV Antibiotics and does not reach any of the release paths.
- `V0219`: The narrative ends with Leucocytes and does not reach any of the release paths.
- `V0232`: The narrative outcome is IV Antibiotics, which does not match any of the release categories.
- `V0234`: The narrative outcome is Leucocytes, which does not match any of the release categories.
- `V0260`: The narrative ends in IV Antibiotics without reaching any inpatient release path.
- `V0268`: The narrative ends in Leucocytes without reaching any inpatient release path.
- `V0287`: The process terminates at CRP and does not reach any release category.
- `V0292`: The process terminates at Leucocytes and does not reach any release category.
- `V0295`: The process terminates at IV Antibiotics and does not reach any release category.
- `V0302`: The narrative terminates at ER Sepsis Triage and does not complete a release path.
- `V0305`: The process terminates at IV Antibiotics without reaching a release path.
- `V0309`: The process ends at Admission NC after a mention of Release B midway, which does not constitute a final release category path.
- `V0322`: The process terminates at IV Antibiotics without reaching any patient release category.
- `V0325`: The narrative stops at IV Antibiotics and does not complete a release path.
- `V0330`: The variant ends in IV Liquid and does not reach a release path.
- `V0336`: The variant ends at CRP and does not complete a release.
- `V0342`: The variant ends at CRP and does not complete a release.
- `V0349`: The variant ends at ER Sepsis Triage and does not complete a release.
- `V0365`: The narrative terminates in lab tests (Leucocytes) and does not realize any of the release path categories.
- `V0368`: The narrative terminates at Admission NC and does not reach any patient release category.
- `V0374`: The narrative ends with Leucocytes and does not complete a patient release path.
- `V0378`: The narrative ends in IV Antibiotics rather than any inpatient release path.
- `V0379`: The narrative ends in IV Antibiotics without reaching a discharge or release category.
- `V0411`: The variant does not cleanly realize a final release category as it contains extended lab loops and ends with additional diagnostic activities rather than a clear release.
- `V0415`: The variant ends prematurely at Admission NC and does not reach any release category.
- `V0417`: The process ends unexpectedly with ER Triage without reaching any ward admission or release path.
- `V0427`: The narrative outcome is Return ER following Release C, which goes beyond the standard release scope.
- `V0429`: The narrative ends with IV Antibiotics and does not reach any patient release category.
- `V0435`: The narrative outcome is Return ER after Release A, so it does not fit a clean single release category.
- `V0440`: The narrative outcome is Return ER after Release A.
- `V0441`: The narrative outcome is Return ER after Release A.
- `V0442`: The narrative outcome is Return ER after Release A.
- `V0443`: The narrative outcome is Return ER after Release A.
- `V0447`: The narrative outcome is Return ER following Release C.
- `V0448`: The narrative outcome is Return ER following Release A.
- `V0449`: The narrative outcome is Return ER following Release A.
- `V0462`: The process terminates with CRP instead of any release activity, thus falling into the residual.
- `V0488`: The narrative does not conclude with any release path, terminating at IV Liquid.
- `V0492`: The narrative does not conclude with any release path, terminating at IV Liquid.
- `V0495`: The narrative does not conclude with any release path, terminating at IV Antibiotics.
- `V0501`: The narrative ends with IV Liquid and does not reach a final inpatient release path category.
- `V0502`: The narrative ends with Admission NC and does not reach a final inpatient release path.
- `V0507`: The narrative terminates at IV Antibiotics and does not reach an inpatient release path.
- `V0510`: The narrative ends with IV Antibiotics without reaching a release path.
- `V0516`: The narrative ends with Leucocytes and does not reach a release path.
- `V0517`: The narrative ends with ER Triage and does not reach a release path.
- `V0549`: The variant terminates at IV Liquid and does not reach any release category.
- `V0565`: The narrative terminates at Admission NC and does not reach any release category.
- `V0575`: The narrative ends prematurely at Leucocytes and does not complete any release path.
- `V0580`: The narrative ends with CRP, meaning the patient was not released from the inpatient ward.
- `V0584`: The narrative terminates at IV Liquid within the ER phase and does not reach an inpatient release path.
- `V0585`: The process terminates at LacticAcid in the ER without proceeding to inpatient release.
- `V0587`: The variant ends with CRP during the diagnostic workup without an inpatient release.
- `V0592`: The sequence stops at IV Antibiotics in the ER and does not represent an inpatient release path.
- `V0605`: Although the narrative contains Release A, the final outcome is Return ER, representing post-discharge deterioration rather than successful standard release.
- `V0614`: Although the narrative contains Release A, the final outcome is Return ER, indicating post-discharge deterioration.
- `V0615`: Although the intermediate outcome is Release C, the final outcome is Return ER, indicating failure against post-discharge ER returns.
- `V0625`: Although the intermediate outcome is Release A, the final outcome is Return ER, indicating post-discharge deterioration.
- `V0636`: The narrative ends with LacticAcid and does not reach any release activity, hence no release category fits.
- `V0644`: The narrative ends with CRP and does not complete a patient release path.
- `V0645`: The narrative terminates at LacticAcid without completing any release path.
- `V0654`: The process variant ends with Leucocytes and does not culminate in any recognized release path.
- `V0663`: The process variant ends with Admission NC and does not reach a release activity.
- `V0664`: The process variant terminates at IV Liquid and does not reach any release category.
- `V0676`: The narrative ends with IV Antibiotics and does not reach a patient release path.
- `V0679`: The narrative ends with IV Antibiotics and does not reach a patient release path.
- `V0685`: The narrative ends with IV Antibiotics and does not reach a patient release path.
- `V0689`: The narrative ends with IV Antibiotics and does not reach a patient release path.
- `V0694`: The narrative ends at ER Sepsis Triage and does not reach a patient release path.
- `V0703`: The outcome is IV Liquid, meaning the patient was not released from an inpatient ward in this variant.
- `V0705`: Although the patient was released with Release A initially, the variant results in a Return ER outcome representing post-discharge deterioration, fitting outside standard successful paths.
- `V0707`: The process ends at Admission NC without a release event.
- `V0708`: The process terminates at IV Antibiotics without concluding in a release category.
- `V0712`: The narrative leads to Return ER after an initial Release A, failing to maintain successful post-discharge status.
- `V0713`: The process terminates at IV Antibiotics without a patient release.
- `V0719`: The process results in a Return ER outcome, making it part of the residual category.
- `V0720`: The process results in a Return ER outcome after Release A, fitting into the residual.
- `V0721`: The process results in a Return ER outcome following Release A, fitting into the residual.
- `V0724`: The process ends with a Return ER outcome after Release A.
- `V0742`: The outcome is 'LacticAcid', not a release path.
- `V0750`: The outcome is 'IV Antibiotics', not a release path.
- `V0759`: The outcome is IV Antibiotics, not a patient release path.
- `V0764`: The outcome is ER Sepsis Triage, which does not realize any patient release path.
- `V0772`: The final activity is CRP, so no release path is realized.
- `V0774`: The outcome is ER Sepsis Triage, not a release path.
- `V0775`: The outcome is CRP, which is not a patient release path.
- `V0777`: The process terminates at Leucocytes without reaching any discharge or release activity, hence no release category applies.
- `V0778`: The process ends at Leucocytes without reaching a patient release or ward discharge step.
- `V0779`: The narrative includes a return to the ER after Release A, but as an incomplete or non-standard pattern regarding the primary taxonomy focus, or failing to match a distinct path safely.
- `V0785`: The narrative features a return to the ER after an intermediate release, not cleanly falling under a single primary release path classification without residual classification.
- `V0787`: The case results in a return to the ER after an initial release, leaving it outside the standard mapped pathways.
- `V0791`: The process terminates at IV Antibiotics without any ward admission or release activity.
- `V0794`: The patient returns to the ER following a release, representing a complex or residual trajectory.
- `V0797`: The narrative involves an extremely long duration and subsequent return to the ER following release, falling into the residual category.
- `V0798`: The narrative shows a return to the ER after a long delay following Release A, fitting the residual classification.
- `V0804`: The patient returns to the ER after Release A, so it does not fit the successful post-discharge deterioration avoidance criteria directly.
- `V0806`: The narrative results in a Return ER event after Release A.
- `V0808`: The narrative results in a Return ER event after Release A.
- `V0812`: The narrative results in a Return ER event after Release A.
- `V0815`: The narrative results in a Return ER event after Release A.
- `V0816`: The process terminates at IV Antibiotics without reaching a discharge or release category.
- `V0820`: The process terminates at LacticAcid without reaching a discharge or release category.
- `V0821`: The narrative results in a Return ER event after Release A.
- `V0822`: The narrative results in a Return ER event after Release A.
- `V0823`: The narrative results in a Return ER event after Release A.
- `V0825`: The narrative results in a Return ER event after Release A.
- `V0826`: The narrative ends with Admission NC and does not complete a patient release path (Release A-F).
- `V0832`: The narrative terminates at IV Antibiotics without reaching any patient release path.
- `V0843`: The narrative terminates at IV Liquid without reaching a release path.
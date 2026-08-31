# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_pertA_remove_21_rep1` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Admission to Normal Care Inpatient Ward (`admission_nc`)

Patients are admitted to a standard non-ICU inpatient ward (Admission NC). This advances the organization's goal of reaching a documented disposition, though extended stays or repeated ward transfers can impact overall care progression.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative id=15 (Admission NC) under the OR-decomposed goal 5. Supported by variants such as V0008, V0625, and V0551.

**Goal-model linkage:** 15 (Task): Admission NC

**Coverage:** macro 74/846 variants (8.7%) · micro 116/1050 cases (11.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 7.94, nearest other category `release_a` at mean distance 10.26

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.471, nearest other category `release_a` at mean distance 0.432

## Admission to Intensive Care Ward (`admission_ic`)

Patients are admitted directly to an Intensive Care unit (Admission IC). While necessary for critical stabilization, it carries a negative contribution (-25) to minimizing time-to-treatment softgoals due to higher coordination overhead.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative id=16 (Admission IC) under the OR-decomposed goal 5. Supported by variants such as V0605, V0317, V0273, and V0068.

**Goal-model linkage:** 16 (Task): Admission IC

**Coverage:** macro 7/846 variants (0.8%) · micro 7/1050 cases (0.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 29.29, nearest other category `release_d` at mean distance 23.73

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.366, nearest other category `release_a` at mean distance 0.413

## Discharge Disposition Type A (`release_a`)

Patient is discharged via pathway Release A, contributing positively (+50) to avoiding post-discharge deterioration and measured against post-discharge ER return indicators.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative id=17 (Release A) under the OR-decomposed goal 6. Supported by variants such as V0008, V0551, V0625, and V0449.

**Goal-model linkage:** 17 (Task): Release A

**Coverage:** macro 521/846 variants (61.6%) · micro 527/1050 cases (50.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.81, nearest other category `admission_nc` at mean distance 10.26

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.344, nearest other category `admission_ic` at mean distance 0.413

## Discharge Disposition Type B (`release_b`)

Patient is discharged via pathway Release B, helping to avoid post-discharge deterioration as measured by post-discharge ER return indicators.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative id=18 (Release B) under the OR-decomposed goal 6. Supported by rare variant samples such as V0068 and V0145.

**Goal-model linkage:** 18 (Task): Release B

**Coverage:** macro 51/846 variants (6.0%) · micro 51/1050 cases (4.9%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 17.07, nearest other category `admission_nc` at mean distance 13.97

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.230, nearest other category `admission_ic` at mean distance 0.509

## Discharge Disposition Type C (`release_c`)

Patient is discharged via pathway Release C, representing specialized extended treatment release outcomes.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative id=19 (Release C) under the OR-decomposed goal 6. Supported by complex long-duration variant V0710.

**Goal-model linkage:** 19 (Task): Release C

**Coverage:** macro 23/846 variants (2.7%) · micro 23/1050 cases (2.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 23.04, nearest other category `admission_nc` at mean distance 17.24

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.243, nearest other category `release_d` at mean distance 0.425

## Discharge Disposition Type D (`release_d`)

Patient is discharged via pathway Release D, representing alternative complex clinical release flows.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative id=20 (Release D) under the OR-decomposed goal 6. Supported by length-high variant V0273.

**Goal-model linkage:** 20 (Task): Release D

**Coverage:** macro 23/846 variants (2.7%) · micro 23/1050 cases (2.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 14.47, nearest other category `admission_nc` at mean distance 13.91

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.302, nearest other category `admission_ic` at mean distance 0.413

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0084` / `V0710` (category `release_c`): structural=174, profile=0.253
- `V0615` / `V0710` (category `release_c`): structural=174, profile=0.504
- `V0138` / `V0710` (category `release_c`): structural=173, profile=0.253
- `V0313` / `V0710` (category `release_c`): structural=173, profile=0.165
- `V0314` / `V0710` (category `release_c`): structural=173, profile=0.148
- `V0427` / `V0710` (category `release_c`): structural=173, profile=0.418
- `V0433` / `V0710` (category `release_c`): structural=173, profile=0.313
- `V0601` / `V0710` (category `release_c`): structural=173, profile=0.248
- `V0710` / `V0747` (category `release_c`): structural=173, profile=0.049
- `V0423` / `V0710` (category `release_c`): structural=172, profile=0.126

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0008` (`admission_nc`) / `V0058` (`release_a`): structural=1, profile=0.011
- `V0008` (`admission_nc`) / `V0686` (`release_a`): structural=1, profile=0.454
- `V0008` (`admission_nc`) / `V0706` (`release_a`): structural=1, profile=0.029
- `V0008` (`admission_nc`) / `V0766` (`release_a`): structural=1, profile=0.336
- `V0014` (`admission_nc`) / `V0058` (`release_a`): structural=1, profile=0.015
- `V0015` (`admission_nc`) / `V0116` (`release_a`): structural=1, profile=0.429
- `V0015` (`admission_nc`) / `V0122` (`release_a`): structural=1, profile=0.056
- `V0015` (`admission_nc`) / `V0758` (`release_a`): structural=1, profile=0.120
- `V0016` (`admission_nc`) / `V0362` (`release_a`): structural=1, profile=0.006
- `V0016` (`admission_nc`) / `V0431` (`release_a`): structural=1, profile=0.002

## Residual

147/846 variants (17.4%), 303/1050 cases (28.9%) unassigned.

- `V0001`: The narrative ends at ER Sepsis Triage and does not reach any ward admission or discharge category.
- `V0002`: The narrative terminates at CRP testing without any admission or release step.
- `V0003`: The narrative ends with Leucocytes testing, lacking admission or discharge dispositions.
- `V0004`: The narrative concludes at IV Antibiotics administration and does not enter an inpatient ward or discharge flow.
- `V0005`: The case stops at LacticAcid without proceeding to admission or release.
- `V0006`: The narrative ends at IV Antibiotics without any admission or release categories.
- `V0007`: The trace concludes at IV Antibiotics and does not reach ward admission or release.
- `V0009`: The sequence stops at IV Antibiotics and does not include admission or release events.
- `V0010`: The narrative terminates at ER Sepsis Triage without reaching admission or discharge.
- `V0011`: The trace ends at IV Antibiotics without any ward admission or release disposition.
- `V0012`: The sequence ends at IV Antibiotics without reaching admission or release.
- `V0013`: The narrative finishes at Leucocytes and lacks admission or release steps.
- `V0017`: The trace terminates at ER Sepsis Triage without admission or release.
- `V0019`: The trace finishes at IV Antibiotics and does not reach admission or release.
- `V0020`: The sequence terminates at CRP testing without admission or release disposition.
- `V0025`: The sequence ends at IV Antibiotics without any admission or release events.
- `V0027`: The narrative stops at IV Antibiotics without reaching admission or release.
- `V0029`: The narrative finishes at Leucocytes without admission or release dispositions.
- `V0031`: The trace terminates at LacticAcid without admission or release.
- `V0034`: The trace finishes at IV Liquid without ward admission or release.
- `V0036`: The sequence terminates at CRP testing without admission or release.
- `V0038`: The narrative ends at IV Antibiotics without reaching admission or release steps.
- `V0043`: The trace ends at LacticAcid without admission or release disposition.
- `V0050`: The trace terminates at CRP testing without reaching admission or release.
- `V0052`: The variant ends with Return ER after Release A, so it does not cleanly realize a primary release category.
- `V0054`: The variant ends with Return ER following Release A.
- `V0055`: The variant ends with Return ER following Release A.
- `V0056`: The outcome is IV Antibiotics without any admission or release categories realized.
- `V0060`: The variant ends with Return ER.
- `V0062`: The outcome is IV Antibiotics without any admission or release categories realized.
- `V0071`: The variant ends with Return ER.
- `V0072`: The variant ends with Return ER.
- `V0074`: The variant ends with Return ER.
- `V0075`: The variant ends with Return ER.
- `V0078`: The variant ends with Return ER.
- `V0080`: The variant ends with Return ER.
- `V0081`: The outcome is IV Liquid without any admission or release categories realized.
- `V0083`: The variant ends with Return ER.
- `V0085`: The variant ends with Return ER.
- `V0088`: The outcome is IV Antibiotics without any admission or release categories realized.
- `V0089`: The variant ends with Return ER.
- `V0092`: The outcome is LacticAcid without any admission or release categories realized.
- `V0094`: The variant ends with Return ER.
- `V0098`: The variant ends with Return ER.
- `V0127`: The narrative ends at LacticAcid without reaching an admission or discharge goal, falling into the residual.
- `V0132`: The process stops at IV Antibiotics without reaching an admission or release goal, forming part of the residual.
- `V0133`: The narrative ends at IV Antibiotics without any admission or release outcome, placing it in the residual.
- `V0137`: The variant terminates at LacticAcid without any qualifying admission or release outcome, belonging to the residual.
- `V0146`: The narrative stops at Leucocytes without an admission or release milestone, fitting into the residual.
- `V0148`: The process ends at IV Antibiotics without reaching any defined admission or release category, placing it in the residual.
- `V0187`: Incomplete pathway ending in diagnostic assessment; does not match any admission or release goal category.
- `V0196`: The variant ends with an unspecified or malformed release activity (Release E) which is not part of the taxonomy.
- `V0197`: Incomplete process path ending in Leucocytes without reaching any admission or release category.
- `V0217`: The narrative ends at IV Antibiotics without reaching a defined release or admission category.
- `V0219`: The narrative terminates early at Leucocytes without reaching any release or admission stage.
- `V0232`: The narrative terminates at IV Antibiotics without final admission or release categories.
- `V0234`: The narrative ends at Leucocytes without matching any release or admission category.
- `V0260`: The narrative terminates at IV Antibiotics without reaching a ward admission or a recognized release category.
- `V0268`: The narrative ends at Leucocytes without achieving ward admission or any release disposition.
- `V0287`: The narrative ends at CRP without reaching any ward admission or release category.
- `V0292`: The narrative terminates at Leucocytes without reaching any ward admission or release category.
- `V0302`: The outcome is ER Sepsis Triage, which does not represent admission or release.
- `V0305`: The outcome is IV Antibiotics, which does not represent admission or release.
- `V0316`: The outcome is Release E, which does not match any defined category in the taxonomy.
- `V0322`: The outcome is IV Antibiotics, which does not represent admission or release.
- `V0325`: The outcome is IV Antibiotics, which does not represent admission or release.
- `V0330`: The outcome is IV Liquid, which does not represent admission or release.
- `V0336`: The outcome is CRP, which does not represent admission or release.
- `V0342`: The outcome is CRP, which does not represent admission or release.
- `V0349`: The outcome is ER Sepsis Triage, which does not represent admission or release.
- `V0365`: The narrative terminates at Leucocytes without reaching any admission or release category.
- `V0374`: The narrative ends at Leucocytes and does not complete an admission or release goal.
- `V0378`: The narrative stops at IV Antibiotics in the ER phase and does not reach admission or release.
- `V0379`: The process terminates at IV Antibiotics without proceeding to a ward admission or release.
- `V0417`: The narrative loops back to ER Triage and does not complete a ward admission or final release category.
- `V0429`: The narrative ends at IV Antibiotics without reaching a ward admission or release category.
- `V0462`: The outcome is CRP and does not reach any of the specified release or admission endpoints.
- `V0488`: The outcome is IV Liquid and does not reach any of the specified release or admission endpoints.
- `V0492`: The outcome is IV Liquid and does not reach any of the specified release or admission endpoints.
- `V0495`: The outcome is IV Antibiotics and does not reach any of the specified release or admission endpoints.
- `V0507`: The narrative stops at IV Antibiotics without an admission or release event.
- `V0510`: The variant terminates at IV Antibiotics without reaching a ward admission or release category.
- `V0516`: The trace terminates at Leucocytes without an admission or release milestone.
- `V0517`: The trace terminates prematurely at ER Triage.
- `V0549`: The variant ends at IV Liquid without an admission or release event.
- `V0553`: The narrative concludes with Release E, which does not map to any of the standard defined release categories in the taxonomy.
- `V0556`: The outcome is Return ER, which is outside the defined taxonomy categories.
- `V0558`: The outcome is Return ER, not mapped in the taxonomy.
- `V0559`: The outcome is Return ER, which does not fit any taxonomy category.
- `V0560`: The outcome is Return ER.
- `V0564`: The outcome is Return ER.
- `V0567`: The outcome is Return ER.
- `V0573`: The outcome is Return ER.
- `V0575`: The outcome is Leucocytes, which is a diagnostic activity, not a discharge or admission category.
- `V0577`: The outcome is Return ER.
- `V0578`: The outcome is Return ER.
- `V0579`: The outcome is Return ER.
- `V0580`: The outcome is CRP, which is a diagnostic test, not a category.
- `V0584`: The outcome is IV Liquid, which is an ongoing treatment step rather than a taxonomy category.
- `V0585`: The outcome is LacticAcid, a diagnostic test.
- `V0587`: The outcome is CRP, a diagnostic test.
- `V0590`: The outcome is Return ER.
- `V0591`: The outcome is Return ER.
- `V0592`: The outcome is IV Antibiotics, a treatment step.
- `V0595`: The outcome is Return ER.
- `V0598`: The outcome is Release E, which is not in the taxonomy.
- `V0603`: The narrative ends with Release E, which does not match any of the defined categories.
- `V0629`: The narrative ends with Release E, which does not match any of the defined categories.
- `V0636`: The narrative ends with LacticAcid and does not reach a recognized discharge disposition category.
- `V0644`: The narrative terminates at CRP and lacks a recognized discharge disposition.
- `V0645`: The narrative terminates at LacticAcid and lacks a recognized discharge disposition.
- `V0654`: The process terminates at Leucocytes without reaching any of the defined disposition categories.
- `V0664`: The process terminates at IV Liquid and does not reach a ward admission or release disposition.
- `V0676`: The process terminates at IV Antibiotics without reaching any defined discharge or admission category.
- `V0679`: The process terminates at IV Antibiotics without reaching any defined discharge or admission category.
- `V0685`: The process terminates at IV Antibiotics without reaching any defined discharge or admission category.
- `V0689`: The process terminates at IV Antibiotics without reaching any defined discharge or admission category.
- `V0694`: The process terminates at ER Sepsis Triage and does not reach a ward admission or release disposition.
- `V0703`: The narrative does not reach a discharge disposition or admission ward, ending instead at IV Liquid.
- `V0708`: The narrative ends at IV Antibiotics without reaching any admission or release category.
- `V0713`: The narrative ends at IV Antibiotics without reaching any terminal admission or release goal.
- `V0742`: The narrative ends at LacticAcid without realizing any admission or release category.
- `V0750`: The narrative ends at IV Antibiotics without reaching any admission or release category.
- `V0759`: The process terminates at IV Antibiotics without reaching any ward admission or release disposition.
- `V0764`: The narrative terminates early at ER Sepsis Triage without any admission or release categories.
- `V0772`: The sequence stops at CRP following an admission, missing a definitive release or discharge category.
- `V0774`: The sequence terminates at ER Sepsis Triage without reaching admission or release.
- `V0775`: The process ends at CRP without reaching admission or discharge stages.
- `V0777`: The sequence stops at Leucocytes without reaching any admission or release phases.
- `V0778`: The process terminates at Leucocytes without reaching admission or discharge steps.
- `V0791`: The process terminates at IV Antibiotics without an admission or discharge disposition.
- `V0804`: The process variant ends with Return ER, which does not match any discharge or admission category in the taxonomy.
- `V0806`: The process variant ends with Return ER, which does not fit any of the defined categories.
- `V0808`: The process variant ends with Return ER, which is outside the defined taxonomy categories.
- `V0812`: The process variant ends with Return ER, which does not match any of the taxonomy categories.
- `V0815`: The process variant ends with Return ER, which falls outside the scope of the taxonomy categories.
- `V0816`: The process variant terminates at IV Antibiotics, which is not a recognized final release or admission category.
- `V0820`: The process variant terminates at LacticAcid, which is not part of the admission or release categories.
- `V0821`: The process variant ends with Return ER, which does not match any category.
- `V0823`: The process variant ends with Return ER, which does not fit the taxonomy.
- `V0825`: The process variant ends with Return ER, which is not covered by the categories.
- `V0827`: The process variant ends with Return ER, which does not fit any category.
- `V0828`: The process variant ends with Return ER, failing to match any category.
- `V0832`: The process variant terminates at IV Antibiotics, which is not part of the taxonomy.
- `V0834`: The process variant ends with Return ER, which is not represented in the categories.
- `V0842`: The process variant ends with Return ER, which does not match any category.
- `V0843`: The process variant terminates at IV Liquid, which is not a valid category endpoint.
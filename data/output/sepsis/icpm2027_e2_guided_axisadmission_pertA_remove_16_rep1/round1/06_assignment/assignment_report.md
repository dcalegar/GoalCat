# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_axisadmission_pertA_remove_16_rep1` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Admission NC (`admission_nc`)

Patient is admitted to a non-critical inpatient ward, realizing the goal of admitting a sepsis patient to an inpatient care unit.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=15 (Admission NC) under the OR-decomposition of goal id=5. Supported by multiple sampled variants (e.g., V0008, V0625, V0605) where Admission NC is recorded in the trace before discharge or further care steps.

**Goal-model linkage:** 15 (Task): Admission NC

**Coverage:** macro 747/846 variants (88.3%) · micro 799/1050 cases (76.1%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 12.51, nearest other category `None` at mean distance n/a

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.407, nearest other category `None` at mean distance n/a

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0286` / `V0710` (category `admission_nc`): structural=182, profile=0.756
- `V0053` / `V0710` (category `admission_nc`): structural=181, profile=0.788
- `V0351` / `V0710` (category `admission_nc`): structural=181, profile=0.765
- `V0058` / `V0710` (category `admission_nc`): structural=180, profile=0.781
- `V0306` / `V0710` (category `admission_nc`): structural=180, profile=0.664
- `V0309` / `V0710` (category `admission_nc`): structural=180, profile=0.865
- `V0323` / `V0710` (category `admission_nc`): structural=180, profile=0.800
- `V0350` / `V0710` (category `admission_nc`): structural=180, profile=0.670
- `V0489` / `V0710` (category `admission_nc`): structural=180, profile=0.755
- `V0497` / `V0710` (category `admission_nc`): structural=180, profile=0.751

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- none

## Residual

99/846 variants (11.7%), 251/1050 cases (23.9%) unassigned.

- `V0001`: The narrative ends at ER Sepsis Triage and does not include an admission to a non-critical inpatient ward.
- `V0002`: The narrative ends with diagnostic tests (CRP) and does not involve admission to a non-critical inpatient ward.
- `V0003`: The narrative terminates at Leucocytes without patient admission to a non-critical inpatient ward.
- `V0004`: The narrative stops at IV Antibiotics in the emergency phase and does not show an inpatient admission.
- `V0005`: The narrative concludes with LacticAcid testing in the ER without proceeding to non-critical inpatient admission.
- `V0006`: The narrative finishes at IV Antibiotics without an admission event to a non-critical ward.
- `V0007`: The patient receives IV Antibiotics in the ER but is not admitted to a non-critical inpatient ward.
- `V0009`: The sequence terminates at IV Antibiotics without showing an inpatient admission step.
- `V0010`: The narrative ends at ER Sepsis Triage and does not contain any inpatient ward admission activity.
- `V0011`: The pathway ends with IV Antibiotics administration and lacks a non-critical ward admission event.
- `V0012`: The sequence finishes at IV Antibiotics without an admission to a non-critical ward.
- `V0013`: The narrative terminates at Leucocytes and does not include inpatient admission.
- `V0017`: The narrative stops at ER Sepsis Triage and does not record an inpatient admission.
- `V0019`: The sequence ends at IV Antibiotics within the ER phase and does not show an inpatient admission.
- `V0020`: The narrative concludes with CRP measurement and lacks a non-critical ward admission.
- `V0025`: The process terminates with IV Antibiotics and does not involve an inpatient admission event.
- `V0027`: The narrative ends with 'IV Antibiotics' and does not contain any admission activity to a non-critical inpatient ward.
- `V0029`: The narrative ends with 'Leucocytes' and does not contain any admission activity to a non-critical inpatient ward.
- `V0031`: The narrative ends with 'LacticAcid' and does not contain any admission activity to a non-critical inpatient ward.
- `V0034`: The narrative ends with 'IV Liquid' and does not contain any admission activity to a non-critical inpatient ward.
- `V0036`: The narrative ends with 'CRP' and does not contain any admission activity to a non-critical inpatient ward.
- `V0038`: The narrative ends with 'IV Antibiotics' and does not contain any admission activity to a non-critical inpatient ward.
- `V0043`: The narrative ends with 'LacticAcid' and does not contain any admission activity to a non-critical inpatient ward.
- `V0050`: The narrative ends with 'CRP' and does not contain any admission activity to a non-critical inpatient ward.
- `V0056`: The narrative ends with 'IV Antibiotics' and does not contain any admission activity to an inpatient ward.
- `V0062`: The narrative ends with 'IV Antibiotics' and lacks any inpatient ward admission.
- `V0081`: The narrative ends with 'IV Liquid' and does not contain any admission activity, thus not realizing the admission_nc category.
- `V0088`: The narrative terminates at 'IV Antibiotics' and does not include an inpatient ward admission.
- `V0092`: The narrative ends at 'LacticAcid' without proceeding to inpatient ward admission.
- `V0127`: The narrative ends with LacticAcid and does not include any inpatient admission activity.
- `V0132`: The narrative terminates at 'IV Antibiotics' without proceeding to inpatient ward admission.
- `V0133`: The process ends at 'IV Antibiotics' and does not involve admission to a non-critical inpatient ward.
- `V0137`: The narrative ends with 'LacticAcid' and does not show any inpatient ward admission.
- `V0145`: The narrative routes the patient to 'Admission IC' and subsequently releases them, omitting non-critical ward admission.
- `V0146`: The process terminates at 'Leucocytes' and does not contain any admission activity.
- `V0148`: The narrative stops at 'IV Antibiotics' without proceeding to inpatient ward admission.
- `V0167`: The narrative includes 'Admission IC' rather than 'Admission NC', and thus does not realize the non-critical admission category.
- `V0187`: The narrative does not contain an admission to a non-critical inpatient ward ('Admission NC').
- `V0197`: The narrative does not contain an admission to a non-critical inpatient ward ('Admission NC').
- `V0217`: The narrative lacks an admission to a non-critical inpatient ward (Admission NC).
- `V0218`: The narrative includes 'Admission IC' instead of non-critical admission, so it does not realize the admission_nc category.
- `V0219`: The narrative lacks an admission to a non-critical inpatient ward (Admission NC).
- `V0232`: The narrative does not include any admission activity to a non-critical inpatient ward, as it terminates at IV Antibiotics.
- `V0234`: The narrative does not include any admission activity to a non-critical inpatient ward, terminating prematurely at Leucocytes.
- `V0260`: The narrative ends at 'IV Antibiotics' and does not contain any admission activity to a non-critical inpatient ward.
- `V0287`: The narrative ends at 'CRP' and does not contain any inpatient ward admission activity.
- `V0292`: The narrative ends at 'Leucocytes' and does not contain any inpatient ward admission activity.
- `V0302`: The narrative terminates at ER Sepsis Triage and does not include an inpatient admission activity.
- `V0305`: The narrative terminates at IV Antibiotics without proceeding to inpatient admission.
- `V0322`: The narrative terminates at IV Antibiotics without proceeding to an inpatient care unit.
- `V0325`: The narrative terminates at IV Antibiotics without proceeding to inpatient admission.
- `V0330`: The narrative does not include any inpatient admission activity, ending at IV Liquid instead.
- `V0342`: The narrative ends at CRP and does not include an inpatient admission activity.
- `V0349`: The narrative terminates at ER Sepsis Triage without containing any inpatient admission activity.
- `V0365`: The narrative ends in 'Leucocytes' and includes 'Admission IC', meaning it does not realize the goal of admitting a patient to a non-critical inpatient ward.
- `V0378`: The narrative ends with 'IV Antibiotics' and does not contain any admission activity to a non-critical inpatient ward.
- `V0379`: The narrative ends with 'IV Antibiotics' and lacks any inpatient admission step.
- `V0407`: The narrative contains 'Admission IC' instead of 'Admission NC', indicating intensive care rather than a non-critical ward.
- `V0417`: The narrative ends at 'ER Triage' and lacks an admission activity to an inpatient ward.
- `V0429`: The narrative lacks any admission activity and terminates at IV Antibiotics, therefore it does not realize the non-critical admission category.
- `V0432`: The narrative includes 'Admission IC' rather than 'Admission NC', indicating intensive care rather than non-critical admission.
- `V0488`: The narrative ends at 'IV Liquid' and does not contain any admission to a non-critical inpatient ward.
- `V0492`: The narrative ends at 'IV Liquid' and does not contain any admission to a non-critical inpatient ward.
- `V0495`: The narrative ends at 'IV Antibiotics' and does not contain any admission to a non-critical inpatient ward.
- `V0507`: The narrative ends at IV Antibiotics without containing an admission activity, so it does not realize admission to a non-critical inpatient care unit.
- `V0510`: The narrative ends at IV Antibiotics without containing an admission activity, so it does not realize admission to a non-critical inpatient care unit.
- `V0516`: The narrative terminates at Leucocytes without an admission activity, thus not realizing admission to a non-critical inpatient care unit.
- `V0517`: The narrative terminates at ER Triage without any admission activity, thus not realizing admission to a non-critical inpatient care unit.
- `V0549`: The narrative ends at 'IV Liquid' and does not contain any admission activity, hence it does not realize the admission category.
- `V0575`: The narrative does not include any admission to a non-critical inpatient ward, ending with Leucocytes instead.
- `V0580`: The narrative does not include any admission activity to a non-critical inpatient ward, so it does not realize the admission_nc category.
- `V0584`: The narrative does not contain Admission NC, failing to realize the admission_nc category.
- `V0585`: The narrative does not contain Admission NC, failing to realize the admission_nc category.
- `V0587`: The narrative does not contain Admission NC, failing to realize the admission_nc category.
- `V0592`: The narrative does not contain Admission NC, failing to realize the admission_nc category.
- `V0621`: The narrative only shows 'Admission IC' and lacks 'Admission NC', therefore it does not fit the Admission NC category.
- `V0645`: The narrative does not include any admission activity to a non-critical or critical ward, hence it does not realize the category.
- `V0654`: The narrative contains 'Admission IC' instead of 'Admission NC', thus it does not realize admission to a non-critical inpatient ward.
- `V0664`: The narrative does not contain any admission activity, ending at 'IV Liquid'.
- `V0676`: The narrative ends at IV Antibiotics and does not feature admission to a non-critical inpatient ward.
- `V0679`: The patient's care sequence terminates at IV Antibiotics without an inpatient ward admission.
- `V0685`: The treatment sequence concludes with IV Antibiotics and does not involve inpatient ward admission.
- `V0689`: The narrative ends at IV Antibiotics and does not proceed to an inpatient ward admission.
- `V0694`: The process terminates at ER Sepsis Triage and does not reach inpatient admission.
- `V0713`: The narrative lacks an admission to a non-critical inpatient ward, therefore it does not realize the category.
- `V0715`: The narrative routes the patient to 'Admission IC' rather than a non-critical ward, failing to realize the category.
- `V0742`: The narrative does not contain 'Admission NC' and therefore does not realize the corresponding goal.
- `V0750`: The narrative does not contain 'Admission NC' and therefore does not realize the corresponding goal.
- `V0759`: The narrative ends at 'IV Antibiotics' and does not contain any admission activity to a non-critical inpatient ward.
- `V0764`: The narrative terminates at 'ER Sepsis Triage' and does not progress to any inpatient admission.
- `V0774`: The narrative terminates at 'ER Sepsis Triage' and does not progress to any inpatient admission.
- `V0775`: The narrative terminates at 'CRP' and does not contain any admission activity to a non-critical inpatient ward.
- `V0777`: The narrative ends at 'Leucocytes' and does not contain any admission activity to an inpatient care unit.
- `V0778`: The narrative terminates without an inpatient admission activity.
- `V0791`: The narrative terminates at 'IV Antibiotics' without proceeding to any inpatient admission.
- `V0793`: The narrative contains 'Admission IC' rather than 'Admission NC', so it does not realize the non-critical inpatient admission category.
- `V0816`: The narrative does not contain any admission activity, terminating at IV Antibiotics.
- `V0820`: The narrative does not contain any admission activity, terminating at LacticAcid.
- `V0832`: The narrative ends at IV Antibiotics and does not contain any admission activity to an inpatient care unit.
# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_axisadmission_pertA_remove_16_rep2` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Admission Non-Critical (`admission_nc`)

Patient is admitted to a non-critical inpatient ward, advancing the clinical workflow toward final discharge or release while being measured against potential post-discharge complications and ER return rates.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the single declared alternative under the OR-decomposition of goal id=5 (Patient is admitted to an inpatient ward), specifically task id=15 (Admission NC), which is heavily evidenced across multiple sampled variants such as V0008, V0625, V0605, and V0551.

**Goal-model linkage:** 15 (Task): Admission NC

**Coverage:** macro 742/846 variants (87.7%) · micro 794/1050 cases (75.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 12.49, nearest other category `None` at mean distance n/a

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

104/846 variants (12.3%), 256/1050 cases (24.4%) unassigned.

- `V0001`: This narrative stops at ER Sepsis Triage and does not involve admission to a non-critical inpatient ward.
- `V0002`: This narrative ends at CRP testing during the ER phase without admission to a non-critical inpatient ward.
- `V0003`: This narrative ends with Leucocytes testing in the ER and does not involve inpatient admission.
- `V0004`: This narrative concludes with IV Antibiotics administration in the ER and does not involve inpatient admission.
- `V0005`: This narrative concludes with LacticAcid testing in the ER without proceeding to inpatient admission.
- `V0006`: This narrative finishes with IV Antibiotics treatment in the ER and lacks an inpatient admission step.
- `V0007`: This narrative stops at IV Antibiotics administration in the ER without any non-critical inpatient admission.
- `V0009`: This narrative ends with IV Antibiotics in the ER and does not advance to inpatient admission.
- `V0010`: This narrative involves ER assessment steps but does not result in an inpatient admission.
- `V0011`: This narrative ends with IV Antibiotics in the ER and does not contain any inpatient admission activities.
- `V0012`: This narrative concludes with IV Antibiotics inside the ER workflow without reaching inpatient admission.
- `V0013`: This narrative stops at Leucocytes testing during the ER stage and does not progress to inpatient admission.
- `V0017`: This narrative is confined to initial ER evaluations and does not feature inpatient admission.
- `V0019`: This narrative ends with IV Antibiotics in the ER and does not proceed to inpatient admission.
- `V0020`: This narrative terminates at CRP testing in the ER without advancing to inpatient admission.
- `V0025`: This narrative concludes with IV Antibiotics in the ER and lacks an inpatient admission step.
- `V0027`: The narrative stops at IV Antibiotics without any admission to an inpatient ward.
- `V0029`: The narrative ends at Leucocytes testing during ER workup without any inpatient admission.
- `V0031`: The case terminates at LacticAcid during the initial evaluation phase.
- `V0034`: The narrative concludes at IV Liquid administration within the emergency workflow.
- `V0036`: Terminates at CRP laboratory testing without reaching any ward admission.
- `V0038`: Ends at IV Antibiotics inside the emergency department timeline.
- `V0043`: Ends at LacticAcid testing without any admission step.
- `V0050`: Ends at CRP testing during early emergency assessment.
- `V0056`: The workflow ends at IV Antibiotics without involving an admission to a non-critical inpatient ward.
- `V0062`: Terminates at IV Antibiotics without any admission to a non-critical ward.
- `V0081`: The narrative ends at IV Liquid and does not include any admission to an inpatient ward.
- `V0088`: The narrative ends at IV Antibiotics without any admission event.
- `V0092`: The narrative terminates at LacticAcid without progressing to an admission.
- `V0125`: This narrative includes Admission IC (critical intensive care) prior to Admission NC, which deviates significantly from a purely non-critical admission pathway under this specific taxonomy.
- `V0127`: The narrative does not contain any admission to a non-critical inpatient ward, stopping at LacticAcid.
- `V0132`: The narrative terminates at IV Antibiotics without any non-critical admission.
- `V0133`: The narrative terminates at IV Antibiotics without any non-critical admission.
- `V0137`: The narrative terminates at LacticAcid without any non-critical admission.
- `V0145`: The narrative contains only intensive care and emergency diagnostics/treatments without Admission NC.
- `V0146`: The narrative terminates at Leucocytes without any non-critical admission.
- `V0148`: The narrative terminates at IV Antibiotics without any non-critical admission.
- `V0167`: The narrative includes Admission IC but lacks Admission NC, meaning it does not realize the non-critical admission category.
- `V0187`: The narrative lacks any 'Admission NC' activity, so it does not realize the admission_nc category.
- `V0197`: The narrative lacks any 'Admission NC' activity, so it does not realize the admission_nc category.
- `V0217`: The narrative does not include Admission NC; it terminates at IV Antibiotics without non-critical inpatient ward admission.
- `V0218`: The narrative features Admission IC instead of Admission NC, realizing intensive rather than non-critical care.
- `V0219`: The narrative does not include Admission NC and terminates prematurely during diagnostic testing.
- `V0232`: The narrative ends at IV Antibiotics without involving Admission NC, so it does not realize the admission category.
- `V0234`: The narrative terminates at Leucocytes and lacks an inpatient admission activity.
- `V0260`: The patient's journey ends at IV Antibiotics in the ER and does not involve admission to a non-critical inpatient ward.
- `V0287`: Does not reach an inpatient admission activity; terminates at CRP.
- `V0292`: Terminates at Leucocytes without proceeding to a non-critical ward admission.
- `V0302`: The narrative ends at ER Sepsis Triage and does not include any non-critical inpatient ward admission.
- `V0305`: The narrative terminates at IV Antibiotics and lacks any inpatient ward admission activity.
- `V0322`: The narrative ends at IV Antibiotics without incorporating any inpatient ward admission steps.
- `V0325`: The narrative stops at IV Antibiotics and contains no admission activity to a non-critical ward.
- `V0330`: The variant ends at IV Liquid without proceeding to a non-critical admission.
- `V0342`: The variant terminates at CRP without reaching a ward admission.
- `V0349`: The process terminates at ER Sepsis Triage without reaching inpatient admission.
- `V0365`: The narrative does not include Admission NC; it involves intensive care and lacks the non-critical ward admission.
- `V0378`: The narrative does not include any inpatient admission activity, ending at IV Antibiotics without non-critical ward admission.
- `V0379`: The narrative does not include any inpatient admission activity, ending at IV Antibiotics without non-critical ward admission.
- `V0407`: The patient is admitted to a critical care unit (Admission IC) rather than a non-critical ward, failing to realize the admission_nc category.
- `V0417`: The workflow terminates at ER Triage without any inpatient admission step.
- `V0422`: The patient is admitted to an intensive care unit (Admission IC) rather than a non-critical inpatient ward.
- `V0429`: The narrative ends at IV Antibiotics without involving Admission NC.
- `V0432`: The narrative contains Admission IC instead of Admission NC.
- `V0488`: The narrative ends at IV Liquid without reaching non-critical inpatient ward admission.
- `V0492`: The narrative terminates at IV Liquid before any inpatient admission step occurs.
- `V0495`: The workflow terminates at IV Antibiotics without inpatient ward admission.
- `V0507`: The narrative terminates at IV Antibiotics without reaching non-critical inpatient admission.
- `V0510`: The narrative ends at IV Antibiotics and lacks any inpatient admission step.
- `V0516`: The narrative terminates at Leucocytes and does not contain any admission step.
- `V0517`: The narrative terminates at ER Triage and lacks inpatient admission.
- `V0531`: The variant includes admissions to an intensive care unit (Admission IC) rather than solely non-critical inpatient wards, so it does not exclusively realize the non-critical admission category.
- `V0542`: The variant features an intensive care admission (Admission IC), making it inconsistent with the non-critical admission category definition.
- `V0543`: The narrative includes intensive care admission (Admission IC), which disqualifies it from the non-critical admission category.
- `V0549`: The narrative terminates at IV Liquid and does not include any inpatient ward admission (Admission NC).
- `V0575`: The narrative terminates early at Leucocytes and does not contain any admission to a non-critical inpatient ward (Admission NC).
- `V0580`: The narrative terminates at CRP and does not include an admission to a non-critical inpatient ward (Admission NC).
- `V0584`: The process terminates at IV Liquid without any non-critical inpatient ward admission.
- `V0585`: The process terminates at LacticAcid and lacks any inpatient ward admission step.
- `V0587`: Terminates at CRP without any inpatient ward admission step.
- `V0592`: Terminates at IV Antibiotics without involving a non-critical inpatient admission.
- `V0621`: The narrative contains 'Admission IC' instead of 'Admission NC', meaning it does not realize the non-critical admission category.
- `V0645`: The narrative lacks an Admission NC activity, terminating in LacticAcid without realizing the inpatient admission category.
- `V0654`: The narrative focuses on Admission IC rather than non-critical ward admission, so the category does not fit.
- `V0664`: The narrative terminates at IV Liquid and lacks admission to a non-critical inpatient ward.
- `V0676`: The narrative does not involve admission to a non-critical inpatient ward as it terminates at IV Antibiotics.
- `V0679`: The narrative concludes at IV Antibiotics and does not involve inpatient ward admission.
- `V0685`: The process stops at IV Antibiotics in the ER without reaching inpatient ward admission.
- `V0689`: The pathway terminates at IV Antibiotics without any inpatient admission step.
- `V0694`: The sequence stops at ER Sepsis Triage and does not contain any inpatient admission.
- `V0713`: The workflow terminates at IV Antibiotics without reaching a non-critical admission stage.
- `V0715`: The variant transitions to Admission IC rather than non-critical admission.
- `V0742`: The narrative ends at LacticAcid and does not include any non-critical ward admission steps.
- `V0750`: The narrative terminates at IV Antibiotics without involving any non-critical ward admissions.
- `V0759`: The narrative ends at IV Antibiotics without proceeding to an inpatient admission phase.
- `V0764`: The case terminates early at ER Sepsis Triage without reaching any ward admission.
- `V0772`: The narrative terminates at a CRP lab measurement before reaching discharge or release outcomes.
- `V0774`: The narrative stops at ER Sepsis Triage without an admission phase.
- `V0775`: The process terminates at a CRP check without any ward admission.
- `V0777`: The process stops at Leucocytes without advancing to a non-critical admission phase.
- `V0778`: The process ends at Leucocytes and lacks an admission to a non-critical ward.
- `V0791`: The process terminates at IV Antibiotics in the ER and does not progress to inpatient admission.
- `V0816`: The variant ends at IV Antibiotics without any admission activity, so it does not realize the admission_nc category.
- `V0820`: The variant terminates at LacticAcid without any inpatient admission activity, hence it does not realize admission_nc.
- `V0832`: The narrative ends at IV Antibiotics without reaching non-critical admission or discharge workflows.
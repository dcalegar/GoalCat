# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_axisadmission_rep3` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Non-Critical Ward Admission (`admission_nc`)

Represents admission of the patient to a non-critical inpatient ward (Admission NC). This pathway supports standard inpatient care following sepsis screening and initial workup and treatment.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=15 (Admission NC) from the OR decomposition of goal id=5. Supported by frequent and extreme variant samples such as V0008, V0551, and V0317 where patients are transitioned to non-critical care.

**Goal-model linkage:** 15 (Task): Admission NC

**Coverage:** macro 669/846 variants (79.1%) · micro 721/1050 cases (68.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 9.80, nearest other category `admission_ic` at mean distance 22.83

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.408, nearest other category `admission_ic` at mean distance 0.426

## Intensive Care Ward Admission (`admission_ic`)

Represents admission of the patient to an intensive care inpatient ward (Admission IC). This pathway is chosen for severe cases requiring intensive monitoring and treatment, impacting the goal softgoal 'Minimize time-to-treatment' with a negative contribution (-25) due to intensive transfer overhead.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=16 (Admission IC) from the OR decomposition of goal id=5. Supported by variant samples such as V0605 and V0317 which show direct realization of intensive care ward admission.

**Goal-model linkage:** 16 (Task): Admission IC

**Coverage:** macro 89/846 variants (10.5%) · micro 89/1050 cases (8.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 27.67, nearest other category `admission_nc` at mean distance 22.83

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.331, nearest other category `admission_nc` at mean distance 0.426

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0654` / `V0710` (category `admission_ic`): structural=177, profile=0.576
- `V0082` / `V0710` (category `admission_ic`): structural=176, profile=0.680
- `V0710` / `V0742` (category `admission_ic`): structural=176, profile=0.583
- `V0621` / `V0710` (category `admission_ic`): structural=175, profile=0.752
- `V0407` / `V0710` (category `admission_ic`): structural=174, profile=0.624
- `V0710` / `V0793` (category `admission_ic`): structural=174, profile=0.480
- `V0639` / `V0710` (category `admission_ic`): structural=173, profile=0.375
- `V0710` / `V0715` (category `admission_ic`): structural=173, profile=0.556
- `V0154` / `V0710` (category `admission_ic`): structural=172, profile=0.338
- `V0391` / `V0710` (category `admission_ic`): structural=172, profile=0.513

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0051` (`admission_nc`) / `V0391` (`admission_ic`): structural=2, profile=0.172
- `V0082` (`admission_ic`) / `V0156` (`admission_nc`): structural=2, profile=0.025
- `V0082` (`admission_ic`) / `V0400` (`admission_nc`): structural=2, profile=0.333
- `V0082` (`admission_ic`) / `V0451` (`admission_nc`): structural=2, profile=0.012
- `V0008` (`admission_nc`) / `V0082` (`admission_ic`): structural=3, profile=0.340
- `V0040` (`admission_nc`) / `V0082` (`admission_ic`): structural=3, profile=0.759
- `V0044` (`admission_nc`) / `V0793` (`admission_ic`): structural=3, profile=0.151
- `V0076` (`admission_nc`) / `V0621` (`admission_ic`): structural=3, profile=0.389
- `V0077` (`admission_nc`) / `V0407` (`admission_ic`): structural=3, profile=0.173
- `V0082` (`admission_ic`) / `V0110` (`admission_nc`): structural=3, profile=0.774

## Residual

88/846 variants (10.4%), 240/1050 cases (22.9%) unassigned.

- `V0001`: The narrative stops at ER Sepsis Triage and does not show any ward admission.
- `V0002`: The narrative ends with blood tests (CRP) in the ER and does not contain ward admission.
- `V0003`: The sequence ends with diagnostic tests (Leucocytes) without any ward admission activity.
- `V0004`: The trace covers initial ER workup and IV antibiotics but does not progress to ward admission.
- `V0005`: The case concludes in the ER with LacticAcid and lacks any inpatient ward admission.
- `V0006`: The narrative records emergency care and IV antibiotics administration, stopping before admission.
- `V0007`: The process terminates after IV antibiotics are given in the emergency setting without admission.
- `V0009`: Only emergency diagnostic and treatment steps are present, without an inpatient admission step.
- `V0010`: The trace concludes at ER Sepsis Triage and does not indicate ward admission.
- `V0011`: This sequence features ER steps and IV antibiotics treatment, but no subsequent ward admission.
- `V0012`: The trace ends with IV Antibiotics in the ER and does not reach any ward admission.
- `V0013`: The narrative finishes with diagnostic blood tests in the emergency department.
- `V0017`: The narrative consists purely of ER triage and initial diagnostics without ward admission.
- `V0019`: The trace details emergency workup and IV antibiotics, stopping before any admission.
- `V0020`: The narrative terminates after ER diagnostics and treatment without an inpatient admission.
- `V0025`: The trace captures emergency treatment and antibiotics, ending without ward admission.
- `V0027`: Emergency diagnostics and IV antibiotics are performed, but no ward admission is recorded.
- `V0029`: The trace stops at ER lab work (Leucocytes) without ward admission.
- `V0031`: Only emergency screening and initial treatment steps are included.
- `V0034`: The sequence terminates at IV Liquid administration within the emergency setting.
- `V0036`: The trace ends with emergency lab work (CRP) without any inpatient admission.
- `V0038`: Emergency diagnostics and IV antibiotics are administered, concluding without admission.
- `V0043`: The trace ends with ER diagnostic tests (LacticAcid) without ward admission.
- `V0050`: The trace finishes with emergency laboratory testing (CRP) and lacks ward admission.
- `V0056`: The narrative ends at IV Antibiotics without any ward admission activity, so neither admission category fits.
- `V0062`: The sequence terminates at IV Antibiotics with no admission step present.
- `V0081`: Terminates at IV Liquid with no ward admission activity present.
- `V0088`: Terminates at IV Antibiotics without any admission steps.
- `V0092`: Terminates at LacticAcid without any inpatient admission activity.
- `V0127`: The variant narrative does not include any ward admission activity, ending at LacticAcid.
- `V0132`: The variant narrative does not include any ward admission activity, ending at IV Antibiotics.
- `V0133`: The variant narrative does not include any ward admission activity, ending at IV Antibiotics.
- `V0137`: The variant narrative does not include any ward admission activity, ending at LacticAcid.
- `V0146`: The variant narrative does not include any ward admission activity, ending at Leucocytes.
- `V0148`: The variant narrative does not include any ward admission activity, ending at IV Antibiotics.
- `V0187`: The narrative terminates early at diagnostic and screening stages without reaching any ward admission activity.
- `V0197`: The narrative terminates early at diagnostic and screening stages without reaching any ward admission activity.
- `V0217`: The narrative does not contain any admission activity, ending at IV Antibiotics.
- `V0219`: The narrative does not contain any admission activity, ending at Leucocytes.
- `V0232`: The narrative does not contain any admission activity, ending at IV Antibiotics.
- `V0234`: The narrative does not contain any admission activity, ending at Leucocytes.
- `V0260`: The narrative ends at IV Antibiotics without any ward admission activity.
- `V0287`: The narrative terminates at CRP testing without reaching any ward admission.
- `V0292`: The narrative terminates at Leucocytes testing without reaching any ward admission.
- `V0302`: The process terminates at 'ER Sepsis Triage' and does not involve any ward admission.
- `V0305`: The process terminates at 'IV Antibiotics' without proceeding to any inpatient ward admission.
- `V0322`: The process terminates at 'IV Antibiotics' without proceeding to any inpatient ward admission.
- `V0325`: The process terminates at 'IV Antibiotics' without proceeding to any inpatient ward admission.
- `V0330`: The process terminates at 'IV Liquid' without proceeding to any inpatient ward admission.
- `V0342`: The process terminates at 'CRP' without proceeding to any inpatient ward admission.
- `V0349`: The process terminates at 'ER Sepsis Triage' and does not involve any ward admission.
- `V0378`: The narrative terminates at IV Antibiotics without reaching any ward admission step.
- `V0379`: The narrative terminates at IV Antibiotics without reaching any ward admission step.
- `V0417`: The narrative does not include any ward admission activity, ending instead at ER Triage.
- `V0429`: The narrative does not include any ward admission activity, ending at IV Antibiotics.
- `V0488`: The narrative ends at IV Liquid without any ward admission activity.
- `V0492`: The narrative ends at IV Liquid without any ward admission activity.
- `V0495`: The narrative ends at IV Antibiotics without any ward admission activity.
- `V0507`: The narrative ends with 'IV Antibiotics' and does not contain any ward admission steps.
- `V0510`: The narrative ends with 'IV Antibiotics' without proceeding to any ward admission.
- `V0516`: The narrative terminates at 'Leucocytes' and does not contain ward admission activities.
- `V0517`: The narrative terminates prematurely at 'ER Triage' without ward admission.
- `V0549`: The narrative terminates at 'IV Liquid' without ward admission activities.
- `V0575`: The narrative ends at Leucocytes without reaching an admission step, so neither category fits.
- `V0580`: The narrative terminates at CRP without any ward admission activity.
- `V0584`: The narrative terminates at IV Liquid without an admission activity.
- `V0585`: The narrative terminates at LacticAcid without an admission activity.
- `V0587`: The narrative terminates at CRP without reaching ward admission.
- `V0592`: The narrative terminates at IV Antibiotics without an admission activity.
- `V0645`: The narrative does not include any ward admission step, ending in LacticAcid.
- `V0664`: The process terminates at IV Liquid and does not reach any ward admission category.
- `V0676`: The process terminates at IV Antibiotics without proceeding to ward admission.
- `V0679`: The process terminates at IV Antibiotics without proceeding to ward admission.
- `V0685`: The process terminates at IV Antibiotics without proceeding to ward admission.
- `V0689`: The process terminates at IV Antibiotics without proceeding to ward admission.
- `V0694`: The process terminates at ER Sepsis Triage without proceeding to ward admission.
- `V0713`: The pathway terminates at IV Antibiotics without reaching any ward admission category.
- `V0750`: The pathway terminates at IV Antibiotics without reaching any ward admission category.
- `V0759`: The narrative terminates at IV Antibiotics without recording any ward admission event.
- `V0764`: The narrative terminates at ER Sepsis Triage without reaching any ward admission.
- `V0774`: The narrative terminates at ER Sepsis Triage without reaching any ward admission.
- `V0775`: The narrative terminates at CRP without reaching any ward admission.
- `V0777`: The narrative terminates at Leucocytes without reaching any ward admission.
- `V0778`: The narrative terminates at Leucocytes without reaching any ward admission.
- `V0791`: The narrative terminates at IV Antibiotics without reaching any ward admission.
- `V0816`: The process ends at IV Antibiotics without reaching any ward admission stage.
- `V0820`: The process terminates at LacticAcid without any ward admission activity.
- `V0832`: The process ends at IV Antibiotics without an admission step.
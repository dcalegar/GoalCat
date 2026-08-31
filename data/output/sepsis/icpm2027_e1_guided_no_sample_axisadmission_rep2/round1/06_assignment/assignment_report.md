# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_no_sample_axisadmission_rep2` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Normal Care Admission (`admission_nc`)

Patient is admitted to a normal care inpatient ward (Admission NC), advancing the standard treatment pathway without intensive care requirements.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative Admission NC (id=15) under the OR-decomposition of goal id=5.

**Goal-model linkage:** 15 (Task): Admission NC

**Coverage:** macro 680/846 variants (80.4%) · micro 732/1050 cases (69.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 10.90, nearest other category `admission_ic` at mean distance 20.21

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.408, nearest other category `admission_ic` at mean distance 0.427

## Intensive Care Admission (`admission_ic`)

Patient is admitted to an intensive care inpatient ward (Admission IC). This path involves intensive monitoring but carries a negative contribution (-25) to the softgoal Minimize time-to-treatment.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative Admission IC (id=16) under the OR-decomposition of goal id=5.

**Goal-model linkage:** 16 (Task): Admission IC

**Coverage:** macro 78/846 variants (9.2%) · micro 78/1050 cases (7.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 23.28, nearest other category `admission_nc` at mean distance 20.21

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.330, nearest other category `admission_nc` at mean distance 0.427

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0654` / `V0710` (category `admission_ic`): structural=177, profile=0.576
- `V0082` / `V0710` (category `admission_ic`): structural=176, profile=0.680
- `V0710` / `V0742` (category `admission_ic`): structural=176, profile=0.583
- `V0621` / `V0710` (category `admission_ic`): structural=175, profile=0.752
- `V0141` / `V0710` (category `admission_ic`): structural=174, profile=0.418
- `V0407` / `V0710` (category `admission_ic`): structural=174, profile=0.624
- `V0710` / `V0793` (category `admission_ic`): structural=174, profile=0.480
- `V0068` / `V0710` (category `admission_ic`): structural=173, profile=0.509
- `V0639` / `V0710` (category `admission_ic`): structural=173, profile=0.375
- `V0710` / `V0715` (category `admission_ic`): structural=173, profile=0.556

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

- `V0001`: This narrative ends at ER Sepsis Triage and does not involve admission to a normal care or intensive care inpatient ward.
- `V0002`: The narrative concludes after blood tests (CRP) and does not contain any inpatient admission activity.
- `V0003`: The narrative finishes at Leucocytes and lacks any ward admission step.
- `V0004`: The patient receives IV Antibiotics in the emergency phase but is not admitted to a ward.
- `V0005`: The process sequence terminates at LacticAcid without any inpatient admission.
- `V0006`: Involves ER care and IV Antibiotics administration, but no inpatient admission is recorded.
- `V0007`: Contains emergency diagnostic and treatment steps without proceeding to inpatient ward admission.
- `V0009`: Stops at IV Antibiotics following emergency procedures; no admission activity is present.
- `V0010`: Consists only of emergency registration, triage, and lab work without inpatient admission.
- `V0011`: Completes the emergency treatment path with IV Antibiotics but does not lead to ward admission.
- `V0012`: Represents emergency diagnostics and IV therapy without any subsequent ward admission.
- `V0013`: Terminates at Leucocytes laboratory testing without inpatient admission.
- `V0017`: Stops at ER Sepsis Triage and lab testing without inpatient admission.
- `V0019`: Covers emergency triage, diagnostics, and IV antibiotics without ward admission.
- `V0020`: Ends at CRP after emergency diagnostics and treatment, with no inpatient admission.
- `V0025`: Finishes with IV Antibiotics after emergency care; no ward admission is recorded.
- `V0027`: Emergency pathway ending in IV Antibiotics without inpatient ward admission.
- `V0029`: Terminates at Leucocytes after emergency procedures without ward admission.
- `V0031`: Emergency care pathway ending with LacticAcid testing, lacking inpatient admission.
- `V0034`: Emergency phase pathway ending in IV Liquid administration without ward admission.
- `V0036`: Emergency diagnostic and treatment sequence ending at CRP without inpatient admission.
- `V0038`: Emergency management sequence ending in IV Antibiotics without inpatient admission.
- `V0043`: Emergency lab testing sequence ending at LacticAcid without inpatient ward admission.
- `V0050`: Emergency pathway ending with CRP blood testing without any inpatient admission.
- `V0056`: The narrative does not include any inpatient ward admission activity.
- `V0062`: The narrative does not include any inpatient ward admission activity.
- `V0081`: The narrative does not include any inpatient ward admission activity.
- `V0088`: The narrative does not include any inpatient ward admission activity.
- `V0092`: The narrative does not include any inpatient ward admission activity.
- `V0127`: The narrative ends at 'LacticAcid' and does not contain any ward admission steps.
- `V0132`: The process terminates at 'IV Antibiotics' without any ward admission activity.
- `V0133`: The narrative stops at 'IV Antibiotics' without entering a ward admission category.
- `V0137`: The process terminates at 'LacticAcid' without reaching an inpatient admission category.
- `V0146`: The process ends at 'Leucocytes' without any ward admission activity.
- `V0148`: The narrative finishes at 'IV Antibiotics' without proceeding to a ward admission.
- `V0187`: The narrative stops at diagnostic steps and does not reach any inpatient ward admission category.
- `V0197`: The narrative does not include any inpatient ward admission category.
- `V0217`: The narrative does not contain any admission step (neither normal care nor intensive care), ending at IV Antibiotics.
- `V0219`: The narrative does not contain any admission step, ending prematurely at Leucocytes.
- `V0232`: The narrative does not contain any admission step, ending at IV Antibiotics.
- `V0234`: The narrative does not contain any admission step, ending at Leucocytes.
- `V0260`: The narrative terminates at IV Antibiotics without reaching any inpatient admission category.
- `V0287`: The narrative terminates at CRP without reaching any inpatient admission category.
- `V0292`: The narrative terminates at Leucocytes without reaching any inpatient admission category.
- `V0302`: The narrative stops at ER Sepsis Triage and does not contain any inpatient ward admission activity.
- `V0305`: The narrative terminates at IV Antibiotics without reaching an inpatient ward admission.
- `V0322`: The narrative terminates at IV Antibiotics without reaching an inpatient ward admission.
- `V0325`: The narrative terminates at IV Antibiotics without reaching an inpatient ward admission.
- `V0330`: The narrative terminates at IV Liquid without reaching an inpatient ward admission.
- `V0342`: The narrative terminates at CRP without reaching an inpatient ward admission.
- `V0349`: The narrative terminates at ER Sepsis Triage without reaching an inpatient ward admission.
- `V0378`: The variant ends at 'IV Antibiotics' without proceeding to an inpatient admission category.
- `V0379`: The variant ends at 'IV Antibiotics' without proceeding to an inpatient admission category.
- `V0417`: The narrative does not contain any admission activity, hence it falls into the residual category.
- `V0429`: The narrative does not contain any admission activity, hence it falls into the residual category.
- `V0488`: The narrative does not include any inpatient admission activity, hence it is part of the residual.
- `V0492`: The narrative does not include any inpatient admission activity, hence it is part of the residual.
- `V0495`: The narrative does not include any inpatient admission activity, hence it is part of the residual.
- `V0507`: The narrative stops at 'IV Antibiotics' without any admission step.
- `V0510`: The process terminates at 'IV Antibiotics' without proceeding to any inpatient admission.
- `V0516`: The narrative terminates at 'Leucocytes' without any admission activity.
- `V0517`: The narrative terminates at 'ER Triage' without any admission activity.
- `V0549`: The narrative terminates at 'IV Liquid' without any inpatient admission activity.
- `V0575`: Neither Admission NC nor Admission IC is present in the sequence.
- `V0580`: The narrative terminates at CRP and does not include an admission activity.
- `V0584`: The narrative terminates at IV Liquid and lacks an admission step.
- `V0585`: The narrative terminates at LacticAcid without any ward admission.
- `V0587`: The narrative terminates at CRP without any ward admission.
- `V0592`: The narrative terminates at IV Antibiotics without any admission activity.
- `V0645`: The narrative terminates at LacticAcid and does not contain any inpatient ward admission activity (Admission NC or Admission IC).
- `V0664`: The narrative ends at IV Liquid and does not reach any inpatient admission category.
- `V0676`: The narrative ends at IV Antibiotics without reaching any inpatient admission.
- `V0679`: The narrative ends at IV Antibiotics without reaching any inpatient admission.
- `V0685`: The narrative ends at IV Antibiotics without reaching any inpatient admission.
- `V0689`: The narrative ends at IV Antibiotics without reaching any inpatient admission.
- `V0694`: The narrative terminates at ER Sepsis Triage and does not reach admission.
- `V0713`: The narrative ends at IV Antibiotics without any ward admission activity, so neither admission category fits.
- `V0750`: The narrative ends at IV Antibiotics without any ward admission activity, so neither admission category fits.
- `V0759`: The narrative ends with IV Antibiotics and does not include any inpatient ward admission activity.
- `V0764`: The narrative ends at ER Sepsis Triage and does not include any inpatient ward admission activity.
- `V0774`: The narrative ends at ER Sepsis Triage and does not include any inpatient ward admission activity.
- `V0775`: The narrative ends at CRP and does not include any inpatient ward admission activity.
- `V0777`: The narrative ends at Leucocytes and does not include any inpatient ward admission activity.
- `V0778`: The narrative ends at Leucocytes and does not include any inpatient ward admission activity.
- `V0791`: The narrative ends at IV Antibiotics and does not include any inpatient ward admission activity.
- `V0816`: The narrative terminates at IV Antibiotics without any ward admission activity, so neither category fits.
- `V0820`: The pathway terminates at LacticAcid without any ward admission, fitting neither category.
- `V0832`: The pathway ends at IV Antibiotics without any admission activity, fitting neither category.
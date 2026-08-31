# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_no_sample_axisadmission_rep1` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Admission to Normal Care (`admission_nc`)

Patient is admitted to a normal care inpatient ward (Admission NC). Advances the goal of inpatient care disposition while managing patient flow, assessed against indicators such as time to treatment and post-discharge outcomes.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared OR alternative Admission NC (id=15).

**Goal-model linkage:** 15 (Task): Admission NC

**Coverage:** macro 688/846 variants (81.3%) · micro 740/1050 cases (70.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.39, nearest other category `admission_ic` at mean distance 19.01

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.407, nearest other category `admission_ic` at mean distance 0.429

## Admission to Intensive Care (`admission_ic`)

Patient is admitted to an intensive care inpatient ward (Admission IC). This alternative advances treatment speed but carries a negative contribution to minimizing time-to-treatment softgoals.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared OR alternative Admission IC (id=16).

**Goal-model linkage:** 16 (Task): Admission IC

**Coverage:** macro 70/846 variants (8.3%) · micro 70/1050 cases (6.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 20.62, nearest other category `admission_nc` at mean distance 19.01

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.345, nearest other category `admission_nc` at mean distance 0.429

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

- `V0001`: The narrative ends at ER Sepsis Triage and does not include any inpatient admission activity.
- `V0002`: The narrative stops at diagnostic blood tests (CRP) and does not involve inpatient admission.
- `V0003`: The narrative only performs diagnostic triage and blood work without reaching an admission step.
- `V0004`: The narrative includes initial treatment in the ER but does not proceed to normal or intensive care admission.
- `V0005`: The narrative represents emergency diagnostics only without an inpatient admission.
- `V0006`: The variant covers ER diagnostics and antibiotics but does not show an inpatient admission event.
- `V0007`: The variant ends with IV Antibiotics in the emergency context without proceeding to admission.
- `V0009`: The patient receives ER care and IV antibiotics but is not admitted to an inpatient ward.
- `V0010`: The sequence is restricted to ER-level diagnostic and triage actions.
- `V0011`: The workflow finishes with IV antibiotics in the emergency setting without an admission record.
- `V0012`: The narrative contains ER diagnostics and treatment without an inpatient admission step.
- `V0013`: The variant consists of ER triage and lab tests only.
- `V0017`: The narrative is limited to ER evaluation and triage.
- `V0019`: The process variant handles ER stabilization and treatment without an inpatient ward admission.
- `V0020`: The narrative concludes with laboratory tests in the emergency department.
- `V0025`: The patient is treated in the ER without proceeding to an inpatient ward admission.
- `V0027`: The patient receives emergency care and treatment without an admission event.
- `V0029`: The narrative stays within emergency diagnostics and treatment.
- `V0031`: The narrative represents emergency department evaluation and lab work only.
- `V0034`: The narrative ends in the ER with IV liquid administration and lacks an admission event.
- `V0036`: The narrative is confined to emergency diagnostics and lab work.
- `V0038`: The workflow finishes with IV antibiotics in the ER without inpatient admission.
- `V0043`: The process variant is limited to emergency triage and blood tests.
- `V0050`: The narrative consists entirely of emergency department evaluation and lab testing.
- `V0056`: The narrative ends with IV Antibiotics and does not reach any inpatient admission stage.
- `V0062`: The narrative ends with IV Antibiotics and does not reach any inpatient admission stage.
- `V0081`: The narrative ends with IV Liquid and does not reach any inpatient admission stage.
- `V0088`: The narrative ends with IV Antibiotics and does not reach any inpatient admission stage.
- `V0092`: The narrative ends with LacticAcid and does not reach any inpatient admission stage.
- `V0127`: The narrative terminates at LacticAcid without any inpatient ward admission event.
- `V0132`: The narrative terminates at IV Antibiotics without any inpatient ward admission event.
- `V0133`: The narrative terminates at IV Antibiotics without any inpatient ward admission event.
- `V0137`: The narrative terminates at LacticAcid without any inpatient ward admission event.
- `V0146`: The narrative terminates at Leucocytes without any inpatient ward admission event.
- `V0148`: The narrative terminates at IV Antibiotics without any inpatient ward admission event.
- `V0187`: The narrative does not contain any admission activity, ending at CRP.
- `V0197`: The narrative does not contain any admission activity, ending at Leucocytes.
- `V0217`: The narrative stops at IV Antibiotics and does not reach any inpatient admission category.
- `V0219`: The narrative ends with Leucocytes and does not reach any inpatient admission category.
- `V0232`: The narrative stops at IV Antibiotics and does not reach any inpatient admission category.
- `V0234`: The narrative terminates at Leucocytes without any inpatient admission.
- `V0260`: The narrative stops at IV Antibiotics and does not contain any ward admission activities.
- `V0287`: The narrative stops at CRP and does not contain any ward admission activities.
- `V0292`: The narrative stops at Leucocytes and does not contain any ward admission activities.
- `V0302`: The narrative ends at 'ER Sepsis Triage' and does not involve any inpatient ward admission.
- `V0305`: The variant terminates at 'IV Antibiotics' without proceeding to inpatient ward admission.
- `V0322`: The variant ends at 'IV Antibiotics' without proceeding to inpatient ward admission.
- `V0325`: The variant terminates at 'IV Antibiotics' without ward admission.
- `V0330`: The variant ends at 'IV Liquid' without ward admission.
- `V0342`: The variant ends at 'CRP' without ward admission.
- `V0349`: The variant terminates at 'ER Sepsis Triage' without ward admission.
- `V0378`: The narrative ends at 'IV Antibiotics' and does not contain any admission activity.
- `V0379`: The narrative ends at 'IV Antibiotics' and does not contain any admission activity.
- `V0417`: The narrative ends at 'ER Triage' and contains no admission activity, falling into the residual.
- `V0429`: The narrative ends at 'IV Antibiotics' and contains no admission activity, falling into the residual.
- `V0488`: The narrative ends at IV Liquid without any inpatient admission step, so neither admission category fits.
- `V0492`: The narrative ends at IV Liquid without any inpatient admission step, so neither admission category fits.
- `V0495`: The narrative ends at IV Antibiotics without any inpatient admission step, so neither admission category fits.
- `V0507`: The variant ends at IV Antibiotics without involving any ward admission step.
- `V0510`: The process terminates at IV Antibiotics without any admission activity.
- `V0516`: The narrative ends at Leucocytes without reaching any admission stage.
- `V0517`: The narrative stops at ER Triage without progressing to admission.
- `V0549`: The narrative terminates at IV Liquid without reaching any ward admission activity.
- `V0575`: The narrative terminates at Leucocytes without any ward admission activity, thus realizing neither category.
- `V0580`: The narrative terminates at CRP without reaching any ward admission activity.
- `V0584`: The narrative ends at IV Liquid without an inpatient admission activity.
- `V0585`: The narrative terminates at LacticAcid without any ward admission step.
- `V0587`: The narrative ends at CRP without reaching an admission goal.
- `V0592`: The narrative terminates at IV Antibiotics without an admission activity.
- `V0645`: The narrative lacks any admission activity (Admission NC or Admission IC), resulting in a residual classification.
- `V0664`: The narrative ends at IV Liquid and does not reach any inpatient admission category.
- `V0676`: The narrative ends at IV Antibiotics without reaching any inpatient admission category.
- `V0679`: The narrative ends at IV Antibiotics without reaching any inpatient admission category.
- `V0685`: The narrative ends at IV Antibiotics without reaching any inpatient admission category.
- `V0689`: The narrative ends at IV Antibiotics without reaching any inpatient admission category.
- `V0694`: The narrative ends at ER Sepsis Triage without reaching any inpatient admission category.
- `V0713`: The variant ends with IV Antibiotics and does not reach any inpatient admission stage.
- `V0750`: The variant stops at IV Antibiotics without reaching any inpatient admission category.
- `V0759`: The narrative does not contain any admission activity to normal or intensive care.
- `V0764`: The narrative does not contain any admission activity to normal or intensive care.
- `V0774`: The narrative does not contain any admission activity to normal or intensive care.
- `V0775`: The narrative does not contain any admission activity to normal or intensive care.
- `V0777`: The narrative does not contain any admission activity to normal or intensive care.
- `V0778`: The narrative does not contain any admission activity to normal or intensive care.
- `V0791`: The narrative does not contain any admission activity to normal or intensive care.
- `V0816`: The narrative terminates at IV Antibiotics without any ward admission activity.
- `V0820`: The process ends at LacticAcid without any inpatient admission steps.
- `V0832`: Terminates at IV Antibiotics without any admission activities.
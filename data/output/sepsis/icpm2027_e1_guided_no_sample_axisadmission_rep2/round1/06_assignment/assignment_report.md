# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_no_sample_axisadmission_rep2` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Admission to Normal Care (NC) (`admission_nc`)

Patient is admitted to a normal care inpatient ward (Admission NC), advancing treatment pathways while balancing resource utilization.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=15 under the OR decomposition of goal id=5, representing standard inpatient ward admission.

**Goal-model linkage:** 15 (Task): Admission NC

**Coverage:** macro 661/846 variants (78.1%) · micro 713/1050 cases (67.9%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 10.11, nearest other category `admission_ic` at mean distance 20.92

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.407, nearest other category `admission_ic` at mean distance 0.429

## Admission to Intensive Care (IC) (`admission_ic`)

Patient is admitted to the intensive care unit (Admission IC), advancing clinical stabilization while carrying a SomeNegative contribution to minimizing time-to-treatment due to specialized coordination overhead.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=16 under the OR decomposition of goal id=5, representing intensive care ward admission.

**Goal-model linkage:** 16 (Task): Admission IC

**Coverage:** macro 97/846 variants (11.5%) · micro 97/1050 cases (9.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 24.09, nearest other category `admission_nc` at mean distance 20.92

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.329, nearest other category `admission_nc` at mean distance 0.429

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

- `V0001`: The variant ends at ER Sepsis Triage and does not involve any admission to a normal care or intensive care ward.
- `V0002`: The pathway ends with lab tests (CRP) in the emergency room without proceeding to inpatient admission.
- `V0003`: The process concludes at Leucocytes testing in the ER, with no ward admission occurring.
- `V0004`: The trace stops at IV Antibiotics administration in the emergency department, lacking any inpatient admission activity.
- `V0005`: The variant finishes after completing initial diagnostics (LacticAcid) in the ER without being admitted.
- `V0006`: The treatment is completed with IV Antibiotics in the ER without progressing to hospital admission.
- `V0007`: The patient receives emergency care up to IV Antibiotics administration, with no subsequent ward admission.
- `V0009`: The sequence terminates following IV Antibiotics in the ER, without any hospital admission step.
- `V0010`: The case consists purely of emergency room assessment and lab work, without any admission category realized.
- `V0011`: The patient's journey ends after emergency IV Antibiotics treatment without an inpatient admission.
- `V0012`: The activities are confined to emergency diagnostics and treatment, with no subsequent ward admission.
- `V0013`: The variant finishes at Leucocytes testing in the ER, lacking any admission event.
- `V0017`: The variant ends at ER Sepsis Triage and does not involve any ward admission.
- `V0019`: The patient is treated with IV Antibiotics within the emergency setting, with no inpatient admission recorded.
- `V0020`: The trace concludes at CRP testing in the ER without proceeding to an inpatient ward.
- `V0025`: The narrative stops at IV Antibiotics in the ER without any inpatient ward admission event.
- `V0027`: The narrative ends with IV Antibiotics and does not contain any admission activity to normal or intensive care.
- `V0029`: The narrative terminates at Leucocytes and does not contain an admission step.
- `V0031`: The narrative terminates at LacticAcid without any inpatient ward admission.
- `V0034`: The narrative ends at IV Liquid and lacks any admission activities.
- `V0036`: The narrative terminates at CRP and lacks any admission activities.
- `V0038`: The narrative ends at IV Antibiotics without an admission step.
- `V0043`: The narrative terminates at LacticAcid and contains no admission activities.
- `V0050`: The narrative ends at CRP and lacks any admission activities.
- `V0056`: The narrative ends at IV Antibiotics without any admission activity, hence no category fits.
- `V0062`: The process terminates at IV Antibiotics without involving any ward admission step.
- `V0081`: The narrative ends at IV Liquid and does not contain any admission activity.
- `V0088`: The narrative ends at IV Antibiotics and does not contain any admission activity.
- `V0092`: The narrative ends at LacticAcid and does not contain any admission activity.
- `V0127`: The narrative ends at LacticAcid and does not contain any admission activity.
- `V0132`: The narrative terminates at 'IV Antibiotics' without any ward admission activity.
- `V0133`: The narrative terminates at 'IV Antibiotics' without any ward admission activity.
- `V0137`: The narrative terminates at 'LacticAcid' without any ward admission activity.
- `V0146`: The narrative terminates at 'Leucocytes' without any ward admission activity.
- `V0148`: The narrative terminates at 'IV Antibiotics' without any ward admission activity.
- `V0187`: The narrative ends at CRP without any admission activity, hence it does not realize either admission category.
- `V0197`: The narrative ends at Leucocytes without an admission activity, hence it does not realize either admission category.
- `V0217`: The narrative ends at IV Antibiotics without any admission activity, hence it does not realize either admission category.
- `V0219`: The narrative terminates at Leucocytes without an admission step, hence no category applies.
- `V0232`: The narrative ends at IV Antibiotics and does not contain any admission activity to normal care or intensive care.
- `V0234`: The narrative terminates at Leucocytes and lacks any admission events.
- `V0260`: The narrative ends at IV Antibiotics without any inpatient ward or ICU admission.
- `V0287`: The narrative does not contain any admission activity, ending at CRP instead.
- `V0292`: The narrative terminates early at Leucocytes without containing any admission activity.
- `V0302`: The narrative ends at ER Sepsis Triage and does not contain any inpatient admission activity.
- `V0305`: The narrative terminates at IV Antibiotics in the ER phase without subsequent inpatient admission.
- `V0322`: The narrative ends at IV Antibiotics without any ward or ICU admission.
- `V0325`: The narrative terminates at IV Antibiotics without involving any inpatient admission category.
- `V0330`: The narrative ends at IV Liquid without any inpatient ward admission event.
- `V0342`: The narrative terminates at CRP without reaching any ward admission event.
- `V0349`: The narrative terminates at ER Sepsis Triage without reaching any ward admission.
- `V0378`: The narrative ends at 'IV Antibiotics' without any admission step, so neither normal care nor intensive care admission is realized.
- `V0379`: The narrative ends at 'IV Antibiotics' without an admission activity, thus not realizing either category.
- `V0417`: The narrative ends at 'ER Triage' and lacks any admission activity, hence it falls into the residual category.
- `V0429`: The narrative ends with 'IV Antibiotics' and does not contain any admission activity.
- `V0488`: The narrative ends at IV Liquid without any admission activity, hence it belongs to the residual.
- `V0492`: The narrative ends at IV Liquid without any admission activity, hence it belongs to the residual.
- `V0495`: The narrative ends at IV Antibiotics without any admission activity, hence it belongs to the residual.
- `V0507`: The narrative terminates at 'IV Antibiotics' without proceeding to any ward admission, leaving it outside the target categories.
- `V0510`: The narrative ends at 'IV Antibiotics' without showing an inpatient admission event.
- `V0516`: The pathway ends at 'Leucocytes' and does not involve any hospital admission activity.
- `V0517`: The pathway terminates early at 'ER Triage' without proceeding to treatment or admission.
- `V0549`: The narrative ends at IV Liquid and does not include an inpatient admission activity, leaving it in the residual.
- `V0575`: The narrative ends before any inpatient admission (NC or IC) occurs, so neither category fits.
- `V0580`: The narrative ends at CRP without any inpatient admission, so neither category is realized.
- `V0584`: The narrative ends at IV Liquid without any inpatient admission, so neither category is realized.
- `V0585`: The narrative ends at LacticAcid without any inpatient admission, so neither category is realized.
- `V0587`: The narrative ends at CRP without any inpatient admission, so neither category is realized.
- `V0592`: The narrative ends at IV Antibiotics without any inpatient admission, so neither category is realized.
- `V0645`: The narrative lacks any admission event, thus neither category is realized.
- `V0664`: The variant ends at IV Liquid without reaching any inpatient admission category.
- `V0676`: The narrative stops at IV Antibiotics without involving any hospital admission event.
- `V0679`: The patient receives IV Antibiotics but is not admitted to a hospital ward.
- `V0685`: The narrative ends with IV Antibiotics and lacks any admission event.
- `V0689`: The narrative stops at IV Antibiotics without an admission event.
- `V0694`: The narrative terminates at ER Sepsis Triage and does not proceed to admission.
- `V0713`: The narrative ends at 'IV Antibiotics' without any inpatient admission activity, hence neither admission category fits.
- `V0750`: The narrative ends with IV Antibiotics and does not contain any admission activity to normal or intensive care.
- `V0759`: The narrative terminates at IV Antibiotics without any admission activity, hence neither admission category fits.
- `V0764`: The narrative terminates at ER Sepsis Triage without reaching any ward admission.
- `V0774`: The narrative terminates at ER Sepsis Triage without any admission activity.
- `V0775`: The narrative terminates at CRP without reaching any admission activity.
- `V0777`: The narrative ends at Leucocytes without involving admission to normal or intensive care.
- `V0778`: The narrative terminates at Leucocytes and does not contain any admission activity.
- `V0791`: The sequence ends at IV Antibiotics and does not reach an admission step.
- `V0816`: The narrative does not contain any admission activity, only ER processes and IV Antibiotics.
- `V0820`: The narrative terminates at LacticAcid and does not contain any admission activity.
- `V0832`: The narrative ends at IV Antibiotics without any admission activity to normal or intensive care, so neither category fits.
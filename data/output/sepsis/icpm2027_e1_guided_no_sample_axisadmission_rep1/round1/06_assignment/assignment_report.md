# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_no_sample_axisadmission_rep1` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Admission to Normal Care (NC) (`admission_nc`)

Patient is admitted to a normal care inpatient ward (Admission NC), advancing the patient toward disposition while balancing ward capacity and care needs. Judged against post-discharge indicators and timeliness.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared OR alternative id=15 (Admission NC). It represents standard inpatient admission without intensive care routing.

**Goal-model linkage:** 15 (Task): Admission NC

**Coverage:** macro 655/846 variants (77.4%) · micro 707/1050 cases (67.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 9.41, nearest other category `admission_ic` at mean distance 22.30

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.407, nearest other category `admission_ic` at mean distance 0.429

## Admission to Intensive Care (IC) (`admission_ic`)

Patient is admitted to an intensive care inpatient ward (Admission IC). This option impacts the Minimize time-to-treatment softgoal via a SomeNegative (-25) contribution due to resource intensity, and is measured against treatment windows and outcomes.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared OR alternative id=16 (Admission IC). Represents high-acuity ward placement for severe sepsis presentations.

**Goal-model linkage:** 16 (Task): Admission IC

**Coverage:** macro 103/846 variants (12.2%) · micro 103/1050 cases (9.8%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 26.47, nearest other category `admission_nc` at mean distance 22.30

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.331, nearest other category `admission_nc` at mean distance 0.429

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

- `V0001`: The narrative ends at ER Sepsis Triage and does not involve any patient admission to a normal care or intensive care ward.
- `V0002`: The process concludes with lab tests (CRP) and contains no admission activity.
- `V0003`: The process concludes with lab tests (Leucocytes) and does not involve an inpatient admission.
- `V0004`: The narrative ends with the administration of IV Antibiotics in the emergency phase without proceeding to ward admission.
- `V0005`: The sequence stops at LacticAcid testing without any admission to an inpatient ward.
- `V0006`: The treatment concludes with IV Antibiotics and lacks any inpatient ward admission step.
- `V0007`: The narrative terminates after IV Antibiotics treatment without an admission event.
- `V0009`: The case sequence finishes upon delivering IV Antibiotics and does not reach an admission milestone.
- `V0010`: The workflow stops at ER Sepsis Triage and includes no admission events.
- `V0011`: The variant ends with IV Antibiotics administration and does not include ward admission.
- `V0012`: The process terminates after IV Antibiotics without advancing to an inpatient ward.
- `V0013`: The sequence ends with Leucocytes testing and contains no admission process.
- `V0017`: The variant concludes at ER Sepsis Triage without any subsequent ward admission.
- `V0019`: The narrative terminates after IV Antibiotics and does not involve an inpatient admission.
- `V0020`: The process ends with CRP testing and lacks any admission milestone.
- `V0025`: The variant ends with IV Antibiotics administration and does not progress to an inpatient admission.
- `V0027`: The narrative ends with 'IV Antibiotics' and does not contain any admission activity to normal care or intensive care.
- `V0029`: The variant terminates at 'Leucocytes' without including any ward admission activities.
- `V0031`: The variant ends at 'LacticAcid' and does not include an inpatient ward admission.
- `V0034`: The variant terminates at 'IV Liquid' and contains no admission actions.
- `V0036`: The variant ends at 'CRP' without any inpatient admission steps.
- `V0038`: The variant ends at 'IV Antibiotics' without proceeding to inpatient admission.
- `V0043`: The variant terminates at 'LacticAcid' without including any ward admissions.
- `V0050`: The variant ends at 'CRP' and does not involve any ward admission.
- `V0056`: The narrative ends at 'IV Antibiotics' without any inpatient ward admission activity.
- `V0062`: The narrative ends at 'IV Antibiotics' without any inpatient ward admission activity.
- `V0081`: The narrative terminates at 'IV Liquid' without any inpatient ward admission activity.
- `V0088`: The narrative terminates at 'IV Antibiotics' without any inpatient ward admission activity.
- `V0092`: The narrative terminates at 'LacticAcid' without any inpatient ward admission activity.
- `V0127`: The variant narrative ends at LacticAcid and does not contain any admission to an inpatient ward.
- `V0132`: The variant narrative ends at IV Antibiotics without involving any ward admission.
- `V0133`: The variant narrative terminates at IV Antibiotics and contains no inpatient ward admissions.
- `V0137`: The variant narrative concludes at LacticAcid with no ward admission activities.
- `V0146`: The variant narrative ends at Leucocytes and lacks any inpatient ward admission steps.
- `V0148`: The variant narrative ends at IV Antibiotics without any admission activities.
- `V0187`: The narrative stops at CRP and does not feature any inpatient ward admission activity.
- `V0197`: The narrative lacks any inpatient ward admission activity.
- `V0217`: The narrative ends at IV Antibiotics without any inpatient ward admission activity.
- `V0219`: The narrative terminates early at Leucocytes without reaching any ward admission.
- `V0232`: The variant terminates at IV Antibiotics without involving any ward admission activities.
- `V0234`: The variant terminates at Leucocytes testing without reaching any ward admission.
- `V0260`: The narrative ends at IV Antibiotics without any inpatient ward admission activity.
- `V0287`: The variant terminates at CRP without reaching any admission step, thus it does not realize either admission category.
- `V0292`: The variant terminates at Leucocytes without reaching any admission step, thus it does not realize either admission category.
- `V0302`: The narrative ends at ER Sepsis Triage and does not contain any inpatient ward admission activities.
- `V0305`: The narrative ends at IV Antibiotics without involving any ward admission.
- `V0322`: The narrative ends at IV Antibiotics without involving any ward admission.
- `V0325`: The narrative ends at IV Antibiotics without involving any ward admission.
- `V0330`: The narrative terminates at IV Liquid without reaching any inpatient admission category.
- `V0342`: The narrative terminates at CRP without reaching any inpatient admission category.
- `V0349`: The narrative terminates at ER Sepsis Triage without reaching any inpatient admission category.
- `V0378`: The narrative ends with 'IV Antibiotics' and does not contain any admission activities.
- `V0379`: The narrative ends with 'IV Antibiotics' and lacks any admission activities.
- `V0417`: The narrative ends in 'ER Triage' without any inpatient admission activity, hence it does not realize either admission category.
- `V0429`: The narrative ends with IV Antibiotics and lacks any inpatient ward admission activity, hence no category fits.
- `V0488`: The narrative ends with IV Liquid and lacks any ward admission activities (NC or IC), so it fits neither category.
- `V0492`: The narrative ends with IV Liquid and does not contain ward admission activities, so it fits neither category.
- `V0495`: The narrative ends with IV Antibiotics and lacks any ward admission activities, so it fits neither category.
- `V0507`: The narrative ends with 'IV Antibiotics' and does not contain any admission activity, hence it does not fit either category.
- `V0510`: The narrative terminates at 'IV Antibiotics' without proceeding to any inpatient admission, so no category is realized.
- `V0516`: The narrative terminates at 'Leucocytes' and lacks an admission activity, making it part of the residual.
- `V0517`: The sequence stops at 'ER Triage' without any admission step, so it does not realize either taxonomy category.
- `V0549`: The process terminates at IV Liquid without reaching any inpatient admission category.
- `V0575`: The narrative ends with laboratory and assessment steps without containing any inpatient ward admission (NC or IC).
- `V0580`: The narrative ends at CRP testing and does not contain any inpatient admission steps.
- `V0584`: The narrative stops at IV Liquid administration and does not include inpatient admission.
- `V0585`: The narrative terminates at LacticAcid without any ward admission activity.
- `V0587`: The narrative ends with CRP testing and contains no admission steps.
- `V0592`: The narrative terminates at IV Antibiotics without proceeding to ward admission.
- `V0645`: The narrative does not contain any admission step (NC or IC), representing a residual path without ward admission.
- `V0664`: The narrative ends at IV Liquid without reaching any admission category.
- `V0676`: The narrative ends with IV Antibiotics and does not contain any admission activity to normal or intensive care.
- `V0679`: The narrative terminates at IV Antibiotics without any ward admission activity.
- `V0685`: The narrative stops at IV Antibiotics and contains no ward admission step.
- `V0689`: The narrative ends at IV Antibiotics and lacks any inpatient ward admission.
- `V0694`: The narrative terminates at ER Sepsis Triage and does not reach any ward admission.
- `V0713`: The narrative ends at IV Antibiotics without any admission category activity.
- `V0750`: The narrative does not contain any admission activity, hence it fits neither normal care nor intensive care admission categories.
- `V0759`: The narrative ends at IV Antibiotics without involving any ward admission activities, so neither admission category fits.
- `V0764`: The narrative terminates at ER Sepsis Triage and does not contain any ward admission steps.
- `V0774`: The narrative terminates at ER Sepsis Triage without reaching any ward admission activity.
- `V0775`: The narrative ends at CRP and does not include any ward admission event.
- `V0777`: The narrative ends at 'Leucocytes' and does not contain any admission activity.
- `V0778`: The narrative ends at 'Leucocytes' and does not contain any admission activity.
- `V0791`: The narrative ends at 'IV Antibiotics' without any subsequent inpatient admission activity.
- `V0816`: The variant terminates at IV Antibiotics without any ward admission activity, falling into the residual.
- `V0820`: The variant ends at LacticAcid without any inpatient admission, thus belonging to the residual.
- `V0832`: The narrative terminates at IV Antibiotics and does not contain any admission activities.
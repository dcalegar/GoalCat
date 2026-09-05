# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_axisadmission_rep4` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Admission NC (`admission_nc`)

Patient is admitted to a non-critical inpatient ward.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative Admission NC (id=15) under the OR-decomposition of goal id=5. It appears frequently in the sample (e.g. V0008, V0068) representing standard inpatient ward placement.

**Goal-model linkage:** 15 (Task): Admission NC

**Coverage:** macro 660/846 variants (78.0%) · micro 712/1050 cases (67.8%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 10.02, nearest other category `admission_ic` at mean distance 21.07

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.406, nearest other category `admission_ic` at mean distance 0.432

## Admission IC (`admission_ic`)

Patient is admitted to an intensive care inpatient ward, which harms the softgoal to minimize time-to-treatment via some negative contribution.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative Admission IC (id=16) under the OR-decomposition of goal id=5. Evidence in the sample (such as V0605 and V0317) shows cases realizing intensive care admission.

**Goal-model linkage:** 16 (Task): Admission IC

**Coverage:** macro 98/846 variants (11.6%) · micro 98/1050 cases (9.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 24.41, nearest other category `admission_nc` at mean distance 21.07

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.338, nearest other category `admission_nc` at mean distance 0.432

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

- `V0001`: The narrative ends at ER Sepsis Triage and does not involve any patient admission.
- `V0002`: The narrative ends at CRP and does not involve any patient admission.
- `V0003`: The narrative ends at Leucocytes and does not involve any patient admission.
- `V0004`: The narrative ends at IV Antibiotics in the emergency context and does not involve any patient admission.
- `V0005`: The narrative ends at LacticAcid and does not involve any patient admission.
- `V0006`: The narrative ends at IV Antibiotics without involving any patient admission.
- `V0007`: The narrative ends at IV Antibiotics without involving any patient admission.
- `V0009`: The narrative ends at IV Antibiotics and does not involve an admission.
- `V0010`: The narrative terminates at ER Sepsis Triage without any admission step.
- `V0011`: The narrative ends at IV Antibiotics and does not involve any admission.
- `V0012`: The narrative terminates at IV Antibiotics and contains no admission activity.
- `V0013`: The narrative ends at Leucocytes without patient admission.
- `V0017`: The narrative ends at ER Sepsis Triage without any admission.
- `V0019`: The narrative ends at IV Antibiotics and lacks any patient admission.
- `V0020`: The narrative ends at CRP without involving an admission.
- `V0025`: The narrative ends at IV Antibiotics and does not involve any patient admission.
- `V0027`: The narrative ends at 'IV Antibiotics' and does not contain any admission activity to an inpatient ward.
- `V0029`: The activity sequence terminates at 'Leucocytes' without any inpatient admission steps.
- `V0031`: The process stops at 'LacticAcid' and lacks any admission event.
- `V0034`: The variant ends at 'IV Liquid' and does not feature an admission event.
- `V0036`: The sequence ends at 'CRP' without any inpatient ward admission.
- `V0038`: Ends at 'IV Antibiotics' with no admission activity recorded.
- `V0043`: The sequence terminates at 'LacticAcid' without inpatient admission.
- `V0050`: The variant ends at 'CRP' and does not contain any admission activity.
- `V0056`: The narrative ends at 'IV Antibiotics' without containing any admission activity.
- `V0062`: The narrative ends at 'IV Antibiotics' without containing any admission activity.
- `V0081`: The narrative ends at IV Liquid and does not contain any admission activity.
- `V0088`: The narrative ends at IV Antibiotics and does not contain any admission activity.
- `V0092`: The narrative ends at LacticAcid and does not contain any admission activity.
- `V0127`: The narrative ends at LacticAcid without any inpatient ward admission event.
- `V0132`: The narrative terminates at 'IV Antibiotics' without any ward admission.
- `V0133`: The narrative terminates at 'IV Antibiotics' without any ward admission.
- `V0137`: The narrative terminates at 'LacticAcid' without any ward admission.
- `V0146`: The narrative terminates at 'Leucocytes' without any ward admission.
- `V0148`: The narrative terminates at 'IV Antibiotics' without any ward admission.
- `V0187`: The narrative stops at CRP and does not contain any admission activity.
- `V0197`: The narrative ends at Leucocytes without containing any admission event.
- `V0217`: The narrative ends at 'IV Antibiotics' without any inpatient ward admission activity.
- `V0219`: The narrative ends at 'Leucocytes' without any inpatient ward admission activity.
- `V0232`: The narrative ends at 'IV Antibiotics' and does not contain any admission activity.
- `V0234`: The narrative terminates at 'Leucocytes' without involving any ward admission.
- `V0260`: The narrative ends at IV Antibiotics without any inpatient ward admission activity.
- `V0287`: The narrative ends at 'CRP' without any inpatient ward admission activity.
- `V0292`: The narrative terminates at 'Leucocytes' and does not contain any ward admission activity.
- `V0302`: The variant ends at ER Sepsis Triage and does not contain any admission activity.
- `V0305`: The variant terminates at IV Antibiotics without reaching any ward admission.
- `V0322`: The variant terminates at IV Antibiotics without reaching any ward admission.
- `V0325`: The variant terminates at IV Antibiotics without reaching any ward admission.
- `V0330`: The process variant ends at 'IV Liquid' and does not contain any inpatient ward admission activities.
- `V0342`: The process variant ends at 'CRP' and lacks any inpatient ward admission activities.
- `V0349`: The process variant ends at 'ER Sepsis Triage' and does not contain any inpatient ward admission activities.
- `V0378`: The narrative ends with 'IV Antibiotics' and does not contain any admission activity.
- `V0379`: The narrative ends with 'IV Antibiotics' and does not contain any admission activity.
- `V0417`: The narrative ends at 'ER Triage' and does not contain any admission activity, hence it fits neither admission category.
- `V0429`: The narrative ends at 'IV Antibiotics' and does not contain any admission activity.
- `V0488`: The narrative does not contain any admission activity, ending at IV Liquid.
- `V0492`: The narrative does not contain any admission activity, ending at IV Liquid.
- `V0495`: The narrative does not contain any admission activity, ending at IV Antibiotics.
- `V0507`: The narrative does not include any patient admission activity, ending at IV Antibiotics.
- `V0510`: The narrative does not contain an admission step, concluding with IV Antibiotics.
- `V0516`: The process variant terminates at Leucocytes without any inpatient admission steps.
- `V0517`: The process variant terminates at ER Triage without any inpatient admission steps.
- `V0549`: The narrative ends at IV Liquid and contains no admission activity, so neither category is realized.
- `V0575`: The variant ends without any admission event, thus fitting neither admission category.
- `V0580`: The narrative does not contain any admission activity, ending at CRP.
- `V0584`: The narrative does not contain any admission activity, ending at IV Liquid.
- `V0585`: The narrative does not contain any admission activity, ending at LacticAcid.
- `V0587`: The narrative does not contain any admission activity, ending at CRP.
- `V0592`: The narrative does not contain any admission activity, ending at IV Antibiotics.
- `V0645`: The narrative does not contain any admission to an inpatient ward.
- `V0664`: The narrative ends at IV Liquid and does not reach any inpatient admission activity.
- `V0676`: The narrative ends at IV Antibiotics without any admission activity to an inpatient ward.
- `V0679`: The narrative finishes at IV Antibiotics and does not contain any inpatient admission steps.
- `V0685`: The narrative ends at IV Antibiotics without any inpatient admission.
- `V0689`: The narrative concludes at IV Antibiotics without involving an inpatient ward admission.
- `V0694`: The narrative terminates at ER Sepsis Triage and does not show an inpatient admission.
- `V0713`: Neither Admission NC nor Admission IC is present in the sequence; the process ends at IV Antibiotics.
- `V0750`: The narrative does not contain any admission activity, ending at IV Antibiotics without realizing any admission categories.
- `V0759`: The narrative ends at IV Antibiotics without any ward admission activity.
- `V0764`: The narrative ends at ER Sepsis Triage without any ward admission activity.
- `V0774`: The narrative ends at ER Sepsis Triage without any ward admission activity.
- `V0775`: The narrative ends at CRP without any ward admission activity.
- `V0777`: The narrative ends at 'Leucocytes' without any inpatient ward admission activity.
- `V0778`: The narrative concludes at 'Leucocytes' and does not contain any admission events.
- `V0791`: The narrative ends at 'IV Antibiotics' without any admission step.
- `V0816`: The variant ends at IV Antibiotics without any admission activity, hence it does not realize either admission category.
- `V0820`: The variant ends at LacticAcid without any admission activity, hence it does not realize either admission category.
- `V0832`: The narrative ends at 'IV Antibiotics' and does not contain any admission activity to an inpatient ward.
# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_axisadmission_pertA_remove_16_rep1` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Admission NC (`admission_nc`)

Patient is admitted to a standard inpatient ward. This contributes to the process completing its pathway but does not directly target softgoals like time-to-treatment, though performance is evaluated via indicators such as post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the single declared alternative id=15 (Admission NC) under goal id=5, as supported by multiple sampled variants (e.g., V0008, V0625, V0551) showing standard ward admission.

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

- `V0001`: The process terminates at ER Sepsis Triage and does not involve admission to a standard inpatient ward.
- `V0002`: The process ends at CRP without any inpatient ward admission.
- `V0003`: The process concludes with Leucocytes and does not include standard ward admission.
- `V0004`: The pathway finishes at IV Antibiotics without an inpatient admission event.
- `V0005`: The variant ends at LacticAcid without proceeding to an inpatient ward.
- `V0006`: The variant ends with IV Antibiotics and lacks any inpatient ward admission.
- `V0007`: The narrative completes at IV Antibiotics without reaching a standard inpatient ward.
- `V0009`: The pathway finishes at IV Antibiotics and does not involve inpatient ward admission.
- `V0010`: The sequence ends at ER Sepsis Triage with no standard ward admission.
- `V0011`: The process ends at IV Antibiotics without an inpatient admission event.
- `V0012`: The pathway terminates at IV Antibiotics and does not reach standard inpatient admission.
- `V0013`: The variant ends at Leucocytes without including an admission step.
- `V0017`: The sequence ends at ER Sepsis Triage without any admission to an inpatient ward.
- `V0019`: The process ends at IV Antibiotics without reaching a standard inpatient ward.
- `V0020`: The narrative terminates at CRP without an inpatient admission.
- `V0025`: The pathway concludes at IV Antibiotics without an inpatient ward admission.
- `V0027`: The process finishes at IV Antibiotics without involving an inpatient ward admission.
- `V0029`: The variant ends at Leucocytes without an inpatient admission step.
- `V0031`: The narrative concludes at LacticAcid without standard inpatient ward admission.
- `V0034`: The sequence ends at IV Liquid without reaching a standard inpatient ward.
- `V0036`: The narrative finishes at CRP without an inpatient admission event.
- `V0038`: The variant ends at IV Antibiotics without standard inpatient ward admission.
- `V0043`: The narrative ends at LacticAcid without an inpatient admission.
- `V0050`: The variant terminates at CRP without reaching a standard inpatient ward.
- `V0056`: The narrative does not contain Admission NC and therefore does not realize the admission_nc category.
- `V0062`: The narrative does not contain Admission NC and therefore does not realize the admission_nc category.
- `V0081`: The narrative does not contain Admission NC and therefore does not realize the admission_nc category.
- `V0088`: The narrative does not contain Admission NC and therefore does not realize the admission_nc category.
- `V0092`: The narrative does not contain Admission NC and therefore does not realize the admission_nc category.
- `V0127`: The narrative does not include Admission NC.
- `V0132`: The narrative does not include Admission NC.
- `V0133`: The narrative does not include Admission NC.
- `V0137`: The narrative does not include Admission NC.
- `V0145`: The narrative does not include Admission NC.
- `V0146`: The narrative does not include Admission NC.
- `V0148`: The narrative does not include Admission NC.
- `V0167`: The narrative does not include the 'Admission NC' activity.
- `V0187`: The narrative does not include the 'Admission NC' activity.
- `V0197`: The narrative does not include the 'Admission NC' activity.
- `V0217`: The narrative does not include Admission NC.
- `V0218`: The narrative does not include Admission NC.
- `V0219`: The narrative does not include Admission NC.
- `V0232`: The narrative does not include Admission NC.
- `V0234`: The narrative does not include Admission NC.
- `V0260`: The narrative terminates at IV Antibiotics without reaching any inpatient admission step.
- `V0287`: The narrative terminates at CRP without reaching an inpatient admission step.
- `V0292`: The narrative terminates at Leucocytes without reaching an inpatient admission step.
- `V0302`: The narrative stops at ER Sepsis Triage and does not contain any admission to a standard inpatient ward.
- `V0305`: The narrative terminates at IV Antibiotics in the ER without proceeding to standard inpatient ward admission.
- `V0322`: The narrative terminates at IV Antibiotics in the ER without proceeding to standard inpatient ward admission.
- `V0325`: The narrative terminates at IV Antibiotics in the ER without proceeding to standard inpatient ward admission.
- `V0330`: The narrative terminates at IV Liquid without standard inpatient ward admission.
- `V0342`: The narrative terminates at CRP without standard inpatient ward admission.
- `V0349`: The narrative terminates at ER Sepsis Triage without standard inpatient ward admission.
- `V0365`: The narrative includes Admission IC rather than Admission NC, so it does not realize the target category.
- `V0378`: The narrative ends at IV Antibiotics without an inpatient ward admission, so the category is not realized.
- `V0379`: The narrative terminates at IV Antibiotics and does not include Admission NC.
- `V0407`: The narrative uses 'Admission IC' rather than standard inpatient ward admission.
- `V0417`: The narrative does not contain an inpatient admission activity.
- `V0429`: The narrative does not contain an inpatient admission activity.
- `V0432`: The narrative uses 'Admission IC' rather than standard inpatient ward admission.
- `V0488`: The narrative ends at IV Liquid and does not include an inpatient ward admission, so it does not realize the category.
- `V0492`: The trace ends at IV Liquid without any ward admission, falling into the residual.
- `V0495`: The process terminates at IV Antibiotics without reaching inpatient admission.
- `V0507`: The narrative does not contain 'Admission NC' or any equivalent category process step.
- `V0510`: The narrative does not contain 'Admission NC'.
- `V0516`: The narrative does not contain 'Admission NC'.
- `V0517`: The narrative does not contain 'Admission NC'.
- `V0549`: The narrative does not contain 'Admission NC'.
- `V0575`: The narrative does not include Admission NC, so it does not realize the category.
- `V0580`: The narrative does not include Admission NC, so it does not realize the category.
- `V0584`: The narrative does not include Admission NC, so it does not realize the category.
- `V0585`: The narrative does not include Admission NC, so it does not realize the category.
- `V0587`: The narrative does not include Admission NC, so it does not realize the category.
- `V0592`: The narrative does not include Admission NC, so it does not realize the category.
- `V0621`: The narrative lacks the Admission NC activity, so it does not realize the standard inpatient ward admission category.
- `V0645`: The narrative lacks the Admission NC activity, so it does not realize the standard inpatient ward admission category.
- `V0654`: The narrative ends in 'Leucocytes' and involves 'Admission IC' rather than a standard inpatient ward ('Admission NC').
- `V0664`: The narrative ends at 'IV Liquid' and does not contain any admission activity.
- `V0676`: The narrative ends at 'IV Antibiotics' and does not contain an admission activity.
- `V0679`: The narrative ends at 'IV Antibiotics' without proceeding to a standard inpatient admission.
- `V0685`: The narrative terminates at 'IV Antibiotics' and lacks an admission activity.
- `V0689`: The narrative ends at 'IV Antibiotics' without containing any admission activity.
- `V0694`: The narrative terminates at 'ER Sepsis Triage' and does not involve any admission activity.
- `V0713`: The narrative does not contain Admission NC.
- `V0715`: The narrative contains Admission IC instead of Admission NC.
- `V0742`: The narrative does not contain Admission NC.
- `V0750`: The narrative does not contain Admission NC.
- `V0759`: The variant terminates at IV Antibiotics and does not reach standard inpatient admission (Admission NC).
- `V0764`: The variant terminates at ER Sepsis Triage and does not proceed to admission.
- `V0772`: The process terminates at CRP and does not include Admission NC.
- `V0774`: The sequence stops at ER Sepsis Triage without reaching inpatient admission.
- `V0775`: The process ends at CRP without proceeding to Admission NC.
- `V0777`: The pathway terminates at Leucocytes without reaching Admission NC.
- `V0778`: The variant ends at Leucocytes and does not include Admission NC.
- `V0791`: The variant terminates at IV Antibiotics without advancing to Admission NC.
- `V0816`: The narrative does not contain Admission NC.
- `V0820`: The narrative does not contain Admission NC.
- `V0832`: The narrative does not contain Admission NC.
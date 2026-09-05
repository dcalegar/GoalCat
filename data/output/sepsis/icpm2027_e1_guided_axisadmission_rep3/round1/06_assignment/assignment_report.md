# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_axisadmission_rep3` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Admission to Non-Critical Ward (`admission_nc`)

Patient is admitted to an inpatient non-critical ward. Advances the patient along the disposition path and is typically measured by downstream post-discharge outcomes.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Admission NC (id=15) under the OR-decomposition of goal 5. Supported by frequent and rare variants like V0008, V0625, and V0068 where Admission NC realizes the inpatient ward admission.

**Goal-model linkage:** 15 (Task): Admission NC

**Coverage:** macro 663/846 variants (78.4%) · micro 715/1050 cases (68.1%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 10.14, nearest other category `admission_ic` at mean distance 21.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.407, nearest other category `admission_ic` at mean distance 0.429

## Admission to Intensive Care (`admission_ic`)

Patient is admitted to an intensive care inpatient ward. Associated with intensive care management and carries a negative contribution to minimizing time-to-treatment (SomeNegative -25).

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Admission IC (id=16) under the OR-decomposition of goal 5. Supported by narrative evidence in variants like V0605, V0317, and V0710 where patients are routed to intensive care.

**Goal-model linkage:** 16 (Task): Admission IC

**Coverage:** macro 95/846 variants (11.2%) · micro 95/1050 cases (9.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 24.61, nearest other category `admission_nc` at mean distance 21.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.337, nearest other category `admission_nc` at mean distance 0.429

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
- `V0296` (`admission_nc`) / `V0357` (`admission_ic`): structural=2, profile=0.060
- `V0357` (`admission_ic`) / `V0408` (`admission_nc`): structural=2, profile=0.135
- `V0008` (`admission_nc`) / `V0082` (`admission_ic`): structural=3, profile=0.340
- `V0040` (`admission_nc`) / `V0082` (`admission_ic`): structural=3, profile=0.759
- `V0044` (`admission_nc`) / `V0793` (`admission_ic`): structural=3, profile=0.151
- `V0076` (`admission_nc`) / `V0621` (`admission_ic`): structural=3, profile=0.389

## Residual

88/846 variants (10.4%), 240/1050 cases (22.9%) unassigned.

- `V0001`: The narrative ends at ER Sepsis Triage and does not involve any inpatient ward admission.
- `V0002`: The narrative involves initial diagnostics (CRP) but does not include any inpatient ward admission.
- `V0003`: The narrative stops at diagnostic lab tests (Leucocytes) and does not contain an admission step.
- `V0004`: The narrative ends at IV Antibiotics administration in the ER without proceeding to an inpatient ward admission.
- `V0005`: The narrative concludes with LacticAcid testing and does not show any inpatient ward admission.
- `V0006`: The narrative ends after IV Antibiotics delivery and does not advance to an inpatient ward.
- `V0007`: The narrative finishes at IV Antibiotics and lacks any inpatient ward admission event.
- `V0009`: The narrative stops at IV Antibiotics and does not involve admission to a hospital ward.
- `V0010`: The narrative involves basic ER evaluations and triage but no inpatient admission.
- `V0011`: The narrative finishes with IV Antibiotics and does not show an inpatient admission step.
- `V0012`: The narrative ends at IV Antibiotics without proceeding to an inpatient ward.
- `V0013`: The narrative finishes with laboratory diagnostics and does not include an admission event.
- `V0017`: The narrative ends at ER Sepsis Triage and does not feature any inpatient ward admission.
- `V0019`: The narrative finishes at IV Antibiotics and does not progress to an inpatient ward admission.
- `V0020`: The narrative ends with CRP diagnostics and lacks any inpatient ward admission event.
- `V0025`: The narrative terminates at IV Antibiotics and does not contain an inpatient ward admission.
- `V0027`: The narrative ends at IV Antibiotics without reaching any inpatient ward admission activity.
- `V0029`: The narrative terminates at Leucocytes without an inpatient ward admission.
- `V0031`: Ends at LacticAcid without any ward admission activity.
- `V0034`: Terminates at IV Liquid without an inpatient ward admission.
- `V0036`: Ends at CRP without any ward admission.
- `V0038`: Terminates at IV Antibiotics without reaching a ward admission.
- `V0043`: Ends at LacticAcid without an inpatient ward admission.
- `V0050`: Terminates at CRP without an inpatient ward admission.
- `V0056`: The variant stops at IV Antibiotics without any admission activity, hence it does not realize either ward admission category.
- `V0062`: The process terminates at IV Antibiotics with no admission step, so no category applies.
- `V0081`: The narrative ends at 'IV Liquid' and contains no admission activity, so neither category fits.
- `V0088`: The narrative ends at 'IV Antibiotics' without any admission step, so neither category fits.
- `V0092`: The narrative ends at 'LacticAcid' without any admission step, so neither category fits.
- `V0127`: The narrative ends with LacticAcid and does not contain any inpatient ward admission activity.
- `V0132`: The narrative ends with IV Antibiotics and does not contain any inpatient ward admission activity.
- `V0133`: The narrative ends with IV Antibiotics and does not contain any inpatient ward admission activity.
- `V0137`: The narrative ends with LacticAcid and does not contain any inpatient ward admission activity.
- `V0146`: The narrative ends with Leucocytes and does not contain any inpatient ward admission activity.
- `V0148`: The narrative ends with IV Antibiotics and does not contain any inpatient ward admission activity.
- `V0187`: The narrative does not contain any admission activity, ending at CRP.
- `V0197`: The narrative does not contain any admission activity.
- `V0217`: The narrative does not contain any admission activity, ending in IV Antibiotics.
- `V0219`: The narrative does not contain any admission activity, ending in Leucocytes.
- `V0232`: The narrative ends at 'IV Antibiotics' and does not contain any inpatient admission activity.
- `V0234`: The narrative terminates at 'Leucocytes' and does not contain any inpatient admission activity.
- `V0260`: The narrative ends at IV Antibiotics without reaching any inpatient ward admission category.
- `V0287`: The narrative ends at CRP and does not include any admission activity.
- `V0292`: The narrative ends at Leucocytes and does not include any admission activity.
- `V0302`: The process stops at ER Sepsis Triage and does not reach any inpatient admission category.
- `V0305`: The process ends at IV Antibiotics without any inpatient ward admission.
- `V0322`: The process terminates at IV Antibiotics without reaching any ward admission category.
- `V0325`: The process ends at IV Antibiotics without an admission event.
- `V0330`: The process ends at IV Liquid and does not reach any ward admission milestone.
- `V0342`: The process terminates at a CRP lab test without reaching any ward admission event.
- `V0349`: The trace stops at ER Sepsis Triage and does not proceed to any admission.
- `V0378`: The narrative does not contain any admission activity, thus realizing neither category.
- `V0379`: The narrative does not contain any admission activity, thus realizing neither category.
- `V0417`: The narrative does not contain any admission activity to a ward, terminating at ER Triage.
- `V0429`: The narrative ends with 'IV Antibiotics' and does not contain any admission activity.
- `V0488`: The narrative ends at 'IV Liquid' and does not contain any inpatient admission activity, so neither category fits.
- `V0492`: The trace terminates at 'IV Liquid' without any ward admission activity, so no category is realized.
- `V0495`: The process terminates at 'IV Antibiotics' without proceeding to inpatient ward admission.
- `V0507`: The narrative ends at 'IV Antibiotics' without containing any ward admission activity, so it does not fit the taxonomy categories.
- `V0510`: The narrative ends at 'IV Antibiotics' without containing any ward admission activity, so it does not fit the taxonomy categories.
- `V0516`: The narrative ends at 'Leucocytes' without containing any ward admission activity, so it does not fit the taxonomy categories.
- `V0517`: The narrative ends at 'ER Triage' without containing any ward admission activity, so it does not fit the taxonomy categories.
- `V0549`: The narrative terminates at 'IV Liquid' and contains no inpatient ward admission steps, falling into the residual.
- `V0575`: The narrative ends without any inpatient admission activity, focusing only on ER and lab tests, so neither category fits.
- `V0580`: The variant ends at CRP without any inpatient ward admission activity.
- `V0584`: The process terminates at IV Liquid without reaching any inpatient ward admission.
- `V0585`: The process ends at LacticAcid without any ward admission.
- `V0587`: The process concludes at CRP with no inpatient ward admission taking place.
- `V0592`: The process stops at IV Antibiotics and does not involve any inpatient ward admission.
- `V0645`: The narrative does not contain any ward admission event, hence it does not realize either admission category.
- `V0664`: The process variant terminates at 'IV Liquid' and does not reach any inpatient ward admission category.
- `V0676`: The narrative ends at IV Antibiotics without any admission event, so it does not realize either admission category.
- `V0679`: The narrative stops at IV Antibiotics without an admission to any ward.
- `V0685`: The narrative concludes with IV Antibiotics and contains no admission event.
- `V0689`: The process terminates at IV Antibiotics without any admission.
- `V0694`: The process stops at ER Sepsis Triage without reaching any ward admission.
- `V0713`: The narrative ends at IV Antibiotics without any ward admission activity, so neither admission category fits.
- `V0750`: The narrative terminates at IV Antibiotics without reaching any ward admission event.
- `V0759`: The narrative ends at IV Antibiotics without reaching any inpatient ward admission category.
- `V0764`: The narrative terminates at ER Sepsis Triage and does not contain any ward admission.
- `V0774`: The narrative ends at ER Sepsis Triage without any ward admission activity.
- `V0775`: The narrative terminates at CRP and lacks any inpatient ward admission.
- `V0777`: The narrative stops at 'Leucocytes' and does not contain any patient admission or ward placement activities.
- `V0778`: The narrative terminates at 'Leucocytes' without any inpatient admission step.
- `V0791`: The narrative ends at 'IV Antibiotics' and contains no admission steps.
- `V0816`: The variant ends at 'IV Antibiotics' without any admission activity, so it does not realize either admission category.
- `V0820`: The variant terminates at 'LacticAcid' without proceeding to any inpatient admission category.
- `V0832`: The narrative ends at IV Antibiotics without any ward admission activity, so neither category is realized.
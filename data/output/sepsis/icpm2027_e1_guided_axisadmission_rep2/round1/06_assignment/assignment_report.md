# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_axisadmission_rep2` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Non-Critical Admission (`admission_nc`)

Patient is admitted to a non-critical inpatient ward, advancing the goal of reaching a documented disposition while supporting avoidance of post-discharge deterioration, measured against post-discharge ER return indicators.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Admission NC (id=15) under the OR decomposition of goal id=5. Supported by frequent samples such as variant V0008 where Admission NC precedes Release A.

**Goal-model linkage:** 15 (Task): Admission NC

**Coverage:** macro 656/846 variants (77.5%) · micro 708/1050 cases (67.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 9.30, nearest other category `admission_ic` at mean distance 22.72

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.406, nearest other category `admission_ic` at mean distance 0.432

## Intensive Care Admission (`admission_ic`)

Patient is admitted to an intensive care unit, realizing inpatient ward admission with some negative contribution to minimizing time-to-treatment.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Admission IC (id=16) under the OR decomposition of goal id=5. Supported by variants such as V0605 and V0317 where Admission IC is utilized.

**Goal-model linkage:** 16 (Task): Admission IC

**Coverage:** macro 102/846 variants (12.1%) · micro 102/1050 cases (9.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 27.03, nearest other category `admission_nc` at mean distance 22.72

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.335, nearest other category `admission_nc` at mean distance 0.432

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

- `V0001`: The variant ends at ER Sepsis Triage and does not involve any ward admission.
- `V0002`: The variant ends at CRP diagnostics and does not include an admission.
- `V0003`: The variant ends at Leucocytes diagnostics without any admission activity.
- `V0004`: The variant administers IV Antibiotics in the ER but does not result in an inpatient admission.
- `V0005`: The variant ends with LacticAcid testing without admission.
- `V0006`: The variant ends with IV Antibiotics administration in the ER, with no admission.
- `V0007`: The variant ends with IV Antibiotics administration without an inpatient admission.
- `V0009`: The variant administers IV Antibiotics in the ER without proceeding to admission.
- `V0010`: The variant concludes in the ER and does not contain an admission step.
- `V0011`: The variant finishes with IV Antibiotics without an inpatient admission.
- `V0012`: The variant treats the patient with IV Antibiotics in the ER without admission.
- `V0013`: The variant ends with Leucocytes testing in the ER without admission.
- `V0017`: The variant ends at ER Sepsis Triage without any admission.
- `V0019`: The variant concludes with IV Antibiotics in the ER without admission.
- `V0020`: The variant ends with CRP testing and no admission.
- `V0025`: The variant administers IV Antibiotics in the ER without proceeding to admission.
- `V0027`: The narrative ends at IV Antibiotics without any ward admission activity.
- `V0029`: The narrative stops at Leucocytes and does not contain any admission activity.
- `V0031`: The narrative ends at LacticAcid without any inpatient ward admission.
- `V0034`: The narrative ends at IV Liquid and lacks any admission step.
- `V0036`: The narrative ends at CRP without any ward admission.
- `V0038`: The narrative terminates at IV Antibiotics without proceeding to admission.
- `V0043`: The narrative ends at LacticAcid without any admission activity.
- `V0050`: The narrative ends at CRP without any ward admission activity.
- `V0056`: The narrative terminates at 'IV Antibiotics' without proceeding to inpatient ward admission or disposition.
- `V0062`: The narrative ends at 'IV Antibiotics' without ward admission.
- `V0081`: The narrative does not contain any admission activity, ending in IV Liquid.
- `V0088`: The narrative does not contain any admission activity, ending in IV Antibiotics.
- `V0092`: The narrative does not contain any admission activity, ending in LacticAcid.
- `V0127`: The narrative does not contain any admission activity, ending at LacticAcid.
- `V0132`: The narrative ends at IV Antibiotics without any ward admission activity.
- `V0133`: The narrative ends at IV Antibiotics without any ward admission activity.
- `V0137`: The narrative terminates at LacticAcid without any inpatient admission.
- `V0146`: The narrative terminates at Leucocytes without any inpatient admission.
- `V0148`: The narrative terminates at IV Antibiotics without any ward admission activity.
- `V0187`: The narrative ends at CRP without any inpatient ward or ICU admission.
- `V0197`: The narrative terminates at Leucocytes without any inpatient ward or ICU admission.
- `V0217`: The narrative lacks any inpatient admission activity, thus realizing neither category.
- `V0219`: The narrative terminates early without any admission activity.
- `V0232`: The narrative stops at IV Antibiotics without involving any admission activity.
- `V0234`: The narrative stops at Leucocytes without involving any admission activity.
- `V0260`: The process ends at IV Antibiotics without any ward or ICU admission step.
- `V0287`: The patient did not reach an admission activity; the trace ends at CRP.
- `V0292`: The variant terminates at Leucocytes without reaching any admission activity.
- `V0302`: The process terminates at 'ER Sepsis Triage' and does not involve an inpatient ward admission.
- `V0305`: The process ends at 'IV Antibiotics' without proceeding to an inpatient ward admission.
- `V0322`: The process terminates at 'IV Antibiotics' without any inpatient admission.
- `V0325`: The process ends at 'IV Antibiotics' and does not involve inpatient ward or ICU admission.
- `V0330`: The process terminates at IV Liquid without any inpatient admission activity.
- `V0342`: The process terminates at CRP without any inpatient admission activity.
- `V0349`: The process terminates at ER Sepsis Triage without any inpatient admission activity.
- `V0378`: The narrative ends at 'IV Antibiotics' and does not contain any admission activity.
- `V0379`: The narrative ends at 'IV Antibiotics' and does not contain any admission activity.
- `V0417`: The narrative does not contain any admission activity, ending instead at ER Triage.
- `V0429`: The narrative ends at IV Antibiotics without any inpatient ward admission event.
- `V0488`: The narrative ends at IV Liquid without any ward admission activity, so neither admission category fits.
- `V0492`: The narrative terminates at IV Liquid and lacks any ward admission event.
- `V0495`: The narrative ends at IV Antibiotics and does not involve any inpatient admission.
- `V0507`: The narrative ends at IV Antibiotics without reaching any inpatient admission category.
- `V0510`: The narrative terminates at IV Antibiotics and does not realize any ward admission.
- `V0516`: The narrative terminates at Leucocytes without achieving inpatient ward admission.
- `V0517`: The narrative terminates at ER Triage without any admission.
- `V0549`: The narrative terminates at IV Liquid and does not reach any inpatient ward admission category.
- `V0575`: The variant does not contain any inpatient admission activity, ending in diagnostic laboratory tests.
- `V0580`: The process ends at CRP and does not include any inpatient admission activity.
- `V0584`: The process terminates at IV Liquid without any admission step.
- `V0585`: The process concludes at LacticAcid and lacks an admission event.
- `V0587`: The process ends at CRP without any ward admission activities.
- `V0592`: The process terminates at IV Antibiotics without admission.
- `V0645`: The process ends at LacticAcid without any inpatient ward admission (Admission NC or Admission IC).
- `V0664`: The narrative stops at IV Liquid without reaching a ward admission category.
- `V0676`: The narrative ends with IV Antibiotics and does not include an inpatient ward admission.
- `V0679`: The narrative terminates at IV Antibiotics without any ward admission activity.
- `V0685`: The narrative ends with IV Antibiotics and lacks any inpatient ward admission.
- `V0689`: The narrative terminates at IV Antibiotics without any admission event.
- `V0694`: The narrative ends at ER Sepsis Triage and does not contain any ward admission.
- `V0713`: The narrative ends at IV Antibiotics without any inpatient ward or intensive care admission step, so neither admission category fits.
- `V0750`: The narrative ends at IV Antibiotics without reaching any inpatient ward admission category.
- `V0759`: The narrative ends at IV Antibiotics without any ward or ICU admission event.
- `V0764`: The narrative terminates at ER Sepsis Triage and does not contain any admission event.
- `V0774`: The narrative terminates at ER Sepsis Triage and does not contain any admission event.
- `V0775`: The narrative terminates at CRP and does not contain any admission event.
- `V0777`: The narrative ends at Leucocytes without any admission event.
- `V0778`: The narrative ends at Leucocytes without any admission event.
- `V0791`: The narrative ends at IV Antibiotics without any admission event.
- `V0816`: The narrative ends at IV Antibiotics without involving any ward admission activities.
- `V0820`: The narrative ends at LacticAcid without involving any ward admission activities.
- `V0832`: The narrative ends at IV Antibiotics without reaching any inpatient admission category.
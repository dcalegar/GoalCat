# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_axisadmission_pertC_distractor_5_112_rep5` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Admission to Normal Care (`admission_nc`)

Patient is admitted to a normal care inpatient ward (Admission NC), supporting general inpatient stabilization and discharge pathways without intensive or high-dependency intervention.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative id=15 from the OR decomposition of goal id=5. Supported by frequent sampled variants such as V0008, where normal care admission leads to subsequent release or further observation.

**Goal-model linkage:** 15 (Task): Admission NC

**Coverage:** macro 659/846 variants (77.9%) · micro 711/1050 cases (67.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 9.82, nearest other category `admission_ic` at mean distance 21.50

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.408, nearest other category `admission_ic` at mean distance 0.429

## Admission to Intensive Care (`admission_ic`)

Patient is admitted to an Intensive Care unit (Admission IC), reflecting higher acuity treatment needs. Note that Admission IC carries a negative contribution (-25) to minimizing time-to-treatment in the goal model context.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative id=16 from the OR decomposition of goal id=5. Supported by sampled variants like V0605 and V0317 where intensive care admission is explicitly observed.

**Goal-model linkage:** 16 (Task): Admission IC

**Coverage:** macro 100/846 variants (11.8%) · micro 100/1050 cases (9.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 24.75, nearest other category `admission_nc` at mean distance 21.50

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.332, nearest other category `admission_nc` at mean distance 0.429

## Admission to High-Dependency Unit (`admission_hdu`)

Patient is admitted to a High-Dependency Unit (Admission to High-Dependency Unit) to receive intermediate level care between normal ward and intensive care.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative id=112 from the OR decomposition of goal id=5. Maintained as a distinct declared alternative despite lower direct frequency in the sample, following the rule that lack of frequent samples does not merge a declared alternative.

**Goal-model linkage:** 112 (Task): Admission to High-Dependency Unit

**Coverage:** macro 0/846 variants (0.0%) · micro 0/1050 cases (0.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a, nearest other category `None` at mean distance n/a

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a, nearest other category `None` at mean distance n/a

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0654` / `V0710` (category `admission_ic`): structural=177, profile=0.576
- `V0082` / `V0710` (category `admission_ic`): structural=176, profile=0.680
- `V0710` / `V0742` (category `admission_ic`): structural=176, profile=0.583
- `V0621` / `V0710` (category `admission_ic`): structural=175, profile=0.752
- `V0407` / `V0710` (category `admission_ic`): structural=174, profile=0.624
- `V0710` / `V0793` (category `admission_ic`): structural=174, profile=0.480
- `V0068` / `V0710` (category `admission_ic`): structural=173, profile=0.509
- `V0639` / `V0710` (category `admission_ic`): structural=173, profile=0.375
- `V0710` / `V0715` (category `admission_ic`): structural=173, profile=0.556
- `V0154` / `V0710` (category `admission_ic`): structural=172, profile=0.338

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

87/846 variants (10.3%), 239/1050 cases (22.8%) unassigned.

- `V0001`: This narrative ends at ER Sepsis Triage and does not involve any patient admission.
- `V0002`: This narrative ends at CRP testing without any admission to a care unit.
- `V0003`: This narrative concludes with Leucocytes testing and does not show an inpatient admission.
- `V0004`: This narrative terminates at IV Antibiotics in the emergency phase and does not include an admission event.
- `V0005`: This narrative ends with LacticAcid testing without progressing to an admission category.
- `V0006`: This narrative finishes with IV Antibiotics and does not involve hospital admission.
- `V0007`: This narrative stops at IV Antibiotics without any admission to normal care, HDU, or ICU.
- `V0009`: This narrative concludes after IV Antibiotics and contains no admission step.
- `V0010`: This narrative involves emergency lab tests and triage without any admission activity.
- `V0011`: This narrative ends with IV Antibiotics administration and lacks an admission event.
- `V0012`: This narrative terminates at IV Antibiotics and does not involve an inpatient admission.
- `V0013`: This narrative stops at Leucocytes testing with no admission to any unit.
- `V0017`: This narrative concludes at ER Sepsis Triage and does not show an inpatient admission.
- `V0019`: This narrative ends at IV Antibiotics and does not record an admission.
- `V0020`: This narrative finishes with CRP testing without any admission process.
- `V0025`: This narrative terminates at IV Antibiotics and does not contain an admission event.
- `V0027`: The narrative ends with 'IV Antibiotics' and does not contain any ward or unit admission activity.
- `V0029`: The narrative terminates at 'Leucocytes' and does not contain any inpatient admission step.
- `V0031`: The sequence ends with 'LacticAcid' without including any admission category.
- `V0034`: The sequence concludes with 'IV Liquid' and contains no ward admission steps.
- `V0036`: The variant ends with 'CRP' and lacks any admission category.
- `V0038`: The sequence finishes with 'IV Antibiotics' and does not involve any unit admission.
- `V0043`: The sequence ends with 'LacticAcid' without containing any admission events.
- `V0050`: The variant ends with 'CRP' and does not include any admission activities.
- `V0056`: The pathway terminates at IV Antibiotics without any ward admission activity.
- `V0062`: Ends at IV Antibiotics without any admission category.
- `V0081`: The narrative ends at 'IV Liquid' and contains no admission activity matching normal care, intensive care, or high-dependency unit categories.
- `V0092`: The narrative terminates at 'LacticAcid' and does not contain any admission activity.
- `V0127`: The narrative ends at LacticAcid and does not contain any ward admission steps.
- `V0132`: The narrative terminates at IV Antibiotics without any admission to a care unit.
- `V0133`: The narrative terminates at IV Antibiotics without any ward admission steps.
- `V0137`: The narrative stops at LacticAcid without any inpatient admission.
- `V0146`: The narrative stops at Leucocytes without an inpatient admission.
- `V0148`: The narrative stops at IV Antibiotics without inpatient admission.
- `V0187`: The narrative only shows ER triage, registration, and lab tests without any ward admission activity.
- `V0197`: The narrative consists solely of ER and lab tests without any admission activity.
- `V0217`: The narrative ends at IV Antibiotics without any ward admission activity, falling into the residual category.
- `V0219`: The narrative terminates at Leucocytes without an admission activity, falling into the residual category.
- `V0232`: The process ends at IV Antibiotics without any ward or unit admission activity.
- `V0234`: Terminates at Leucocytes testing with no admission events.
- `V0260`: The narrative ends at IV Antibiotics without any ward admission activity.
- `V0287`: The narrative ends at diagnostic testing (CRP) in the ER and does not contain any ward admission event.
- `V0292`: The narrative ends at Leucocytes and does not contain any ward admission event.
- `V0302`: The narrative stops at 'ER Sepsis Triage' without any inpatient ward or ICU admission activity.
- `V0305`: The narrative ends at 'IV Antibiotics' in the emergency setting without any admission to a ward or unit.
- `V0322`: The narrative ends at 'IV Antibiotics' without any admission activity.
- `V0325`: The narrative ends at 'IV Antibiotics' without any admission activity.
- `V0330`: The narrative ends at IV Liquid and does not contain any admission category activities.
- `V0342`: The narrative ends at CRP and does not contain any admission category activities.
- `V0349`: The narrative ends at ER Sepsis Triage and does not contain any admission category activities.
- `V0378`: The narrative stops at IV Antibiotics without any admission to normal care, ICU, or HDU.
- `V0379`: The narrative stops at IV Antibiotics without any admission to normal care, ICU, or HDU.
- `V0417`: The narrative ends at ER Triage and does not contain any admission activity, hence it is part of the residual.
- `V0429`: The narrative stops at IV Antibiotics and does not involve any ward admission category.
- `V0488`: The narrative does not contain any admission activity (NC, IC, or HDU).
- `V0492`: The narrative does not contain any admission activity (NC, IC, or HDU).
- `V0495`: The narrative does not contain any admission activity (NC, IC, or HDU).
- `V0507`: The narrative terminates at IV Antibiotics without reaching any inpatient admission category.
- `V0510`: The narrative ends at IV Antibiotics and does not contain any admission activity.
- `V0516`: The narrative terminates at Leucocytes and lacks any admission activity.
- `V0517`: The narrative ends at ER Triage and does not contain any admission pathway.
- `V0549`: The narrative ends at IV Liquid and does not include any ward admission category.
- `V0575`: The narrative stops at ER tests (Leucocytes) and does not realize any inpatient admission category.
- `V0580`: The narrative terminates at CRP and contains no admission events, meaning it does not realize any inpatient admission category.
- `V0584`: The narrative ends at IV Liquid and contains no admission events.
- `V0585`: The narrative ends at LacticAcid and includes no inpatient admission activities.
- `V0587`: The narrative terminates at CRP without any inpatient admission events.
- `V0592`: The narrative terminates at IV Antibiotics without involving any ward admission.
- `V0645`: The narrative does not contain any admission events, thus it belongs to the residual.
- `V0664`: The narrative terminates at IV Liquid without reaching any ward admission category.
- `V0676`: The narrative ends at IV Antibiotics without any admission activity to normal care, intensive care, or high-dependency unit.
- `V0679`: The narrative terminates at IV Antibiotics without an inpatient admission step.
- `V0685`: The narrative ends at IV Antibiotics without any ward or unit admission.
- `V0689`: The narrative terminates at IV Antibiotics with no admission activities.
- `V0694`: The narrative ends at ER Sepsis Triage without any admission steps.
- `V0713`: The narrative ends with IV Antibiotics without any ward admission activity, so it does not fit any admission category.
- `V0750`: The narrative does not contain any inpatient ward admission activities (normal care, high-dependency, or intensive care).
- `V0759`: The process terminates at IV Antibiotics without reaching any ward admission category.
- `V0764`: The process terminates at ER Sepsis Triage without any ward admission.
- `V0774`: The process ends at ER Sepsis Triage without proceeding to any ward admission.
- `V0775`: The process terminates at CRP without reaching any ward admission category.
- `V0777`: The narrative ends at 'Leucocytes' without any ward admission activity.
- `V0778`: The narrative terminates at 'Leucocytes' with no admission event.
- `V0791`: The narrative terminates at 'IV Antibiotics' without any ward admission activity.
- `V0816`: The narrative stops at IV Antibiotics and does not contain any ward or ICU admission activities.
- `V0820`: The narrative stops at LacticAcid and does not contain any ward or ICU admission activities.
- `V0832`: The narrative ends at IV Antibiotics and does not include any ward admission category.
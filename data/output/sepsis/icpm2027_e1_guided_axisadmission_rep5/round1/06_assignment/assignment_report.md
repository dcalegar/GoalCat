# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_axisadmission_rep5` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Non-Critical Admission (`admission_nc`)

Admission of the patient to a non-critical inpatient ward (Admission NC), realizing the goal of admitting a patient to an inpatient ward. This contributes toward standard post-discharge recovery outcomes.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared XOR alternative Admission NC (id=15) based on the goal model decomposition. Sample variants such as V0008, V0070, and V0066 realize this alternative directly.

**Goal-model linkage:** 15 (Task): Admission NC

**Coverage:** macro 667/846 variants (78.8%) · micro 719/1050 cases (68.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 10.48, nearest other category `admission_ic` at mean distance 20.32

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.407, nearest other category `admission_ic` at mean distance 0.429

## Intensive Care Admission (`admission_ic`)

Admission of the patient to an intensive care unit (Admission IC), realizing the goal of inpatient admission while incurring a negative contribution (-25) to minimizing time-to-treatment due to specialized handling requirements.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared XOR alternative Admission IC (id=16) as defined in the goal model. Sample variants such as V0605, V0317, and V0068 reflect patient cases routed through intensive care.

**Goal-model linkage:** 16 (Task): Admission IC

**Coverage:** macro 91/846 variants (10.8%) · micro 91/1050 cases (8.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 23.47, nearest other category `admission_nc` at mean distance 20.32

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.338, nearest other category `admission_nc` at mean distance 0.429

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

- `V0001`: The narrative stops at ER Sepsis Triage and does not involve any patient admission.
- `V0002`: The narrative ends with diagnostic tests (CRP) and does not involve admission.
- `V0003`: The narrative ends with diagnostic tests (Leucocytes) without admission.
- `V0004`: The narrative concludes with IV Antibiotics administration and does not include ward or ICU admission.
- `V0005`: The narrative ends with LacticAcid testing and does not include admission.
- `V0006`: The narrative ends with IV Antibiotics and does not include an inpatient admission.
- `V0007`: The narrative ends with IV Antibiotics and does not involve admission.
- `V0009`: The narrative concludes with IV Antibiotics without admission.
- `V0010`: The narrative ends with ER Sepsis Triage and contains no admission activity.
- `V0011`: The narrative terminates at IV Antibiotics without admission.
- `V0012`: The narrative terminates at IV Antibiotics without admission.
- `V0013`: The narrative ends with Leucocytes testing and does not involve admission.
- `V0017`: The narrative ends with ER Sepsis Triage and does not contain admission activities.
- `V0019`: The narrative ends with IV Antibiotics and does not involve any patient admission.
- `V0020`: The narrative ends with CRP testing and does not include admission.
- `V0025`: The narrative terminates at IV Antibiotics without any admission activity.
- `V0027`: The narrative does not contain any admission activity, ending at IV Antibiotics.
- `V0029`: The narrative lacks any inpatient admission activity, ending at Leucocytes.
- `V0031`: The narrative does not contain any admission activity.
- `V0034`: The narrative lacks an admission activity, ending at IV Liquid.
- `V0036`: The narrative does not contain any admission activity, ending at CRP.
- `V0038`: The narrative lacks an admission activity, ending at IV Antibiotics.
- `V0043`: The narrative does not contain an admission activity.
- `V0050`: The narrative does not contain any admission activity, ending at CRP.
- `V0056`: The narrative ends at 'IV Antibiotics' and does not contain any inpatient admission activity, so it does not fit any admission category.
- `V0062`: The narrative ends at 'IV Antibiotics' without any inpatient admission, leaving it outside the available categories.
- `V0081`: The narrative does not include any inpatient admission activity, ending at 'IV Liquid'.
- `V0088`: The narrative does not include any inpatient admission activity, ending at 'IV Antibiotics'.
- `V0092`: The narrative does not include any inpatient admission activity, ending at 'LacticAcid'.
- `V0127`: The narrative ends with LacticAcid and does not contain any inpatient admission activities.
- `V0132`: The narrative ends at 'IV Antibiotics' and does not involve any ward or ICU admission.
- `V0133`: The narrative terminates at 'IV Antibiotics' without proceeding to inpatient admission.
- `V0137`: The narrative terminates at diagnostic/treatment steps without any inpatient admission.
- `V0146`: The narrative ends at 'Leucocytes' without any inpatient admission steps.
- `V0148`: The narrative ends at 'IV Antibiotics' without proceeding to inpatient admission.
- `V0187`: The narrative terminates at CRP and does not include any inpatient admission activities.
- `V0197`: The narrative terminates at Leucocytes and does not contain any inpatient admission activities.
- `V0217`: The narrative does not contain any inpatient ward or intensive care admission activity, ending at IV Antibiotics.
- `V0219`: The narrative does not contain any admission activity, ending prematurely at Leucocytes.
- `V0232`: The narrative ends at 'IV Antibiotics' without any inpatient admission activity, so neither admission category is realized.
- `V0234`: The narrative ends at 'Leucocytes' without any inpatient admission activity, so neither admission category is realized.
- `V0260`: The narrative ends at IV Antibiotics without any inpatient admission activity.
- `V0287`: The narrative terminates at CRP and does not include any inpatient admission activity.
- `V0292`: The narrative terminates at Leucocytes and does not include any inpatient admission activity.
- `V0302`: The case stops at ER Sepsis Triage and does not reach any inpatient admission stage.
- `V0305`: The patient's journey ends at IV Antibiotics without inpatient admission.
- `V0322`: The process terminates at IV Antibiotics without any admission activity.
- `V0325`: The patient sequence stops at IV Antibiotics without reaching any ward admission stage.
- `V0330`: The narrative ends at 'IV Liquid' and does not contain any inpatient admission activities.
- `V0342`: The narrative terminates at 'CRP' without any inpatient admission steps.
- `V0349`: The narrative ends at 'ER Sepsis Triage' and contains no admission activities.
- `V0378`: The narrative ends at 'IV Antibiotics' and does not contain any inpatient admission activity.
- `V0379`: The narrative ends at 'IV Antibiotics' and does not contain any inpatient admission activity.
- `V0417`: The narrative lacks any inpatient admission activity, ending prematurely at ER Triage.
- `V0429`: The narrative ends at IV Antibiotics without any inpatient admission activity, so it does not fit any admission category.
- `V0488`: The narrative stops at 'IV Liquid' and does not contain any inpatient admission activity.
- `V0492`: The narrative stops at 'IV Liquid' and does not contain any inpatient admission activity.
- `V0495`: The narrative stops at 'IV Antibiotics' and does not contain any inpatient admission activity.
- `V0507`: The narrative terminates at IV Antibiotics without reaching any inpatient ward admission activity.
- `V0510`: The narrative terminates at IV Antibiotics without reaching any inpatient ward admission activity.
- `V0516`: The narrative terminates at Leucocytes without reaching any inpatient ward admission activity.
- `V0517`: The narrative terminates at ER Triage without reaching any inpatient ward admission activity.
- `V0549`: The narrative does not contain any admission activities, ending instead at IV Liquid.
- `V0575`: The narrative ends at Leucocytes without including any inpatient admission activity, hence it does not realize either admission category.
- `V0580`: The narrative ends at CRP without any inpatient admission activity.
- `V0584`: The narrative ends at IV Liquid without any inpatient admission activity.
- `V0585`: The narrative ends at LacticAcid without any inpatient admission activity.
- `V0587`: The narrative ends at CRP without any inpatient admission activity.
- `V0592`: The narrative ends at IV Antibiotics without any inpatient admission activity.
- `V0645`: The narrative does not contain any inpatient admission activities (Admission NC or Admission IC).
- `V0664`: The narrative does not contain any inpatient admission activities ('Admission NC' or 'Admission IC'), ending instead at IV Liquid.
- `V0676`: The narrative ends with IV Antibiotics and does not include any inpatient ward or intensive care admission.
- `V0679`: The narrative terminates at IV Antibiotics without involving any admission activity.
- `V0685`: The narrative ends at IV Antibiotics and lacks any inpatient or intensive care admission.
- `V0689`: The narrative concludes with IV Antibiotics and contains no admission event.
- `V0694`: The process stops at ER Sepsis Triage without reaching any ward admission.
- `V0713`: The narrative ends at IV Antibiotics without any inpatient ward or ICU admission activity, so neither category is realized.
- `V0750`: The narrative does not contain any inpatient admission activity, hence it falls into the residual.
- `V0759`: The narrative does not contain any admission activity, ending at IV Antibiotics.
- `V0764`: The narrative terminates at ER Sepsis Triage without any admission activity.
- `V0774`: The narrative terminates at ER Sepsis Triage without any admission activity.
- `V0775`: The narrative terminates at CRP without any admission activity.
- `V0777`: The narrative does not contain any inpatient admission activities (ends at Leucocytes).
- `V0778`: The narrative does not contain any inpatient admission activities.
- `V0791`: The narrative does not contain any inpatient admission activities.
- `V0816`: The narrative terminates at IV Antibiotics without involving any inpatient admission activities.
- `V0820`: The narrative terminates at LacticAcid without involving any inpatient admission activities.
- `V0832`: The narrative does not contain any admission activity, ending instead at IV Antibiotics.
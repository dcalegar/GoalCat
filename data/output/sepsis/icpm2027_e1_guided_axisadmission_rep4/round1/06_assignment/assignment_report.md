# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_axisadmission_rep4` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Admission NC (`admission_nc`)

Patient is admitted to a non-critical inpatient ward. This contributes to general inpatient care after stabilization or initial sepsis workup in the emergency department.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared OR alternative Admission NC (id=15), as evidenced by frequent occurrences in standard inpatient paths such as variant V0008, and measured by discharge outcomes.

**Goal-model linkage:** 15 (Task): Admission NC

**Coverage:** macro 670/846 variants (79.2%) · micro 722/1050 cases (68.8%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 9.92, nearest other category `admission_ic` at mean distance 22.55

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.407, nearest other category `admission_ic` at mean distance 0.430

## Admission IC (`admission_ic`)

Patient is admitted to an intensive care inpatient ward. This alternative has a negative contribution link to minimizing time-to-treatment due to higher transfer overhead, but is utilized for severe cases.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared OR alternative Admission IC (id=16), as observed in severe and complex variants like V0605 and V0317.

**Goal-model linkage:** 16 (Task): Admission IC

**Coverage:** macro 88/846 variants (10.4%) · micro 88/1050 cases (8.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 27.48, nearest other category `admission_nc` at mean distance 22.55

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.335, nearest other category `admission_nc` at mean distance 0.430

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

- `V0001`: The process variant ends at ER Sepsis Triage without any hospital admission.
- `V0002`: The process variant only includes ER diagnostic steps (CRP) without any hospital admission.
- `V0003`: The process variant ends with diagnostic tests in the emergency department and does not involve admission.
- `V0004`: The narrative stops at administering IV antibiotics in the emergency setting and lacks admission.
- `V0005`: The narrative ends at LacticAcid testing in the ER without proceeding to an inpatient ward.
- `V0006`: The variant contains ER treatment steps only, without any subsequent inpatient admission.
- `V0007`: The variant represents emergency care and treatment without an admission step.
- `V0009`: The narrative consists entirely of ER-based diagnostic and treatment procedures without ward admission.
- `V0010`: The narrative concludes in the emergency department without an inpatient ward admission.
- `V0011`: The sequence stops at emergency IV antibiotic administration without an admission step.
- `V0012`: The variant is confined to emergency evaluation and treatment steps.
- `V0013`: The narrative concludes with emergency laboratory tests without ward admission.
- `V0017`: The sequence remains entirely within the emergency department.
- `V0019`: The process variant handles the patient entirely in the emergency setting.
- `V0020`: The narrative ends with emergency lab work (CRP) without inpatient admission.
- `V0025`: The process stays in the emergency department throughout the variant.
- `V0027`: The narrative stops at emergency IV antibiotic administration without an admission.
- `V0029`: The process variant is limited to emergency department activities.
- `V0031`: The narrative is confined to emergency department diagnostic and treatment steps.
- `V0034`: The narrative is restricted to emergency care without an inpatient admission.
- `V0036`: The process variant concludes in the emergency department.
- `V0038`: The narrative comprises only emergency department procedures.
- `V0043`: The narrative is confined to emergency diagnostic steps.
- `V0050`: The narrative is limited to emergency department procedures without admission.
- `V0056`: The narrative does not contain any admission activity, ending at IV Antibiotics.
- `V0062`: The narrative does not contain any admission activity, ending at IV Antibiotics.
- `V0081`: The narrative does not contain any admission activity, ending at IV Liquid.
- `V0088`: The narrative does not contain any admission activity, ending at IV Antibiotics.
- `V0092`: The narrative does not contain any admission activity, ending at LacticAcid.
- `V0127`: The narrative ends with LacticAcid and does not contain any ward admission steps.
- `V0132`: The narrative ends with IV Antibiotics and does not contain any ward admission steps.
- `V0133`: The narrative ends with IV Antibiotics and does not contain any ward admission steps.
- `V0137`: The narrative ends with LacticAcid and does not contain any ward admission steps.
- `V0146`: The narrative ends with Leucocytes and does not contain any ward admission steps.
- `V0148`: The narrative ends with IV Antibiotics and does not contain any ward admission steps.
- `V0187`: The narrative does not contain any admission activity, ending prematurely at CRP.
- `V0197`: The narrative lacks any admission activity and ends with Leucocytes.
- `V0217`: The narrative does not contain any inpatient admission activities.
- `V0219`: The narrative does not contain any inpatient admission activities.
- `V0232`: The narrative does not contain any inpatient admission activities.
- `V0234`: The narrative does not contain any inpatient admission activities.
- `V0260`: The narrative terminates at IV Antibiotics without any ward admission activity.
- `V0287`: The narrative terminates at CRP without any ward admission activity.
- `V0292`: The narrative terminates at Leucocytes without any ward admission activity.
- `V0302`: The narrative stops at ER Sepsis Triage and does not include any inpatient ward admission activity.
- `V0305`: The pathway terminates at IV Antibiotics without involving an inpatient ward admission.
- `V0322`: The path ends at IV Antibiotics without any inpatient admission activity.
- `V0325`: The process terminates at IV Antibiotics without an inpatient admission step.
- `V0330`: The sequence ends at IV Liquid and does not progress to any inpatient admission.
- `V0342`: The pathway ends at CRP without reaching an inpatient admission step.
- `V0349`: The pathway terminates at ER Sepsis Triage without progressing to an inpatient admission.
- `V0378`: The narrative terminates before any admission occurs.
- `V0379`: The narrative terminates before any admission occurs.
- `V0417`: The narrative ends at ER Triage without any ward admission activity.
- `V0429`: The narrative terminates at IV Antibiotics without any ward admission activity.
- `V0488`: The narrative ends at IV Liquid and does not contain any inpatient admission activities.
- `V0492`: The narrative ends at IV Liquid without including any inpatient admissions.
- `V0495`: The narrative ends at IV Antibiotics without any inpatient ward admissions.
- `V0507`: The narrative stops at IV Antibiotics without any ward admission activity.
- `V0510`: The narrative ends at IV Antibiotics and does not involve any ward admission.
- `V0516`: The narrative ends at Leucocytes without containing any admission activity.
- `V0517`: The narrative stops at ER Triage and does not feature any inpatient admission.
- `V0549`: The narrative stops at IV Liquid without any inpatient ward admission.
- `V0575`: The narrative stops at diagnostic workup and does not contain an inpatient admission activity.
- `V0580`: The narrative stops at laboratory checks and does not show an inpatient ward admission.
- `V0584`: The narrative ends at IV Liquid without an inpatient admission step.
- `V0585`: The narrative ends at LacticAcid without an inpatient admission step.
- `V0587`: The narrative ends during diagnostics without an inpatient admission step.
- `V0592`: The narrative ends during initial treatment without an inpatient admission step.
- `V0645`: The narrative lacks any admission activity, ending in LacticAcid.
- `V0664`: The narrative stops at IV Liquid without any inpatient admission activity, hence it fits neither non-critical nor intensive care admission.
- `V0676`: The narrative terminates at IV Antibiotics in the ER without any inpatient admission event.
- `V0679`: The narrative terminates at IV Antibiotics without any admission activity.
- `V0685`: The narrative terminates at IV Antibiotics in the ER without any inpatient admission event.
- `V0689`: The narrative terminates at IV Antibiotics without any admission activity.
- `V0694`: The narrative terminates at ER Sepsis Triage without reaching any inpatient admission category.
- `V0713`: The narrative terminates at IV Antibiotics without reaching any inpatient admission category.
- `V0750`: The narrative terminates at IV Antibiotics without reaching any inpatient admission category.
- `V0759`: The narrative ends at IV Antibiotics without any ward admission activity.
- `V0764`: The narrative ends at ER Sepsis Triage without ward admission.
- `V0774`: The narrative ends at ER Sepsis Triage without ward admission.
- `V0775`: The narrative ends at CRP without ward admission.
- `V0777`: The narrative ends at Leucocytes without ward admission.
- `V0778`: The narrative ends at Leucocytes without ward admission.
- `V0791`: The narrative ends at IV Antibiotics without ward admission.
- `V0816`: The process terminates at IV Antibiotics without any inpatient ward admission step.
- `V0820`: The process terminates at LacticAcid without any inpatient ward admission step.
- `V0832`: The process terminates at IV Antibiotics without any inpatient ward admission step.
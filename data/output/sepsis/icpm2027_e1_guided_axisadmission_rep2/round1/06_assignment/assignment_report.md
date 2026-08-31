# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_axisadmission_rep2` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Non-Critical Ward Admission (`admission_nc`)

Represents the patient admission to a non-critical inpatient ward (Admission NC), supporting general treatment flow and aiming for discharge outcomes.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=15 (Admission NC) as observed in frequent sample variants like V0008, where non-critical ward admission leads toward release outcomes such as Release A.

**Goal-model linkage:** 15 (Task): Admission NC

**Coverage:** macro 683/846 variants (80.7%) · micro 735/1050 cases (70.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 10.73, nearest other category `admission_ic` at mean distance 21.28

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.408, nearest other category `admission_ic` at mean distance 0.427

## Intensive Care Ward Admission (`admission_ic`)

Represents the patient admission to an intensive care inpatient ward (Admission IC). This path involves intensive resources and carries a negative contribution (-25) to minimizing time-to-treatment softgoals due to heightened complexity.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=16 (Admission IC). Grounded in evidence from variants like V0605 and V0317 where Admission IC is utilized for complex patient trajectories.

**Goal-model linkage:** 16 (Task): Admission IC

**Coverage:** macro 75/846 variants (8.9%) · micro 75/1050 cases (7.1%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 24.96, nearest other category `admission_nc` at mean distance 21.28

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.338, nearest other category `admission_nc` at mean distance 0.427

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

- `V0001`: This variant ends at ER Sepsis Triage and does not involve any inpatient ward admission.
- `V0002`: This variant only performs diagnostic tests and does not include an inpatient ward admission.
- `V0003`: This variant consists of emergency diagnostics without reaching an inpatient admission stage.
- `V0004`: This variant covers initial emergency treatment and IV antibiotics, but stops before any ward admission.
- `V0005`: This variant represents outpatient or emergency workup without subsequent inpatient admission.
- `V0006`: This variant provides emergency stabilization and antibiotics in the ER without admitting the patient.
- `V0007`: This variant handles acute care and antibiotic administration in the ER without an inpatient admission step.
- `V0009`: This variant concludes with IV antibiotics in the emergency setting and lacks ward admission.
- `V0010`: This variant reflects emergency pathway activities without proceeding to an inpatient ward.
- `V0011`: This variant focuses on emergency treatment and IV antibiotics without an inpatient admission.
- `V0012`: This variant stays entirely within the emergency and diagnostic phase.
- `V0013`: This variant involves preliminary blood tests and diagnostic evaluations without admission.
- `V0017`: This variant is restricted to initial emergency triage and tests.
- `V0019`: This variant finishes with IV antibiotics in the ER phase.
- `V0020`: This variant consists solely of ER diagnostics and initial interventions.
- `V0025`: This variant deals with emergency care and IV antibiotics without an inpatient admission activity.
- `V0027`: This variant stops at IV antibiotics in the emergency setting.
- `V0029`: This variant is limited to emergency diagnostics and lab work.
- `V0031`: This variant concludes with emergency blood work (LacticAcid) without admission.
- `V0034`: This variant only covers emergency procedures and IV fluid administration.
- `V0036`: This variant represents ER-level diagnostics and treatment without admission.
- `V0038`: This variant is restricted to emergency care and IV antibiotics.
- `V0043`: This variant consists purely of emergency lab diagnostics.
- `V0050`: This variant is confined to emergency diagnostic tests without inpatient admission.
- `V0056`: The variant ends at IV Antibiotics without involving any ward admission activity.
- `V0062`: The variant terminates at IV Antibiotics and contains no ward admission step.
- `V0081`: Terminates at IV Liquid without any ward admission activity.
- `V0088`: Terminates at IV Antibiotics without any ward admission activity.
- `V0092`: Terminates at LacticAcid and lacks any ward admission step.
- `V0127`: The narrative does not contain any admission activities, so it fits into the residual.
- `V0132`: The narrative does not contain any admission activities, so it fits into the residual.
- `V0133`: The narrative does not contain any admission activities, so it fits into the residual.
- `V0137`: The narrative does not contain any admission activities, so it fits into the residual.
- `V0146`: The narrative does not contain any admission activities, so it fits into the residual.
- `V0148`: The narrative does not contain any admission activities, so it fits into the residual.
- `V0187`: The narrative does not contain any admission activity, hence it fits neither category.
- `V0197`: The narrative does not contain any admission activity, hence it fits neither category.
- `V0217`: The narrative does not contain any ward admission activities (neither non-critical nor intensive care).
- `V0219`: The narrative ends at Leucocytes without including any ward admission activities.
- `V0232`: The narrative does not contain any ward admission activities.
- `V0234`: The narrative does not contain any ward admission activities.
- `V0260`: The variant ends at IV Antibiotics without reaching any inpatient ward admission activity.
- `V0287`: The variant ends at CRP without reaching any inpatient ward admission activity.
- `V0292`: The variant ends at Leucocytes without reaching any inpatient ward admission activity.
- `V0302`: The narrative stops at ER Sepsis Triage and does not contain any ward admission activity.
- `V0305`: The narrative ends at IV Antibiotics and does not involve any ward admission.
- `V0322`: The narrative stops at IV Antibiotics without any admission events.
- `V0325`: The narrative ends at IV Antibiotics without any admission events.
- `V0330`: The narrative ends at IV Liquid without any admission events.
- `V0342`: The narrative ends at CRP without any ward admission events.
- `V0349`: The narrative ends at ER Sepsis Triage without any admission events.
- `V0378`: The narrative ends at IV Antibiotics without any ward admission activity.
- `V0379`: The narrative ends at IV Antibiotics without any ward admission activity.
- `V0417`: The narrative does not contain any ward admission activities ('Admission NC' or 'Admission IC'), therefore it fits the residual.
- `V0429`: The narrative does not contain any ward admission activities ('Admission NC' or 'Admission IC'), therefore it fits the residual.
- `V0488`: The narrative terminates at IV Liquid without any ward admission activity.
- `V0492`: The narrative terminates at IV Liquid without any ward admission activity.
- `V0495`: The narrative terminates at IV Antibiotics without any ward admission activity.
- `V0507`: The narrative ends with 'IV Antibiotics' and does not contain any ward admission activities.
- `V0510`: The narrative terminates at 'IV Antibiotics' without proceeding to a ward admission.
- `V0516`: The narrative ends at 'Leucocytes' and does not feature any ward admission.
- `V0517`: The narrative terminates at 'ER Triage' and lacks ward admission steps.
- `V0549`: The narrative terminates at 'IV Liquid' without any ward admission activity.
- `V0575`: The narrative ends at Leucocytes without featuring any ward admission activity.
- `V0580`: The variant ends at CRP without any ward admission activity.
- `V0584`: The process stops at IV Liquid and lacks any ward admission event.
- `V0585`: The process terminates at LacticAcid without admission steps.
- `V0587`: The trace ends at CRP without reaching an admission step.
- `V0592`: The process ends at IV Antibiotics without any admission activity.
- `V0645`: The narrative lacks any ward admission event and terminates at LacticAcid.
- `V0664`: The narrative ends at IV Liquid and does not reach any inpatient ward admission category.
- `V0676`: The narrative terminates at IV Antibiotics without reaching any inpatient admission stage.
- `V0679`: The narrative terminates at IV Antibiotics without an inpatient admission activity.
- `V0685`: The narrative terminates at IV Antibiotics without an inpatient admission.
- `V0689`: The narrative terminates at IV Antibiotics without an inpatient admission.
- `V0694`: The narrative terminates at ER Sepsis Triage and does not reach an inpatient admission.
- `V0713`: The narrative terminates at IV Antibiotics without any ward admission activity.
- `V0750`: The narrative terminates at IV Antibiotics without any ward admission activity.
- `V0759`: The narrative ends at IV Antibiotics without any ward admission activity.
- `V0764`: The narrative ends at ER Sepsis Triage without any ward admission.
- `V0774`: The narrative terminates at ER Sepsis Triage without any ward admission activity.
- `V0775`: The narrative terminates at CRP without any ward admission activity.
- `V0777`: The narrative terminates at Leucocytes without any ward admission.
- `V0778`: The narrative terminates at Leucocytes without any ward admission.
- `V0791`: The narrative terminates at IV Antibiotics without any ward admission activity.
- `V0816`: The variant ends at 'IV Antibiotics' without any ward admission activity, so it does not realize either admission category.
- `V0820`: The variant ends at 'LacticAcid' without any ward admission activity, so it does not realize either admission category.
- `V0832`: The variant ends at 'IV Antibiotics' without any ward admission activity, so it does not realize either admission category.
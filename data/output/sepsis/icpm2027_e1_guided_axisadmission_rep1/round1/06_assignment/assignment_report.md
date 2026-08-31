# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_axisadmission_rep1` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Non-Critical Ward Admission (`admission_nc`)

Patient is admitted to a non-critical inpatient ward (Admission NC), supporting general recovery goals.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Admission NC (id=15) under the XOR decomposition of goal id=5. Evidenced in variants such as V0008, where Admission NC leads to ward care without critical unit escalation.

**Goal-model linkage:** 15 (Task): Admission NC

**Coverage:** macro 685/846 variants (81.0%) · micro 737/1050 cases (70.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 10.64, nearest other category `admission_ic` at mean distance 21.91

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.408, nearest other category `admission_ic` at mean distance 0.428

## Intensive Care Ward Admission (`admission_ic`)

Patient is admitted to an intensive care unit (Admission IC), which incurs a negative contribution profile for minimizing time-to-treatment due to heightened acuity.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Admission IC (id=16) under the XOR decomposition of goal id=5. Evidenced in variants like V0605 and V0317, realizing intensive care pathways with associated softgoal impacts.

**Goal-model linkage:** 16 (Task): Admission IC

**Coverage:** macro 73/846 variants (8.6%) · micro 73/1050 cases (7.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 26.66, nearest other category `admission_nc` at mean distance 21.91

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.337, nearest other category `admission_nc` at mean distance 0.428

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

- `V0001`: The narrative stops at ER Sepsis Triage and does not involve admission to a ward.
- `V0002`: The process ends at CRP diagnostics without reaching any ward admission stage.
- `V0003`: The process finishes at Leucocytes and contains no admission activity.
- `V0004`: The trace concludes at IV Antibiotics in the emergency context, with no ward admission.
- `V0005`: The trace ends after LacticAcid diagnostics without inpatient admission.
- `V0006`: Contains emergency interventions ending with IV Antibiotics, lacking an admission event.
- `V0007`: Consists of emergency steps and IV Antibiotics without any ward admission activity.
- `V0009`: Only emergency and diagnostic procedures are performed, without an admission.
- `V0010`: Diagnostic and triage steps only; no inpatient ward admission is present.
- `V0011`: Treatment remains in the emergency/outpatient phase ending with IV Antibiotics.
- `V0012`: Involves acute tests and IV treatment without an admission step.
- `V0013`: Diagnostic sequence ending at Leucocytes without hospital admission.
- `V0017`: Emergency triage and basic labs only, with no ward admission.
- `V0019`: Emergency workup and antibiotics without ward admission.
- `V0020`: Emergency diagnostics and treatment finishing at CRP, without admission.
- `V0025`: Acute care steps only, ending in IV Antibiotics without an admission.
- `V0027`: Emergency assessment and treatment only; no admission event.
- `V0029`: Emergency diagnostics ending with Leucocytes, lacking ward admission.
- `V0031`: Emergency lab tests and acute treatment without ward admission.
- `V0034`: Emergency care pathway ending in IV Liquid without admission.
- `V0036`: Emergency assessment and blood tests only, with no ward admission.
- `V0038`: Emergency treatment sequence ending at IV Antibiotics without admission.
- `V0043`: Emergency laboratory workup ending at LacticAcid without admission.
- `V0050`: Emergency triage and diagnostics ending at CRP without any ward admission.
- `V0056`: The narrative ends at 'IV Antibiotics' without any ward admission activity, so neither category is realized.
- `V0062`: The narrative terminates at 'IV Antibiotics' without any ward admission steps.
- `V0081`: The narrative terminates at 'IV Liquid' without any ward admission activity.
- `V0088`: The narrative ends at 'IV Antibiotics' without any admission steps.
- `V0092`: The narrative terminates at 'LacticAcid' without any ward admission activity.
- `V0127`: The narrative stops at LacticAcid without admission to either ward type.
- `V0132`: The narrative ends at IV Antibiotics without any ward admission.
- `V0133`: The narrative ends at IV Antibiotics without any ward admission.
- `V0137`: The narrative ends at LacticAcid without ward admission.
- `V0146`: The narrative ends at Leucocytes without ward admission.
- `V0148`: The narrative ends at IV Antibiotics without ward admission.
- `V0187`: The narrative stops at CRP and does not include any ward admission event.
- `V0197`: The narrative ends with Leucocytes and does not contain any admission event.
- `V0217`: The variant narrative does not contain any ward admission activity.
- `V0219`: The variant narrative does not contain any ward admission activity.
- `V0232`: The variant narrative does not contain any ward admission activity.
- `V0234`: The variant narrative does not contain any ward admission activity.
- `V0260`: The narrative ends at IV Antibiotics without any ward admission activity, so neither category fits.
- `V0287`: The narrative ends at CRP without any ward admission activity, so neither category fits.
- `V0292`: The narrative ends at Leucocytes without any ward admission activity, so neither category fits.
- `V0302`: The narrative stops at ER Sepsis Triage and does not contain any ward admission activity.
- `V0305`: The variant ends at IV Antibiotics without any admission event.
- `V0322`: The variant ends at IV Antibiotics without any admission event.
- `V0325`: The variant ends at IV Antibiotics without any admission event.
- `V0330`: The variant ends at IV Liquid without any admission event.
- `V0342`: The variant ends at CRP without any ward admission activity.
- `V0349`: The variant ends at ER Sepsis Triage without any ward admission activity.
- `V0378`: The narrative ends at IV Antibiotics without any ward admission activity.
- `V0379`: The narrative ends at IV Antibiotics without any ward admission activity.
- `V0417`: The narrative does not contain any ward admission activities.
- `V0429`: The narrative does not contain any ward admission activities.
- `V0488`: The narrative does not include any ward admission event.
- `V0492`: The narrative does not include any ward admission event.
- `V0495`: The narrative does not include any ward admission event.
- `V0507`: The narrative does not include any ward admission activity corresponding to the taxonomy categories.
- `V0510`: The narrative does not include any ward admission activity corresponding to the taxonomy categories.
- `V0516`: The narrative does not include any ward admission activity corresponding to the taxonomy categories.
- `V0517`: The narrative does not include any ward admission activity corresponding to the taxonomy categories.
- `V0549`: The narrative does not include any ward admission activity corresponding to the taxonomy categories.
- `V0575`: The trace ends without any ward admission activity, so neither category fits.
- `V0580`: The trace terminates at CRP without any ward admission activity.
- `V0584`: The process terminates at IV Liquid without any admission event.
- `V0585`: The process terminates at LacticAcid without any admission event.
- `V0587`: The trace ends at CRP without a ward admission.
- `V0592`: The process ends at IV Antibiotics without reaching a ward admission.
- `V0645`: The narrative does not contain any ward admission steps.
- `V0664`: The narrative terminates at IV Liquid without an inpatient ward admission.
- `V0676`: The narrative terminates at IV Antibiotics without an inpatient ward admission.
- `V0679`: The narrative terminates at IV Antibiotics without an inpatient ward admission.
- `V0685`: The narrative terminates at IV Antibiotics without an inpatient ward admission.
- `V0689`: The narrative terminates at IV Antibiotics without an inpatient ward admission.
- `V0694`: The narrative terminates at ER Sepsis Triage without an inpatient ward admission.
- `V0713`: The narrative ends at IV Antibiotics without involving any ward admission.
- `V0750`: The narrative ends at IV Antibiotics without involving any ward admission.
- `V0759`: The narrative does not contain any admission activity, ending at IV Antibiotics.
- `V0764`: The narrative ends at ER Sepsis Triage without any admission activity.
- `V0774`: The narrative ends at ER Sepsis Triage without any admission activity.
- `V0775`: The narrative ends at CRP without any admission activity.
- `V0777`: The narrative ends at Leucocytes without any admission activity.
- `V0778`: The narrative ends at Leucocytes without any admission activity.
- `V0791`: The narrative ends at IV Antibiotics without any admission activity.
- `V0816`: The variant terminates at IV Antibiotics without any ward admission activity.
- `V0820`: The variant ends at LacticAcid without any inpatient ward admission.
- `V0832`: The variant ends at IV Antibiotics without any admission activity.
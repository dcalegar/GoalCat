# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_axisadmission_rep5` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Non-Critical Admission (`admission_nc`)

Patient is admitted to a non-critical inpatient ward, contributing to standard care flows and tracking against discharge outcomes.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Admission NC (id=15) from the OR decomposition of Goal 5. Observed in multiple variants such as V0008, where it supports patient disposition.

**Goal-model linkage:** 15 (Task): Admission NC

**Coverage:** macro 663/846 variants (78.4%) · micro 715/1050 cases (68.1%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 10.32, nearest other category `admission_ic` at mean distance 20.47

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.408, nearest other category `admission_ic` at mean distance 0.427

## Intensive Care Admission (`admission_ic`)

Patient is admitted to an intensive care inpatient ward, introducing a negative contribution to minimizing time-to-treatment due to specialized routing.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Admission IC (id=16) from the OR decomposition of Goal 5. Associated with softgoal trade-offs (SomeNegative contribution to time-to-treatment) and observed in complex variants such as V0605 and V0317.

**Goal-model linkage:** 16 (Task): Admission IC

**Coverage:** macro 95/846 variants (11.2%) · micro 95/1050 cases (9.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 23.22, nearest other category `admission_nc` at mean distance 20.47

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.329, nearest other category `admission_nc` at mean distance 0.427

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

- `V0001`: The narrative stops at ER Sepsis Triage and does not contain any admission activity.
- `V0002`: The sequence ends at CRP without any inpatient admission.
- `V0003`: The sequence ends at Leucocytes without an inpatient ward admission.
- `V0004`: The variant concludes with IV Antibiotics in the ER phase, lacking admission.
- `V0005`: The narrative finishes at LacticAcid without any admission step.
- `V0006`: The variant consists of ER diagnostics and treatment without an admission step.
- `V0007`: Contains ER diagnostics and IV Antibiotics but no ward admission.
- `V0009`: Process completes with IV Antibiotics and does not feature an admission event.
- `V0010`: Sequence of ER steps without any inpatient admission.
- `V0011`: ER diagnostics and treatment only; no admission recorded.
- `V0012`: Concludes with IV Antibiotics in the ER without admission.
- `V0013`: Stops at Leucocytes evaluation in the ER.
- `V0017`: ER triage and diagnostic labs only, with no ward admission.
- `V0019`: ER phase treatments and diagnostics only, no admission step.
- `V0020`: Stops at CRP diagnostic without any admission.
- `V0025`: ER workflow without inpatient admission.
- `V0027`: ER diagnostic and treatment process without admission.
- `V0029`: ER-based diagnostic sequence without admission.
- `V0031`: ER treatment sequence without any admission event.
- `V0034`: ER treatment and liquid administration without admission.
- `V0036`: ER diagnostic sequence without inpatient admission.
- `V0038`: ER treatment workflow without admission.
- `V0043`: ER diagnostics only, no ward admission.
- `V0050`: ER diagnostic workflow without inpatient admission.
- `V0056`: The variant ends at IV Antibiotics without any admission activity, so it fits neither admission category.
- `V0062`: The variant ends at IV Antibiotics without any admission activity, so it fits neither admission category.
- `V0081`: The variant ends at IV Liquid without any admission activity, so it fits neither admission category.
- `V0088`: The variant ends at IV Antibiotics without any admission activity, so it fits neither admission category.
- `V0092`: The variant ends at LacticAcid without any admission activity, so it fits neither admission category.
- `V0127`: The process variant stops at LacticAcid without admission and does not fit any admission category.
- `V0132`: The process variant stops at IV Antibiotics and does not fit any admission category.
- `V0133`: The process variant stops at IV Antibiotics and does not fit any admission category.
- `V0137`: The process variant ends at LacticAcid without any inpatient admission.
- `V0146`: The process variant stops at Leucocytes without admission and does not fit any admission category.
- `V0148`: The process variant stops at IV Antibiotics without admission and does not fit any admission category.
- `V0187`: The narrative does not contain any admission activity, so it does not fit either taxonomy category.
- `V0197`: The narrative does not contain any admission activity, so it does not fit either taxonomy category.
- `V0217`: The narrative ends at IV Antibiotics without any admission activity, hence it does not realize either admission category.
- `V0219`: The narrative terminates at Leucocytes without an admission event.
- `V0232`: The narrative stops at IV Antibiotics with no admission step.
- `V0234`: The narrative ends at Leucocytes without an admission step.
- `V0260`: The process terminates at IV Antibiotics without involving any ward admission step, thus fitting neither category.
- `V0287`: The process terminates at CRP without involving any ward admission step, thus fitting neither category.
- `V0292`: The process terminates at Leucocytes without involving any ward admission step, thus fitting neither category.
- `V0302`: The narrative stops at ER Sepsis Triage and does not contain any admission activity.
- `V0305`: The narrative ends at IV Antibiotics and lacks any admission step.
- `V0322`: The narrative ends at IV Antibiotics without any admission step.
- `V0325`: The narrative ends at IV Antibiotics without an admission step.
- `V0330`: The narrative ends at IV Liquid without an admission step.
- `V0342`: The narrative ends at CRP without any admission step.
- `V0349`: The narrative ends at ER Sepsis Triage and does not contain any admission step.
- `V0378`: The narrative does not contain any admission activity, so neither category fits.
- `V0379`: The narrative does not contain any admission activity, so neither category fits.
- `V0417`: The narrative does not contain any admission activity, ending at ER Triage; thus, no category fits.
- `V0429`: The narrative ends at IV Antibiotics without any admission activity; thus, no category fits.
- `V0488`: The narrative does not include any inpatient ward admission event.
- `V0492`: The narrative does not include any inpatient ward admission event.
- `V0495`: The narrative does not include any inpatient ward admission event.
- `V0507`: The narrative does not contain any admission activity, hence it does not realize either category.
- `V0510`: The narrative does not contain any admission activity, hence it does not realize either category.
- `V0516`: The narrative does not contain any admission activity, hence it does not realize either category.
- `V0517`: The narrative does not contain any admission activity, hence it does not realize either category.
- `V0549`: The narrative does not contain any admission activity, hence it does not realize either category.
- `V0575`: The variant terminates in an early diagnostic phase and does not reach any ward admission category.
- `V0580`: Terminates at CRP testing without reaching any inpatient admission category.
- `V0584`: Terminates during IV liquid treatment without reaching an inpatient admission.
- `V0585`: Terminates at LacticAcid test without reaching an inpatient admission.
- `V0587`: Terminates at diagnostic testing without reaching any inpatient admission category.
- `V0592`: Terminates during initial treatment and diagnostic steps without reaching an admission.
- `V0645`: The narrative does not contain any admission activity, making it part of the residual.
- `V0664`: The narrative does not contain any admission activity, hence it belongs to the residual.
- `V0676`: The narrative does not contain any admission activity, hence it belongs to the residual.
- `V0679`: The narrative does not contain any admission activity, hence it belongs to the residual.
- `V0685`: The narrative does not contain any admission activity, hence it belongs to the residual.
- `V0689`: The narrative does not contain any admission activity, hence it belongs to the residual.
- `V0694`: The narrative does not contain any admission activity, hence it belongs to the residual.
- `V0713`: The process terminates at IV Antibiotics without any ward admission activity.
- `V0750`: The narrative terminates at IV Antibiotics without any ward admission activity.
- `V0759`: The narrative ends at IV Antibiotics without any admission activity, so it does not fit either admission category.
- `V0764`: The narrative ends at ER Sepsis Triage without any admission activity, so it does not fit either admission category.
- `V0774`: The narrative ends at ER Sepsis Triage without any admission activity, so it does not fit either admission category.
- `V0775`: The narrative ends at CRP without any admission activity, so it does not fit either admission category.
- `V0777`: The narrative ends at Leucocytes without any admission activity, so it does not fit either admission category.
- `V0778`: The narrative ends at Leucocytes without any admission activity, so it does not fit either admission category.
- `V0791`: The narrative ends at IV Antibiotics without any admission activity, so it does not fit either admission category.
- `V0816`: The narrative ends at IV Antibiotics without inpatient admission, making neither category fit.
- `V0820`: The narrative terminates at LacticAcid without any inpatient admission.
- `V0832`: The narrative ends at IV Antibiotics without any inpatient admission.
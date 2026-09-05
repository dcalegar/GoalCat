# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_axisadmission_rep1` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Non-Critical Admission (`admission_nc`)

Admission of the patient to a non-critical inpatient ward (Admission NC), realizing the goal of admitting an inpatient for ongoing management and eventual discharge.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative id=15 (Admission NC). The narrative sample shows patients routed to Admission NC in standard pathways (e.g. V0008, V0070), supporting the non-critical admission track. It does not warrant further subdivision as the logged activity cleanly realizes the non-critical care alternative.

**Goal-model linkage:** 15 (Task): Admission NC

**Coverage:** macro 669/846 variants (79.1%) · micro 721/1050 cases (68.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 10.83, nearest other category `admission_ic` at mean distance 19.40

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.407, nearest other category `admission_ic` at mean distance 0.428

## Intensive Care Admission (`admission_ic`)

Admission of the patient to an intensive care inpatient unit (Admission IC), realizing the goal of inpatient admission with higher-acuity care. This alternative has a negative contribution (-25) to minimizing time-to-treatment softgoals due to resource constraints or stabilization overhead.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative id=16 (Admission IC). The narrative sample shows this alternative taken in complex or severe cases (e.g., V0605, V0317), reflecting intensive ward routing rather than standard non-critical admission.

**Goal-model linkage:** 16 (Task): Admission IC

**Coverage:** macro 89/846 variants (10.5%) · micro 89/1050 cases (8.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 21.37, nearest other category `admission_nc` at mean distance 19.40

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.339, nearest other category `admission_nc` at mean distance 0.428

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

- `V0001`: The narrative stops at ER Sepsis Triage and does not involve any inpatient admission.
- `V0002`: The narrative only covers initial diagnostics (CRP, Leucocytes) and does not involve an inpatient admission.
- `V0003`: The narrative concludes with lab tests and does not contain any inpatient admission activity.
- `V0004`: The narrative ends with the administration of IV Antibiotics in the emergency/outpatient phase without admission.
- `V0005`: The narrative only contains triage and lab diagnostics without any subsequent ward admission.
- `V0006`: The variant involves emergency treatment and IV antibiotics, but no inpatient admission step is recorded.
- `V0007`: The narrative stops at emergency treatment with IV antibiotics and contains no admission event.
- `V0009`: The narrative covers ER diagnostics and IV antibiotics but lacks an inpatient admission step.
- `V0010`: The narrative consists solely of initial ER screening and tests without any inpatient admission.
- `V0011`: The narrative ends after administering IV antibiotics in the emergency setting without an admission event.
- `V0012`: The process sequence finishes with IV Antibiotics and does not proceed to an inpatient admission.
- `V0013`: The narrative is restricted to emergency diagnostic tests and does not contain an inpatient admission.
- `V0017`: The narrative is limited to ER assessment activities and does not include any inpatient admission.
- `V0019`: The narrative concludes with IV antibiotics and does not contain an admission step.
- `V0020`: The narrative stops at diagnostic workup in the ER without proceeding to an inpatient admission.
- `V0025`: The narrative ends with IV Antibiotics and does not include an inpatient admission activity.
- `V0027`: The variant ends in 'IV Antibiotics' without proceeding to inpatient admission.
- `V0029`: The variant ends in 'Leucocytes' without proceeding to inpatient admission.
- `V0031`: The variant terminates at 'LacticAcid' without inpatient admission.
- `V0034`: The variant terminates at 'IV Liquid' without inpatient admission.
- `V0036`: The variant terminates at 'CRP' without inpatient admission.
- `V0038`: The variant terminates at 'IV Antibiotics' without inpatient admission.
- `V0043`: The variant terminates at 'LacticAcid' without inpatient admission.
- `V0050`: The variant terminates at 'CRP' without inpatient admission.
- `V0056`: The narrative terminates at 'IV Antibiotics' without any inpatient admission activity.
- `V0062`: The narrative terminates at 'IV Antibiotics' without any inpatient admission activity.
- `V0081`: The narrative ends with 'IV Liquid' and contains no admission activity.
- `V0088`: The narrative ends with 'IV Antibiotics' and contains no admission activity.
- `V0092`: The narrative ends with 'LacticAcid' and contains no admission activity.
- `V0127`: The narrative ends with 'LacticAcid' and does not contain any inpatient admission activities.
- `V0132`: The narrative ends at 'IV Antibiotics' without proceeding to any inpatient admission.
- `V0133`: The narrative ends at 'IV Antibiotics' without inpatient admission.
- `V0137`: The narrative finishes at 'LacticAcid' without any inpatient admission steps.
- `V0146`: The narrative ends at 'Leucocytes' without any inpatient admission.
- `V0148`: The narrative ends at 'IV Antibiotics' without inpatient admission.
- `V0187`: The narrative does not contain any inpatient admission activity, so it does not realize either category.
- `V0197`: The narrative does not contain any inpatient admission activity, so it does not realize either category.
- `V0217`: The narrative lacks any admission activity, ending at IV Antibiotics without inpatient admission.
- `V0219`: The narrative lacks any admission activity, ending at Leucocytes without inpatient admission.
- `V0232`: The narrative ends at IV Antibiotics without any inpatient admission activity.
- `V0234`: The narrative terminates at Leucocytes without reaching any admission goal.
- `V0260`: The narrative ends at IV Antibiotics without any inpatient admission activity, so neither category fits.
- `V0287`: The narrative ends at CRP and does not contain any admission activity.
- `V0292`: The narrative ends at Leucocytes and does not contain any admission activity.
- `V0302`: The process stops at 'ER Sepsis Triage' and does not reach any inpatient admission stage.
- `V0305`: The process ends at 'IV Antibiotics' without proceeding to inpatient admission.
- `V0322`: The process stops at 'IV Antibiotics' without proceeding to inpatient admission.
- `V0325`: The process stops at 'IV Antibiotics' without proceeding to inpatient admission.
- `V0330`: The narrative ends at 'IV Liquid' and does not contain any inpatient admission activities.
- `V0342`: The narrative ends at 'CRP' and does not contain any inpatient admission activities.
- `V0349`: The narrative ends at 'ER Sepsis Triage' and does not contain any inpatient admission activities.
- `V0378`: The narrative ends at 'IV Antibiotics' without any inpatient admission activity, hence it belongs to the residual.
- `V0379`: The narrative ends at 'IV Antibiotics' without any inpatient admission activity, hence it belongs to the residual.
- `V0417`: The narrative does not contain any admission activity, ending instead at ER Triage, so it does not realize either admission category.
- `V0429`: The narrative ends with 'IV Antibiotics' and does not contain any inpatient admission activities.
- `V0488`: The narrative stops at IV Liquid without any inpatient admission activity, so it does not realize either admission category.
- `V0492`: The process terminates without any admission activity, hence it fits neither category.
- `V0495`: The case ends at IV Antibiotics without any inpatient admission, so no category is realized.
- `V0507`: The narrative ends at 'IV Antibiotics' without proceeding to inpatient admission.
- `V0510`: The narrative ends at 'IV Antibiotics' without proceeding to inpatient admission.
- `V0516`: The narrative terminates at diagnostic labs without reaching an admission goal.
- `V0517`: The narrative terminates early at ER Triage without reaching any admission goal.
- `V0549`: The narrative ends at IV Liquid and does not include any inpatient admission activity, hence it fits neither category.
- `V0575`: The narrative terminates at Leucocytes without reaching any inpatient admission activity, hence it fits neither admission category.
- `V0580`: The narrative does not contain any inpatient admission activities (Admission NC or Admission IC), so it belongs to the residual.
- `V0584`: The narrative lacks any inpatient admission activities, thus falling into the residual.
- `V0585`: The narrative lacks any inpatient admission activities, thus falling into the residual.
- `V0587`: The narrative lacks any inpatient admission activities, thus falling into the residual.
- `V0592`: The narrative lacks any inpatient admission activities, thus falling into the residual.
- `V0645`: The narrative lacks any explicit inpatient admission activity ('Admission NC' or 'Admission IC'), thus falling into the residual category.
- `V0664`: The narrative terminates at 'IV Liquid' without any inpatient admission activity.
- `V0676`: The narrative ends at IV Antibiotics without any inpatient admission activity.
- `V0679`: The narrative terminates at IV Antibiotics without any inpatient admission steps.
- `V0685`: The narrative ends at IV Antibiotics without any admission activity.
- `V0689`: The narrative ends at IV Antibiotics without any inpatient admission activity.
- `V0694`: The narrative terminates early at ER Sepsis Triage without any admission or discharge activities.
- `V0713`: The narrative does not contain any admission activity, ending at IV Antibiotics in the ER.
- `V0750`: The narrative ends at IV Antibiotics without any inpatient admission activity, hence it falls into the residual.
- `V0759`: The narrative ends at IV Antibiotics without any inpatient admission activity, hence no category fits.
- `V0764`: The narrative terminates at ER Sepsis Triage without reaching any inpatient admission category.
- `V0774`: The narrative terminates at ER Sepsis Triage without reaching any inpatient admission category.
- `V0775`: The narrative ends at CRP without any inpatient admission activity.
- `V0777`: The narrative ends at Leucocytes and does not contain any admission activity.
- `V0778`: The narrative ends at Leucocytes without involving any inpatient admission.
- `V0791`: The narrative ends at IV Antibiotics without any admission activity.
- `V0816`: The narrative terminates at 'IV Antibiotics' without any inpatient admission activity, hence it falls into the residual.
- `V0820`: The narrative ends with 'LacticAcid' and contains no admission activity, placing it in the residual.
- `V0832`: The narrative ends in IV Antibiotics without any inpatient admission activity, so neither admission category fits.
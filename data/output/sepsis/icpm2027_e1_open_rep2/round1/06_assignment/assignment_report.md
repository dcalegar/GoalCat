# Step 6 — Narrative assignment report

Run: `icpm2027_e1_open_rep2` | Log: `sepsis` | Taxonomy mode: `open` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Rapid Triage and Outpatient Discharge (`rapid_triage_and_discharge`)

Short diagnostic pathways characterized by fast ER registration, triage, and immediate laboratory workups (CRP, Leucocytes, LacticAcid) resulting in rapid discharge or completion of the initial emergency visit without admission.

**Taxonomy-derivation rationale (Step 5):** Groups fast, low-complexity variants with short trace lengths and quick durations ending in early triage or initial test outcomes.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 54/846 variants (6.4%) · micro 160/1050 cases (15.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.52, nearest other category `acute_medical_intervention` at mean distance 4.96

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.484, nearest other category `acute_medical_intervention` at mean distance 0.460

## Acute Medical Intervention (`acute_medical_intervention`)

Pathways featuring comprehensive emergency evaluation followed by prompt fluid resuscitation and intravenous antibiotic administration, indicating active treatment of suspected sepsis in the emergency department.

**Taxonomy-derivation rationale (Step 5):** Captures standard, moderately-paced clinical pathways where patients receive targeted IV interventions after standard blood work.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 46/846 variants (5.4%) · micro 93/1050 cases (8.9%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.88, nearest other category `rapid_triage_and_discharge` at mean distance 4.96

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.403, nearest other category `rapid_triage_and_discharge` at mean distance 0.460

## Inpatient Admission and Planned Release (`inpatient_admission_and_release`)

Process variants where patients are admitted to nursing care (NC) or intensive care (IC) units following initial stabilization and treatment, eventually leading to successful release variants (Release A, B, C, or D).

**Taxonomy-derivation rationale (Step 5):** Represents the standard inpatient lifecycle from emergency arrival through ward admission to eventual discharge.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 467/846 variants (55.2%) · micro 505/1050 cases (48.1%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 8.93, nearest other category `acute_medical_intervention` at mean distance 9.13

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.365, nearest other category `extended_chronic_rework` at mean distance 0.440

## Extended Stay with Chronic Rework and Readmission (`extended_chronic_rework`)

Extremely long, highly complex process variants characterized by extensive repetition of laboratory tests and ward admissions, frequently culminating in patient readmission or long-term hospital stays.

**Taxonomy-derivation rationale (Step 5):** Isolates outlier and extreme cases marked by massive trace lengths, severe rework loops, and high durations.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 261/846 variants (30.9%) · micro 274/1050 cases (26.1%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 18.08, nearest other category `inpatient_admission_and_release` at mean distance 14.97

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.315, nearest other category `inpatient_admission_and_release` at mean distance 0.440

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0497` / `V0710` (category `extended_chronic_rework`): structural=180, profile=0.751
- `V0686` / `V0710` (category `extended_chronic_rework`): structural=179, profile=0.683
- `V0101` / `V0710` (category `extended_chronic_rework`): structural=178, profile=0.522
- `V0104` / `V0710` (category `extended_chronic_rework`): structural=178, profile=0.673
- `V0110` / `V0710` (category `extended_chronic_rework`): structural=178, profile=0.677
- `V0242` / `V0710` (category `extended_chronic_rework`): structural=178, profile=0.585
- `V0614` / `V0710` (category `extended_chronic_rework`): structural=178, profile=0.677
- `V0650` / `V0710` (category `extended_chronic_rework`): structural=178, profile=0.601
- `V0710` / `V0823` (category `extended_chronic_rework`): structural=178, profile=0.690
- `V0033` / `V0710` (category `extended_chronic_rework`): structural=177, profile=0.597

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0004` (`acute_medical_intervention`) / `V0679` (`rapid_triage_and_discharge`): structural=1, profile=0.024
- `V0008` (`inpatient_admission_and_release`) / `V0686` (`extended_chronic_rework`): structural=1, profile=0.454
- `V0008` (`inpatient_admission_and_release`) / `V0706` (`rapid_triage_and_discharge`): structural=1, profile=0.029
- `V0008` (`inpatient_admission_and_release`) / `V0707` (`rapid_triage_and_discharge`): structural=1, profile=0.425
- `V0011` (`acute_medical_intervention`) / `V0502` (`inpatient_admission_and_release`): structural=1, profile=0.344
- `V0011` (`acute_medical_intervention`) / `V0510` (`rapid_triage_and_discharge`): structural=1, profile=0.019
- `V0011` (`acute_medical_intervention`) / `V0679` (`rapid_triage_and_discharge`): structural=1, profile=0.002
- `V0012` (`acute_medical_intervention`) / `V0510` (`rapid_triage_and_discharge`): structural=1, profile=0.041
- `V0012` (`acute_medical_intervention`) / `V0645` (`rapid_triage_and_discharge`): structural=1, profile=0.745
- `V0013` (`rapid_triage_and_discharge`) / `V0713` (`acute_medical_intervention`): structural=1, profile=0.398

## Residual

18/846 variants (2.1%), 18/1050 cases (1.7%) unassigned.

- `V0092`: Incomplete pathway ending in LacticAcid without admission or release, fitting none of the completed categories.
- `V0268`: The variant ends abruptly on a Leucocytes event rather than completing a discharge, release, or standard terminal milestone.
- `V0287`: Incomplete pathway ending at initial diagnostic workup without admission or discharge sequence.
- `V0292`: Terminates early at diagnostic test without treatment, admission, or discharge.
- `V0295`: Variant ends abruptly during IV antibiotics administration without admission or release steps.
- `V0342`: Incomplete or atypical pathway ending prematurely at a CRP laboratory activity without reaching an intervention, admission, or discharge outcome.
- `V0349`: Abnormal sequence starting directly with lab tests out-of-order and terminating at ER Sepsis Triage without standard emergency care flow.
- `V0365`: The variant ends in repeated laboratory tests rather than an admission or discharge, making it an incomplete or non-standard trajectory.
- `V0374`: Terminates abruptly with repeated lab tests while still admitted, not fitting standard completion patterns.
- `V0417`: Does not fit standard categories as it loops back to ER triage instead of leading to discharge or admission.
- `V0516`: The process sequence is highly atypical and disordered (beginning with ER Sepsis Triage and ending abruptly at Leucocytes), failing to cleanly fit standard diagnostic or inpatient categories.
- `V0694`: Variant terminates prematurely at ER Sepsis Triage and does not fit any complete pathway category.
- `V0727`: The patient is admitted and released, but then returns to the ER after an extended period, which does not fit neatly into simple discharge, acute intervention, standard inpatient release, or extended chronic rework without ambiguity.
- `V0734`: The variant culminates in a return to the ER after a long duration, making it a readmission case that doesn't cleanly fit standard planned single admissions.
- `V0764`: Incomplete pathway terminating abruptly at ER Sepsis Triage without completion of treatment or admission.
- `V0772`: Incomplete pathway ending prematurely on a CRP activity without a final release or admission outcome.
- `V0774`: Truncated sequence ending early at ER Sepsis Triage without reaching any treatment or discharge milestone.
- `V0775`: Incomplete pathway terminating at a repeated CRP activity without progressing to admission or discharge.
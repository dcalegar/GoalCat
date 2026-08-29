# Step 6 — Narrative assignment report

Run: `icpm2027_e1_open_rep2` | Log: `sepsis` | Taxonomy mode: `open` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Fast ER Triage Only (`fast_er_triage_only`)

Short, rapid sequences that terminate immediately after initial ER registration and triage or basic lab work (CRP/Leucocytes) without progressing to intensive interventions or hospital admission.

**Taxonomy-derivation rationale (Step 5):** These variants represent low-acuity or fast-exit cases with durations under 30 minutes and minimal trace lengths, distinct from admitted or treated patients.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 57/846 variants (6.7%) · micro 161/1050 cases (15.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.62, nearest other category `standard_acute_intervention` at mean distance 4.86

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.463, nearest other category `standard_acute_intervention` at mean distance 0.433

## Standard Acute Intervention (`standard_acute_intervention`)

Moderately long pathways involving standard sepsis diagnostic labs (CRP, Leucocytes, LacticAcid) followed by active medical treatment such as IV fluids and IV antibiotics.

**Taxonomy-derivation rationale (Step 5):** Represents the standard clinical pathway for acute sepsis management where patients receive timely stabilization and therapeutic intervention.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 31/846 variants (3.7%) · micro 79/1050 cases (7.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.46, nearest other category `fast_er_triage_only` at mean distance 4.86

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.338, nearest other category `fast_er_triage_only` at mean distance 0.433

## Hospital Admission and Release (`hospital_admission_and_release`)

Pathways featuring formal ward admission (Admission NC or IC) following acute stabilization, culminating in a successful discharge or release after a few days.

**Taxonomy-derivation rationale (Step 5):** Captures inpatient care trajectories that require observation or treatment on a nursing care or intensive care unit before final release.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 425/846 variants (50.2%) · micro 462/1050 cases (44.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 9.53, nearest other category `standard_acute_intervention` at mean distance 9.80

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.285, nearest other category `chronic_extended_rework` at mean distance 0.391

## Chronic Extended Rework (`chronic_extended_rework`)

Extremely long, highly repetitive sequences characterized by persistent cyclical lab tests (CRP, Leucocytes, LacticAcid) and repeated ward transfers or readmissions over weeks or months.

**Taxonomy-derivation rationale (Step 5):** Significantly deviates from standard flows through massive trace lengths and high frequencies of internal rework, reflecting complex or deteriorating patient conditions.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 32/846 variants (3.8%) · micro 32/1050 cases (3.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 38.59, nearest other category `hospital_admission_and_release` at mean distance 34.57

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.366, nearest other category `hospital_admission_and_release` at mean distance 0.391

## Readmission / Return to ER (`readmission_return_er`)

Pathways where patients are initially treated or released but experience complications resulting in a return visit or readmission to the emergency department.

**Taxonomy-derivation rationale (Step 5):** Identifies a specific adverse outcome trajectory where post-discharge care fails or complications arise, leading to repeat emergency utilization.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 274/846 variants (32.4%) · micro 289/1050 cases (27.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.61, nearest other category `hospital_admission_and_release` at mean distance 11.54

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.180, nearest other category `chronic_extended_rework` at mean distance 0.449

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0365` / `V0710` (category `chronic_extended_rework`): structural=170, profile=0.558
- `V0548` / `V0710` (category `chronic_extended_rework`): structural=169, profile=0.415
- `V0683` / `V0710` (category `chronic_extended_rework`): structural=169, profile=0.476
- `V0538` / `V0710` (category `chronic_extended_rework`): structural=167, profile=0.470
- `V0673` / `V0710` (category `chronic_extended_rework`): structural=167, profile=0.493
- `V0710` / `V0813` (category `chronic_extended_rework`): structural=164, profile=0.558
- `V0317` / `V0350` (category `readmission_return_er`): structural=163, profile=0.352
- `V0317` / `V0497` (category `readmission_return_er`): structural=163, profile=0.403
- `V0317` / `V0828` (category `readmission_return_er`): structural=163, profile=0.343
- `V0598` / `V0710` (category `chronic_extended_rework`): structural=163, profile=0.456

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0004` (`standard_acute_intervention`) / `V0679` (`fast_er_triage_only`): structural=1, profile=0.024
- `V0004` (`standard_acute_intervention`) / `V0713` (`fast_er_triage_only`): structural=1, profile=0.044
- `V0007` (`standard_acute_intervention`) / `V0040` (`hospital_admission_and_release`): structural=1, profile=0.336
- `V0008` (`hospital_admission_and_release`) / `V0686` (`readmission_return_er`): structural=1, profile=0.454
- `V0011` (`standard_acute_intervention`) / `V0417` (`fast_er_triage_only`): structural=1, profile=0.707
- `V0011` (`standard_acute_intervention`) / `V0502` (`hospital_admission_and_release`): structural=1, profile=0.344
- `V0011` (`standard_acute_intervention`) / `V0679` (`fast_er_triage_only`): structural=1, profile=0.002
- `V0012` (`standard_acute_intervention`) / `V0645` (`fast_er_triage_only`): structural=1, profile=0.745
- `V0015` (`hospital_admission_and_release`) / `V0116` (`readmission_return_er`): structural=1, profile=0.429
- `V0016` (`hospital_admission_and_release`) / `V0052` (`readmission_return_er`): structural=1, profile=0.429

## Residual

27/846 variants (3.2%), 27/1050 cases (2.6%) unassigned.

- `V0127`: Stops prematurely at LacticAcid without progressing to intensive interventions, admission, or standard release.
- `V0132`: Terminates immediately after IV Antibiotics without progressing to admission or release.
- `V0133`: Terminates at IV Antibiotics without reaching ward admission or release.
- `V0137`: Ends with LacticAcid repeating without progressing to admission or discharge.
- `V0146`: Terminates prematurely at Leucocytes without admission or release.
- `V0181`: Does not fit standard categories due to anomalous ending activity ('Leucocytes') after a prior release.
- `V0260`: Terminates early at IV Antibiotics without proceeding to hospital admission or being a simple triage-only case.
- `V0268`: Terminates at a repeated Leucocytes test after admission without reaching a final discharge or other defined terminal event.
- `V0295`: Unusual ordering where IV treatment occurs late after admission, not fitting the standard acute intervention or other standard patterns cleanly.
- `V0336`: The sequence terminates at a CRP lab measurement without progressing to admission or discharge, placing it outside the standard categories.
- `V0342`: The pathway ends abruptly after a repeating CRP activity without advancing to admission or discharge.
- `V0368`: Terminates early at Admission NC without showing complete release or long-term rework.
- `V0374`: Terminates mid-sequence with repetitive lab testing without reaching admission, release, or ER return.
- `V0378`: Terminates early at IV Antibiotics without progressing to admission or release.
- `V0379`: Terminates early at IV Antibiotics without advancing to ward admission or release.
- `V0462`: The pathway terminates with repeated CRP labs rather than progressing to a full admission or release outcome.
- `V0636`: Does not fit any category because it terminates abnormally with a lab activity ('LacticAcid') instead of an ER triage termination, release, or return.
- `V0644`: Incomplete or truncated sequence ending in a lab test ('CRP') without reaching a terminal outcome like release or return.
- `V0654`: The outcome terminates abruptly with a lab test (Leucocytes) rather than standard release, admission, or return, leaving it outside the standard categories.
- `V0664`: Incomplete or truncated pathway ending with IV Liquid without progressing to discharge, admission, or full acute treatment.
- `V0703`: Terminates with IV Liquid rather than a standard discharge or completion event, fitting no specific category well.
- `V0707`: Short sequence terminating abruptly at Admission NC without showing full ward stay and release.
- `V0708`: Terminates at IV Antibiotics without admission or release.
- `V0772`: The pathway terminates unexpectedly at a repeat CRP lab without a formal release or admission outcome.
- `V0775`: Terminates at repeat CRP testing without reaching an admission or release outcome.
- `V0826`: The variant terminates abruptly at Admission NC without showing a subsequent release or full intervention cycle fitting the standard categories.
- `V0843`: Terminates unusually with IV Liquid after admission, not fitting the standard outcomes cleanly.
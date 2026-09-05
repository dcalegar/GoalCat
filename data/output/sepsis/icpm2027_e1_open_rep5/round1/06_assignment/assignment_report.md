# Step 6 — Narrative assignment report

Run: `icpm2027_e1_open_rep5` | Log: `sepsis` | Taxonomy mode: `open` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Rapid Assessment and Triage (`rapid_assessment_triage`)

Short, fast-tracked patient encounters consisting strictly of initial registration, triage, and basic blood work or diagnostics without admission or intensive intervention, resulting in quick release or completion within minutes.

**Taxonomy-derivation rationale (Step 5):** Groups low-duration, low-length variants where patients undergo immediate screening and initial diagnostic labs (CRP, Leucocytes) and are resolved rapidly.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 54/846 variants (6.4%) · micro 157/1050 cases (15.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.25, nearest other category `acute_emergency_treatment` at mean distance 5.10

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.459, nearest other category `acute_emergency_treatment` at mean distance 0.491

## Acute Emergency Treatment (`acute_emergency_treatment`)

Patient paths that involve immediate stabilization via IV fluids and IV antibiotics following triage and lab work, representing acute medical management within the emergency setting.

**Taxonomy-derivation rationale (Step 5):** Characterized by moderate duration and intermediate trace lengths where administration of IV fluids and antibiotics is the core intervention.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 57/846 variants (6.7%) · micro 106/1050 cases (10.1%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.20, nearest other category `rapid_assessment_triage` at mean distance 5.10

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.465, nearest other category `rapid_assessment_triage` at mean distance 0.491

## Inpatient Admission and Recovery (`inpatient_admission_recovery`)

Encounters requiring formal hospital admission (NC or IC) following initial emergency stabilization and diagnostics, ultimately culminating in a successful discharge or release category.

**Taxonomy-derivation rationale (Step 5):** Captured by variants showing transition from ER activities to ward admissions (Admission NC/IC) and subsequent releases (Release A, B, C, D).

**Goal-model linkage:** (no goal model)

**Coverage:** macro 371/846 variants (43.9%) · micro 401/1050 cases (38.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 8.49, nearest other category `acute_emergency_treatment` at mean distance 8.81

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.309, nearest other category `chronic_rework_readmission` at mean distance 0.476

## Chronic Rework and Readmission (`chronic_rework_readmission`)

Complex, highly prolonged variants featuring extensive repetition of diagnostic tests (CRP, Leucocytes, LacticAcid) and ward readmissions, frequently ending in a return to the emergency room or prolonged stays spanning months.

**Taxonomy-derivation rationale (Step 5):** Clearly separated by extreme duration (up to hundreds of days), massive trace lengths, and explicit rework flags on diagnostic activities.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 355/846 variants (42.0%) · micro 377/1050 cases (35.9%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 16.17, nearest other category `inpatient_admission_recovery` at mean distance 13.60

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.307, nearest other category `inpatient_admission_recovery` at mean distance 0.476

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0350` / `V0710` (category `chronic_rework_readmission`): structural=180, profile=0.670
- `V0098` / `V0710` (category `chronic_rework_readmission`): structural=179, profile=0.646
- `V0686` / `V0710` (category `chronic_rework_readmission`): structural=179, profile=0.683
- `V0045` / `V0710` (category `chronic_rework_readmission`): structural=178, profile=0.694
- `V0101` / `V0710` (category `chronic_rework_readmission`): structural=178, profile=0.522
- `V0104` / `V0710` (category `chronic_rework_readmission`): structural=178, profile=0.673
- `V0110` / `V0710` (category `chronic_rework_readmission`): structural=178, profile=0.677
- `V0180` / `V0710` (category `chronic_rework_readmission`): structural=178, profile=0.607
- `V0242` / `V0710` (category `chronic_rework_readmission`): structural=178, profile=0.585
- `V0270` / `V0710` (category `chronic_rework_readmission`): structural=178, profile=0.505

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0003` (`rapid_assessment_triage`) / `V0379` (`acute_emergency_treatment`): structural=1, profile=0.388
- `V0004` (`acute_emergency_treatment`) / `V0679` (`rapid_assessment_triage`): structural=1, profile=0.024
- `V0004` (`acute_emergency_treatment`) / `V0713` (`rapid_assessment_triage`): structural=1, profile=0.044
- `V0006` (`acute_emergency_treatment`) / `V0148` (`rapid_assessment_triage`): structural=1, profile=0.011
- `V0007` (`acute_emergency_treatment`) / `V0040` (`inpatient_admission_recovery`): structural=1, profile=0.336
- `V0007` (`acute_emergency_treatment`) / `V0148` (`rapid_assessment_triage`): structural=1, profile=0.004
- `V0008` (`inpatient_admission_recovery`) / `V0686` (`chronic_rework_readmission`): structural=1, profile=0.454
- `V0008` (`inpatient_admission_recovery`) / `V0707` (`rapid_assessment_triage`): structural=1, profile=0.425
- `V0009` (`acute_emergency_treatment`) / `V0148` (`rapid_assessment_triage`): structural=1, profile=0.022
- `V0011` (`acute_emergency_treatment`) / `V0510` (`rapid_assessment_triage`): structural=1, profile=0.019

## Residual

9/846 variants (1.1%), 9/1050 cases (0.9%) unassigned.

- `V0365`: Unusual short path ending in uncompleted diagnostic activity rather than full recovery or acute discharge.
- `V0374`: Truncated trace ending on an intermediate diagnostic activity without standard completion.
- `V0417`: Short encounter with anomalous looping back to ER Triage without clear completion or admission, fitting none of the standard categories.
- `V0654`: The process is incomplete, terminating at Leucocytes without reaching a definitive release or admission recovery category.
- `V0664`: An incomplete variant terminating abruptly at IV Liquid without reaching a release or admission endpoint.
- `V0764`: Incomplete or truncated sequence ending prematurely at ER Sepsis Triage without completing treatment or admission.
- `V0772`: Incomplete sequence terminating unexpectedly after repeated CRP tests without a clear release or admission outcome.
- `V0774`: Abnormal ordering with tests performed before registration and triage, ending prematurely at ER Sepsis Triage.
- `V0775`: Incomplete sequence terminating at a repetitive CRP test without reaching admission, release, or emergency completion.
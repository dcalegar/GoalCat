# Step 6 — Narrative assignment report

Run: `icpm2027_e1_open_rep2` | Log: `sepsis` | Taxonomy mode: `open` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Rapid Triage and Outpatient-Style Resolution (`rapid_triage_and_discharge`)

Cases that move swiftly through registration, triage, and basic lab work (CRP, Leucocytes) with very short total durations (minutes to hours) and terminate directly after initial evaluation or mild intervention without requiring inpatient admission.

**Taxonomy-derivation rationale (Step 5):** Grouped based on low duration, short trace length, and simple diagnostic or triage outcomes without ward admissions.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 67/846 variants (7.9%) · micro 173/1050 cases (16.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.60, nearest other category `active_medical_intervention` at mean distance 6.02

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.456, nearest other category `active_medical_intervention` at mean distance 0.554

## Active Medical Intervention & Short Stay (`active_medical_intervention`)

Cases requiring active treatment steps such as IV liquids and IV antibiotics following initial lab and triage workups. These resolve either with discharge (Release A, B, etc.) or short-term observation within a moderate timeframe.

**Taxonomy-derivation rationale (Step 5):** Reflects standard acute care pathways involving medication administration (IV Antibiotics/Liquid) and moderate durations.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 75/846 variants (8.9%) · micro 124/1050 cases (11.8%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 6.19, nearest other category `rapid_triage_and_discharge` at mean distance 6.02

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.517, nearest other category `inpatient_admission_standard` at mean distance 0.553

## Standard Inpatient Admission & Release (`inpatient_admission_standard`)

Cases where patients are admitted to nursing care (Admission NC) or intensive care (Admission IC) units following diagnostic testing and interventions, culminating in a successful discharge or release after several days.

**Taxonomy-derivation rationale (Step 5):** Characterized by formal ward admission steps and medium-range durations spanning multiple days.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 388/846 variants (45.9%) · micro 422/1050 cases (40.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 9.03, nearest other category `active_medical_intervention` at mean distance 8.94

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.320, nearest other category `chronic_rework_and_readmission` at mean distance 0.458

## Extended Stay with Chronic Rework and Readmission (`chronic_rework_and_readmission`)

Complex, highly extended cases featuring extensive repetitive testing (frequent looping of CRP, LacticAcid, Leucocytes), multiple ward transfers, and extreme durations (weeks to over a year), often culminating in return to the emergency room or prolonged hospitalization.

**Taxonomy-derivation rationale (Step 5):** Captures extreme outliers characterized by massive trace lengths, severe rework, and exceptionally long durations leading to return visits or complex releases.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 305/846 variants (36.1%) · micro 320/1050 cases (30.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 17.05, nearest other category `inpatient_admission_standard` at mean distance 14.05

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.294, nearest other category `inpatient_admission_standard` at mean distance 0.458

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0350` / `V0710` (category `chronic_rework_and_readmission`): structural=180, profile=0.670
- `V0497` / `V0710` (category `chronic_rework_and_readmission`): structural=180, profile=0.751
- `V0098` / `V0710` (category `chronic_rework_and_readmission`): structural=179, profile=0.646
- `V0424` / `V0710` (category `chronic_rework_and_readmission`): structural=179, profile=0.731
- `V0686` / `V0710` (category `chronic_rework_and_readmission`): structural=179, profile=0.683
- `V0045` / `V0710` (category `chronic_rework_and_readmission`): structural=178, profile=0.694
- `V0180` / `V0710` (category `chronic_rework_and_readmission`): structural=178, profile=0.607
- `V0242` / `V0710` (category `chronic_rework_and_readmission`): structural=178, profile=0.585
- `V0270` / `V0710` (category `chronic_rework_and_readmission`): structural=178, profile=0.505
- `V0614` / `V0710` (category `chronic_rework_and_readmission`): structural=178, profile=0.677

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0004` (`active_medical_intervention`) / `V0679` (`rapid_triage_and_discharge`): structural=1, profile=0.024
- `V0006` (`active_medical_intervention`) / `V0148` (`rapid_triage_and_discharge`): structural=1, profile=0.011
- `V0007` (`active_medical_intervention`) / `V0056` (`rapid_triage_and_discharge`): structural=1, profile=0.033
- `V0007` (`active_medical_intervention`) / `V0148` (`rapid_triage_and_discharge`): structural=1, profile=0.004
- `V0008` (`inpatient_admission_standard`) / `V0686` (`chronic_rework_and_readmission`): structural=1, profile=0.454
- `V0008` (`inpatient_admission_standard`) / `V0707` (`rapid_triage_and_discharge`): structural=1, profile=0.425
- `V0009` (`active_medical_intervention`) / `V0148` (`rapid_triage_and_discharge`): structural=1, profile=0.022
- `V0011` (`active_medical_intervention`) / `V0510` (`rapid_triage_and_discharge`): structural=1, profile=0.019
- `V0011` (`active_medical_intervention`) / `V0679` (`rapid_triage_and_discharge`): structural=1, profile=0.002
- `V0012` (`active_medical_intervention`) / `V0510` (`rapid_triage_and_discharge`): structural=1, profile=0.041

## Residual

11/846 variants (1.3%), 11/1050 cases (1.0%) unassigned.

- `V0365`: Terminates mid-sequence at Leucocytes without an endpoint like release or return, making classification incomplete.
- `V0374`: Incomplete outcome sequence ending abruptly with Leucocytes.
- `V0417`: Does not fit standard discharge or admission paths; the sequence loops back to ER Triage quickly, making it a residual case.
- `V0636`: Incomplete or abnormal trajectory ending prematurely in a LacticAcid test rather than a terminal discharge or release category.
- `V0644`: Truncated process path terminating unexpectedly in a CRP lab test instead of an appropriate resolution or release outcome.
- `V0654`: The narrative terminates abruptly at Leucocytes after ICU admission and rework without a final discharge or standard completion outcome.
- `V0664`: Truncated trace ending at IV Liquid without completing triage, admission, or discharge phases.
- `V0694`: Incomplete trace ending prematurely at ER Sepsis Triage without treatment, admission, or discharge.
- `V0772`: Process terminates unexpectedly at CRP activity without a standard release or clear outcome.
- `V0774`: Incomplete or non-standard sequence starting with labs before registration, terminating at ER Sepsis Triage.
- `V0775`: Terminates on repeated CRP activity without formal discharge or admission.
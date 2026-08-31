# Step 6 — Narrative assignment report

Run: `icpm2027_e1_open_rep1` | Log: `sepsis` | Taxonomy mode: `open` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Rapid Triage and Outpatient Evaluation (`rapid_triage_and_discharge`)

Short-duration, low-length paths consisting primarily of initial emergency room registration, triage, and rapid blood work or sepsis screening without subsequent inpatient admission.

**Taxonomy-derivation rationale (Step 5):** These variants represent low-acuity or fast-resolved cases where patients spend minutes to hours in the ER and are processed with minimal steps.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 93/846 variants (11.0%) · micro 200/1050 cases (19.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.96, nearest other category `acute_medical_intervention` at mean distance 7.66

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.480, nearest other category `acute_medical_intervention` at mean distance 0.594

## Acute Medical Intervention (`acute_medical_intervention`)

Standard acute care pathways that involve extensive diagnostics (CRP, Leucocytes, Lactic Acid) followed by active treatment such as IV liquids and IV antibiotics within a moderate duration.

**Taxonomy-derivation rationale (Step 5):** Characterized by moderate trace lengths and durations of hours to days, leading to treatment interventions like IV antibiotics.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 49/846 variants (5.8%) · micro 94/1050 cases (9.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 8.31, nearest other category `rapid_triage_and_discharge` at mean distance 7.66

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.522, nearest other category `short_inpatient_admission` at mean distance 0.486

## Short Inpatient Admission and Release (`short_inpatient_admission`)

Cases requiring short-term ward admission (Admission NC or Admission IC) spanning a few days, concluding with a standard patient release.

**Taxonomy-derivation rationale (Step 5):** Captures standard inpatient stays that are moderately prolonged compared to pure ER visits, but lacking chronic or extreme complications.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 342/846 variants (40.4%) · micro 365/1050 cases (34.8%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 8.33, nearest other category `acute_medical_intervention` at mean distance 8.67

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.297, nearest other category `chronic_rework_and_readmission` at mean distance 0.477

## Chronic Rework and Readmission (`chronic_rework_and_readmission`)

Extremely long, highly complex paths involving heavy repetition of diagnostics and admissions (rework), frequently resulting in patient return to the ER or extended recovery.

**Taxonomy-derivation rationale (Step 5):** Identified by high trace lengths, extensive durations spanning dozens to hundreds of days, and repeated diagnostic tests or ward admissions.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 357/846 variants (42.2%) · micro 386/1050 cases (36.8%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 16.28, nearest other category `short_inpatient_admission` at mean distance 13.51

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.305, nearest other category `short_inpatient_admission` at mean distance 0.477

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0350` / `V0710` (category `chronic_rework_and_readmission`): structural=180, profile=0.670
- `V0497` / `V0710` (category `chronic_rework_and_readmission`): structural=180, profile=0.751
- `V0098` / `V0710` (category `chronic_rework_and_readmission`): structural=179, profile=0.646
- `V0424` / `V0710` (category `chronic_rework_and_readmission`): structural=179, profile=0.731
- `V0686` / `V0710` (category `chronic_rework_and_readmission`): structural=179, profile=0.683
- `V0045` / `V0710` (category `chronic_rework_and_readmission`): structural=178, profile=0.694
- `V0101` / `V0710` (category `chronic_rework_and_readmission`): structural=178, profile=0.522
- `V0110` / `V0710` (category `chronic_rework_and_readmission`): structural=178, profile=0.677
- `V0180` / `V0710` (category `chronic_rework_and_readmission`): structural=178, profile=0.607
- `V0242` / `V0710` (category `chronic_rework_and_readmission`): structural=178, profile=0.585

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0004` (`acute_medical_intervention`) / `V0415` (`rapid_triage_and_discharge`): structural=1, profile=0.361
- `V0004` (`acute_medical_intervention`) / `V0679` (`rapid_triage_and_discharge`): structural=1, profile=0.024
- `V0004` (`acute_medical_intervention`) / `V0713` (`rapid_triage_and_discharge`): structural=1, profile=0.044
- `V0006` (`acute_medical_intervention`) / `V0148` (`rapid_triage_and_discharge`): structural=1, profile=0.011
- `V0007` (`acute_medical_intervention`) / `V0040` (`short_inpatient_admission`): structural=1, profile=0.336
- `V0007` (`acute_medical_intervention`) / `V0056` (`rapid_triage_and_discharge`): structural=1, profile=0.033
- `V0007` (`acute_medical_intervention`) / `V0148` (`rapid_triage_and_discharge`): structural=1, profile=0.004
- `V0008` (`short_inpatient_admission`) / `V0686` (`chronic_rework_and_readmission`): structural=1, profile=0.454
- `V0008` (`short_inpatient_admission`) / `V0707` (`rapid_triage_and_discharge`): structural=1, profile=0.425
- `V0009` (`acute_medical_intervention`) / `V0148` (`rapid_triage_and_discharge`): structural=1, profile=0.022

## Residual

5/846 variants (0.6%), 5/1050 cases (0.5%) unassigned.

- `V0365`: Path ends unexpectedly with diagnostic activities rather than standard inpatient admission or release, fitting none of the clean categories.
- `V0374`: Very short path that concludes prematurely with a diagnostic test (Leucocytes) instead of a discharge or admission outcome.
- `V0462`: Very short duration sequence ending prematurely with a diagnostic outcome (CRP) rather than standard discharge or admission flow.
- `V0516`: Incomplete path ending abruptly with Leucocytes without standard triage or admission conclusion.
- `V0517`: Very short incomplete sequence ending in ER Triage without treatment or discharge.
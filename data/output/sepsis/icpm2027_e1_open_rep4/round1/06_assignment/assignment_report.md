# Step 6 — Narrative assignment report

Run: `icpm2027_e1_open_rep4` | Log: `sepsis` | Taxonomy mode: `open` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Fast Triage / Minimal Evaluation (`fast_triage_only`)

Short, rapid patient encounters concluding quickly after initial triage and minimal lab work without progression to admission or intensive treatment.

**Taxonomy-derivation rationale (Step 5):** Characterized by very low duration (minutes), short trace lengths, and outcomes like ER Sepsis Triage or basic lab tests.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 75/846 variants (8.9%) · micro 180/1050 cases (17.1%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.66, nearest other category `standard_acute_care` at mean distance 6.34

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.480, nearest other category `standard_acute_care` at mean distance 0.571

## Standard Acute Care & Treatment (`standard_acute_care`)

Standard emergency department pathways involving comprehensive diagnostics (blood tests) followed by acute interventions such as IV liquids and IV antibiotics.

**Taxonomy-derivation rationale (Step 5):** Medium duration (hours to a few days) with intermediate trace lengths, ending in IV antibiotics or initial admission/release.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 70/846 variants (8.3%) · micro 118/1050 cases (11.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 6.54, nearest other category `fast_triage_only` at mean distance 6.34

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.501, nearest other category `inpatient_admission_release` at mean distance 0.502

## Inpatient Admission & Controlled Release (`inpatient_admission_release`)

Encounters requiring inpatient nursing or intensive care unit admission following diagnostics and treatment, eventually resulting in a stable release.

**Taxonomy-derivation rationale (Step 5):** Longer durations (days) involving bed allocation (Admission NC/IC) and structured discharge outcomes (Release A, B, C, D).

**Goal-model linkage:** (no goal model)

**Coverage:** macro 369/846 variants (43.6%) · micro 401/1050 cases (38.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 9.14, nearest other category `standard_acute_care` at mean distance 8.72

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.326, nearest other category `chronic_readmission_rework` at mean distance 0.466

## Chronic Readmission & Heavy Rework (`chronic_readmission_rework`)

Extremely long, highly complex pathways characterized by extensive repetition of lab tests and admissions, frequently resulting in patient return to the emergency room.

**Taxonomy-derivation rationale (Step 5):** Extreme duration (up to hundreds of days), massive trace lengths, heavy rework observed across multiple variables, and Return ER outcomes.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 325/846 variants (38.4%) · micro 344/1050 cases (32.8%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 16.33, nearest other category `inpatient_admission_release` at mean distance 13.88

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.297, nearest other category `inpatient_admission_release` at mean distance 0.466

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0350` / `V0710` (category `chronic_readmission_rework`): structural=180, profile=0.670
- `V0098` / `V0710` (category `chronic_readmission_rework`): structural=179, profile=0.646
- `V0686` / `V0710` (category `chronic_readmission_rework`): structural=179, profile=0.683
- `V0101` / `V0710` (category `chronic_readmission_rework`): structural=178, profile=0.522
- `V0104` / `V0710` (category `chronic_readmission_rework`): structural=178, profile=0.673
- `V0110` / `V0710` (category `chronic_readmission_rework`): structural=178, profile=0.677
- `V0180` / `V0710` (category `chronic_readmission_rework`): structural=178, profile=0.607
- `V0242` / `V0710` (category `chronic_readmission_rework`): structural=178, profile=0.585
- `V0614` / `V0710` (category `chronic_readmission_rework`): structural=178, profile=0.677
- `V0650` / `V0710` (category `chronic_readmission_rework`): structural=178, profile=0.601

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0004` (`standard_acute_care`) / `V0415` (`fast_triage_only`): structural=1, profile=0.361
- `V0004` (`standard_acute_care`) / `V0679` (`fast_triage_only`): structural=1, profile=0.024
- `V0006` (`standard_acute_care`) / `V0148` (`fast_triage_only`): structural=1, profile=0.011
- `V0007` (`standard_acute_care`) / `V0056` (`fast_triage_only`): structural=1, profile=0.033
- `V0007` (`standard_acute_care`) / `V0148` (`fast_triage_only`): structural=1, profile=0.004
- `V0008` (`inpatient_admission_release`) / `V0686` (`chronic_readmission_rework`): structural=1, profile=0.454
- `V0008` (`inpatient_admission_release`) / `V0706` (`fast_triage_only`): structural=1, profile=0.029
- `V0008` (`inpatient_admission_release`) / `V0707` (`fast_triage_only`): structural=1, profile=0.425
- `V0009` (`standard_acute_care`) / `V0148` (`fast_triage_only`): structural=1, profile=0.022
- `V0011` (`standard_acute_care`) / `V0417` (`fast_triage_only`): structural=1, profile=0.707

## Residual

7/846 variants (0.8%), 7/1050 cases (0.7%) unassigned.

- `V0181`: Incomplete or irregular trajectory ending abruptly with leucocytes instead of a proper clinical release or admission endpoint.
- `V0636`: Incomplete or truncated episode ending with a lab test (LacticAcid) rather than a clear release or admission outcome.
- `V0644`: Truncated encounter ending with a lab test (CRP) without completing a proper disposition or release.
- `V0764`: Incomplete or truncated encounter ending prematurely at ER Sepsis Triage without concluding in a known category.
- `V0772`: Incomplete or interrupted encounter that concludes unexpectedly on a lab test (CRP) instead of a proper disposition.
- `V0774`: Incomplete path terminating early at ER Sepsis Triage without standard treatment or outcome.
- `V0775`: Encounter halts prematurely at a lab test (CRP) without progression to admission or formal release.
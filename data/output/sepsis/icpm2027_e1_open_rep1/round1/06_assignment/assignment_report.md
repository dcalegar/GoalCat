# Step 6 — Narrative assignment report

Run: `icpm2027_e1_open_rep1` | Log: `sepsis` | Taxonomy mode: `open` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Fast ER Triage & Minimal Diagnostics (`fast_er_triage`)

Short, rapid cases that conclude immediately at triage or with basic lab tests (Leucocytes/CRP) within minutes and without hospitalization or intensive interventions.

**Taxonomy-derivation rationale (Step 5):** Grounded in variants like V0001, V0002, V0003, and V0292, which show extremely short durations (minutes) and very low trace lengths ending in triage or quick lab results.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 48/846 variants (5.7%) · micro 152/1050 cases (14.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.63, nearest other category `acute_iv_treatment` at mean distance 5.55

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.463, nearest other category `acute_iv_treatment` at mean distance 0.492

## Acute ER Care with IV Intervention (`acute_iv_treatment`)

Standard acute sepsis care pathways involving triage, comprehensive blood work (CRP, Leucocytes, LacticAcid), and administration of intravenous liquids and antibiotics within a short duration.

**Taxonomy-derivation rationale (Step 5):** Grounded in frequent variants like V0004, V0005, V0006, V0007, and V0009, which feature standard diagnostic panels followed by IV therapy within hours.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 67/846 variants (7.9%) · micro 115/1050 cases (11.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.67, nearest other category `fast_er_triage` at mean distance 5.55

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.472, nearest other category `fast_er_triage` at mean distance 0.492

## Standard Hospital Admission and Release (`standard_admission_release`)

Cases requiring formal hospital admission (Admission NC or Admission IC) followed by a standard inpatient stay and subsequent discharge (Release A, B, C, or D).

**Taxonomy-derivation rationale (Step 5):** Grounded in variants that incorporate ward admissions and end in regular release outcomes over a span of days, such as V0008, V0068, and V0070.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 482/846 variants (57.0%) · micro 511/1050 cases (48.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 8.96, nearest other category `acute_iv_treatment` at mean distance 9.35

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.369, nearest other category `chronic_rework_readmission` at mean distance 0.430

## Chronic Rework and Readmission (`chronic_rework_readmission`)

Extreme outliers characterized by extensive loops, highly repeated lab tests (CRP, LacticAcid, Leucocytes) and ward admissions, spanning multiple months and frequently culminating in returns to the ER or prolonged stays.

**Taxonomy-derivation rationale (Step 5):** Grounded in extremely long and complex variants like V0317, V0551, V0605, V0625, and V0710, where extensive rework and long durations dominate the process profile.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 238/846 variants (28.1%) · micro 261/1050 cases (24.9%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 19.03, nearest other category `standard_admission_release` at mean distance 15.38

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.314, nearest other category `standard_admission_release` at mean distance 0.430

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0098` / `V0710` (category `chronic_rework_readmission`): structural=179, profile=0.646
- `V0686` / `V0710` (category `chronic_rework_readmission`): structural=179, profile=0.683
- `V0710` / `V0828` (category `chronic_rework_readmission`): structural=179, profile=0.674
- `V0045` / `V0710` (category `chronic_rework_readmission`): structural=178, profile=0.694
- `V0614` / `V0710` (category `chronic_rework_readmission`): structural=178, profile=0.677
- `V0650` / `V0710` (category `chronic_rework_readmission`): structural=178, profile=0.601
- `V0658` / `V0710` (category `chronic_rework_readmission`): structural=178, profile=0.584
- `V0710` / `V0823` (category `chronic_rework_readmission`): structural=178, profile=0.690
- `V0026` / `V0710` (category `chronic_rework_readmission`): structural=177, profile=0.638
- `V0033` / `V0710` (category `chronic_rework_readmission`): structural=177, profile=0.597

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0003` (`fast_er_triage`) / `V0379` (`acute_iv_treatment`): structural=1, profile=0.388
- `V0004` (`acute_iv_treatment`) / `V0679` (`fast_er_triage`): structural=1, profile=0.024
- `V0007` (`acute_iv_treatment`) / `V0040` (`standard_admission_release`): structural=1, profile=0.336
- `V0008` (`standard_admission_release`) / `V0686` (`chronic_rework_readmission`): structural=1, profile=0.454
- `V0011` (`acute_iv_treatment`) / `V0510` (`fast_er_triage`): structural=1, profile=0.019
- `V0011` (`acute_iv_treatment`) / `V0679` (`fast_er_triage`): structural=1, profile=0.002
- `V0012` (`acute_iv_treatment`) / `V0510` (`fast_er_triage`): structural=1, profile=0.041
- `V0013` (`fast_er_triage`) / `V0713` (`acute_iv_treatment`): structural=1, profile=0.398
- `V0016` (`standard_admission_release`) / `V0041` (`chronic_rework_readmission`): structural=1, profile=0.115
- `V0016` (`standard_admission_release`) / `V0052` (`chronic_rework_readmission`): structural=1, profile=0.429

## Residual

11/846 variants (1.3%), 11/1050 cases (1.0%) unassigned.

- `V0417`: Does not fit any category cleanly due to ending back at ER triage.
- `V0636`: The case does not fit any standard category because it terminates abnormally at a LacticAcid activity instead of a release or ER return.
- `V0644`: The case terminates with a CRP lab test instead of concluding with a standard release or ER return.
- `V0645`: The case is truncated, terminating on a LacticAcid activity without reaching a formal release or admission resolution.
- `V0703`: The case ends with IV Liquid rather than an admission or discharge, making it an incomplete or non-standard trajectory.
- `V0707`: The process concludes at Admission NC, lacking a complete hospital stay or final release sequence.
- `V0764`: Incomplete case concluding prematurely at ER Sepsis Triage without standard treatments or admissions.
- `V0772`: Incomplete process ending abruptly in a repeated CRP activity.
- `V0774`: Truncated trace that does not progress to any treatment or admission.
- `V0775`: Incomplete trace ending at CRP without reaching a release or admission.
- `V0778`: Truncated trace ending unexpectedly at Leucocytes.
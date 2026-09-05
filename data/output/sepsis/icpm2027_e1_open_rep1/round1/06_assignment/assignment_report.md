# Step 6 — Narrative assignment report

Run: `icpm2027_e1_open_rep1` | Log: `sepsis` | Taxonomy mode: `open` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Fast Triage / Minimal Evaluation (`fast_triage_only`)

Short, rapid pathways consisting exclusively of ER registration, triage, and basic lab tests or immediate release with very short durations (minutes), requiring no admission or intensive treatment.

**Taxonomy-derivation rationale (Step 5):** Represents very low duration and low length cases that quickly resolve or terminate at triage without complications.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 41/846 variants (4.8%) · micro 144/1050 cases (13.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.25, nearest other category `acute_iv_treatment` at mean distance 5.54

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.453, nearest other category `acute_iv_treatment` at mean distance 0.528

## Acute Intervention with IV Therapy (`acute_iv_treatment`)

Pathways where patients receive immediate stabilization via IV fluids and IV antibiotics alongside lab evaluations, reflecting moderate duration (hours) and an active medical intervention profile.

**Taxonomy-derivation rationale (Step 5):** Captures standard acute sepsis care pathways involving active pharmacological intervention but lacking prolonged hospital stays.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 91/846 variants (10.8%) · micro 141/1050 cases (13.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.57, nearest other category `fast_triage_only` at mean distance 5.54

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.499, nearest other category `fast_triage_only` at mean distance 0.528

## Standard Admission and Release (`standard_admission_release`)

Pathways involving hospital ward admission (Admission NC) followed by eventual standard discharge (Release A, B, C, or D) over a timeframe of days, with limited or controlled test repetitions.

**Taxonomy-derivation rationale (Step 5):** Groups typical inpatient recovery cycles where patients are successfully stabilized and released.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 337/846 variants (39.8%) · micro 370/1050 cases (35.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 7.65, nearest other category `acute_iv_treatment` at mean distance 8.22

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.295, nearest other category `chronic_rework_readmission` at mean distance 0.467

## Chronic Rework and Readmission (`chronic_rework_readmission`)

Extremely long, highly complex pathways characterized by extensive test repetitions (CRP, Leucocytes, LacticAcid), multiple ward transfers (Admission NC, Admission IC), and frequent readmissions or 'Return ER' outcomes.

**Taxonomy-derivation rationale (Step 5):** Isolates outlier and extreme cases marked by severe instability, high trace length, massive duration, and persistent diagnostic rework.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 375/846 variants (44.3%) · micro 393/1050 cases (37.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 16.33, nearest other category `standard_admission_release` at mean distance 13.45

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.319, nearest other category `standard_admission_release` at mean distance 0.467

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0350` / `V0710` (category `chronic_rework_readmission`): structural=180, profile=0.670
- `V0497` / `V0710` (category `chronic_rework_readmission`): structural=180, profile=0.751
- `V0098` / `V0710` (category `chronic_rework_readmission`): structural=179, profile=0.646
- `V0686` / `V0710` (category `chronic_rework_readmission`): structural=179, profile=0.683
- `V0045` / `V0710` (category `chronic_rework_readmission`): structural=178, profile=0.694
- `V0101` / `V0710` (category `chronic_rework_readmission`): structural=178, profile=0.522
- `V0104` / `V0710` (category `chronic_rework_readmission`): structural=178, profile=0.673
- `V0110` / `V0710` (category `chronic_rework_readmission`): structural=178, profile=0.677
- `V0131` / `V0710` (category `chronic_rework_readmission`): structural=178, profile=0.653
- `V0180` / `V0710` (category `chronic_rework_readmission`): structural=178, profile=0.607

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0003` (`fast_triage_only`) / `V0379` (`acute_iv_treatment`): structural=1, profile=0.388
- `V0008` (`standard_admission_release`) / `V0686` (`chronic_rework_readmission`): structural=1, profile=0.454
- `V0008` (`standard_admission_release`) / `V0707` (`fast_triage_only`): structural=1, profile=0.425
- `V0011` (`acute_iv_treatment`) / `V0417` (`fast_triage_only`): structural=1, profile=0.707
- `V0011` (`acute_iv_treatment`) / `V0510` (`fast_triage_only`): structural=1, profile=0.019
- `V0012` (`acute_iv_treatment`) / `V0510` (`fast_triage_only`): structural=1, profile=0.041
- `V0013` (`fast_triage_only`) / `V0713` (`acute_iv_treatment`): structural=1, profile=0.398
- `V0015` (`standard_admission_release`) / `V0116` (`chronic_rework_readmission`): structural=1, profile=0.429
- `V0016` (`standard_admission_release`) / `V0041` (`chronic_rework_readmission`): structural=1, profile=0.115
- `V0016` (`standard_admission_release`) / `V0052` (`chronic_rework_readmission`): structural=1, profile=0.429

## Residual

2/846 variants (0.2%), 2/1050 cases (0.2%) unassigned.

- `V0636`: Does not fit any primary category cleanly as its outcome is LacticAcid rather than a standard release or return ER, despite having ward admission.
- `V0644`: Duration is short (12h) and outcome is CRP rather than release or admission completion, making it a partial or atypical pathway.
# Step 6 — Narrative assignment report

Run: `icpm2027_e1_open_rep3` | Log: `sepsis` | Taxonomy mode: `open` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Rapid Triage / Outpatient Workup (`rapid_triage_only`)

Short, fast-paced pathways ending quickly with basic triage or initial blood work (CRP/Leucocytes) without admission, typically completing within minutes.

**Taxonomy-derivation rationale (Step 5):** Grounded in short trace lengths, low durations, and early terminal activities like ER Sepsis Triage, CRP, or Leucocytes.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 40/846 variants (4.7%) · micro 143/1050 cases (13.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.35, nearest other category `acute_iv_treatment` at mean distance 5.13

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.462, nearest other category `acute_iv_treatment` at mean distance 0.497

## Acute IV Intervention (`acute_iv_treatment`)

Mid-length pathways featuring administration of intravenous fluids and antibiotics alongside standard blood panels, resolving within hours.

**Taxonomy-derivation rationale (Step 5):** Characterized by the inclusion of IV Liquid and IV Antibiotics and intermediate durations (1-4 hours).

**Goal-model linkage:** (no goal model)

**Coverage:** macro 67/846 variants (7.9%) · micro 119/1050 cases (11.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.84, nearest other category `rapid_triage_only` at mean distance 5.13

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.418, nearest other category `rapid_triage_only` at mean distance 0.497

## Standard Inpatient Admission & Release (`standard_admission_release`)

Pathways requiring ward admission (Admission NC/IC) followed by multi-day observation and eventual successful release (Release A, B, C, or D).

**Taxonomy-derivation rationale (Step 5):** Reflects standard hospital stays involving nursing or intensive care admissions and structured release outcomes.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 446/846 variants (52.7%) · micro 480/1050 cases (45.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.66, nearest other category `acute_iv_treatment` at mean distance 11.20

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.283, nearest other category `readmission_loop` at mean distance 0.539

## Readmission / Extended Complication Path (`readmission_loop`)

Complex, highly repetitive or long-duration pathways that result in patient readmissions or return to the emergency room ('Return ER').

**Taxonomy-derivation rationale (Step 5):** Identified by exceptionally long durations (weeks to over a year), high trace lengths, and the 'Return ER' final outcome.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 281/846 variants (33.2%) · micro 296/1050 cases (28.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 13.64, nearest other category `standard_admission_release` at mean distance 13.57

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.184, nearest other category `standard_admission_release` at mean distance 0.539

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0286` / `V0710` (category `standard_admission_release`): structural=182, profile=0.756
- `V0053` / `V0710` (category `standard_admission_release`): structural=181, profile=0.788
- `V0351` / `V0710` (category `standard_admission_release`): structural=181, profile=0.765
- `V0058` / `V0710` (category `standard_admission_release`): structural=180, profile=0.781
- `V0306` / `V0710` (category `standard_admission_release`): structural=180, profile=0.664
- `V0323` / `V0710` (category `standard_admission_release`): structural=180, profile=0.800
- `V0489` / `V0710` (category `standard_admission_release`): structural=180, profile=0.755
- `V0710` / `V0768` (category `standard_admission_release`): structural=180, profile=0.758
- `V0008` / `V0710` (category `standard_admission_release`): structural=179, profile=0.770
- `V0014` / `V0710` (category `standard_admission_release`): structural=179, profile=0.766

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0003` (`rapid_triage_only`) / `V0379` (`acute_iv_treatment`): structural=1, profile=0.388
- `V0008` (`standard_admission_release`) / `V0686` (`readmission_loop`): structural=1, profile=0.454
- `V0011` (`acute_iv_treatment`) / `V0417` (`rapid_triage_only`): structural=1, profile=0.707
- `V0011` (`acute_iv_treatment`) / `V0510` (`rapid_triage_only`): structural=1, profile=0.019
- `V0012` (`acute_iv_treatment`) / `V0510` (`rapid_triage_only`): structural=1, profile=0.041
- `V0013` (`rapid_triage_only`) / `V0713` (`acute_iv_treatment`): structural=1, profile=0.398
- `V0015` (`standard_admission_release`) / `V0116` (`readmission_loop`): structural=1, profile=0.429
- `V0016` (`standard_admission_release`) / `V0052` (`readmission_loop`): structural=1, profile=0.429
- `V0016` (`standard_admission_release`) / `V0462` (`acute_iv_treatment`): structural=1, profile=0.392
- `V0022` (`standard_admission_release`) / `V0415` (`acute_iv_treatment`): structural=1, profile=0.428

## Residual

12/846 variants (1.4%), 12/1050 cases (1.1%) unassigned.

- `V0181`: Involves admission and blood work but ends unusually with Leucocytes rather than a proper release or readmission event.
- `V0365`: The pathway ends with blood work (Leucocytes) rather than a clear admission, release, or ER return outcome.
- `V0368`: This pathway terminates directly at Admission NC without showing any triage completion, intervention, or final release/return outcome.
- `V0374`: The pathway halts at Leucocytes and does not complete a full admission, release, or readmission cycle.
- `V0636`: Path ends with intermediate lab work (LacticAcid) rather than triage completion, acute IV intervention, standard release, or a readmission event.
- `V0644`: Process concludes with a standalone CRP lab test activity rather than a terminal category outcome like release or return ER.
- `V0654`: The pathway is incomplete with an ending at Leucocytes and does not cleanly fit rapid triage, acute IV treatment, standard admission and release, or a readmission loop.
- `V0663`: The pathway ends abruptly at Admission NC and lacks the duration or completion required for standard admission and release.
- `V0670`: Contains a chaotic sequence of release followed by a Return ER and further lab work, not fitting neatly into a standard pattern.
- `V0703`: Path ends with IV Liquid rather than an admission or discharge, making it anomalous or incomplete.
- `V0707`: Terminates at Admission NC without an explicit release or other final workflow.
- `V0742`: Finishes with LacticAcid and does not result in admission, release, or ER return.
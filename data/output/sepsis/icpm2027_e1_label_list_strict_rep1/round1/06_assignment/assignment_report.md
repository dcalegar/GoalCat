# Step 6 — Narrative assignment report

Run: `icpm2027_e1_label_list_strict_rep1` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Uncomplicated recovery (`uncomplicated_recovery`)

The case follows a standard course to discharge, with no recorded escalation of care and no extended observation beyond the ordinary stay pattern.

**Taxonomy-derivation rationale (Step 5):** The baseline disposition category against which the other four represent some departure — either in duration, care intensity, or discharge circumstance.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 305/846 variants (36.1%) · micro 336/1050 cases (32.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 7.61, nearest other category `early_or_irregular_discharge` at mean distance 8.52

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.294, nearest other category `extended_monitoring_recovery` at mean distance 0.334

## Extended monitoring before discharge (`extended_monitoring_recovery`)

The case recovers without escalation of care, but the trace shows a materially longer observation period than the uncomplicated pattern before discharge.

**Taxonomy-derivation rationale (Step 5):** Separates duration from severity: a longer stay is not, on its own, evidence that care was escalated.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 115/846 variants (13.6%) · micro 125/1050 cases (11.9%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 14.40, nearest other category `uncomplicated_recovery` at mean distance 12.12

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.323, nearest other category `uncomplicated_recovery` at mean distance 0.334

## Escalation of care during the stay (`care_escalation_during_stay`)

The trace shows an increase in care intensity at some point after admission (e.g., a transfer to a higher level of care) followed by eventual discharge.

**Taxonomy-derivation rationale (Step 5):** Captures cases whose clinical course was non-monotonic — an escalation mid-stay — independent of which specific unit received the transfer.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 90/846 variants (10.6%) · micro 90/1050 cases (8.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 23.12, nearest other category `uncomplicated_recovery` at mean distance 20.83

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.324, nearest other category `extended_monitoring_recovery` at mean distance 0.389

## Early or irregular discharge (`early_or_irregular_discharge`)

The trace ends in a discharge that departs from the standard pattern captured by the other categories — e.g., an unusually short stay relative to the case's recorded severity indicators, suggesting discharge ahead of the typical course.

**Taxonomy-derivation rationale (Step 5):** A residual pattern distinct from non_home_disposition: the case still ends in a discharge event, just not one following the ordinary course.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 65/846 variants (7.7%) · micro 67/1050 cases (6.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.71, nearest other category `uncomplicated_recovery` at mean distance 8.52

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.520, nearest other category `uncomplicated_recovery` at mean distance 0.655

## Non-home disposition (`non_home_disposition`)

The trace ends in a disposition other than a routine discharge — e.g., in-hospital death or transfer to another facility — rather than release to the patient's prior living situation.

**Taxonomy-derivation rationale (Step 5):** The most severe disposition category, kept separate because it reflects a different kind of case ending than any discharge-based category.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 215/846 variants (25.4%) · micro 223/1050 cases (21.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 10.29, nearest other category `uncomplicated_recovery` at mean distance 9.91

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.191, nearest other category `care_escalation_during_stay` at mean distance 0.402

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0650` / `V0710` (category `extended_monitoring_recovery`): structural=178, profile=0.601
- `V0710` / `V0783` (category `extended_monitoring_recovery`): structural=178, profile=0.569
- `V0033` / `V0710` (category `extended_monitoring_recovery`): structural=177, profile=0.597
- `V0156` / `V0710` (category `extended_monitoring_recovery`): structural=177, profile=0.655
- `V0274` / `V0710` (category `extended_monitoring_recovery`): structural=177, profile=0.390
- `V0015` / `V0710` (category `extended_monitoring_recovery`): structural=176, profile=0.611
- `V0016` / `V0710` (category `extended_monitoring_recovery`): structural=176, profile=0.598
- `V0028` / `V0710` (category `extended_monitoring_recovery`): structural=176, profile=0.503
- `V0073` / `V0710` (category `extended_monitoring_recovery`): structural=176, profile=0.589
- `V0396` / `V0710` (category `extended_monitoring_recovery`): structural=176, profile=0.586

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0008` (`uncomplicated_recovery`) / `V0686` (`non_home_disposition`): structural=1, profile=0.454
- `V0008` (`uncomplicated_recovery`) / `V0706` (`early_or_irregular_discharge`): structural=1, profile=0.029
- `V0008` (`uncomplicated_recovery`) / `V0707` (`early_or_irregular_discharge`): structural=1, profile=0.425
- `V0015` (`extended_monitoring_recovery`) / `V0116` (`non_home_disposition`): structural=1, profile=0.429
- `V0015` (`extended_monitoring_recovery`) / `V0758` (`uncomplicated_recovery`): structural=1, profile=0.120
- `V0016` (`extended_monitoring_recovery`) / `V0041` (`uncomplicated_recovery`): structural=1, profile=0.115
- `V0016` (`extended_monitoring_recovery`) / `V0052` (`non_home_disposition`): structural=1, profile=0.429
- `V0016` (`extended_monitoring_recovery`) / `V0362` (`uncomplicated_recovery`): structural=1, profile=0.006
- `V0016` (`extended_monitoring_recovery`) / `V0431` (`uncomplicated_recovery`): structural=1, profile=0.002
- `V0016` (`extended_monitoring_recovery`) / `V0462` (`early_or_irregular_discharge`): structural=1, profile=0.392

## Residual

56/846 variants (6.6%), 209/1050 cases (19.9%) unassigned.

- `V0001`: The trace ends at ER Sepsis Triage without reaching a discharge or admission, so none of the standard recovery or disposition categories apply.
- `V0002`: The trace terminates at CRP in the emergency phase without a final disposition or admission.
- `V0003`: The trace ends at Leucocytes in the emergency phase without proceeding to admission or discharge.
- `V0004`: The trace concludes at IV Antibiotics within the ER setting, lacking a subsequent hospital admission or formal discharge event.
- `V0005`: The trace stops at LacticAcid during the emergency workup without a recorded admission or discharge disposition.
- `V0006`: The trace ends with IV Antibiotics administration in the ER without reaching an admission or formal discharge step.
- `V0007`: The trace finishes at IV Antibiotics in the ER without a hospital admission or discharge event.
- `V0009`: The trace ends with IV Antibiotics in the ER without proceeding to admission or discharge.
- `V0010`: The trace loops back and terminates at ER Sepsis Triage without reaching a discharge or admission.
- `V0011`: The trace terminates with IV Antibiotics in the ER without an admission or final discharge.
- `V0012`: The trace ends at IV Antibiotics in the emergency department without an admission or discharge event.
- `V0013`: The trace ends at Leucocytes in the ER without proceeding to admission or discharge.
- `V0017`: The trace concludes at ER Sepsis Triage out of order, without reaching an admission or discharge.
- `V0019`: The trace ends at IV Antibiotics in the ER without an admission or release event.
- `V0020`: The trace stops at CRP during the emergency assessment without proceeding to admission or discharge.
- `V0024`: The trace ends abruptly at Admission NC without showing the final release or disposition.
- `V0025`: The trace concludes with IV Antibiotics in the ER without an admission or discharge step.
- `V0027`: The trace terminates at IV Antibiotics without reaching a discharge or completion disposition.
- `V0029`: The trace ends abruptly at Leucocytes without reaching a discharge disposition.
- `V0031`: The trace ends at LacticAcid without any recorded admission or discharge.
- `V0034`: The trace terminates at IV Liquid without a discharge event.
- `V0036`: The trace ends at CRP without a discharge or completion event.
- `V0038`: The trace stops at IV Antibiotics without an admission or discharge.
- `V0040`: The trace ends at Admission NC without reaching a discharge disposition.
- `V0043`: The trace stops at LacticAcid without an admission or discharge.
- `V0050`: The trace stops at CRP without an admission or discharge event.
- `V0081`: The trace ends in IV Liquid and does not reach a final discharge or disposition state.
- `V0088`: The trace ends prematurely at IV Antibiotics without a final outcome.
- `V0092`: The trace ends in LacticAcid without completing a discharge.
- `V0260`: The trace ends in IV Antibiotics without reaching a discharge or completion disposition, thus fitting none of the standard recovery or discharge categories.
- `V0268`: The trace terminates at Leucocytes testing without reaching a discharge or final disposition.
- `V0287`: The trace terminates prematurely at CRP without a completed hospital stay or discharge event.
- `V0292`: The trace ends abruptly at Leucocytes without reaching a discharge or disposition event.
- `V0295`: The trace stops at IV Antibiotics without recording a final discharge or disposition.
- `V0330`: The trace ends prematurely at IV Liquid without a recorded discharge or definitive outcome.
- `V0336`: The trace terminates at CRP without a final discharge or disposition event.
- `V0342`: Incomplete trace ending in CRP without discharge.
- `V0349`: Incomplete trace ending at ER Sepsis Triage.
- `V0501`: The trace ends in 'IV Liquid' inside the hospital without an explicit discharge or terminal outcome matching the defined categories.
- `V0507`: The trace terminates at 'IV Antibiotics' before any admission or disposition step is reached.
- `V0510`: The trace ends abruptly at 'IV Antibiotics' without proceeding to a ward admission or final disposition.
- `V0516`: The trace ends at 'Leucocytes' in an out-of-sequence fashion, lacking a proper discharge or disposition.
- `V0517`: The trace terminates prematurely at 'ER Triage' without completing the care process.
- `V0549`: The trace is incomplete, ending prematurely at IV Liquid without reaching a discharge or final disposition outcome.
- `V0676`: The narrative ends in IV Antibiotics rather than a recognized discharge or disposition state, indicating an incomplete or intermediate trace.
- `V0679`: The trace terminates at IV Antibiotics without reaching a final discharge disposition.
- `V0685`: The trace stops at IV Antibiotics and does not reach a completion state.
- `V0689`: The trace terminates at IV Antibiotics without a final disposition.
- `V0694`: The trace ends prematurely at ER Sepsis Triage.
- `V0742`: The trace terminates in a lab measurement (LacticAcid) rather than a final disposition, leaving it outside the standard categories.
- `V0750`: The trace terminates abruptly at an IV Antibiotics event rather than a complete discharge disposition.
- `V0759`: The trace ends prematurely at IV Antibiotics without reaching a final disposition or completion.
- `V0764`: The trace is incomplete, ending at ER Sepsis Triage.
- `V0772`: The trace ends abruptly at CRP without a final disposition.
- `V0774`: Incomplete trace ending at ER Sepsis Triage.
- `V0775`: Incomplete trace ending at CRP.
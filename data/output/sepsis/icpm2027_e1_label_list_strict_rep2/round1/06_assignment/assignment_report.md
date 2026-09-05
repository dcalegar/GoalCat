# Step 6 — Narrative assignment report

Run: `icpm2027_e1_label_list_strict_rep2` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Uncomplicated recovery (`uncomplicated_recovery`)

The case follows a standard course to discharge, with no recorded escalation of care and no extended observation beyond the ordinary stay pattern.

**Taxonomy-derivation rationale (Step 5):** The baseline disposition category against which the other four represent some departure — either in duration, care intensity, or discharge circumstance.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 315/846 variants (37.2%) · micro 341/1050 cases (32.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 7.50, nearest other category `early_or_irregular_discharge` at mean distance 8.38

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.285, nearest other category `extended_monitoring_recovery` at mean distance 0.313

## Extended monitoring before discharge (`extended_monitoring_recovery`)

The case recovers without escalation of care, but the trace shows a materially longer observation period than the uncomplicated pattern before discharge.

**Taxonomy-derivation rationale (Step 5):** Separates duration from severity: a longer stay is not, on its own, evidence that care was escalated.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 93/846 variants (11.0%) · micro 107/1050 cases (10.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 16.55, nearest other category `uncomplicated_recovery` at mean distance 13.57

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.303, nearest other category `uncomplicated_recovery` at mean distance 0.313

## Escalation of care during the stay (`care_escalation_during_stay`)

The trace shows an increase in care intensity at some point after admission (e.g., a transfer to a higher level of care) followed by eventual discharge.

**Taxonomy-derivation rationale (Step 5):** Captures cases whose clinical course was non-monotonic — an escalation mid-stay — independent of which specific unit received the transfer.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 88/846 variants (10.4%) · micro 88/1050 cases (8.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 25.25, nearest other category `non_home_disposition` at mean distance 21.66

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.317, nearest other category `non_home_disposition` at mean distance 0.392

## Early or irregular discharge (`early_or_irregular_discharge`)

The trace ends in a discharge that departs from the standard pattern captured by the other categories — e.g., an unusually short stay relative to the case's recorded severity indicators, suggesting discharge ahead of the typical course.

**Taxonomy-derivation rationale (Step 5):** A residual pattern distinct from non_home_disposition: the case still ends in a discharge event, just not one following the ordinary course.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 60/846 variants (7.1%) · micro 70/1050 cases (6.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.76, nearest other category `uncomplicated_recovery` at mean distance 8.38

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.496, nearest other category `uncomplicated_recovery` at mean distance 0.672

## Non-home disposition (`non_home_disposition`)

The trace ends in a disposition other than a routine discharge — e.g., in-hospital death or transfer to another facility — rather than release to the patient's prior living situation.

**Taxonomy-derivation rationale (Step 5):** The most severe disposition category, kept separate because it reflects a different kind of case ending than any discharge-based category.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 228/846 variants (27.0%) · micro 237/1050 cases (22.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 8.98, nearest other category `uncomplicated_recovery` at mean distance 9.25

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.187, nearest other category `care_escalation_during_stay` at mean distance 0.392

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0018` / `V0710` (category `extended_monitoring_recovery`): structural=178, profile=0.765
- `V0022` / `V0710` (category `extended_monitoring_recovery`): structural=178, profile=0.765
- `V0710` / `V0783` (category `extended_monitoring_recovery`): structural=178, profile=0.569
- `V0033` / `V0710` (category `extended_monitoring_recovery`): structural=177, profile=0.597
- `V0156` / `V0710` (category `extended_monitoring_recovery`): structural=177, profile=0.655
- `V0015` / `V0710` (category `extended_monitoring_recovery`): structural=176, profile=0.611
- `V0016` / `V0710` (category `extended_monitoring_recovery`): structural=176, profile=0.598
- `V0073` / `V0710` (category `extended_monitoring_recovery`): structural=176, profile=0.589
- `V0647` / `V0710` (category `extended_monitoring_recovery`): structural=176, profile=0.590
- `V0710` / `V0719` (category `extended_monitoring_recovery`): structural=176, profile=0.527

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

62/846 variants (7.3%), 207/1050 cases (19.7%) unassigned.

- `V0001`: The trace stops at ER Sepsis Triage without reaching a final disposition or admission, meaning it represents an incomplete or unadmitted emergency visit rather than a completed recovery path.
- `V0002`: The trace ends at CRP laboratory work without admission or discharge disposition, representing an incomplete episode.
- `V0003`: The trace terminates at Leucocytes without an admission or disposition outcome, representing an incomplete episode.
- `V0004`: The trace ends with IV Antibiotics administration in the emergency setting without an admission or final discharge recorded.
- `V0005`: The trace ends at LacticAcid without admission or discharge.
- `V0006`: The trace ends with IV Antibiotics in the emergency phase without proceeding to admission or final disposition.
- `V0007`: The trace ends with IV Antibiotics administration without a recorded hospital admission or formal discharge event.
- `V0009`: The trace concludes with IV Antibiotics in the emergency department without admission or final disposition.
- `V0010`: The trace ends unexpectedly at ER Sepsis Triage following initial lab work, without admission or discharge.
- `V0011`: The trace ends with IV Antibiotics in the emergency setting without leading to admission or formal discharge.
- `V0012`: The trace terminates with IV Antibiotics without admission or discharge disposition.
- `V0013`: The trace ends at Leucocytes without an admission or discharge outcome.
- `V0017`: The trace ends at ER Sepsis Triage without an admission or discharge disposition.
- `V0019`: The trace concludes with IV Antibiotics administration in the emergency area without hospital admission or final discharge.
- `V0020`: The trace ends with CRP lab work without admission or discharge disposition.
- `V0024`: The trace ends upon admission to normal care (Admission NC) without a final discharge or disposition event recorded.
- `V0025`: The trace finishes with IV Antibiotics in the emergency setting without any admission or discharge recorded.
- `V0056`: The trace ends in IV Antibiotics rather than a recognized final disposition state or discharge, placing it outside standard completed paths.
- `V0062`: Incomplete trace ending at IV Antibiotics without final discharge or disposition.
- `V0081`: The trace ends in an intermediate activity (IV Liquid) rather than a final disposition, meaning it does not fit any complete recovery or discharge category.
- `V0088`: The trace terminates at IV Antibiotics without reaching a discharge or final disposition activity.
- `V0092`: The trace terminates prematurely at LacticAcid before any admission or discharge disposition.
- `V0127`: The trace terminates at LacticAcid during initial evaluation without reaching a final discharge or disposition.
- `V0132`: The trace ends abruptly at IV Antibiotics without reaching a discharge or disposition.
- `V0133`: The trace stops at IV Antibiotics in the early phase without a final disposition.
- `V0137`: The trace terminates at LacticAcid without completing a hospital stay or discharge.
- `V0146`: The trace ends prematurely at Leucocytes without reaching a discharge disposition.
- `V0148`: The trace terminates at IV Antibiotics without reaching a discharge or disposition event.
- `V0287`: The trace terminates prematurely at CRP without an admission or final disposition.
- `V0292`: Incomplete trace ending in Leucocytes without an admission or disposition.
- `V0295`: Trace ends at IV Antibiotics without recording a final discharge or disposition.
- `V0330`: Incomplete stay ending prematurely at IV Liquid without a final disposition.
- `V0336`: Incomplete stay ending abruptly at CRP.
- `V0342`: Incomplete sequence terminating at CRP.
- `V0349`: Incomplete trace ending at ER Sepsis Triage.
- `V0501`: The trace ends in IV Liquid and does not reach a final disposition like routine discharge or transfer.
- `V0502`: The trace stops at Admission NC and lacks a final discharge outcome.
- `V0507`: The trace ends in IV Antibiotics without reaching a discharge disposition.
- `V0510`: The trace ends in IV Antibiotics without concluding with a discharge.
- `V0516`: The trace ends in Leucocytes without reaching a discharge.
- `V0517`: Incomplete trace ending in ER Triage.
- `V0549`: The trace ends in IV Liquid and does not have a terminal discharge or disposition outcome, making it part of the residual.
- `V0580`: The trace is incomplete and does not reach a final disposition or discharge.
- `V0584`: The trace is incomplete and does not reach a final disposition or discharge.
- `V0585`: The trace is incomplete and does not reach a final disposition or discharge.
- `V0587`: The trace is incomplete and does not reach a final disposition or discharge.
- `V0592`: The trace is incomplete and does not reach a final disposition or discharge.
- `V0636`: The trace ends prematurely at LacticAcid without any recorded discharge or final disposition event.
- `V0644`: The trace ends on CRP without a recorded discharge or terminal disposition.
- `V0645`: The trace ends abruptly on LacticAcid without a final disposition or discharge.
- `V0676`: The narrative ends in an intermediate activity (IV Antibiotics) rather than a final disposition, fitting none of the recovery or discharge categories.
- `V0679`: The trace terminates at IV Antibiotics without reaching a completion or discharge event.
- `V0685`: The trace stops abruptly at IV Antibiotics and lacks a final disposition.
- `V0689`: The narrative terminates at IV Antibiotics without a completed disposition.
- `V0694`: The trace cuts off at ER Sepsis Triage and does not reach a discharge or final outcome.
- `V0742`: The trace terminates prematurely at LacticAcid before any completion or discharge outcome is recorded, making it part of the residual.
- `V0750`: The sequence terminates at IV Antibiotics without an actual discharge or disposition outcome, leaving it in the residual.
- `V0759`: Incomplete trace ending prematurely at IV Antibiotics; does not reach a final disposition or fit standard categories.
- `V0764`: Truncated trace ending at ER Sepsis Triage without completion of treatment or discharge.
- `V0772`: Incomplete log ending abruptly on a CRP measurement without a final disposition.
- `V0774`: Incomplete trace ending at ER Sepsis Triage.
- `V0775`: Incomplete sequence terminating at CRP measurement.
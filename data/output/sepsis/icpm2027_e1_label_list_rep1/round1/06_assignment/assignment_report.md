# Step 6 — Narrative assignment report

Run: `icpm2027_e1_label_list_rep1` | Log: `sepsis` | Taxonomy mode: `open` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Uncomplicated recovery (`uncomplicated_recovery`)

The case follows a standard course to discharge, with no recorded escalation of care and no extended observation beyond the ordinary stay pattern.

**Taxonomy-derivation rationale (Step 5):** The baseline disposition category against which the other four represent some departure — either in duration, care intensity, or discharge circumstance.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 322/846 variants (38.1%) · micro 346/1050 cases (33.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 7.68, nearest other category `early_or_irregular_discharge` at mean distance 8.54

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.299, nearest other category `extended_monitoring_recovery` at mean distance 0.358

## Extended monitoring before discharge (`extended_monitoring_recovery`)

The case recovers without escalation of care, but the trace shows a materially longer observation period than the uncomplicated pattern before discharge.

**Taxonomy-derivation rationale (Step 5):** Separates duration from severity: a longer stay is not, on its own, evidence that care was escalated.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 117/846 variants (13.8%) · micro 131/1050 cases (12.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 12.76, nearest other category `uncomplicated_recovery` at mean distance 11.30

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.346, nearest other category `uncomplicated_recovery` at mean distance 0.358

## Escalation of care during the stay (`care_escalation_during_stay`)

The trace shows an increase in care intensity at some point after admission (e.g., a transfer to a higher level of care) followed by eventual discharge.

**Taxonomy-derivation rationale (Step 5):** Captures cases whose clinical course was non-monotonic — an escalation mid-stay — independent of which specific unit received the transfer.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 82/846 variants (9.7%) · micro 82/1050 cases (7.8%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 27.90, nearest other category `extended_monitoring_recovery` at mean distance 22.85

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.315, nearest other category `extended_monitoring_recovery` at mean distance 0.384

## Early or irregular discharge (`early_or_irregular_discharge`)

The trace ends in a discharge that departs from the standard pattern captured by the other categories — e.g., an unusually short stay relative to the case's recorded severity indicators, suggesting discharge ahead of the typical course.

**Taxonomy-derivation rationale (Step 5):** A residual pattern distinct from non_home_disposition: the case still ends in a discharge event, just not one following the ordinary course.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 65/846 variants (7.7%) · micro 77/1050 cases (7.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.70, nearest other category `uncomplicated_recovery` at mean distance 8.54

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.512, nearest other category `uncomplicated_recovery` at mean distance 0.677

## Non-home disposition (`non_home_disposition`)

The trace ends in a disposition other than a routine discharge — e.g., in-hospital death or transfer to another facility — rather than release to the patient's prior living situation.

**Taxonomy-derivation rationale (Step 5):** The most severe disposition category, kept separate because it reflects a different kind of case ending than any discharge-based category.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 198/846 variants (23.4%) · micro 202/1050 cases (19.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 10.16, nearest other category `uncomplicated_recovery` at mean distance 9.93

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.195, nearest other category `care_escalation_during_stay` at mean distance 0.392

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0082` / `V0710` (category `care_escalation_during_stay`): structural=176, profile=0.680
- `V0407` / `V0710` (category `care_escalation_during_stay`): structural=174, profile=0.624
- `V0710` / `V0793` (category `care_escalation_during_stay`): structural=174, profile=0.480
- `V0639` / `V0710` (category `care_escalation_during_stay`): structural=173, profile=0.375
- `V0710` / `V0715` (category `care_escalation_during_stay`): structural=173, profile=0.556
- `V0154` / `V0710` (category `care_escalation_during_stay`): structural=172, profile=0.338
- `V0391` / `V0710` (category `care_escalation_during_stay`): structural=172, profile=0.513
- `V0542` / `V0710` (category `care_escalation_during_stay`): structural=172, profile=0.507
- `V0655` / `V0710` (category `care_escalation_during_stay`): structural=172, profile=0.436
- `V0682` / `V0710` (category `care_escalation_during_stay`): structural=172, profile=0.428

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0015` (`extended_monitoring_recovery`) / `V0116` (`non_home_disposition`): structural=1, profile=0.429
- `V0015` (`extended_monitoring_recovery`) / `V0758` (`uncomplicated_recovery`): structural=1, profile=0.120
- `V0016` (`extended_monitoring_recovery`) / `V0362` (`uncomplicated_recovery`): structural=1, profile=0.006
- `V0016` (`extended_monitoring_recovery`) / `V0431` (`uncomplicated_recovery`): structural=1, profile=0.002
- `V0022` (`uncomplicated_recovery`) / `V0274` (`non_home_disposition`): structural=1, profile=0.374
- `V0022` (`uncomplicated_recovery`) / `V0415` (`early_or_irregular_discharge`): structural=1, profile=0.428
- `V0023` (`non_home_disposition`) / `V0697` (`uncomplicated_recovery`): structural=1, profile=0.410
- `V0035` (`uncomplicated_recovery`) / `V0395` (`extended_monitoring_recovery`): structural=1, profile=0.004
- `V0040` (`early_or_irregular_discharge`) / `V0503` (`uncomplicated_recovery`): structural=1, profile=0.387
- `V0041` (`extended_monitoring_recovery`) / `V0647` (`uncomplicated_recovery`): structural=1, profile=0.123

## Residual

62/846 variants (7.3%), 212/1050 cases (20.2%) unassigned.

- `V0001`: This trace ends in ER Sepsis Triage and does not proceed to admission or complete a full recovery/discharge cycle.
- `V0002`: The trace terminates at CRP testing in the ER without admission or final disposition.
- `V0003`: The trace terminates at Leucocytes testing in the ER without admission or final disposition.
- `V0004`: The trace terminates at IV Antibiotics administration in the ER without proceeding to an inpatient admission.
- `V0005`: The trace terminates at LacticAcid testing in the ER without admission or final disposition.
- `V0006`: The trace terminates at IV Antibiotics in the ER without an inpatient stay.
- `V0007`: The trace terminates at IV Antibiotics in the ER without an inpatient stay.
- `V0009`: The trace terminates at IV Antibiotics in the ER without an inpatient stay or formal disposition.
- `V0010`: The trace terminates at ER Sepsis Triage and does not result in an inpatient stay or discharge.
- `V0011`: The trace terminates at IV Antibiotics in the ER without an inpatient stay.
- `V0012`: The trace terminates at IV Antibiotics in the ER without proceeding to admission.
- `V0013`: The trace terminates at Leucocytes testing in the ER without an inpatient stay.
- `V0017`: The trace terminates at ER Sepsis Triage without progressing to admission or discharge.
- `V0019`: The trace terminates at IV Antibiotics in the ER without an inpatient stay.
- `V0020`: The trace terminates at CRP testing in the ER without admission or final disposition.
- `V0024`: The trace ends at Admission NC, lacking a final recorded discharge or disposition.
- `V0025`: The trace terminates at IV Antibiotics in the ER without an inpatient stay.
- `V0026`: The trace ends in a return to the ER after release, which does not fit standard uncomplicated recovery or other specific categories since it is not a direct inpatient care escalation.
- `V0028`: The trace features an extended duration with a return to the ER following release, which does not cleanly map to routine recovery categories.
- `V0032`: Involves a return to the ER after release, representing a post-discharge event rather than an inpatient escalation.
- `V0033`: Features a very long span before returning to the ER, not fitting the standard inpatient recovery definitions.
- `V0045`: Includes a return to the ER after release, which falls outside the standard inpatient recovery taxonomy.
- `V0049`: Long duration ending in a return to the ER, not fitting standard recovery definitions.
- `V0081`: The trace terminates abruptly at IV Liquid without reaching a discharge or disposition activity.
- `V0088`: The trace stops at IV Antibiotics without concluding with a discharge or disposition event.
- `V0092`: The trace ends abruptly at LacticAcid without any final discharge or disposition event.
- `V0127`: The variant ends in LacticAcid without completing a full admission or discharge course.
- `V0132`: The trace terminates prematurely at IV Antibiotics without reaching a disposition.
- `V0133`: The trace terminates at IV Antibiotics with no completed admission or release.
- `V0137`: The trace ends in LacticAcid without completing an admission or discharge sequence.
- `V0146`: The trace ends abruptly at Leucocytes without reaching a disposition or discharge.
- `V0148`: The sequence terminates at IV Antibiotics without an admission or release phase.
- `V0330`: The trace is incomplete, ending abruptly at IV Liquid without reaching a final discharge or release activity.
- `V0336`: The trace terminates prematurely on a lab test (CRP) rather than reaching a definitive disposition or release activity.
- `V0342`: The trace ends prematurely at a lab test (CRP) and lacks a proper discharge or disposition event.
- `V0349`: The sequence is an incomplete or irregular ER-only trace ending at ER Sepsis Triage without an admission or disposition.
- `V0411`: The trace has an irregular and incomplete path ending in diagnostic tests rather than a standard discharge or disposition.
- `V0462`: The outcome is incomplete (CRP), making standard categorization ambiguous.
- `V0501`: The narrative terminates at IV Liquid without reaching a discharge or final disposition step, making it incomplete regarding a full hospital course.
- `V0502`: The trace ends abruptly at Admission NC, lacking a final disposition or completion stage.
- `V0507`: The trace terminates at IV Antibiotics without admission or final disposition, representing an incomplete or truncated observation.
- `V0510`: The trace ends at IV Antibiotics inside the emergency setting without an inpatient admission or final outcome.
- `V0516`: The trace finishes at Leucocytes without an inpatient admission or final disposition.
- `V0517`: The narrative loops back to ER Triage and terminates prematurely without progressing to admission or discharge.
- `V0580`: The trace ends abruptly at CRP without a final discharge or release activity, falling outside standard complete paths.
- `V0584`: The trace terminates at IV Liquid rather than a discharge or release event.
- `V0585`: The trace terminates at LacticAcid rather than a discharge or release event.
- `V0587`: The trace terminates at CRP without reaching a disposition or release event.
- `V0592`: The trace terminates at IV Antibiotics without reaching a discharge or release event.
- `V0676`: The narrative ends in IV Antibiotics rather than a discharge or other disposition, so none of the completion-based categories fit.
- `V0677`: The trace does not fit a clean recovery pattern, ending in Return ER after a prolonged overall span without matching specific monitored criteria.
- `V0679`: The trace ends prematurely at IV Antibiotics without an admission or final disposition.
- `V0685`: The process trace stops at IV Antibiotics and lacks a final disposition.
- `V0689`: The trace terminates at IV Antibiotics without reaching a discharge disposition.
- `V0694`: The trace is very short and terminates at ER Sepsis Triage, never reaching admission or discharge.
- `V0703`: The trace terminates abruptly at IV Liquid before any formal discharge or release activity, fitting none of the standard categories.
- `V0707`: The trace halts at Admission NC without reaching any final disposition or release status.
- `V0708`: The trace ends prematurely at IV Antibiotics without concluding with a discharge or release event.
- `V0713`: The sequence ends at IV Antibiotics without completing a discharge process.
- `V0826`: The narrative ends in 'Admission NC' rather than a final discharge or typical outcome.
- `V0832`: The trace terminates abruptly at 'IV Antibiotics' without proceeding to admission or discharge.
- `V0843`: The trace terminates at 'IV Liquid' without reaching a discharge or completion outcome.
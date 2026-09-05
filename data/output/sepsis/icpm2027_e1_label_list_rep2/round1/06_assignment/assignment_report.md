# Step 6 — Narrative assignment report

Run: `icpm2027_e1_label_list_rep2` | Log: `sepsis` | Taxonomy mode: `open` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Uncomplicated recovery (`uncomplicated_recovery`)

The case follows a standard course to discharge, with no recorded escalation of care and no extended observation beyond the ordinary stay pattern.

**Taxonomy-derivation rationale (Step 5):** The baseline disposition category against which the other four represent some departure — either in duration, care intensity, or discharge circumstance.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 312/846 variants (36.9%) · micro 333/1050 cases (31.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 7.68, nearest other category `early_or_irregular_discharge` at mean distance 8.51

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.291, nearest other category `extended_monitoring_recovery` at mean distance 0.313

## Extended monitoring before discharge (`extended_monitoring_recovery`)

The case recovers without escalation of care, but the trace shows a materially longer observation period than the uncomplicated pattern before discharge.

**Taxonomy-derivation rationale (Step 5):** Separates duration from severity: a longer stay is not, on its own, evidence that care was escalated.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 100/846 variants (11.8%) · micro 113/1050 cases (10.8%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.75, nearest other category `uncomplicated_recovery` at mean distance 10.78

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.301, nearest other category `uncomplicated_recovery` at mean distance 0.313

## Escalation of care during the stay (`care_escalation_during_stay`)

The trace shows an increase in care intensity at some point after admission (e.g., a transfer to a higher level of care) followed by eventual discharge.

**Taxonomy-derivation rationale (Step 5):** Captures cases whose clinical course was non-monotonic — an escalation mid-stay — independent of which specific unit received the transfer.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 87/846 variants (10.3%) · micro 87/1050 cases (8.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 28.35, nearest other category `extended_monitoring_recovery` at mean distance 22.86

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.322, nearest other category `extended_monitoring_recovery` at mean distance 0.388

## Early or irregular discharge (`early_or_irregular_discharge`)

The trace ends in a discharge that departs from the standard pattern captured by the other categories — e.g., an unusually short stay relative to the case's recorded severity indicators, suggesting discharge ahead of the typical course.

**Taxonomy-derivation rationale (Step 5):** A residual pattern distinct from non_home_disposition: the case still ends in a discharge event, just not one following the ordinary course.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 68/846 variants (8.0%) · micro 82/1050 cases (7.8%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 6.13, nearest other category `uncomplicated_recovery` at mean distance 8.51

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.549, nearest other category `uncomplicated_recovery` at mean distance 0.662

## Non-home disposition (`non_home_disposition`)

The trace ends in a disposition other than a routine discharge — e.g., in-hospital death or transfer to another facility — rather than release to the patient's prior living situation.

**Taxonomy-derivation rationale (Step 5):** The most severe disposition category, kept separate because it reflects a different kind of case ending than any discharge-based category.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 215/846 variants (25.4%) · micro 219/1050 cases (20.9%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 9.94, nearest other category `uncomplicated_recovery` at mean distance 9.81

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.191, nearest other category `care_escalation_during_stay` at mean distance 0.396

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0082` / `V0710` (category `care_escalation_during_stay`): structural=176, profile=0.680
- `V0141` / `V0710` (category `care_escalation_during_stay`): structural=174, profile=0.418
- `V0407` / `V0710` (category `care_escalation_during_stay`): structural=174, profile=0.624
- `V0710` / `V0793` (category `care_escalation_during_stay`): structural=174, profile=0.480
- `V0068` / `V0710` (category `care_escalation_during_stay`): structural=173, profile=0.509
- `V0639` / `V0710` (category `care_escalation_during_stay`): structural=173, profile=0.375
- `V0710` / `V0715` (category `care_escalation_during_stay`): structural=173, profile=0.556
- `V0154` / `V0710` (category `care_escalation_during_stay`): structural=172, profile=0.338
- `V0391` / `V0710` (category `care_escalation_during_stay`): structural=172, profile=0.513
- `V0542` / `V0710` (category `care_escalation_during_stay`): structural=172, profile=0.507

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0008` (`uncomplicated_recovery`) / `V0686` (`non_home_disposition`): structural=1, profile=0.454
- `V0008` (`uncomplicated_recovery`) / `V0706` (`early_or_irregular_discharge`): structural=1, profile=0.029
- `V0015` (`extended_monitoring_recovery`) / `V0116` (`non_home_disposition`): structural=1, profile=0.429
- `V0015` (`extended_monitoring_recovery`) / `V0758` (`uncomplicated_recovery`): structural=1, profile=0.120
- `V0016` (`extended_monitoring_recovery`) / `V0041` (`uncomplicated_recovery`): structural=1, profile=0.115
- `V0016` (`extended_monitoring_recovery`) / `V0052` (`early_or_irregular_discharge`): structural=1, profile=0.429
- `V0016` (`extended_monitoring_recovery`) / `V0362` (`uncomplicated_recovery`): structural=1, profile=0.006
- `V0016` (`extended_monitoring_recovery`) / `V0431` (`uncomplicated_recovery`): structural=1, profile=0.002
- `V0018` (`extended_monitoring_recovery`) / `V0096` (`uncomplicated_recovery`): structural=1, profile=0.342
- `V0022` (`uncomplicated_recovery`) / `V0274` (`non_home_disposition`): structural=1, profile=0.374

## Residual

64/846 variants (7.6%), 216/1050 cases (20.6%) unassigned.

- `V0001`: This narrative stops at ER Sepsis Triage and does not result in admission or final disposition, representing an incomplete or abandoned ED visit rather than a completed recovery or hospital stay.
- `V0002`: The trace ends at CRP laboratory testing within the emergency department without admission or final disposition, falling outside the standard completed hospital stay patterns.
- `V0003`: The trace terminates at Leucocytes testing in the emergency department without reaching an admission or discharge disposition.
- `V0004`: The trace ends after administering IV Antibiotics in the emergency department without any subsequent admission or discharge event.
- `V0005`: The trace ends at LacticAcid testing in the emergency department without proceeding to admission or discharge.
- `V0006`: The trace concludes with IV Antibiotics in the emergency department and lacks an inpatient admission or final release disposition.
- `V0007`: The trace ends at IV Antibiotics in the emergency setting without an admission or formal discharge event.
- `V0009`: The trace finishes at IV Antibiotics in the emergency department without an inpatient admission or final disposition.
- `V0010`: The trace ends with an out-of-order ER Sepsis Triage event and lacks a proper hospital admission or final discharge disposition.
- `V0011`: The trace terminates at IV Antibiotics in the emergency department without admission or discharge tracking.
- `V0012`: The trace ends with IV Antibiotics in the emergency department without proceeding to admission or release.
- `V0013`: The trace ends at Leucocytes testing in the emergency department without inpatient admission or discharge.
- `V0017`: The trace features an atypical sequence ending back at ER Sepsis Triage without an admission or final discharge.
- `V0019`: The trace terminates at IV Antibiotics in the emergency department without an inpatient admission or discharge disposition.
- `V0020`: The trace ends at CRP testing in the emergency department without an admission or formal release.
- `V0024`: The trace stops abruptly at Admission NC without showing the subsequent hospital stay or final discharge disposition.
- `V0025`: The trace ends at IV Antibiotics in the emergency department without an inpatient admission or final release.
- `V0026`: The trace ends in a Return ER outcome after release, which reflects a readmission rather than a simple recovery or standard inpatient escalation, but it does not cleanly fit standard care escalation or non-home disposition categories.
- `V0028`: The case involves a lengthy stay and a return to ER, but the extended duration combined with a readmission does not cleanly fit the standard categories.
- `V0032`: The case has a multi-day admission with repeat labs leading to Release A, followed later by a Return ER, representing a readmission pattern.
- `V0033`: Involves a prolonged timeline resulting in a Return ER, not fitting straightforward inpatient recovery.
- `V0045`: Inpatient admission followed by release and subsequent Return ER, representing a readmission pattern.
- `V0049`: Extended timeline with a final outcome of Return ER.
- `V0056`: Trace ends prematurely at IV Antibiotics without admission or final disposition.
- `V0062`: Trace terminates at IV Antibiotics without reaching disposition or admission.
- `V0081`: The case does not reach a terminal discharge or release state, ending instead in IV Liquid.
- `V0088`: The case terminates prematurely at IV Antibiotics without a final disposition.
- `V0092`: The trace ends mid-process at LacticAcid without any discharge or release.
- `V0127`: The trace ends in LacticAcid without any final discharge or disposition event, remaining incomplete in terms of taxonomy pathways.
- `V0132`: Terminates at IV Antibiotics without reaching a discharge or disposition milestone.
- `V0133`: Terminates at IV Antibiotics with no discharge or disposition outcome recorded.
- `V0137`: Stops at LacticAcid without showing any discharge or disposition event.
- `V0146`: Incomplete trace ending in Leucocytes without discharge.
- `V0148`: Trace stops at IV Antibiotics without final disposition.
- `V0287`: The trace terminates prematurely at CRP without reaching a final discharge disposition, fitting none of the completed recovery categories.
- `V0292`: Trace terminates early at Leucocytes without reaching any discharge outcome.
- `V0295`: The trace ends abruptly at IV Antibiotics before any discharge or disposition activity occurs.
- `V0330`: The trace is incomplete, ending in IV Liquid without a final discharge disposition.
- `V0336`: The trace terminates abruptly at CRP rather than ending in a complete discharge disposition.
- `V0342`: Incomplete trace ending prematurely in CRP.
- `V0349`: Incomplete trace ending at ER Sepsis Triage.
- `V0462`: The outcome is an intermediate diagnostic activity (CRP) rather than a completed discharge or disposition.
- `V0501`: The trace stops at IV Liquid without reaching a final discharge or release outcome, making it incomplete regarding disposition.
- `V0502`: The trace terminates at Admission NC without a complete hospital stay or disposition outcome.
- `V0507`: The trace ends abruptly at IV Antibiotics without an admission or final disposition.
- `V0510`: The trace ends at IV Antibiotics with no admission or discharge recorded.
- `V0516`: The trace ends prematurely at Leucocytes without reaching a discharge or completion state.
- `V0517`: The trace stops at ER Triage without any admission or disposition.
- `V0636`: The trace ends abruptly with a lab activity (LacticAcid) rather than a final disposition or release.
- `V0644`: The trace ends abruptly with a lab activity (CRP) rather than a standard discharge or disposition.
- `V0645`: The trace terminates on a lab activity (LacticAcid) rather than a complete discharge disposition.
- `V0646`: The trace ends in a sequence of lab activities after an apparent return to ER, leaving no clear final disposition.
- `V0676`: The narrative stops at IV Antibiotics and does not reach a final disposition like discharge or transfer.
- `V0679`: The trace terminates at IV Antibiotics without a disposition.
- `V0685`: Ends at IV Antibiotics without final disposition.
- `V0689`: Trace stops at IV Antibiotics without disposition.
- `V0694`: Incomplete trace ending at ER Sepsis Triage.
- `V0703`: The trace terminates abruptly at IV Liquid before any admission or discharge disposition, leaving the disposition unclear.
- `V0707`: The trace stops at Admission NC with no final discharge recorded.
- `V0708`: The trace terminates at IV Antibiotics without an admission or discharge event.
- `V0713`: The trace ends at IV Antibiotics without completing a hospital stay or discharge.
- `V0826`: The narrative ends in 'Admission NC', which is an incomplete stay or intermediate state rather than a final discharge or typical recovery outcome.
- `V0832`: The trace ends abruptly at 'IV Antibiotics', which does not constitute a completed recovery or discharge event.
- `V0843`: The trace terminates at 'IV Liquid', which represents an incomplete or ongoing treatment sequence rather than a final disposition.
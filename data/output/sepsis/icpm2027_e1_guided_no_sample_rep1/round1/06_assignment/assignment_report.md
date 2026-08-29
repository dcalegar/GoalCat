# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_no_sample_rep1` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Patient admission ward routing (`admission_ward_routing`)

Represents the OR-decomposed choice of admitting the patient to either a non-critical inpatient ward or an intensive care unit, advancing the clinical pathway towards final disposition while influencing treatment timing metrics.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to the OR-decomposed parent goal id=5 encompassing Admission NC (id=15) and Admission IC (id=16). The IC admission path carries a contribution to minimize time-to-treatment softgoal evaluated via indicator id=24 and id=25.

**Goal-model linkage:** 5 (Goal): Patient is admitted to an inpatient ward

**Coverage:** macro 443/846 variants (52.4%) · micro 449/1050 cases (42.8%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 13.50, nearest other category `discharge_disposition` at mean distance 12.66

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.411, nearest other category `discharge_disposition` at mean distance 0.417

## Captured discharge disposition (`discharge_disposition`)

Represents the OR-decomposed alternative pathways for concluding an admitted sepsis case through one of the designated release routes, impacting the post-discharge ER return indicator and avoiding post-discharge deterioration.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to the OR-decomposed parent goal id=6 covering release variants Release A (id=17), Release B (id=18), Release C (id=19), Release D (id=20), and Release E (id=21). These alternatives connect to the Avoid post-discharge deterioration softgoal and are measured by post-discharge ER return indicator id=26.

**Goal-model linkage:** 6 (Goal): Admitted case reaches a captured discharge

**Coverage:** macro 313/846 variants (37.0%) · micro 359/1050 cases (34.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.63, nearest other category `admission_ward_routing` at mean distance 12.66

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.392, nearest other category `admission_ward_routing` at mean distance 0.417

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0286` / `V0710` (category `discharge_disposition`): structural=182, profile=0.756
- `V0497` / `V0710` (category `discharge_disposition`): structural=180, profile=0.751
- `V0008` / `V0710` (category `discharge_disposition`): structural=179, profile=0.770
- `V0014` / `V0710` (category `discharge_disposition`): structural=179, profile=0.766
- `V0399` / `V0710` (category `discharge_disposition`): structural=179, profile=0.861
- `V0424` / `V0710` (category `discharge_disposition`): structural=179, profile=0.731
- `V0550` / `V0710` (category `discharge_disposition`): structural=179, profile=0.682
- `V0710` / `V0731` (category `discharge_disposition`): structural=179, profile=0.688
- `V0018` / `V0710` (category `discharge_disposition`): structural=178, profile=0.765
- `V0022` / `V0710` (category `discharge_disposition`): structural=178, profile=0.765

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0008` (`discharge_disposition`) / `V0058` (`admission_ward_routing`): structural=1, profile=0.011
- `V0008` (`discharge_disposition`) / `V0686` (`admission_ward_routing`): structural=1, profile=0.454
- `V0008` (`discharge_disposition`) / `V0707` (`admission_ward_routing`): structural=1, profile=0.425
- `V0008` (`discharge_disposition`) / `V0766` (`admission_ward_routing`): structural=1, profile=0.336
- `V0014` (`discharge_disposition`) / `V0058` (`admission_ward_routing`): structural=1, profile=0.015
- `V0015` (`discharge_disposition`) / `V0758` (`admission_ward_routing`): structural=1, profile=0.120
- `V0016` (`discharge_disposition`) / `V0362` (`admission_ward_routing`): structural=1, profile=0.006
- `V0016` (`discharge_disposition`) / `V0462` (`admission_ward_routing`): structural=1, profile=0.392
- `V0018` (`discharge_disposition`) / `V0096` (`admission_ward_routing`): structural=1, profile=0.342
- `V0022` (`discharge_disposition`) / `V0415` (`admission_ward_routing`): structural=1, profile=0.428

## Residual

90/846 variants (10.6%), 242/1050 cases (23.0%) unassigned.

- `V0001`: The narrative stops at ER Sepsis Triage and does not reach ward routing or discharge disposition.
- `V0002`: The narrative ends at CRP testing during the diagnostic phase and does not involve ward admission or discharge.
- `V0003`: The narrative concludes with Leucocytes testing in the ER without proceeding to admission or discharge.
- `V0004`: The narrative stops at IV Antibiotics administration in the emergency phase without ward routing or discharge.
- `V0005`: The narrative ends with LacticAcid testing and does not reach downstream clinical pathways.
- `V0006`: The narrative concludes with IV Antibiotics and does not involve admission or final disposition.
- `V0007`: The narrative stops at IV Antibiotics administration in the ER without proceeding to admission or release.
- `V0009`: The narrative ends with IV Antibiotics during emergency treatment without further routing or disposition.
- `V0010`: The narrative terminates at ER Sepsis Triage and does not progress toward admission or discharge.
- `V0011`: The narrative concludes with IV Antibiotics administration and does not reach ward admission or release.
- `V0012`: The narrative stops at IV Antibiotics in the emergency department without inpatient routing or discharge.
- `V0013`: The narrative ends with Leucocytes testing in the ER, remaining entirely within the diagnostic phase.
- `V0017`: The narrative terminates at ER Sepsis Triage and does not involve ward routing or discharge.
- `V0019`: The narrative ends at IV Antibiotics without reaching inpatient admission or final release.
- `V0020`: The narrative concludes with CRP testing in the ER without proceeding to admission or discharge.
- `V0025`: The narrative stops at IV Antibiotics in the emergency department without inpatient routing or discharge.
- `V0027`: The narrative terminates at IV Antibiotics without progressing to admission or release.
- `V0029`: The narrative ends with Leucocytes testing and does not reach admission or discharge stages.
- `V0031`: The narrative concludes with LacticAcid testing in the ER without ward routing or disposition.
- `V0034`: The narrative ends at IV Liquid administration without proceeding to inpatient admission or discharge.
- `V0036`: The narrative terminates at CRP testing in the ER without further clinical routing or discharge.
- `V0038`: The narrative stops at IV Antibiotics in the emergency department without reaching admission or discharge.
- `V0043`: The narrative ends with LacticAcid testing in the ER without ward admission or discharge.
- `V0050`: The narrative terminates at CRP testing in the ER without proceeding to admission or discharge.
- `V0056`: The process terminates at IV Antibiotics without reaching ward routing or discharge disposition.
- `V0062`: The process stops at IV Antibiotics before ward admission or discharge.
- `V0081`: The trace terminates at IV Liquid without reaching ward routing or discharge.
- `V0088`: The sequence stops at IV Antibiotics without admission or discharge.
- `V0092`: The process ends at LacticAcid before any ward routing or discharge.
- `V0127`: The process stops at LacticAcid and does not reach ward routing or final discharge disposition.
- `V0132`: The pathway terminates at IV Antibiotics without proceeding to ward routing or final release.
- `V0133`: The process ends at IV Antibiotics and does not realize ward routing or discharge disposition.
- `V0137`: The narrative stops at LacticAcid, omitting ward routing and discharge disposition.
- `V0146`: The sequence terminates at Leucocytes without reaching ward routing or release.
- `V0148`: The narrative stops at IV Antibiotics, omitting ward routing and final disposition.
- `V0217`: The narrative stops at IV Antibiotics and does not reach an admission ward routing or final discharge disposition step.
- `V0219`: Terminates early at Leucocytes without advancing to ward routing or discharge.
- `V0232`: Stops at IV Antibiotics without reaching ward routing or discharge disposition.
- `V0234`: Ends at Leucocytes without advancing to admission or discharge.
- `V0260`: The pathway ends at IV Antibiotics without reaching ward admission or discharge disposition categories.
- `V0268`: The narrative stops at Leucocytes and does not involve ward routing or final discharge disposition.
- `V0287`: The variant terminates at CRP and does not reach ward routing or discharge steps.
- `V0292`: The variant ends at Leucocytes, lacking ward routing or discharge disposition activities.
- `V0295`: The pathway stops at IV Antibiotics after a non-critical ward admission, lacking a final discharge outcome.
- `V0302`: The narrative terminates at ER Sepsis Triage and does not reach ward routing or discharge disposition.
- `V0305`: The trace stops at IV Antibiotics in the emergency department without ward routing or discharge disposition.
- `V0322`: Terminates at IV Antibiotics without proceeding to ward routing or discharge.
- `V0325`: Ends at IV Antibiotics in the ER without reaching ward admission or discharge.
- `V0330`: Terminates at IV Liquid without reaching ward routing or discharge disposition.
- `V0342`: Terminates at CRP diagnostics without reaching ward admission or discharge.
- `V0349`: Terminates at ER Sepsis Triage without reaching ward admission or discharge disposition.
- `V0378`: The narrative terminates early at IV Antibiotics without reaching ward routing or discharge disposition.
- `V0379`: The narrative terminates early at IV Antibiotics without ward routing or final discharge.
- `V0417`: The variant terminates inside the ER with 'ER Triage' and does not reach ward admission or final discharge disposition.
- `V0429`: The process terminates at 'IV Antibiotics' within the ER and does not progress to ward routing or discharge disposition.
- `V0488`: The narrative terminates early at IV Liquid and does not reach ward admission or discharge disposition.
- `V0492`: The narrative terminates early at IV Liquid and does not contain ward admission or discharge disposition.
- `V0495`: The narrative terminates early at IV Antibiotics and does not reach ward admission or final discharge.
- `V0507`: The narrative stops at 'IV Antibiotics' and does not reach ward routing or discharge disposition phases.
- `V0510`: The process sequence halts at 'IV Antibiotics' without proceeding to admission or discharge steps.
- `V0516`: The narrative terminates early at diagnostic activities ('Leucocytes') without reaching admission or discharge.
- `V0517`: The sequence stops at an early stage ('ER Triage') and does not progress to ward routing or discharge.
- `V0549`: The process stops at 'IV Liquid' and does not progress to ward routing or discharge disposition phases.
- `V0575`: The narrative terminates early at Leucocytes without reaching a ward admission or a final discharge disposition.
- `V0580`: The narrative ends at CRP without progressing to ward admission or discharge disposition.
- `V0584`: The sequence stops at IV Liquid without advancing to ward admission or discharge disposition.
- `V0585`: The sequence terminates at LacticAcid without any ward routing or discharge steps.
- `V0587`: The process ends at CRP without proceeding to admission or discharge.
- `V0592`: The sequence stops at IV Antibiotics without reaching ward admission or discharge.
- `V0645`: The narrative terminates prematurely at LacticAcid without any admission or discharge disposition activities, so it fits neither category.
- `V0664`: The process terminates at IV Liquid before any ward admission or final discharge.
- `V0676`: The trace stops at IV Antibiotics without reaching ward routing or discharge disposition.
- `V0679`: Terminates early at IV Antibiotics before ward admission or discharge.
- `V0685`: Stops at IV Antibiotics without reaching ward admission or discharge.
- `V0689`: Trace ends at IV Antibiotics without proceeding to ward routing or disposition.
- `V0694`: Terminates early at ER Sepsis Triage before reaching ward admission or discharge.
- `V0703`: The pathway ends at IV Liquid and does not reach ward routing or discharge disposition.
- `V0713`: The pathway stops at IV Antibiotics and does not realize ward routing or discharge.
- `V0742`: The pathway terminates at LacticAcid and does not reach ward routing or discharge disposition.
- `V0750`: The pathway stops at IV Antibiotics and does not realize ward routing or discharge.
- `V0759`: The narrative ends at IV Antibiotics without reaching any ward admission or discharge disposition step.
- `V0764`: The narrative ends prematurely at ER Sepsis Triage and does not contain ward routing or discharge disposition.
- `V0774`: The narrative terminates early at ER Sepsis Triage without reaching any admission or discharge activities.
- `V0775`: The narrative stops at CRP and does not include ward routing or final discharge disposition.
- `V0777`: The narrative terminates at Leucocytes and lacks ward admission or discharge disposition.
- `V0778`: The narrative terminates at Leucocytes without reaching ward admission or discharge steps.
- `V0791`: The narrative ends at IV Antibiotics without containing any ward routing or discharge disposition.
- `V0816`: The narrative terminates at IV Antibiotics without any ward admission or final disposition routing.
- `V0820`: The variant terminates at LacticAcid measurement in the ER without reaching admission or disposition.
- `V0832`: The process terminates at IV Antibiotics in the ER without any ward routing or discharge disposition.
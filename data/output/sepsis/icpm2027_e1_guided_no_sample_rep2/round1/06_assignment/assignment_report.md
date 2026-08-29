# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_no_sample_rep2` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Admission Ward Pathway (`admission_ward_pathway`)

Represents the choices of admitting the patient to either a normal care ward or an intensive care unit. Admission IC negatively impacts the softgoal 'Minimize time-to-treatment' (SomeNegative -25), while both routes contribute toward the overarching goal of patient disposition under indicator evaluations.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the OR-decomposed goal element id 5 (Patient is admitted to an inpatient ward), which encompasses tasks Admission NC (15) and Admission IC (16). The goal model marks them mutually exclusive via OR/XOR, so they form the boundary of this admission pathway category.

**Goal-model linkage:** 5 (Goal): Patient is admitted to an inpatient ward

**Coverage:** macro 420/846 variants (49.6%) · micro 447/1050 cases (42.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 13.22, nearest other category `discharge_release_pathway` at mean distance 12.71

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.419, nearest other category `discharge_release_pathway` at mean distance 0.408

## Discharge Release Pathway (`discharge_release_pathway`)

Represents the multiple discharge release options (Release A through E) for admitted cases. Release A and Release B help advance the softgoal 'Avoid post-discharge deterioration' (+50), and performance is evaluated against post-discharge ER return indicators.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the OR-decomposed goal element id 6 (Admitted case reaches a captured discharge), which covers the alternative release tasks (17, 18, 19, 20, 21). These represent the distinct paths for completing patient care.

**Goal-model linkage:** 6 (Goal): Admitted case reaches a captured discharge

**Coverage:** macro 335/846 variants (39.6%) · micro 360/1050 cases (34.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 12.21, nearest other category `admission_ward_pathway` at mean distance 12.71

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.397, nearest other category `admission_ward_pathway` at mean distance 0.408

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0098` / `V0710` (category `discharge_release_pathway`): structural=179, profile=0.646
- `V0152` / `V0710` (category `discharge_release_pathway`): structural=179, profile=0.694
- `V0380` / `V0710` (category `discharge_release_pathway`): structural=179, profile=0.764
- `V0383` / `V0710` (category `discharge_release_pathway`): structural=179, profile=0.772
- `V0399` / `V0710` (category `discharge_release_pathway`): structural=179, profile=0.861
- `V0424` / `V0710` (category `discharge_release_pathway`): structural=179, profile=0.731
- `V0550` / `V0710` (category `discharge_release_pathway`): structural=179, profile=0.682
- `V0668` / `V0710` (category `discharge_release_pathway`): structural=179, profile=0.790
- `V0686` / `V0710` (category `discharge_release_pathway`): structural=179, profile=0.683
- `V0710` / `V0731` (category `discharge_release_pathway`): structural=179, profile=0.688

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0008` (`admission_ward_pathway`) / `V0686` (`discharge_release_pathway`): structural=1, profile=0.454
- `V0008` (`admission_ward_pathway`) / `V0706` (`discharge_release_pathway`): structural=1, profile=0.029
- `V0016` (`admission_ward_pathway`) / `V0041` (`discharge_release_pathway`): structural=1, profile=0.115
- `V0016` (`admission_ward_pathway`) / `V0052` (`discharge_release_pathway`): structural=1, profile=0.429
- `V0016` (`admission_ward_pathway`) / `V0362` (`discharge_release_pathway`): structural=1, profile=0.006
- `V0016` (`admission_ward_pathway`) / `V0431` (`discharge_release_pathway`): structural=1, profile=0.002
- `V0021` (`discharge_release_pathway`) / `V0124` (`admission_ward_pathway`): structural=1, profile=0.036
- `V0028` (`discharge_release_pathway`) / `V0100` (`admission_ward_pathway`): structural=1, profile=0.420
- `V0028` (`discharge_release_pathway`) / `V0307` (`admission_ward_pathway`): structural=1, profile=0.011
- `V0032` (`discharge_release_pathway`) / `V0237` (`admission_ward_pathway`): structural=1, profile=0.125

## Residual

91/846 variants (10.8%), 243/1050 cases (23.1%) unassigned.

- `V0001`: This variant ends at ER Sepsis Triage and does not reach an admission ward or discharge pathway.
- `V0002`: This variant terminates at CRP testing without proceeding to admission or discharge.
- `V0003`: This variant terminates at Leucocytes testing without reaching ward admission or discharge.
- `V0004`: This variant ends with IV Antibiotics and does not involve ward admission or release choices.
- `V0005`: This variant ends at LacticAcid testing without admission or discharge activities.
- `V0006`: This variant terminates at IV Antibiotics without proceeding to ward admission or discharge.
- `V0007`: This variant ends at IV Antibiotics and does not include admission or release actions.
- `V0009`: Terminates at IV Antibiotics without admission or discharge pathways.
- `V0010`: Ends at ER Sepsis Triage without reaching admission or discharge.
- `V0011`: Ends at IV Antibiotics without reaching ward admission or discharge.
- `V0012`: Ends at IV Antibiotics without admission or discharge actions.
- `V0013`: Terminates at Leucocytes testing without admission or discharge.
- `V0017`: Terminates at ER Sepsis Triage without reaching admission or discharge.
- `V0019`: Ends at IV Antibiotics without admission or discharge pathways.
- `V0020`: Terminates at CRP without admission or discharge actions.
- `V0025`: Terminates at IV Antibiotics without admission or discharge.
- `V0027`: Terminates at IV Antibiotics without admission or discharge.
- `V0029`: Terminates at Leucocytes without admission or discharge.
- `V0031`: Terminates at LacticAcid without admission or discharge.
- `V0034`: Terminates at IV Liquid without admission or discharge.
- `V0036`: Terminates at CRP without admission or discharge.
- `V0038`: Terminates at IV Antibiotics without admission or discharge.
- `V0043`: Terminates at LacticAcid without admission or discharge.
- `V0050`: Terminates at CRP without admission or discharge.
- `V0056`: The narrative terminates at IV Antibiotics without reaching ward admission or discharge release pathways.
- `V0062`: The narrative terminates at IV Antibiotics without reaching ward admission or discharge release pathways.
- `V0081`: The narrative terminates at IV Liquid without reaching ward admission or discharge release pathways.
- `V0088`: The narrative terminates at IV Antibiotics without reaching ward admission or discharge release pathways.
- `V0092`: The narrative terminates at LacticAcid without reaching ward admission or discharge release pathways.
- `V0127`: The narrative ends at LacticAcid without any ward admission or discharge option.
- `V0132`: The narrative ends at IV Antibiotics without reaching a ward admission or discharge step.
- `V0133`: The narrative ends at IV Antibiotics without reaching a ward admission or discharge step.
- `V0137`: The narrative ends at LacticAcid without reaching a ward admission or discharge step.
- `V0146`: The narrative terminates at Leucocytes without including ward admission or discharge options.
- `V0148`: The narrative terminates at IV Antibiotics without any ward admission or discharge option.
- `V0187`: The narrative stops at CRP and does not reach an admission decision or a discharge release option.
- `V0197`: The narrative ends with Leucocytes and does not contain admission or release choices.
- `V0217`: The variant ends at IV Antibiotics without any ward admission or discharge/release activity, so neither pathway category fits.
- `V0219`: The variant terminates at Leucocytes without an admission or release activity, fitting neither category.
- `V0232`: The variant terminates at IV Antibiotics without proceeding to ward admission or discharge/release.
- `V0234`: The variant terminates at Leucocytes without an admission or release event, fitting neither category.
- `V0260`: The process terminates at IV Antibiotics without involving ward admission or any release option, so it fits neither category.
- `V0287`: The process terminates at CRP without involving ward admission or discharge options, so it fits neither category.
- `V0292`: The process terminates at Leucocytes without involving ward admission or discharge options, so it fits neither category.
- `V0302`: The trace ends at ER Sepsis Triage and does not reach any ward admission or discharge release steps.
- `V0305`: The trace stops at IV Antibiotics in the ER and does not proceed to admission or discharge categories.
- `V0322`: Ends at IV Antibiotics without proceeding to ward admission or discharge release categories.
- `V0325`: Terminates at IV Antibiotics without entering the ward admission or discharge pathways.
- `V0330`: Ends at IV Liquid without reaching ward admission or discharge release steps.
- `V0342`: Terminates at CRP and does not enter ward admission or discharge pathways.
- `V0349`: Terminates at ER Sepsis Triage without reaching any ward admission or discharge steps.
- `V0374`: The narrative terminates at Leucocytes without reaching a ward admission or a discharge release option.
- `V0378`: Terminates at IV Antibiotics prior to any ward admission or release.
- `V0379`: Terminates at IV Antibiotics without reaching admission or release.
- `V0417`: The narrative ends in ER Triage and does not reach an admission ward or discharge release milestone.
- `V0429`: The narrative ends at IV Antibiotics without proceeding to a ward admission or discharge release.
- `V0488`: Does not reach an admission or discharge pathway as it terminates at IV Liquid.
- `V0492`: Does not reach an admission or discharge pathway as it terminates at IV Liquid.
- `V0495`: Does not reach an admission or discharge pathway as it terminates at IV Antibiotics.
- `V0507`: The narrative ends with IV Antibiotics and does not reach an admission ward or discharge pathway.
- `V0510`: The narrative terminates at IV Antibiotics without admission or discharge activities.
- `V0516`: The variant ends at Leucocytes and lacks any admission or discharge pathway actions.
- `V0517`: The narrative stops at ER Triage without progressing to admission or discharge.
- `V0549`: The narrative terminates at IV Liquid without admission or discharge activities.
- `V0575`: The narrative stops at Leucocytes and does not contain any admission or discharge pathway events.
- `V0580`: The narrative stops at CRP and does not contain any admission or discharge pathway events.
- `V0584`: The narrative stops at IV Liquid and does not contain any admission or discharge pathway events.
- `V0585`: The narrative stops at LacticAcid and does not contain any admission or discharge pathway events.
- `V0587`: The narrative stops at CRP and does not contain any admission or discharge pathway events.
- `V0592`: The narrative stops at IV Antibiotics and does not contain any admission or discharge pathway events.
- `V0645`: The narrative lacks any ward or intensive care admission step, stopping at LacticAcid.
- `V0664`: The narrative stops at IV Liquid before any ward admission or discharge activity occurs.
- `V0676`: The trace terminates at IV Antibiotics without reaching ward admission or discharge steps.
- `V0679`: Ends at IV Antibiotics without any admission or discharge activities.
- `V0685`: Stops at IV Antibiotics without ward admission or release events.
- `V0689`: Terminates at IV Antibiotics without reaching admission or discharge.
- `V0694`: Ends at ER Sepsis Triage, lacking admission or discharge activities.
- `V0703`: The narrative ends before any discharge or release event occurs, so neither category is realized.
- `V0713`: The narrative terminates at IV Antibiotics without reaching admission or release.
- `V0750`: The narrative terminates at IV Antibiotics without reaching admission or release.
- `V0759`: The narrative ends at IV Antibiotics without any admission or discharge activities, so neither category fits.
- `V0764`: The narrative ends at ER Sepsis Triage without any admission or discharge activities.
- `V0774`: The narrative ends at ER Sepsis Triage without reaching any ward admission or discharge.
- `V0775`: The narrative ends at CRP without reaching any ward admission or discharge.
- `V0777`: The narrative ends at Leucocytes without reaching any ward admission or discharge.
- `V0778`: The narrative ends at Leucocytes without reaching any ward admission or discharge.
- `V0791`: The narrative ends at IV Antibiotics without reaching any ward admission or discharge.
- `V0816`: The process terminates at IV Antibiotics without reaching any ward admission or discharge category.
- `V0820`: The process stops at LacticAcid before any admission or discharge occurs.
- `V0832`: The process stops at IV Antibiotics without any admission or discharge activity.
- `V0843`: The process terminates at IV Liquid after an initial ward admission, failing to complete a full pathway matching the goal categories.
# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_axisdischarge_pertC_distractor_6_112_rep2` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Release A (`release_a`)

Standard release pathway for discharged patients supporting recovery and minimizing post-discharge deterioration.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Task Release A (id=17), supported by variants such as V0008, V0070, and V0069 where patients are discharged via Release A.

**Goal-model linkage:** 17 (Task): Release A

**Coverage:** macro 573/846 variants (67.7%) · micro 617/1050 cases (58.8%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.49, nearest other category `release_b` at mean distance 15.11

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.346, nearest other category `release_d` at mean distance 0.449

## Release B (`release_b`)

Alternative discharge pathway for admitted cases, contributing to avoiding post-discharge deterioration.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Task Release B (id=18), supported by variant V0068 and V0145.

**Goal-model linkage:** 18 (Task): Release B

**Coverage:** macro 55/846 variants (6.5%) · micro 56/1050 cases (5.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 16.61, nearest other category `release_a` at mean distance 15.11

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.248, nearest other category `release_c` at mean distance 0.544

## Release C (`release_c`)

Discharge pathway for extended inpatient cases, leading to final release.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Task Release C (id=19), supported by long-running variant V0710.

**Goal-model linkage:** 19 (Task): Release C

**Coverage:** macro 22/846 variants (2.6%) · micro 22/1050 cases (2.1%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 24.46, nearest other category `release_a` at mean distance 19.10

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.221, nearest other category `release_d` at mean distance 0.446

## Release D (`release_d`)

Specialized discharge route for cases completing extended inpatient treatment.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Task Release D (id=20), supported by complex variant V0273.

**Goal-model linkage:** 20 (Task): Release D

**Coverage:** macro 23/846 variants (2.7%) · micro 23/1050 cases (2.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 18.19, nearest other category `release_a` at mean distance 16.44

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.294, nearest other category `release_e` at mean distance 0.442

## Release E (`release_e`)

Declared discharge alternative for admitted cases under the patient release goal.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Task Release E (id=21) based on the goal model decomposition, preserving the complete set of alternative outcomes.

**Goal-model linkage:** 21 (Task): Release E

**Coverage:** macro 6/846 variants (0.7%) · micro 6/1050 cases (0.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 17.67, nearest other category `release_a` at mean distance 16.43

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.253, nearest other category `release_d` at mean distance 0.442

## Release F (`release_f`)

Declared discharge alternative for admitted cases under the patient release goal.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Task Release F (id=112) based on the goal model decomposition, preserving the complete set of alternative outcomes.

**Goal-model linkage:** 112 (Task): Release F

**Coverage:** macro 0/846 variants (0.0%) · micro 0/1050 cases (0.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a, nearest other category `None` at mean distance n/a

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a, nearest other category `None` at mean distance n/a

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0274` / `V0710` (category `release_c`): structural=177, profile=0.390
- `V0084` / `V0710` (category `release_c`): structural=174, profile=0.253
- `V0138` / `V0710` (category `release_c`): structural=173, profile=0.253
- `V0313` / `V0710` (category `release_c`): structural=173, profile=0.165
- `V0314` / `V0710` (category `release_c`): structural=173, profile=0.148
- `V0433` / `V0710` (category `release_c`): structural=173, profile=0.313
- `V0601` / `V0710` (category `release_c`): structural=173, profile=0.248
- `V0710` / `V0747` (category `release_c`): structural=173, profile=0.049
- `V0423` / `V0710` (category `release_c`): structural=172, profile=0.126
- `V0426` / `V0710` (category `release_c`): structural=172, profile=0.161

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0022` (`release_a`) / `V0274` (`release_c`): structural=1, profile=0.374
- `V0037` (`release_b`) / `V0706` (`release_a`): structural=1, profile=0.359
- `V0100` (`release_a`) / `V0586` (`release_b`): structural=1, profile=0.339
- `V0396` (`release_a`) / `V0410` (`release_d`): structural=1, profile=0.334
- `V0008` (`release_a`) / `V0037` (`release_b`): structural=2, profile=0.337
- `V0014` (`release_a`) / `V0691` (`release_b`): structural=2, profile=0.388
- `V0014` (`release_a`) / `V0725` (`release_d`): structural=2, profile=0.674
- `V0028` (`release_a`) / `V0586` (`release_b`): structural=2, profile=0.414
- `V0035` (`release_a`) / `V0426` (`release_c`): structural=2, profile=0.445
- `V0037` (`release_b`) / `V0209` (`release_a`): structural=2, profile=0.339

## Residual

167/846 variants (19.7%), 326/1050 cases (31.0%) unassigned.

- `V0001`: The narrative ends at ER Sepsis Triage and does not involve any discharge or release pathway.
- `V0002`: The narrative terminates at CRP testing during the emergency phase and does not represent a patient release.
- `V0003`: The process sequence ends at Leucocytes testing in the emergency department without reaching any discharge pathway.
- `V0004`: The variant concludes with IV Antibiotics administration and does not progress to a discharge or release.
- `V0005`: The narrative stops at LacticAcid testing and does not show an inpatient admission or release pathway.
- `V0006`: The workflow finishes at IV Antibiotics without any subsequent admission or release event.
- `V0007`: The sequence ends with IV Antibiotics administration and does not reach a release stage.
- `V0009`: The process stops at IV Antibiotics in the ER phase and does not include an admission or release.
- `V0010`: The variant terminates at ER Sepsis Triage and does not realize any release category.
- `V0011`: The narrative concludes with IV Antibiotics and lacks any discharge or release event.
- `V0012`: The variant ends with IV Antibiotics and does not reach any release or discharge milestone.
- `V0013`: The activity sequence ends at Leucocytes testing without proceeding to admission or release.
- `V0017`: The narrative terminates at ER Sepsis Triage and does not represent a discharge pathway.
- `V0019`: The process ends with IV Antibiotics in the emergency phase and does not reach a release milestone.
- `V0020`: The narrative terminates at CRP testing in the ER and does not include any discharge pathway.
- `V0021`: Although the variant includes Release A, it ultimately results in Return ER, indicating post-discharge deterioration rather than the standard release recovery pathway.
- `V0023`: The variant includes Release A but ends with Return ER, pointing to a readmission rather than a successful standard release.
- `V0024`: The narrative terminates at Admission NC without continuing to a release outcome.
- `V0025`: The sequence ends at IV Antibiotics during the emergency phase and does not reach a discharge or release.
- `V0027`: The variant ends with IV Antibiotics and does not reach any discharge or release phase.
- `V0029`: The variant terminates at Leucocytes and does not represent a discharge pathway.
- `V0031`: The variant terminates at LacticAcid and does not represent a discharge pathway.
- `V0034`: The variant ends with IV Liquid and lacks any release event.
- `V0036`: The variant ends at CRP and does not include a discharge pathway.
- `V0038`: The variant terminates at IV Antibiotics without reaching a release step.
- `V0040`: The variant terminates at Admission NC and does not complete a discharge route.
- `V0043`: The variant terminates at LacticAcid and does not represent a release pathway.
- `V0050`: The variant terminates at CRP and does not include a discharge pathway.
- `V0056`: The variant outcome is IV Antibiotics rather than a discharge or release category.
- `V0062`: The variant outcome is IV Antibiotics and does not reach any release pathway.
- `V0081`: The variant ends in IV Liquid and does not reach any release pathway.
- `V0088`: The variant ends in IV Antibiotics and does not reach any release pathway.
- `V0092`: The variant terminates at LacticAcid and does not reach any release pathway.
- `V0111`: The narrative ends at Admission NC without reaching any release or discharge outcome.
- `V0127`: The outcome is LacticAcid rather than a patient release event, so it does not fit any discharge pathway category.
- `V0132`: The process terminates at IV Antibiotics without any patient release event.
- `V0133`: The outcome is IV Antibiotics, meaning no discharge or release pathway is realized.
- `V0137`: The variant terminates at LacticAcid and does not represent a patient release pathway.
- `V0146`: The narrative ends with Leucocytes and lacks any release or discharge milestone.
- `V0148`: The process stops at IV Antibiotics without reaching any discharge event.
- `V0187`: The process terminates at CRP without reaching any release outcome.
- `V0197`: The narrative ends abruptly at Leucocytes without reaching a release outcome.
- `V0217`: The narrative ends prematurely with IV Antibiotics and does not reach any discharge category.
- `V0219`: The narrative terminates at Leucocytes without reaching any discharge or release category.
- `V0232`: The narrative ends with IV Antibiotics and does not reach any discharge category.
- `V0234`: The narrative terminates at Leucocytes without reaching any release pathway.
- `V0260`: The narrative ends at IV Antibiotics without reaching any discharge pathway.
- `V0268`: The process sequence halts at Leucocytes without achieving any discharge category.
- `V0287`: The narrative terminates at CRP testing without reaching any discharge category.
- `V0292`: The process terminates prematurely at the Leucocytes testing stage.
- `V0295`: The case terminates during the IV Antibiotics phase without a discharge outcome.
- `V0302`: The variant terminates at ER Sepsis Triage and does not complete a discharge pathway.
- `V0305`: The process terminates at IV Antibiotics inside the emergency setting without reaching a discharge pathway.
- `V0322`: The process stops at IV Antibiotics without reaching a discharge destination.
- `V0325`: The variant terminates at IV Antibiotics during emergency treatment.
- `V0330`: The process terminates prematurely at IV Liquid and does not reach any discharge or release category.
- `V0336`: The process stops at CRP without reaching any release or discharge outcome.
- `V0342`: The trace terminates at CRP and does not reach a patient release outcome.
- `V0349`: The process halts early at ER Sepsis Triage and does not reach a discharge goal.
- `V0365`: The narrative ends in a diagnostic activity (Leucocytes) rather than any designated discharge category.
- `V0368`: The trace stops at Admission NC and does not reach a discharge or release category.
- `V0374`: The sequence terminates with Leucocytes without reaching any discharge pathway.
- `V0378`: The narrative ends with IV Antibiotics and does not reach any designated discharge or release pathway.
- `V0379`: The narrative ends with IV Antibiotics and lacks any recognized discharge outcome.
- `V0382`: The narrative terminates with Return ER, which does not fit any of the specified release categories.
- `V0385`: The narrative ends with Return ER after an interim Release A, failing to align with a final discharge category.
- `V0386`: The outcome is Return ER following Release A, which does not map to the primary release categories.
- `V0398`: The final outcome is Return ER after an interim Release A, which does not fit any category.
- `V0415`: The outcome is Admission NC without any release event, so none of the release categories fit.
- `V0417`: The outcome is ER Triage, which does not realize any of the patient release categories.
- `V0427`: The outcome is Return ER rather than a standard final release pathway.
- `V0429`: The process ends at IV Antibiotics without reaching a final release outcome.
- `V0435`: The narrative results in a Return ER outcome.
- `V0437`: The narrative results in a Return ER outcome following extended treatment.
- `V0440`: The narrative results in a Return ER outcome.
- `V0441`: The narrative results in a Return ER outcome.
- `V0442`: The narrative results in a Return ER outcome.
- `V0443`: The narrative results in a Return ER outcome.
- `V0447`: The narrative results in a Return ER outcome.
- `V0448`: The narrative results in a Return ER outcome.
- `V0449`: The narrative results in a Return ER outcome.
- `V0462`: The trace terminates at CRP without reaching any final release activity.
- `V0476`: The narrative ends with Return ER after an initial Release A, which does not cleanly map to standard discharge pathways without readmission.
- `V0479`: The narrative culminates in a Return ER event after Release A, representing a post-discharge complication rather than a standard final recovery.
- `V0482`: The narrative includes a Return ER after Release A, so it is placed in the residual.
- `V0484`: The outcome is Return ER after an intermediate Release A, falling outside standard successful discharge categories.
- `V0488`: The narrative terminates at IV Liquid without reaching a discharge or release event.
- `V0492`: The narrative ends at IV Liquid and does not reach any release category.
- `V0495`: The narrative terminates at IV Antibiotics without a discharge outcome.
- `V0497`: The narrative ends in a Return ER event following Release A.
- `V0501`: The variant ends with IV Liquid and does not reach a discharge or release state.
- `V0502`: The variant ends with Admission NC and does not complete a release pathway.
- `V0504`: The narrative includes Release A but ultimately leads to Return ER, indicating a readmission rather than a successful standard recovery pathway.
- `V0505`: The narrative shows Release A followed by Return ER, representing an unfulfilled standard recovery.
- `V0507`: The variant terminates at IV Antibiotics without reaching a discharge or release goal.
- `V0508`: The narrative ends with Return ER after Release A, denoting post-discharge deterioration and readmission.
- `V0510`: The variant terminates prematurely at IV Antibiotics.
- `V0515`: The narrative ends with Return ER following Release A, meaning the standard recovery pathway failed due to post-discharge deterioration.
- `V0516`: The sequence ends on Leucocytes and does not reach a release outcome.
- `V0517`: The sequence terminates at ER Triage without reaching any discharge alternative.
- `V0519`: The patient returns to the ER after Release A, indicating a failure of the recovery pathway.
- `V0520`: The narrative terminates with Return ER after Release A.
- `V0526`: The narrative ends with Return ER rather than a standard discharge or final release category.
- `V0528`: The variant ends in Return ER instead of a final release pathway.
- `V0529`: The narrative concludes with Return ER.
- `V0530`: The narrative ends with Return ER.
- `V0531`: The variant terminates in Return ER.
- `V0535`: The narrative ends with Return ER.
- `V0539`: The narrative results in Return ER.
- `V0543`: The narrative ends with Return ER.
- `V0546`: The variant ends with Return ER.
- `V0549`: The narrative ends prematurely with IV Liquid and does not reach a discharge category.
- `V0556`: The outcome is Return ER rather than any standard release pathway.
- `V0558`: The variant results in a Return ER after discharge, not fitting the specified release pathways.
- `V0559`: The process outcome is Return ER.
- `V0560`: The process results in a Return ER outcome.
- `V0564`: The variant ends with Return ER.
- `V0565`: The process terminates at Admission NC without reaching a final release category.
- `V0567`: The process results in Return ER.
- `V0573`: The outcome is Return ER.
- `V0575`: The process terminates at Leucocytes without reaching a release category.
- `V0580`: The narrative terminates at CRP and does not reach any designated release or discharge goal.
- `V0584`: The variant ends at IV Liquid and lacks any discharge or release activity.
- `V0585`: The sequence ends at LacticAcid without completing a patient release pathway.
- `V0587`: The narrative ends at CRP and does not involve any release or discharge action.
- `V0592`: The process ends at IV Antibiotics and does not realize any release category.
- `V0605`: The case does not end with a final release, instead resulting in Return ER after initial Release A, making standard discharge categories inapplicable.
- `V0614`: Although Release A is recorded mid-pathway, the final outcome is Return ER, meaning it does not end as a successful standard discharge.
- `V0615`: The variant ends with Return ER following a brief Release C, invalidating a final stable discharge status.
- `V0625`: The variant terminates with Return ER after an intermediate Release A, meaning the overall trajectory is a return to the emergency room rather than a final discharge.
- `V0636`: The narrative ends with LacticAcid and does not reach any discharge category.
- `V0644`: The narrative concludes with CRP and does not complete a discharge category.
- `V0645`: The narrative ends with LacticAcid without completing any release pathway.
- `V0654`: The process terminates with Leucocytes and does not reach any designated release pathway.
- `V0663`: The process stops at Admission NC and does not complete a discharge pathway.
- `V0664`: The process stops at IV Liquid without reaching a discharge pathway.
- `V0670`: The narrative ends with Leucocytes after returning to ER, missing a clean release category.
- `V0676`: The narrative ends with IV Antibiotics and does not reach a discharge/release outcome.
- `V0679`: The process concludes at IV Antibiotics without a discharge outcome.
- `V0685`: The sequence terminates at IV Antibiotics without discharge.
- `V0689`: The variant stops at IV Antibiotics.
- `V0694`: The narrative ends at ER Sepsis Triage and does not represent a release pathway.
- `V0703`: The process variant terminates at IV Liquid and does not reach a discharge goal.
- `V0705`: The process variant ends with Return ER after an initial release, falling outside the direct discharge pathway categories.
- `V0707`: The process variant terminates at Admission NC and does not reach a discharge outcome.
- `V0708`: The process variant terminates at IV Antibiotics without reaching a discharge destination.
- `V0712`: The process variant concludes with Return ER following initial release.
- `V0713`: The process variant terminates at IV Antibiotics without reaching a final discharge.
- `V0719`: The process variant concludes with Return ER following an initial release.
- `V0720`: The process variant concludes with Return ER following an initial release.
- `V0721`: The process variant concludes with Return ER following an initial release.
- `V0724`: The process variant concludes with Return ER following an initial release.
- `V0742`: The narrative ends with LacticAcid and does not reach a discharge goal.
- `V0750`: The narrative ends with IV Antibiotics and does not reach any release or discharge outcome.
- `V0759`: The process terminates at IV Antibiotics without reaching any discharge or release phase.
- `V0764`: The process is cut short at ER Sepsis Triage and does not complete an admission or release pathway.
- `V0772`: The process terminates at CRP lab tests and does not reach a discharge goal.
- `V0774`: Variant stops prematurely at ER Sepsis Triage without any admission or release.
- `V0775`: Terminates during diagnostic evaluation (CRP) without entering an admission or release phase.
- `V0777`: The process terminates at Leucocytes without reaching a discharge or release event.
- `V0778`: The process terminates at Leucocytes and does not conclude with a release outcome.
- `V0791`: The process terminates at IV Antibiotics and does not reach any release category.
- `V0816`: The outcome is IV Antibiotics and does not reach any release pathway category.
- `V0820`: The outcome is LacticAcid and does not reach any release pathway category.
- `V0826`: The variant ends with Admission NC and does not complete a discharge or release pathway.
- `V0832`: The variant terminates with IV Antibiotics and does not reach a discharge or release phase.
- `V0843`: The variant terminates with IV Liquid and does not reach any release or discharge category.
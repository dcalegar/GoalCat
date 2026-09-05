# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_axisdischarge_pertA_remove_21_rep1` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Release A (`release_a`)

Discharge representing standard patient release, advancing Avoid post-discharge deterioration and judged against Post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative Release A (id=17), observed in variants such as V0008, V0070, and V0071.

**Goal-model linkage:** 17 (Task): Release A

**Coverage:** macro 554/846 variants (65.5%) · micro 598/1050 cases (57.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.46, nearest other category `release_b` at mean distance 15.15

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.342, nearest other category `release_d` at mean distance 0.453

## Release B (`release_b`)

Discharge variant representing alternative release processing, advancing Avoid post-discharge deterioration and judged against Post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative Release B (id=18), observed in variants such as V0068 and V0145.

**Goal-model linkage:** 18 (Task): Release B

**Coverage:** macro 54/846 variants (6.4%) · micro 55/1050 cases (5.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 16.68, nearest other category `release_a` at mean distance 15.15

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.230, nearest other category `release_c` at mean distance 0.541

## Release C (`release_c`)

Discharge variant representing complex or extended patient release, advancing Avoid post-discharge deterioration and judged against Post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative Release C (id=19), observed in long-running variant V0710.

**Goal-model linkage:** 19 (Task): Release C

**Coverage:** macro 23/846 variants (2.7%) · micro 23/1050 cases (2.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 23.74, nearest other category `release_a` at mean distance 18.68

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.241, nearest other category `release_d` at mean distance 0.442

## Release D (`release_d`)

Discharge variant representing alternate disposition processing, advancing Avoid post-discharge deterioration and judged against Post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative Release D (id=20), observed in variant V0273.

**Goal-model linkage:** 20 (Task): Release D

**Coverage:** macro 23/846 variants (2.7%) · micro 23/1050 cases (2.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 18.19, nearest other category `release_a` at mean distance 16.44

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.294, nearest other category `release_c` at mean distance 0.442

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0274` / `V0710` (category `release_c`): structural=177, profile=0.390
- `V0084` / `V0710` (category `release_c`): structural=174, profile=0.253
- `V0615` / `V0710` (category `release_c`): structural=174, profile=0.504
- `V0138` / `V0710` (category `release_c`): structural=173, profile=0.253
- `V0313` / `V0710` (category `release_c`): structural=173, profile=0.165
- `V0314` / `V0710` (category `release_c`): structural=173, profile=0.148
- `V0433` / `V0710` (category `release_c`): structural=173, profile=0.313
- `V0601` / `V0710` (category `release_c`): structural=173, profile=0.248
- `V0710` / `V0747` (category `release_c`): structural=173, profile=0.049
- `V0423` / `V0710` (category `release_c`): structural=172, profile=0.126

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

192/846 variants (22.7%), 351/1050 cases (33.4%) unassigned.

- `V0001`: This narrative ends with ER Sepsis Triage and does not reach a patient release step.
- `V0002`: This narrative ends with CRP and does not reach a patient release step.
- `V0003`: This narrative ends with Leucocytes and does not reach a patient release step.
- `V0004`: This narrative ends with IV Antibiotics and does not reach a patient release step.
- `V0005`: This narrative ends with LacticAcid and does not reach a patient release step.
- `V0006`: This narrative ends with IV Antibiotics and does not reach a patient release step.
- `V0007`: This narrative ends with IV Antibiotics and does not reach a patient release step.
- `V0009`: This narrative ends with IV Antibiotics and does not reach a patient release step.
- `V0010`: This narrative ends with ER Sepsis Triage and does not reach a patient release step.
- `V0011`: This narrative ends with IV Antibiotics and does not reach a patient release step.
- `V0012`: This narrative ends with IV Antibiotics and does not reach a patient release step.
- `V0013`: This narrative ends with Leucocytes and does not reach a patient release step.
- `V0017`: This narrative ends with ER Sepsis Triage and does not reach a patient release step.
- `V0019`: This narrative ends with IV Antibiotics and does not reach a patient release step.
- `V0020`: This narrative ends with CRP and does not reach a patient release step.
- `V0021`: This narrative results in a Return ER outcome after release, which falls outside standard release tracking categories.
- `V0023`: This narrative results in a Return ER outcome after release, which falls outside standard release tracking categories.
- `V0024`: This narrative ends with Admission NC and does not reach a patient release step.
- `V0025`: This narrative ends with IV Antibiotics and does not reach a patient release step.
- `V0027`: The variant ends with IV Antibiotics and does not reach any release activity.
- `V0029`: The variant terminates at Leucocytes without performing a release activity.
- `V0031`: The variant ends at LacticAcid without a release activity.
- `V0034`: The variant ends at IV Liquid and does not execute a release activity.
- `V0036`: The variant stops at CRP without reaching a release step.
- `V0038`: The variant ends at IV Antibiotics without a release activity.
- `V0040`: The variant terminates at Admission NC and lacks any release activity.
- `V0043`: The variant stops at LacticAcid without any release processing.
- `V0050`: The variant terminates at CRP without reaching a release activity.
- `V0056`: The narrative ends with IV Antibiotics and does not reach any release activity.
- `V0062`: The narrative ends with IV Antibiotics without concluding with a release activity.
- `V0081`: The narrative outcome is IV Liquid, not any form of patient release.
- `V0088`: The narrative outcome is IV Antibiotics, not any form of patient release.
- `V0092`: The narrative outcome is LacticAcid, not any form of patient release.
- `V0111`: The process variant ends with Admission NC, which does not match any of the release categories.
- `V0127`: The variant ends with LacticAcid and does not reach any release stage.
- `V0132`: The variant terminates at IV Antibiotics without any patient release event.
- `V0133`: The variant terminates at IV Antibiotics without any patient release event.
- `V0137`: The variant terminates at LacticAcid without completing any release processing.
- `V0146`: The variant ends at Leucocytes without reaching any discharge or release category.
- `V0148`: The variant ends at IV Antibiotics without reaching a release phase.
- `V0187`: The narrative does not reach any release activity, terminating early at CRP.
- `V0196`: The narrative ends with Release E which does not correspond to any defined release category in the taxonomy.
- `V0197`: The narrative does not reach any release activity, terminating early at Leucocytes.
- `V0217`: The narrative outcome is IV Antibiotics, which does not match any discharge category.
- `V0219`: The narrative outcome is Leucocytes, which does not match any discharge category.
- `V0232`: The narrative ends at IV Antibiotics without reaching a discharge or release category.
- `V0234`: The narrative ends at Leucocytes without completing a patient release.
- `V0260`: The narrative terminates at IV Antibiotics and does not reach any release category.
- `V0268`: The narrative terminates at Leucocytes and does not reach any release category.
- `V0287`: The process terminates at CRP and does not reach any release activity, so no release category applies.
- `V0292`: The variant terminates prematurely at Leucocytes without reaching any patient release category.
- `V0295`: The process terminates at IV Antibiotics and does not reach a release outcome.
- `V0302`: The narrative does not culminate in any release or disposition activity, ending prematurely at ER Sepsis Triage.
- `V0305`: The process terminates at IV Antibiotics without reaching a release phase.
- `V0309`: The sequence contains Release B but terminates at Admission NC, making it an incomplete or non-standard disposition path for classification.
- `V0316`: The narrative ends with Release E, which does not exist in the defined taxonomy categories.
- `V0322`: The process concludes at IV Antibiotics without any release or disposition step.
- `V0325`: The variant ends at IV Antibiotics without reaching a discharge or release category.
- `V0330`: The narrative ends with IV Liquid and does not reach a recognized discharge category.
- `V0336`: The narrative ends with CRP and lacks a discharge activity.
- `V0342`: The narrative ends with CRP and does not include any release activity.
- `V0349`: The narrative ends with ER Sepsis Triage and does not complete a discharge process.
- `V0352`: The narrative outcome is Return ER following Release A, meaning it does not cleanly realize standard unproblematic release.
- `V0353`: The narrative results in a Return ER outcome after Release A.
- `V0357`: Ends with a Return ER event after Release A.
- `V0358`: Followed by a Return ER event after the release.
- `V0359`: Resulted in Return ER.
- `V0364`: Finished with Return ER after initial release.
- `V0365`: The outcome is Leucocytes rather than any release category.
- `V0366`: Followed by Return ER.
- `V0367`: Results in Return ER after Release A.
- `V0368`: The process stops at Admission NC, not reaching any release category.
- `V0369`: Ends with Return ER.
- `V0370`: The outcome is Return ER.
- `V0374`: Outcome is Leucocytes, not a release category.
- `V0378`: The outcome is IV Antibiotics, meaning the patient was not discharged during this variant sequence.
- `V0379`: The outcome is IV Antibiotics, with no final discharge event present.
- `V0382`: The outcome is Return ER following an initial Release A, which falls outside standard release classification criteria.
- `V0385`: The outcome is Return ER after a Release A, representing a post-discharge ER return.
- `V0386`: The outcome is Return ER following a Release A.
- `V0398`: The outcome is Return ER following a Release A.
- `V0415`: The narrative outcome is Admission NC without any release event, so it does not realize any discharge category.
- `V0417`: The narrative outcome is ER Triage, so it does not realize any discharge category.
- `V0427`: The narrative ends with 'Return ER' rather than any patient release category.
- `V0429`: The narrative ends with 'IV Antibiotics' without a patient release outcome.
- `V0435`: The narrative ends with 'Return ER' after a prior 'Release A', indicating a post-discharge ER return.
- `V0437`: The narrative concludes with 'Return ER' following 'Release D', indicating a return to ER.
- `V0440`: The narrative culminates in 'Return ER' after 'Release A'.
- `V0441`: The narrative culminates in 'Return ER' after 'Release A'.
- `V0442`: The narrative culminates in 'Return ER' after 'Release A'.
- `V0443`: The narrative culminates in 'Return ER' after 'Release A'.
- `V0447`: The narrative culminates in 'Return ER' following 'Release C'.
- `V0448`: The narrative culminates in 'Return ER' following 'Release A'.
- `V0449`: The narrative culminates in 'Return ER' following 'Release A'.
- `V0453`: The patient experienced an ER return after initial Release A, which falls outside the scope of direct categorizable release types without fitting alternative release processing.
- `V0454`: The variant ends in a post-discharge ER return after Release A, categorizing as residual due to the return outcome.
- `V0458`: The case involves a post-discharge ER return following Release A, making it part of the residual category.
- `V0460`: This case ends with a post-discharge ER return, classifying it as residual.
- `V0462`: The outcome is incomplete (CRP) rather than a final release disposition, placing it in the residual.
- `V0463`: The narrative ends with a return to the ER after Release A, making it residual.
- `V0464`: The sequence results in an ER return after Release A, therefore falling into the residual category.
- `V0467`: The case features a return to the ER following Release A, categorizing as residual.
- `V0468`: This sequence leads to an ER return following standard release, placing it in the residual category.
- `V0469`: The patient returns to the ER post-discharge, meaning it falls under the residual category.
- `V0473`: An ER return occurs after Release A, classifying this narrative as residual.
- `V0474`: The narrative results in a subsequent return to the ER after release, placing it in the residual.
- `V0488`: The narrative does not reach a release activity, ending at IV Liquid.
- `V0492`: The narrative does not reach a release activity, ending at IV Liquid.
- `V0495`: The narrative does not reach a release activity, ending at IV Antibiotics.
- `V0501`: The narrative ends with IV Liquid and does not reach a patient release outcome.
- `V0502`: The narrative ends with Admission NC and does not reach a patient release outcome.
- `V0504`: The narrative ends with Return ER after Release A, representing a post-discharge ER return rather than a successful standard release.
- `V0505`: The narrative ends with Return ER, indicating a post-discharge ER return.
- `V0507`: The narrative terminates at IV Antibiotics without any patient release activity.
- `V0508`: The narrative results in a Return ER event following Release A.
- `V0510`: The narrative terminates at IV Antibiotics without reaching a release outcome.
- `V0515`: The narrative ends with Return ER following Release A.
- `V0516`: The narrative ends with Leucocytes and does not reach a patient release outcome.
- `V0517`: The narrative ends prematurely with ER Triage and lacks a release outcome.
- `V0519`: The narrative results in Return ER following a release.
- `V0520`: The narrative results in Return ER following a release.
- `V0549`: The variant ends prematurely at IV Liquid and does not realize any release category.
- `V0553`: The narrative ends with Release E, which is outside the defined taxonomy categories of A, B, C, and D.
- `V0556`: The narrative ends with Return ER after an intermediate Release A, representing a post-discharge ER return rather than a finalized release category from the primary axis.
- `V0558`: The narrative ends with Return ER following Release A, which falls outside standard release categorization.
- `V0559`: The narrative ends with Return ER following Release A, representing a post-discharge ER return.
- `V0560`: The narrative ends with Return ER after a release, falling outside the standard release categories.
- `V0564`: The narrative ends with Return ER following a release outcome, rendering it part of the residual.
- `V0565`: The narrative terminates at Admission NC and does not reach a discharge/release outcome.
- `V0567`: The narrative ends with Return ER following a release.
- `V0573`: The narrative ends with Return ER following Release A.
- `V0575`: The narrative terminates early at Leucocytes without reaching any release outcome.
- `V0580`: The narrative ends with CRP and does not complete a patient release.
- `V0584`: The narrative ends with IV Liquid and does not reach a patient release.
- `V0585`: The narrative ends with LacticAcid and does not reach a patient release.
- `V0587`: The narrative ends with CRP and does not complete a patient release.
- `V0592`: The narrative ends with IV Antibiotics and does not reach a patient release.
- `V0598`: The narrative ends with Release E, which does not match any of the defined release categories in the taxonomy.
- `V0603`: The narrative ends with Release E, which does not match any of the defined release categories (release_a, release_b, release_c, release_d).
- `V0629`: The outcome is Release E, which does not match any of the defined categories (release_a, release_b, release_c, release_d).
- `V0636`: The outcome is LacticAcid, which does not represent any form of patient release.
- `V0644`: The outcome is CRP, which does not represent patient release.
- `V0645`: The outcome is LacticAcid, which does not represent patient release.
- `V0654`: The narrative ends with 'Leucocytes' and does not involve any patient release activity.
- `V0663`: The narrative ends with 'Admission NC' and does not reach any release stage.
- `V0664`: The narrative concludes with 'IV Liquid' and contains no discharge or release steps.
- `V0670`: The narrative concludes with 'Leucocytes' after a return to the ER, with no final release categorization matching the end state.
- `V0676`: The process ends with IV Antibiotics and does not reach a patient release activity.
- `V0679`: The process terminates at IV Antibiotics without any release step.
- `V0685`: The process terminates at IV Antibiotics and does not include release.
- `V0689`: The narrative terminates at IV Antibiotics without reaching a discharge activity.
- `V0694`: The process ends prematurely at ER Sepsis Triage.
- `V0703`: The outcome is IV Liquid, which does not correspond to any of the release categories.
- `V0705`: The narrative outcome is Return ER following Release A, which does not map cleanly into the specified discharge release category goal.
- `V0707`: The narrative outcome is Admission NC, which is not a patient release category.
- `V0708`: The narrative outcome is IV Antibiotics, which is not a patient release category.
- `V0712`: The narrative outcome involves Return ER following a release, making it part of the residual.
- `V0713`: The narrative outcome is IV Antibiotics, which is not a release category.
- `V0719`: The narrative outcome includes a return to the ER after Release A.
- `V0720`: The narrative outcome includes a return to the ER after Release A.
- `V0721`: The narrative outcome includes a return to the ER after Release A.
- `V0724`: The narrative outcome includes a return to the ER after Release A.
- `V0742`: The narrative does not reach any release activity, concluding with LacticAcid instead.
- `V0750`: The narrative terminates early at IV Antibiotics without reaching a release activity.
- `V0759`: The variant ends with IV Antibiotics and does not reach any patient release category.
- `V0764`: The variant ends with ER Sepsis Triage and does not reach any patient release category.
- `V0772`: The variant ends with CRP and does not reach any patient release category.
- `V0774`: The variant ends with ER Sepsis Triage and does not reach any patient release category.
- `V0775`: The variant ends with CRP and does not reach any patient release category.
- `V0777`: The narrative terminates at Leucocytes and does not complete a patient release process.
- `V0778`: The narrative terminates at Leucocytes without reaching a patient release activity.
- `V0779`: The narrative ends with Return ER after an initial Release A, which does not fit standard clean categories.
- `V0785`: The narrative ends with Return ER following a Release A, indicating post-discharge ER return.
- `V0787`: The narrative ends with Return ER after a standard release, representing post-discharge ER return.
- `V0791`: The narrative terminates at IV Antibiotics without reaching a discharge or release state.
- `V0794`: The narrative ends with Return ER, reflecting a post-discharge ER return after release.
- `V0797`: The narrative terminates in a Return ER event after release.
- `V0798`: The narrative terminates in a Return ER event after release.
- `V0804`: The narrative results in a return to the ER after a release, which does not fit standard successful discharge categories.
- `V0806`: The narrative ends with a return to the ER following Release A.
- `V0808`: The narrative results in a return to the ER.
- `V0812`: The narrative results in a return to the ER.
- `V0815`: The narrative results in a return to the ER.
- `V0816`: The narrative terminates at IV Antibiotics without reaching a discharge or release state.
- `V0820`: The narrative terminates at LacticAcid without reaching a release outcome.
- `V0821`: The narrative results in a return to the ER.
- `V0822`: The narrative results in a return to the ER.
- `V0823`: The narrative results in a return to the ER.
- `V0825`: The narrative results in a return to the ER.
- `V0826`: The narrative ends with Admission NC and does not feature a final release activity corresponding to any of the release categories.
- `V0832`: The narrative ends at IV Antibiotics and does not reach a discharge or release phase.
- `V0843`: The narrative terminates at IV Liquid and lacks any release or discharge activity.
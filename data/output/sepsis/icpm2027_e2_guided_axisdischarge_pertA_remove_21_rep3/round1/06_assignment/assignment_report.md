# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_axisdischarge_pertA_remove_21_rep3` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Release A (`release_a`)

Represents the discharge of an admitted patient via pathway A, advancing the softgoal to avoid post-discharge deterioration and being measured against post-discharge ER return indicators.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative Release A (id 17), observed across multiple variants such as V0008, V0070, and V0069.

**Goal-model linkage:** 17 (Task): Release A

**Coverage:** macro 598/846 variants (70.7%) · micro 646/1050 cases (61.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.47, nearest other category `release_b` at mean distance 15.11

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.349, nearest other category `release_d` at mean distance 0.442

## Release B (`release_b`)

Represents the discharge of an admitted patient via pathway B, contributing to avoiding post-discharge deterioration and evaluated against post-discharge ER return rates.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative Release B (id 18), observed in narrative variant V0068 and V0145.

**Goal-model linkage:** 18 (Task): Release B

**Coverage:** macro 55/846 variants (6.5%) · micro 56/1050 cases (5.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 16.61, nearest other category `release_a` at mean distance 15.11

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.248, nearest other category `release_d` at mean distance 0.546

## Release C (`release_c`)

Represents the discharge of an admitted patient via pathway C, contributing to post-discharge stability and measured via downstream ER return indicators.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative Release C (id 19), observed in complex variant V0710.

**Goal-model linkage:** 19 (Task): Release C

**Coverage:** macro 25/846 variants (3.0%) · micro 25/1050 cases (2.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 22.70, nearest other category `release_a` at mean distance 18.16

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.268, nearest other category `release_d` at mean distance 0.433

## Release D (`release_d`)

Represents the discharge of an admitted patient via pathway D, advancing the organization's objective of preventing post-discharge deterioration.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative Release D (id 20), observed in variant V0273.

**Goal-model linkage:** 20 (Task): Release D

**Coverage:** macro 24/846 variants (2.8%) · micro 24/1050 cases (2.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 19.12, nearest other category `release_a` at mean distance 17.11

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.300, nearest other category `release_c` at mean distance 0.433

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0274` / `V0710` (category `release_c`): structural=177, profile=0.390
- `V0084` / `V0710` (category `release_c`): structural=174, profile=0.253
- `V0615` / `V0710` (category `release_c`): structural=174, profile=0.504
- `V0138` / `V0710` (category `release_c`): structural=173, profile=0.253
- `V0313` / `V0710` (category `release_c`): structural=173, profile=0.165
- `V0314` / `V0710` (category `release_c`): structural=173, profile=0.148
- `V0427` / `V0710` (category `release_c`): structural=173, profile=0.418
- `V0433` / `V0710` (category `release_c`): structural=173, profile=0.313
- `V0601` / `V0710` (category `release_c`): structural=173, profile=0.248
- `V0710` / `V0747` (category `release_c`): structural=173, profile=0.049

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

144/846 variants (17.0%), 299/1050 cases (28.5%) unassigned.

- `V0001`: The narrative ends with ER Sepsis Triage and does not involve patient discharge.
- `V0002`: The narrative terminates at CRP testing without patient discharge.
- `V0003`: The narrative terminates at Leucocytes testing without patient discharge.
- `V0004`: The narrative ends with IV Antibiotics administration and lacks patient discharge.
- `V0005`: The narrative ends with LacticAcid testing without patient discharge.
- `V0006`: The narrative ends with IV Antibiotics administration and does not involve discharge.
- `V0007`: The narrative terminates at IV Antibiotics without patient discharge.
- `V0009`: The narrative ends with IV Antibiotics without any discharge step.
- `V0010`: The narrative terminates at ER Sepsis Triage without patient discharge.
- `V0011`: The narrative terminates at IV Antibiotics without patient discharge.
- `V0012`: The narrative terminates at IV Antibiotics without patient discharge.
- `V0013`: The narrative terminates at Leucocytes testing without patient discharge.
- `V0017`: The narrative terminates at ER Sepsis Triage without patient discharge.
- `V0019`: The narrative terminates at IV Antibiotics without patient discharge.
- `V0020`: The narrative terminates at CRP testing without patient discharge.
- `V0024`: The narrative ends with Admission NC and lacks patient discharge.
- `V0025`: The narrative ends with IV Antibiotics without patient discharge.
- `V0027`: The process terminates at IV Antibiotics without any patient release or discharge event.
- `V0029`: The process ends at Leucocytes without reaching a patient discharge milestone.
- `V0031`: The process terminates at LacticAcid without completing any discharge pathway.
- `V0034`: The process ends at IV Liquid and lacks any discharge or release activity.
- `V0036`: The process terminates at CRP without reaching a discharge or release event.
- `V0038`: The process ends at IV Antibiotics with no discharge milestone.
- `V0040`: The process ends at Admission NC, representing an admission rather than a release.
- `V0043`: The process ends at LacticAcid without reaching a discharge milestone.
- `V0050`: The process terminates at CRP and does not include any discharge or release activity.
- `V0056`: The variant ends with IV Antibiotics and does not conclude with a patient release.
- `V0062`: The trace stops at IV Antibiotics without any release event.
- `V0081`: The variant ends with IV Liquid and does not conclude with a discharge activity corresponding to any of the release pathways.
- `V0088`: The variant ends with IV Antibiotics and does not conclude with any discharge pathway.
- `V0092`: The variant ends with LacticAcid and does not conclude with any discharge pathway.
- `V0111`: The variant ends with Admission NC rather than any discharge activity, so none of the release categories apply.
- `V0127`: The narrative concludes with LacticAcid rather than a patient discharge pathway, so it does not realize any of the release categories.
- `V0132`: The sequence terminates at IV Antibiotics without any patient discharge event.
- `V0133`: The pathway terminates at IV Antibiotics without reaching a discharge activity.
- `V0137`: Terminates with LacticAcid and does not include a patient discharge step.
- `V0146`: The narrative terminates at Leucocytes and lacks any discharge event.
- `V0148`: Terminates at IV Antibiotics without reaching a discharge activity.
- `V0181`: Outcome does not match any of the specified release categories.
- `V0187`: Process terminates early at CRP without reaching any release outcome.
- `V0196`: Outcome is Release E which does not correspond to release_a, release_b, release_c, or release_d.
- `V0197`: Terminates at Leucocytes without a valid release outcome.
- `V0217`: The narrative ends with IV Antibiotics and does not reach any release outcome.
- `V0219`: The narrative terminates at Leucocytes without reaching a discharge or release outcome.
- `V0232`: The narrative terminates at IV Antibiotics and does not reach any discharge or release category.
- `V0234`: The case stops at Leucocytes and does not contain a release event.
- `V0260`: The narrative terminates at IV Antibiotics and does not reach any discharge category.
- `V0268`: The narrative terminates at Leucocytes and does not reach any discharge category.
- `V0287`: The process terminates at CRP without reaching any discharge or release event, so no release category applies.
- `V0292`: The process stops at Leucocytes without reaching any release outcome, fitting none of the categories.
- `V0295`: The process terminates at IV Antibiotics without any release event, thus fitting no category.
- `V0302`: The process terminates at ER Sepsis Triage and does not reach any discharge activity.
- `V0305`: The trace stops at IV Antibiotics and does not complete a patient discharge.
- `V0316`: The narrative ends with Release E, which is not part of the defined taxonomy categories (release_a, release_b, release_c, release_d).
- `V0322`: The trace ends at IV Antibiotics without reaching a discharge activity.
- `V0325`: The process stops at IV Antibiotics and does not reach any discharge category.
- `V0330`: The process terminates at IV Liquid rather than a patient release or return outcome.
- `V0336`: The process ends prematurely at CRP testing without reaching a discharge or release state.
- `V0342`: The process terminates at CRP and does not reach a discharge or release category.
- `V0349`: The process terminates at ER Sepsis Triage and does not realize a discharge category.
- `V0365`: The variant does not end with any release activity, terminating instead at Leucocytes.
- `V0368`: The process terminates at Admission NC without reaching any discharge category.
- `V0374`: The sequence terminates at Leucocytes without any discharge outcome.
- `V0378`: The narrative terminates at IV Antibiotics without any discharge or release event, so it does not fit any release category.
- `V0379`: The narrative ends at IV Antibiotics and lacks a final patient release activity.
- `V0382`: Although it contains Release A, the final outcome is Return ER rather than a standard complete discharge path without subsequent return indicator classification.
- `V0385`: The final outcome is Return ER, rendering it outside the standard successful release categories.
- `V0386`: The final outcome is Return ER, disqualifying it from being a straightforward successful release pathway.
- `V0398`: The final outcome is Return ER, meaning it does not represent a standard uncomplicated release category.
- `V0415`: The outcome is Admission NC without a corresponding discharge category from the taxonomy.
- `V0417`: The process stops at ER Triage and does not reach any discharge category.
- `V0429`: The outcome is IV Antibiotics rather than a discharge pathway, so none of the release categories fit.
- `V0462`: The outcome is CRP rather than a recognized release pathway.
- `V0488`: The variant ends in IV Liquid and does not reach any discharge or release category.
- `V0492`: The variant ends in IV Liquid without completing a release or discharge.
- `V0495`: The variant ends with IV Antibiotics and does not reach a release milestone.
- `V0501`: The narrative does not end with a release activity corresponding to any of the defined release pathways.
- `V0502`: The variant ends with Admission NC and does not feature a patient release activity.
- `V0504`: Although it contains Release A, the final outcome of the narrative is Return ER, which does not match the success criteria of the release categories.
- `V0505`: The narrative terminates with Return ER after Release A, failing to represent a successful final discharge pathway.
- `V0507`: The variant ends with IV Antibiotics and lacks any release activity.
- `V0508`: The narrative's final outcome is Return ER, making none of the release categories appropriate.
- `V0510`: The sequence ends at IV Antibiotics without reaching a patient release step.
- `V0515`: The narrative ends with Return ER following Release A, meaning it does not realize a successful release category outcome.
- `V0516`: The variant terminates at Leucocytes and lacks a discharge activity.
- `V0517`: The narrative ends prematurely at ER Triage without reaching admission or release.
- `V0519`: The final outcome is Return ER after Release A, so no release category applies.
- `V0520`: The narrative terminates with Return ER, failing to fit the release category criteria.
- `V0549`: The variant outcome is IV Liquid, which does not correspond to any discharge category in the taxonomy.
- `V0553`: The narrative ends with Release E, which does not correspond to any of the categories release_a, release_b, release_c, or release_d.
- `V0556`: The final outcome is Return ER, which is not part of the release pathways.
- `V0558`: The final outcome is Return ER following Release A, making it part of the residual.
- `V0559`: The final outcome is Return ER following Release A, making it part of the residual.
- `V0560`: The final outcome is Return ER following Release A, making it part of the residual.
- `V0564`: The final outcome is Return ER following Release A, placing it in the residual.
- `V0565`: The outcome is Admission NC, so no discharge category is realized.
- `V0567`: The final outcome is Return ER, placing it in the residual.
- `V0573`: The final outcome is Return ER following Release A, placing it in the residual.
- `V0575`: The outcome is Leucocytes, so no discharge category is realized.
- `V0580`: The narrative does not culminate in any release outcome, ending instead in CRP.
- `V0584`: The narrative ends in IV Liquid without any release outcome.
- `V0585`: The narrative ends in LacticAcid without any release outcome.
- `V0587`: The narrative ends in CRP without any release outcome.
- `V0592`: The narrative terminates at IV Antibiotics without a release outcome.
- `V0598`: The narrative ends with Release E, which does not exist in the taxonomy categories.
- `V0603`: The outcome is Release E, which does not correspond to any of the four defined release categories (A, B, C, D).
- `V0629`: The narrative ends with Release E, which does not match any of the defined release pathways (A, B, C, D).
- `V0636`: The process terminates at LacticAcid without a proper discharge outcome matching any category.
- `V0644`: The process ends at CRP without any final discharge or release outcome.
- `V0645`: The process ends at LacticAcid without any discharge outcome.
- `V0654`: The variant ends in Leucocytes and does not result in any discharge activity or fit the release categories.
- `V0663`: The variant ends in Admission NC and does not reach any discharge category.
- `V0664`: The variant terminates at IV Liquid and has no discharge step.
- `V0670`: The narrative ends with Leucocytes following an intermediate Release A and Return ER cycle, leaving it outside a standard category match.
- `V0676`: The narrative ends with IV Antibiotics and does not involve patient discharge or subsequent release pathway.
- `V0679`: The process terminates at IV Antibiotics without reaching a discharge or release event.
- `V0685`: The workflow stops at IV Antibiotics and does not involve patient release.
- `V0689`: The narrative terminates at IV Antibiotics with no discharge milestone.
- `V0694`: The process sequence halts at ER Sepsis Triage and does not reach discharge.
- `V0703`: The outcome is IV Liquid, which does not represent a patient discharge event.
- `V0707`: The outcome is Admission NC, which is not a discharge category.
- `V0708`: The outcome is IV Antibiotics, which does not represent patient discharge.
- `V0713`: The outcome is IV Antibiotics, representing treatment rather than discharge.
- `V0727`: The narrative ends in Return ER after Release A, so it does not cleanly realize standard release pathway goals without re-admission issues.
- `V0734`: The narrative ends with a Return ER following Release A.
- `V0742`: The narrative outcome is LacticAcid, not a discharge category.
- `V0744`: The narrative ends in a Return ER after Release A.
- `V0745`: The narrative ends in a Return ER after Release A.
- `V0746`: The narrative ends in a Return ER after Release A.
- `V0748`: The narrative ends in a Return ER after Release A.
- `V0750`: The narrative outcome is IV Antibiotics, not a discharge category.
- `V0759`: The variant ends with IV Antibiotics and does not reach a discharge event.
- `V0764`: The process terminates early at ER Sepsis Triage without reaching any release pathway.
- `V0772`: The variant ends on CRP and does not complete a discharge process.
- `V0774`: The process terminates at ER Sepsis Triage and does not reach discharge.
- `V0775`: The variant stops at CRP without reaching a release category.
- `V0777`: The process ends at Leucocytes without an actual patient discharge outcome.
- `V0778`: The process concludes at Leucocytes and does not reach a discharge goal.
- `V0791`: The process stops at IV Antibiotics without any patient discharge.
- `V0816`: The narrative terminates prematurely at IV Antibiotics and does not reach any discharge or release state.
- `V0820`: The process terminates at LacticAcid and does not achieve any patient discharge or release milestone.
- `V0826`: The process terminates with Admission NC and does not reach any discharge activity.
- `V0832`: The process ends at IV Antibiotics and does not reach a discharge milestone.
- `V0843`: The process terminates at IV Liquid and does not reach a discharge activity.
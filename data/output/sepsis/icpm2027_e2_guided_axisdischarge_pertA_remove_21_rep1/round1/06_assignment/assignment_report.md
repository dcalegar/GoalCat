# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_axisdischarge_pertA_remove_21_rep1` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Release A (`release_a`)

Patient discharge pathway A, contributing to avoiding post-discharge deterioration and measured against post-discharge ER return indicators.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative Release A (id=17), supported by variants like V0008, V0066, V0070.

**Goal-model linkage:** 17 (Task): Release A

**Coverage:** macro 609/846 variants (72.0%) · micro 657/1050 cases (62.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.34, nearest other category `release_b` at mean distance 15.06

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.349, nearest other category `release_d` at mean distance 0.449

## Release B (`release_b`)

Patient discharge pathway B, contributing to avoiding post-discharge deterioration and measured against post-discharge ER return indicators.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative Release B (id=18), supported by variants like V0068 and V0145.

**Goal-model linkage:** 18 (Task): Release B

**Coverage:** macro 55/846 variants (6.5%) · micro 56/1050 cases (5.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 16.61, nearest other category `release_a` at mean distance 15.06

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.248, nearest other category `release_d` at mean distance 0.545

## Release C (`release_c`)

Patient discharge pathway C, supporting discharge tracking and evaluated against standard post-discharge recovery metrics.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative Release C (id=19), supported by variant V0710.

**Goal-model linkage:** 19 (Task): Release C

**Coverage:** macro 25/846 variants (3.0%) · micro 25/1050 cases (2.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 22.70, nearest other category `release_a` at mean distance 18.09

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.268, nearest other category `release_d` at mean distance 0.438

## Release D (`release_d`)

Patient discharge pathway D, representing specialized or extended inpatient release outcomes.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative Release D (id=20), supported by variant V0273.

**Goal-model linkage:** 20 (Task): Release D

**Coverage:** macro 21/846 variants (2.5%) · micro 21/1050 cases (2.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 19.33, nearest other category `release_a` at mean distance 16.98

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.284, nearest other category `release_c` at mean distance 0.438

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

136/846 variants (16.1%), 291/1050 cases (27.7%) unassigned.

- `V0001`: This narrative ends at ER Sepsis Triage and does not involve any patient discharge pathway.
- `V0002`: This narrative terminates at CRP testing in the ER and does not represent a discharge pathway.
- `V0003`: This narrative ends at Leucocytes testing in the ER and lacks a discharge pathway.
- `V0004`: This narrative concludes with IV Antibiotics administration in the ER without reaching a discharge destination.
- `V0005`: This narrative stops at LacticAcid measurement in the ER and does not include inpatient admission or release.
- `V0006`: This narrative ends at IV Antibiotics treatment in the ER and does not reach a release outcome.
- `V0007`: This narrative terminates at IV Antibiotics in the ER without proceeding to patient release.
- `V0009`: This narrative ends with IV Antibiotics in the ER and does not show an inpatient release outcome.
- `V0010`: This narrative ends at ER Sepsis Triage and does not realize any discharge category.
- `V0011`: This narrative stops at IV Antibiotics in the ER and does not contain a release pathway.
- `V0012`: This narrative concludes with IV Antibiotics in the ER without proceeding to hospital discharge.
- `V0013`: This narrative ends at Leucocytes testing in the ER and does not reach a discharge pathway.
- `V0017`: This narrative ends at ER Sepsis Triage and lacks any discharge pathway.
- `V0019`: This narrative stops at IV Antibiotics in the ER and does not reach an inpatient release outcome.
- `V0020`: This narrative terminates at CRP testing in the ER without a discharge event.
- `V0024`: This narrative ends at Admission NC and does not specify the final release outcome.
- `V0025`: This narrative concludes with IV Antibiotics in the ER and lacks a release destination.
- `V0027`: This narrative ends at IV Antibiotics in the ER without an inpatient release.
- `V0029`: This narrative terminates at Leucocytes testing in the ER and does not reach a discharge pathway.
- `V0031`: This narrative ends at LacticAcid measurement in the ER and has no discharge outcome.
- `V0034`: This narrative stops at IV Liquid in the ER and lacks an inpatient release event.
- `V0036`: This narrative terminates at CRP testing in the ER without a discharge pathway.
- `V0038`: This narrative ends with IV Antibiotics in the ER and does not reach an inpatient release.
- `V0040`: This narrative ends at Admission NC without specifying a final release category.
- `V0043`: This narrative stops at LacticAcid measurement in the ER and does not include a discharge pathway.
- `V0050`: This narrative ends at CRP testing in the ER and lacks any discharge pathway.
- `V0056`: The outcome is IV Antibiotics, which does not match any discharge category.
- `V0062`: The outcome is IV Antibiotics, so no discharge category is realized.
- `V0081`: The outcome is IV Liquid, which does not correspond to any release category.
- `V0088`: The outcome is IV Antibiotics, which does not match a release category.
- `V0092`: The outcome is LacticAcid, which does not match any release category.
- `V0111`: The narrative ends with Admission NC, which does not realize any of the defined release pathways.
- `V0117`: The narrative terminates with Release D, but the taxonomy categories are limited to release_a, release_b, release_c, and release_d? Wait, release_d is present in taxonomy categories, so this realizes Release D.
- `V0127`: The narrative ends with LacticAcid, which is not a release category.
- `V0132`: The narrative ends with IV Antibiotics, which is not a release category.
- `V0133`: The narrative ends with IV Antibiotics, which is not a release category.
- `V0137`: The narrative ends with LacticAcid, which is not a release category.
- `V0146`: The narrative ends with Leucocytes, which is not a release category.
- `V0148`: The narrative ends with IV Antibiotics, which is not a release category.
- `V0187`: The narrative does not reach any recognized release outcome, ending prematurely at CRP.
- `V0196`: The narrative ends with a non-standard outcome 'Release E' which is not part of the taxonomy categories.
- `V0197`: The narrative does not reach any recognized release outcome, ending at Leucocytes.
- `V0217`: The narrative does not conclude with a release activity, so none of the release categories apply.
- `V0219`: The narrative does not end with any release pathway.
- `V0232`: The narrative stops at IV Antibiotics and does not reach any release category.
- `V0234`: The narrative terminates at Leucocytes and contains no release outcome.
- `V0260`: The narrative ends at IV Antibiotics without reaching a discharge or release outcome.
- `V0268`: The case terminates at Leucocytes without reaching any discharge event.
- `V0287`: The variant terminates at CRP without reaching any release outcome.
- `V0292`: The variant terminates at Leucocytes without reaching a discharge or release event.
- `V0295`: The variant stops at IV Antibiotics without reaching a discharge pathway.
- `V0302`: The variant ends at ER Sepsis Triage and does not reach a discharge pathway.
- `V0305`: Variant terminates at IV Antibiotics without reaching any patient discharge outcome.
- `V0316`: Variant concludes with Release E, which is not part of the defined taxonomy categories.
- `V0322`: Terminates at IV Antibiotics without completing a discharge pathway.
- `V0325`: Terminates at IV Antibiotics with no discharge outcome.
- `V0330`: Terminates at IV Liquid without reaching a discharge pathway.
- `V0334`: Concludes with Release D, which does not match the available taxonomy options.
- `V0336`: Terminates at CRP without reaching a discharge category.
- `V0342`: Terminates at CRP without any discharge outcome.
- `V0347`: Concludes with Release D, which is outside the defined taxonomy categories.
- `V0349`: Terminates at ER Sepsis Triage without reaching a discharge pathway.
- `V0365`: The narrative terminates at Leucocytes without reaching a discharge pathway.
- `V0368`: The process terminates at Admission NC without completing a discharge pathway.
- `V0374`: The trace stops at Leucocytes and does not contain a discharge event.
- `V0378`: The trace stops at IV Antibiotics and lacks a discharge activity.
- `V0379`: The process ends at IV Antibiotics without a discharge action.
- `V0415`: Process ends in Admission NC without any release category.
- `V0417`: Process ends in ER Triage prematurely without reaching a release pathway.
- `V0429`: Process stops at IV Antibiotics without reaching a release category.
- `V0462`: The narrative terminates at CRP without reaching a release outcome.
- `V0488`: The narrative terminates at IV Liquid without reaching a release outcome.
- `V0492`: The narrative terminates at IV Liquid without reaching a release outcome.
- `V0495`: The narrative terminates at IV Antibiotics without reaching a release outcome.
- `V0501`: The narrative ends with IV Liquid and does not reach any discharge pathway or return indicator.
- `V0502`: The narrative ends with Admission NC and does not reach any release or ER return outcome.
- `V0507`: The narrative ends with IV Antibiotics and does not reach a discharge pathway.
- `V0510`: The narrative terminates at IV Antibiotics without reaching a discharge or release pathway.
- `V0516`: The narrative terminates at Leucocytes without reaching any discharge or release pathway.
- `V0517`: The narrative terminates at ER Triage without reaching any discharge or release pathway.
- `V0549`: The narrative terminates at IV Liquid without reaching any discharge or release pathway.
- `V0553`: The outcome is Release E, which does not match any of the defined taxonomy categories (release_a, release_b, release_c, release_d).
- `V0565`: The outcome is Admission NC, which is not one of the final discharge pathways defined in the taxonomy.
- `V0575`: The final activity is Leucocytes, which does not constitute a discharge category.
- `V0580`: The outcome is CRP, which does not correspond to any category in the taxonomy.
- `V0584`: The outcome is IV Liquid, which is not a discharge pathway category.
- `V0585`: The outcome is LacticAcid, which does not match any taxonomy category.
- `V0587`: The outcome is CRP, not matching any category.
- `V0592`: The outcome is IV Antibiotics, which is not a release category.
- `V0598`: The outcome is Release E, which is not part of the taxonomy.
- `V0603`: Outcome is Release E, which does not map to any of the defined release categories (release_a, release_b, release_c, release_d).
- `V0629`: Outcome is Release E, which does not fit any of the valid category options.
- `V0636`: Outcome is LacticAcid, which is not a discharge pathway category.
- `V0644`: Outcome is CRP, which is not a discharge pathway category.
- `V0645`: Outcome is LacticAcid, which is not a discharge pathway category.
- `V0654`: The variant ends with Leucocytes and does not reach a discharge outcome category.
- `V0663`: The process terminates at Admission NC without reaching any release pathway.
- `V0664`: The process ends at IV Liquid without reaching a discharge category.
- `V0670`: The narrative terminates with Leucocytes and does not complete a release category.
- `V0676`: The process terminates at IV Antibiotics without reaching a release pathway.
- `V0679`: The process terminates at IV Antibiotics without reaching a release category.
- `V0685`: The process terminates at IV Antibiotics without a discharge category.
- `V0689`: The process terminates at IV Antibiotics without reaching a release category.
- `V0694`: The process ends at ER Sepsis Triage without reaching any discharge outcome.
- `V0703`: The outcome is IV Liquid, not any of the recognized release categories.
- `V0707`: The outcome is Admission NC, which does not constitute a release category.
- `V0708`: The outcome is IV Antibiotics, not a release category.
- `V0713`: The outcome is IV Antibiotics, which is not a release category.
- `V0742`: The outcome is LacticAcid, which is not a release category.
- `V0750`: The outcome is IV Antibiotics, which is not a release category.
- `V0759`: The narrative ends at IV Antibiotics without reaching a discharge destination.
- `V0764`: Variant terminates early at ER Sepsis Triage.
- `V0772`: Terminates at CRP without a release activity.
- `V0774`: Stops at ER Sepsis Triage.
- `V0775`: Terminates at CRP.
- `V0777`: Ends at Leucocytes without reaching a release phase.
- `V0778`: Ends at Leucocytes.
- `V0791`: Terminates at IV Antibiotics.
- `V0804`: The narrative ends in Return ER rather than a standard discharge pathway category.
- `V0806`: The narrative ends in Return ER instead of a release category.
- `V0808`: The final outcome is Return ER.
- `V0812`: The final outcome is Return ER.
- `V0815`: The final outcome is Return ER.
- `V0816`: The narrative ends in IV Antibiotics without reaching a discharge category.
- `V0820`: The narrative ends in LacticAcid without completing a release pathway.
- `V0821`: The final outcome is Return ER.
- `V0822`: The final outcome is Return ER.
- `V0823`: The final outcome is Return ER.
- `V0825`: The final outcome is Return ER.
- `V0826`: The narrative ends in Admission NC without reaching release.
- `V0827`: The final outcome is Return ER.
- `V0828`: The final outcome is Return ER.
- `V0832`: The narrative ends in IV Antibiotics.
- `V0834`: The final outcome is Return ER.
- `V0842`: The final outcome is Return ER.
- `V0843`: The narrative ends in IV Liquid.
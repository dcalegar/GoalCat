# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_no_sample_axisdischarge_rep2` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Release A (`release_a`)

Discharge pathway Release A for admitted cases. Advances the softgoal Avoid post-discharge deterioration through Help contributions.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative Release A (id=17) under the OR decomposition of goal id=6.

**Goal-model linkage:** 17 (Task): Release A

**Coverage:** macro 570/846 variants (67.4%) · micro 618/1050 cases (58.9%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.23, nearest other category `release_b` at mean distance 15.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.342, nearest other category `release_d` at mean distance 0.449

## Release B (`release_b`)

Discharge pathway Release B for admitted cases. Advances the softgoal Avoid post-discharge deterioration through Help contributions.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative Release B (id=18) under the OR decomposition of goal id=6.

**Goal-model linkage:** 18 (Task): Release B

**Coverage:** macro 55/846 variants (6.5%) · micro 56/1050 cases (5.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 16.61, nearest other category `release_a` at mean distance 15.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.248, nearest other category `release_e` at mean distance 0.547

## Release C (`release_c`)

Discharge pathway Release C for admitted cases.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative Release C (id=19) under the OR decomposition of goal id=6.

**Goal-model linkage:** 19 (Task): Release C

**Coverage:** macro 23/846 variants (2.7%) · micro 23/1050 cases (2.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 23.86, nearest other category `release_a` at mean distance 18.62

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.242, nearest other category `release_d` at mean distance 0.443

## Release D (`release_d`)

Discharge pathway Release D for admitted cases.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative Release D (id=20) under the OR decomposition of goal id=6.

**Goal-model linkage:** 20 (Task): Release D

**Coverage:** macro 23/846 variants (2.7%) · micro 23/1050 cases (2.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 19.47, nearest other category `release_a` at mean distance 17.33

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.298, nearest other category `release_e` at mean distance 0.442

## Release E (`release_e`)

Discharge pathway Release E for admitted cases.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative Release E (id=21) under the OR decomposition of goal id=6.

**Goal-model linkage:** 21 (Task): Release E

**Coverage:** macro 6/846 variants (0.7%) · micro 6/1050 cases (0.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 17.67, nearest other category `release_a` at mean distance 16.34

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.253, nearest other category `release_d` at mean distance 0.442

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0274` / `V0710` (category `release_c`): structural=177, profile=0.390
- `V0084` / `V0710` (category `release_c`): structural=174, profile=0.253
- `V0138` / `V0710` (category `release_c`): structural=173, profile=0.253
- `V0313` / `V0710` (category `release_c`): structural=173, profile=0.165
- `V0314` / `V0710` (category `release_c`): structural=173, profile=0.148
- `V0427` / `V0710` (category `release_c`): structural=173, profile=0.418
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

169/846 variants (20.0%), 324/1050 cases (30.9%) unassigned.

- `V0001`: The narrative ends at ER Sepsis Triage and does not involve any discharge pathway.
- `V0002`: The narrative ends at CRP and does not involve any discharge pathway.
- `V0003`: The narrative ends at Leucocytes and does not involve any discharge pathway.
- `V0004`: The narrative ends at IV Antibiotics without any admission or discharge pathway.
- `V0005`: The narrative ends at LacticAcid without admission or discharge.
- `V0006`: The narrative ends at IV Antibiotics without an admission or discharge pathway.
- `V0007`: The narrative ends at IV Antibiotics without an admission or discharge pathway.
- `V0009`: The narrative ends at IV Antibiotics without reaching a discharge pathway.
- `V0010`: The narrative terminates at ER Sepsis Triage without any discharge pathway.
- `V0011`: The narrative ends at IV Antibiotics without a discharge pathway.
- `V0012`: The narrative ends at IV Antibiotics without reaching a discharge category.
- `V0013`: The narrative terminates at Leucocytes without reaching a discharge pathway.
- `V0017`: The narrative terminates at ER Sepsis Triage without reaching a discharge pathway.
- `V0019`: The narrative ends at IV Antibiotics without reaching a discharge pathway.
- `V0020`: The narrative terminates at CRP without reaching a discharge pathway.
- `V0024`: The narrative ends at Admission NC without reaching any of the specified release categories.
- `V0025`: The narrative ends at IV Antibiotics without reaching a discharge pathway.
- `V0027`: The narrative ends at IV Antibiotics without reaching a discharge pathway.
- `V0029`: The narrative terminates at Leucocytes without reaching a discharge pathway.
- `V0031`: The narrative ends at LacticAcid without reaching a discharge pathway.
- `V0034`: The narrative ends at IV Liquid without reaching a discharge pathway.
- `V0036`: The narrative ends at CRP without reaching a discharge pathway.
- `V0038`: The narrative ends at IV Antibiotics without reaching a discharge pathway.
- `V0040`: The narrative ends at Admission NC without reaching a discharge pathway.
- `V0043`: The narrative terminates at LacticAcid without reaching a discharge pathway.
- `V0050`: The narrative terminates at CRP without reaching a discharge pathway.
- `V0056`: The variant ends with IV Antibiotics and does not reach any discharge pathway category.
- `V0062`: The variant ends with IV Antibiotics and does not reach any discharge pathway category.
- `V0081`: The variant ends with IV Liquid and does not reach any discharge pathway category.
- `V0088`: The variant ends with IV Antibiotics and does not reach any discharge pathway category.
- `V0092`: The variant ends with LacticAcid and does not reach any discharge pathway category.
- `V0111`: The variant ends at Admission NC without reaching any of the discharge categories.
- `V0117`: The variant results in Release D which is not among the listed categories.
- `V0127`: The variant terminates at LacticAcid without any discharge pathway.
- `V0132`: The variant terminates at IV Antibiotics without reaching a discharge pathway category.
- `V0133`: The variant terminates at IV Antibiotics without reaching a discharge pathway category.
- `V0137`: The variant terminates at LacticAcid without reaching a discharge pathway category.
- `V0146`: The variant terminates at Leucocytes without reaching a discharge pathway category.
- `V0148`: The variant terminates at IV Antibiotics without reaching a discharge pathway category.
- `V0187`: The narrative does not contain any valid discharge pathway matching the taxonomy categories.
- `V0197`: The narrative ends with Leucocytes and does not reach a discharge pathway category.
- `V0217`: The variant ends with IV Antibiotics and does not conclude with any of the release pathways.
- `V0219`: The variant ends with Leucocytes and does not conclude with any of the release pathways.
- `V0232`: The variant ends with IV Antibiotics and does not conclude with any of the release pathways.
- `V0234`: The variant ends with Leucocytes and does not conclude with any of the release pathways.
- `V0260`: The narrative terminates at IV Antibiotics and does not reach any of the specified release pathways.
- `V0268`: The narrative terminates at Leucocytes and does not reach a discharge pathway.
- `V0287`: The narrative terminates at CRP and does not reach a discharge pathway.
- `V0292`: The narrative terminates at Leucocytes and does not reach a discharge pathway.
- `V0295`: The narrative terminates at IV Antibiotics and does not reach any of the specified release pathways.
- `V0302`: The narrative ends with ER Sepsis Triage and does not reach any discharge pathway category.
- `V0305`: The process stops at IV Antibiotics and does not realize any release category.
- `V0322`: The process stops at IV Antibiotics without a discharge pathway.
- `V0325`: The process ends at IV Antibiotics and does not realize a release category.
- `V0330`: The process terminates at IV Liquid and does not reach a discharge category.
- `V0336`: The process stops at CRP without reaching a discharge pathway.
- `V0342`: The process finishes at CRP and does not include a release category.
- `V0349`: The process ends at ER Sepsis Triage and does not realize a release category.
- `V0365`: The process variant ends with Leucocytes and does not reach any release category.
- `V0368`: The process variant ends with Admission NC and does not reach any release category.
- `V0374`: The process variant ends with Leucocytes and does not reach any release category.
- `V0378`: The process variant ends with IV Antibiotics and does not reach any release category.
- `V0379`: The process variant ends with IV Antibiotics and does not reach any release category.
- `V0415`: The narrative ends with Admission NC and does not reach any specified release pathway.
- `V0417`: The narrative terminates at ER Triage without reaching a release pathway.
- `V0429`: The narrative terminates at IV Antibiotics without reaching a release pathway.
- `V0462`: The narrative outcome is CRP, which does not match any of the release pathways.
- `V0488`: The narrative outcome is IV Liquid, which does not match any of the release pathways.
- `V0492`: The narrative outcome is IV Liquid, which does not match any of the release pathways.
- `V0495`: The narrative outcome is IV Antibiotics, which does not match any of the release pathways.
- `V0501`: The narrative ends with IV Liquid and does not reach a discharge pathway category.
- `V0502`: The narrative ends with Admission NC and does not reach a final discharge pathway category.
- `V0507`: The narrative ends with IV Antibiotics and does not reach any discharge pathway category.
- `V0510`: The narrative ends with IV Antibiotics and does not reach any discharge pathway category.
- `V0516`: The narrative ends with Leucocytes and does not reach any discharge pathway category.
- `V0517`: The narrative ends with ER Triage and does not reach any discharge pathway category.
- `V0549`: The narrative ends with IV Liquid and does not reach any discharge pathway category.
- `V0556`: The outcome is Return ER, which does not match any of the defined release pathways.
- `V0558`: The outcome is Return ER, which does not match any of the defined release pathways.
- `V0559`: The outcome is Return ER, which does not match any of the defined release pathways.
- `V0560`: The outcome is Return ER, which does not match any of the defined release pathways.
- `V0564`: The outcome is Return ER, which does not match any of the defined release pathways.
- `V0565`: The outcome is Admission NC, which does not match any of the defined release pathways.
- `V0567`: The outcome is Return ER, which does not match any of the defined release pathways.
- `V0573`: The outcome is Return ER, which does not match any of the defined release pathways.
- `V0575`: The outcome is Leucocytes, which does not match any of the defined release pathways.
- `V0577`: The outcome is Return ER, which does not match any of the defined release pathways.
- `V0578`: The outcome is Return ER, which does not match any of the defined release pathways.
- `V0579`: The outcome is Return ER, which does not match any of the defined release pathways.
- `V0580`: The outcome is CRP, which does not match any of the defined release pathways.
- `V0584`: The outcome is IV Liquid, which does not match any of the defined release pathways.
- `V0585`: The outcome is LacticAcid, which does not match any of the defined release pathways.
- `V0587`: The outcome is CRP, which does not match any of the defined release pathways.
- `V0590`: The outcome is Return ER, which does not match any of the defined release pathways.
- `V0591`: The outcome is Return ER, which does not match any of the defined release pathways.
- `V0592`: The outcome is IV Antibiotics, which does not match any of the defined release pathways.
- `V0595`: The outcome is Return ER, which does not match any of the defined release pathways.
- `V0605`: The narrative outcome is Return ER rather than a standard release category.
- `V0614`: The narrative ends in Return ER after an intermediate Release A.
- `V0615`: The narrative ends in Return ER after an intermediate Release C.
- `V0625`: The narrative ends with Return ER.
- `V0627`: The narrative ends with Return ER.
- `V0631`: The narrative ends with Return ER.
- `V0632`: The narrative ends with Return ER.
- `V0635`: The narrative ends with Return ER.
- `V0636`: The outcome is LacticAcid, which does not correspond to any valid release category.
- `V0638`: The narrative ends with Return ER.
- `V0639`: The narrative ends with Return ER.
- `V0640`: The narrative ends with Return ER.
- `V0641`: The narrative ends with Return ER.
- `V0643`: The narrative ends with Return ER.
- `V0644`: The outcome is CRP, which does not correspond to any valid release category.
- `V0645`: The outcome is LacticAcid, which does not correspond to any valid release category.
- `V0646`: The narrative ends with Return ER.
- `V0649`: The narrative ends with Return ER.
- `V0650`: The narrative ends with Return ER.
- `V0654`: The narrative ends with Leucocytes and does not conclude with any of the release pathways.
- `V0663`: The process ends with Admission NC and does not complete a release pathway.
- `V0664`: The process terminates with IV Liquid and does not reach any release category.
- `V0676`: The process ends at IV Antibiotics without reaching a discharge pathway.
- `V0679`: The process terminates with IV Antibiotics and does not realize a release category.
- `V0685`: The process stops at IV Antibiotics without a release event.
- `V0689`: The process terminates at IV Antibiotics.
- `V0694`: The process stops at ER Sepsis Triage.
- `V0703`: The narrative does not culminate in any of the discharge pathways (Release A-E); its final activity is IV Liquid.
- `V0705`: Although the pathway passes through a release, the final outcome is Return ER rather than a recognized discharge pathway category.
- `V0707`: The process terminates at Admission NC without reaching any of the discharge categories.
- `V0708`: The narrative terminates at IV Antibiotics and does not reach a discharge pathway category.
- `V0712`: The process ultimately leads to Return ER, not realizing any of the discharge categories.
- `V0713`: The narrative ends at IV Antibiotics without reaching a release category.
- `V0719`: The narrative ends with Return ER after an intermediate Release A, therefore not fitting a primary discharge category.
- `V0720`: The final outcome is Return ER, rendering the discharge pathway category inapplicable.
- `V0721`: The final outcome is Return ER.
- `V0724`: The process ends with Return ER.
- `V0727`: The final outcome of the case is Return ER.
- `V0734`: The process ends with Return ER.
- `V0742`: The process terminates at LacticAcid without reaching a discharge pathway.
- `V0744`: The final outcome is Return ER.
- `V0745`: The final outcome is Return ER.
- `V0746`: The final outcome is Return ER.
- `V0748`: The final outcome is Return ER.
- `V0750`: The process terminates at IV Antibiotics without reaching a discharge pathway category.
- `V0759`: The outcome is IV Antibiotics and does not reach any discharge pathway category.
- `V0764`: The outcome is ER Sepsis Triage and does not complete a discharge category.
- `V0772`: The outcome is CRP and does not realize any discharge category.
- `V0774`: The outcome is ER Sepsis Triage without reaching a discharge category.
- `V0775`: The outcome is CRP and lacks a discharge pathway.
- `V0777`: The outcome is Leucocytes without achieving any discharge category.
- `V0778`: The outcome is Leucocytes and does not reach a discharge pathway.
- `V0791`: The outcome is IV Antibiotics and does not reach a discharge category.
- `V0804`: The narrative outcome is Return ER rather than a standard release category.
- `V0806`: The narrative outcome is Return ER rather than a standard release category.
- `V0808`: The narrative outcome is Return ER rather than a standard release category.
- `V0812`: The narrative outcome is Return ER rather than a standard release category.
- `V0815`: The narrative outcome is Return ER rather than a standard release category.
- `V0816`: The narrative does not conclude with any of the release pathways.
- `V0817`: The narrative outcome is Return ER rather than a standard release category.
- `V0820`: The narrative does not conclude with any of the release pathways.
- `V0821`: The narrative outcome is Return ER rather than a standard release category.
- `V0822`: The narrative outcome is Return ER rather than a standard release category.
- `V0823`: The narrative outcome is Return ER rather than a standard release category.
- `V0825`: The narrative outcome is Return ER rather than a standard release category.
- `V0826`: The narrative does not conclude with any of the release pathways.
- `V0827`: The narrative outcome is Return ER rather than a standard release category.
- `V0828`: The narrative outcome is Return ER rather than a standard release category.
- `V0832`: The narrative does not conclude with any of the release pathways.
- `V0834`: The narrative outcome is Return ER rather than a standard release category.
- `V0842`: The narrative outcome is Return ER rather than a standard release category.
- `V0843`: The narrative does not conclude with any of the release pathways.
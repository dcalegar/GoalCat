# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_axisdischarge_rep2` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Release A (`release_a`)

Represents the standard discharge pathway (Release A) for admitted patients who reach a captured discharge, helping to avoid post-discharge deterioration as measured by post-discharge ER return indicators.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release A (id=17). Observed in multiple variants such as V0008, V0066, and V0070 where patients successfully complete the inpatient stay and are discharged.

**Goal-model linkage:** 17 (Task): Release A

**Coverage:** macro 581/846 variants (68.7%) · micro 629/1050 cases (59.9%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.38, nearest other category `release_b` at mean distance 15.07

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.344, nearest other category `release_d` at mean distance 0.449

## Release B (`release_b`)

Represents discharge pathway B for admitted cases reaching a captured discharge, contributing to avoiding post-discharge deterioration as measured by post-discharge ER return indicators.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release B (id=18). Observed in variant V0068 and V0145 as a distinct terminal discharge milestone.

**Goal-model linkage:** 18 (Task): Release B

**Coverage:** macro 55/846 variants (6.5%) · micro 56/1050 cases (5.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 16.61, nearest other category `release_a` at mean distance 15.07

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.248, nearest other category `release_d` at mean distance 0.546

## Release C (`release_c`)

Represents discharge pathway C for admitted cases reaching a captured discharge, contributing to avoiding post-discharge deterioration as measured by post-discharge ER return indicators.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release C (id=19). Observed in variant V0710 where an exceptionally long and complex trace ultimately culminates in Release C.

**Goal-model linkage:** 19 (Task): Release C

**Coverage:** macro 24/846 variants (2.8%) · micro 24/1050 cases (2.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 23.18, nearest other category `release_a` at mean distance 18.29

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.258, nearest other category `release_d` at mean distance 0.440

## Release D (`release_d`)

Represents discharge pathway D for admitted cases reaching a captured discharge, contributing to avoiding post-discharge deterioration as measured by post-discharge ER return indicators.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release D (id=20). Observed in variant V0273 as the terminal activity concluding the patient's inpatient workflow.

**Goal-model linkage:** 20 (Task): Release D

**Coverage:** macro 22/846 variants (2.6%) · micro 22/1050 cases (2.1%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 19.21, nearest other category `release_a` at mean distance 17.07

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.291, nearest other category `release_c` at mean distance 0.440

## Release E (`release_e`)

Represents discharge pathway E for admitted cases reaching a captured discharge, contributing to avoiding post-discharge deterioration as measured by post-discharge ER return indicators.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release E (id=21). Retained as a declared alternative per standard decomposition mapping rules even though instances are sparse in this specific sample.

**Goal-model linkage:** 21 (Task): Release E

**Coverage:** macro 6/846 variants (0.7%) · micro 6/1050 cases (0.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 17.67, nearest other category `release_a` at mean distance 16.37

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.253, nearest other category `release_d` at mean distance 0.444

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

158/846 variants (18.7%), 313/1050 cases (29.8%) unassigned.

- `V0001`: The narrative ends at ER Sepsis Triage and does not reach a discharge pathway.
- `V0002`: The narrative ends at CRP testing and does not reach a discharge pathway.
- `V0003`: The narrative ends at Leucocytes testing and does not reach a discharge pathway.
- `V0004`: The narrative ends at IV Antibiotics administration and does not reach a discharge pathway.
- `V0005`: The narrative ends at LacticAcid testing and does not reach a discharge pathway.
- `V0006`: The narrative ends at IV Antibiotics and does not reach a discharge pathway.
- `V0007`: The narrative ends at IV Antibiotics and does not reach a discharge pathway.
- `V0009`: The narrative ends at IV Antibiotics and does not reach a discharge pathway.
- `V0010`: The narrative ends at ER Sepsis Triage and does not reach a discharge pathway.
- `V0011`: The narrative ends at IV Antibiotics and does not reach a discharge pathway.
- `V0012`: The narrative ends at IV Antibiotics and does not reach a discharge pathway.
- `V0013`: The narrative ends at Leucocytes and does not reach a discharge pathway.
- `V0017`: The narrative ends at ER Sepsis Triage and does not reach a discharge pathway.
- `V0019`: The narrative ends at IV Antibiotics and does not reach a discharge pathway.
- `V0020`: The narrative ends at CRP and does not reach a discharge pathway.
- `V0024`: The narrative ends at Admission NC and does not reach a captured discharge.
- `V0025`: The narrative ends at IV Antibiotics and does not reach a discharge pathway.
- `V0027`: The narrative ends at IV Antibiotics and does not reach a discharge pathway.
- `V0029`: The narrative ends at Leucocytes and does not reach a discharge pathway.
- `V0031`: The narrative ends at LacticAcid and does not reach a discharge pathway.
- `V0034`: The narrative ends at IV Liquid and does not reach a discharge pathway.
- `V0036`: The narrative ends at CRP and does not reach a discharge pathway.
- `V0038`: The narrative ends at IV Antibiotics and does not reach a discharge pathway.
- `V0040`: The narrative ends at Admission NC and does not reach a captured discharge.
- `V0043`: The narrative ends at LacticAcid and does not reach a discharge pathway.
- `V0050`: The narrative ends at CRP and does not reach a discharge pathway.
- `V0056`: The narrative ends with IV Antibiotics and does not reach a captured discharge pathway.
- `V0062`: The narrative terminates at IV Antibiotics without reaching a discharge category.
- `V0081`: The narrative terminates at IV Liquid without reaching a discharge category.
- `V0088`: The narrative terminates at IV Antibiotics without reaching a discharge category.
- `V0092`: The narrative terminates at LacticAcid without reaching a discharge category.
- `V0111`: The process ends at Admission NC without reaching any discharge category.
- `V0117`: The process records Release D, which does not map to release_a through release_e in the given taxonomy definition.
- `V0127`: The variant terminates at LacticAcid without achieving discharge.
- `V0132`: The case terminates at IV Antibiotics without reaching a discharge category.
- `V0133`: The process ends at IV Antibiotics without a discharge step.
- `V0137`: The variant terminates with LacticAcid and does not reach a discharge category.
- `V0146`: The variant ends at Leucocytes without reaching a discharge pathway.
- `V0148`: The process stops at IV Antibiotics without completing a discharge.
- `V0181`: The narrative does not terminate in a standard release category, ending with Leucocytes instead.
- `V0187`: The narrative is incomplete and does not reach any discharge pathway.
- `V0197`: The narrative ends abruptly at Leucocytes without completing a discharge path.
- `V0217`: The narrative ends with IV Antibiotics and does not reach a captured discharge.
- `V0219`: The narrative ends with Leucocytes and does not reach a captured discharge.
- `V0232`: The narrative ends with IV Antibiotics and does not reach a captured discharge.
- `V0234`: The narrative ends with Leucocytes and does not reach a captured discharge.
- `V0260`: The variant ends at IV Antibiotics without reaching a discharge event.
- `V0268`: The variant ends at Leucocytes without reaching a discharge event.
- `V0287`: The variant ends at CRP without reaching a discharge event.
- `V0292`: The variant ends at Leucocytes without reaching a discharge event.
- `V0295`: The variant ends at IV Antibiotics without reaching a discharge event.
- `V0302`: The narrative ends at ER Sepsis Triage and does not reach a captured discharge pathway.
- `V0305`: The case terminates at IV Antibiotics without reaching a discharge pathway.
- `V0322`: The process ends at IV Antibiotics without reaching a discharge destination.
- `V0325`: The narrative terminates at IV Antibiotics and lacks a discharge pathway.
- `V0330`: The narrative terminates at IV Liquid and does not reach a discharge category.
- `V0336`: The process stops at CRP and does not reach any discharge category.
- `V0342`: The narrative stops at CRP and has no discharge event.
- `V0349`: The process ends at ER Sepsis Triage without reaching a discharge pathway.
- `V0365`: The narrative ends with Leucocytes and does not reach any captured discharge pathway.
- `V0368`: The narrative terminates at Admission NC without reaching a discharge pathway.
- `V0374`: The narrative ends at Leucocytes and does not reach a discharge category.
- `V0378`: The narrative ends at IV Antibiotics and does not reach a discharge category.
- `V0379`: The narrative ends at IV Antibiotics without reaching discharge.
- `V0415`: The narrative ends at Admission NC without reaching any discharge category.
- `V0417`: The process terminates at ER Triage without reaching any discharge category.
- `V0429`: The process ends at IV Antibiotics without reaching a discharge category.
- `V0453`: The process variant ends with Return ER, which does not fit any of the discharge categories.
- `V0454`: The process variant ends with Return ER, which does not fit any of the discharge categories.
- `V0458`: The process variant ends with Return ER after an intermediate Release A, meaning the final outcome is Return ER.
- `V0460`: The process variant ends with Return ER, which does not fit any of the discharge categories.
- `V0462`: The process variant ends with CRP, which does not fit any of the discharge categories.
- `V0463`: The process variant ends with Return ER, which does not fit any of the discharge categories.
- `V0464`: The process variant ends with Return ER, which does not fit any of the discharge categories.
- `V0467`: The process variant ends with Return ER, which does not fit any of the discharge categories.
- `V0468`: The process variant ends with Return ER, which does not fit any of the discharge categories.
- `V0469`: The process variant ends with Return ER, which does not fit any of the discharge categories.
- `V0473`: The process variant ends with Return ER, which does not fit any of the discharge categories.
- `V0474`: The process variant ends with Return ER, which does not fit any of the discharge categories.
- `V0476`: The process variant ends with Return ER, which does not fit any of the discharge categories.
- `V0479`: The process variant ends with Return ER, which does not fit any of the discharge categories.
- `V0482`: The process variant ends with Return ER, which does not fit any of the discharge categories.
- `V0484`: The process variant ends with Return ER, which does not fit any of the discharge categories.
- `V0488`: The process variant ends with IV Liquid, which does not fit any of the discharge categories.
- `V0492`: The process variant ends with IV Liquid, which does not fit any of the discharge categories.
- `V0495`: The process variant ends with IV Antibiotics, which does not fit any of the discharge categories.
- `V0497`: The process variant ends with Return ER, which does not fit any of the discharge categories.
- `V0501`: The narrative ends with IV Liquid and does not reach a discharge pathway category.
- `V0502`: The narrative ends with Admission NC and does not reach a discharge pathway category.
- `V0507`: The narrative ends with IV Antibiotics and does not reach a discharge pathway category.
- `V0510`: The narrative ends with IV Antibiotics and does not reach a discharge pathway category.
- `V0516`: The narrative ends with Leucocytes and does not reach a discharge pathway category.
- `V0517`: The narrative ends with ER Triage and does not reach a discharge pathway category.
- `V0549`: The narrative ends with IV Liquid and does not reach a discharge pathway category.
- `V0565`: The variant terminates at Admission NC and does not reach a captured discharge.
- `V0575`: The process ends at Leucocytes and does not reach a captured discharge.
- `V0580`: The process ends at CRP and does not reach a captured discharge.
- `V0584`: The process ends at IV Liquid and does not reach a captured discharge.
- `V0585`: The process ends at LacticAcid and does not reach a captured discharge.
- `V0587`: The process ends at CRP and does not reach a captured discharge.
- `V0592`: The process ends at IV Antibiotics and does not reach a captured discharge.
- `V0636`: The narrative does not conclude with any captured discharge pathway; it ends with LacticAcid.
- `V0644`: The narrative does not conclude with any captured discharge pathway; it ends with CRP.
- `V0645`: The narrative does not conclude with any captured discharge pathway; it ends with LacticAcid.
- `V0654`: The process terminates at Leucocytes without reaching any of the specified release categories.
- `V0663`: The narrative terminates at Admission NC without reaching any release pathway.
- `V0664`: The process ends at IV Liquid, falling outside the defined discharge categories.
- `V0676`: The process stops at IV Antibiotics without reaching a discharge pathway.
- `V0679`: The process ends at IV Antibiotics without a discharge event.
- `V0685`: The sequence terminates at IV Antibiotics without concluding with a release pathway.
- `V0689`: The sequence stops at IV Antibiotics without reaching any release category.
- `V0694`: The pathway ends at ER Sepsis Triage, lacking any discharge event.
- `V0703`: The narrative ends with IV Liquid and does not reach a captured discharge pathway.
- `V0705`: The narrative culminates in Return ER after an initial release, which does not fit standard discharge pathways.
- `V0707`: The narrative ends at Admission NC without reaching a final discharge category.
- `V0708`: The narrative terminates at IV Antibiotics and does not reach a discharge pathway.
- `V0712`: The narrative results in a Return ER event following discharge, falling outside the main stable pathways.
- `V0713`: The narrative terminates at IV Antibiotics without reaching a discharge destination.
- `V0718`: The narrative concludes with Release D followed by Return ER, which does not map cleanly to standard stable outcomes.
- `V0719`: The narrative ends with a Return ER event.
- `V0720`: The narrative ends with a Return ER event.
- `V0721`: The narrative ends with a Return ER event.
- `V0724`: The narrative ends with a Return ER event.
- `V0727`: The narrative ends with a Return ER event.
- `V0734`: The narrative ends with a Return ER event.
- `V0742`: The narrative ends with LacticAcid and does not reach a discharge pathway.
- `V0744`: The narrative ends with a Return ER event.
- `V0745`: The narrative ends with a Return ER event.
- `V0746`: The narrative ends with a Return ER event.
- `V0748`: The narrative ends with a Return ER event.
- `V0750`: The narrative terminates at IV Antibiotics without reaching a discharge destination.
- `V0759`: The narrative outcome is IV Antibiotics and does not reach a captured discharge pathway.
- `V0764`: The sequence stops at ER Sepsis Triage and does not reach any discharge category.
- `V0772`: Outcome is CRP and does not reach discharge.
- `V0774`: Outcome is ER Sepsis Triage.
- `V0775`: Outcome is CRP.
- `V0777`: Outcome is Leucocytes.
- `V0778`: Outcome is Leucocytes.
- `V0791`: Outcome is IV Antibiotics.
- `V0804`: The narrative ends with Return ER, which indicates post-discharge deterioration rather than a successful captured discharge pathway.
- `V0806`: The narrative ends with Return ER, representing post-discharge deterioration rather than a standard discharge pathway.
- `V0808`: The narrative ends with Return ER, meaning it does not fall under any of the release pathways.
- `V0812`: The narrative ends with Return ER, indicating post-discharge deterioration rather than a finalized release category.
- `V0815`: The narrative ends with Return ER, indicating post-discharge deterioration.
- `V0816`: The narrative ends with IV Antibiotics, meaning it did not reach a captured discharge pathway.
- `V0817`: Although it has Release C earlier, the ultimate outcome is Return ER, representing post-discharge deterioration.
- `V0820`: The narrative ends with LacticAcid, lacking any final discharge pathway.
- `V0821`: The narrative ends with Return ER, representing post-discharge deterioration.
- `V0822`: The narrative ends with Return ER, indicating post-discharge deterioration.
- `V0823`: The narrative ends with Return ER, representing post-discharge deterioration.
- `V0825`: The narrative ends with Return ER, indicating post-discharge deterioration.
- `V0826`: The narrative ends with Admission NC, without reaching a discharge pathway.
- `V0827`: The narrative ends with Return ER, representing post-discharge deterioration.
- `V0828`: The narrative ends with Return ER, indicating post-discharge deterioration.
- `V0832`: The narrative ends with IV Antibiotics, lacking a discharge pathway.
- `V0834`: The narrative ends with Return ER, representing post-discharge deterioration.
- `V0842`: The narrative ends with Return ER, indicating post-discharge deterioration.
- `V0843`: The narrative ends with IV Liquid, lacking a final discharge pathway.
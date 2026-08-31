# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_axisdischarge_rep5` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Release A (`release_a`)

Patient discharge pathway A realizing captured discharge, contributing to avoiding post-discharge deterioration and measured against post-discharge ER return indicators.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release A under goal id=6. Observed in variants such as V0008.

**Goal-model linkage:** 17 (Task): Release A

**Coverage:** macro 566/846 variants (66.9%) · micro 614/1050 cases (58.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.35, nearest other category `release_b` at mean distance 15.04

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.342, nearest other category `release_d` at mean distance 0.454

## Release B (`release_b`)

Patient discharge pathway B realizing captured discharge, contributing to avoiding post-discharge deterioration and measured against post-discharge ER return indicators.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release B under goal id=6. Observed in variants such as V0068 and V0145.

**Goal-model linkage:** 18 (Task): Release B

**Coverage:** macro 55/846 variants (6.5%) · micro 56/1050 cases (5.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 16.61, nearest other category `release_a` at mean distance 15.04

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.248, nearest other category `release_e` at mean distance 0.547

## Release C (`release_c`)

Patient discharge pathway C realizing captured discharge, contributing to avoiding post-discharge deterioration and measured against post-discharge ER return indicators.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release C under goal id=6. Observed in variant V0710.

**Goal-model linkage:** 19 (Task): Release C

**Coverage:** macro 24/846 variants (2.8%) · micro 24/1050 cases (2.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 23.18, nearest other category `release_a` at mean distance 18.28

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.258, nearest other category `release_d` at mean distance 0.443

## Release D (`release_d`)

Patient discharge pathway D realizing captured discharge, contributing to avoiding post-discharge deterioration and measured against post-discharge ER return indicators.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release D under goal id=6. Observed in variant V0273.

**Goal-model linkage:** 20 (Task): Release D

**Coverage:** macro 22/846 variants (2.6%) · micro 22/1050 cases (2.1%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 19.82, nearest other category `release_a` at mean distance 17.68

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.296, nearest other category `release_c` at mean distance 0.443

## Release E (`release_e`)

Patient discharge pathway E realizing captured discharge, contributing to avoiding post-discharge deterioration and measured against post-discharge ER return indicators.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release E under goal id=6. Kept as a distinct category by default despite lack of sampled narratives.

**Goal-model linkage:** 21 (Task): Release E

**Coverage:** macro 6/846 variants (0.7%) · micro 6/1050 cases (0.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 17.67, nearest other category `release_a` at mean distance 16.36

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.253, nearest other category `release_d` at mean distance 0.445

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

173/846 variants (20.4%), 328/1050 cases (31.2%) unassigned.

- `V0001`: The narrative ends at ER Sepsis Triage and does not reach any discharge pathway.
- `V0002`: The narrative ends at CRP and does not reach a discharge pathway.
- `V0003`: The narrative ends at Leucocytes and does not reach a discharge pathway.
- `V0004`: The narrative ends at IV Antibiotics without reaching any discharge pathway.
- `V0005`: The narrative ends at LacticAcid without reaching a discharge pathway.
- `V0006`: The narrative ends at IV Antibiotics without reaching a discharge pathway.
- `V0007`: The narrative ends at IV Antibiotics without reaching a discharge pathway.
- `V0009`: The narrative ends at IV Antibiotics without reaching a discharge pathway.
- `V0010`: The narrative ends at ER Sepsis Triage and does not reach any discharge pathway.
- `V0011`: The narrative ends at IV Antibiotics without reaching a discharge pathway.
- `V0012`: The narrative ends at IV Antibiotics without reaching a discharge pathway.
- `V0013`: The narrative ends at Leucocytes without reaching a discharge pathway.
- `V0017`: The narrative ends at ER Sepsis Triage without reaching a discharge pathway.
- `V0019`: The narrative ends at IV Antibiotics without reaching a discharge pathway.
- `V0020`: The narrative ends at CRP without reaching a discharge pathway.
- `V0024`: The narrative ends at Admission NC without completing a discharge pathway.
- `V0025`: The narrative ends at IV Antibiotics without reaching a discharge pathway.
- `V0027`: The narrative ends at IV Antibiotics without reaching a discharge pathway.
- `V0029`: The narrative ends at Leucocytes without reaching a discharge pathway.
- `V0031`: The narrative ends at LacticAcid without reaching a discharge pathway.
- `V0034`: The narrative ends at IV Liquid without reaching a discharge pathway.
- `V0036`: The narrative ends at CRP without reaching a discharge pathway.
- `V0038`: The narrative ends at IV Antibiotics without reaching a discharge pathway.
- `V0040`: The narrative ends at Admission NC without completing a discharge pathway.
- `V0043`: The narrative ends at LacticAcid without reaching a discharge pathway.
- `V0050`: The narrative ends at CRP without reaching a discharge pathway.
- `V0056`: The narrative ends in IV Antibiotics and does not reach any discharge category.
- `V0062`: The process terminates at IV Antibiotics without any discharge outcome.
- `V0081`: The process terminates at IV Liquid without reaching a discharge category.
- `V0088`: The process terminates at IV Antibiotics without reaching a discharge category.
- `V0092`: The process terminates at LacticAcid without a discharge category.
- `V0111`: The narrative ends in Admission NC without reaching a discharge category.
- `V0117`: The narrative culminates in Release D, which is not part of the defined release categories.
- `V0127`: The narrative terminates at LacticAcid without reaching a release category.
- `V0132`: The narrative terminates at IV Antibiotics without reaching a release category.
- `V0133`: The narrative terminates at IV Antibiotics without reaching a release category.
- `V0137`: The narrative terminates at LacticAcid without reaching a release category.
- `V0146`: The narrative terminates at Leucocytes without reaching a release category.
- `V0148`: The narrative terminates at IV Antibiotics without reaching a release category.
- `V0181`: The narrative ends with Leucocytes rather than a known discharge pathway, thus it falls into the residual.
- `V0187`: The narrative ends with CRP and does not complete a discharge pathway, falling into the residual.
- `V0197`: The narrative ends with Leucocytes and does not complete a discharge pathway, falling into the residual.
- `V0217`: The variant does not culminate in any release category.
- `V0219`: The variant does not culminate in any release category.
- `V0232`: The variant does not culminate in any release category.
- `V0234`: The variant does not culminate in any release category.
- `V0260`: The process terminates at IV Antibiotics without reaching any patient discharge pathway.
- `V0268`: The process terminates at Leucocytes without reaching any patient discharge pathway.
- `V0287`: The process terminates at CRP without reaching any patient discharge pathway.
- `V0292`: The process terminates at Leucocytes without reaching any patient discharge pathway.
- `V0295`: The process terminates at IV Antibiotics without reaching any patient discharge pathway.
- `V0302`: The process terminates at ER Sepsis Triage and does not realize a discharge pathway.
- `V0305`: The process terminates early at IV Antibiotics without a discharge event.
- `V0322`: The process terminates at IV Antibiotics without any discharge event.
- `V0325`: The process terminates at IV Antibiotics without a discharge category.
- `V0330`: The process terminates at IV Liquid without reaching a discharge pathway.
- `V0336`: The process terminates at CRP without a discharge category.
- `V0342`: The process terminates at CRP without a discharge event.
- `V0349`: The process terminates at ER Sepsis Triage without a discharge event.
- `V0352`: The narrative ends with Return ER rather than a recognized release pathway.
- `V0353`: The narrative ends with Return ER instead of a discharge pathway category.
- `V0357`: The final activity is Return ER, so no release category is realized.
- `V0358`: The narrative terminates in Return ER.
- `V0359`: The outcome of the variant is Return ER.
- `V0364`: The outcome is Return ER, not a designated release category.
- `V0365`: The narrative terminates at Leucocytes rather than a release category.
- `V0366`: The variant ends with Return ER.
- `V0367`: The narrative terminates with Return ER.
- `V0368`: The outcome is Admission NC, which does not fit any release category.
- `V0369`: The variant's outcome is Return ER.
- `V0370`: The outcome is Return ER.
- `V0374`: The outcome is Leucocytes, not a release category.
- `V0378`: The outcome is IV Antibiotics, which is not a release category.
- `V0379`: The outcome is IV Antibiotics.
- `V0382`: The narrative concludes with Return ER.
- `V0385`: The outcome is Return ER.
- `V0386`: The outcome is Return ER.
- `V0398`: The outcome is Return ER.
- `V0415`: The narrative terminates at Admission NC and does not reach a discharge pathway category.
- `V0417`: The narrative terminates at ER Triage and does not complete a discharge pathway.
- `V0429`: The narrative terminates at IV Antibiotics and does not reach a discharge pathway category.
- `V0453`: The narrative culminates in Return ER rather than a matching discharge category.
- `V0454`: The narrative ends with Return ER.
- `V0458`: The narrative ends with Return ER.
- `V0460`: The narrative ends with Return ER.
- `V0462`: The outcome is CRP, not one of the release categories.
- `V0463`: The narrative ends with Return ER.
- `V0464`: The narrative ends with Return ER.
- `V0467`: The narrative ends with Return ER.
- `V0468`: The narrative ends with Return ER.
- `V0469`: The narrative ends with Return ER.
- `V0473`: The narrative ends with Return ER.
- `V0474`: The narrative ends with Return ER.
- `V0476`: The narrative ends with Return ER.
- `V0479`: The narrative ends with Return ER.
- `V0482`: The narrative ends with Return ER.
- `V0484`: The narrative ends with Return ER.
- `V0488`: The outcome is IV Liquid, not a release category.
- `V0492`: The outcome is IV Liquid, not a release category.
- `V0495`: The outcome is IV Antibiotics, not a release category.
- `V0497`: The narrative ends with Return ER.
- `V0501`: The narrative outcome is IV Liquid, which does not conclude with any of the release pathways defined in the taxonomy.
- `V0502`: The narrative outcome is Admission NC, lacking a discharge category.
- `V0507`: The narrative outcome is IV Antibiotics, which does not correspond to a release pathway.
- `V0510`: The narrative outcome is IV Antibiotics without any release event.
- `V0516`: The narrative outcome is Leucocytes, which is not a discharge pathway.
- `V0517`: The narrative outcome is ER Triage, which does not constitute a discharge event.
- `V0549`: The narrative outcome is IV Liquid, lacking a discharge event.
- `V0556`: The process variant ends with Return ER after an initial Release A, which does not map cleanly to a standard single discharge pathway completion without return.
- `V0558`: The process variant ends with Return ER.
- `V0559`: The process variant ends with Return ER.
- `V0560`: The process variant ends with Return ER.
- `V0564`: The process variant ends with Return ER.
- `V0565`: The process variant ends with Admission NC and does not reach a release outcome.
- `V0567`: The process variant ends with Return ER.
- `V0573`: The process variant ends with Return ER.
- `V0575`: The process variant ends with Leucocytes and does not reach a release outcome.
- `V0577`: The process variant ends with Return ER.
- `V0578`: The process variant ends with Return ER.
- `V0579`: The process variant ends with Return ER.
- `V0580`: The process variant ends with CRP and does not reach a release outcome.
- `V0581`: The process variant ends with Return ER.
- `V0584`: The process variant ends with IV Liquid and does not reach a release outcome.
- `V0585`: The process variant ends with LacticAcid and does not reach a release outcome.
- `V0587`: The process variant ends with CRP and does not reach a release outcome.
- `V0590`: The process variant ends with Return ER.
- `V0591`: The process variant ends with Return ER.
- `V0592`: The process variant ends with IV Antibiotics and does not reach a release outcome.
- `V0595`: The process variant ends with Return ER.
- `V0636`: The narrative ends prematurely with LacticAcid and does not realize any of the release pathways.
- `V0644`: The narrative ends prematurely with CRP and does not realize any of the release pathways.
- `V0645`: The narrative ends prematurely with LacticAcid and does not realize any of the release pathways.
- `V0654`: The narrative ends with Leucocytes and does not culminate in any release pathway.
- `V0663`: The narrative ends with Admission NC and does not reach a discharge category.
- `V0664`: The narrative ends with IV Liquid and does not reach a discharge category.
- `V0676`: The narrative ends with IV Antibiotics and does not reach a discharge category.
- `V0679`: The narrative ends with IV Antibiotics and does not reach a discharge category.
- `V0685`: The narrative ends with IV Antibiotics and does not reach a discharge category.
- `V0689`: The narrative ends with IV Antibiotics and does not reach a discharge category.
- `V0694`: The narrative ends with ER Sepsis Triage and does not reach a discharge category.
- `V0703`: The narrative ends in IV Liquid without a discharge outcome, so no release category fits.
- `V0707`: The narrative terminates at Admission NC without a release event.
- `V0708`: The narrative terminates at IV Antibiotics without a release event.
- `V0713`: The narrative terminates at IV Antibiotics without a release event.
- `V0742`: The narrative terminates at LacticAcid without a release event.
- `V0750`: The narrative terminates at IV Antibiotics without a release event.
- `V0759`: The outcome is IV Antibiotics rather than a discharge pathway, so it does not fit any release category.
- `V0764`: The process stops at ER Sepsis Triage and does not reach a discharge category.
- `V0772`: The narrative outcome is CRP, which does not correspond to any release category.
- `V0774`: The process terminates at ER Sepsis Triage, lacking any release event.
- `V0775`: The narrative outcome is CRP, with no discharge pathway realized.
- `V0777`: The narrative concludes with Leucocytes, not a discharge category.
- `V0778`: The sequence ends with Leucocytes and does not reach a release category.
- `V0791`: The outcome is IV Antibiotics, lacking any discharge event.
- `V0804`: The narrative concludes with Return ER after Release A, so it does not cleanly realize the standard discharge pathway category due to post-discharge ER return.
- `V0806`: The narrative concludes with Return ER, meaning it does not fit the successful discharge pathway.
- `V0808`: The narrative results in a Return ER event following Release A.
- `V0812`: The narrative ends with a Return ER outcome.
- `V0815`: The narrative ends with a Return ER outcome.
- `V0816`: The narrative ends with IV Antibiotics and does not reach any discharge category.
- `V0817`: The narrative ends with Return ER despite a Release C marker.
- `V0820`: The narrative stops at LacticAcid and does not reach a discharge category.
- `V0821`: The narrative ends with Return ER.
- `V0822`: The narrative ends with Return ER.
- `V0823`: The narrative ends with Return ER.
- `V0825`: The narrative ends with Return ER.
- `V0826`: The narrative stops at Admission NC.
- `V0827`: The narrative ends with Return ER.
- `V0828`: The narrative ends with Return ER.
- `V0832`: The narrative stops at IV Antibiotics.
- `V0834`: The narrative ends with Return ER.
- `V0842`: The narrative ends with Return ER.
- `V0843`: The narrative stops at IV Liquid.
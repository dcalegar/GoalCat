# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_no_sample_axisdischarge_rep1` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Release A Discharge (`release_a`)

Represents the discharge pathway through Release A, which helps avoid post-discharge deterioration and contributes to overall discharge completion.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative Release A (id=17) under the OR-decomposition of goal id=6.

**Goal-model linkage:** 17 (Task): Release A

**Coverage:** macro 569/846 variants (67.3%) · micro 617/1050 cases (58.8%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.40, nearest other category `release_b` at mean distance 15.07

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.343, nearest other category `release_d` at mean distance 0.449

## Release B Discharge (`release_b`)

Represents the discharge pathway through Release B, which helps avoid post-discharge deterioration and contributes to overall discharge completion.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative Release B (id=18) under the OR-decomposition of goal id=6.

**Goal-model linkage:** 18 (Task): Release B

**Coverage:** macro 55/846 variants (6.5%) · micro 56/1050 cases (5.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 16.61, nearest other category `release_a` at mean distance 15.07

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.248, nearest other category `release_c` at mean distance 0.543

## Release C Discharge (`release_c`)

Represents the discharge pathway through Release C, leading to a captured discharge for the admitted case.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative Release C (id=19) under the OR-decomposition of goal id=6.

**Goal-model linkage:** 19 (Task): Release C

**Coverage:** macro 21/846 variants (2.5%) · micro 21/1050 cases (2.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 25.08, nearest other category `release_a` at mean distance 19.33

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.201, nearest other category `release_d` at mean distance 0.452

## Release D Discharge (`release_d`)

Represents the discharge pathway through Release D, leading to a captured discharge for the admitted case.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative Release D (id=20) under the OR-decomposition of goal id=6.

**Goal-model linkage:** 20 (Task): Release D

**Coverage:** macro 23/846 variants (2.7%) · micro 23/1050 cases (2.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 18.19, nearest other category `release_a` at mean distance 16.41

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.294, nearest other category `release_e` at mean distance 0.442

## Release E Discharge (`release_e`)

Represents the discharge pathway through Release E, leading to a captured discharge for the admitted case.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative Release E (id=21) under the OR-decomposition of goal id=6.

**Goal-model linkage:** 21 (Task): Release E

**Coverage:** macro 6/846 variants (0.7%) · micro 6/1050 cases (0.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 17.67, nearest other category `release_a` at mean distance 16.40

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.253, nearest other category `release_d` at mean distance 0.442

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

172/846 variants (20.3%), 327/1050 cases (31.1%) unassigned.

- `V0001`: The variant ends in ER Sepsis Triage and does not reach any discharge pathway.
- `V0002`: The variant terminates at CRP and does not complete a discharge pathway.
- `V0003`: The variant terminates at Leucocytes without reaching a discharge destination.
- `V0004`: The variant ends in IV Antibiotics and does not involve any discharge category.
- `V0005`: The variant terminates at LacticAcid and does not reach a discharge pathway.
- `V0006`: The variant ends with IV Antibiotics and does not proceed to discharge.
- `V0007`: The variant concludes with IV Antibiotics without reaching a discharge destination.
- `V0009`: The variant ends in IV Antibiotics and does not reach a discharge category.
- `V0010`: The variant terminates at ER Sepsis Triage and lacks a discharge activity.
- `V0011`: The variant ends at IV Antibiotics without reaching a discharge destination.
- `V0012`: The variant concludes with IV Antibiotics and does not reach any discharge category.
- `V0013`: The variant ends at Leucocytes and does not include a discharge pathway.
- `V0017`: The variant terminates at ER Sepsis Triage and does not reach a discharge category.
- `V0019`: The variant ends in IV Antibiotics and does not reach a discharge destination.
- `V0020`: The variant terminates at CRP without reaching any discharge pathway.
- `V0024`: The variant ends at Admission NC and does not reach a specific release pathway category.
- `V0025`: The variant terminates at IV Antibiotics without completing a discharge pathway.
- `V0027`: The variant ends with IV Antibiotics and does not reach any discharge category.
- `V0029`: The variant ends with Leucocytes and does not reach a discharge category.
- `V0031`: The variant ends with LacticAcid and does not reach a discharge category.
- `V0034`: The variant ends with IV Liquid and does not reach a discharge category.
- `V0036`: The variant ends with CRP and does not reach a discharge category.
- `V0038`: The variant ends with IV Antibiotics and does not reach a discharge category.
- `V0040`: The variant ends with Admission NC and does not reach a discharge category.
- `V0043`: The variant ends with LacticAcid and does not reach a discharge category.
- `V0050`: The variant ends with CRP and does not reach a discharge category.
- `V0056`: The narrative terminates at IV Antibiotics without reaching any discharge pathway.
- `V0062`: The narrative terminates at IV Antibiotics without reaching any discharge pathway.
- `V0081`: The variant ends with IV Liquid and does not reach any discharge pathway.
- `V0088`: The variant ends with IV Antibiotics and does not complete a discharge pathway.
- `V0092`: The variant ends with LacticAcid and does not achieve a discharge outcome.
- `V0111`: The process terminates at Admission NC without reaching any of the specified release categories.
- `V0127`: The outcome is LacticAcid, which does not correspond to any discharge category.
- `V0132`: The process ends at IV Antibiotics, which does not fit any discharge pathway.
- `V0133`: The process terminates with IV Antibiotics, lacking a discharge category realization.
- `V0137`: The final activity is LacticAcid, which does not map to any discharge category.
- `V0146`: The process ends at Leucocytes, which does not match any discharge category.
- `V0148`: The outcome is IV Antibiotics, which is not a discharge pathway category.
- `V0187`: The narrative does not reach any discharge pathway, ending in diagnostic activities.
- `V0197`: The narrative does not reach any discharge pathway, ending in diagnostic activities.
- `V0217`: The narrative terminates with 'IV Antibiotics' and does not reach any of the specified discharge categories.
- `V0219`: The process stops at 'Leucocytes' and does not complete a discharge pathway.
- `V0232`: The narrative ends at IV Antibiotics and does not reach any discharge category.
- `V0234`: The narrative ends at Leucocytes and does not reach any discharge category.
- `V0260`: The narrative terminates at IV Antibiotics and does not reach any discharge pathway.
- `V0268`: The narrative terminates at Leucocytes and does not reach any discharge pathway.
- `V0287`: The process terminates at CRP and does not reach any discharge pathway.
- `V0292`: The narrative ends abruptly at Leucocytes without reaching any discharge destination.
- `V0295`: The process stops at IV Antibiotics and does not complete a discharge pathway.
- `V0302`: The variant terminates at ER Sepsis Triage and does not reach a discharge pathway.
- `V0305`: The variant terminates at IV Antibiotics without reaching any discharge category.
- `V0322`: The variant terminates at IV Antibiotics without reaching a discharge category.
- `V0325`: The variant terminates at IV Antibiotics without reaching any discharge category.
- `V0330`: The process terminates at IV Liquid without reaching any discharge outcome.
- `V0336`: The process terminates at CRP and does not complete a discharge pathway.
- `V0342`: The process stops at CRP without reaching a discharge pathway.
- `V0349`: The process terminates at ER Sepsis Triage and does not reach a discharge category.
- `V0365`: The outcome is Leucocytes, which does not correspond to any of the defined discharge categories.
- `V0368`: The outcome is Admission NC, so no release pathway is realized.
- `V0374`: The narrative terminates at Leucocytes, not realizing any discharge category.
- `V0378`: The variant ends with IV Antibiotics and does not reach any discharge pathway.
- `V0379`: The variant ends with IV Antibiotics and does not reach any discharge pathway.
- `V0382`: The narrative ends with Return ER after Release A, so it does not conclude as a primary release category.
- `V0385`: The narrative ultimately results in Return ER, making none of the standard release categories applicable.
- `V0386`: The narrative ends with Return ER following Release A, meaning it does not fit the discharge category criteria.
- `V0398`: The narrative ends with Return ER after Release A, so it does not correspond to a direct discharge category.
- `V0415`: The narrative ends at 'Admission NC' and does not reach any discharge pathway category.
- `V0417`: The narrative ends at 'ER Triage' and does not reach any discharge pathway category.
- `V0427`: The narrative outcome is Return ER, which does not correspond to any of the specified release categories.
- `V0429`: The narrative terminates at IV Antibiotics, lacking a discharge category.
- `V0435`: The narrative outcome is Return ER after a release, which does not match a direct terminal discharge category from the taxonomy.
- `V0437`: The narrative outcome is Return ER after Release D, which does not map cleanly into the specific discharge goal-model axis.
- `V0440`: The narrative outcome is Return ER following Release A.
- `V0441`: The narrative outcome is Return ER following Release A.
- `V0442`: The narrative outcome is Return ER following Release A.
- `V0443`: The narrative outcome is Return ER following Release A.
- `V0447`: The narrative outcome is Return ER following Release C.
- `V0448`: The narrative outcome is Return ER following Release A.
- `V0449`: The narrative outcome is Return ER following Release A.
- `V0453`: The variant ends with Return ER after an intermediate Release A, so it does not cleanly realize a primary discharge category.
- `V0454`: The variant results in a Return ER outcome following Release A.
- `V0458`: The variant results in a Return ER outcome.
- `V0460`: The variant results in a Return ER outcome.
- `V0462`: The variant ends with CRP rather than a discharge pathway.
- `V0463`: The variant results in a Return ER outcome.
- `V0464`: The variant results in a Return ER outcome.
- `V0467`: The variant results in a Return ER outcome.
- `V0468`: The variant results in a Return ER outcome.
- `V0469`: The variant results in a Return ER outcome.
- `V0473`: The variant results in a Return ER outcome.
- `V0474`: The variant results in a Return ER outcome.
- `V0488`: The variant ends with IV Liquid and does not reach any discharge category.
- `V0492`: The variant ends with IV Liquid without completing a discharge category.
- `V0495`: The process ends at IV Antibiotics without reaching a discharge destination.
- `V0501`: The narrative ends with IV Liquid and does not reach any of the specified release pathways.
- `V0502`: The narrative ends with Admission NC and does not reach any of the specified release pathways.
- `V0507`: The narrative terminates at IV Antibiotics without reaching a discharge destination.
- `V0510`: The narrative ends at IV Antibiotics and does not reach any release destination.
- `V0516`: The narrative ends with Leucocytes and does not reach a release pathway.
- `V0517`: The narrative terminates at ER Triage without reaching any release category.
- `V0549`: The variant ends with IV Liquid and does not reach any of the specified release pathways.
- `V0556`: The outcome is Return ER, which does not match any of the release pathways.
- `V0558`: The outcome is Return ER, which does not match any of the release pathways.
- `V0559`: The outcome is Return ER, which does not match any of the release pathways.
- `V0560`: The outcome is Return ER, which does not match any of the release pathways.
- `V0564`: The outcome is Return ER, which does not match any of the release pathways.
- `V0565`: The outcome is Admission NC, which does not match any of the release pathways.
- `V0567`: The outcome is Return ER, which does not match any of the release pathways.
- `V0573`: The outcome is Return ER, which does not match any of the release pathways.
- `V0575`: The outcome is Leucocytes, which does not match any of the release pathways.
- `V0580`: The outcome is CRP and does not correspond to any discharge release pathway category.
- `V0584`: The outcome is IV Liquid and does not correspond to any discharge release pathway category.
- `V0585`: The outcome is LacticAcid and does not correspond to any discharge release pathway category.
- `V0587`: The outcome is CRP and does not correspond to any discharge release pathway category.
- `V0592`: The outcome is IV Antibiotics and does not correspond to any discharge release pathway category.
- `V0605`: The narrative results in a readmission (Return ER) rather than a final discharge category.
- `V0614`: The outcome is a return to the ER following a temporary Release A, making it part of the residual.
- `V0615`: The narrative involves a return to the ER after Release C, so it falls into the residual.
- `V0625`: The patient returns to the ER after Release A, placing this variant in the residual category.
- `V0636`: The narrative outcome is LacticAcid, which does not match any of the release pathways in the taxonomy.
- `V0644`: The variant outcome is CRP, which does not correspond to any discharge category.
- `V0645`: The variant outcome is LacticAcid, which is not part of the discharge taxonomy.
- `V0654`: The narrative ends with Leucocytes and does not culminate in any of the discharge pathways.
- `V0663`: The narrative ends at Admission NC without reaching any of the specified discharge categories.
- `V0664`: The narrative stops at IV Liquid without completing any discharge pathway.
- `V0670`: Although Release A appears, the final activity is Leucocytes after a return to the ER, not fitting a final discharge category cleanly.
- `V0676`: The narrative ends with IV Antibiotics and does not reach any discharge pathway.
- `V0679`: The narrative terminates at IV Antibiotics without a discharge activity.
- `V0685`: The case sequence stops at IV Antibiotics without any discharge events.
- `V0689`: The variant ends at IV Antibiotics and lacks a discharge category.
- `V0694`: The trace stops at ER Sepsis Triage and does not reach any discharge category.
- `V0703`: The narrative ends with IV Liquid and does not reach any discharge destination category.
- `V0705`: The narrative concludes with Return ER after an initial Release A, which does not map cleanly to a primary discharge category.
- `V0707`: The narrative ends with Admission NC and does not reach a terminal discharge pathway.
- `V0708`: The narrative ends with IV Antibiotics and does not reach a terminal discharge pathway.
- `V0712`: The narrative concludes with Return ER following Release A.
- `V0713`: The narrative terminates at IV Antibiotics without reaching a discharge pathway.
- `V0742`: The narrative ends with LacticAcid instead of any release category.
- `V0750`: The narrative ends with IV Antibiotics rather than any release category.
- `V0759`: The outcome is IV Antibiotics, which does not match any of the specified discharge categories.
- `V0764`: The outcome is ER Sepsis Triage, which is not a discharge category.
- `V0772`: The narrative ends with CRP, which does not fit any of the discharge categories.
- `V0774`: The outcome is ER Sepsis Triage, which is not a discharge category.
- `V0775`: The final activity is CRP, which does not correspond to any discharge category.
- `V0777`: The narrative terminates at Leucocytes without reaching any discharge pathway.
- `V0778`: The narrative terminates at Leucocytes and does not complete any discharge pathway.
- `V0779`: The narrative ends with Return ER after Release A, so it does not represent a standard completion of the release category.
- `V0785`: Although Release A occurs, the final outcome of the variant is Return ER, rendering it part of the residual.
- `V0787`: The final outcome is Return ER after Release A, meaning it does not fit the discharge capture goal cleanly.
- `V0791`: The narrative terminates at IV Antibiotics and does not reach any discharge category.
- `V0794`: The process ends with Return ER, placing it outside the standard discharge completion categories.
- `V0797`: The final outcome is Return ER, making it fall into the residual category.
- `V0798`: The narrative ultimately results in Return ER, not a direct discharge completion pathway.
- `V0804`: The process variant ends with Return ER after Release A, so it does not represent a final successful discharge within the specified categories.
- `V0806`: The process variant ends with Return ER after Release A, so it does not represent a final successful discharge within the specified categories.
- `V0808`: The process variant ends with Return ER after Release A, so it does not represent a final successful discharge within the specified categories.
- `V0812`: The process variant ends with Return ER after Release A, so it does not represent a final successful discharge within the specified categories.
- `V0815`: The process variant ends with Return ER after Release A, so it does not represent a final successful discharge within the specified categories.
- `V0816`: The process variant ends at IV Antibiotics and does not reach a discharge category.
- `V0817`: The process variant ends with Return ER after Release C, so it does not represent a final successful discharge within the specified categories.
- `V0820`: The process variant ends at LacticAcid and does not reach a discharge category.
- `V0821`: The process variant ends with Return ER after Release A, so it does not represent a final successful discharge within the specified categories.
- `V0822`: The process variant ends with Return ER after Release A, so it does not represent a final successful discharge within the specified categories.
- `V0823`: The process variant ends with Return ER after Release A, so it does not represent a final successful discharge within the specified categories.
- `V0825`: The process variant ends with Return ER after Release A, so it does not represent a final successful discharge within the specified categories.
- `V0826`: The narrative ends with Admission NC and does not reach any discharge activity.
- `V0827`: The narrative terminates with Return ER after Release A, representing a readmission path rather than a pure discharge category realization.
- `V0828`: The narrative terminates with Return ER following Release A.
- `V0832`: The narrative ends prematurely with IV Antibiotics and does not complete a discharge pathway.
- `V0834`: The narrative finishes with Return ER following Release A.
- `V0842`: The narrative terminates with Return ER after Release A.
- `V0843`: The narrative ends with IV Liquid and does not reach a discharge category.
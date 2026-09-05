# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_axisdischarge_pertC_distractor_6_112_rep4` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Release A (`release_a`)

Represents the standard discharge pathway (Release A) for an admitted patient, helping to avoid post-discharge deterioration and measured against post-discharge ER returns.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release A (id=17) which is observed in multiple narrative variants (e.g. V0008, V0065, V0070) concluding normal inpatient care pathways.

**Goal-model linkage:** 17 (Task): Release A

**Coverage:** macro 594/846 variants (70.2%) · micro 642/1050 cases (61.1%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.31, nearest other category `release_b` at mean distance 15.10

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.347, nearest other category `release_d` at mean distance 0.445

## Release B (`release_b`)

Represents discharge pathway B for an admitted patient, contributing to avoiding post-discharge deterioration and monitored via post-discharge ER return indicators.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release B (id=18) observed in rare and extended inpatient recovery variants such as V0068 and V0145.

**Goal-model linkage:** 18 (Task): Release B

**Coverage:** macro 54/846 variants (6.4%) · micro 55/1050 cases (5.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 16.68, nearest other category `release_a` at mean distance 15.10

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.230, nearest other category `release_c` at mean distance 0.541

## Release C (`release_c`)

Represents discharge pathway C for an admitted patient, aligning with long-term inpatient care outcomes and post-discharge stability.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release C (id=19) which is realized in long-running complex variants such as V0710.

**Goal-model linkage:** 19 (Task): Release C

**Coverage:** macro 22/846 variants (2.6%) · micro 22/1050 cases (2.1%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 24.29, nearest other category `release_a` at mean distance 18.83

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.225, nearest other category `release_d` at mean distance 0.447

## Release D (`release_d`)

Represents discharge pathway D for an admitted patient, contributing to avoidance of post-discharge deterioration.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release D (id=20) observed in length-high diagnostic variants like V0273.

**Goal-model linkage:** 20 (Task): Release D

**Coverage:** macro 23/846 variants (2.7%) · micro 23/1050 cases (2.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 18.19, nearest other category `release_a` at mean distance 16.36

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.294, nearest other category `release_e` at mean distance 0.442

## Release E (`release_e`)

Represents discharge pathway E for an admitted patient, targeting safe discharge transitions.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release E (id=21) based on the goal-model decomposition axis.

**Goal-model linkage:** 21 (Task): Release E

**Coverage:** macro 6/846 variants (0.7%) · micro 6/1050 cases (0.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 17.67, nearest other category `release_a` at mean distance 16.36

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.253, nearest other category `release_d` at mean distance 0.442

## Release F (`release_f`)

Represents discharge pathway F for an admitted patient, concluding the inpatient treatment trajectory.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release F (id=112) based on the goal-model decomposition axis.

**Goal-model linkage:** 112 (Task): Release F

**Coverage:** macro 0/846 variants (0.0%) · micro 0/1050 cases (0.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a, nearest other category `None` at mean distance n/a

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a, nearest other category `None` at mean distance n/a

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

147/846 variants (17.4%), 302/1050 cases (28.8%) unassigned.

- `V0001`: This variant ends at ER Sepsis Triage and does not reach any discharge pathway.
- `V0002`: This variant ends at CRP diagnostic testing and does not progress to any discharge pathway.
- `V0003`: This variant terminates with Leucocytes testing and does not reach a discharge pathway.
- `V0004`: This variant concludes with IV Antibiotics administration without proceeding to discharge.
- `V0005`: This variant ends at LacticAcid testing and does not reach any discharge pathway.
- `V0006`: This variant terminates after IV Antibiotics treatment without reaching discharge.
- `V0007`: This variant ends with IV Antibiotics and does not progress to a discharge pathway.
- `V0009`: This variant ends at IV Antibiotics without reaching a discharge pathway.
- `V0010`: This variant concludes with ER Sepsis Triage and does not reach any discharge pathway.
- `V0011`: This variant ends with IV Antibiotics administration and does not reach discharge.
- `V0012`: This variant terminates at IV Antibiotics without proceeding to a discharge pathway.
- `V0013`: This variant ends at Leucocytes testing and does not reach any discharge pathway.
- `V0017`: This variant ends at ER Sepsis Triage and does not reach any discharge pathway.
- `V0019`: This variant terminates at IV Antibiotics without reaching a discharge pathway.
- `V0020`: This variant ends at CRP testing and does not proceed to discharge.
- `V0024`: This variant ends at Admission NC and does not reach a final discharge pathway in this sequence.
- `V0025`: This variant terminates at IV Antibiotics without proceeding to discharge.
- `V0027`: The variant ends at IV Antibiotics without reaching any discharge pathway.
- `V0029`: The variant ends prematurely at Leucocytes without reaching a discharge pathway.
- `V0031`: The variant ends at LacticAcid without any discharge activity.
- `V0034`: The variant terminates at IV Liquid and does not reach a discharge category.
- `V0036`: The variant terminates at CRP without reaching a discharge pathway.
- `V0038`: The variant ends at IV Antibiotics without reaching a discharge pathway.
- `V0040`: The variant terminates at Admission NC without reaching a discharge pathway.
- `V0043`: The variant ends at LacticAcid without reaching a discharge pathway.
- `V0050`: The variant ends at CRP without reaching a discharge pathway.
- `V0056`: The narrative ends at IV Antibiotics and does not reach any release pathway.
- `V0062`: The process terminates at IV Antibiotics without reaching a release category.
- `V0081`: The process ends with IV Liquid and does not reach any discharge category.
- `V0088`: The variant terminates at IV Antibiotics without reaching a discharge pathway.
- `V0092`: The process ends with LacticAcid and does not result in any discharge pathway.
- `V0111`: The narrative ends in Admission NC without any discharge event, thus not fitting any release category.
- `V0127`: The variant ends with LacticAcid and does not reach a discharge pathway category.
- `V0132`: The variant ends at IV Antibiotics and does not reach any discharge category.
- `V0133`: The narrative terminates at IV Antibiotics without reaching a discharge pathway.
- `V0137`: The variant ends with LacticAcid and does not reach a discharge pathway.
- `V0146`: The variant ends with Leucocytes and does not reach a discharge pathway.
- `V0148`: The narrative ends at IV Antibiotics without reaching any release category.
- `V0181`: The narrative concludes with Leucocytes and does not culminate in a standard discharge category.
- `V0187`: The narrative is incomplete, ending in CRP during the early ER phase.
- `V0197`: The narrative terminates early at Leucocytes without reaching a recognized discharge category.
- `V0217`: The narrative terminates with IV Antibiotics rather than any discharge pathway.
- `V0219`: The narrative ends with Leucocytes and lacks a discharge event.
- `V0232`: The narrative ends with IV Antibiotics without reaching any discharge pathway category.
- `V0234`: The narrative terminates at Leucocytes without achieving any release pathway category.
- `V0260`: The variant terminates at IV Antibiotics without reaching any of the defined discharge pathways.
- `V0268`: The variant terminates at Leucocytes and does not reach any specified discharge pathway.
- `V0287`: The variant terminates at CRP without reaching any discharge pathway category.
- `V0292`: The variant stops at Leucocytes without reaching a discharge category.
- `V0295`: The sequence ends at IV Antibiotics prior to any discharge pathway.
- `V0302`: The process terminates at ER Sepsis Triage and does not reach a discharge pathway category.
- `V0305`: The process terminates at IV Antibiotics and does not reach a discharge pathway category.
- `V0309`: The narrative ends with Admission NC and includes an interim Release B event, but does not realize the complete discharge category outcome.
- `V0322`: The process terminates at IV Antibiotics and does not reach a discharge pathway category.
- `V0325`: The process terminates at IV Antibiotics and does not reach a discharge pathway category.
- `V0330`: The outcome is IV Liquid, which does not correspond to any of the defined release pathways.
- `V0336`: The outcome is CRP, which does not match any discharge pathway category.
- `V0342`: The outcome is CRP, which does not correspond to any discharge pathway.
- `V0349`: The outcome is ER Sepsis Triage, which does not match any release pathway.
- `V0365`: The outcome is Leucocytes rather than any recognized discharge pathway.
- `V0368`: The outcome is Admission NC, which does not match any discharge category.
- `V0374`: The outcome is Leucocytes, which does not fit any of the release pathways.
- `V0378`: The narrative ends with IV Antibiotics rather than any of the specified release pathways.
- `V0379`: The narrative ends with IV Antibiotics and does not reach a recognized discharge pathway category.
- `V0382`: The final outcome is Return ER following an interim Release A, which does not fit a standard successful release pathway category.
- `V0385`: The narrative terminates with Return ER after Release A, so it does not realize a clean category.
- `V0386`: The outcome ends with Return ER after an interim Release A.
- `V0398`: The narrative terminates with Return ER.
- `V0415`: The narrative ends at Admission NC without reaching any of the defined release pathways.
- `V0417`: The narrative ends in ER Triage and does not complete any discharge pathway.
- `V0427`: The patient ends with Return ER after Release C, which does not map cleanly to standard outcomes.
- `V0429`: The narrative terminates at IV Antibiotics rather than a release category.
- `V0435`: The pathway concludes with Return ER after Release A, making it an unmapped residual case.
- `V0437`: The trajectory ends in Return ER following Release D.
- `V0440`: The process variant ends with Return ER after Release A.
- `V0441`: The narrative involves a return to ER after Release A.
- `V0442`: The narrative includes a return to ER following Release A.
- `V0443`: The process terminates with Return ER after Release A.
- `V0447`: The pathway results in Return ER after Release C.
- `V0448`: The case ends with Return ER following Release A.
- `V0449`: The narrative terminates with Return ER after Release A.
- `V0462`: The narrative does not culminate in a recognized release pathway, ending instead with CRP.
- `V0488`: The narrative ends with IV Liquid and does not reach any discharge pathway category.
- `V0492`: The narrative ends with IV Liquid and does not reach any discharge pathway category.
- `V0495`: The narrative ends with IV Antibiotics and does not reach any discharge pathway category.
- `V0501`: The narrative terminates at IV Liquid and does not reach any designated discharge pathway or final outcome category in the taxonomy.
- `V0502`: The variant ends with Admission NC and does not complete a discharge pathway.
- `V0507`: The trace stops at IV Antibiotics without reaching a discharge pathway.
- `V0510`: The trace concludes at IV Antibiotics and does not realize any discharge categories.
- `V0516`: The narrative ends with Leucocytes and does not represent a valid discharge pathway.
- `V0517`: The trace ends abruptly at ER Triage without reaching any discharge event.
- `V0549`: The process variant ends with IV Liquid and does not reach any of the specified release pathways.
- `V0556`: The narrative results in a Return ER outcome, which does not map to any standard release pathway category.
- `V0558`: The narrative ends with a Return ER outcome, failing to fit any release pathway category.
- `V0559`: The outcome is Return ER, so it does not fit the target release categories.
- `V0560`: The narrative results in Return ER, which is outside the release pathway categories.
- `V0564`: The narrative ends with a Return ER outcome rather than a completed release category.
- `V0565`: The outcome is Admission NC, which is not a release category.
- `V0567`: The narrative results in a Return ER outcome, not fitting any release pathway category.
- `V0573`: The outcome is Return ER, which does not fall under any of the release pathway categories.
- `V0575`: The narrative outcome is Leucocytes, which does not match any discharge release category.
- `V0580`: The narrative does not conclude with any discharge pathway, ending in CRP instead.
- `V0584`: The outcome is IV Liquid, which does not correspond to any discharge pathway category.
- `V0585`: The outcome is LacticAcid, which is not a discharge pathway category.
- `V0587`: The outcome is CRP, failing to reach any recognized discharge pathway.
- `V0592`: The outcome is IV Antibiotics, which does not match any discharge pathway.
- `V0636`: The narrative ends with LacticAcid instead of a recognized discharge pathway, so it does not fit any release category.
- `V0644`: The narrative terminates with CRP instead of a discharge event, so it does not fit any release category.
- `V0645`: The narrative concludes with LacticAcid rather than a discharge pathway.
- `V0646`: The trajectory terminates with LacticAcid after an interim Release A and return to ER, not matching a coherent primary release category.
- `V0654`: The narrative ends with Leucocytes and does not reach any of the release pathways.
- `V0663`: The narrative terminates at Admission NC without reaching any release pathway.
- `V0664`: The narrative terminates at IV Liquid without reaching any release pathway.
- `V0676`: The narrative ends with IV Antibiotics and does not reach a discharge pathway.
- `V0679`: The narrative ends with IV Antibiotics and does not reach a discharge pathway.
- `V0685`: The narrative ends with IV Antibiotics and does not reach a discharge pathway.
- `V0689`: The narrative ends with IV Antibiotics and does not reach a discharge pathway.
- `V0694`: The narrative ends at ER Sepsis Triage and does not reach a discharge pathway.
- `V0703`: The narrative ends with IV Liquid and does not reach any discharge category.
- `V0707`: The narrative ends with Admission NC and does not reach a discharge pathway.
- `V0708`: The narrative terminates at IV Antibiotics without reaching any discharge category.
- `V0713`: The narrative terminates at IV Antibiotics and does not reach a discharge pathway.
- `V0742`: The narrative does not conclude with a recognized release pathway, ending instead with LacticAcid.
- `V0750`: The narrative ends prematurely with IV Antibiotics and does not reach any designated release pathway.
- `V0759`: The process terminates at IV Antibiotics without reaching any discharge pathway.
- `V0764`: The process terminates at ER Sepsis Triage and does not involve an inpatient admission or release.
- `V0772`: The process ends at CRP testing and does not progress to any release category.
- `V0774`: The process terminates early at ER Sepsis Triage without reaching any discharge pathway.
- `V0775`: The process concludes at CRP testing without an admission or release pathway.
- `V0777`: The narrative does not conclude with a discharge pathway, ending instead with Leucocytes.
- `V0778`: The narrative does not culminate in any of the recognized release pathways.
- `V0791`: The process terminates at IV Antibiotics without reaching a release category.
- `V0804`: Although it features Release A earlier, the final outcome is a return to the ER, making the standard discharge category inapplicable as the final pathway.
- `V0806`: The narrative ends with a return to the ER rather than a completed discharge pathway.
- `V0808`: The patient ultimately returns to the ER after initial release, placing it outside a successful final discharge pathway category.
- `V0812`: The narrative ends in a return to the ER following a brief release.
- `V0815`: The final outcome is a return to the ER rather than completion of a discharge category.
- `V0816`: The process terminates at IV Antibiotics without reaching a discharge pathway.
- `V0817`: Although Release C is mentioned, the final outcome is a return to the ER.
- `V0820`: The process terminates at LacticAcid without completing any discharge pathway.
- `V0821`: The final outcome is a return to the ER.
- `V0822`: The final outcome is a return to the ER.
- `V0823`: The final outcome is a return to the ER.
- `V0825`: The final outcome is a return to the ER.
- `V0826`: The narrative terminates at Admission NC without reaching any specific discharge pathway.
- `V0832`: The narrative ends with IV Antibiotics, which is an in-treatment step rather than a discharge pathway.
- `V0843`: The narrative terminates at IV Liquid and does not reach a discharge pathway.
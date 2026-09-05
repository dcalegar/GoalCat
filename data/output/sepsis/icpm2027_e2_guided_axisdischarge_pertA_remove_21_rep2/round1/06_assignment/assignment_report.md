# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_axisdischarge_pertA_remove_21_rep2` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Release A (`release_a`)

Discharge via Release A pathway, advancing the softgoal to avoid post-discharge deterioration and measured against post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative Release A (id=17) under goal-model element 6, observed in variants such as V0008 and V0070.

**Goal-model linkage:** 17 (Task): Release A

**Coverage:** macro 606/846 variants (71.6%) · micro 650/1050 cases (61.9%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.45, nearest other category `release_b` at mean distance 15.17

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.350, nearest other category `release_d` at mean distance 0.441

## Release B (`release_b`)

Discharge via Release B pathway, contributing to the softgoal of avoiding post-discharge deterioration and evaluated using post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative Release B (id=18) under goal-model element 6, evidenced in variants like V0068 and V0145.

**Goal-model linkage:** 18 (Task): Release B

**Coverage:** macro 54/846 variants (6.4%) · micro 55/1050 cases (5.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 16.68, nearest other category `release_a` at mean distance 15.17

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.230, nearest other category `release_d` at mean distance 0.541

## Release C (`release_c`)

Discharge via Release C pathway, aligned with avoiding post-discharge deterioration and tracked by post-discharge ER return indicators.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative Release C (id=19) under goal-model element 6, as seen in variant V0710.

**Goal-model linkage:** 19 (Task): Release C

**Coverage:** macro 25/846 variants (3.0%) · micro 25/1050 cases (2.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 22.70, nearest other category `release_a` at mean distance 18.14

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.268, nearest other category `release_d` at mean distance 0.433

## Release D (`release_d`)

Discharge via Release D pathway, supporting the softgoal to avoid post-discharge deterioration against the post-discharge ER return indicator.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative Release D (id=20) under goal-model element 6, realized in variant V0273.

**Goal-model linkage:** 20 (Task): Release D

**Coverage:** macro 24/846 variants (2.8%) · micro 24/1050 cases (2.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 19.12, nearest other category `release_a` at mean distance 17.08

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

137/846 variants (16.2%), 296/1050 cases (28.2%) unassigned.

- `V0001`: The narrative ends at ER Sepsis Triage and does not reach any discharge pathway.
- `V0002`: The narrative terminates at CRP testing and does not contain a discharge event.
- `V0003`: The narrative ends at Leucocytes and does not include any discharge activity.
- `V0004`: The process terminates at IV Antibiotics administration without reaching a discharge pathway.
- `V0005`: The trace ends at LacticAcid and lacks a discharge activity.
- `V0006`: The narrative finishes at IV Antibiotics without any subsequent discharge events.
- `V0007`: The narrative ends at IV Antibiotics and does not progress to discharge.
- `V0009`: The trace stops at IV Antibiotics without reaching a discharge event.
- `V0010`: The narrative terminates at ER Sepsis Triage and does not include a discharge.
- `V0011`: The sequence ends at IV Antibiotics without proceeding to discharge.
- `V0012`: The narrative finishes at IV Antibiotics and does not reach a discharge pathway.
- `V0013`: The trace stops at Leucocytes without any discharge events.
- `V0017`: The trace ends at ER Sepsis Triage without reaching any discharge pathway.
- `V0019`: The narrative ends at IV Antibiotics without any discharge outcome.
- `V0020`: The trace terminates at CRP and lacks a discharge activity.
- `V0021`: Although Release A occurs intermediately, the final outcome is Return ER, which does not map to any of the release categories.
- `V0023`: Although Release A is present in the trace, the final outcome is Return ER, which falls outside the release categories.
- `V0024`: The narrative terminates at Admission NC without reaching a discharge pathway.
- `V0025`: The trace ends at IV Antibiotics without a discharge event.
- `V0027`: The variant ends with IV Antibiotics and does not reach any discharge pathway.
- `V0029`: The process terminates at Leucocytes without any discharge event.
- `V0031`: The process stops at LacticAcid without reaching a discharge destination.
- `V0034`: The variant stops at IV Liquid without reaching a release activity.
- `V0036`: The narrative terminates at CRP and lacks a discharge milestone.
- `V0038`: The process ends at IV Antibiotics without any release step.
- `V0040`: The sequence terminates at Admission NC without discharge.
- `V0043`: The process ends at LacticAcid without a discharge outcome.
- `V0050`: The process ends at CRP without reaching any release category.
- `V0056`: The outcome is IV Antibiotics rather than any discharge pathway.
- `V0062`: The outcome is IV Antibiotics rather than any discharge pathway.
- `V0081`: The narrative ends with IV Liquid and does not reach any discharge pathway category.
- `V0088`: The narrative ends with IV Antibiotics and does not reach any discharge pathway category.
- `V0092`: The narrative ends with LacticAcid and does not reach any discharge pathway category.
- `V0111`: The narrative ends with Admission NC and does not reach any discharge pathway category.
- `V0127`: The variant ends with LacticAcid and does not complete any discharge pathway.
- `V0132`: The variant ends with IV Antibiotics and does not reach any discharge event.
- `V0133`: The variant finishes at IV Antibiotics without executing a discharge pathway.
- `V0137`: The variant ends with LacticAcid and lacks any discharge pathway.
- `V0146`: The variant ends with Leucocytes and does not reach a discharge destination.
- `V0148`: The variant stops at IV Antibiotics without completing a discharge event.
- `V0181`: The narrative terminates at Leucocytes and does not result in a discharge pathway.
- `V0187`: The narrative terminates at CRP and does not result in a discharge pathway.
- `V0196`: The narrative results in Release E, which does not match any of the specified release categories.
- `V0197`: The narrative terminates at Leucocytes and does not result in a discharge pathway.
- `V0217`: The process variant terminates with IV Antibiotics rather than any discharge category.
- `V0219`: The process variant terminates with Leucocytes and does not reach a discharge category.
- `V0232`: The process variant terminates at IV Antibiotics without reaching any discharge pathway.
- `V0234`: The process variant terminates at Leucocytes without reaching any discharge pathway.
- `V0260`: The process terminates at IV Antibiotics without reaching any final release pathway.
- `V0268`: The sequence ends at Leucocytes without achieving any release pathway.
- `V0287`: The process terminates at CRP and does not complete any discharge pathway.
- `V0292`: The process terminates at Leucocytes and does not complete any discharge pathway.
- `V0295`: The narrative terminates at IV Antibiotics and does not reach a discharge endpoint.
- `V0302`: The process terminates at ER Sepsis Triage and does not reach a discharge pathway category.
- `V0305`: The process ends at IV Antibiotics inside the emergency phase and does not reach a discharge category.
- `V0309`: The variant features Release B followed by Admission NC, but does not realize the specific Release B category criteria since it continues past release activities or isn't a final terminal pathway matching the exact discharge definition.
- `V0316`: The narrative outcome is Release E, which is not part of the taxonomy.
- `V0322`: The process ends at IV Antibiotics and does not reach a discharge category.
- `V0325`: The variant ends at IV Antibiotics without reaching any discharge pathway.
- `V0327`: The narrative ends with Return ER rather than a recognized release pathway.
- `V0328`: The narrative ends with Return ER after Release A, so it does not fit standard discharge pathways.
- `V0330`: The outcome is IV Liquid, which does not match any release pathway.
- `V0335`: The narrative ends with Return ER after a Release A event.
- `V0336`: The outcome is CRP, which is not a discharge pathway.
- `V0339`: The outcome is Return ER following Release A.
- `V0342`: The outcome is CRP, not a release category.
- `V0346`: The narrative ends with Return ER following Release A.
- `V0348`: The narrative results in a Return ER after Release A.
- `V0349`: The outcome is ER Sepsis Triage, which does not correspond to a discharge category.
- `V0350`: The narrative terminates in Return ER after Release A.
- `V0365`: The process variant does not reach any release pathway, ending instead with Leucocytes.
- `V0368`: The process variant terminates at Admission NC without completing a discharge pathway.
- `V0374`: The process variant ends with Leucocytes and does not reach a release outcome.
- `V0378`: The narrative ends with IV Antibiotics and does not reach any discharge pathway.
- `V0379`: The narrative ends with IV Antibiotics and does not reach any discharge pathway.
- `V0415`: The variant outcome is Admission NC without any release event, so it does not fit any release category.
- `V0417`: The variant outcome is ER Triage without any release event, so it does not fit any release category.
- `V0429`: The narrative outcome is IV Antibiotics, which does not match any discharge release category.
- `V0462`: The narrative does not culminate in any release category, ending instead with CRP.
- `V0488`: The process terminates at IV Liquid without reaching any release pathway.
- `V0492`: The case terminates at IV Liquid before any discharge category is achieved.
- `V0495`: The trace ends at IV Antibiotics without a release activity.
- `V0501`: The narrative ends with IV Liquid and does not reach any discharge pathway corresponding to the release categories.
- `V0502`: The narrative ends with Admission NC and does not reach a discharge category.
- `V0507`: The narrative terminates at IV Antibiotics and does not reach a discharge pathway.
- `V0510`: The narrative ends with IV Antibiotics and does not reach any release category.
- `V0516`: The narrative ends with Leucocytes and does not reach any release pathway.
- `V0517`: The narrative terminates at ER Triage and does not reach a release category.
- `V0549`: The narrative does not conclude with any of the release pathways, ending with IV Liquid instead.
- `V0553`: The narrative outcome is Release E, which does not match any of the defined release categories A through D.
- `V0565`: The narrative outcome is Admission NC, which does not match any of the release pathways.
- `V0575`: The narrative outcome is Leucocytes, which does not match any of the defined release categories.
- `V0580`: The outcome is CRP and does not involve any of the discharge pathways (Release A, B, C, or D).
- `V0584`: The process terminates at IV Liquid without reaching a discharge or release pathway.
- `V0585`: The process finishes at LacticAcid, lacking any release event.
- `V0587`: The variant ends at CRP without any release pathway.
- `V0592`: The trace stops at IV Antibiotics and contains no release activity.
- `V0598`: The narrative ends with Release E, which is outside the defined release_a through release_d taxonomy.
- `V0603`: The narrative ends with Release E, which does not match any of the four defined release categories.
- `V0629`: The narrative ends with Release E, which does not map to Release A, B, C, or D.
- `V0636`: The narrative ends with LacticAcid instead of any recognized release pathway.
- `V0644`: The narrative ends with CRP instead of any recognized release pathway.
- `V0645`: The narrative ends with LacticAcid instead of any recognized release pathway.
- `V0654`: The outcome is Leucocytes rather than any of the release pathways.
- `V0663`: The process ends with Admission NC and does not reach any discharge category.
- `V0664`: The sequence stops at IV Liquid without reaching a discharge pathway.
- `V0670`: Although Release A is visited, the final outcome is Leucocytes following an ER return.
- `V0676`: The process ends at IV Antibiotics and does not reach any discharge pathway.
- `V0679`: The process terminates at IV Antibiotics without reaching a discharge activity.
- `V0685`: The variant ends at IV Antibiotics without a discharge event.
- `V0689`: The case ends with IV Antibiotics and does not reach a discharge activity.
- `V0694`: The process ends at ER Sepsis Triage and does not reach a discharge state.
- `V0703`: The narrative outcome is IV Liquid, which does not correspond to any of the discharge release pathways.
- `V0707`: The narrative outcome is Admission NC, which is not a discharge release pathway.
- `V0708`: The narrative outcome is IV Antibiotics, which is not a discharge release pathway.
- `V0713`: The narrative outcome is IV Antibiotics, which does not correspond to a discharge pathway.
- `V0742`: The narrative terminates with LacticAcid and does not execute any release pathway.
- `V0750`: The narrative ends with 'IV Antibiotics' and does not reach a discharge or release category.
- `V0759`: The process terminates at IV Antibiotics without reaching any discharge outcome.
- `V0764`: The trace stops at ER Sepsis Triage, meaning no release pathway was realized.
- `V0772`: The process ends at CRP without reaching a discharge destination.
- `V0774`: The trace halts at ER Sepsis Triage without progressing to any release.
- `V0775`: The trace terminates at CRP, missing any discharge milestone.
- `V0777`: The narrative does not culminate in any release activity, thus it does not realize any of the release categories.
- `V0778`: The outcome is Leucocytes, not a discharge or release event corresponding to any taxonomy category.
- `V0779`: Although it passes through Release A, the final outcome is Return ER, meaning it does not cleanly fit the terminal pathway definition.
- `V0785`: The pathway results in a Return ER outcome after Release A, so it does not realize the standard discharge category cleanly.
- `V0787`: The process ends with Return ER after Release A, failing to align as a standard release outcome.
- `V0791`: The outcome is IV Antibiotics, which is not a release category.
- `V0794`: The process leads to Return ER after an intermediate Release A, falling outside the target discharge categories.
- `V0797`: The variant results in Return ER following Release A, meaning it does not fit the category.
- `V0798`: The process terminates with Return ER, disqualifying it from the release categories.
- `V0816`: The narrative ends with 'IV Antibiotics' and does not reach any discharge pathway category.
- `V0820`: The narrative ends with 'LacticAcid' and does not reach any discharge pathway category.
- `V0826`: The narrative ends with Admission NC and does not feature any discharge pathway mapped in the taxonomy.
- `V0832`: The narrative terminates at IV Antibiotics without reaching any discharge activity.
- `V0843`: The narrative ends with IV Liquid and does not reach a recognized discharge pathway.
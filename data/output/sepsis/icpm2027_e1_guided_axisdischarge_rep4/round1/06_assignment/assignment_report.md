# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_axisdischarge_rep4` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Release A (`release_a`)

Represents the standard discharge pathway for patients treated within guideline windows. Advances the softgoal Avoid post-discharge deterioration and is measured against the Post-discharge ER return indicator.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative Release A (id=17) as observed in multiple variants (e.g. V0008, V0070).

**Goal-model linkage:** 17 (Task): Release A

**Coverage:** macro 525/846 variants (62.1%) · micro 569/1050 cases (54.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.43, nearest other category `release_b` at mean distance 15.07

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.331, nearest other category `release_d` at mean distance 0.455

## Release B (`release_b`)

Represents an alternative discharge pathway following extended monitoring. Advances the softgoal Avoid post-discharge deterioration and is measured against the Post-discharge ER return indicator.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative Release B (id=18) as observed in variant V0068 and V0145.

**Goal-model linkage:** 18 (Task): Release B

**Coverage:** macro 55/846 variants (6.5%) · micro 56/1050 cases (5.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 16.61, nearest other category `release_a` at mean distance 15.07

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.248, nearest other category `release_d` at mean distance 0.546

## Release C (`release_c`)

Represents a specific discharge pathway for long-stay complex cases. Advances the softgoal Avoid post-discharge deterioration and is measured against the Post-discharge ER return indicator.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative Release C (id=19) as observed in variant V0710.

**Goal-model linkage:** 19 (Task): Release C

**Coverage:** macro 25/846 variants (3.0%) · micro 25/1050 cases (2.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 22.70, nearest other category `release_a` at mean distance 18.14

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.268, nearest other category `release_d` at mean distance 0.433

## Release D (`release_d`)

Represents a specific discharge pathway for extended rework cases. Advances the softgoal Avoid post-discharge deterioration and is measured against the Post-discharge ER return indicator.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative Release D (id=20) as observed in variant V0273.

**Goal-model linkage:** 20 (Task): Release D

**Coverage:** macro 24/846 variants (2.8%) · micro 24/1050 cases (2.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 19.12, nearest other category `release_a` at mean distance 17.10

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.300, nearest other category `release_c` at mean distance 0.433

## Release E (`release_e`)

Represents the alternative discharge pathway E for completed cases. Advances the softgoal Avoid post-discharge deterioration and is measured against the Post-discharge ER return indicator.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative Release E (id=21) per the goal model decomposition axis.

**Goal-model linkage:** 21 (Task): Release E

**Coverage:** macro 6/846 variants (0.7%) · micro 6/1050 cases (0.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 17.67, nearest other category `release_a` at mean distance 16.40

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.253, nearest other category `release_d` at mean distance 0.440

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

211/846 variants (24.9%), 370/1050 cases (35.2%) unassigned.

- `V0001`: This variant ends in ER Sepsis Triage and does not reach any discharge pathway.
- `V0002`: This variant stops at CRP testing without reaching a discharge pathway.
- `V0003`: This variant terminates at Leucocytes testing before any discharge activity occurs.
- `V0004`: This variant ends with IV Antibiotics administration and does not include a release step.
- `V0005`: This variant ends at LacticAcid testing without proceeding to admission or discharge.
- `V0006`: This variant ends with IV Antibiotics and does not reach a discharge pathway.
- `V0007`: This variant concludes with IV Antibiotics and lacks a discharge milestone.
- `V0009`: This variant terminates at IV Antibiotics without any subsequent discharge.
- `V0010`: This variant ends in ER Sepsis Triage and does not represent a discharge pathway.
- `V0011`: This variant ends at IV Antibiotics and does not reach a release milestone.
- `V0012`: This variant finishes with IV Antibiotics without reaching a discharge pathway.
- `V0013`: This variant ends at Leucocytes testing and does not include admission or discharge.
- `V0017`: This variant terminates at ER Sepsis Triage without reaching a discharge milestone.
- `V0019`: This variant ends with IV Antibiotics and does not feature a discharge event.
- `V0020`: This variant ends at CRP without progressing to discharge.
- `V0024`: This variant stops at Admission NC without completing a discharge path.
- `V0025`: This variant terminates at IV Antibiotics without a discharge step.
- `V0027`: This variant ends with IV Antibiotics and does not reach discharge.
- `V0029`: This variant ends at Leucocytes testing without reaching any release pathway.
- `V0031`: This variant stops at LacticAcid without progressing to hospital admission or discharge.
- `V0034`: This variant concludes with IV Liquid administration and lacks a discharge milestone.
- `V0036`: This variant ends at CRP without reaching a discharge event.
- `V0038`: This variant ends with IV Antibiotics without any release event.
- `V0040`: This variant ends at Admission NC and does not reach a discharge pathway.
- `V0043`: This variant terminates at LacticAcid testing without reaching admission or release.
- `V0050`: This variant terminates at CRP testing and does not reach any discharge pathway.
- `V0052`: Outcome is Return ER, which does not match any of the standard release categories.
- `V0054`: Outcome is Return ER, falling outside the defined release pathways.
- `V0055`: Outcome is Return ER, which does not fit any release category.
- `V0056`: Outcome is IV Antibiotics, lacking a final discharge outcome.
- `V0060`: Outcome is Return ER, not matching any successful release category.
- `V0062`: Outcome is IV Antibiotics, which is not a discharge category.
- `V0071`: Outcome is Return ER, which does not map to any release category.
- `V0072`: Outcome is Return ER, not matching any successful discharge category.
- `V0074`: Outcome is Return ER, which is outside the release categories.
- `V0075`: Outcome is Return ER, which does not fit any release category.
- `V0078`: Outcome is Return ER, failing to match any release category.
- `V0080`: Outcome is Return ER, not a matching discharge category.
- `V0081`: Outcome is IV Liquid, which is not a discharge pathway.
- `V0083`: Outcome is Return ER, which does not fit any release category.
- `V0085`: Outcome is Return ER, failing to match any release category.
- `V0088`: Outcome is IV Antibiotics, which is not a discharge pathway.
- `V0089`: Outcome is Return ER, which does not match any release category.
- `V0092`: Outcome is LacticAcid, which is not a discharge category.
- `V0094`: Outcome is Return ER, failing to match any release category.
- `V0098`: Outcome is Return ER, which does not fit any release category.
- `V0111`: The process terminates at Admission NC without reaching any of the specified release categories.
- `V0127`: The process terminates at LacticAcid without reaching any of the specified release categories.
- `V0132`: The process terminates at IV Antibiotics without reaching any of the specified release categories.
- `V0133`: The process terminates at IV Antibiotics without reaching any of the specified release categories.
- `V0137`: The process terminates at LacticAcid without reaching any of the specified release categories.
- `V0146`: The process terminates at Leucocytes without reaching any of the specified release categories.
- `V0148`: The process terminates at IV Antibiotics without reaching any of the specified release categories.
- `V0187`: Incomplete case lacking any discharge or release activity.
- `V0197`: Incomplete case missing a formal release or discharge outcome.
- `V0217`: The variant terminates at IV Antibiotics without reaching any of the defined discharge outcomes.
- `V0219`: The variant terminates at Leucocytes without reaching any of the defined discharge outcomes.
- `V0232`: The variant terminates at IV Antibiotics without reaching any of the defined discharge outcomes.
- `V0234`: The variant terminates at Leucocytes without reaching any of the defined discharge outcomes.
- `V0260`: The process terminates at IV Antibiotics without reaching any discharge pathway.
- `V0268`: The process terminates at Leucocytes without reaching any discharge pathway.
- `V0287`: The process terminates at CRP without reaching any discharge pathway.
- `V0292`: The process terminates at Leucocytes without reaching any discharge pathway.
- `V0295`: The process terminates at IV Antibiotics without reaching any discharge pathway.
- `V0302`: The process terminates at ER Sepsis Triage and does not complete a discharge pathway.
- `V0305`: The process ends at IV Antibiotics without reaching any discharge pathway.
- `V0322`: The case ends at IV Antibiotics without reaching discharge.
- `V0325`: The case stops at IV Antibiotics.
- `V0330`: The narrative terminates at IV Liquid without reaching a discharge category.
- `V0336`: The process terminates at CRP and does not reach any discharge activity.
- `V0342`: The case ends at CRP without reaching a discharge point.
- `V0349`: The case terminates at ER Sepsis Triage without discharge.
- `V0352`: The outcome is Return ER, and the variant shows repeated admissions and lab work, falling outside standard guideline release pathways.
- `V0353`: The narrative ends in Return ER following extended checks, which does not map to any standard release category.
- `V0357`: The narrative ends in Return ER after multiple monitoring cycles and rework.
- `V0358`: The process terminates with Return ER, failing to fit any successful release category.
- `V0359`: The outcome is Return ER following prolonged post-discharge readmission, not aligning with structured discharge categories.
- `V0364`: The case ends with Return ER, which is not part of the valid release pathways.
- `V0365`: The outcome is Leucocytes rather than a discharge pathway, representing an incomplete or ongoing path.
- `V0366`: The narrative ends in Return ER, making it part of the residual rather than standard release categories.
- `V0367`: The extensive rework and final Return ER outcome place this variant in the residual.
- `V0368`: The process stops at Admission NC, representing an incomplete pathway without a final release event.
- `V0369`: The narrative terminates with Return ER after multiple rework iterations.
- `V0370`: The case results in Return ER, falling outside the defined successful discharge categories.
- `V0374`: The trace stops at Leucocytes without achieving a terminal release outcome.
- `V0378`: The process ends at IV Antibiotics without reaching a discharge destination.
- `V0379`: The trace terminates at IV Antibiotics, lacking a final discharge event.
- `V0382`: The variant ends in Return ER after multiple admission and test cycles.
- `V0385`: The case ends in Return ER following heavy rework, falling outside standard release categories.
- `V0386`: The outcome is Return ER, which does not match any valid release category.
- `V0398`: The outcome is Return ER following prolonged loops and rework.
- `V0415`: The outcome is Admission NC without any discharge event, so it does not fit any of the release categories.
- `V0417`: The narrative ends at ER Triage without reaching any discharge pathway, leaving it in the residual.
- `V0429`: The narrative ends at IV Antibiotics without reaching a discharge pathway, placing it in the residual.
- `V0453`: The variant outcome is Return ER, and none of the release discharge pathways fit the residual trajectory.
- `V0454`: The variant outcome is Return ER, outside standard successful completion pathways.
- `V0458`: The variant outcome is Return ER.
- `V0460`: The variant outcome is Return ER.
- `V0462`: Outcome is CRP, which does not match any of the standard discharge categories.
- `V0463`: The variant outcome is Return ER.
- `V0464`: The variant outcome is Return ER.
- `V0467`: The variant outcome is Return ER.
- `V0468`: The variant outcome is Return ER.
- `V0469`: The variant outcome is Return ER.
- `V0473`: The variant outcome is Return ER.
- `V0474`: The variant outcome is Return ER.
- `V0476`: The variant outcome is Return ER.
- `V0479`: The variant outcome is Return ER.
- `V0482`: The variant outcome is Return ER.
- `V0484`: The variant outcome is Return ER.
- `V0488`: Outcome is IV Liquid, not a discharge category.
- `V0492`: Outcome is IV Liquid, not a discharge category.
- `V0495`: Outcome is IV Antibiotics, not a discharge category.
- `V0497`: The variant outcome is Return ER.
- `V0501`: The narrative ends with IV Liquid and does not reach any discharge pathway.
- `V0502`: The narrative ends with Admission NC and does not reach any discharge pathway.
- `V0504`: The narrative ends with Return ER after Release A, representing a post-discharge readmission rather than a successful standard pathway.
- `V0505`: The narrative ends with Return ER after Release A, indicating a readmission.
- `V0507`: The narrative ends with IV Antibiotics and does not reach discharge.
- `V0508`: The narrative ends with Return ER after Release A.
- `V0510`: The narrative ends with IV Antibiotics.
- `V0515`: The narrative ends with Return ER.
- `V0516`: The narrative ends with Leucocytes.
- `V0517`: The narrative ends with ER Triage.
- `V0519`: The narrative ends with Return ER.
- `V0520`: The narrative ends with Return ER.
- `V0526`: The narrative ends with Return ER.
- `V0528`: The narrative ends with Return ER.
- `V0529`: The narrative ends with Return ER.
- `V0530`: The narrative ends with Return ER.
- `V0531`: The narrative ends with Return ER.
- `V0535`: The narrative ends with Return ER.
- `V0539`: The narrative ends with Return ER.
- `V0543`: The narrative ends with Return ER.
- `V0546`: The narrative ends with Return ER.
- `V0549`: The narrative ends with IV Liquid.
- `V0556`: The narrative ends with Return ER, which does not correspond to any of the designated release categories.
- `V0558`: The narrative ends with Return ER, falling outside the release categories.
- `V0559`: The narrative ends with Return ER, which is outside the scope of release pathways.
- `V0560`: The narrative ends with Return ER, so no release category applies.
- `V0564`: The narrative ends with Return ER, thus no release category fits.
- `V0565`: The narrative terminates at Admission NC without reaching any release outcome.
- `V0567`: The narrative ends with Return ER, which does not match any release category.
- `V0573`: The narrative ends with Return ER, making it part of the residual.
- `V0575`: The narrative terminates at Leucocytes without reaching a release outcome.
- `V0577`: The narrative ends with Return ER, falling into the residual.
- `V0578`: The narrative ends with Return ER, no release category matches.
- `V0579`: The narrative ends with Return ER, outside of the release taxonomy.
- `V0580`: The narrative terminates at CRP without reaching any release outcome.
- `V0584`: The narrative terminates at IV Liquid without reaching a release outcome.
- `V0585`: The narrative terminates at LacticAcid without reaching a release outcome.
- `V0587`: The narrative terminates at CRP without reaching a release outcome.
- `V0590`: The narrative ends with Return ER, not fitting any release category.
- `V0591`: The narrative ends with Return ER, falling into the residual.
- `V0592`: The narrative terminates at IV Antibiotics without reaching a release outcome.
- `V0595`: The narrative ends with Return ER, outside of the release categories.
- `V0636`: The narrative ends with LacticAcid instead of a recognized release activity, meaning it falls into the residual category.
- `V0644`: The narrative ends with CRP instead of a recognized release activity, meaning it falls into the residual category.
- `V0645`: The narrative ends with LacticAcid instead of a recognized release activity, meaning it falls into the residual category.
- `V0654`: The narrative does not reach any discharge or release activity, ending at Leucocytes.
- `V0663`: The narrative terminates at Admission NC and does not reach a release category.
- `V0664`: The narrative terminates at IV Liquid and does not reach a release category.
- `V0676`: The narrative terminates at IV Antibiotics and does not reach a release category.
- `V0679`: The narrative terminates at IV Antibiotics and does not reach a release category.
- `V0685`: The narrative terminates at IV Antibiotics and does not reach a release category.
- `V0689`: The narrative terminates at IV Antibiotics and does not reach a release category.
- `V0694`: The narrative terminates at ER Sepsis Triage and does not reach a release category.
- `V0703`: The narrative terminates with IV Liquid and does not reach any discharge pathway category.
- `V0705`: The narrative ends with Return ER, which indicates an ER return rather than a successful standard or alternative release pathway.
- `V0707`: The narrative terminates with Admission NC and does not reach a discharge category.
- `V0708`: The narrative terminates with IV Antibiotics and does not reach a release category.
- `V0712`: The narrative ends with Return ER, indicating a post-discharge ER return after Release A.
- `V0713`: The narrative terminates with IV Antibiotics and does not reach a discharge category.
- `V0719`: The narrative ends with Return ER following Release A, representing a post-discharge ER return.
- `V0720`: The narrative ends with Return ER following Release A.
- `V0721`: The narrative ends with Return ER following Release A.
- `V0724`: The narrative ends with Return ER following Release A.
- `V0727`: The narrative ends with Return ER following Release A.
- `V0734`: The narrative ends with Return ER following Release A.
- `V0742`: The narrative terminates with LacticAcid and does not reach a discharge category.
- `V0744`: The narrative ends with Return ER following Release A.
- `V0745`: The narrative ends with Return ER following Release A.
- `V0746`: The narrative ends with Return ER following Release A.
- `V0748`: The narrative ends with Return ER following Release A.
- `V0750`: The narrative terminates with IV Antibiotics and does not reach a discharge category.
- `V0759`: The narrative terminates at IV Antibiotics without reaching any discharge pathway.
- `V0764`: The narrative terminates at ER Sepsis Triage without reaching any discharge pathway.
- `V0772`: The narrative terminates at CRP without reaching any discharge pathway.
- `V0774`: The narrative terminates at ER Sepsis Triage without reaching any discharge pathway.
- `V0775`: The narrative terminates at CRP without reaching any discharge pathway.
- `V0777`: The narrative terminates at Leucocytes without reaching any discharge pathway.
- `V0778`: The narrative terminates at Leucocytes without reaching any discharge pathway.
- `V0791`: The narrative terminates at IV Antibiotics without reaching any discharge pathway.
- `V0804`: The narrative ends with Return ER, which does not fit any of the discharge categories.
- `V0806`: The narrative ends with Return ER, which is outside the specified discharge success categories.
- `V0808`: The narrative ends with Return ER, indicating readmission and failing to realize any successful release category.
- `V0812`: The narrative ends with Return ER, meaning it does not realize a successful release category.
- `V0815`: The narrative ends with Return ER, which does not qualify for any release category.
- `V0816`: The narrative terminates at IV Antibiotics, which is an intermediate treatment step rather than a discharge outcome.
- `V0820`: The narrative terminates at LacticAcid, which is an intermediate diagnostic step.
- `V0821`: The narrative ends with Return ER, indicating readmission.
- `V0822`: The narrative ends with Return ER, indicating readmission.
- `V0823`: The narrative ends with Return ER, indicating readmission.
- `V0825`: The narrative ends with Return ER, indicating readmission.
- `V0826`: The narrative terminates at Admission NC, which is an intermediate hospitalization step.
- `V0827`: The narrative ends with Return ER, indicating readmission.
- `V0828`: The narrative ends with Return ER, indicating readmission.
- `V0832`: The narrative terminates at IV Antibiotics, an intermediate treatment step.
- `V0834`: The narrative ends with Return ER, indicating readmission.
- `V0842`: The narrative ends with Return ER, indicating readmission.
- `V0843`: The narrative terminates at IV Liquid, which is an intermediate care activity.
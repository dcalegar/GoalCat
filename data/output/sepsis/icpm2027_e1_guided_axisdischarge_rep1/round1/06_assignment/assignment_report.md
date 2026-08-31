# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_axisdischarge_rep1` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Release A (`release_a`)

Standard release pathway supporting discharge for admitted patients, contributing to avoiding post-discharge deterioration and measured against post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release A (id=17) as observed in variants like V0008, contributing to avoid post-discharge deterioration softgoal and measured by post-discharge ER return indicator.

**Goal-model linkage:** 17 (Task): Release A

**Coverage:** macro 569/846 variants (67.3%) · micro 617/1050 cases (58.8%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.23, nearest other category `release_b` at mean distance 15.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.341, nearest other category `release_d` at mean distance 0.446

## Release B (`release_b`)

Alternative discharge pathway for admitted patients, contributing to avoiding post-discharge deterioration and measured against post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release B (id=18) as observed in variants like V0068, contributing to avoid post-discharge deterioration softgoal and measured by post-discharge ER return indicator.

**Goal-model linkage:** 18 (Task): Release B

**Coverage:** macro 55/846 variants (6.5%) · micro 56/1050 cases (5.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 16.61, nearest other category `release_a` at mean distance 15.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.248, nearest other category `release_d` at mean distance 0.546

## Release C (`release_c`)

Specific discharge pathway for long-stay admitted patients, measured against post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release C (id=19) as observed in variant V0710, measured against the post-discharge ER return indicator.

**Goal-model linkage:** 19 (Task): Release C

**Coverage:** macro 25/846 variants (3.0%) · micro 25/1050 cases (2.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 22.70, nearest other category `release_a` at mean distance 18.05

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.268, nearest other category `release_d` at mean distance 0.433

## Release D (`release_d`)

Alternative discharge pathway for complex admitted cases, measured against post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release D (id=20) as observed in variant V0273, measured against the post-discharge ER return indicator.

**Goal-model linkage:** 20 (Task): Release D

**Coverage:** macro 24/846 variants (2.8%) · micro 24/1050 cases (2.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 19.12, nearest other category `release_a` at mean distance 17.03

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.300, nearest other category `release_c` at mean distance 0.433

## Release E (`release_e`)

Alternative discharge pathway for specific admitted cases, measured against post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release E (id=21) based on the goal model decomposition, acting as a mutually exclusive discharge option.

**Goal-model linkage:** 21 (Task): Release E

**Coverage:** macro 6/846 variants (0.7%) · micro 6/1050 cases (0.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 17.67, nearest other category `release_a` at mean distance 16.34

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

167/846 variants (19.7%), 322/1050 cases (30.7%) unassigned.

- `V0001`: The narrative ends at ER Sepsis Triage and does not involve any discharge or release pathway.
- `V0002`: The narrative terminates at CRP testing in the ER and does not represent a discharge pathway.
- `V0003`: The process ends at Leucocytes testing and does not lead to a patient release.
- `V0004`: The process ends at IV Antibiotics administration without admission or discharge.
- `V0005`: The sequence concludes with LacticAcid testing in the emergency department.
- `V0006`: The narrative finishes after administering IV Antibiotics in the ER.
- `V0007`: The trace stops at IV Antibiotics without any admission or discharge activity.
- `V0009`: The narrative concludes with IV Antibiotics treatment in the ER.
- `V0010`: The process trace ends at ER Sepsis Triage.
- `V0011`: The sequence terminates at IV Antibiotics without reaching any discharge activity.
- `V0012`: The narrative ends with IV Antibiotics administration in the ER.
- `V0013`: The process stops at Leucocytes testing in the emergency department.
- `V0017`: The sequence terminates at ER Sepsis Triage.
- `V0019`: The narrative ends at IV Antibiotics administration in the ER.
- `V0020`: The process terminates with CRP testing in the ER.
- `V0024`: The narrative stops at Admission NC without showing a release pathway.
- `V0025`: The sequence ends with IV Antibiotics administration in the ER.
- `V0027`: The narrative terminates after IV Antibiotics treatment in the ER.
- `V0029`: The process ends at Leucocytes testing in the emergency department.
- `V0031`: The narrative ends at LacticAcid testing in the ER.
- `V0034`: The process terminates with IV Liquid administration in the ER.
- `V0036`: The narrative finishes at CRP testing in the ER.
- `V0038`: The narrative terminates after IV Antibiotics administration in the ER.
- `V0040`: The sequence ends at Admission NC without an explicit release activity.
- `V0043`: The narrative ends with LacticAcid testing in the ER.
- `V0050`: The narrative concludes with CRP testing in the ER.
- `V0056`: The process ends at IV Antibiotics without reaching any release pathway.
- `V0062`: The process terminates at IV Antibiotics without discharge.
- `V0081`: The process terminates at IV Liquid without reaching a release event.
- `V0088`: The process terminates at IV Antibiotics without reaching any release event.
- `V0092`: The process terminates at LacticAcid without any patient discharge.
- `V0111`: The narrative ends with Admission NC and does not complete a discharge pathway.
- `V0127`: The narrative ends at LacticAcid and does not reach any discharge category.
- `V0132`: The narrative terminates at IV Antibiotics without reaching a discharge destination.
- `V0133`: The narrative terminates at IV Antibiotics without completing a discharge pathway.
- `V0137`: The narrative terminates at LacticAcid without achieving a discharge outcome.
- `V0146`: The narrative terminates at Leucocytes without reaching a discharge status.
- `V0148`: The narrative stops at IV Antibiotics without a completion event matching any discharge category.
- `V0187`: The process ends at CRP without any release activity, thus falling into the residual.
- `V0197`: The process ends at Leucocytes without any release activity, thus falling into the residual.
- `V0217`: The process terminates at IV Antibiotics without reaching any discharge or release activity.
- `V0219`: The process ends prematurely at Leucocytes without reaching any release event.
- `V0232`: The process terminates at IV Antibiotics without any release event.
- `V0234`: The process stops at Leucocytes without reaching a discharge or release state.
- `V0260`: The process terminates at IV Antibiotics and does not reach any discharge category.
- `V0268`: The process stops at Leucocytes and does not culminate in any discharge category.
- `V0287`: The process stops at CRP testing and does not reach any release category.
- `V0292`: The narrative halts at Leucocytes without reaching any discharge pathway.
- `V0295`: The sequence stops at IV Antibiotics without completing a discharge milestone.
- `V0302`: The narrative terminates at ER Sepsis Triage and does not complete any discharge pathway.
- `V0305`: The process terminates at IV Antibiotics without reaching a discharge pathway.
- `V0322`: The process stops at IV Antibiotics without reaching any release category.
- `V0325`: The sequence ends at IV Antibiotics without discharge activities.
- `V0330`: The process ends at IV Liquid and does not reach a discharge category.
- `V0336`: The narrative terminates at CRP without reaching a release activity.
- `V0342`: The sequence stops at CRP without reaching any release pathway.
- `V0349`: The process terminates at ER Sepsis Triage without completing a discharge pathway.
- `V0365`: The outcome is Leucocytes, not culminating in any release category.
- `V0368`: The outcome is Admission NC, therefore it does not realize a release category.
- `V0374`: The process ends with Leucocytes, not a release category.
- `V0378`: The outcome is IV Antibiotics, not a release pathway.
- `V0379`: The outcome is IV Antibiotics, not a release category.
- `V0415`: The narrative terminates at Admission NC without reaching any discharge pathway category.
- `V0417`: The narrative terminates at ER Triage and does not complete a discharge pathway.
- `V0429`: The narrative ends at IV Antibiotics without reaching any discharge pathway category.
- `V0462`: The narrative terminates at CRP and does not reach any discharge activity.
- `V0488`: The narrative ends at IV Liquid and does not reach any discharge activity.
- `V0492`: The narrative terminates at IV Liquid without reaching discharge.
- `V0495`: The narrative ends at IV Antibiotics without reaching a discharge activity.
- `V0501`: The narrative ends with IV Liquid and does not reach a discharge or release outcome.
- `V0502`: The narrative ends with Admission NC and does not reach a release outcome.
- `V0507`: The narrative ends with IV Antibiotics and does not reach any release pathway.
- `V0510`: The narrative ends with IV Antibiotics and does not reach a discharge or release pathway.
- `V0516`: The narrative terminates at Leucocytes without reaching any discharge or release pathway.
- `V0517`: The narrative terminates at ER Triage without reaching a release pathway.
- `V0549`: The narrative ends with IV Liquid and does not reach any release pathway.
- `V0556`: The narrative results in Return ER after an intermediate Release A, not cleanly mapping to a distinct final discharge category variant.
- `V0558`: The narrative ends with Return ER after an intermediate Release A.
- `V0559`: The narrative ends with Return ER following a standard Release A.
- `V0560`: The narrative terminates with Return ER after an intermediate Release A.
- `V0564`: The variant results in Return ER following a Release A.
- `V0565`: The outcome is Admission NC, lacking any final release category.
- `V0567`: The variant ends with Return ER after Release A.
- `V0573`: The narrative ends with Return ER following an intermediate Release A.
- `V0575`: The outcome is Leucocytes, lacking any final release event.
- `V0577`: The narrative ends with Return ER following a Release A.
- `V0578`: The narrative ends with Return ER following a Release A.
- `V0579`: The narrative ends with Return ER following an intermediate Release A.
- `V0580`: The narrative ends at CRP, with no final release event.
- `V0584`: The outcome is IV Liquid, with no final release activity.
- `V0585`: The outcome is LacticAcid, lacking any final release category.
- `V0587`: The outcome is CRP, with no final release event.
- `V0590`: The narrative ends with Return ER after Release A.
- `V0591`: The narrative ends with Return ER after an intermediate Release A.
- `V0592`: The outcome is IV Antibiotics, lacking any final release category.
- `V0595`: The narrative ends with Return ER following a Release A.
- `V0605`: The outcome is Return ER, so it does not realize a standard release pathway category.
- `V0614`: The outcome involves returning to the ER, not fitting any release category.
- `V0625`: The outcome is Return ER, so it does not realize a category.
- `V0627`: The outcome is Return ER, so it does not realize a category.
- `V0631`: The outcome is Return ER, so it does not realize a category.
- `V0632`: The outcome is Return ER, so it does not realize a category.
- `V0635`: The outcome is Return ER, so it does not realize a category.
- `V0636`: The outcome is LacticAcid, lacking a discharge event.
- `V0638`: The outcome involves returning to the ER, not fitting any release category.
- `V0639`: The outcome involves returning to the ER, not fitting any release category.
- `V0640`: The outcome involves returning to the ER, not fitting any release category.
- `V0641`: The outcome involves returning to the ER, not fitting any release category.
- `V0643`: The outcome involves returning to the ER, not fitting any release category.
- `V0644`: The outcome is CRP, lacking a discharge event.
- `V0645`: The outcome is LacticAcid, lacking a discharge event.
- `V0646`: The outcome involves returning to the ER, not fitting any release category.
- `V0649`: The outcome involves returning to the ER, not fitting any release category.
- `V0650`: The outcome involves returning to the ER, not fitting any release category.
- `V0654`: The narrative does not culminate in any release activity, ending prematurely at Leucocytes.
- `V0663`: The process stops at Admission NC and does not complete any release pathway.
- `V0664`: The narrative terminates at IV Liquid and contains no discharge or release steps.
- `V0670`: Although Release A appears midway, the variant ultimately ends with Leucocytes following an ER return, fitting none of the clean terminal release categories.
- `V0676`: The process stops at IV Antibiotics and does not reach any release pathway.
- `V0679`: The narrative terminates at IV Antibiotics without any discharge event.
- `V0685`: The process stops at IV Antibiotics with no release or discharge activity.
- `V0689`: The narrative terminates at IV Antibiotics without reaching a release activity.
- `V0694`: The process stops early at ER Sepsis Triage and does not reach any release pathway.
- `V0703`: The process terminates with IV Liquid and does not reach any discharge or release category.
- `V0705`: The narrative results in a Return ER outcome after Release A, so it does not fit cleanly into a standard category evaluation without residual post-discharge return context.
- `V0707`: The narrative terminates at Admission NC and does not reach a completion or release state.
- `V0708`: The process ends at IV Antibiotics without reaching any discharge or release outcome.
- `V0712`: The narrative ends with a Return ER outcome following initial release, failing to fit standard single-release definitions cleanly.
- `V0713`: The process terminates at IV Antibiotics without a final release or discharge activity.
- `V0719`: The narrative ends with a Return ER outcome after Release A, so it does not match standard release definitions.
- `V0720`: The process results in a Return ER outcome following Release A.
- `V0721`: The narrative concludes with a Return ER outcome after Release A.
- `V0724`: The narrative concludes with a Return ER outcome following initial release.
- `V0727`: The narrative results in a Return ER outcome following Release A.
- `V0734`: The process results in a Return ER outcome following Release A.
- `V0742`: The narrative terminates at LacticAcid and does not reach any release or discharge outcome.
- `V0744`: The narrative results in a Return ER outcome following Release A.
- `V0745`: The process concludes with a Return ER outcome after Release A.
- `V0746`: The narrative results in a Return ER outcome following Release A.
- `V0748`: The narrative ends with a Return ER outcome following Release A.
- `V0750`: The narrative terminates at IV Antibiotics without reaching a discharge or release state.
- `V0759`: The narrative terminates at IV Antibiotics without reaching any discharge activity.
- `V0764`: The variant ends at ER Sepsis Triage and does not involve an inpatient release pathway.
- `V0772`: The trace stops at CRP and does not complete a discharge activity.
- `V0774`: The process trace terminates at ER Sepsis Triage without an admission or release.
- `V0775`: The process terminates at CRP without reaching a release activity.
- `V0777`: The narrative ends at Leucocytes without reaching a discharge or release.
- `V0778`: The narrative terminates at Leucocytes without an inpatient release.
- `V0791`: The process terminates at IV Antibiotics with no discharge or release.
- `V0804`: The narrative results in a Return ER event after initial Release A, falling outside standard success criteria.
- `V0806`: The narrative terminates with Return ER after an initial Release A.
- `V0808`: The narrative concludes with a Return ER event.
- `V0812`: The narrative concludes with a Return ER event following Release A.
- `V0815`: The narrative terminates with a Return ER event.
- `V0816`: Outcome is IV Antibiotics, not a discharge category.
- `V0820`: Outcome is LacticAcid, not a discharge category.
- `V0821`: The narrative concludes with a Return ER event.
- `V0822`: The narrative terminates with a Return ER event.
- `V0823`: The narrative terminates with a Return ER event.
- `V0825`: The narrative concludes with a Return ER event.
- `V0826`: Outcome is Admission NC, not a discharge category.
- `V0827`: The narrative terminates with a Return ER event.
- `V0828`: The narrative concludes with a Return ER event.
- `V0832`: Outcome is IV Antibiotics, not a discharge category.
- `V0834`: The narrative terminates with a Return ER event.
- `V0842`: The narrative terminates with a Return ER event.
- `V0843`: Outcome is IV Liquid, not a discharge category.
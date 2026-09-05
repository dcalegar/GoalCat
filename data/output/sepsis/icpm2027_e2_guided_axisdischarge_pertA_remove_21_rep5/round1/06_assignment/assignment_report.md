# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_axisdischarge_pertA_remove_21_rep5` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Release A (`release_a`)

Represents the standard discharge pathway for patients treated within the facility, helping avoid post-discharge deterioration and measured against post-discharge ER return indicators.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative Release A (id=17), supported by frequent and rare sample variants ending in Release A (e.g., V0008, V0070).

**Goal-model linkage:** 17 (Task): Release A

**Coverage:** macro 589/846 variants (69.6%) · micro 633/1050 cases (60.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.42, nearest other category `release_b` at mean distance 15.08

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.349, nearest other category `release_d` at mean distance 0.446

## Release B (`release_b`)

Represents an alternative discharge path for admitted cases, contributing to avoiding post-discharge deterioration and evaluated against post-discharge ER return indicators.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative Release B (id=18), observed in variants such as V0068 and V0145.

**Goal-model linkage:** 18 (Task): Release B

**Coverage:** macro 55/846 variants (6.5%) · micro 56/1050 cases (5.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 16.61, nearest other category `release_a` at mean distance 15.08

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.248, nearest other category `release_d` at mean distance 0.544

## Release C (`release_c`)

Represents a distinct discharge option for complex or long-stay cases, aiding in post-discharge stability and measured via post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative Release C (id=19), evidenced in extreme length variants such as V0710.

**Goal-model linkage:** 19 (Task): Release C

**Coverage:** macro 25/846 variants (3.0%) · micro 25/1050 cases (2.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 22.70, nearest other category `release_a` at mean distance 18.13

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.268, nearest other category `release_d` at mean distance 0.433

## Release D (`release_d`)

Represents an alternative discharge pathway used for specific patient trajectories, measured against post-discharge ER return indicators.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative Release D (id=20), evidenced in complex length variants such as V0273.

**Goal-model linkage:** 20 (Task): Release D

**Coverage:** macro 23/846 variants (2.7%) · micro 23/1050 cases (2.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 18.85, nearest other category `release_a` at mean distance 16.78

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.295, nearest other category `release_c` at mean distance 0.433

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

154/846 variants (18.2%), 313/1050 cases (29.8%) unassigned.

- `V0001`: This narrative ends in ER Sepsis Triage and does not reach any discharge pathway category.
- `V0002`: This narrative terminates at CRP testing without reaching a discharge pathway.
- `V0003`: This narrative ends at Leucocytes testing and does not represent a discharge pathway.
- `V0004`: This narrative stops at IV Antibiotics administration in the ER and does not show a discharge outcome.
- `V0005`: This narrative concludes with LacticAcid testing without a patient discharge event.
- `V0006`: This narrative ends with IV Antibiotics and does not reach any patient discharge category.
- `V0007`: This narrative terminates at IV Antibiotics without concluding in a discharge event.
- `V0009`: This narrative ends with IV Antibiotics administration and lacks a discharge activity.
- `V0010`: This narrative ends with ER Sepsis Triage and does not involve any discharge pathway.
- `V0011`: This narrative concludes with IV Antibiotics and does not reach a discharge pathway.
- `V0012`: This narrative ends at IV Antibiotics without proceeding to a discharge outcome.
- `V0013`: This narrative terminates at Leucocytes and does not represent a discharge pathway.
- `V0017`: This narrative ends with ER Sepsis Triage and does not contain a discharge pathway.
- `V0019`: This narrative ends with IV Antibiotics and does not reach a discharge pathway.
- `V0020`: This narrative terminates at CRP testing without any discharge event.
- `V0021`: This narrative includes a return to the ER after Release A, but does not fit standard categorization for uncomplicated release pathways.
- `V0023`: This narrative involves an ER return following discharge, falling outside standard category specifications.
- `V0024`: This narrative stops at Admission NC and does not complete a full discharge pathway.
- `V0025`: This narrative ends at IV Antibiotics without reaching a discharge pathway.
- `V0027`: The process ends at IV Antibiotics without any discharge or release activity, so no category fits.
- `V0029`: Terminates at Leucocytes without any discharge event, thus fitting none of the release categories.
- `V0031`: Ends with LacticAcid and lacks a discharge activity, so it belongs to the residual.
- `V0034`: Stops at IV Liquid without reaching a discharge destination.
- `V0036`: Terminates at CRP without any release pathway represented.
- `V0038`: Stops at IV Antibiotics with no discharge activity present.
- `V0040`: Ends at Admission NC without concluding with a release pathway.
- `V0043`: Stops at LacticAcid without a discharge outcome.
- `V0050`: Ends at CRP without any release event, falling into the residual category.
- `V0056`: The process terminates at IV Antibiotics without reaching any discharge pathway.
- `V0062`: The narrative finishes at IV Antibiotics and does not reach a discharge category.
- `V0081`: The narrative terminates at IV Liquid without reaching any discharge or release pathway.
- `V0088`: The narrative stops at IV Antibiotics without concluding via a release pathway.
- `V0092`: The process terminates at LacticAcid without completing any release pathway.
- `V0111`: The narrative ends with Admission NC and does not reach any discharge pathway category.
- `V0127`: The variant ends with LacticAcid and does not reach any discharge pathway.
- `V0132`: The narrative terminates at IV Antibiotics and does not complete a discharge pathway.
- `V0133`: The process ends at IV Antibiotics without reaching a discharge destination.
- `V0137`: The narrative concludes with LacticAcid and lacks a discharge pathway.
- `V0146`: The variant ends with Leucocytes and does not reach any discharge category.
- `V0148`: The narrative terminates at IV Antibiotics and does not realize any discharge category.
- `V0187`: The narrative terminates at CRP without reaching any discharge pathway or completing a full treatment lifecycle.
- `V0196`: The narrative ends with Release E, which does not match any of the defined categories (Release A, Release B, Release C, Release D).
- `V0197`: The process terminates at Leucocytes and does not reach any discharge category.
- `V0217`: The narrative stops at IV Antibiotics and does not reach any discharge or release category.
- `V0219`: The narrative terminates early at Leucocytes without reaching a discharge pathway.
- `V0232`: The narrative ends at IV Antibiotics without reaching any of the defined discharge pathways.
- `V0234`: The variant terminates at Leucocytes and does not contain a discharge event.
- `V0260`: The narrative terminates at IV Antibiotics and does not reach any discharge or release category.
- `V0268`: The narrative terminates at Leucocytes and does not reach any discharge or release category.
- `V0287`: The narrative ends with CRP and does not reach any discharge pathway.
- `V0292`: The narrative stops at Leucocytes without reaching any discharge event.
- `V0295`: The narrative ends at IV Antibiotics without completing a discharge pathway.
- `V0302`: The narrative terminates at ER Sepsis Triage and does not reach any discharge pathway.
- `V0305`: The narrative terminates at IV Antibiotics without reaching a discharge pathway.
- `V0316`: The narrative ends with Release E, which does not exist in the taxonomy categories.
- `V0322`: The narrative terminates at IV Antibiotics without a discharge event.
- `V0325`: The narrative terminates at IV Antibiotics without reaching a discharge pathway.
- `V0330`: The process terminates in IV Liquid without reaching a discharge or release state.
- `V0336`: The process stops at CRP without reaching a release or discharge state.
- `V0342`: The variant terminates at CRP without reaching a release category.
- `V0349`: The narrative terminates at ER Sepsis Triage and does not reach any release category.
- `V0365`: The outcome is Leucocytes rather than any discharge or release pathway, so none of the release categories fit.
- `V0368`: The narrative ends with Admission NC and does not reach any release or discharge activity.
- `V0374`: The narrative ends with Leucocytes and does not reach a release or discharge event.
- `V0378`: The narrative ends with IV Antibiotics and does not reach a discharge pathway category.
- `V0379`: The narrative terminates at IV Antibiotics without reaching a discharge destination.
- `V0382`: Although it includes Release A, the final outcome is Return ER, making it a residual case regarding post-discharge status.
- `V0385`: The narrative ends with Return ER after an interim Release A, falling outside stable standard discharge outcomes.
- `V0386`: The case results in a Return ER outcome after Release A.
- `V0398`: The narrative concludes with a Return ER outcome following Release A.
- `V0415`: The process ends at Admission NC without reaching any of the defined discharge pathways.
- `V0417`: The process ends prematurely at ER Triage and does not realize a discharge category.
- `V0429`: The narrative ends with IV Antibiotics and does not reach a discharge pathway category.
- `V0462`: The outcome is CRP, which does not correspond to any discharge category in the taxonomy.
- `V0488`: The narrative ends at IV Liquid and does not reach any discharge or release category.
- `V0492`: The narrative stops at IV Liquid without reaching a release category.
- `V0495`: The variant ends at IV Antibiotics and does not reach any release category.
- `V0501`: The narrative ends with IV Liquid rather than a recognized discharge pathway category.
- `V0502`: The narrative terminates at Admission NC and does not complete a discharge pathway.
- `V0504`: Although it contains Release A, the final outcome is Return ER, representing an ER return indicator rather than a standard discharge pathway success.
- `V0505`: The variant ends in Return ER after Release A, pointing to a post-discharge ER return rather than a successful standard discharge.
- `V0507`: The sequence ends prematurely at IV Antibiotics without a discharge event.
- `V0508`: The final outcome is Return ER, which does not map to a successful discharge category.
- `V0510`: The process stops at IV Antibiotics without reaching any discharge category.
- `V0515`: The final outcome is Return ER, meaning it represents an ER return rather than a final successful release pathway.
- `V0516`: The narrative terminates at Leucocytes and lacks a discharge pathway.
- `V0517`: The process ends at ER Triage without reaching any discharge or admission destination.
- `V0519`: The final outcome is Return ER, indicating readmission or ER return after release.
- `V0520`: The narrative results in Return ER, not a successful stable discharge outcome.
- `V0549`: The narrative ends in IV Liquid and does not reach any of the specified discharge categories.
- `V0553`: The outcome is Release E, which does not correspond to any of the defined taxonomy categories (release_a, release_b, release_c, release_d).
- `V0556`: Although it passes through Release A, the final outcome is Return ER, which does not align with a successful category completion.
- `V0558`: The process ends with a Return ER outcome, meaning it does not fall under the primary discharge pathway categories.
- `V0559`: The final outcome is Return ER, rendering the discharge classification inapplicable due to readmission.
- `V0560`: The variant results in a Return ER outcome, meaning it fails to satisfy the long-term stable release categories.
- `V0564`: The process concludes with Return ER after an interim release, disqualifying it from the target categories.
- `V0565`: The process terminates with Admission NC and does not reach any discharge pathway category.
- `V0567`: The outcome is Return ER, so it does not realize any of the stable discharge categories.
- `V0573`: The final outcome is Return ER, disqualifying it from a permanent discharge category.
- `V0575`: The narrative terminates at Leucocytes and does not reach any discharge or release category.
- `V0580`: The outcome is 'CRP', which does not match any discharge pathway.
- `V0584`: The outcome is 'IV Liquid', which does not correspond to any discharge release category.
- `V0585`: The outcome is 'LacticAcid', representing an intermediate lab step rather than a discharge pathway.
- `V0587`: The outcome is 'CRP', indicating no match to a release category.
- `V0592`: The outcome is 'IV Antibiotics', which is not a discharge pathway.
- `V0598`: The outcome is 'Release E', which is outside the defined taxonomy categories (release_a to release_d).
- `V0603`: The narrative ends with Release E, which does not correspond to any of the defined taxonomy categories (release_a, release_b, release_c, release_d).
- `V0629`: The narrative terminates with Release E, which does not correspond to any of the specified release categories (release_a, release_b, release_c, release_d).
- `V0636`: The narrative terminates with LacticAcid rather than a recognized discharge pathway, so it falls into the residual.
- `V0644`: The process variant ends with CRP and lacks a recognized discharge outcome, fitting the residual.
- `V0645`: The process variant ends with LacticAcid and lacks a recognized discharge outcome, fitting the residual.
- `V0654`: The variant terminates in Leucocytes without reaching any discharge or release activity.
- `V0663`: The variant ends at Admission NC, lacking any final release or discharge category.
- `V0664`: The variant ends with IV Liquid and does not reach any release pathway.
- `V0676`: The narrative ends with IV Antibiotics and does not reach any discharge pathway.
- `V0679`: The narrative terminates at IV Antibiotics without reaching a discharge activity.
- `V0685`: The narrative stops at IV Antibiotics without reaching any discharge destination.
- `V0689`: The narrative ends at IV Antibiotics without a discharge step.
- `V0694`: The narrative stops at ER Sepsis Triage without reaching any discharge category.
- `V0703`: The narrative ends with IV Liquid and does not reach any discharge outcome.
- `V0705`: Although it passes through Release A, the final outcome is Return ER, placing it outside normal successful discharge pathways.
- `V0707`: The narrative ends at Admission NC without completing a discharge path.
- `V0708`: The narrative terminates at IV Antibiotics and does not reach a discharge category.
- `V0712`: The process terminates with Return ER after a temporary Release A, indicating post-discharge deterioration.
- `V0713`: The narrative stops at IV Antibiotics without reaching any discharge destination.
- `V0718`: The narrative ends with Release D followed by Return ER, indicating a failed trajectory under Release D.
- `V0719`: The narrative ends with Return ER after an intermediate Release A.
- `V0720`: The process ultimately results in Return ER despite an intermediate Release A event.
- `V0721`: The case terminates with Return ER following a standard Release A.
- `V0724`: The narrative terminates with Return ER after an intermediate Release A.
- `V0742`: The outcome is 'LacticAcid' rather than any release category, so it does not fit the taxonomy.
- `V0750`: The outcome is 'IV Antibiotics' without any discharge event, so it does not fit any release category.
- `V0759`: The narrative terminates at IV Antibiotics without reaching any discharge or release category.
- `V0764`: The process terminates at ER Sepsis Triage, which does not constitute any release pathway.
- `V0772`: The process ends with CRP and does not complete a discharge pathway.
- `V0774`: The sequence stops at ER Sepsis Triage and does not reach a release outcome.
- `V0775`: The narrative terminates at CRP without reaching any release category.
- `V0777`: The narrative terminates at Leucocytes and does not reach any discharge pathway category.
- `V0778`: The narrative terminates at Leucocytes without reaching a valid discharge pathway.
- `V0791`: The narrative terminates at IV Antibiotics without reaching any discharge pathway category.
- `V0804`: The narrative results in a Return ER outcome following Release A, meaning it does not cleanly fit standard successful release pathways.
- `V0806`: The narrative results in a Return ER outcome after Release A, so it does not represent a successfully realized category instance.
- `V0808`: The narrative leads to Return ER after Release A, failing to realize a final discharge goal category.
- `V0812`: The narrative results in Return ER after Release A, representing an unsuccessful post-discharge outcome.
- `V0815`: The narrative leads to Return ER following Release A, thus falling into the residual.
- `V0816`: The narrative terminates with IV Antibiotics and does not reach a discharge destination.
- `V0820`: The narrative ends at LacticAcid without completing any discharge pathway.
- `V0821`: The narrative results in Return ER following Release A, hence it does not realize a clean category.
- `V0822`: The narrative terminates with Return ER after Release A.
- `V0823`: The narrative ends with Return ER following Release A.
- `V0825`: The narrative leads to Return ER after Release A.
- `V0826`: The narrative ends in Admission NC without reaching any discharge pathway or final outcome specified in the taxonomy categories.
- `V0832`: The variant ends in IV Antibiotics and does not reach a discharge category.
- `V0843`: The process ends in IV Liquid and does not reach a recognized discharge category.
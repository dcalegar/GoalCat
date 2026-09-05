# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_axisdischarge_rep3` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Release A (`release_a`)

Represents the standard discharge pathway for patients reaching a captured discharge, contributing to avoiding post-discharge deterioration and measured against post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative Release A of goal id=6. Evidenced in multiple variants such as V0008 and V0070.

**Goal-model linkage:** 17 (Task): Release A

**Coverage:** macro 592/846 variants (70.0%) · micro 640/1050 cases (61.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.42, nearest other category `release_b` at mean distance 15.05

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.348, nearest other category `release_d` at mean distance 0.446

## Release B (`release_b`)

Represents an alternative discharge pathway for admitted cases, contributing to avoiding post-discharge deterioration and measured against post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative Release B of goal id=6. Evidenced in variants such as V0068 and V0145.

**Goal-model linkage:** 18 (Task): Release B

**Coverage:** macro 58/846 variants (6.9%) · micro 59/1050 cases (5.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 16.70, nearest other category `release_a` at mean distance 15.05

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.283, nearest other category `release_d` at mean distance 0.538

## Release C (`release_c`)

Represents an alternative discharge pathway for long-stay or complex admitted cases, measured against post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative Release C of goal id=6. Evidenced in variant V0710.

**Goal-model linkage:** 19 (Task): Release C

**Coverage:** macro 22/846 variants (2.6%) · micro 22/1050 cases (2.1%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 24.46, nearest other category `release_a` at mean distance 19.08

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.221, nearest other category `release_d` at mean distance 0.446

## Release D (`release_d`)

Represents an alternative discharge pathway for complex admitted cases requiring extensive monitoring, measured against post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative Release D of goal id=6. Evidenced in variant V0273.

**Goal-model linkage:** 20 (Task): Release D

**Coverage:** macro 23/846 variants (2.7%) · micro 23/1050 cases (2.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 18.19, nearest other category `release_a` at mean distance 16.42

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.294, nearest other category `release_e` at mean distance 0.442

## Release E (`release_e`)

Represents an alternative discharge pathway for captured discharges, measured against post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative Release E of goal id=6. Default mapping applied.

**Goal-model linkage:** 21 (Task): Release E

**Coverage:** macro 6/846 variants (0.7%) · micro 6/1050 cases (0.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 17.67, nearest other category `release_a` at mean distance 16.42

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

145/846 variants (17.1%), 300/1050 cases (28.6%) unassigned.

- `V0001`: This narrative ends at ER Sepsis Triage and does not reach any discharge pathway.
- `V0002`: This narrative ends at CRP testing in the ER and does not reach a discharge pathway.
- `V0003`: This narrative ends at Leucocytes testing in the ER without reaching a discharge pathway.
- `V0004`: This narrative ends at IV Antibiotics administration in the ER and does not reach a discharge pathway.
- `V0005`: This narrative terminates at LacticAcid testing in the ER and does not reach any discharge pathway.
- `V0006`: This narrative ends at IV Antibiotics administration within the ER and lacks a discharge pathway.
- `V0007`: This narrative ends at IV Antibiotics in the ER without reaching a discharge pathway.
- `V0009`: This narrative ends at IV Antibiotics in the ER and does not reach a discharge pathway.
- `V0010`: This narrative terminates at ER Sepsis Triage and does not reach a discharge pathway.
- `V0011`: This narrative concludes with IV Antibiotics in the ER and does not reach a discharge pathway.
- `V0012`: This narrative ends with IV Antibiotics in the ER without a discharge event.
- `V0013`: This narrative terminates at Leucocytes testing and does not reach any discharge pathway.
- `V0017`: This narrative terminates at ER Sepsis Triage and does not reach a discharge pathway.
- `V0019`: This narrative concludes with IV Antibiotics in the ER and lacks a discharge pathway.
- `V0020`: This narrative ends at CRP testing in the ER without reaching any discharge pathway.
- `V0024`: This narrative terminates at Admission NC and does not reach a complete discharge pathway.
- `V0025`: This narrative concludes with IV Antibiotics in the ER and does not reach a discharge pathway.
- `V0027`: The process terminates at IV Antibiotics without reaching any discharge or release activity.
- `V0029`: The process terminates at Leucocytes without reaching a discharge pathway.
- `V0031`: The process terminates at LacticAcid before any discharge step occurs.
- `V0034`: The process terminates at IV Liquid without reaching a discharge pathway.
- `V0036`: The process terminates at CRP without reaching any release activity.
- `V0038`: The process ends at IV Antibiotics without any recorded discharge event.
- `V0040`: The process terminates at Admission NC without any subsequent release or discharge activity.
- `V0043`: The process terminates at LacticAcid without a discharge pathway.
- `V0050`: The process terminates at CRP without reaching a discharge pathway.
- `V0056`: The narrative terminates at IV Antibiotics without reaching a discharge pathway.
- `V0062`: The variant process ends at IV Antibiotics without achieving discharge.
- `V0081`: The narrative ends with IV Liquid rather than a discharge pathway, so no category fits.
- `V0088`: The narrative ends with IV Antibiotics rather than a discharge pathway, so no category fits.
- `V0092`: The narrative ends with LacticAcid rather than a discharge pathway, so no category fits.
- `V0111`: The outcome is Admission NC rather than a discharge pathway, so no release category fits.
- `V0127`: The variant ends in LacticAcid and does not represent a discharge pathway.
- `V0132`: The pathway finishes with IV Antibiotics and does not reach a discharge category.
- `V0133`: The variant ends at IV Antibiotics without concluding with a discharge event.
- `V0137`: The narrative ends with LacticAcid and lacks a discharge milestone.
- `V0146`: The process terminates at Leucocytes without reaching a discharge category.
- `V0148`: The sequence ends at IV Antibiotics and does not involve any discharge classification.
- `V0181`: The variant does not end in a recognized discharge or release activity, instead terminating on Leucocytes.
- `V0187`: The variant is incomplete and terminates on CRP without any discharge or release activity.
- `V0197`: The variant terminates on Leucocytes without reaching any release or discharge activity.
- `V0217`: The narrative terminates at IV Antibiotics without reaching any discharge category.
- `V0219`: The narrative terminates at Leucocytes without reaching any discharge category.
- `V0232`: The variant terminates at IV Antibiotics without reaching any discharge or release activity.
- `V0234`: The process terminates at Leucocytes and does not reach a discharge pathway.
- `V0260`: The narrative terminates at IV Antibiotics and does not reach any discharge pathway category.
- `V0268`: The narrative terminates at Leucocytes and does not reach a discharge pathway category.
- `V0287`: Incomplete case ending in CRP without reaching a release or discharge outcome.
- `V0292`: Incomplete case terminating at Leucocytes without reaching a discharge or release state.
- `V0295`: Incomplete case ending at IV Antibiotics without reaching a discharge or release category.
- `V0302`: The process terminates at ER Sepsis Triage and does not reach any discharge pathway.
- `V0305`: The variant stops at IV Antibiotics in the ER phase without reaching a discharge destination.
- `V0322`: The variant ends at IV Antibiotics without reaching a discharge category.
- `V0325`: The variant terminates at IV Antibiotics in the emergency department, lacking any discharge step.
- `V0330`: The process terminates at IV Liquid and does not reach a discharge category.
- `V0336`: The process ends at CRP and does not reach any discharge pathway.
- `V0342`: The process ends at CRP without reaching a discharge destination.
- `V0349`: The process ends at ER Sepsis Triage without reaching any discharge destination.
- `V0365`: The outcome is Leucocytes rather than any discharge or release activity, so no release category applies.
- `V0368`: The pathway terminates at Admission NC without reaching any discharge or release outcome.
- `V0374`: The sequence ends with Leucocytes and does not reach a recognized discharge pathway.
- `V0378`: The narrative ends with IV Antibiotics rather than a recognized discharge category.
- `V0379`: The narrative terminates at IV Antibiotics without reaching a discharge pathway.
- `V0382`: The final outcome is Return ER after a Release A event, which does not map cleanly into a standard planned release category.
- `V0385`: The narrative leads to Return ER after a Release A event, falling outside normal discharge categories.
- `V0386`: The outcome is Return ER following Release A, which does not fit standard discharge pathways.
- `V0398`: The final outcome is Return ER after Release A, which falls outside the intended discharge taxonomy.
- `V0415`: The variant terminates at Admission NC and does not reach any discharge or release outcome.
- `V0417`: The variant loops back to ER Triage and does not reach any release pathway.
- `V0427`: The narrative ends with Return ER rather than a recognized discharge category.
- `V0429`: The narrative does not reach a discharge endpoint, ending with IV Antibiotics.
- `V0435`: The narrative ultimately results in Return ER, not fitting any valid final release category.
- `V0437`: The narrative ends with Return ER after an intermediate Release D outcome.
- `V0440`: The narrative terminates with Return ER.
- `V0441`: The narrative terminates with Return ER.
- `V0442`: The narrative terminates with Return ER.
- `V0443`: The narrative terminates with Return ER.
- `V0447`: The narrative terminates with Return ER.
- `V0448`: The narrative terminates with Return ER.
- `V0449`: The narrative terminates with Return ER.
- `V0462`: The narrative does not culminate in any recognized discharge pathway (ends with CRP).
- `V0488`: The narrative ends in IV Liquid without reaching any discharge category.
- `V0492`: The narrative ends in IV Liquid without reaching a discharge destination.
- `V0495`: The process terminates at IV Antibiotics without reaching a discharge category.
- `V0501`: The process terminates at IV Liquid rather than a recognized discharge category.
- `V0502`: The process terminates at Admission NC without any discharge outcome.
- `V0504`: The outcome is Return ER after a standard discharge, meaning it represents a post-discharge ER return rather than a pure discharge category pathway realization.
- `V0505`: The outcome is Return ER, not fitting any distinct release path category in the taxonomy.
- `V0507`: The process ends at IV Antibiotics without discharge.
- `V0508`: The process terminates with a Return ER event.
- `V0510`: The process ends at IV Antibiotics without reaching a discharge pathway.
- `V0515`: The process results in a Return ER outcome.
- `V0516`: The process terminates prematurely at Leucocytes.
- `V0517`: The process terminates prematurely at ER Triage.
- `V0519`: The process results in a Return ER outcome.
- `V0520`: The process results in a Return ER outcome.
- `V0549`: The narrative does not reach any discharge or release category, ending prematurely at IV Liquid.
- `V0556`: The narrative results in a Return ER outcome following Release A, meaning it does not fit the standard single discharge pathway scope of the categories without a return condition.
- `V0558`: The narrative culminates in a Return ER outcome after Release A, so it does not cleanly match the final discharge categories.
- `V0559`: The outcome is Return ER after Release A, making it part of the residual.
- `V0560`: The narrative leads to Return ER after Release A, so it is excluded from the direct release categories.
- `V0564`: The case ends with Return ER following Release A.
- `V0565`: The narrative terminates at Admission NC without a final release outcome.
- `V0567`: The narrative ends with Return ER after Release A.
- `V0573`: The narrative leads to a Return ER outcome after Release A.
- `V0575`: The narrative ends at Leucocytes without reaching a discharge or release category.
- `V0580`: The narrative does not reach any release or discharge outcome, ending on CRP instead.
- `V0584`: The process terminates at IV Liquid without reaching any discharge category.
- `V0585`: The process ends at LacticAcid and does not reach a discharge pathway.
- `V0587`: The process stops at CRP without reaching a release event.
- `V0592`: The process ends at IV Antibiotics without any discharge outcome.
- `V0605`: The outcome is Return ER, meaning it does not successfully complete a standard discharge pathway category.
- `V0614`: The outcome is Return ER, so it does not realize a final discharge category.
- `V0615`: The outcome is Return ER despite ending temporarily with Release C.
- `V0625`: The outcome is Return ER, meaning it does not fall into a successful discharge category.
- `V0636`: The narrative does not conclude with a recognized release activity, ending instead with LacticAcid.
- `V0644`: The process variant ends with CRP instead of a discharge event.
- `V0645`: The process variant terminates with LacticAcid without completing a discharge path.
- `V0654`: The narrative ends with Leucocytes and does not reach any discharge pathway category.
- `V0663`: The narrative terminates at Admission NC and does not reach any release or discharge category.
- `V0664`: The narrative terminates at IV Liquid and does not reach any discharge category.
- `V0676`: The narrative ends with IV Antibiotics and does not reach a discharge pathway.
- `V0679`: The narrative ends with IV Antibiotics and does not reach a discharge pathway.
- `V0685`: The narrative ends with IV Antibiotics and does not reach a discharge pathway.
- `V0689`: The narrative ends with IV Antibiotics and does not reach a discharge pathway.
- `V0694`: The narrative ends with ER Sepsis Triage and does not reach a discharge pathway.
- `V0703`: The narrative does not conclude with any release pathway matching the taxonomy, ending in IV Liquid instead.
- `V0707`: The narrative terminates at Admission NC and does not reach any release pathway.
- `V0708`: The narrative terminates at IV Antibiotics without reaching a discharge pathway.
- `V0713`: The narrative terminates at IV Antibiotics without any discharge outcome.
- `V0742`: The narrative does not culminate in any discharge pathway, ending instead in LacticAcid.
- `V0750`: The narrative terminates at IV Antibiotics without reaching any discharge pathway.
- `V0759`: The outcome is IV Antibiotics rather than a discharge pathway, so no release category applies.
- `V0764`: The case terminates at ER Sepsis Triage without reaching a discharge or release pathway.
- `V0772`: The process terminates at CRP and does not reach a discharge pathway.
- `V0774`: The variant ends at ER Sepsis Triage and does not complete a discharge pathway.
- `V0775`: The process ends at CRP without reaching a release or discharge event.
- `V0777`: The narrative does not conclude with a discharge pathway, ending instead at Leucocytes.
- `V0778`: The narrative ends with Leucocytes rather than any discharge category.
- `V0791`: The narrative terminates at IV Antibiotics and does not reach any discharge category.
- `V0816`: The process terminates at IV Antibiotics without reaching any release or discharge outcome.
- `V0820`: The process ends at LacticAcid without completing any discharge pathway.
- `V0826`: The narrative ends in Admission NC without a release activity, so it does not realize any discharge pathway category.
- `V0832`: The narrative terminates at IV Antibiotics and does not reach any release activity.
- `V0843`: The narrative ends with IV Liquid and does not reach a release activity.
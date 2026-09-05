# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_axisdischarge_rep1` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Release A (`release_a`)

Represents the standard discharge pathway for patients after successful admission and treatment, evaluated against post-discharge ER return indicators, contributing positively to avoiding post-discharge deterioration.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release A (id=17) as observed in multiple variants such as V0008, V0070, and V0069 representing normal discharge outcomes.

**Goal-model linkage:** 17 (Task): Release A

**Coverage:** macro 563/846 variants (66.5%) · micro 607/1050 cases (57.8%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.16, nearest other category `release_b` at mean distance 13.97

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.343, nearest other category `release_d` at mean distance 0.450

## Release B (`release_b`)

Represents an alternative discharge pathway following inpatient care, tracked via post-discharge ER return measures and supporting the avoidance of post-discharge deterioration.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release B (id=18) as seen in rare variants like V0068 and V0145.

**Goal-model linkage:** 18 (Task): Release B

**Coverage:** macro 77/846 variants (9.1%) · micro 82/1050 cases (7.8%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 15.62, nearest other category `release_a` at mean distance 13.97

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.370, nearest other category `release_d` at mean distance 0.486

## Release C (`release_c`)

Represents a specific discharge route for long-stay or complex admitted cases, measured against post-discharge return rates.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release C (id=19) as observed in prolonged complex variants such as V0710.

**Goal-model linkage:** 19 (Task): Release C

**Coverage:** macro 29/846 variants (3.4%) · micro 29/1050 cases (2.8%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 25.09, nearest other category `release_a` at mean distance 19.46

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.310, nearest other category `release_d` at mean distance 0.427

## Release D (`release_d`)

Represents a specialized discharge pathway for patients requiring extended recovery monitoring prior to leaving the hospital.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release D (id=20) corresponding to outcomes found in complex long-duration trace samples like V0273.

**Goal-model linkage:** 20 (Task): Release D

**Coverage:** macro 23/846 variants (2.7%) · micro 23/1050 cases (2.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 19.17, nearest other category `release_a` at mean distance 16.91

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.296, nearest other category `release_c` at mean distance 0.427

## Release E (`release_e`)

Represents alternative discharge routing for specific treated patient subsets.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release E (id=21) based on the goal model decomposition axis without subdivision since no distinct sub-patterns emerged.

**Goal-model linkage:** 21 (Task): Release E

**Coverage:** macro 6/846 variants (0.7%) · micro 6/1050 cases (0.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 17.67, nearest other category `release_a` at mean distance 16.37

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.253, nearest other category `release_d` at mean distance 0.443

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

- `V0021` (`release_b`) / `V0124` (`release_a`): structural=1, profile=0.036
- `V0021` (`release_b`) / `V0529` (`release_a`): structural=1, profile=0.051
- `V0022` (`release_a`) / `V0274` (`release_c`): structural=1, profile=0.374
- `V0023` (`release_b`) / `V0697` (`release_a`): structural=1, profile=0.410
- `V0026` (`release_a`) / `V0734` (`release_b`): structural=1, profile=0.072
- `V0037` (`release_b`) / `V0706` (`release_a`): structural=1, profile=0.359
- `V0044` (`release_a`) / `V0754` (`release_b`): structural=1, profile=0.378
- `V0052` (`release_a`) / `V0734` (`release_b`): structural=1, profile=0.186
- `V0100` (`release_a`) / `V0586` (`release_b`): structural=1, profile=0.339
- `V0200` (`release_a`) / `V0734` (`release_b`): structural=1, profile=0.246

## Residual

148/846 variants (17.5%), 303/1050 cases (28.9%) unassigned.

- `V0001`: The process terminates at ER Sepsis Triage without any admission or discharge pathway.
- `V0002`: The process terminates at CRP during the emergency department phase without admission.
- `V0003`: The process ends at Leucocytes in the ER and does not represent a discharge pathway.
- `V0004`: The process concludes with IV Antibiotics in the ER without inpatient admission or discharge.
- `V0005`: The process stops at LacticAcid in the ER with no admission or discharge event.
- `V0006`: The sequence ends with IV Antibiotics in the ER and does not involve hospital admission.
- `V0007`: The process finishes at IV Antibiotics in the ER without any discharge pathway.
- `V0009`: The process ends with IV Antibiotics in the emergency department phase.
- `V0010`: The process terminates at ER Sepsis Triage without reaching any discharge activity.
- `V0011`: The pathway concludes with IV Antibiotics in the ER and does not include an admission or discharge.
- `V0012`: The variant ends at IV Antibiotics in the ER without proceeding to admission.
- `V0013`: The sequence terminates at Leucocytes in the ER without inpatient care.
- `V0017`: The process ends at ER Sepsis Triage and does not represent a discharge pathway.
- `V0019`: The process terminates at IV Antibiotics in the ER without inpatient admission.
- `V0020`: The sequence ends at CRP in the ER and does not involve hospital discharge.
- `V0024`: The process stops at Admission NC and does not reach a final discharge pathway or outcome.
- `V0025`: The sequence ends with IV Antibiotics in the ER without reaching admission or discharge.
- `V0027`: The variant ends in IV Antibiotics without reaching a discharge pathway.
- `V0029`: The process terminates at Leucocytes, lacking a discharge event.
- `V0031`: Terminates at LacticAcid before any discharge or ward transfer occurs.
- `V0034`: Stops at IV Liquid without reaching a discharge pathway.
- `V0036`: Ends at CRP and does not include a discharge pathway.
- `V0038`: Terminates at IV Antibiotics without reaching any discharge category.
- `V0040`: Ends immediately after Admission NC without progressing to a final discharge pathway.
- `V0043`: Terminates at LacticAcid without completing a hospital stay or discharge.
- `V0050`: Terminates at CRP during initial assessment without a discharge event.
- `V0056`: The narrative terminates at 'IV Antibiotics' without reaching any discharge or release activity.
- `V0062`: The sequence ends at 'IV Antibiotics' and does not involve any discharge pathway.
- `V0081`: The outcome is IV Liquid rather than any discharge category.
- `V0088`: The outcome is IV Antibiotics, not a discharge route.
- `V0092`: The outcome is LacticAcid, which is not a discharge pathway.
- `V0111`: The narrative terminates at Admission NC and does not reach any release pathway.
- `V0127`: The outcome is LacticAcid, which does not correspond to any discharge pathway category.
- `V0132`: The outcome is IV Antibiotics, which is not a discharge pathway.
- `V0133`: The outcome is IV Antibiotics, which is not a discharge pathway.
- `V0137`: The outcome is LacticAcid, which is not a discharge pathway.
- `V0146`: The outcome is Leucocytes, which is not a discharge pathway.
- `V0148`: The outcome is IV Antibiotics, which is not a discharge pathway.
- `V0151`: The narrative ends with Return ER after an extended monitoring pathway, but does not fit any of the standard release categories as its final outcome is Return ER.
- `V0154`: Although it passes through Admission NC and Release A, the ultimate outcome is Return ER after a prolonged period, placing it outside the clean discharge criteria.
- `V0155`: The variant ends with Return ER, disqualifying it from standard successful discharge categories.
- `V0157`: The patient returns to the ER, resulting in Return ER as the final outcome.
- `V0160`: The pathway concludes with a Return ER outcome.
- `V0161`: The variant ends with Return ER after a long-duration stay.
- `V0163`: The case results in Return ER, making it ineligible for a successful release category.
- `V0164`: The pathway ends with Return ER.
- `V0168`: The final outcome is Return ER.
- `V0171`: The final outcome is Return ER.
- `V0172`: The pathway ends with Return ER.
- `V0174`: The case ultimately results in Return ER.
- `V0181`: The process terminates with Leucocytes rather than a recognized discharge category.
- `V0187`: Incomplete pathway ending in CRP without reaching any discharge category.
- `V0197`: The sequence terminates in Leucocytes without reaching a discharge category.
- `V0217`: The narrative terminates at IV Antibiotics without reaching any discharge pathway category.
- `V0219`: The narrative ends with Leucocytes and does not reach any discharge category.
- `V0232`: The narrative does not conclude with any discharge pathway activity (ends at IV Antibiotics).
- `V0234`: The narrative does not conclude with any discharge pathway activity (ends at Leucocytes).
- `V0260`: The narrative terminates at IV Antibiotics without reaching any discharge pathway.
- `V0268`: The process ends at Leucocytes without reaching any discharge outcome.
- `V0287`: Does not reach a discharge or release state, ending in CRP.
- `V0292`: Does not reach a release state, ending prematurely at Leucocytes.
- `V0295`: Incomplete pathway ending in IV Antibiotics without reaching a discharge category.
- `V0302`: The narrative stops at ER Sepsis Triage and does not reach any discharge pathway or final resolution category.
- `V0305`: The variant terminates at IV Antibiotics inside the emergency department without reaching a discharge destination.
- `V0309`: The narrative routes through Release B early in the process rather than serving as a terminal discharge pathway matching the category criteria.
- `V0322`: Terminates at IV Antibiotics in the emergency room without reaching a discharge destination.
- `V0325`: Process stops at IV Antibiotics in the ER and does not reach any discharge category.
- `V0330`: The variant ends in IV Liquid and does not reach a recognized discharge category.
- `V0336`: The variant ends with CRP and does not complete a discharge pathway.
- `V0342`: The process stops at CRP and does not reach any discharge category.
- `V0349`: The sequence ends at ER Sepsis Triage and does not complete a discharge process.
- `V0365`: The variant ends with Leucocytes rather than any recognized discharge pathway.
- `V0368`: The narrative terminates at Admission NC without reaching a discharge pathway.
- `V0374`: The process stops at Leucocytes and does not complete a discharge activity.
- `V0378`: The outcome is IV Antibiotics, which is not a discharge pathway or one of the defined release categories.
- `V0379`: The outcome is IV Antibiotics, representing treatment rather than a final discharge category.
- `V0382`: The narrative results in a Return ER outcome following Release A, representing a post-discharge ER return rather than a direct realization of the primary release categories.
- `V0385`: The narrative ends with a Return ER outcome after Release A, which does not fit any of the primary release categories.
- `V0386`: The final outcome is Return ER after Release A, so it does not directly realize any standard release category.
- `V0398`: The final outcome is Return ER following Release A, meaning it does not fall cleanly into a standard release category.
- `V0415`: The process terminates prematurely at Admission NC without reaching any of the discharge release categories.
- `V0417`: The process loops back to ER Triage and does not reach a discharge release category.
- `V0429`: The narrative terminates at IV Antibiotics without reaching any discharge pathway.
- `V0462`: The variant terminates in CRP rather than a discharge pathway, so none of the release categories fit.
- `V0488`: The outcome is IV Liquid, meaning the patient was not discharged during this path.
- `V0492`: The variant terminates at IV Liquid and does not reach any discharge category.
- `V0495`: The variant outcome is IV Antibiotics with no discharge activity present.
- `V0501`: The narrative ends with IV Liquid and does not reach any discharge pathway.
- `V0502`: The narrative ends with Admission NC and lacks a discharge activity.
- `V0504`: The narrative terminates with Return ER after Release A, indicating a post-discharge ER return.
- `V0505`: The narrative terminates with Return ER after Release A, indicating a post-discharge ER return.
- `V0507`: The narrative terminates at IV Antibiotics without reaching any discharge event.
- `V0508`: The narrative terminates with Return ER following Release A, representing a post-discharge return.
- `V0510`: The narrative ends at IV Antibiotics without any discharge outcome.
- `V0515`: The narrative ends with Return ER following Release A.
- `V0516`: The narrative terminates at Leucocytes without reaching any discharge pathway.
- `V0517`: The narrative ends prematurely at ER Triage.
- `V0519`: The narrative ends with Return ER following Release A.
- `V0520`: The narrative ends with Return ER following Release A.
- `V0549`: The narrative terminates at IV Liquid and does not reach any discharge category.
- `V0565`: The narrative terminates at Admission NC and does not reach any discharge category.
- `V0575`: The narrative terminates at Leucocytes and does not reach any discharge category.
- `V0580`: The variant ends in CRP and does not reach any discharge pathway category.
- `V0584`: The variant terminates at IV Liquid and does not complete a discharge pathway.
- `V0585`: The variant ends at LacticAcid and does not reach a discharge category.
- `V0587`: The variant terminates at CRP without any discharge event.
- `V0592`: The variant ends at IV Antibiotics without reaching a discharge pathway.
- `V0605`: The patient returns to the ER after discharge, meaning it does not successfully realize the standard post-discharge non-return criteria of the categories.
- `V0614`: The variant ends with a return to the ER following Release A, failing to meet the successful post-discharge condition.
- `V0615`: The variant ends with a return to the ER following Release C, failing the post-discharge non-return criteria.
- `V0625`: The variant results in a return to the ER after Release A, failing the successful post-discharge evaluation.
- `V0636`: Does not end in a recognized discharge pathway category, terminating with LacticAcid instead.
- `V0644`: Terminates with CRP without a formal discharge category outcome.
- `V0645`: Terminates with LacticAcid rather than reaching a recognized discharge pathway.
- `V0654`: The narrative terminates at Leucocytes rather than any discharge category.
- `V0663`: The sequence terminates at Admission NC without reaching any discharge pathway.
- `V0664`: The sequence halts at IV Liquid early in the process, well before any discharge category.
- `V0670`: The narrative terminates after Leucocytes following an inconclusive sequence involving a return and re-testing.
- `V0676`: The narrative ends with IV Antibiotics and does not reach any discharge pathway.
- `V0679`: The process terminates at IV Antibiotics without any discharge event.
- `V0685`: The sequence ends at IV Antibiotics without reaching a discharge activity.
- `V0689`: The process ends at IV Antibiotics without reaching any discharge state.
- `V0694`: The process stops at ER Sepsis Triage, far before any discharge.
- `V0703`: The narrative ends with IV Liquid and does not reach a discharge pathway category.
- `V0707`: The narrative ends at Admission NC and does not reach a discharge category.
- `V0708`: The narrative terminates at IV Antibiotics without reaching discharge routing.
- `V0713`: The narrative ends at IV Antibiotics and does not reach any release category.
- `V0742`: The narrative terminates at LacticAcid without completing any discharge pathway, so no release category applies.
- `V0750`: The narrative terminates at IV Antibiotics and does not reach any patient discharge or release event.
- `V0759`: The process terminates at IV Antibiotics without reaching any discharge pathway, so no category fits.
- `V0764`: The process terminates at ER Sepsis Triage and does not involve any discharge route.
- `V0772`: The process ends prematurely at CRP before reaching any discharge event.
- `V0774`: The process terminates at ER Sepsis Triage and has no discharge pathway.
- `V0775`: The process terminates at CRP without reaching a discharge pathway.
- `V0777`: The variant ends with Leucocytes and does not complete a discharge pathway.
- `V0778`: The variant ends with Leucocytes and does not reach a discharge outcome.
- `V0779`: The variant results in a Return ER outcome following Release A, meaning it does not fit the standard successful discharge criteria.
- `V0785`: The variant results in a Return ER outcome after Release A, disqualifying it from successful standard discharge.
- `V0787`: The variant terminates with a Return ER outcome following initial release.
- `V0791`: The variant stops at IV Antibiotics in the emergency department and does not reach any discharge pathway.
- `V0794`: The variant results in a Return ER outcome after initial release.
- `V0797`: The variant results in a Return ER outcome after release.
- `V0798`: The variant ends with a Return ER outcome following initial release.
- `V0816`: The process terminates at IV Antibiotics without reaching any discharge pathway category.
- `V0820`: The process terminates at LacticAcid without progressing to any discharge category.
- `V0826`: The narrative ends with Admission NC and does not reach any discharge pathway or final outcome specified in the categories.
- `V0832`: The narrative terminates at IV Antibiotics without reaching any discharge activity.
- `V0843`: The narrative terminates at IV Liquid and does not reach a discharge endpoint.
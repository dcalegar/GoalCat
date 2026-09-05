# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_axisdischarge_rep2` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Release A (`release_a`)

Represents the standard discharge pathway for patients after successful treatment and admission, contributing to avoiding post-discharge deterioration and measured against post-discharge ER return indicators.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative Release A of goal id=6. Evidenced in multiple variants such as V0008.

**Goal-model linkage:** 17 (Task): Release A

**Coverage:** macro 585/846 variants (69.1%) · micro 629/1050 cases (59.9%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.40, nearest other category `release_b` at mean distance 14.86

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.347, nearest other category `release_d` at mean distance 0.444

## Release B (`release_b`)

Represents an alternative discharge pathway following inpatient care, contributing to avoiding post-discharge deterioration and evaluated against post-discharge readmission indicators.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative Release B of goal id=6. Evidenced in narrative variants like V0068 and V0145.

**Goal-model linkage:** 18 (Task): Release B

**Coverage:** macro 61/846 variants (7.2%) · micro 62/1050 cases (5.9%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 16.57, nearest other category `release_a` at mean distance 14.86

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.312, nearest other category `release_d` at mean distance 0.529

## Release C (`release_c`)

Represents a distinct discharge pathway for long-stay or complex admitted patients, measured against post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative Release C of goal id=6, supported by long-running complex variants such as V0710.

**Goal-model linkage:** 19 (Task): Release C

**Coverage:** macro 25/846 variants (3.0%) · micro 25/1050 cases (2.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 22.70, nearest other category `release_a` at mean distance 18.12

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.268, nearest other category `release_d` at mean distance 0.433

## Release D (`release_d`)

Represents an alternative discharge path for patients with specialized recovery trajectories, evaluated against post-discharge outcomes.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative Release D of goal id=6, evidenced by variant V0273.

**Goal-model linkage:** 20 (Task): Release D

**Coverage:** macro 24/846 variants (2.8%) · micro 24/1050 cases (2.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 19.12, nearest other category `release_a` at mean distance 17.07

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.300, nearest other category `release_c` at mean distance 0.433

## Release E (`release_e`)

Represents an alternative discharge path for specific clinical outcomes under goal id=6.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative Release E of goal id=6 as declared in the goal model decomposition.

**Goal-model linkage:** 21 (Task): Release E

**Coverage:** macro 6/846 variants (0.7%) · micro 6/1050 cases (0.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 17.67, nearest other category `release_a` at mean distance 16.39

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
- `V0026` (`release_a`) / `V0734` (`release_b`): structural=1, profile=0.072
- `V0037` (`release_b`) / `V0706` (`release_a`): structural=1, profile=0.359
- `V0052` (`release_a`) / `V0734` (`release_b`): structural=1, profile=0.186
- `V0100` (`release_a`) / `V0586` (`release_b`): structural=1, profile=0.339
- `V0200` (`release_a`) / `V0734` (`release_b`): structural=1, profile=0.246
- `V0396` (`release_a`) / `V0410` (`release_d`): structural=1, profile=0.334
- `V0008` (`release_a`) / `V0037` (`release_b`): structural=2, profile=0.337
- `V0014` (`release_a`) / `V0691` (`release_b`): structural=2, profile=0.388
- `V0014` (`release_a`) / `V0725` (`release_d`): structural=2, profile=0.674

## Residual

145/846 variants (17.1%), 304/1050 cases (29.0%) unassigned.

- `V0001`: This variant ends at ER Sepsis Triage without leading to an admission or discharge pathway corresponding to the defined categories.
- `V0002`: The process terminates at CRP in the emergency phase and does not represent a discharge pathway.
- `V0003`: The variant stops at Leucocytes testing in the emergency department, with no admission or discharge outcome.
- `V0004`: The process concludes with IV Antibiotics administration in the ER and does not involve admission or discharge.
- `V0005`: The variant ends at LacticAcid testing in the emergency setting without any downstream admission or release.
- `V0006`: The sequence ends with IV Antibiotics in the ER, lacking any inpatient admission or release pathway.
- `V0007`: The process concludes at IV Antibiotics in the ER without reaching an admission or discharge stage.
- `V0009`: The variant finishes with IV Antibiotics in the ER and does not proceed to an admission or discharge category.
- `V0010`: The sequence terminates at ER Sepsis Triage and does not represent an inpatient admission or discharge pathway.
- `V0011`: The variant ends with IV Antibiotics in the ER without any admission or subsequent release event.
- `V0012`: The process finishes with IV Antibiotics in the ER and lacks inpatient care or a discharge pathway.
- `V0013`: The variant stops at Leucocytes evaluation in the ER, with no subsequent admission or release.
- `V0017`: The process terminates at ER Sepsis Triage and does not reach an admission or discharge phase.
- `V0019`: The variant ends with IV Antibiotics in the ER without involving inpatient admission or release.
- `V0020`: The sequence terminates at CRP testing in the ER, with no admission or discharge recorded.
- `V0021`: Although the variant includes Release A, it results in a subsequent Return ER event (readmission/ER return indicator), which does not align with the clean standard discharge categories without post-discharge ER return.
- `V0023`: The variant features Release A followed by Return ER, indicating a post-discharge ER return which falls outside the successful standard discharge pathway criteria.
- `V0024`: The process ends at Admission NC, meaning the patient was admitted but the discharge pathway was not completed within this variant's scope.
- `V0025`: The variant terminates with IV Antibiotics in the emergency department and does not involve admission or release.
- `V0027`: The narrative ends with IV Antibiotics and does not reach any discharge or release pathway.
- `V0029`: The process terminates at Leucocytes without an inpatient stay or discharge outcome.
- `V0031`: The narrative ends at LacticAcid without admission or discharge.
- `V0034`: The process ends at IV Liquid and does not progress to admission or discharge.
- `V0036`: The sequence terminates at CRP without reaching a release or discharge stage.
- `V0038`: The sequence terminates at IV Antibiotics without admission or discharge.
- `V0040`: The process stops at Admission NC and does not complete a discharge pathway.
- `V0043`: The process ends at LacticAcid without any admission or discharge activities.
- `V0050`: The sequence ends at CRP without reaching admission or discharge.
- `V0056`: The variant ends with IV Antibiotics rather than a discharge activity, so it does not fit any release category.
- `V0062`: The variant terminates at IV Antibiotics and does not reach a discharge activity.
- `V0081`: The narrative terminates in IV Liquid without reaching a discharge or release pathway.
- `V0088`: The narrative ends at IV Antibiotics without any admission or discharge event.
- `V0092`: The narrative stops at LacticAcid without admission or discharge.
- `V0111`: The process terminates at Admission NC without reaching any discharge category.
- `V0127`: The narrative ends with LacticAcid and does not reach any discharge pathway.
- `V0132`: The process terminates at IV Antibiotics without reaching a discharge pathway.
- `V0133`: The process terminates at IV Antibiotics without reaching a discharge pathway.
- `V0137`: The process terminates with clinical tests (LacticAcid) rather than a discharge pathway.
- `V0146`: The process terminates at Leucocytes without reaching a discharge pathway.
- `V0148`: The process terminates at IV Antibiotics without reaching a discharge pathway.
- `V0181`: The narrative does not conclude with a recognized discharge outcome, ending in Leucocytes instead.
- `V0187`: Incomplete pathway ending in diagnostic activity CRP without any discharge event.
- `V0197`: Incomplete diagnostic sequence ending in Leucocytes without a discharge event.
- `V0217`: The narrative terminates at IV Antibiotics without reaching any discharge or release category.
- `V0219`: The process variant ends at Leucocytes and does not reach a discharge or release category.
- `V0232`: The narrative stops at IV Antibiotics and does not reach any discharge or release category.
- `V0234`: The process terminates at Leucocytes and does not reach any discharge pathway.
- `V0260`: The process terminates at IV Antibiotics without reaching any discharge pathway or final outcome category.
- `V0268`: The process terminates at Leucocytes and does not reach a discharge category.
- `V0287`: The variant terminates at CRP and does not reach any discharge pathway.
- `V0292`: The variant terminates at Leucocytes and does not reach a discharge category.
- `V0295`: The variant terminates at IV Antibiotics without reaching a discharge pathway.
- `V0302`: The variant terminates at ER Sepsis Triage and does not reach any discharge pathway.
- `V0305`: The process ends at IV Antibiotics without reaching a discharge category.
- `V0322`: The narrative ends at IV Antibiotics and does not reach any discharge category.
- `V0325`: The process terminates at IV Antibiotics without reaching a discharge category.
- `V0330`: The narrative terminates at IV Liquid and does not reach any discharge pathway.
- `V0336`: The narrative terminates at CRP and does not lead to a discharge pathway.
- `V0342`: The narrative terminates at CRP without reaching any discharge outcome.
- `V0349`: The narrative terminates at ER Sepsis Triage and does not complete any discharge pathway.
- `V0365`: The variant does not complete a discharge pathway and instead ends with Leucocytes.
- `V0368`: The process terminates at Admission NC without reaching any discharge category.
- `V0374`: The sequence ends on Leucocytes and does not represent a completed discharge pathway.
- `V0378`: The narrative terminates at IV Antibiotics without reaching a discharge pathway.
- `V0379`: The narrative terminates at IV Antibiotics without reaching a discharge pathway.
- `V0415`: The outcome is Admission NC without any discharge event, meaning no discharge category is realized.
- `V0417`: The outcome is ER Triage without any discharge or admission pathway completion, thus no category fits.
- `V0429`: The process terminates at IV Antibiotics without an inpatient admission or discharge pathway.
- `V0462`: The narrative does not conclude with a recognized release pathway, ending instead with CRP testing.
- `V0488`: The narrative terminates in IV Liquid without reaching a discharge or release event.
- `V0492`: The narrative ends with IV Liquid and does not reach any release or discharge activity.
- `V0495`: The narrative terminates with IV Antibiotics and does not reach a discharge event.
- `V0501`: The narrative ends with IV Liquid rather than a standard discharge pathway or release event.
- `V0502`: The narrative terminates at Admission NC and does not reach a discharge or release state.
- `V0507`: The narrative terminates at IV Antibiotics without an admission or discharge event.
- `V0510`: The process terminates at IV Antibiotics without any admission or discharge activities.
- `V0516`: The narrative ends with Leucocytes, which does not constitute a valid discharge or release pathway.
- `V0517`: The narrative terminates at ER Triage and does not involve admission or discharge.
- `V0549`: The narrative terminates at IV Liquid without reaching any discharge or release event, so no release category fits.
- `V0556`: The outcome is Return ER rather than any standard discharge category, making it part of the residual.
- `V0558`: The outcome is Return ER, so it does not fit the discharge categories.
- `V0559`: The outcome is Return ER, therefore outside of the discharge categories.
- `V0560`: The outcome is Return ER, not fitting any of the discharge release pathways.
- `V0564`: The outcome leads to Return ER, so it does not map to any release pathway category.
- `V0565`: The process terminates with Admission NC and lacks a final release outcome, rendering it part of the residual.
- `V0567`: The outcome is Return ER, falling outside the defined release pathways.
- `V0573`: The outcome is Return ER, which does not fit any of the release categories.
- `V0575`: The variant ends with Leucocytes rather than any discharge category, making it part of the residual.
- `V0580`: The narrative terminates at CRP and does not reach any discharge pathway.
- `V0584`: The narrative stops at IV Liquid and does not reach a discharge pathway.
- `V0585`: The narrative terminates at LacticAcid without any discharge event.
- `V0587`: The narrative ends at CRP without reaching a discharge pathway.
- `V0592`: The narrative terminates at IV Antibiotics without reaching a discharge pathway.
- `V0636`: The outcome is LacticAcid rather than a recognized release pathway, so it falls into the residual.
- `V0644`: Outcome is CRP, which does not represent a discharge pathway.
- `V0645`: Outcome is LacticAcid, lacking a discharge event.
- `V0654`: The narrative ends before any discharge activity is reached, hence no release category applies.
- `V0663`: The process halts at Admission NC without reaching any discharge pathway.
- `V0664`: The process ends at IV Liquid without reaching a discharge category.
- `V0670`: The narrative ends with Leucocytes following an ER return and further lab work, matching no discharge category.
- `V0676`: The narrative ends with IV Antibiotics and does not reach a discharge or release pathway.
- `V0679`: The narrative terminates at IV Antibiotics without any discharge outcome.
- `V0685`: The process terminates at IV Antibiotics without reaching a discharge pathway.
- `V0689`: Ends with IV Antibiotics and does not reach a discharge status.
- `V0694`: Terminates prematurely at ER Sepsis Triage without discharge or admission.
- `V0703`: The narrative outcome is IV Liquid, not fitting any of the discharge-oriented taxonomy categories.
- `V0705`: The narrative ends in Return ER after an initial Release A, falling outside the target discharge goal alternatives.
- `V0707`: The process terminates at Admission NC without a final discharge outcome matching the categories.
- `V0708`: The process concludes with IV Antibiotics rather than a discharge pathway.
- `V0712`: The narrative ends in Return ER after Release A, which is not captured by the specific release pathway definitions.
- `V0713`: The process terminates with IV Antibiotics and does not reach a discharge category.
- `V0719`: The narrative ends in Return ER following Release A, outside the core categories.
- `V0720`: The narrative results in a Return ER after Release A, not fitting the direct pathway categories.
- `V0721`: The process results in Return ER following Release A, thus not fitting the primary release categories.
- `V0724`: The narrative ends in Return ER after Release A, which is outside the modeled pathways.
- `V0742`: The process terminates at LacticAcid instead of a discharge or release event, so it does not fit any release category.
- `V0750`: Terminates at IV Antibiotics without reaching any discharge or release event, failing to match any release taxonomy category.
- `V0759`: The narrative terminates at IV Antibiotics without reaching any discharge or release phase, so it does not fit the release categories.
- `V0764`: The process stops at ER Sepsis Triage and does not complete an admission or discharge pathway.
- `V0772`: The sequence terminates at CRP during ongoing treatment without reaching any release or discharge activity.
- `V0774`: Incomplete process ending at ER Sepsis Triage, with no admission or discharge present.
- `V0775`: The variant ends at CRP during the diagnostic phase and does not reach any discharge milestone.
- `V0777`: The variant ends with Leucocytes and does not reach any discharge or release pathway.
- `V0778`: The variant terminates at Leucocytes without completing a discharge or release activity.
- `V0779`: The variant concludes with Return ER after an initial Release A, which does not fit standard successful discharge pathways.
- `V0785`: Although it passes through Release A, the variant ultimately ends with Return ER.
- `V0787`: The variant results in a Return ER outcome after Release A.
- `V0791`: The narrative stops at IV Antibiotics and does not reach a discharge pathway.
- `V0794`: The variant ultimately terminates with Return ER.
- `V0797`: The variant ends with Return ER after an intermediate Release A.
- `V0798`: The narrative ultimately terminates with Return ER.
- `V0804`: The narrative involves a return to the ER after Release A, which does not cleanly fit any of the exclusive single-path discharge definitions in the taxonomy.
- `V0806`: The variant ends with Return ER after Release A, placing it outside the standard categories.
- `V0808`: Ends in Return ER following Release A.
- `V0812`: Ends in Return ER after Release A.
- `V0815`: Ends with Return ER following Release A.
- `V0816`: The process terminates at IV Antibiotics without reaching a discharge or release state.
- `V0820`: The process stops at LacticAcid without any discharge outcome.
- `V0821`: Ends with Return ER following Release A.
- `V0822`: Ends with Return ER following Release A after an extended stay.
- `V0823`: Ends with Return ER following Release A.
- `V0825`: Ends with Return ER following Release A.
- `V0826`: The variant ends in Admission NC without proceeding to a recognized release pathway.
- `V0832`: The variant terminates at IV Antibiotics and does not reach any discharge category.
- `V0843`: The variant terminates in IV Liquid without completing a discharge pathway.
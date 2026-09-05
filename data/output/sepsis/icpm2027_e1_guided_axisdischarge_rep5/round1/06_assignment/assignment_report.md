# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_axisdischarge_rep5` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Release A (`release_a`)

Represents the standard discharge outcome for admitted patients, contributing to avoiding post-discharge deterioration and measured against post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release A (id=17) as observed in the narrative sample (e.g., V0008, V0065).

**Goal-model linkage:** 17 (Task): Release A

**Coverage:** macro 585/846 variants (69.1%) · micro 629/1050 cases (59.9%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.44, nearest other category `release_b` at mean distance 15.09

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.347, nearest other category `release_d` at mean distance 0.444

## Release B (`release_b`)

Represents an alternative discharge path for admitted cases, contributing to avoiding post-discharge deterioration and measured against post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release B (id=18) as observed in the narrative sample (e.g., V0068, V0145).

**Goal-model linkage:** 18 (Task): Release B

**Coverage:** macro 55/846 variants (6.5%) · micro 56/1050 cases (5.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 16.61, nearest other category `release_a` at mean distance 15.09

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.248, nearest other category `release_d` at mean distance 0.546

## Release C (`release_c`)

Represents an alternative discharge outcome for complex or long-stay admitted cases, measured against post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release C (id=19) as observed in long-duration variants like V0710.

**Goal-model linkage:** 19 (Task): Release C

**Coverage:** macro 24/846 variants (2.8%) · micro 24/1050 cases (2.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 23.33, nearest other category `release_a` at mean distance 18.51

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.255, nearest other category `release_d` at mean distance 0.436

## Release D (`release_d`)

Represents an alternative discharge outcome for admitted patients, measured against post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release D (id=20) as observed in the narrative sample (e.g., V0273).

**Goal-model linkage:** 20 (Task): Release D

**Coverage:** macro 24/846 variants (2.8%) · micro 24/1050 cases (2.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 19.12, nearest other category `release_a` at mean distance 17.09

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.300, nearest other category `release_c` at mean distance 0.436

## Release E (`release_e`)

Represents an alternative discharge path for admitted cases, measured against post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative Release E (id=21) per goal model decomposition.

**Goal-model linkage:** 21 (Task): Release E

**Coverage:** macro 6/846 variants (0.7%) · micro 6/1050 cases (0.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 17.67, nearest other category `release_a` at mean distance 16.40

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.253, nearest other category `release_d` at mean distance 0.440

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

152/846 variants (18.0%), 311/1050 cases (29.6%) unassigned.

- `V0001`: This narrative ends in ER Sepsis Triage without an admission or discharge outcome corresponding to the categories.
- `V0002`: This narrative ends with CRP during the ER phase and does not represent a final patient discharge path.
- `V0003`: This narrative ends with Leucocytes in the ER and does not reach a discharge outcome.
- `V0004`: This narrative concludes with IV Antibiotics administered in the ER and does not represent an admission or discharge category.
- `V0005`: This narrative ends with LacticAcid during the ER phase and is not a discharge path.
- `V0006`: This narrative ends with IV Antibiotics in the ER, with no subsequent admission or release recorded.
- `V0007`: This narrative terminates with IV Antibiotics in the ER and does not involve any patient release or admission category.
- `V0009`: This narrative stops at IV Antibiotics in the ER without reaching an admission or release outcome.
- `V0010`: This narrative ends in ER Sepsis Triage and does not represent an admission or discharge path.
- `V0011`: This narrative concludes with IV Antibiotics in the ER and lacks a discharge outcome.
- `V0012`: This narrative ends with IV Antibiotics in the ER, prior to any admission or release phase.
- `V0013`: This narrative ends with Leucocytes in the ER and does not correspond to a discharge category.
- `V0017`: This narrative terminates with ER Sepsis Triage and does not contain an admission or discharge outcome.
- `V0019`: This narrative ends with IV Antibiotics in the ER and does not reach a release outcome.
- `V0020`: This narrative concludes with CRP in the ER and does not represent an admission or release pathway.
- `V0021`: Although this variant includes Release A, it ultimately results in a Return ER outcome, leaving it outside the simple discharge categories.
- `V0023`: Although this narrative includes Release A, the final outcome is Return ER, making it fall outside the standard discharge category scope.
- `V0024`: This narrative ends with Admission NC and does not reach a final release or discharge outcome.
- `V0025`: This narrative ends with IV Antibiotics in the ER without proceeding to an admission or discharge category.
- `V0027`: The narrative ends with IV Antibiotics and does not reach a discharge outcome category.
- `V0029`: The narrative terminates at Leucocytes without reaching a discharge outcome.
- `V0031`: The narrative ends at LacticAcid and does not represent a discharge outcome.
- `V0034`: The narrative ends with IV Liquid and does not reach a discharge category.
- `V0036`: The narrative terminates at CRP without a discharge outcome.
- `V0038`: The narrative ends with IV Antibiotics and does not reach a discharge outcome.
- `V0040`: The narrative terminates at Admission NC without reaching a final discharge event.
- `V0043`: The narrative ends at LacticAcid and has no discharge outcome.
- `V0050`: The narrative terminates at CRP without reaching a discharge outcome.
- `V0056`: The narrative ends with IV Antibiotics and does not reach any discharge outcome.
- `V0062`: The outcome is IV Antibiotics with no discharge activity present.
- `V0081`: The narrative outcome is IV Liquid, which is not a discharge outcome matching any defined release category.
- `V0088`: The narrative outcome is IV Antibiotics, which does not match any discharge release category.
- `V0092`: The narrative outcome is LacticAcid, which does not correspond to a discharge outcome category.
- `V0111`: The narrative ends with Admission NC and does not reach any discharge outcome category.
- `V0127`: The process variant ends with LacticAcid and does not reach any discharge outcome.
- `V0132`: The variant stops at IV Antibiotics and does not reach a discharge category.
- `V0133`: The variant ends with IV Antibiotics and does not reach a discharge outcome.
- `V0137`: The variant finishes at LacticAcid without achieving any discharge outcome.
- `V0146`: The process variant ends with Leucocytes and lacks a discharge outcome.
- `V0148`: The variant ends with IV Antibiotics and does not reach a discharge category.
- `V0187`: The narrative terminates at CRP without reaching a discharge or release outcome.
- `V0197`: The narrative terminates at Leucocytes without reaching a discharge or release outcome.
- `V0217`: The outcome is IV Antibiotics, which does not represent any of the discharge categories.
- `V0219`: The outcome is Leucocytes, which does not represent any of the discharge categories.
- `V0232`: The narrative ends with IV Antibiotics and does not reach a discharge outcome, so no release category fits.
- `V0234`: The narrative terminates at Leucocytes without reaching a discharge outcome, meaning no category fits.
- `V0260`: The variant ends with IV Antibiotics and does not reach any discharge outcome category.
- `V0268`: The variant terminates at Leucocytes without reaching a discharge destination.
- `V0287`: The narrative ends with CRP and does not reach any discharge outcome.
- `V0292`: The narrative stops at Leucocytes and does not reach any discharge category.
- `V0295`: The narrative ends with IV Antibiotics and does not reach a discharge outcome.
- `V0302`: The variant ends at ER Sepsis Triage without an admission or discharge outcome.
- `V0305`: The process terminates at IV Antibiotics in the ER phase without reaching any discharge category.
- `V0322`: The process ends at IV Antibiotics without reaching a discharge category.
- `V0325`: The process terminates at IV Antibiotics without any discharge outcome.
- `V0330`: The narrative outcome is IV Liquid, which does not correspond to any discharge category in the taxonomy.
- `V0336`: The narrative outcome is CRP, which is a diagnostic activity rather than a discharge outcome.
- `V0342`: The narrative outcome is CRP, which does not correspond to any discharge category.
- `V0349`: The narrative outcome is ER Sepsis Triage, which is not a discharge outcome.
- `V0365`: The narrative ends with Leucocytes and does not reach any of the specified release categories.
- `V0368`: The narrative terminates at Admission NC and does not reach any of the specified release categories.
- `V0374`: The narrative terminates at Leucocytes and does not reach any of the specified release categories.
- `V0378`: The narrative outcome is IV Antibiotics, which does not correspond to any discharge category.
- `V0379`: The narrative outcome is IV Antibiotics, which does not correspond to any discharge category.
- `V0382`: The narrative outcome is Return ER following Release A, which does not fit the target categories.
- `V0385`: The narrative outcome is Return ER, which does not fit the taxonomy discharge outcomes.
- `V0386`: The narrative outcome is Return ER, which does not fit the taxonomy discharge outcomes.
- `V0398`: The narrative outcome is Return ER, which does not fit the taxonomy discharge outcomes.
- `V0415`: The outcome is Admission NC, which does not map to any of the release categories.
- `V0417`: The outcome is ER Triage rather than any final discharge category.
- `V0429`: The outcome is IV Antibiotics, which does not fit any standard discharge outcome category.
- `V0462`: The narrative ends with CRP instead of any standard or alternative release outcome.
- `V0488`: The process terminates at IV Liquid without reaching a discharge category.
- `V0492`: The process terminates at IV Liquid without reaching a discharge category.
- `V0495`: The process terminates at IV Antibiotics without reaching a discharge category.
- `V0501`: The process terminates with IV Liquid, which does not represent any of the discharge outcome categories.
- `V0502`: The variant ends with Admission NC and does not reach a discharge category.
- `V0504`: The variant ends with Return ER after Release A, representing a post-discharge ER return rather than a clean release outcome.
- `V0505`: The variant terminates with Return ER, which indicates a post-discharge ER return.
- `V0507`: The process ends with IV Antibiotics and does not reach a discharge outcome.
- `V0508`: The narrative ends with Return ER following Release A, representing a readmission/ER return case.
- `V0510`: The process concludes at IV Antibiotics without a discharge outcome.
- `V0515`: The narrative ends with Return ER, representing a post-discharge ER return.
- `V0516`: The process terminates with Leucocytes and does not reach any discharge outcome category.
- `V0517`: The process ends prematurely at ER Triage without reaching a discharge outcome.
- `V0519`: The narrative terminates with Return ER, indicating a post-discharge ER return.
- `V0520`: The variant ends with Return ER after Release A, representing a post-discharge ER return.
- `V0549`: The narrative ends with IV Liquid and does not reach any discharge category.
- `V0556`: The outcome is Return ER after a temporary Release A, which does not map cleanly to standard discharge tracking categories.
- `V0558`: The narrative results in Return ER after Release A.
- `V0559`: The narrative results in Return ER after Release A.
- `V0560`: The narrative results in Return ER after Release A.
- `V0564`: The narrative results in Return ER following initial discharge.
- `V0565`: The narrative ends with Admission NC and does not reach a discharge outcome.
- `V0567`: The narrative results in Return ER following initial discharge.
- `V0573`: The narrative results in Return ER following discharge.
- `V0575`: The narrative terminates early at Leucocytes without reaching a valid discharge or admission category.
- `V0580`: The narrative does not culminate in any discharge outcome, ending instead with CRP checks.
- `V0584`: The sequence stops at IV Liquid without reaching a discharge destination.
- `V0585`: The process terminates at LacticAcid without any discharge event.
- `V0587`: The process finishes with a CRP test and lacks a discharge outcome.
- `V0592`: The process ends at IV Antibiotics without reaching a discharge category.
- `V0605`: Although it features Release A initially, the ultimate outcome is Return ER after a very long duration, so standard release categories do not adequately capture the long-term post-discharge return trajectory here.
- `V0614`: Although it contains Release A, the case results in Return ER, making it fall into the residual.
- `V0615`: Though Release C is present, the final outcome is Return ER after a prolonged duration, rendering standard release categorization unfitting.
- `V0625`: Despite the intermediate Release A, the case culminates in Return ER, falling outside successful release categories.
- `V0636`: The narrative ends with LacticAcid rather than a discharge outcome, so it does not fit any release category.
- `V0644`: The narrative ends with CRP rather than a discharge outcome, failing to match any release category.
- `V0645`: The narrative ends with LacticAcid instead of a discharge event.
- `V0654`: The process outcome is Leucocytes rather than any discharge category.
- `V0663`: The process ends at Admission NC, with no discharge outcome reached.
- `V0664`: The process terminates at IV Liquid and does not reach a discharge category.
- `V0670`: The final activity is Leucocytes following an interim Release A and return.
- `V0676`: The narrative ends with IV Antibiotics and does not reach a discharge outcome.
- `V0679`: The narrative terminates at IV Antibiotics without a discharge outcome.
- `V0685`: The variant terminates at IV Antibiotics and does not show any discharge activity.
- `V0689`: The narrative ends with IV Antibiotics without reaching a discharge state.
- `V0694`: The narrative ends at ER Sepsis Triage and does not reach a discharge outcome.
- `V0703`: The outcome is IV Liquid, which does not match any discharge category in the taxonomy.
- `V0705`: Although it features a release, the final outcome is Return ER, and the taxonomy focuses on discharge pathways and post-discharge ER returns rather than matching this sequence.
- `V0707`: The outcome is Admission NC, which is not a discharge category.
- `V0708`: The outcome is IV Antibiotics, which is not a discharge category.
- `V0712`: The final outcome is Return ER after a temporary Release A, making it part of the residual.
- `V0713`: The outcome is IV Antibiotics, which is not a discharge category.
- `V0719`: The final outcome is Return ER following an intermediate Release A, falling into the residual.
- `V0720`: The final outcome is Return ER following an intermediate Release A, placing it in the residual.
- `V0721`: The final outcome is Return ER after an intermediate Release A, which does not cleanly map to a single direct discharge category.
- `V0724`: The ultimate outcome is Return ER after an intermediate Release A, placing it in the residual category.
- `V0742`: The narrative outcome is LacticAcid, which does not match any of the release categories.
- `V0750`: The narrative outcome is IV Antibiotics, which does not map to any discharge release category.
- `V0759`: The narrative terminates at IV Antibiotics without reaching a discharge or release outcome.
- `V0764`: The process narrative terminates at ER Sepsis Triage and does not reach any release or discharge outcome.
- `V0772`: The process variant terminates at CRP measurement and does not achieve a release or discharge outcome.
- `V0774`: The process narrative stops at ER Sepsis Triage without reaching any discharge outcome.
- `V0775`: The narrative ends with a CRP lab test and does not reach a release or discharge outcome.
- `V0777`: The narrative ends with Leucocytes and does not culminate in any discharge category.
- `V0778`: The narrative ends with Leucocytes and lacks any discharge outcome.
- `V0791`: The narrative ends with IV Antibiotics and contains no discharge event.
- `V0804`: The outcome is Return ER following Release A, which does not map cleanly into the standard category definitions as a final outcome state for this trajectory.
- `V0806`: The outcome is Return ER after a Release A event, which is part of the post-discharge measurement rather than a primary category realization.
- `V0808`: The narrative ends with Return ER after Release A.
- `V0812`: The narrative ends with Return ER following Release A.
- `V0815`: The narrative ends with Return ER after Release A.
- `V0816`: The process terminates at IV Antibiotics without reaching any discharge outcome.
- `V0820`: The process terminates at LacticAcid without reaching any discharge outcome.
- `V0821`: The narrative ends with Return ER after Release A.
- `V0822`: The narrative ends with Return ER following a Release A outcome.
- `V0823`: The narrative ends with Return ER following Release A.
- `V0825`: The narrative ends with Return ER following Release A.
- `V0826`: The outcome is Admission NC, which does not represent any of the discharge categories (Release A through E).
- `V0832`: The outcome is IV Antibiotics, which is not a discharge category.
- `V0843`: The outcome is IV Liquid, which is not a discharge category.
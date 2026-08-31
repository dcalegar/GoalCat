# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_axisdischarge_rep3` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Release A (`release_a`)

Represents the standard discharge pathway for patients after successful treatment and ward admission, contributing to avoiding post-discharge deterioration and measured against post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release A (id=17) under the discharge goal decomposition (id=6). Supported by frequent variants like V0008, V0070, and V0069.

**Goal-model linkage:** 17 (Task): Release A

**Coverage:** macro 581/846 variants (68.7%) · micro 629/1050 cases (59.9%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.27, nearest other category `release_b` at mean distance 15.02

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.343, nearest other category `release_d` at mean distance 0.443

## Release B (`release_b`)

Represents an alternative discharge pathway following ward treatment, contributing to avoiding post-discharge deterioration and measured against post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release B (id=18) under the discharge goal decomposition (id=6). Supported by rare/alternative variants such as V0068 and V0145.

**Goal-model linkage:** 18 (Task): Release B

**Coverage:** macro 55/846 variants (6.5%) · micro 56/1050 cases (5.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 16.61, nearest other category `release_a` at mean distance 15.02

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.248, nearest other category `release_d` at mean distance 0.546

## Release C (`release_c`)

Represents a specific discharge route for long-stay or complex admitted patients, measured against post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release C (id=19) under the discharge goal decomposition (id=6), observed in long complex cases such as V0710.

**Goal-model linkage:** 19 (Task): Release C

**Coverage:** macro 24/846 variants (2.8%) · micro 24/1050 cases (2.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 23.33, nearest other category `release_a` at mean distance 18.43

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.255, nearest other category `release_d` at mean distance 0.436

## Release D (`release_d`)

Represents a distinct discharge pathway for admitted cases, measured against post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release D (id=20) under the discharge goal decomposition (id=6), evidenced in sample variant V0273.

**Goal-model linkage:** 20 (Task): Release D

**Coverage:** macro 24/846 variants (2.8%) · micro 24/1050 cases (2.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 19.12, nearest other category `release_a` at mean distance 17.03

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.300, nearest other category `release_c` at mean distance 0.436

## Release E (`release_e`)

Represents an alternative discharge pathway under the mutually exclusive discharge goal decomposition.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Release E (id=21) under the discharge goal decomposition (id=6). Maintained as a distinct category per the XOR constraint even without high representation in the current sample.

**Goal-model linkage:** 21 (Task): Release E

**Coverage:** macro 6/846 variants (0.7%) · micro 6/1050 cases (0.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 17.67, nearest other category `release_a` at mean distance 16.34

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

156/846 variants (18.4%), 311/1050 cases (29.6%) unassigned.

- `V0001`: This variant ends in ER Sepsis Triage and does not represent a discharge pathway from ward admission.
- `V0002`: This variant terminates at CRP testing in the ER and does not reach ward admission or discharge.
- `V0003`: This variant terminates at Leucocytes testing in the ER and does not represent a discharge pathway.
- `V0004`: This variant ends with IV Antibiotics administration in the ER and lacks ward admission or discharge.
- `V0005`: This variant terminates at LacticAcid testing in the ER and does not involve ward admission.
- `V0006`: This variant concludes with IV Antibiotics in the ER without proceeding to admission or discharge.
- `V0007`: This variant concludes with IV Antibiotics in the ER and does not include ward admission or discharge.
- `V0009`: This variant ends with IV Antibiotics in the ER and does not reach ward admission or discharge.
- `V0010`: This variant ends with ER Sepsis Triage and does not represent a ward discharge pathway.
- `V0011`: This variant terminates at IV Antibiotics in the ER without reaching ward admission or discharge.
- `V0012`: This variant ends with IV Antibiotics in the ER and has no ward admission or discharge activity.
- `V0013`: This variant ends with Leucocytes testing in the ER and does not involve ward admission.
- `V0017`: This variant concludes at ER Sepsis Triage and does not reach ward admission or discharge.
- `V0019`: This variant ends with IV Antibiotics in the ER and does not involve ward admission or discharge.
- `V0020`: This variant terminates at CRP testing in the ER without reaching ward admission or discharge.
- `V0024`: This variant terminates at Admission NC without reaching any discharge outcome.
- `V0025`: This variant concludes with IV Antibiotics in the ER and does not reach ward admission or discharge.
- `V0027`: This variant ends with IV Antibiotics in the ER and lacks ward admission or discharge.
- `V0029`: This variant ends with Leucocytes testing in the ER and does not reach ward admission or discharge.
- `V0031`: This variant terminates at LacticAcid testing in the ER without ward admission or discharge.
- `V0034`: This variant concludes with IV Liquid in the ER and does not reach ward admission or discharge.
- `V0036`: This variant terminates at CRP testing in the ER without ward admission or discharge.
- `V0038`: This variant ends with IV Antibiotics in the ER and does not reach ward admission or discharge.
- `V0040`: This variant terminates at Admission NC without reaching any discharge outcome.
- `V0043`: This variant terminates at LacticAcid testing in the ER without reaching ward admission or discharge.
- `V0050`: This variant terminates at CRP testing in the ER without reaching ward admission or discharge.
- `V0056`: The process terminates at IV Antibiotics without reaching a discharge pathway.
- `V0062`: Stops at IV Antibiotics without a final discharge outcome.
- `V0081`: Terminates at IV Liquid without reaching a discharge category.
- `V0088`: Terminates at IV Antibiotics without reaching a discharge goal.
- `V0092`: Terminates at LacticAcid without completing a discharge pathway.
- `V0111`: The narrative ends at Admission NC without reaching any discharge activity.
- `V0127`: The process stops at LacticAcid without reaching any discharge category.
- `V0132`: The process terminates at IV Antibiotics without reaching a discharge pathway.
- `V0133`: The narrative stops at IV Antibiotics in the emergency phase.
- `V0137`: The process ends during diagnostics at LacticAcid.
- `V0146`: The process terminates prematurely at Leucocytes.
- `V0148`: The narrative stops at IV Antibiotics in the ER phase.
- `V0181`: The narrative ends with Leucocytes and does not culminate in any recognized discharge category.
- `V0187`: The narrative terminates at CRP without reaching any discharge or release phase.
- `V0197`: The narrative ends at Leucocytes and does not contain any release or discharge category.
- `V0217`: The narrative terminates at IV Antibiotics inside the ER without proceeding to an admission or discharge pathway category.
- `V0219`: The narrative terminates during diagnostic workup in the ER without reaching a discharge category.
- `V0232`: The narrative terminates at IV Antibiotics in the ER without reaching any discharge category.
- `V0234`: The narrative terminates at Leucocytes in the ER without reaching an admission or discharge category.
- `V0260`: The process terminates at IV Antibiotics without reaching any discharge pathway.
- `V0268`: The process terminates at Leucocytes without reaching a discharge category.
- `V0287`: The process terminates at CRP without reaching any discharge pathway.
- `V0292`: The process terminates at Leucocytes without reaching a discharge category.
- `V0295`: The process terminates at IV Antibiotics without reaching a discharge pathway.
- `V0302`: The process terminates at ER Sepsis Triage and does not reach any discharge or ward release pathway.
- `V0305`: The narrative stops at IV Antibiotics inside the emergency setting without reaching a discharge destination.
- `V0322`: The process terminates at IV Antibiotics within the emergency phase.
- `V0325`: The case ends at IV Antibiotics in the ER without reaching a discharge category.
- `V0330`: The process stops at IV Liquid in the emergency unit and does not reach a discharge category.
- `V0336`: The variant ends on a diagnostic CRP test while still in the hospital, without reaching discharge.
- `V0342`: The sequence stops at a CRP measurement in the ER without reaching any discharge pathway.
- `V0349`: The process terminates at ER Sepsis Triage and does not proceed to admission or discharge.
- `V0365`: The narrative does not conclude with a release activity, ending instead on diagnostic lab work.
- `V0368`: The process terminates immediately upon Admission NC without any release outcome.
- `V0374`: Terminates on a diagnostic test rather than a discharge category.
- `V0378`: Stops at IV Antibiotics without reaching a discharge destination.
- `V0379`: Ends at IV Antibiotics without a final release outcome.
- `V0415`: The narrative ends with Admission NC and does not reach any discharge category.
- `V0417`: The process terminates at ER Triage without reaching any discharge pathway.
- `V0429`: The process halts at IV Antibiotics and does not reach a discharge category.
- `V0462`: The narrative ends with CRP instead of any discharge category.
- `V0488`: The narrative terminates at IV Liquid without reaching a discharge category.
- `V0492`: The process ends at IV Liquid and does not reach a discharge category.
- `V0495`: The narrative ends at IV Antibiotics and does not reach a discharge category.
- `V0501`: The narrative ends with IV Liquid and does not reach any discharge pathway category.
- `V0502`: The narrative ends with Admission NC and does not reach any discharge pathway category.
- `V0507`: The narrative stops at IV Antibiotics without completing a discharge pathway.
- `V0510`: The narrative terminates with IV Antibiotics and lacks a discharge activity.
- `V0516`: The narrative ends with Leucocytes and does not reach a discharge pathway.
- `V0517`: The narrative ends with ER Triage and does not reach a discharge pathway.
- `V0549`: The narrative ends with IV Liquid and does not reach a discharge category.
- `V0556`: The outcome is Return ER rather than a recognized discharge category from the taxonomy.
- `V0558`: The outcome is Return ER, which does not fit any of the discharge release categories.
- `V0559`: The outcome is Return ER, making it part of the residual category.
- `V0560`: The outcome is Return ER, falling outside the defined release pathways.
- `V0564`: The outcome is Return ER after a brief release, fitting the residual category.
- `V0565`: The process terminates at Admission NC without a formal release or categorized pathway.
- `V0567`: The final outcome is Return ER, which does not map to any of the taxonomy release categories.
- `V0573`: The final outcome is Return ER, placing it in the residual.
- `V0575`: The process ends prematurely at Leucocytes without reaching a discharge destination.
- `V0577`: The final outcome is Return ER, falling outside the taxonomy categories.
- `V0578`: The outcome is Return ER, making it part of the residual.
- `V0579`: The outcome is Return ER, which is not covered by the release categories.
- `V0580`: The process terminates at CRP without a discharge outcome.
- `V0584`: The process stops at IV Liquid without a discharge pathway.
- `V0585`: The process stops at LacticAcid without reaching a discharge destination.
- `V0587`: The process terminates at CRP without a release outcome.
- `V0590`: The outcome is Return ER, falling into the residual category.
- `V0591`: The outcome is Return ER after Release A, but the primary classification for such return paths is residual.
- `V0592`: The process stops at IV Antibiotics without reaching a discharge destination.
- `V0595`: The outcome is Return ER, which does not map to any defined taxonomy category.
- `V0605`: The narrative outcomes in Return ER, which indicates a post-discharge ER return rather than successfully realizing a standard release category goal without deterioration.
- `V0614`: The narrative outcomes in Return ER, indicating a post-discharge ER return after the initial Release A.
- `V0615`: The narrative outcomes in Return ER following Release C, thus failing to avoid post-discharge deterioration.
- `V0625`: The narrative outcomes in Return ER after Release A.
- `V0627`: The narrative outcomes in Return ER following Release A.
- `V0631`: The narrative outcomes in Return ER following Release A.
- `V0632`: The narrative outcomes in Return ER following Release A.
- `V0635`: The narrative outcomes in Return ER following Release A.
- `V0636`: The narrative ends without any discharge or release activity, terminating at LacticAcid.
- `V0638`: The narrative outcomes in Return ER following Release A.
- `V0639`: The narrative outcomes in Return ER following Release A.
- `V0640`: The narrative outcomes in Return ER following Release A.
- `V0641`: The narrative outcomes in Return ER following Release A.
- `V0643`: The narrative outcomes in Return ER following Release A.
- `V0644`: The narrative terminates at CRP without any release or discharge activity.
- `V0645`: The narrative terminates at LacticAcid without any release or discharge activity.
- `V0646`: The narrative outcomes in Return ER after going through Release A and additional tests.
- `V0649`: The narrative outcomes in Return ER following Release A.
- `V0650`: The narrative outcomes in Return ER following Release A.
- `V0654`: The process terminates at Leucocytes without reaching any discharge pathway.
- `V0663`: The narrative ends at Admission NC and does not reach a discharge pathway.
- `V0664`: The narrative terminates at IV Liquid without reaching discharge.
- `V0676`: The trace ends at IV Antibiotics without reaching a discharge category.
- `V0679`: The process terminates at IV Antibiotics without reaching discharge.
- `V0685`: The process ends at IV Antibiotics without reaching a discharge pathway.
- `V0689`: The process terminates at IV Antibiotics without reaching a discharge pathway.
- `V0694`: The process ends at ER Sepsis Triage without reaching discharge.
- `V0703`: The narrative does not conclude with a discharge outcome, ending in IV Liquid instead.
- `V0707`: The process terminates at Admission NC without reaching a discharge category.
- `V0708`: The process terminates at IV Antibiotics without reaching a discharge category.
- `V0713`: The process terminates at IV Antibiotics without reaching a discharge category.
- `V0742`: The process terminates at LacticAcid without reaching a discharge category.
- `V0750`: The process terminates at IV Antibiotics without reaching a discharge category.
- `V0759`: The narrative terminates at IV Antibiotics and does not reach any discharge or release activity.
- `V0764`: The narrative terminates at ER Sepsis Triage and does not proceed to discharge.
- `V0772`: The narrative ends at CRP without reaching a discharge or release category.
- `V0774`: The narrative ends at ER Sepsis Triage and does not progress to any release phase.
- `V0775`: The narrative terminates at CRP and does not include a discharge activity.
- `V0777`: The narrative stops at Leucocytes without reaching a release pathway.
- `V0778`: The narrative concludes with Leucocytes and lacks any discharge event.
- `V0791`: The narrative terminates at IV Antibiotics without reaching a discharge destination.
- `V0804`: The outcome is Return ER rather than a standard final discharge category from the taxonomy.
- `V0806`: The outcome is Return ER, so it does not conclude as a taxonomy release category.
- `V0808`: The final outcome is Return ER after Release A, which falls outside the primary successful discharge categories.
- `V0812`: The final outcome is Return ER.
- `V0815`: The final outcome is Return ER.
- `V0816`: The process terminates at IV Antibiotics without reaching a discharge category.
- `V0820`: The process terminates at LacticAcid without completing a discharge pathway.
- `V0821`: The outcome is Return ER following Release A.
- `V0822`: The final outcome is Return ER.
- `V0823`: The final outcome is Return ER.
- `V0825`: The final outcome is Return ER.
- `V0826`: The process terminates at Admission NC without reaching a release category.
- `V0827`: The final outcome is Return ER.
- `V0828`: The final outcome is Return ER.
- `V0832`: The process terminates at IV Antibiotics without reaching a discharge pathway.
- `V0834`: The final outcome is Return ER.
- `V0842`: The final outcome is Return ER.
- `V0843`: The process terminates at IV Liquid without reaching a discharge pathway.
# Step 6 — Narrative assignment report

Run: `20260828_182820` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Admission to Normal Care (`admission_nc`)

Patient is admitted to a normal care inpatient ward (Admission NC), advancing treatment goals but subject to normal ward management and discharge pathways.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative id=15 under the OR-decomposed Patient is admitted to an inpatient ward goal. The sample shows this alternative realized in numerous variants (e.g., V0008, V0065).

**Goal-model linkage:** 15 (Task): Admission NC

**Coverage:** macro 85/846 variants (10.0%) · micro 98/1050 cases (9.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 7.53, nearest other category `release_a` at mean distance 10.05

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.454, nearest other category `release_a` at mean distance 0.411

## Admission to Intensive Care (`admission_ic`)

Patient is admitted to an intensive care inpatient ward (Admission IC). This option incurs some negative impact on minimizing time-to-treatment due to transfer overhead, but is required for critical stabilization.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative id=16 under the OR-decomposed Patient is admitted to an inpatient ward goal, contributing negatively to minimize time-to-treatment softgoal as specified in the goal model and observed in variants such as V0068 and V0605.

**Goal-model linkage:** 16 (Task): Admission IC

**Coverage:** macro 11/846 variants (1.3%) · micro 11/1050 cases (1.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 13.67, nearest other category `admission_nc` at mean distance 12.97

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.407, nearest other category `release_a` at mean distance 0.435

## Release Pathway A (`release_a`)

Captured discharge representing standard release pathway A, helping to avoid post-discharge deterioration.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative id=17 under the OR-decomposed Admitted case reaches a captured discharge goal. Evidenced by multiple sample variants such as V0008 and V0069.

**Goal-model linkage:** 17 (Task): Release A

**Coverage:** macro 487/846 variants (57.6%) · micro 525/1050 cases (50.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.76, nearest other category `admission_nc` at mean distance 10.05

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.336, nearest other category `admission_nc` at mean distance 0.411

## Release Pathway B (`release_b`)

Captured discharge representing release pathway B, helping to avoid post-discharge deterioration.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative id=18 under the OR-decomposed Admitted case reaches a captured discharge goal, supported by sample traces like V0068 and V0145.

**Goal-model linkage:** 18 (Task): Release B

**Coverage:** macro 53/846 variants (6.3%) · micro 54/1050 cases (5.1%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 16.78, nearest other category `admission_nc` at mean distance 13.71

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.232, nearest other category `admission_ic` at mean distance 0.539

## Release Pathway C (`release_c`)

Captured discharge representing release pathway C for specific patient recovery profiles.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative id=19 under the OR-decomposed Admitted case reaches a captured discharge goal, observed in long-duration variants such as V0710.

**Goal-model linkage:** 19 (Task): Release C

**Coverage:** macro 23/846 variants (2.7%) · micro 23/1050 cases (2.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 23.86, nearest other category `admission_nc` at mean distance 17.56

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.242, nearest other category `release_d` at mean distance 0.443

## Release Pathway D (`release_d`)

Captured discharge representing release pathway D.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative id=20 under the OR-decomposed Admitted case reaches a captured discharge goal, evidenced in complex variants like V0273.

**Goal-model linkage:** 20 (Task): Release D

**Coverage:** macro 23/846 variants (2.7%) · micro 23/1050 cases (2.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 19.60, nearest other category `admission_nc` at mean distance 16.85

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.296, nearest other category `release_e` at mean distance 0.441

## Release Pathway E (`release_e`)

Captured discharge representing release pathway E.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative id=21 under the OR-decomposed Admitted case reaches a captured discharge goal.

**Goal-model linkage:** 21 (Task): Release E

**Coverage:** macro 6/846 variants (0.7%) · micro 6/1050 cases (0.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 17.67, nearest other category `admission_nc` at mean distance 16.01

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.253, nearest other category `release_d` at mean distance 0.441

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

- `V0008` (`release_a`) / `V0058` (`admission_nc`): structural=1, profile=0.011
- `V0008` (`release_a`) / `V0707` (`admission_nc`): structural=1, profile=0.425
- `V0014` (`release_a`) / `V0058` (`admission_nc`): structural=1, profile=0.015
- `V0016` (`release_a`) / `V0052` (`admission_nc`): structural=1, profile=0.429
- `V0018` (`release_a`) / `V0096` (`admission_nc`): structural=1, profile=0.342
- `V0022` (`release_a`) / `V0274` (`release_c`): structural=1, profile=0.374
- `V0022` (`release_a`) / `V0415` (`admission_nc`): structural=1, profile=0.428
- `V0026` (`release_a`) / `V0052` (`admission_nc`): structural=1, profile=0.219
- `V0028` (`release_a`) / `V0100` (`admission_nc`): structural=1, profile=0.420
- `V0033` (`release_a`) / `V0054` (`admission_nc`): structural=1, profile=0.210

## Residual

158/846 variants (18.7%), 310/1050 cases (29.5%) unassigned.

- `V0001`: The narrative ends in ER Sepsis Triage and does not reach any admission or release pathway.
- `V0002`: The narrative terminates at CRP testing without any subsequent admission or discharge events.
- `V0003`: The narrative stops at Leucocytes blood test without an inpatient admission or release pathway.
- `V0004`: The patient receives IV Antibiotics in the ER but is not admitted or discharged within this sequence.
- `V0005`: The narrative ends with LacticAcid testing without progressing to admission or release.
- `V0006`: The patient receives IV antibiotics in the emergency setting but the process variant ends there.
- `V0007`: The process variant concludes after administering IV antibiotics in the ER without an admission or release event.
- `V0009`: The variant ends with IV Antibiotics administration in the ER without reaching an admission or release category.
- `V0010`: The narrative ends at ER Sepsis Triage and lacks any admission or release endpoint.
- `V0011`: The process concludes following IV Antibiotics in the ER without proceeding to admission or release.
- `V0012`: The sequence stops at IV Antibiotics without an inpatient admission or discharge category.
- `V0013`: The narrative terminates at Leucocytes evaluation without reaching any of the target categories.
- `V0017`: The trace stops at ER Sepsis Triage without any admission or release pathway.
- `V0019`: The narrative ends at IV Antibiotics in the emergency department without reaching admission or release.
- `V0020`: The process variant terminates at CRP testing in the ER.
- `V0025`: The sequence ends with IV Antibiotics in the emergency setting without an admission or release event.
- `V0027`: The narrative terminates with IV Antibiotics administered in the ER.
- `V0029`: The narrative ends with Leucocytes testing in the ER.
- `V0031`: The process variant concludes at LacticAcid testing without further inpatient progression.
- `V0034`: The variant ends with IV Liquid administration in the ER.
- `V0036`: The sequence stops at CRP testing without reaching admission or release categories.
- `V0038`: The narrative concludes with IV Antibiotics in the emergency department.
- `V0043`: The process terminates at LacticAcid testing in the ER.
- `V0050`: The narrative stops at CRP testing without an admission or release pathway.
- `V0056`: The narrative terminates at IV Antibiotics without any admission or release pathway event.
- `V0062`: The process ends at IV Antibiotics without reaching any inpatient admission or release category.
- `V0081`: The narrative stops at IV Liquid without any admission or release category.
- `V0088`: The narrative terminates at IV Antibiotics without any admission or release category.
- `V0092`: The narrative terminates at LacticAcid without any inpatient admission or release pathway.
- `V0127`: The process terminates at LacticAcid without any admission or release category being reached, rendering it part of the residual.
- `V0132`: The process ends at IV Antibiotics without reaching any ward admission or release category, falling into the residual.
- `V0133`: The narrative ends at IV Antibiotics without completing an admission or release goal, placing it in the residual.
- `V0137`: The process stops at LacticAcid without progressing to an admission or release category, belonging to the residual.
- `V0146`: The narrative terminates at Leucocytes without achieving any defined admission or release target, falling into the residual.
- `V0148`: The narrative ends at IV Antibiotics without reaching an admission or discharge goal, placing it in the residual.
- `V0187`: The variant does not reach an admission or release outcome, remaining incomplete.
- `V0197`: The variant does not reach an admission or release outcome, remaining incomplete.
- `V0217`: The process terminates at IV Antibiotics without reaching any inpatient admission or discharge category.
- `V0219`: The process terminates prematurely at Leucocytes without reaching any admission or discharge category.
- `V0232`: The process terminates at IV Antibiotics without reaching any inpatient admission or discharge category.
- `V0234`: The process terminates prematurely at Leucocytes without reaching any admission or discharge category.
- `V0260`: The process stops at IV Antibiotics without reaching any admission or release category.
- `V0287`: The process ends at CRP testing inside the ER without any admission or release.
- `V0292`: Terminates at Leucocytes testing in the ER without reaching ward admission or release.
- `V0302`: The narrative ends prematurely at ER Sepsis Triage and does not complete any admission or discharge pathway.
- `V0305`: The narrative ends at IV Antibiotics in the ER and has not reached an inpatient ward or discharge pathway.
- `V0322`: The trace stops at IV Antibiotics and does not reach admission or release categories.
- `V0325`: The narrative ends in the ER with IV Antibiotics without inpatient admission or release.
- `V0330`: The narrative terminates at IV Liquid within the ER setting.
- `V0336`: The trace stops at CRP following Admission NC without completing a discharge path.
- `V0342`: The narrative ends at CRP in the ER without reaching an admission or release pathway.
- `V0349`: The trace stops at ER Sepsis Triage without proceeding to admission or release.
- `V0378`: The process terminates at IV Antibiotics without reaching any ward admission or release category.
- `V0379`: The process ends at IV Antibiotics and does not reach any admission or release goal.
- `V0417`: The narrative loops back to ER Triage and does not complete an admission or release pathway.
- `V0429`: The process terminates at IV Antibiotics without reaching any admission or release goal.
- `V0453`: The narrative ends with Return ER after an intermediate Release A, but the final outcome is not a clean taxonomy release category.
- `V0454`: The final outcome is Return ER following Release A, meaning it does not cleanly fit the terminal release categories.
- `V0458`: The final outcome is Return ER, so it does not match any final release category.
- `V0460`: The process ends with Return ER, meaning no terminal release category applies.
- `V0462`: The final activity is CRP, meaning the case did not reach a discharge or admission decision category.
- `V0463`: The narrative ends with Return ER, falling outside the target discharge pathways.
- `V0464`: The final outcome is Return ER, so no release category is realized.
- `V0467`: The case results in Return ER, making it ineligible for the discharge taxonomy categories.
- `V0468`: The final outcome is Return ER, not a release category.
- `V0469`: The narrative terminates with Return ER, so it does not realize any discharge pathway.
- `V0473`: The outcome is Return ER, thus no release category fits.
- `V0474`: The process ends with Return ER, so no category is realized.
- `V0476`: The final outcome is Return ER, making the discharge pathway categories inapplicable.
- `V0479`: The narrative ends with Return ER, so no release category matches.
- `V0482`: The outcome is Return ER, meaning no terminal release category fits.
- `V0484`: The final event is Return ER, making any release category inappropriate.
- `V0488`: The process terminates at IV Liquid and has no admission or release category.
- `V0492`: The process stops at IV Liquid without reaching any admission or release outcome.
- `V0495`: The narrative ends with IV Antibiotics, lacking an admission or release destination.
- `V0497`: The final activity is Return ER, making it part of the residual.
- `V0507`: The patient received ER treatment and antibiotics but was neither admitted to a ward nor discharged via a known release pathway.
- `V0510`: The narrative stops at IV Antibiotics in the ER without indicating admission or formal release.
- `V0516`: The process sequence ends prematurely at Leucocytes without admission or release.
- `V0517`: The process sequence is incomplete, ending at ER Triage.
- `V0549`: The narrative ends at IV Liquid in the emergency workflow without admission or discharge.
- `V0556`: The outcome is Return ER rather than any standard admission or release category.
- `V0558`: The outcome is Return ER rather than a recognized final discharge or admission goal.
- `V0559`: The outcome is Return ER rather than a standard discharge or ward admission.
- `V0560`: The outcome is Return ER rather than a recognized release or ward pathway.
- `V0564`: The outcome is Return ER, which does not map to any admission or release categories.
- `V0567`: The outcome is Return ER rather than a valid discharge or admission pathway.
- `V0573`: The outcome is Return ER rather than a categorized release or admission.
- `V0575`: The outcome is Leucocytes test, which does not match any admission or release category.
- `V0577`: The outcome is Return ER, falling into the residual category.
- `V0578`: The outcome is Return ER, falling into the residual category.
- `V0579`: The outcome is Return ER, falling into the residual category.
- `V0580`: The outcome is CRP test, falling into the residual category.
- `V0584`: The outcome is IV Liquid, falling into the residual category.
- `V0585`: The outcome is LacticAcid, falling into the residual category.
- `V0587`: The outcome is CRP, falling into the residual category.
- `V0590`: The outcome is Return ER, falling into the residual category.
- `V0591`: The outcome is Return ER, falling into the residual category.
- `V0592`: The outcome is IV Antibiotics, falling into the residual category.
- `V0595`: The outcome is Return ER, falling into the residual category.
- `V0605`: The case results in Return ER after initial Release A, which does not cleanly map to a single stable release pathway in the taxonomy.
- `V0614`: The case results in Return ER after initial Release A, which does not fit cleanly into a terminal release category.
- `V0615`: The case results in Return ER after Release C, so it is part of the residual.
- `V0625`: The case results in Return ER after Release A, placing it in the residual.
- `V0627`: The case results in Return ER after Release A, placing it in the residual.
- `V0631`: The case results in Return ER, placing it in the residual.
- `V0632`: The case results in Return ER, placing it in the residual.
- `V0633`: The case results in Return ER after Release D, placing it in the residual.
- `V0635`: The case results in Return ER after Release A, placing it in the residual.
- `V0636`: The outcome is LacticAcid, which does not match any valid category in the taxonomy.
- `V0638`: The case results in Return ER after Release A, placing it in the residual.
- `V0639`: The case results in Return ER after Release A, placing it in the residual.
- `V0640`: The case results in Return ER after Release A, placing it in the residual.
- `V0641`: The case results in Return ER after Release A, placing it in the residual.
- `V0643`: The case results in Return ER after Release A, placing it in the residual.
- `V0644`: The outcome is CRP, which does not map to any category in the taxonomy.
- `V0645`: The outcome is LacticAcid, which does not map to any category in the taxonomy.
- `V0646`: The case results in Return ER after Release A, placing it in the residual.
- `V0649`: The case results in Return ER after Release A, placing it in the residual.
- `V0650`: The case results in Return ER after Release A, placing it in the residual.
- `V0664`: The sequence terminates at IV Liquid and does not reach any admission or release category.
- `V0670`: The sequence ends with Leucocytes following an ER return attempt, fitting none of the categories.
- `V0676`: Terminates at IV Antibiotics without reaching any ward admission or release category.
- `V0679`: Stops at IV Antibiotics without admission or release.
- `V0685`: Stops at IV Antibiotics without admission or release steps.
- `V0689`: Terminates at IV Antibiotics.
- `V0694`: Stops at ER Sepsis Triage without any admission or release outcome.
- `V0703`: The narrative ends in IV Liquid and does not reach any admission or release category.
- `V0708`: The narrative terminates at IV Antibiotics without completing an admission or discharge goal.
- `V0713`: The narrative stops at IV Antibiotics without an admission or release outcome.
- `V0742`: The process terminates at LacticAcid without completing any admission or release pathway.
- `V0750`: The narrative stops at IV Antibiotics without reaching any admission or discharge goal.
- `V0759`: The variant terminates at IV Antibiotics without any admission or discharge activities, so no category applies.
- `V0764`: The variant stops at ER Sepsis Triage without reaching any ward admission or release milestone.
- `V0772`: The process ends with CRP testing and does not complete an admission or release goal.
- `V0774`: The variant terminates early at ER Sepsis Triage, lacking admission or release pathways.
- `V0775`: The sequence ends at CRP without reaching admission or release targets.
- `V0777`: The process stops at Leucocytes testing without an admission or release milestone.
- `V0778`: The sequence ends at Leucocytes without reaching any category criteria.
- `V0791`: The variant ends at IV Antibiotics without reaching admission or release categories.
- `V0804`: The narrative ends with Return ER after Release A, so it does not fit standard successful release categories cleanly.
- `V0806`: The narrative ends with Return ER, which is outside the standard classification targets.
- `V0808`: The narrative ends with Return ER, leaving it outside the standard categories.
- `V0812`: The narrative ends with Return ER, not fitting any of the core categories.
- `V0815`: The narrative ends with Return ER, making it part of the residual.
- `V0816`: The narrative terminates at IV Antibiotics without reaching admission or release.
- `V0817`: Although it features Release C, it ultimately ends with Return ER, placing it in the residual.
- `V0820`: The narrative terminates at LacticAcid before admission or release.
- `V0821`: The narrative ends with Return ER, placing it in the residual.
- `V0822`: The narrative ends with Return ER, placing it in the residual.
- `V0823`: The narrative ends with Return ER, placing it in the residual.
- `V0825`: The narrative ends with Return ER, placing it in the residual.
- `V0827`: The narrative ends with Return ER, placing it in the residual.
- `V0828`: The narrative ends with Return ER, placing it in the residual.
- `V0832`: The narrative terminates at IV Antibiotics without reaching admission or release.
- `V0834`: The narrative ends with Return ER, placing it in the residual.
- `V0842`: The narrative ends with Return ER, placing it in the residual.
- `V0843`: The narrative terminates at IV Liquid without reaching admission or release.
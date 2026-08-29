# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_rep1` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Admission to Normal Care (`admission_nc`)

Represents the inpatient ward admission pathway via Normal Care, advancing the patient toward discharge while interacting with time-to-treatment softgoals and measured by post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=15 under Goal id=5 (Patient is admitted to an inpatient ward, OR-decomposed).

**Goal-model linkage:** 15 (Task): Admission NC

**Coverage:** macro 50/846 variants (5.9%) · micro 53/1050 cases (5.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 8.23, nearest other category `release_a` at mean distance 9.65

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.507, nearest other category `release_a` at mean distance 0.467

## Admission to Intensive Care (`admission_ic`)

Represents the inpatient ward admission pathway via Intensive Care, carrying a negative contribution to minimizing time-to-treatment (Admission IC --[SomeNegative (-25)]--> Minimize time-to-treatment) and measured by post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=16 under Goal id=5 (Patient is admitted to an inpatient ward, OR-decomposed).

**Goal-model linkage:** 16 (Task): Admission IC

**Coverage:** macro 31/846 variants (3.7%) · micro 31/1050 cases (3.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 27.17, nearest other category `release_a` at mean distance 23.30

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.303, nearest other category `release_a` at mean distance 0.386

## Release Variant A (`release_a`)

Represents the discharge pathway Release A, which helps avoid post-discharge deterioration (Release A --[Help (+50)]--> Avoid post-discharge deterioration) and is measured against post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=17 under Goal id=6 (Admitted case reaches a captured discharge, OR-decomposed).

**Goal-model linkage:** 17 (Task): Release A

**Coverage:** macro 546/846 variants (64.5%) · micro 594/1050 cases (56.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 10.27, nearest other category `admission_nc` at mean distance 9.65

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.350, nearest other category `admission_ic` at mean distance 0.386

## Release Variant B (`release_b`)

Represents the discharge pathway Release B, helping to avoid post-discharge deterioration and judged against the post-discharge ER return indicator.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=18 under Goal id=6 (Admitted case reaches a captured discharge, OR-decomposed).

**Goal-model linkage:** 18 (Task): Release B

**Coverage:** macro 54/846 variants (6.4%) · micro 55/1050 cases (5.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 16.62, nearest other category `admission_nc` at mean distance 13.74

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.250, nearest other category `admission_ic` at mean distance 0.545

## Release Variant C (`release_c`)

Represents the discharge pathway Release C, contributing to avoiding post-discharge deterioration and evaluated via post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=19 under Goal id=6 (Admitted case reaches a captured discharge, OR-decomposed).

**Goal-model linkage:** 19 (Task): Release C

**Coverage:** macro 25/846 variants (3.0%) · micro 25/1050 cases (2.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 22.70, nearest other category `admission_nc` at mean distance 17.28

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.268, nearest other category `release_d` at mean distance 0.432

## Release Variant D (`release_d`)

Represents the discharge pathway Release D, contributing to avoiding post-discharge deterioration and judged against post-discharge ER return performance.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=20 under Goal id=6 (Admitted case reaches a captured discharge, OR-decomposed).

**Goal-model linkage:** 20 (Task): Release D

**Coverage:** macro 22/846 variants (2.6%) · micro 22/1050 cases (2.1%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 18.90, nearest other category `release_a` at mean distance 16.42

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.299, nearest other category `admission_ic` at mean distance 0.425

## Release Variant E (`release_e`)

Represents the discharge pathway Release E, contributing to avoiding post-discharge deterioration and measured by post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=21 under Goal id=6 (Admitted case reaches a captured discharge, OR-decomposed).

**Goal-model linkage:** 21 (Task): Release E

**Coverage:** macro 6/846 variants (0.7%) · micro 6/1050 cases (0.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 17.67, nearest other category `release_a` at mean distance 16.04

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.253, nearest other category `admission_ic` at mean distance 0.441

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

- `V0008` (`release_a`) / `V0707` (`admission_nc`): structural=1, profile=0.425
- `V0008` (`release_a`) / `V0766` (`admission_nc`): structural=1, profile=0.336
- `V0015` (`release_a`) / `V0758` (`admission_nc`): structural=1, profile=0.120
- `V0022` (`release_a`) / `V0274` (`release_c`): structural=1, profile=0.374
- `V0022` (`release_a`) / `V0415` (`admission_nc`): structural=1, profile=0.428
- `V0037` (`release_b`) / `V0706` (`release_a`): structural=1, profile=0.359
- `V0040` (`admission_nc`) / `V0503` (`release_b`): structural=1, profile=0.387
- `V0042` (`release_a`) / `V0771` (`admission_nc`): structural=1, profile=0.131
- `V0044` (`release_a`) / `V0754` (`admission_nc`): structural=1, profile=0.378
- `V0047` (`release_a`) / `V0663` (`admission_nc`): structural=1, profile=0.402

## Residual

112/846 variants (13.2%), 264/1050 cases (25.1%) unassigned.

- `V0001`: This narrative ends at ER Sepsis Triage and does not reach admission or release pathways.
- `V0002`: The process terminates at CRP without proceeding to admission or release.
- `V0003`: The narrative stops at Leucocytes and does not contain admission or release stages.
- `V0004`: This variant stops at IV Antibiotics in the ER and does not progress to admission or release.
- `V0005`: The process ends at LacticAcid without admission or discharge activities.
- `V0006`: This case sequence concludes at IV Antibiotics without reaching inpatient admission or release.
- `V0007`: Terminates at IV Antibiotics in the ER phase, lacking admission or release.
- `V0009`: Stops at IV Antibiotics in the ER without proceeding to admission or release.
- `V0010`: Ends at ER Sepsis Triage and does not include any admission or release activities.
- `V0011`: Concludes at IV Antibiotics within the ER without inpatient admission or release.
- `V0012`: Process stops at IV Antibiotics prior to any inpatient admission or discharge.
- `V0013`: Ends at Leucocytes without reaching admission or release categories.
- `V0017`: Ends at ER Sepsis Triage without reaching admission or release steps.
- `V0019`: Terminates at IV Antibiotics without inpatient admission or release pathways.
- `V0020`: Ends at CRP without any admission or release process elements.
- `V0025`: Ends at IV Antibiotics in the ER without admission or release steps.
- `V0027`: Stops at IV Antibiotics without reaching inpatient admission or release.
- `V0029`: Ends at Leucocytes without admission or release activities.
- `V0031`: Terminates at LacticAcid without admission or discharge pathways.
- `V0034`: Stops at IV Liquid in the ER without reaching admission or release.
- `V0036`: Ends at CRP without reaching inpatient admission or release.
- `V0038`: Terminates at IV Antibiotics in the ER without admission or release.
- `V0043`: Ends at LacticAcid without reaching admission or release.
- `V0050`: Ends at CRP without any inpatient admission or discharge pathway.
- `V0056`: The process ends at IV Antibiotics without reaching any inpatient admission or release pathway.
- `V0062`: Terminates at IV Antibiotics; does not complete an admission or release pathway.
- `V0081`: Stops at IV Liquid without reaching admission or release categories.
- `V0088`: Terminates at IV Antibiotics; lacks admission or release milestones.
- `V0092`: Ends at LacticAcid measurement without an admission or release event.
- `V0127`: The narrative terminates at LacticAcid and does not reach admission or release categories.
- `V0132`: The narrative terminates at IV Antibiotics and does not reach admission or release categories.
- `V0133`: The narrative terminates at IV Antibiotics and does not reach admission or release categories.
- `V0137`: The narrative terminates at LacticAcid and does not reach admission or release categories.
- `V0146`: The narrative terminates at Leucocytes and does not reach admission or release categories.
- `V0148`: The narrative terminates at IV Antibiotics and does not reach admission or release categories.
- `V0187`: The narrative stops at CRP and lacks any admission or release pathway.
- `V0197`: The narrative ends with Leucocytes and does not contain any admission or release category.
- `V0217`: The process stops at IV Antibiotics without reaching any defined admission or release category.
- `V0219`: The process terminates early at Leucocytes without an admission or release outcome.
- `V0232`: The narrative terminates at IV Antibiotics without reaching admission or release.
- `V0234`: The process ends at Leucocytes without an admission or release category.
- `V0260`: The narrative stops at IV Antibiotics and does not reach any admission or release phase.
- `V0268`: The narrative terminates at Leucocytes and does not contain a release or specific outcome category.
- `V0287`: The narrative stops at CRP without reaching any admission or release category.
- `V0292`: The narrative terminates at Leucocytes without reaching an admission or release pathway.
- `V0295`: The narrative terminates at IV Antibiotics after Admission NC, missing a release category.
- `V0302`: The process terminates early at ER Sepsis Triage and does not complete an admission or release pathway.
- `V0305`: Ends at IV Antibiotics without reaching ward admission or discharge.
- `V0322`: Terminates at IV Antibiotics without admission or discharge categories.
- `V0325`: Stops at IV Antibiotics in the ER phase.
- `V0330`: Ends at IV Liquid without reaching ward admission or release.
- `V0336`: Terminates at CRP test without admission or discharge.
- `V0342`: Stops at CRP without completing admission or discharge.
- `V0349`: Terminates at ER Sepsis Triage without reaching admission or release.
- `V0417`: The narrative does not include any inpatient admission or release category from the taxonomy.
- `V0429`: The narrative does not contain any admission or release categories from the taxonomy.
- `V0462`: The outcome is CRP and does not lead to any final admission or release category.
- `V0488`: The outcome is IV Liquid and does not reach any admission or release goal category.
- `V0492`: The outcome is IV Liquid, failing to fit any defined admission or release category.
- `V0495`: The outcome is IV Antibiotics and does not realize an admission or release goal.
- `V0501`: The narrative terminates at IV Liquid and does not reach ward admission or discharge categories.
- `V0510`: The narrative ends at IV Antibiotics without progressing to admission or discharge categories.
- `V0516`: The narrative terminates at Leucocytes and lacks ward admission or discharge milestones.
- `V0517`: The narrative terminates at ER Triage and does not reach admission or release categories.
- `V0549`: The narrative terminates at IV Liquid without reaching ward admission or release categories.
- `V0575`: The narrative terminates at Leucocytes without reaching any admission or release goal category.
- `V0580`: The process terminates at CRP without reaching a category-defining outcome.
- `V0584`: Process ends at IV Liquid; does not realize any admission or release category.
- `V0585`: Process ends at LacticAcid without realizing an admission or release goal.
- `V0587`: Terminates at CRP without reaching admission or release categories.
- `V0592`: Terminates at IV Antibiotics without an admission or release outcome.
- `V0645`: The narrative does not include any inpatient ward admission (neither Normal Care nor Intensive Care) nor a release category, falling into the residual.
- `V0654`: The narrative results in Leucocytes and does not reach a recognized discharge or admission category.
- `V0664`: The narrative ends at IV Liquid and does not reach any taxonomy category.
- `V0676`: The narrative terminates at IV Antibiotics without reaching a defined taxonomy category.
- `V0679`: The narrative ends at IV Antibiotics without completing an admission or release pathway.
- `V0685`: The narrative terminates at IV Antibiotics without reaching a target taxonomy category.
- `V0689`: The narrative ends at IV Antibiotics and does not reach a taxonomy category.
- `V0694`: The narrative ends at ER Sepsis Triage and does not reach an admission or release category.
- `V0703`: The process ends at IV Liquid and does not reach any of the defined admission or release pathways.
- `V0705`: Although it passes through Release A, it terminates with Return ER, which does not fit standard successful release categories.
- `V0708`: The variant ends with IV Antibiotics and does not complete an admission or release pathway.
- `V0712`: The narrative ends with Return ER after an intermediate discharge.
- `V0713`: The process stops at IV Antibiotics without reaching admission or release.
- `V0719`: The outcome is Return ER after a Release A event.
- `V0720`: The final activity is Return ER, making it fall outside the clean release categories.
- `V0721`: The process ends with a return to the emergency room.
- `V0724`: Ends with Return ER.
- `V0727`: Ends with Return ER.
- `V0734`: Ends with Return ER.
- `V0742`: The process stops at LacticAcid without admission or release.
- `V0744`: Ends with Return ER.
- `V0745`: Ends with Return ER.
- `V0746`: Ends with Return ER.
- `V0748`: Ends with Return ER.
- `V0750`: The process stops at IV Antibiotics without reaching admission or release.
- `V0759`: The narrative terminates at IV Antibiotics without reaching any ward admission or release category.
- `V0764`: The narrative ends at ER Sepsis Triage, lacking admission or release pathways.
- `V0774`: The narrative terminates at ER Sepsis Triage without an admission or release outcome.
- `V0775`: The narrative terminates at CRP without reaching ward admission or release categories.
- `V0777`: The narrative ends at Leucocytes without an admission or release.
- `V0778`: The narrative ends at Leucocytes without an admission or release.
- `V0791`: The narrative ends at IV Antibiotics without an admission or release outcome.
- `V0804`: The outcome is Return ER following Release A, which does not map cleanly to any primary admission/discharge category variant since it continues beyond initial release.
- `V0806`: The outcome is Return ER after Release A, therefore does not fit the target admission or release categories.
- `V0808`: The outcome is Return ER after Release A, so it does not fit the target categories.
- `V0812`: The outcome is Return ER, making it fall outside the standard category definitions.
- `V0815`: The outcome is Return ER after Release A, not matching the specific target categories.
- `V0816`: The outcome is IV Antibiotics, which is an intermediate ER stage and does not complete an admission or release pathway.
- `V0820`: The outcome is LacticAcid, an intermediate lab test in the ER, thus not realizing any admission or release category.
- `V0832`: The outcome is IV Antibiotics, which is an intermediate step and does not complete an admission or release pathway.
- `V0843`: The outcome is IV Liquid, which is an ER treatment stage and does not complete an admission or release pathway.
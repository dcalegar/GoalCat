# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_rep2` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Admission to Normal Care (`admission_nc`)

Patient is admitted to a normal care inpatient ward (Admission NC), advancing the organization's valued goals while balancing resource constraints. Performance is judged against the post-discharge ER return indicator.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=15 (Admission NC) under Goal id=5 (Patient is admitted to an inpatient ward, OR-decomposed).

**Goal-model linkage:** 15 (Task): Admission NC

**Coverage:** macro 42/846 variants (5.0%) · micro 45/1050 cases (4.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 9.29, nearest other category `release_a` at mean distance 10.14

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.525, nearest other category `release_a` at mean distance 0.484

## Admission to Intensive Care (`admission_ic`)

Patient is admitted to an intensive care inpatient ward (Admission IC). This alternative carries a negative contribution to minimizing time-to-treatment (-25) and is judged against post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=16 (Admission IC) under Goal id=5 (Patient is admitted to an inpatient ward, OR-decomposed).

**Goal-model linkage:** 16 (Task): Admission IC

**Coverage:** macro 15/846 variants (1.8%) · micro 15/1050 cases (1.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 33.73, nearest other category `release_e` at mean distance 27.68

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.291, nearest other category `release_a` at mean distance 0.395

## Release Variant A (`release_a`)

Admitted case reaches discharge via Release A, which helps avoid post-discharge deterioration (+50 contribution) and is measured against post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=17 (Release A) under Goal id=6 (Admitted case reaches a captured discharge, OR-decomposed).

**Goal-model linkage:** 17 (Task): Release A

**Coverage:** macro 501/846 variants (59.2%) · micro 549/1050 cases (52.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 10.42, nearest other category `admission_nc` at mean distance 10.14

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.330, nearest other category `admission_ic` at mean distance 0.395

## Release Variant B (`release_b`)

Admitted case reaches discharge via Release B, helping avoid post-discharge deterioration (+50 contribution) and measured against post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=18 (Release B) under Goal id=6 (Admitted case reaches a captured discharge, OR-decomposed).

**Goal-model linkage:** 18 (Task): Release B

**Coverage:** macro 53/846 variants (6.3%) · micro 54/1050 cases (5.1%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 16.78, nearest other category `admission_nc` at mean distance 14.16

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.232, nearest other category `release_d` at mean distance 0.538

## Release Variant C (`release_c`)

Admitted case reaches discharge via Release C, measured against post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=19 (Release C) under Goal id=6 (Admitted case reaches a captured discharge, OR-decomposed).

**Goal-model linkage:** 19 (Task): Release C

**Coverage:** macro 22/846 variants (2.6%) · micro 22/1050 cases (2.1%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 24.37, nearest other category `admission_nc` at mean distance 18.18

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.220, nearest other category `release_d` at mean distance 0.449

## Release Variant D (`release_d`)

Admitted case reaches discharge via Release D, measured against post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=20 (Release D) under Goal id=6 (Admitted case reaches a captured discharge, OR-decomposed).

**Goal-model linkage:** 20 (Task): Release D

**Coverage:** macro 20/846 variants (2.4%) · micro 20/1050 cases (1.9%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 19.89, nearest other category `release_a` at mean distance 17.02

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.277, nearest other category `admission_ic` at mean distance 0.437

## Release Variant E (`release_e`)

Admitted case reaches discharge via Release E, measured against post-discharge ER return.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=21 (Release E) under Goal id=6 (Admitted case reaches a captured discharge, OR-decomposed).

**Goal-model linkage:** 21 (Task): Release E

**Coverage:** macro 6/846 variants (0.7%) · micro 6/1050 cases (0.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 17.67, nearest other category `release_a` at mean distance 16.10

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.253, nearest other category `admission_ic` at mean distance 0.436

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

- `V0008` (`release_a`) / `V0707` (`admission_nc`): structural=1, profile=0.425
- `V0022` (`release_a`) / `V0274` (`release_c`): structural=1, profile=0.374
- `V0022` (`release_a`) / `V0415` (`admission_nc`): structural=1, profile=0.428
- `V0028` (`release_a`) / `V0307` (`admission_nc`): structural=1, profile=0.011
- `V0037` (`release_b`) / `V0706` (`release_a`): structural=1, profile=0.359
- `V0040` (`admission_nc`) / `V0503` (`release_b`): structural=1, profile=0.387
- `V0047` (`release_a`) / `V0663` (`admission_nc`): structural=1, profile=0.402
- `V0058` (`release_a`) / `V0350` (`admission_nc`): structural=1, profile=0.451
- `V0064` (`release_a`) / `V0337` (`admission_nc`): structural=1, profile=0.177
- `V0100` (`release_a`) / `V0586` (`release_b`): structural=1, profile=0.339

## Residual

187/846 variants (22.1%), 339/1050 cases (32.3%) unassigned.

- `V0001`: The narrative ends at ER Sepsis Triage without an admission or release outcome, so it does not fit any admission or release category.
- `V0002`: The case terminates at CRP without reaching an inpatient ward admission or discharge.
- `V0003`: The process sequence ends at Leucocytes and does not include admission or release.
- `V0004`: The variant ends at IV Antibiotics within the ER phase and is not admitted or discharged.
- `V0005`: The process terminates at LacticAcid before any ward admission or release event.
- `V0006`: The narrative stops at IV Antibiotics and lacks admission or release milestones.
- `V0007`: The narrative ends at IV Antibiotics without proceeding to admission or release.
- `V0009`: The narrative concludes with IV Antibiotics and does not involve admission or release.
- `V0010`: The trace stops at ER Sepsis Triage without reaching an admission or release category.
- `V0011`: The variant ends with IV Antibiotics and does not reach admission or release.
- `V0012`: The case finishes at IV Antibiotics and lacks downstream admission or release steps.
- `V0013`: The trace ends at Leucocytes without advancing to admission or release.
- `V0017`: The case terminates at ER Sepsis Triage without reaching any admission or release status.
- `V0019`: The variant concludes with IV Antibiotics and does not reach admission or release.
- `V0020`: The trace ends at CRP without any admission or release events.
- `V0025`: The narrative terminates at IV Antibiotics without reaching an admission or release category.
- `V0027`: The case ends at IV Antibiotics without admission or release milestones.
- `V0029`: The trace ends at Leucocytes without admission or release.
- `V0031`: The variant stops at LacticAcid without any inpatient admission or release.
- `V0034`: The trace ends at IV Liquid without reaching admission or release.
- `V0036`: The case ends at CRP without reaching admission or release.
- `V0038`: The variant stops at IV Antibiotics and lacks admission or release events.
- `V0043`: The case terminates at LacticAcid without admission or release.
- `V0050`: The trace stops at CRP without reaching admission or release.
- `V0056`: The narrative stops at IV Antibiotics and does not reach any inpatient admission or release category.
- `V0062`: The narrative ends at IV Antibiotics without reaching inpatient admission or release.
- `V0081`: The narrative terminates at IV Liquid and does not reach admission or release.
- `V0088`: The narrative stops at IV Antibiotics without inpatient admission or release.
- `V0092`: The narrative terminates at LacticAcid and does not reach admission or release.
- `V0127`: The narrative ends before any admission or release category.
- `V0132`: The narrative terminates at IV Antibiotics without any admission or release category.
- `V0133`: The narrative terminates at IV Antibiotics without any admission or release category.
- `V0137`: The narrative terminates at LacticAcid without any admission or release category.
- `V0146`: The narrative terminates at Leucocytes without any admission or release category.
- `V0148`: The narrative terminates at IV Antibiotics without any admission or release category.
- `V0187`: The narrative terminates early at CRP without reaching any admission or release category.
- `V0197`: The narrative terminates early at Leucocytes without reaching any admission or release category.
- `V0217`: The process terminates at IV Antibiotics without admission or release, thus fitting none of the categories.
- `V0219`: The process terminates at Leucocytes without admission or release, thus fitting none of the categories.
- `V0232`: The process terminates at IV Antibiotics without admission or release, thus fitting none of the categories.
- `V0234`: The process terminates at Leucocytes without admission or release, thus fitting none of the categories.
- `V0260`: The variant ends at IV Antibiotics without admission or release, fitting into the residual.
- `V0287`: The variant ends at CRP without admission or release, fitting into the residual.
- `V0292`: The variant ends at Leucocytes without admission or release, fitting into the residual.
- `V0302`: The narrative terminates at ER Sepsis Triage and does not complete an admission or release pathway.
- `V0305`: The process ends at IV Antibiotics without reaching any inpatient admission or release category.
- `V0322`: Terminates at IV Antibiotics without inpatient admission or release.
- `V0325`: Ends at IV Antibiotics without reaching admission or release categories.
- `V0330`: Terminates at IV Liquid without admission or release.
- `V0336`: Terminates at CRP without reaching an admission or release endpoint.
- `V0342`: Terminates at CRP without reaching an admission or release category.
- `V0349`: Terminates at ER Sepsis Triage without inpatient admission or release.
- `V0352`: The variant ends in Return ER rather than a recognized release category or admission category.
- `V0353`: The variant terminates in Return ER.
- `V0357`: The variant terminates in Return ER.
- `V0358`: The variant terminates in Return ER.
- `V0359`: The variant terminates in Return ER.
- `V0364`: The variant terminates in Return ER.
- `V0365`: The outcome is Leucocytes, not a recognized category endpoint.
- `V0366`: The variant terminates in Return ER.
- `V0367`: The variant terminates in Return ER.
- `V0369`: The variant terminates in Return ER.
- `V0370`: The variant terminates in Return ER.
- `V0374`: The outcome is Leucocytes.
- `V0378`: The outcome is IV Antibiotics.
- `V0379`: The outcome is IV Antibiotics.
- `V0382`: The variant terminates in Return ER.
- `V0385`: The variant terminates in Return ER.
- `V0386`: The variant terminates in Return ER.
- `V0398`: The variant terminates in Return ER.
- `V0417`: The outcome is ER Triage, which does not match any admission or release category.
- `V0429`: The outcome is IV Antibiotics, which does not match any admission or release category.
- `V0453`: The patient outcome is Return ER after Release A, which does not map cleanly into the specific final release outcomes without returning.
- `V0454`: The final outcome is Return ER after Release A, so it does not match a primary successful release category directly.
- `V0458`: The outcome is Return ER following Release A, fitting into the residual rather than a clean release category.
- `V0460`: The case ends with Return ER after Release A.
- `V0462`: The outcome is CRP, which does not match any admission or release category.
- `V0463`: The variant terminates with Return ER after Release A.
- `V0464`: The outcome is Return ER following Release A.
- `V0467`: The outcome is Return ER after Release A.
- `V0468`: The outcome is Return ER after Release A.
- `V0469`: The case leads to Return ER following Release A.
- `V0473`: The final outcome is Return ER after Release A.
- `V0474`: The narrative ends with Return ER after Release A.
- `V0476`: The outcome is Return ER following Release A.
- `V0479`: The outcome is Return ER after Release A.
- `V0482`: The outcome is Return ER following Release A.
- `V0484`: The outcome is Return ER after Release A.
- `V0488`: The outcome is IV Liquid, which does not match any admission or release category.
- `V0492`: The outcome is IV Liquid, which does not match any admission or release category.
- `V0495`: The outcome is IV Antibiotics, which does not match any admission or release category.
- `V0497`: The outcome is Return ER following Release A.
- `V0507`: The narrative ends at IV Antibiotics without reaching any inpatient admission or release category.
- `V0510`: The narrative stops at IV Antibiotics without any admission or release.
- `V0516`: The narrative stops at Leucocytes without an admission or release category.
- `V0517`: The narrative stops at ER Triage without an admission or release category.
- `V0549`: The narrative stops at IV Liquid without an admission or release category.
- `V0556`: The outcome is Return ER following Release A, which does not map to any active release goal configuration in the taxonomy.
- `V0558`: The outcome is Return ER after Release A, so it falls into the residual category.
- `V0559`: The outcome is Return ER after Release A, which falls into the residual category.
- `V0560`: The outcome is Return ER after Release A, which falls into the residual category.
- `V0564`: The outcome is Return ER following Release A, falling into the residual category.
- `V0567`: The outcome is Return ER following Release A, falling into the residual category.
- `V0573`: The outcome is Return ER following Release A, falling into the residual category.
- `V0575`: The narrative stops at Leucocytes and does not reach a recognized admission or release category.
- `V0577`: The outcome is Return ER following Release A, falling into the residual category.
- `V0578`: The outcome is Return ER following Release A, falling into the residual category.
- `V0579`: The outcome is Return ER following Release A, falling into the residual category.
- `V0580`: The narrative stops at CRP and does not reach a recognized admission or release category.
- `V0581`: The outcome is Return ER following Release D, falling into the residual category.
- `V0584`: The narrative terminates at IV Liquid before any admission or release takes place.
- `V0585`: The narrative terminates at LacticAcid before any admission or release takes place.
- `V0587`: The narrative terminates at CRP before any admission or release takes place.
- `V0588`: The outcome is Return ER following Release C, falling into the residual category.
- `V0590`: The outcome is Return ER following Release A, falling into the residual category.
- `V0591`: The outcome is Return ER following Release A, falling into the residual category.
- `V0592`: The narrative terminates at IV Antibiotics before any admission or release takes place.
- `V0595`: The outcome is Return ER following Release A, falling into the residual category.
- `V0605`: The patient returns to the ER after release, which falls outside the specific successful release or admission categories of the taxonomy.
- `V0614`: The patient returns to the ER after release, disqualifying it from standard successful release categories.
- `V0615`: The patient returns to the ER after release, disqualifying it from standard successful release categories.
- `V0625`: The patient returns to the ER after release, disqualifying it from standard successful release categories.
- `V0627`: The patient returns to the ER after release, disqualifying it from standard successful release categories.
- `V0631`: The patient returns to the ER after release, disqualifying it from standard successful release categories.
- `V0632`: The patient returns to the ER after release, disqualifying it from standard successful release categories.
- `V0633`: The patient returns to the ER after release, disqualifying it from standard successful release categories.
- `V0635`: The patient returns to the ER after release, disqualifying it from standard successful release categories.
- `V0638`: The patient returns to the ER after release, disqualifying it from standard successful release categories.
- `V0639`: The patient returns to the ER after release, disqualifying it from standard successful release categories.
- `V0640`: The patient returns to the ER after release, disqualifying it from standard successful release categories.
- `V0641`: The patient returns to the ER after release, disqualifying it from standard successful release categories.
- `V0643`: The patient returns to the ER after release, disqualifying it from standard successful release categories.
- `V0645`: The narrative lacks admission to inpatient care or a clear release category.
- `V0646`: The patient returns to the ER after release, disqualifying it from standard successful release categories.
- `V0649`: The patient returns to the ER after release, disqualifying it from standard successful release categories.
- `V0650`: The patient returns to the ER after release, disqualifying it from standard successful release categories.
- `V0654`: The narrative ends prematurely with Leucocytes and does not reach any discharge or admission category.
- `V0664`: Stops at IV Liquid and does not reach admission or release categories.
- `V0670`: Terminates with Leucocytes following an ER return and does not finalize a clean discharge category.
- `V0676`: Stops at IV Antibiotics without proceeding to admission or release.
- `V0679`: Ends at IV Antibiotics, lacking any admission or release step.
- `V0685`: Terminates at IV Antibiotics without reaching admission or discharge.
- `V0689`: Stops at IV Antibiotics without admission or discharge.
- `V0694`: Stops at ER Sepsis Triage without reaching any treatment admission or release.
- `V0703`: The narrative ends in IV Liquid and does not lead to a supported admission or release category.
- `V0705`: The narrative ends in Return ER after Release A, so it does not fit the final successful release taxonomy categories cleanly.
- `V0708`: The narrative terminates at IV Antibiotics without admission or release.
- `V0712`: The narrative ends in Return ER following multiple readmissions and releases.
- `V0713`: The narrative ends in IV Antibiotics without reaching a discharge or admission state.
- `V0719`: The narrative ends with Return ER after Release A.
- `V0720`: The narrative ends with Return ER after Release A.
- `V0721`: The narrative ends with Return ER after Release A.
- `V0724`: The narrative ends with Return ER after Release A.
- `V0727`: The narrative ends with Return ER after Release A.
- `V0734`: The narrative ends with Return ER after Release A.
- `V0742`: The narrative ends in LacticAcid without any matching discharge or admission taxonomy category.
- `V0744`: The narrative ends with Return ER after Release A.
- `V0745`: The narrative ends with Return ER after Release A.
- `V0746`: The narrative ends with Return ER after Release A.
- `V0748`: The narrative ends with Return ER after Release A.
- `V0750`: The narrative ends in IV Antibiotics without reaching any target taxonomy category.
- `V0759`: The narrative stops at IV Antibiotics in the ER and does not contain any admission or release category.
- `V0764`: The narrative halts at ER Sepsis Triage without reaching any inpatient admission or release state.
- `V0772`: The narrative ends abruptly at CRP following normal care admission, without completing a release.
- `V0774`: The narrative terminates early at ER Sepsis Triage.
- `V0775`: The narrative terminates at CRP without any inpatient admission or release activity.
- `V0777`: The process ends at Leucocytes in the ER without reaching admission or release.
- `V0778`: The process terminates at Leucocytes without an inpatient stay.
- `V0791`: Terminates at IV Antibiotics without inpatient admission.
- `V0804`: The variant ends in Return ER following Release A, which falls outside the primary discharge release categories.
- `V0806`: The variant terminates in Return ER after Release A.
- `V0808`: The variant ends with a Return ER event after Release A.
- `V0812`: The variant leads to a Return ER outcome after Release A.
- `V0815`: The variant results in a Return ER outcome after Release A.
- `V0816`: The variant ends in IV Antibiotics without reaching any discharge release category or admission ward.
- `V0817`: The variant terminates with Return ER after Release C.
- `V0820`: The variant terminates at LacticAcid without admission or release.
- `V0821`: The variant leads to Return ER following Release A.
- `V0822`: The variant ends in Return ER after Release A.
- `V0823`: The variant terminates in Return ER following Release A.
- `V0825`: The variant ends in Return ER after Release A.
- `V0827`: The variant ends in Return ER following Release A.
- `V0828`: The variant results in Return ER after Release A.
- `V0832`: The variant ends at IV Antibiotics without admission or release.
- `V0834`: The variant terminates in Return ER after Release A.
- `V0842`: The variant terminates with Return ER after Release A.
- `V0843`: The variant ends at IV Liquid after normal care admission, without a release outcome.
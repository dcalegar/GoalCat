# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_pertB_merge_15_16_rep1` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Admission NC (`admission_nc`)

Patient is admitted to a non-critical inpatient ward, realizing the inpatient admission goal (id=5). This advances the patient's care progression toward discharge while avoiding post-discharge deterioration and is evaluated against post-discharge outcomes.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared OR alternative id=5 (Admission NC represented by task id=15 'Merged 15+16'), as observed in multiple variants such as V0008, V0605, and V0551.

**Goal-model linkage:** 5 (Goal): Patient is admitted to an inpatient ward

**Coverage:** macro 36/846 variants (4.3%) · micro 39/1050 cases (3.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 10.86, nearest other category `release_a` at mean distance 11.49

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.420, nearest other category `release_a` at mean distance 0.444

## Release A (`release_a`)

Admitted case reaches discharge path A, contributing to avoiding post-discharge deterioration and measured via post-discharge ER return indicators.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=17 under the XOR-decomposed goal id=6 'Admitted case reaches a captured discharge', supported by frequent occurrences in the narrative sample such as variant V0008.

**Goal-model linkage:** 6 (Goal): Admitted case reaches a captured discharge

**Coverage:** macro 496/846 variants (58.6%) · micro 540/1050 cases (51.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 11.24, nearest other category `admission_nc` at mean distance 11.49

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.331, nearest other category `admission_nc` at mean distance 0.444

## Release B (`release_b`)

Admitted case reaches discharge path B, helping avoid post-discharge deterioration and monitored via post-discharge ER return indicators.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=18 under the XOR-decomposed goal id=6 'Admitted case reaches a captured discharge', supported by rare occurrences in the narrative sample such as variant V0068 and V0145.

**Goal-model linkage:** 6 (Goal): Admitted case reaches a captured discharge

**Coverage:** macro 54/846 variants (6.4%) · micro 55/1050 cases (5.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 16.68, nearest other category `admission_nc` at mean distance 14.96

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.230, nearest other category `release_d` at mean distance 0.542

## Release C (`release_c`)

Admitted case reaches discharge path C, supporting patient disposition and measured against post-discharge ER return indicators.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=19 under the XOR-decomposed goal id=6 'Admitted case reaches a captured discharge', evidenced by long-running complex traces like variant V0710.

**Goal-model linkage:** 6 (Goal): Admitted case reaches a captured discharge

**Coverage:** macro 23/846 variants (2.7%) · micro 23/1050 cases (2.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 23.82, nearest other category `release_a` at mean distance 18.60

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.236, nearest other category `release_d` at mean distance 0.446

## Release D (`release_d`)

Admitted case reaches discharge path D, supporting final disposition and measured against post-discharge ER return indicators.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=20 under the XOR-decomposed goal id=6 'Admitted case reaches a captured discharge', supported by variant V0273.

**Goal-model linkage:** 6 (Goal): Admitted case reaches a captured discharge

**Coverage:** macro 21/846 variants (2.5%) · micro 21/1050 cases (2.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 20.34, nearest other category `release_a` at mean distance 18.01

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.290, nearest other category `release_e` at mean distance 0.445

## Release E (`release_e`)

Admitted case reaches discharge path E, contributing to final successful patient disposition and measured against post-discharge ER return indicators.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=21 under the XOR-decomposed goal id=6 'Admitted case reaches a captured discharge', completing the set of valid discharge options under goal id=6.

**Goal-model linkage:** 6 (Goal): Admitted case reaches a captured discharge

**Coverage:** macro 6/846 variants (0.7%) · micro 6/1050 cases (0.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 17.67, nearest other category `release_a` at mean distance 16.36

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.253, nearest other category `release_d` at mean distance 0.445

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
- `V0008` (`release_a`) / `V0766` (`admission_nc`): structural=1, profile=0.336
- `V0015` (`release_a`) / `V0758` (`admission_nc`): structural=1, profile=0.120
- `V0022` (`release_a`) / `V0274` (`release_c`): structural=1, profile=0.374
- `V0022` (`release_a`) / `V0415` (`admission_nc`): structural=1, profile=0.428
- `V0037` (`release_b`) / `V0706` (`release_a`): structural=1, profile=0.359
- `V0040` (`admission_nc`) / `V0503` (`release_b`): structural=1, profile=0.387
- `V0042` (`release_a`) / `V0771` (`admission_nc`): structural=1, profile=0.131
- `V0047` (`release_a`) / `V0663` (`admission_nc`): structural=1, profile=0.402
- `V0099` (`release_a`) / `V0771` (`admission_nc`): structural=1, profile=0.000

## Residual

210/846 variants (24.8%), 366/1050 cases (34.9%) unassigned.

- `V0001`: The narrative ends at ER Sepsis Triage and does not involve inpatient admission or any release pathway.
- `V0002`: The narrative terminates at CRP testing within the ER phase, without reaching inpatient admission or release.
- `V0003`: The narrative stops at Leucocytes testing in the emergency department and does not proceed to admission or release.
- `V0004`: The narrative ends with IV Antibiotics administration in the ER and does not progress to inpatient admission.
- `V0005`: The narrative concludes with LacticAcid testing in the ER without achieving inpatient admission.
- `V0006`: The narrative stops after IV Antibiotics in the ER and does not involve an inpatient stay or release path.
- `V0007`: The narrative terminates at IV Antibiotics inside the emergency department without reaching admission.
- `V0009`: The process ends at IV Antibiotics in the ER without proceeding to admission or discharge paths.
- `V0010`: The narrative ends at ER Sepsis Triage and does not include inpatient admission or release.
- `V0011`: The process terminates with IV Antibiotics in the ER, lacking admission or release steps.
- `V0012`: The narrative ends with IV Antibiotics in the ER and does not reach inpatient admission.
- `V0013`: The sequence stops at Leucocytes testing in the emergency department without admission.
- `V0017`: The narrative ends at ER Sepsis Triage without inpatient admission or discharge.
- `V0019`: The narrative concludes at IV Antibiotics in the ER without reaching inpatient care.
- `V0020`: The narrative ends at CRP testing in the ER without admission or release.
- `V0025`: The sequence ends at IV Antibiotics in the ER without reaching inpatient admission.
- `V0027`: The narrative concludes with IV Antibiotics in the ER without admission.
- `V0029`: The narrative stops at Leucocytes testing in the ER without admission.
- `V0031`: The narrative ends at LacticAcid testing in the ER without inpatient admission.
- `V0034`: The sequence ends at IV Liquid in the ER without proceeding to admission.
- `V0036`: The narrative terminates at CRP testing in the ER without admission.
- `V0038`: The process ends at IV Antibiotics in the ER without inpatient admission.
- `V0043`: The narrative ends at LacticAcid testing in the ER without inpatient admission.
- `V0050`: The narrative ends at CRP testing in the ER without reaching inpatient admission or release.
- `V0052`: The outcome is Return ER, which does not map to a successful inpatient release path.
- `V0054`: The outcome is Return ER, which does not map to a successful inpatient release path.
- `V0055`: The outcome is Return ER, which does not map to a successful inpatient release path.
- `V0056`: The process terminates at IV Antibiotics without an admission or release category.
- `V0060`: The outcome is Return ER, which does not map to a successful inpatient release path.
- `V0062`: The process terminates at IV Antibiotics without an admission or release category.
- `V0071`: The outcome is Return ER, which does not map to a successful inpatient release path.
- `V0072`: The outcome is Return ER, which does not map to a successful inpatient release path.
- `V0074`: The outcome is Return ER, which does not map to a successful inpatient release path.
- `V0075`: The outcome is Return ER, which does not map to a successful inpatient release path.
- `V0078`: The outcome is Return ER, which does not map to a successful inpatient release path.
- `V0080`: The outcome is Return ER, which does not map to a successful inpatient release path.
- `V0081`: The process terminates at IV Liquid without an admission or release category.
- `V0083`: The outcome is Return ER, which does not map to a successful inpatient release path.
- `V0085`: The outcome is Return ER, which does not map to a successful inpatient release path.
- `V0088`: The process terminates at IV Antibiotics without an admission or release category.
- `V0089`: The outcome is Return ER, which does not map to a successful inpatient release path.
- `V0092`: The process terminates at LacticAcid without an admission or release category.
- `V0094`: The outcome is Return ER, which does not map to a successful inpatient release path.
- `V0098`: The outcome is Return ER, which does not map to a successful inpatient release path.
- `V0117`: The narrative terminates with Release D, which does not map to any defined category in this version of the taxonomy.
- `V0127`: The narrative ends at LacticAcid without completing inpatient admission or any discharge path.
- `V0132`: The narrative terminates at IV Antibiotics without inpatient admission.
- `V0133`: The narrative terminates at IV Antibiotics without inpatient admission.
- `V0137`: The narrative terminates at LacticAcid without inpatient admission.
- `V0146`: The narrative terminates at Leucocytes without inpatient admission.
- `V0148`: The narrative terminates at IV Antibiotics without inpatient admission.
- `V0181`: The narrative outcome is Leucocytes, which does not fit any of the defined taxonomy categories.
- `V0187`: The narrative outcome is CRP, which does not fit any of the defined taxonomy categories.
- `V0197`: The narrative outcome is Leucocytes, which does not fit any of the defined taxonomy categories.
- `V0217`: The narrative ends at IV Antibiotics without inpatient admission or any discharge path.
- `V0219`: The narrative ends at Leucocytes without reaching inpatient admission or a discharge path.
- `V0232`: The narrative terminates at IV Antibiotics without any admission or discharge activities.
- `V0234`: The narrative ends at Leucocytes without an inpatient admission or discharge path.
- `V0260`: The process terminates at IV Antibiotics without reaching any inpatient admission or release category.
- `V0268`: Ends at Leucocytes without achieving inpatient admission or release.
- `V0287`: Terminates at CRP without any inpatient admission or release.
- `V0292`: Ends at Leucocytes without reaching admission or release.
- `V0295`: Terminates at IV Antibiotics without inpatient admission or release.
- `V0302`: The patient's journey ends at ER Sepsis Triage without inpatient admission or final release disposition.
- `V0305`: The trace stops at IV Antibiotics in the emergency department, lacking inpatient admission and release.
- `V0322`: The event trace ends at IV Antibiotics in the ER without proceeding to admission or discharge.
- `V0325`: The trace stops at IV Antibiotics without inpatient admission or release disposition.
- `V0330`: The variant terminates at IV Liquid within the emergency setting.
- `V0336`: The process trace stops at CRP following ward admission, without reaching a release disposition.
- `V0342`: The narrative terminates at CRP in the ER without reaching admission or release.
- `V0349`: The case ends at ER Sepsis Triage without proceeding to inpatient admission or release.
- `V0352`: The narrative results in a Return ER outcome rather than one of the specified final release paths.
- `V0353`: The narrative results in a Return ER outcome instead of a successful release path.
- `V0357`: The narrative results in a Return ER outcome instead of a final release path.
- `V0358`: The narrative results in a Return ER outcome.
- `V0359`: The narrative results in a Return ER outcome.
- `V0364`: The narrative results in a Return ER outcome.
- `V0365`: The narrative outcome is Leucocytes, which does not match any admission or release category.
- `V0366`: The narrative results in a Return ER outcome.
- `V0367`: The narrative results in a Return ER outcome.
- `V0369`: The narrative results in a Return ER outcome.
- `V0370`: The narrative results in a Return ER outcome.
- `V0374`: The narrative outcome is Leucocytes, not a release category.
- `V0378`: The narrative stops at IV Antibiotics without inpatient admission or release.
- `V0379`: The narrative stops at IV Antibiotics without inpatient admission or release.
- `V0382`: The narrative results in a Return ER outcome.
- `V0385`: The narrative results in a Return ER outcome.
- `V0386`: The narrative results in a Return ER outcome.
- `V0398`: The narrative results in a Return ER outcome.
- `V0417`: The narrative does not include any inpatient admission or discharge path, ending instead at ER Triage.
- `V0429`: The narrative stops at IV Antibiotics without inpatient admission or any discharge path.
- `V0453`: The narrative ends with a return to the ER rather than a recognized release path.
- `V0454`: The narrative terminates with a return to the ER.
- `V0458`: The patient returns to the ER instead of completing a discharge category.
- `V0460`: The narrative terminates with a return to the ER.
- `V0462`: The narrative ends before reaching a discharge path.
- `V0463`: The narrative terminates with a return to the ER.
- `V0464`: The narrative terminates with a return to the ER.
- `V0467`: The narrative terminates with a return to the ER.
- `V0468`: The narrative terminates with a return to the ER.
- `V0469`: The narrative terminates with a return to the ER.
- `V0473`: The narrative terminates with a return to the ER.
- `V0474`: The narrative terminates with a return to the ER.
- `V0476`: The narrative terminates with a return to the ER.
- `V0479`: The narrative terminates with a return to the ER.
- `V0482`: The narrative terminates with a return to the ER.
- `V0484`: The narrative terminates with a return to the ER.
- `V0488`: The narrative ends at IV Liquid without inpatient admission or release.
- `V0492`: The narrative ends at IV Liquid without inpatient admission or release.
- `V0495`: The narrative ends at IV Antibiotics without inpatient admission or release.
- `V0497`: The narrative terminates with a return to the ER.
- `V0507`: The process terminates at IV Antibiotics without reaching admission or discharge.
- `V0510`: The narrative ends at IV Antibiotics without completing admission or discharge.
- `V0516`: The process stops at Leucocytes and does not reach admission or release.
- `V0517`: The narrative terminates prematurely at ER Triage.
- `V0549`: The process terminates at IV Liquid and does not reach admission or release.
- `V0556`: The narrative results in Return ER after Release A, so it does not meet the successful criteria of the release categories.
- `V0558`: The narrative results in Return ER, failing the post-discharge outcome condition.
- `V0559`: The narrative results in Return ER, failing the post-discharge outcome condition.
- `V0560`: The narrative results in Return ER, failing the post-discharge outcome condition.
- `V0564`: The narrative results in Return ER, failing the post-discharge outcome condition.
- `V0567`: The narrative results in Return ER, failing the post-discharge outcome condition.
- `V0573`: The narrative results in Return ER, failing the post-discharge outcome condition.
- `V0575`: The narrative ends at Leucocytes without achieving admission or release.
- `V0577`: The narrative results in Return ER, failing the post-discharge outcome condition.
- `V0578`: The narrative results in Return ER, failing the post-discharge outcome condition.
- `V0579`: The narrative results in Return ER, failing the post-discharge outcome condition.
- `V0580`: The narrative ends at CRP without achieving admission or release.
- `V0581`: The narrative results in Return ER, failing the post-discharge outcome condition.
- `V0584`: The narrative ends at IV Liquid without achieving admission or release.
- `V0585`: The narrative ends at LacticAcid without achieving admission or release.
- `V0587`: The narrative ends at CRP without achieving admission or release.
- `V0588`: The narrative results in Return ER, failing the post-discharge outcome condition.
- `V0590`: The narrative results in Return ER, failing the post-discharge outcome condition.
- `V0591`: The narrative results in Return ER, failing the post-discharge outcome condition.
- `V0592`: The narrative ends at IV Antibiotics without achieving admission or release.
- `V0595`: The narrative results in Return ER, failing the post-discharge outcome condition.
- `V0605`: The case results in a return to the ER after initial Release A, indicating post-discharge deterioration and thus not successfully realizing the long-term stable release goal without readmission.
- `V0614`: The narrative ends with a Return ER event following Release A, indicating post-discharge deterioration.
- `V0615`: The narrative ends with Return ER after Release C, failing post-discharge stability.
- `V0625`: The narrative results in a Return ER after Release A.
- `V0627`: The narrative results in a Return ER after Release A.
- `V0631`: The narrative results in a Return ER after Release A.
- `V0632`: The narrative results in a Return ER after Release A.
- `V0633`: The narrative results in a Return ER after Release D.
- `V0635`: The narrative results in a Return ER after Release A.
- `V0636`: The narrative ends with LacticAcid and does not reach any inpatient admission or release category.
- `V0638`: The narrative results in a Return ER after Release A.
- `V0639`: The narrative results in a Return ER after Release A.
- `V0640`: The narrative results in a Return ER after Release A.
- `V0641`: The narrative results in a Return ER after Release A.
- `V0643`: The narrative results in a Return ER after Release A.
- `V0644`: The narrative ends with CRP and does not reach any release or proper admission completion category.
- `V0645`: The narrative ends with LacticAcid and does not reach an admission or release category.
- `V0646`: The narrative continues past release with a Return ER and subsequent lab work, failing complete stable disposition.
- `V0649`: The narrative results in a Return ER after Release A.
- `V0650`: The narrative results in a Return ER after Release A.
- `V0654`: The process terminates at Leucocytes and does not reach any designated discharge or admission category.
- `V0664`: The process terminates at IV Liquid and does not reach admission or release categories.
- `V0670`: The process ends with Leucocytes after an ER return following Release A, not cleanly realizing a release category at termination.
- `V0676`: The process terminates at IV Antibiotics and does not reach admission or release.
- `V0679`: The process terminates at IV Antibiotics.
- `V0685`: The process terminates at IV Antibiotics.
- `V0689`: The process terminates at IV Antibiotics.
- `V0694`: The process terminates at ER Sepsis Triage.
- `V0703`: The variant ends with IV Liquid and does not reach any discharge or admission destination category.
- `V0708`: The narrative terminates at IV Antibiotics without reaching any defined release path or final non-critical admission disposition.
- `V0713`: The process terminates at IV Antibiotics, failing to achieve admission or release criteria.
- `V0742`: The narrative terminates at LacticAcid and does not reach admission or release categories.
- `V0750`: The narrative stops at IV Antibiotics and does not realize any admission or release goal.
- `V0752`: The narrative outcome is 'Return ER' rather than reaching one of the specified final release paths.
- `V0753`: The narrative outcome is 'Return ER'.
- `V0754`: The narrative outcome is 'Return ER'.
- `V0756`: The narrative outcome is 'Return ER'.
- `V0757`: The narrative outcome is 'Return ER'.
- `V0759`: The narrative stops at 'IV Antibiotics' without proceeding to inpatient admission or release.
- `V0763`: The narrative outcome is 'Return ER'.
- `V0764`: The narrative stops at 'ER Sepsis Triage' and does not involve admission or release.
- `V0765`: The narrative outcome is 'Return ER'.
- `V0767`: The narrative outcome is 'Return ER'.
- `V0770`: The narrative outcome is 'Return ER'.
- `V0772`: The narrative ends with 'CRP' and does not reach admission or release.
- `V0774`: The narrative ends at 'ER Sepsis Triage' without admission or release.
- `V0775`: The narrative ends at 'CRP' without admission or release.
- `V0777`: The narrative ends at 'Leucocytes' without admission or release.
- `V0778`: The narrative ends at 'Leucocytes' without admission or release.
- `V0779`: The narrative outcome is 'Return ER'.
- `V0785`: The narrative outcome is 'Return ER'.
- `V0787`: The narrative outcome is 'Return ER'.
- `V0791`: The narrative ends at 'IV Antibiotics' without admission or release.
- `V0794`: The narrative outcome is 'Return ER'.
- `V0797`: The narrative outcome is 'Return ER'.
- `V0798`: The narrative outcome is 'Return ER'.
- `V0804`: The narrative ends with Return ER after an initial release, which does not fit any of the successful release categories.
- `V0806`: The narrative ends with Return ER, which is outside the successful discharge pathways.
- `V0808`: The narrative ends with Return ER, meaning it does not fall under any final successful release category.
- `V0812`: The narrative ends with Return ER, which does not correspond to a successful discharge category.
- `V0815`: The narrative ends with Return ER, which is excluded from the successful discharge paths.
- `V0816`: The process terminates at IV Antibiotics without reaching an inpatient admission or release category.
- `V0820`: The process terminates at LacticAcid without admission or discharge.
- `V0821`: The narrative ultimately ends with Return ER, failing to achieve a successful final disposition.
- `V0822`: The narrative ends with Return ER after an extended treatment course.
- `V0823`: The narrative ends with Return ER.
- `V0825`: The narrative ends with Return ER.
- `V0827`: The narrative ends with Return ER.
- `V0828`: The narrative ends with Return ER.
- `V0832`: The process terminates at IV Antibiotics without admission or discharge.
- `V0834`: The narrative ends with Return ER.
- `V0842`: The narrative ends with Return ER.
- `V0843`: The process terminates at IV Liquid without reaching a release category.
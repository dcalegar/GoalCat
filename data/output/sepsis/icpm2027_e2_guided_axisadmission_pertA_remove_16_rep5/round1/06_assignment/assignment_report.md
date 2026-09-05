# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_axisadmission_pertA_remove_16_rep5` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Admission to Inpatient Ward Non-Critical (`admission_nc`)

Realizes the patient admission goal by admitting the patient to a non-critical inpatient ward (Admission NC). This pathway advances the organization's goal of structured inpatient placement following sepsis stabilization, and its performance is evaluated against post-discharge outcomes measured by indicators such as Post-discharge ER return (binary) (target 0, worst 1 binary).

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the single declared alternative ID 15 ('Admission NC') under the OR-decomposition of goal id=5. The narrative sample demonstrates this alternative across multiple variants (e.g., V0008, V0625, V0551) leading to ward care and subsequent release or readmission outcomes.

**Goal-model linkage:** 15 (Task): Admission NC

**Coverage:** macro 747/846 variants (88.3%) · micro 799/1050 cases (76.1%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 12.51, nearest other category `None` at mean distance n/a

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.407, nearest other category `None` at mean distance n/a

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0286` / `V0710` (category `admission_nc`): structural=182, profile=0.756
- `V0053` / `V0710` (category `admission_nc`): structural=181, profile=0.788
- `V0351` / `V0710` (category `admission_nc`): structural=181, profile=0.765
- `V0058` / `V0710` (category `admission_nc`): structural=180, profile=0.781
- `V0306` / `V0710` (category `admission_nc`): structural=180, profile=0.664
- `V0309` / `V0710` (category `admission_nc`): structural=180, profile=0.865
- `V0323` / `V0710` (category `admission_nc`): structural=180, profile=0.800
- `V0350` / `V0710` (category `admission_nc`): structural=180, profile=0.670
- `V0489` / `V0710` (category `admission_nc`): structural=180, profile=0.755
- `V0497` / `V0710` (category `admission_nc`): structural=180, profile=0.751

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- none

## Residual

99/846 variants (11.7%), 251/1050 cases (23.9%) unassigned.

- `V0001`: This variant ends at ER Sepsis Triage and does not include inpatient ward admission.
- `V0002`: This variant ends at CRP and does not include inpatient ward admission.
- `V0003`: This variant ends at Leucocytes and does not include inpatient ward admission.
- `V0004`: This variant ends at IV Antibiotics and does not include inpatient ward admission.
- `V0005`: This variant ends at LacticAcid and does not include inpatient ward admission.
- `V0006`: This variant ends at IV Antibiotics and does not include inpatient ward admission.
- `V0007`: This variant ends at IV Antibiotics and does not include inpatient ward admission.
- `V0009`: This variant ends at IV Antibiotics and does not include inpatient ward admission.
- `V0010`: This variant ends at ER Sepsis Triage and does not include inpatient ward admission.
- `V0011`: This variant ends at IV Antibiotics and does not include inpatient ward admission.
- `V0012`: This variant ends at IV Antibiotics and does not include inpatient ward admission.
- `V0013`: This variant ends at Leucocytes and does not include inpatient ward admission.
- `V0017`: This variant ends at ER Sepsis Triage and does not include inpatient ward admission.
- `V0019`: This variant ends at IV Antibiotics and does not include inpatient ward admission.
- `V0020`: This variant ends at CRP and does not include inpatient ward admission.
- `V0025`: This variant ends at IV Antibiotics and does not include inpatient ward admission.
- `V0027`: The pathway ends at 'IV Antibiotics' without proceeding to inpatient admission or final release.
- `V0029`: The process terminates at 'Leucocytes' and does not reach the inpatient admission goal.
- `V0031`: The sequence ends prematurely at 'LacticAcid' without reaching admission.
- `V0034`: The variant terminates at 'IV Liquid' and does not involve inpatient ward admission.
- `V0036`: The process concludes at 'CRP' without continuing to admission.
- `V0038`: Stops at 'IV Antibiotics' without entering an inpatient ward.
- `V0043`: Terminates at 'LacticAcid' without proceeding to admission.
- `V0050`: The process sequence ends at 'CRP' without progressing to inpatient admission.
- `V0056`: The narrative ends with IV Antibiotics and does not include an inpatient ward admission.
- `V0062`: The narrative ends with IV Antibiotics and does not include an inpatient ward admission.
- `V0081`: The narrative ends at 'IV Liquid' and does not contain any admission activity to an inpatient ward.
- `V0088`: The narrative ends with 'IV Antibiotics' and does not contain any inpatient ward admission steps.
- `V0092`: The narrative terminates at 'LacticAcid' and lacks any inpatient ward admission activity.
- `V0127`: The narrative ends at LacticAcid without any inpatient ward admission activity.
- `V0132`: The narrative ends at IV Antibiotics without any inpatient ward admission activity.
- `V0133`: The narrative ends at IV Antibiotics without any inpatient ward admission activity.
- `V0137`: The narrative ends at LacticAcid without any inpatient ward admission activity.
- `V0145`: The narrative only contains Admission IC and does not realize the Admission NC goal.
- `V0146`: The narrative ends at Leucocytes without any inpatient ward admission activity.
- `V0148`: The narrative ends at IV Antibiotics without any inpatient ward admission activity.
- `V0167`: The narrative contains Admission IC but lacks Admission NC, meaning it does not realize the non-critical admission category.
- `V0187`: The narrative does not contain an inpatient admission activity ('Admission NC') and terminates prematurely.
- `V0197`: The narrative does not contain an inpatient admission activity ('Admission NC') and terminates prematurely.
- `V0217`: The narrative does not include 'Admission NC', so it does not realize the inpatient admission category.
- `V0218`: The narrative includes 'Admission IC' instead of 'Admission NC', failing to realize the non-critical ward admission goal.
- `V0219`: The narrative terminates at 'Leucocytes' without any admission activity, so it does not realize the admission category.
- `V0232`: The process variant ends at IV Antibiotics without any admission activity, hence it does not realize the inpatient admission goal.
- `V0234`: The process variant terminates at Leucocytes without reaching any admission step.
- `V0260`: The variant terminates at IV Antibiotics without any inpatient admission, so it does not realize the admission_nc category.
- `V0287`: The narrative terminates at CRP and does not include an admission activity, so it does not realize the category.
- `V0292`: Terminates at Leucocytes without an admission step, therefore it does not fit the admission category.
- `V0302`: The narrative ends at ER Sepsis Triage and does not reach any inpatient admission goal.
- `V0305`: The variant terminates at IV Antibiotics without proceeding to an inpatient ward admission.
- `V0322`: The narrative terminates at IV Antibiotics without admission to a ward.
- `V0325`: The narrative terminates at IV Antibiotics without reaching inpatient admission.
- `V0330`: The narrative terminates at 'IV Liquid' and does not contain any inpatient admission activity.
- `V0342`: The narrative ends at 'CRP' and lacks any inpatient ward admission activity.
- `V0349`: The narrative terminates at 'ER Sepsis Triage' and does not reach inpatient admission.
- `V0365`: The narrative does not include an admission to a non-critical inpatient ward ('Admission NC'), so it does not realize the category.
- `V0378`: The narrative does not include any inpatient admission activity, ending prematurely at IV Antibiotics.
- `V0379`: The narrative terminates at IV Antibiotics without performing an inpatient admission.
- `V0407`: The narrative includes Admission IC instead of Admission NC, so it does not fit the taxonomy category.
- `V0417`: The narrative terminates at ER Triage and does not contain an Admission NC activity.
- `V0429`: The narrative ends with 'IV Antibiotics' and does not contain any admission activity, hence it does not realize the inpatient ward admission category.
- `V0432`: The narrative contains 'Admission IC' instead of 'Admission NC', so it does not realize the non-critical inpatient ward admission category.
- `V0488`: The narrative ends at IV Liquid and does not contain any admission activity to an inpatient ward.
- `V0492`: The narrative ends at IV Liquid and does not contain any admission activity to an inpatient ward.
- `V0495`: The narrative ends at IV Antibiotics and does not contain any admission activity to an inpatient ward.
- `V0507`: The pathway terminates at IV Antibiotics without reaching an inpatient ward admission activity.
- `V0510`: The pathway ends at IV Antibiotics and does not include any inpatient ward admission activity.
- `V0516`: The variant terminates at Leucocytes and lacks any admission activity.
- `V0517`: The pathway ends prematurely at ER Triage without progressing to admission.
- `V0532`: The narrative does not contain any Admission NC activity and therefore does not realize the non-critical inpatient ward admission category.
- `V0549`: The narrative terminates at IV Liquid and lacks Admission NC, failing to realize the admission category.
- `V0575`: The narrative does not include any admission step to a non-critical inpatient ward, terminating in an interim laboratory test instead.
- `V0580`: The narrative ends in CRP and does not contain any inpatient admission activity, hence it does not realize the category.
- `V0584`: The narrative terminates at IV Liquid without any inpatient ward admission activity.
- `V0585`: The narrative ends at LacticAcid and lacks any inpatient ward admission steps.
- `V0587`: The narrative terminates at CRP without reaching an inpatient admission stage.
- `V0592`: The narrative terminates at IV Antibiotics and does not contain an inpatient admission activity.
- `V0621`: The narrative leads to 'Admission IC' instead of 'Admission NC', so it does not realize the non-critical admission category.
- `V0645`: The narrative lacks any inpatient ward admission activity, ending prematurely at LacticAcid, so it does not realize admission_nc.
- `V0654`: The narrative only involves Admission IC, not Admission NC.
- `V0664`: The narrative terminates at IV Liquid and does not reach Admission NC.
- `V0676`: The narrative ends with IV Antibiotics and does not include an inpatient ward admission.
- `V0679`: The narrative ends with IV Antibiotics and lacks any inpatient ward admission activity.
- `V0685`: The narrative terminates at IV Antibiotics without involving any inpatient ward admission.
- `V0689`: The narrative ends at IV Antibiotics and does not reach an inpatient ward admission.
- `V0694`: The narrative terminates at ER Sepsis Triage and does not contain any admission activity.
- `V0713`: The variant ends at IV Antibiotics without an inpatient ward admission step, so it does not realize the category.
- `V0715`: The narrative shows Admission IC rather than Admission NC, thus it does not realize the non-critical admission category.
- `V0742`: The narrative does not include Admission NC, thus failing to realize the category goal.
- `V0750`: The narrative does not include Admission NC, thus failing to realize the category goal.
- `V0759`: The narrative terminates at IV Antibiotics without reaching any inpatient admission activity.
- `V0764`: The pathway ends prematurely at ER Sepsis Triage and does not proceed to inpatient admission.
- `V0774`: The process sequence halts at ER Sepsis Triage without reaching any admission milestone.
- `V0775`: The narrative terminates at CRP testing and does not achieve inpatient ward admission.
- `V0777`: The process terminates at Leucocytes without reaching any inpatient admission or ward placement step.
- `V0778`: The process terminates at Leucocytes and does not contain any inpatient admission activity.
- `V0791`: The process ends at IV Antibiotics and lacks any inpatient ward admission step.
- `V0816`: The narrative ends at IV Antibiotics without reaching any inpatient admission activity, hence it does not realize the admission category.
- `V0820`: The sequence terminates at LacticAcid without any inpatient ward admission activity.
- `V0832`: The narrative terminates at IV Antibiotics without reaching an inpatient ward admission.
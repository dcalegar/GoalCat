# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_axisadmission_pertA_remove_16_rep4` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Admission to Inpatient Ward (Admission NC) (`admission_nc`)

Represents the standard process alternative where a patient is admitted to a non-critical inpatient ward, as realized by the Admission NC task. This step supports the broader goal of inpatient care management and is evaluated against post-discharge outcomes.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the single declared alternative under the OR-decomposed Patient is admitted to an inpatient ward goal (id=5), specifically task id=15 (Admission NC). The narrative sample frequently shows this alternative realized in variants such as V0008, V0065, and V0710 without evidence for further meaningful subdivisions on this specific axis.

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

- `V0001`: The narrative ends at ER Sepsis Triage and does not include any inpatient ward admission steps.
- `V0002`: The narrative stops at CRP testing without proceeding to inpatient ward admission.
- `V0003`: The narrative concludes with Leucocytes testing and lacks an admission step.
- `V0004`: The trace terminates after IV Antibiotics administration in the ER setting.
- `V0005`: The sequence ends with LacticAcid testing without any subsequent admission.
- `V0006`: The narrative terminates at IV Antibiotics without inpatient ward admission.
- `V0007`: The sequence ends with IV Antibiotics and does not progress to ward admission.
- `V0009`: The narrative ends with IV Antibiotics administration and contains no admission activity.
- `V0010`: The process sequence finishes at ER Sepsis Triage without reaching inpatient admission.
- `V0011`: The narrative ends at IV Antibiotics and does not involve ward admission.
- `V0012`: The trace concludes with IV Antibiotics in the emergency department.
- `V0013`: The sequence terminates with Leucocytes testing without further care steps.
- `V0017`: The narrative ends at ER Sepsis Triage without proceeding to admission.
- `V0019`: The sequence concludes with IV Antibiotics without an inpatient admission step.
- `V0020`: The narrative ends at CRP testing and does not involve ward admission.
- `V0025`: The sequence finishes at IV Antibiotics without any inpatient ward admission step.
- `V0027`: The narrative does not contain any admission to an inpatient ward step, ending at IV Antibiotics.
- `V0029`: The narrative terminates at Leucocytes and lacks any inpatient ward admission step.
- `V0031`: The narrative ends with LacticAcid and contains no inpatient ward admission step.
- `V0034`: The narrative ends at IV Liquid and contains no inpatient admission step.
- `V0036`: The narrative terminates at CRP and lacks an inpatient ward admission step.
- `V0038`: The narrative ends at IV Antibiotics without any inpatient ward admission.
- `V0043`: The narrative terminates at LacticAcid and does not include inpatient admission.
- `V0050`: The narrative ends at CRP and contains no inpatient ward admission step.
- `V0056`: The narrative ends at 'IV Antibiotics' without including an inpatient admission step ('Admission NC'), therefore it does not realize the inpatient admission category.
- `V0062`: The narrative terminates at 'IV Antibiotics' without proceeding to inpatient ward admission, so it does not realize the target category.
- `V0081`: The narrative does not contain any admission task to a non-critical inpatient ward, terminating in IV Liquid instead.
- `V0088`: The narrative does not contain any admission task to a non-critical inpatient ward, terminating in IV Antibiotics.
- `V0092`: The narrative does not contain any admission task to a non-critical inpatient ward, terminating in LacticAcid.
- `V0127`: The narrative does not contain Admission NC and ends with LacticAcid, so it does not realize the inpatient admission category.
- `V0132`: The narrative ends at IV Antibiotics without involving Admission NC.
- `V0133`: The narrative ends at IV Antibiotics without involving Admission NC.
- `V0137`: The narrative does not contain Admission NC and ends with LacticAcid.
- `V0145`: The narrative only goes through Admission IC and does not contain Admission NC.
- `V0146`: The narrative ends at Leucocytes without involving Admission NC.
- `V0148`: The narrative ends at IV Antibiotics without involving Admission NC.
- `V0167`: The narrative does not contain 'Admission NC' and therefore does not realize the standard non-critical inpatient ward admission category.
- `V0187`: The narrative does not contain any admission step to an inpatient ward ('Admission NC').
- `V0197`: The narrative does not contain any admission step to an inpatient ward ('Admission NC').
- `V0217`: The narrative does not contain any 'Admission NC' activity, so it does not realize the category.
- `V0218`: The narrative involves 'Admission IC' rather than 'Admission NC', so it does not fit the target category.
- `V0219`: The narrative does not contain any 'Admission NC' activity, so it does not realize the category.
- `V0232`: The narrative does not contain any admission activity to a non-critical inpatient ward, concluding with IV Antibiotics instead.
- `V0234`: The narrative does not contain any admission activity to a non-critical inpatient ward.
- `V0260`: The narrative does not contain an admission step, ending in IV Antibiotics.
- `V0287`: The narrative does not contain the admission step, ending with CRP testing instead.
- `V0292`: The narrative terminates early at Leucocytes and lacks any admission activity.
- `V0302`: The narrative stops at ER Sepsis Triage and does not contain any admission to an inpatient ward.
- `V0305`: The narrative ends at IV Antibiotics without proceeding to inpatient admission.
- `V0322`: The narrative ends at IV Antibiotics without any inpatient ward admission.
- `V0325`: The narrative terminates at IV Antibiotics and does not involve inpatient ward admission.
- `V0330`: The narrative does not contain any admission tasks, so it does not realize the Admission to Inpatient Ward category.
- `V0342`: The narrative does not contain any admission tasks, so it does not realize the Admission to Inpatient Ward category.
- `V0349`: The narrative does not contain any admission tasks, so it does not realize the Admission to Inpatient Ward category.
- `V0365`: The narrative lacks 'Admission NC' and instead goes to 'Admission IC', meaning it does not realize the non-critical admission category.
- `V0378`: The narrative does not contain any Admission NC activity and ends at IV Antibiotics, thus not realizing the category.
- `V0379`: The narrative does not include the Admission NC activity, stopping at IV Antibiotics.
- `V0407`: The narrative involves 'Admission IC' rather than 'Admission NC', so it does not realize the target category.
- `V0417`: The narrative does not contain any admission activity, ending instead at ER Triage.
- `V0429`: The process terminates at IV Antibiotics without involving an inpatient ward admission task.
- `V0432`: The narrative contains Admission IC rather than Admission NC, meaning it does not realize the non-critical ward category.
- `V0488`: The narrative ends at 'IV Liquid' and does not contain any admission activity to an inpatient ward.
- `V0492`: The process concludes at 'IV Liquid' without any inpatient ward admission steps.
- `V0495`: The process terminates at 'IV Antibiotics' and lacks any admission event.
- `V0507`: The narrative terminates at IV Antibiotics without containing any admission task, hence it does not realize admission to a non-critical inpatient ward.
- `V0510`: The narrative terminates at IV Antibiotics and lacks any inpatient admission step.
- `V0516`: The narrative ends at Leucocytes without an inpatient ward admission.
- `V0517`: The narrative ends prematurely at ER Triage without any admission step.
- `V0549`: The narrative ends at IV Liquid and does not include an admission to a non-critical inpatient ward.
- `V0575`: The narrative does not include any Admission NC activity and therefore does not realize the category.
- `V0580`: The narrative ends with 'CRP' and does not contain any admission step to an inpatient ward, so it falls into the residual.
- `V0584`: The process terminates at 'IV Liquid' without any inpatient ward admission step, making it part of the residual.
- `V0585`: The process ends at 'LacticAcid' without containing an inpatient ward admission step.
- `V0587`: The narrative terminates at 'CRP' without any inpatient ward admission activity.
- `V0592`: The narrative ends with 'IV Antibiotics' and lacks any inpatient ward admission task.
- `V0621`: The narrative does not include the 'Admission NC' activity, instead going through 'Admission IC', so it does not realize the target category.
- `V0645`: The narrative does not include any Admission NC task, so it does not realize the category.
- `V0654`: The variant features 'Admission IC' instead of 'Admission NC', hence it does not realize the non-critical ward admission category.
- `V0664`: The narrative does not contain any admission step (Admission NC or IC), making the category inapplicable.
- `V0676`: The narrative ends at IV Antibiotics without any inpatient ward admission step.
- `V0679`: The process terminates at IV Antibiotics without reaching an inpatient ward admission.
- `V0685`: The process terminates at IV Antibiotics without any inpatient ward admission.
- `V0689`: The process concludes at IV Antibiotics with no inpatient admission step.
- `V0694`: The process ends at ER Sepsis Triage without reaching any ward admission.
- `V0713`: The narrative does not include the Admission NC activity or any other fitting category.
- `V0715`: The narrative includes Admission IC instead of Admission NC, and thus does not realize the category.
- `V0742`: The narrative lacks the 'Admission NC' activity, resulting in an admission to intensive care and ending without non-critical ward admission.
- `V0750`: The narrative ends at 'IV Antibiotics' without proceeding to any inpatient admission activity, thus falling into the residual.
- `V0759`: The narrative lacks any admission activity and ends at IV Antibiotics; thus it does not realize the inpatient ward admission category.
- `V0764`: The narrative terminates at ER Sepsis Triage and does not contain any admission step.
- `V0774`: The narrative terminates at ER Sepsis Triage without any patient admission.
- `V0775`: The narrative ends at CRP and contains no admission steps.
- `V0777`: The narrative ends at Leucocytes without including an inpatient ward admission step.
- `V0778`: The process terminates at Leucocytes and lacks any inpatient ward admission activity.
- `V0791`: The narrative stops at IV Antibiotics and lacks any inpatient ward admission step.
- `V0793`: The narrative routes through 'Admission IC' rather than 'Admission NC', thus not realizing the non-critical admission category.
- `V0816`: The narrative terminates at 'IV Antibiotics' without proceeding to inpatient ward admission.
- `V0820`: The narrative terminates at 'LacticAcid' without proceeding to inpatient ward admission.
- `V0832`: The narrative ends at IV Antibiotics without containing any admission to a non-critical inpatient ward task, so it does not realize the category.
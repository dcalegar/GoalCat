# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_axisadmission_pertA_remove_16_rep3` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Admission NC (`admission_nc`)

Patient is admitted to a standard inpatient ward (Admission NC), advancing general care flow towards documented discharge or further disposition.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the single declared alternative under goal 5 (Patient is admitted to an inpatient ward). This alternative is realized in the sample by the Admission NC activity (e.g. in variants V0008, V0625, V0605, V0551, V0449, V0192, V0441, V0317, V0273, V0068, V0145, V0072, V0071, V0070, V0069, V0067, V0066, V0065, V0064, V0063, V0710).

**Goal-model linkage:** 15 (Task): Admission NC

**Coverage:** macro 748/846 variants (88.4%) · micro 800/1050 cases (76.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 12.50, nearest other category `None` at mean distance n/a

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

98/846 variants (11.6%), 250/1050 cases (23.8%) unassigned.

- `V0001`: The narrative stops at ER Sepsis Triage and does not involve admission to a standard inpatient ward (Admission NC).
- `V0002`: The narrative ends with CRP lab work and does not include an inpatient admission.
- `V0003`: The sequence ends with Leucocytes testing and lacks any inpatient ward admission.
- `V0004`: The process terminates at IV Antibiotics administration without proceeding to Admission NC.
- `V0005`: The narrative concludes with LacticAcid testing and does not advance to inpatient admission.
- `V0006`: The process finishes at IV Antibiotics administration without an inpatient admission step.
- `V0007`: The patient receives IV Antibiotics in the emergency context but is not admitted to a standard ward.
- `V0009`: The narrative finishes upon IV Antibiotics delivery and does not show an inpatient admission event.
- `V0010`: The workflow returns to and ends at ER Sepsis Triage without progressing to Admission NC.
- `V0011`: The variant ends with IV Antibiotics administration and lacks any standard ward admission.
- `V0012`: The process sequence concludes with IV Antibiotics and does not involve Admission NC.
- `V0013`: The narrative terminates after Leucocytes testing without proceeding to an inpatient ward.
- `V0017`: The workflow terminates at ER Sepsis Triage and does not include Admission NC.
- `V0019`: The sequence ends with IV Antibiotics and lacks any inpatient ward admission step.
- `V0020`: The narrative terminates at CRP testing without progressing to Admission NC.
- `V0025`: The narrative ends with IV Antibiotics administration and does not contain an inpatient admission event.
- `V0027`: The narrative ends at IV Antibiotics without involving Admission NC.
- `V0029`: The process terminates at Leucocytes and does not reach Admission NC.
- `V0031`: The sequence stops at LacticAcid without any inpatient admission step.
- `V0034`: The narrative ends at IV Liquid and lacks an Admission NC activity.
- `V0036`: The narrative concludes at CRP without reaching Admission NC.
- `V0038`: The narrative terminates at IV Antibiotics without an admission step.
- `V0043`: The sequence terminates at LacticAcid without any admission activity.
- `V0050`: The narrative stops at CRP and does not include Admission NC.
- `V0056`: The narrative ends at 'IV Antibiotics' without proceeding to inpatient ward admission ('Admission NC').
- `V0062`: The narrative terminates at 'IV Antibiotics' without progressing to standard inpatient admission.
- `V0081`: The narrative does not include the 'Admission NC' activity, so it does not realize the category.
- `V0088`: The narrative does not include the 'Admission NC' activity, so it does not realize the category.
- `V0092`: The narrative does not include the 'Admission NC' activity, so it does not realize the category.
- `V0127`: The narrative does not involve an admission to a standard inpatient ward (Admission NC).
- `V0132`: The narrative ends at IV Antibiotics without involving Admission NC.
- `V0133`: The narrative ends at IV Antibiotics and lacks any inpatient ward admission step.
- `V0137`: The narrative terminates at LacticAcid without standard inpatient ward admission.
- `V0145`: The narrative features Admission IC instead of Admission NC.
- `V0146`: The narrative terminates at Leucocytes without involving an inpatient admission.
- `V0148`: The narrative ends at IV Antibiotics without any ward admission activity.
- `V0167`: The narrative contains Admission IC but lacks Admission NC, failing to realize the standard inpatient category.
- `V0187`: The narrative does not include Admission NC.
- `V0197`: The narrative does not include Admission NC.
- `V0217`: The narrative does not contain 'Admission NC' and therefore does not realize the standard inpatient ward admission category.
- `V0218`: The narrative features 'Admission IC' instead of standard inpatient admission ('Admission NC'), so it does not fit the category.
- `V0219`: The narrative lacks 'Admission NC' and terminates early, failing to realize standard inpatient ward admission.
- `V0232`: The narrative terminates at IV Antibiotics without proceeding to admission or standard inpatient care.
- `V0234`: The narrative ends at Leucocytes without reaching any inpatient admission step.
- `V0260`: The narrative ends at IV Antibiotics without involving Admission NC.
- `V0287`: The narrative ends at CRP without reaching Admission NC.
- `V0292`: The narrative terminates at Leucocytes and does not include Admission NC.
- `V0302`: The process terminates at ER Sepsis Triage and does not include an inpatient ward admission.
- `V0305`: The trace stops at IV Antibiotics in the emergency phase without proceeding to an inpatient ward admission.
- `V0322`: The variant ends at IV Antibiotics without any inpatient ward admission.
- `V0325`: The process terminates at IV Antibiotics and does not involve admission to a standard inpatient ward.
- `V0330`: The narrative does not include 'Admission NC', ending at 'IV Liquid'.
- `V0342`: The narrative does not include 'Admission NC', ending at 'CRP'.
- `V0349`: The narrative does not include 'Admission NC', ending at 'ER Sepsis Triage'.
- `V0365`: The narrative does not include an admission to a standard inpatient ward (Admission NC) and instead results in Admission IC and Leucocytes.
- `V0378`: The narrative does not contain 'Admission NC', so it does not realize the category.
- `V0379`: The narrative lacks the 'Admission NC' activity required to realize the category.
- `V0407`: The narrative contains 'Admission IC' instead of 'Admission NC', thus not realizing the category.
- `V0417`: The narrative lacks 'Admission NC', ending with 'ER Triage'.
- `V0429`: The narrative does not include Admission NC, thus it does not realize the standard inpatient admission category.
- `V0432`: The narrative uses Admission IC rather than Admission NC, so it does not realize the standard inpatient ward category.
- `V0488`: The narrative does not contain 'Admission NC' or any standard inpatient ward admission activity.
- `V0492`: The narrative does not contain 'Admission NC' or any standard inpatient ward admission activity.
- `V0495`: The narrative does not contain 'Admission NC' or any standard inpatient ward admission activity.
- `V0507`: The narrative terminates at IV Antibiotics without reaching standard inpatient ward admission.
- `V0510`: The narrative terminates at IV Antibiotics without reaching standard inpatient ward admission.
- `V0516`: The narrative terminates at Leucocytes without reaching standard inpatient ward admission.
- `V0517`: The narrative terminates at ER Triage without reaching standard inpatient ward admission.
- `V0549`: The narrative does not include Admission NC; it terminates at IV Liquid.
- `V0575`: The narrative does not include admission to a standard inpatient ward (Admission NC).
- `V0580`: The narrative does not contain Admission NC, ending in CRP instead.
- `V0584`: The narrative does not reach Admission NC, finishing with IV Liquid.
- `V0585`: The narrative terminates at LacticAcid without any inpatient admission.
- `V0587`: The narrative concludes at CRP without reaching Admission NC.
- `V0592`: The narrative ends at IV Antibiotics without an admission step.
- `V0621`: The narrative only contains Admission IC, lacking Admission NC.
- `V0645`: Admission NC is absent from this variant's sequence.
- `V0654`: The narrative does not include the 'Admission NC' activity; instead, it includes 'Admission IC'.
- `V0664`: The narrative does not contain 'Admission NC'.
- `V0676`: The narrative ends at IV Antibiotics without involving Admission NC.
- `V0679`: The narrative terminates at IV Antibiotics and does not feature admission to a standard inpatient ward.
- `V0685`: The process terminates at IV Antibiotics without an inpatient admission.
- `V0689`: The narrative ends at IV Antibiotics without standard ward admission.
- `V0694`: The narrative terminates early at ER Sepsis Triage.
- `V0713`: The narrative does not include Admission NC, so it does not realize the category.
- `V0715`: The narrative only includes Admission IC, not Admission NC.
- `V0742`: The narrative does not include 'Admission NC' (it terminates at LacticAcid), so it does not realize the standard ward admission category.
- `V0750`: The narrative does not include 'Admission NC' (it terminates at IV Antibiotics), so it does not realize the standard ward admission category.
- `V0759`: The narrative terminates at IV Antibiotics without any standard inpatient ward admission (Admission NC).
- `V0764`: The narrative terminates at ER Sepsis Triage without reaching any standard inpatient ward admission.
- `V0774`: The narrative terminates at ER Sepsis Triage without any admission to a standard inpatient ward.
- `V0775`: The narrative terminates at CRP without any admission to a standard inpatient ward.
- `V0777`: The narrative does not contain Admission NC and does not realize the category.
- `V0778`: The narrative does not contain Admission NC and does not realize the category.
- `V0791`: The narrative does not contain Admission NC and does not realize the category.
- `V0816`: The narrative ends at IV Antibiotics without involving Admission NC.
- `V0820`: The narrative terminates at LacticAcid without any inpatient admission step.
- `V0832`: The narrative terminates at IV Antibiotics without containing Admission NC.
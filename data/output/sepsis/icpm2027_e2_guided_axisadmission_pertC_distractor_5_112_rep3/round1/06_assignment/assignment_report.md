# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_axisadmission_pertC_distractor_5_112_rep3` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Admission NC (`admission_nc`)

Patient is admitted to a normal care inpatient ward. This alternative advances normal care paths and is monitored against post-discharge outcomes.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=15 (Admission NC), appearing frequently in standard inpatient paths such as variant V0008.

**Goal-model linkage:** 15 (Task): Admission NC

**Coverage:** macro 666/846 variants (78.7%) · micro 718/1050 cases (68.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 9.84, nearest other category `admission_ic` at mean distance 22.30

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.406, nearest other category `admission_ic` at mean distance 0.431

## Admission IC (`admission_ic`)

Patient is admitted to an intensive care inpatient ward. This alternative has a negative contribution profile regarding time-to-treatment (Admission IC --[SomeNegative (-25)]--> Minimize time-to-treatment) but handles critical severity cases.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=16 (Admission IC), supported by intensive care pathways such as variant V0605 and V0317.

**Goal-model linkage:** 16 (Task): Admission IC

**Coverage:** macro 92/846 variants (10.9%) · micro 92/1050 cases (8.8%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 26.72, nearest other category `admission_nc` at mean distance 22.30

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.338, nearest other category `admission_nc` at mean distance 0.431

## Admission to High-Dependency Unit (`admission_high_dependency_unit`)

Patient is admitted to a high-dependency unit for specialized intermediate care.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=112 (Admission to High-Dependency Unit). Although sparse in the current sample, following the default rule, lack of sampled narratives is not a reason to fold it.

**Goal-model linkage:** 112 (Task): Admission to High-Dependency Unit

**Coverage:** macro 0/846 variants (0.0%) · micro 0/1050 cases (0.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a, nearest other category `None` at mean distance n/a

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a, nearest other category `None` at mean distance n/a

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0654` / `V0710` (category `admission_ic`): structural=177, profile=0.576
- `V0082` / `V0710` (category `admission_ic`): structural=176, profile=0.680
- `V0710` / `V0742` (category `admission_ic`): structural=176, profile=0.583
- `V0621` / `V0710` (category `admission_ic`): structural=175, profile=0.752
- `V0141` / `V0710` (category `admission_ic`): structural=174, profile=0.418
- `V0407` / `V0710` (category `admission_ic`): structural=174, profile=0.624
- `V0710` / `V0793` (category `admission_ic`): structural=174, profile=0.480
- `V0068` / `V0710` (category `admission_ic`): structural=173, profile=0.509
- `V0639` / `V0710` (category `admission_ic`): structural=173, profile=0.375
- `V0710` / `V0715` (category `admission_ic`): structural=173, profile=0.556

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0051` (`admission_nc`) / `V0391` (`admission_ic`): structural=2, profile=0.172
- `V0082` (`admission_ic`) / `V0156` (`admission_nc`): structural=2, profile=0.025
- `V0082` (`admission_ic`) / `V0400` (`admission_nc`): structural=2, profile=0.333
- `V0082` (`admission_ic`) / `V0451` (`admission_nc`): structural=2, profile=0.012
- `V0008` (`admission_nc`) / `V0082` (`admission_ic`): structural=3, profile=0.340
- `V0040` (`admission_nc`) / `V0082` (`admission_ic`): structural=3, profile=0.759
- `V0044` (`admission_nc`) / `V0793` (`admission_ic`): structural=3, profile=0.151
- `V0076` (`admission_nc`) / `V0621` (`admission_ic`): structural=3, profile=0.389
- `V0077` (`admission_nc`) / `V0407` (`admission_ic`): structural=3, profile=0.173
- `V0082` (`admission_ic`) / `V0110` (`admission_nc`): structural=3, profile=0.774

## Residual

88/846 variants (10.4%), 240/1050 cases (22.9%) unassigned.

- `V0001`: The narrative ends at ER Sepsis Triage without any admission to an inpatient ward or high-dependency unit.
- `V0002`: The narrative stops at diagnostic tests (CRP) and does not show an inpatient admission.
- `V0003`: The narrative concludes with blood tests (Leucocytes) and lacks any ward admission step.
- `V0004`: The process terminates at IV Antibiotics treatment in the emergency setting without subsequent admission.
- `V0005`: The patient receives diagnostic work up ending in LacticAcid, with no inpatient admission recorded.
- `V0006`: The variant finishes upon administering IV Antibiotics in the ER without proceeding to admission.
- `V0007`: The narrative involves ER diagnostics and IV Antibiotics treatment but no admission to a ward.
- `V0009`: The sequence consists of ER care and treatment with IV Antibiotics, stopping short of an inpatient admission.
- `V0010`: This sequence handles initial ER evaluation and tests, concluding at ER Sepsis Triage without ward admission.
- `V0011`: The narrative covers ER assessment, labs, and IV antibiotics, but does not contain an admission step.
- `V0012`: The variant ends with IV Antibiotics administration in the ER department without an inpatient admission.
- `V0013`: The sequence stops at diagnostic lab work (Leucocytes) with no admission activity present.
- `V0017`: The process sequence ends in the ER with ER Sepsis Triage and involves no inpatient admission.
- `V0019`: The narrative is restricted to emergency care and IV antibiotics administration without an admission step.
- `V0020`: The variant concludes with diagnostic blood tests (CRP) in the ER without any inpatient admission.
- `V0025`: The narrative stops after administering IV Antibiotics in the ER and contains no admission activity.
- `V0027`: The narrative ends with 'IV Antibiotics' and does not contain any inpatient admission activity.
- `V0029`: The narrative ends at 'Leucocytes' and does not include an inpatient admission activity.
- `V0031`: The narrative ends with 'LacticAcid' and does not contain an inpatient admission activity.
- `V0034`: The narrative terminates at 'IV Liquid' without an inpatient admission activity.
- `V0036`: The narrative ends with 'CRP' and lacks any inpatient admission activity.
- `V0038`: The narrative terminates at 'IV Antibiotics' without an inpatient admission activity.
- `V0043`: The narrative ends at 'LacticAcid' and lacks any inpatient admission activity.
- `V0050`: The narrative ends at 'CRP' and does not contain an inpatient admission activity.
- `V0056`: The narrative terminates at 'IV Antibiotics' without any inpatient ward admission activity.
- `V0062`: The narrative terminates at 'IV Antibiotics' without any inpatient ward admission activity.
- `V0081`: The narrative terminates at 'IV Liquid' without any inpatient admission activity.
- `V0088`: The narrative terminates at 'IV Antibiotics' without any inpatient admission activity.
- `V0092`: The narrative terminates at 'LacticAcid' without any inpatient admission activity.
- `V0127`: The narrative ends at LacticAcid without any inpatient ward admission activity.
- `V0132`: The narrative ends at IV Antibiotics without involving any inpatient ward admission.
- `V0133`: The narrative ends at IV Antibiotics without inpatient ward admission steps.
- `V0137`: The narrative contains lab tests and treatment in ER but no inpatient admission.
- `V0146`: The narrative stops at Leucocytes without reaching any inpatient admission.
- `V0148`: The narrative ends at IV Antibiotics without any inpatient ward admission step.
- `V0187`: The narrative stops at diagnostic lab tests and does not contain any admission activity, so no category fits.
- `V0197`: The narrative consists only of ER triage and lab tests without any admission step, so no category fits.
- `V0217`: The narrative ends at 'IV Antibiotics' without proceeding to any inpatient admission category.
- `V0219`: The narrative terminates early at 'Leucocytes' without an inpatient admission.
- `V0232`: The narrative ends at IV Antibiotics without any admission activity, so it does not realize any of the defined admission categories.
- `V0234`: The narrative ends at Leucocytes without any admission activity, so it does not realize any of the defined admission categories.
- `V0260`: The variant ends at IV Antibiotics without any admission category.
- `V0287`: The narrative terminates at CRP without any inpatient ward admission activity.
- `V0292`: The narrative terminates at Leucocytes without any inpatient ward admission activity.
- `V0302`: The variant ends at ER Sepsis Triage without any admission activity to inpatient wards or high-dependency units.
- `V0305`: The process terminates at 'IV Antibiotics' within the ER setting without any ward admission.
- `V0322`: The variant ends at 'IV Antibiotics' in the ER without proceeding to any inpatient admission.
- `V0325`: The process terminates at 'IV Antibiotics' in the emergency setting without any ward admission.
- `V0330`: The narrative ends at IV Liquid and does not include any inpatient ward admission activities.
- `V0342`: The narrative stops at CRP and does not contain any ward admission activities.
- `V0349`: The narrative ends at ER Sepsis Triage without proceeding to any inpatient ward admission.
- `V0378`: The process stops at IV Antibiotics and does not reach any inpatient ward admission category.
- `V0379`: The process concludes at IV Antibiotics without any admission to an inpatient ward or high-dependency unit.
- `V0417`: The narrative terminates at ER Triage and does not contain any admission activity (NC, IC, or High-Dependency Unit), so it belongs in the residual.
- `V0429`: The narrative ends with 'IV Antibiotics' and does not contain any ward admission activities.
- `V0488`: The process ends at IV Liquid and contains no admission activity, therefore it does not realize any of the admission categories.
- `V0492`: The process concludes at IV Liquid without any ward admission activity, hence no category fits.
- `V0495`: The process terminates at IV Antibiotics without an inpatient admission step, so no category is realized.
- `V0507`: The narrative ends with 'IV Antibiotics' and does not contain any ward admission activity, so it does not fit any of the taxonomy categories.
- `V0510`: The variant terminates at 'IV Antibiotics' without any admission step, hence no taxonomy category fits.
- `V0516`: The sequence ends at 'Leucocytes' and lacks any admission activity, so it does not match any category.
- `V0517`: The narrative terminates at 'ER Triage' without proceeding to any ward admission, hence it does not fit any category.
- `V0549`: The narrative terminates at IV Liquid without reaching any ward admission category.
- `V0575`: The narrative ends at Leucocytes and lacks any admission activities, thus not fitting any of the taxonomy categories.
- `V0580`: The narrative stops at CRP and contains no admission activity.
- `V0584`: The narrative ends at IV Liquid and lacks any admission activities.
- `V0585`: The narrative ends at LacticAcid and contains no admission steps.
- `V0587`: The narrative terminates at CRP without any admission events.
- `V0592`: The narrative terminates at IV Antibiotics without any admission steps.
- `V0645`: The narrative does not contain any admission activities corresponding to the taxonomy categories.
- `V0664`: The narrative ends at IV Liquid and does not reach any inpatient admission category.
- `V0676`: The narrative ends at IV Antibiotics without any inpatient ward admission activity.
- `V0679`: The narrative terminates at IV Antibiotics without inpatient ward admission.
- `V0685`: The narrative ends at IV Antibiotics without involving any ward admission.
- `V0689`: The narrative terminates at IV Antibiotics without ward admission.
- `V0694`: The narrative ends at ER Sepsis Triage without ward admission.
- `V0713`: The narrative terminates at IV Antibiotics and contains no inpatient ward admission step, thus fitting none of the categories.
- `V0750`: The narrative ends at IV Antibiotics without involving any inpatient ward admission category.
- `V0759`: The case ends with IV Antibiotics and does not contain any ward admission activity.
- `V0764`: The case ends at ER Sepsis Triage and does not contain any inpatient ward admission activity.
- `V0774`: The case ends at ER Sepsis Triage without any ward admission activity.
- `V0775`: The case ends at CRP and does not include any ward admission activity.
- `V0777`: The narrative stops at 'Leucocytes' without any inpatient ward admission event.
- `V0778`: The narrative ends with 'Leucocytes' and does not contain any ward admission.
- `V0791`: The narrative terminates at 'IV Antibiotics' without proceeding to any ward admission.
- `V0816`: The narrative stops at IV Antibiotics without any admission activity, hence it falls into the residual.
- `V0820`: The narrative terminates at LacticAcid without any inpatient admission, hence it belongs to the residual.
- `V0832`: The narrative ends at 'IV Antibiotics' and does not feature any inpatient ward admission category.
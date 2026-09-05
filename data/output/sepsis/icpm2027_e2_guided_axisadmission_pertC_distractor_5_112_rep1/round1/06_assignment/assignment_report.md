# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_axisadmission_pertC_distractor_5_112_rep1` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Admission NC (`admission_nc`)

Admission to normal care ward realizing alternative id=15. Supports standard post-discharge recovery pathways measured against discharge and readmission indicators, though associated with standard ward stays.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=15 (Admission NC) as evidenced in variants such as V0008, V0625, V0605, V0551, V0449, V0192, V0441, V0317, V0273, V0068, V0072, V0071, V0070, V0069, V0067, V0066, V0065, V0064, V0063, and V0710.

**Goal-model linkage:** 15 (Task): Admission NC

**Coverage:** macro 659/846 variants (77.9%) · micro 711/1050 cases (67.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 9.54, nearest other category `admission_ic` at mean distance 22.36

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.406, nearest other category `admission_ic` at mean distance 0.432

## Admission IC (`admission_ic`)

Admission to intensive care unit realizing alternative id=16. Incurs a negative contribution (-25) to minimizing time-to-treatment due to intensive care coordination overhead, evaluated via length of stay and post-discharge return indicators.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=16 (Admission IC) based on sample realizations in complex and critical paths such as variants V0605, V0551, V0317, V0273, V0068, V0145, and V0710.

**Goal-model linkage:** 16 (Task): Admission IC

**Coverage:** macro 99/846 variants (11.7%) · micro 99/1050 cases (9.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 26.82, nearest other category `admission_nc` at mean distance 22.36

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.337, nearest other category `admission_nc` at mean distance 0.432

## Admission to High-Dependency Unit (`admission_high_dependency_unit`)

Admission to a high-dependency unit realizing alternative id=112 for patients requiring intermediate acuity care between normal care and intensive care.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=112 (Admission to High-Dependency Unit). Although no variants in this specific sample trace directly to this leaf due to extreme rarity, folding it into another category is prohibited without co-occurrence evidence.

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

- `V0082` (`admission_ic`) / `V0156` (`admission_nc`): structural=2, profile=0.025
- `V0082` (`admission_ic`) / `V0400` (`admission_nc`): structural=2, profile=0.333
- `V0082` (`admission_ic`) / `V0451` (`admission_nc`): structural=2, profile=0.012
- `V0008` (`admission_nc`) / `V0082` (`admission_ic`): structural=3, profile=0.340
- `V0040` (`admission_nc`) / `V0082` (`admission_ic`): structural=3, profile=0.759
- `V0044` (`admission_nc`) / `V0793` (`admission_ic`): structural=3, profile=0.151
- `V0076` (`admission_nc`) / `V0621` (`admission_ic`): structural=3, profile=0.389
- `V0077` (`admission_nc`) / `V0407` (`admission_ic`): structural=3, profile=0.173
- `V0082` (`admission_ic`) / `V0110` (`admission_nc`): structural=3, profile=0.774
- `V0082` (`admission_ic`) / `V0198` (`admission_nc`): structural=3, profile=0.007

## Residual

88/846 variants (10.4%), 240/1050 cases (22.9%) unassigned.

- `V0001`: The narrative stops at ER Sepsis Triage and does not involve any ward admission.
- `V0002`: The narrative ends at CRP laboratory testing without involving any ward admission.
- `V0003`: The narrative ends with Leucocytes testing and does not include an admission event.
- `V0004`: The narrative ends with IV Antibiotics and contains no hospital admission steps.
- `V0005`: The narrative concludes with LacticAcid testing without any subsequent ward admission.
- `V0006`: The narrative represents emergency treatment up to IV Antibiotics without an admission event.
- `V0007`: The narrative stops at IV Antibiotics in the emergency pathway without a ward admission step.
- `V0009`: The narrative finishes at IV Antibiotics without any admission to a ward.
- `V0010`: The narrative ends at ER Sepsis Triage and has no ward admission activity.
- `V0011`: The narrative concludes at IV Antibiotics without any corresponding hospital admission.
- `V0012`: The narrative stops at IV Antibiotics without an admission event.
- `V0013`: The narrative terminates at Leucocytes testing without proceeding to admission.
- `V0017`: The narrative ends at ER Sepsis Triage without reaching any ward admission.
- `V0019`: The narrative stops at IV Antibiotics without any ward admission activity.
- `V0020`: The narrative ends at CRP testing and does not show an admission step.
- `V0025`: The narrative stops at IV Antibiotics without involving any ward admission.
- `V0027`: The narrative ends with 'IV Antibiotics' and does not contain any ward admission activity.
- `V0029`: The process terminates at 'Leucocytes' without any ward admission step.
- `V0031`: Process ends at 'LacticAcid' with no admission activity present.
- `V0034`: Ends at 'IV Liquid' without any patient ward admission steps.
- `V0036`: Process stops at 'CRP' without an admission activity.
- `V0038`: Terminates at 'IV Antibiotics' without proceeding to ward admission.
- `V0043`: Ends at 'LacticAcid' without any admission step.
- `V0050`: Terminates at 'CRP' without any ward admission activity.
- `V0056`: The narrative does not contain any admission activity, only ending in IV Antibiotics.
- `V0062`: The narrative does not contain any admission activity, ending in IV Antibiotics.
- `V0081`: The narrative does not include any admission activity corresponding to the available categories.
- `V0088`: The narrative does not include any admission activity corresponding to the available categories.
- `V0092`: The narrative does not include any admission activity corresponding to the available categories.
- `V0127`: The narrative ends with 'LacticAcid' and does not contain any ward admission activities matching normal care, intensive care, or high-dependency care.
- `V0132`: The narrative ends at 'IV Antibiotics' without any ward admission steps.
- `V0133`: The process terminates at 'IV Antibiotics' and lacks any admission activities.
- `V0137`: The narrative terminates at 'LacticAcid' and contains no admission-related activities.
- `V0146`: The process terminates at 'Leucocytes' without any admission to a ward.
- `V0148`: The process terminates at 'IV Antibiotics' without any admission step.
- `V0187`: The narrative stops at CRP and does not include any ward or intensive care admission activity.
- `V0197`: The narrative ends with Leucocytes and contains no admission activities.
- `V0217`: The narrative ends at IV Antibiotics without any ward admission activity.
- `V0219`: The narrative ends at Leucocytes without any ward or intensive care admission.
- `V0232`: The narrative stops at IV Antibiotics and contains no ward or ICU admission.
- `V0234`: The narrative stops at Leucocytes without any admission event.
- `V0260`: The narrative ends at IV Antibiotics without any ward or unit admission step.
- `V0287`: The narrative ends at CRP without any ward admission activity, so no category fits.
- `V0292`: The narrative terminates at Leucocytes without any admission event, so none of the categories apply.
- `V0302`: The process terminates at ER Sepsis Triage without any admission event.
- `V0305`: The process terminates at IV Antibiotics without any admission event.
- `V0322`: The process terminates at IV Antibiotics without any admission event.
- `V0325`: The process terminates at IV Antibiotics without any admission event.
- `V0330`: The narrative stops at IV Liquid and does not include any ward or ICU admission activities.
- `V0342`: The narrative ends at CRP and contains no admission activities.
- `V0349`: The narrative terminates at ER Sepsis Triage and does not contain any hospital admission steps.
- `V0378`: The narrative ends with IV Antibiotics and lacks any ward or intensive care admission activity, so no category fits.
- `V0379`: The narrative ends at IV Antibiotics without any admission activity, hence no category applies.
- `V0417`: The narrative does not contain any admission activity, ending at ER Triage, so it fits none of the admission categories.
- `V0429`: The narrative does not contain any admission activity to a ward or unit.
- `V0488`: The narrative ends at IV Liquid without any ward admission activity.
- `V0492`: The narrative ends at IV Liquid without any ward admission activity.
- `V0495`: The narrative ends at IV Antibiotics without any ward admission activity.
- `V0507`: The narrative ends at IV Antibiotics without any ward admission activity, so it does not realize any of the admission categories.
- `V0510`: The process terminates at IV Antibiotics and lacks any admission event, fitting none of the taxonomy categories.
- `V0516`: The sequence stops at Leucocytes without containing any admission event, fitting none of the taxonomy categories.
- `V0517`: The sequence terminates at ER Triage without any admission event, fitting none of the taxonomy categories.
- `V0549`: The narrative ends at IV Liquid and contains no ward or ICU admission events, thus fitting none of the categories.
- `V0575`: The variant ends in Leucocytes without any ward or unit admission activity, thus not realizing any taxonomy category.
- `V0580`: The narrative stops at CRP and does not contain any ward or ICU admission activities.
- `V0584`: The narrative ends with IV Liquid without any admission event.
- `V0585`: The narrative ends with LacticAcid and lacks any hospital admission step.
- `V0587`: The narrative terminates at CRP without an admission activity.
- `V0592`: The narrative terminates at IV Antibiotics without an admission step.
- `V0645`: The narrative does not contain any ward or ICU admission activities.
- `V0664`: The narrative ends at IV Liquid and contains no admission activity.
- `V0676`: The narrative ends at IV Antibiotics without any admission event, so none of the ward admission categories apply.
- `V0679`: The narrative terminates at IV Antibiotics and contains no hospital admission steps.
- `V0685`: The sequence stops at IV Antibiotics without proceeding to ward or ICU admission.
- `V0689`: The narrative ends at IV Antibiotics and lacks any admission category activity.
- `V0694`: The process terminates early at ER Sepsis Triage without any admission.
- `V0713`: The narrative ends at IV Antibiotics without involving any ward admission categories.
- `V0750`: The narrative ends at IV Antibiotics without reaching any ward admission event, hence it does not realize any taxonomy category.
- `V0759`: The narrative ends at IV Antibiotics without any ward or unit admission event.
- `V0764`: Terminates at ER Sepsis Triage without any admission activity.
- `V0774`: Terminates at ER Sepsis Triage without any admission activity.
- `V0775`: Terminates at CRP without any ward or unit admission event.
- `V0777`: The narrative stops at 'Leucocytes' and does not contain any hospital admission activities.
- `V0778`: The process ends at 'Leucocytes' without any admission step.
- `V0791`: Ends at 'IV Antibiotics' without proceeding to any ward or unit admission.
- `V0816`: The narrative ends at IV Antibiotics without any ward admission activity.
- `V0820`: The narrative ends at LacticAcid and lacks any admission activities.
- `V0832`: The narrative ends at IV Antibiotics without involving any ward or unit admission steps, so none of the categories fit.
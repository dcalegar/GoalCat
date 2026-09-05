# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_axisadmission_pertC_distractor_5_112_rep4` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Admission NC (`admission_nc`)

Admission to normal care ward realizing patient inpatient ward admission, advancing general recovery while measuring against post-discharge readmission indicators.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Admission NC (id=15) observed across standard inpatient pathways such as V0008.

**Goal-model linkage:** 15 (Task): Admission NC

**Coverage:** macro 672/846 variants (79.4%) · micro 724/1050 cases (69.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 10.55, nearest other category `admission_ic` at mean distance 20.63

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.407, nearest other category `admission_ic` at mean distance 0.430

## Admission IC (`admission_ic`)

Admission to intensive care unit realizing inpatient ward admission, carrying some negative contribution to minimizing time-to-treatment due to acute stabilization overhead.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Admission IC (id=16) as evidenced by severe path variants like V0605 and V0317.

**Goal-model linkage:** 16 (Task): Admission IC

**Coverage:** macro 86/846 variants (10.2%) · micro 86/1050 cases (8.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 23.76, nearest other category `admission_nc` at mean distance 20.63

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.339, nearest other category `admission_nc` at mean distance 0.430

## Admission to High-Dependency Unit (`admission_high_dependency_unit`)

Admission to a high-dependency unit realizing patient inpatient ward admission for monitored intermediate care.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative Admission to High-Dependency Unit (id=112) representing step-down or intermediate critical care placement.

**Goal-model linkage:** 112 (Task): Admission to High-Dependency Unit

**Coverage:** macro 0/846 variants (0.0%) · micro 0/1050 cases (0.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a, nearest other category `None` at mean distance n/a

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a, nearest other category `None` at mean distance n/a

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0654` / `V0710` (category `admission_ic`): structural=177, profile=0.576
- `V0710` / `V0742` (category `admission_ic`): structural=176, profile=0.583
- `V0621` / `V0710` (category `admission_ic`): structural=175, profile=0.752
- `V0141` / `V0710` (category `admission_ic`): structural=174, profile=0.418
- `V0407` / `V0710` (category `admission_ic`): structural=174, profile=0.624
- `V0710` / `V0793` (category `admission_ic`): structural=174, profile=0.480
- `V0068` / `V0710` (category `admission_ic`): structural=173, profile=0.509
- `V0710` / `V0715` (category `admission_ic`): structural=173, profile=0.556
- `V0154` / `V0710` (category `admission_ic`): structural=172, profile=0.338
- `V0391` / `V0710` (category `admission_ic`): structural=172, profile=0.513

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0051` (`admission_nc`) / `V0391` (`admission_ic`): structural=2, profile=0.172
- `V0044` (`admission_nc`) / `V0793` (`admission_ic`): structural=3, profile=0.151
- `V0076` (`admission_nc`) / `V0621` (`admission_ic`): structural=3, profile=0.389
- `V0077` (`admission_nc`) / `V0407` (`admission_ic`): structural=3, profile=0.173
- `V0154` (`admission_ic`) / `V0466` (`admission_nc`): structural=3, profile=0.479
- `V0189` (`admission_nc`) / `V0837` (`admission_ic`): structural=3, profile=0.006
- `V0382` (`admission_nc`) / `V0837` (`admission_ic`): structural=3, profile=0.464
- `V0391` (`admission_ic`) / `V0466` (`admission_nc`): structural=3, profile=0.206
- `V0391` (`admission_ic`) / `V0769` (`admission_nc`): structural=3, profile=0.139
- `V0413` (`admission_nc`) / `V0621` (`admission_ic`): structural=3, profile=0.852

## Residual

88/846 variants (10.4%), 240/1050 cases (22.9%) unassigned.

- `V0001`: The variant ends at ER Sepsis Triage and does not include any inpatient ward admission.
- `V0002`: The variant ends at CRP and does not include any inpatient ward admission.
- `V0003`: The variant ends at Leucocytes and does not include any inpatient ward admission.
- `V0004`: The variant ends at IV Antibiotics without proceeding to an inpatient ward admission.
- `V0005`: The variant ends at LacticAcid and does not include any inpatient ward admission.
- `V0006`: The variant ends at IV Antibiotics in the ER phase without inpatient ward admission.
- `V0007`: The variant concludes with IV Antibiotics and lacks any inpatient ward admission step.
- `V0009`: The variant terminates at IV Antibiotics and does not feature an admission to a ward.
- `V0010`: The variant ends at ER Sepsis Triage and does not contain any ward admission steps.
- `V0011`: The variant ends at IV Antibiotics and contains no inpatient ward admission.
- `V0012`: The variant ends at IV Antibiotics and does not involve an inpatient ward admission.
- `V0013`: The variant terminates at Leucocytes without advancing to any ward admission.
- `V0017`: The variant ends at ER Sepsis Triage and does not include any inpatient ward admission.
- `V0019`: The variant ends at IV Antibiotics and lacks any inpatient ward admission activity.
- `V0020`: The variant ends at CRP without any inpatient ward admission activity.
- `V0025`: The variant ends at IV Antibiotics and does not involve an inpatient ward admission.
- `V0027`: The narrative terminates at 'IV Antibiotics' without involving any ward admission activities.
- `V0029`: The narrative terminates at laboratory diagnostics ('Leucocytes') without involving any ward admission activities.
- `V0031`: The narrative ends with laboratory results and does not feature any inpatient ward admission steps.
- `V0034`: The narrative concludes after 'IV Liquid' and contains no ward admission process elements.
- `V0036`: The narrative terminates at 'CRP' and lacks any inpatient ward admission activities.
- `V0038`: The narrative ends with 'IV Antibiotics' and does not proceed to inpatient ward admission.
- `V0043`: The narrative terminates at 'LacticAcid' and does not involve any ward admission stages.
- `V0050`: The narrative ends at 'CRP' and lacks any inpatient ward admission steps.
- `V0056`: The narrative ends at 'IV Antibiotics' without proceeding to any inpatient ward admission category.
- `V0062`: The narrative ends at 'IV Antibiotics' without proceeding to any inpatient ward admission category.
- `V0081`: The variant ends at IV Liquid and does not contain any ward admission activities.
- `V0088`: The variant ends at IV Antibiotics and does not contain any ward admission activities.
- `V0092`: The variant ends at LacticAcid and does not contain any ward admission activities.
- `V0127`: The narrative ends at LacticAcid and does not contain any inpatient ward admission activity.
- `V0132`: The narrative stops at IV Antibiotics without any inpatient ward admission.
- `V0133`: The narrative stops at IV Antibiotics without any inpatient ward admission.
- `V0137`: The narrative stops at LacticAcid without any inpatient ward admission.
- `V0146`: The narrative stops at Leucocytes without any inpatient ward admission.
- `V0148`: The narrative stops at IV Antibiotics without any inpatient ward admission.
- `V0187`: The narrative only contains ER triage and diagnostic tests without any inpatient ward admission activity.
- `V0197`: The narrative only contains ER and laboratory activities without any inpatient ward admission.
- `V0217`: The narrative terminates at IV Antibiotics without any ward admission activity.
- `V0219`: The narrative terminates at Leucocytes without any ward admission activity.
- `V0232`: The narrative ends at IV Antibiotics without any ward admission activity.
- `V0234`: The narrative stops at Leucocytes and does not contain any ward admission steps.
- `V0260`: The narrative stops at IV Antibiotics and does not include any ward or ICU admission activity.
- `V0287`: The narrative ends at diagnostic steps without any inpatient ward admission activity.
- `V0292`: The narrative terminates at preliminary diagnostics without any inpatient ward admission.
- `V0302`: The narrative stops at ER Sepsis Triage and does not contain any inpatient ward admission.
- `V0305`: The narrative terminates at IV Antibiotics without any ward admission steps.
- `V0322`: The narrative ends at IV Antibiotics with no inpatient ward admission.
- `V0325`: The narrative terminates at IV Antibiotics without involving any ward admission category.
- `V0330`: The narrative terminates at 'IV Liquid' without any ward admission activity.
- `V0342`: The narrative ends at 'CRP' without any ward admission activity.
- `V0349`: The narrative ends at 'ER Sepsis Triage' without any ward admission.
- `V0378`: The narrative ends at IV Antibiotics without inpatient ward admission.
- `V0379`: The narrative ends at IV Antibiotics without inpatient ward admission.
- `V0417`: The narrative does not contain any inpatient ward admission activity.
- `V0429`: The narrative stops at IV Antibiotics without any ward admission activity.
- `V0488`: The narrative stops at IV Liquid without any inpatient ward admission.
- `V0492`: The narrative stops at IV Liquid without any inpatient ward admission.
- `V0495`: The narrative stops at IV Antibiotics without any inpatient ward admission.
- `V0507`: The narrative does not contain any ward admission activity.
- `V0510`: The narrative does not contain any ward admission activity.
- `V0516`: The narrative does not contain any ward admission activity.
- `V0517`: The narrative does not contain any ward admission activity.
- `V0549`: The narrative ends at IV Liquid and does not contain any ward admission activity.
- `V0575`: The narrative stops at diagnostic lab tests and does not reach any inpatient ward admission category.
- `V0580`: The narrative ends at 'CRP' and does not contain any inpatient ward admission activity.
- `V0584`: The narrative ends at 'IV Liquid' without any inpatient ward admission activity.
- `V0585`: The narrative ends at 'LacticAcid' without any inpatient ward admission activity.
- `V0587`: The narrative ends at 'CRP' without any inpatient ward admission activity.
- `V0592`: The narrative ends at 'IV Antibiotics' without any inpatient ward admission activity.
- `V0645`: The narrative lacks any ward admission activity (such as Admission NC, IC, or high-dependency), meaning it does not realize any of the taxonomy categories.
- `V0664`: The narrative does not contain any admission activity, concluding instead with IV Liquid.
- `V0676`: The narrative ends at IV Antibiotics without any inpatient ward admission activity.
- `V0679`: The narrative terminates at IV Antibiotics without involving any ward admission.
- `V0685`: The narrative ends at IV Antibiotics without any inpatient ward admission.
- `V0689`: The narrative ends at IV Antibiotics without any ward admission activity.
- `V0694`: The narrative terminates early at ER Sepsis Triage with no inpatient admission.
- `V0713`: The narrative terminates at IV Antibiotics without any ward admission activity, so no category fits.
- `V0750`: The narrative does not contain any ward admission steps (Admission NC, IC, or high-dependency unit), ending only at IV Antibiotics.
- `V0759`: The narrative ends at 'IV Antibiotics' and does not contain any inpatient ward admission activities.
- `V0764`: The narrative ends at 'ER Sepsis Triage' and lacks any inpatient ward admission steps.
- `V0774`: The narrative ends at 'ER Sepsis Triage' and does not contain any inpatient ward admission activities.
- `V0775`: The narrative ends at 'CRP' and lacks any inpatient ward admission activities.
- `V0777`: The narrative ends at Leucocytes without any inpatient ward admission activity.
- `V0778`: The narrative ends at Leucocytes without any inpatient ward admission activity.
- `V0791`: The narrative ends at IV Antibiotics without any inpatient ward admission activity.
- `V0816`: The narrative ends at IV Antibiotics without any ward admission activity, so no category fits.
- `V0820`: The narrative ends at LacticAcid without any inpatient ward admission.
- `V0832`: The narrative ends with 'IV Antibiotics' and does not contain any ward admission activity.
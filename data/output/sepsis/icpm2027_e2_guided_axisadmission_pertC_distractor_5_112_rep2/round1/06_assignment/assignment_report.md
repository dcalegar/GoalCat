# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_axisadmission_pertC_distractor_5_112_rep2` | Log: `sepsis` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

846 variants, 1050 cases total.

## Admission Normal Care (`admission_nc`)

Represents standard ward admission for patients requiring ongoing inpatient observation or treatment without intensive care resources. Contributes toward managing overall ward capacity and acts as the baseline path for admitted sepsis pathways.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared goal-model alternative Admission NC (id=15). Evident across numerous sampled variants such as V0008, V0625, and V0070 where patients transition from emergency evaluation to standard inpatient care.

**Goal-model linkage:** 15 (Task): Admission NC

**Coverage:** macro 657/846 variants (77.7%) · micro 709/1050 cases (67.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 9.86, nearest other category `admission_ic` at mean distance 21.24

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.406, nearest other category `admission_ic` at mean distance 0.430

## Admission Intensive Care (`admission_ic`)

Represents admission to the Intensive Care unit for critical stabilization. Carries a negative contribution link (-25) to minimizing time-to-treatment due to specialized coordination overhead, but handles severe acute presentations.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared goal-model alternative Admission IC (id=16). Supported by narrative samples such as V0605, V0317, and V0068 which explicitly realize intensive care admissions.

**Goal-model linkage:** 16 (Task): Admission IC

**Coverage:** macro 101/846 variants (11.9%) · micro 101/1050 cases (9.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 24.52, nearest other category `admission_nc` at mean distance 21.24

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.335, nearest other category `admission_nc` at mean distance 0.430

## Admission to High-Dependency Unit (`admission_high_dependency_unit`)

Represents admission to a high-dependency step-down unit for patients requiring closer monitoring than normal care provides, but not full intensive care.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared goal-model alternative Admission to High-Dependency Unit (id=112). Default representation for this declared OR branch.

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

- `V0001`: This variant only covers ER triage and registration without any admission activity, so it does not realize any of the admission categories.
- `V0002`: This variant ends at CRP diagnostics and does not include an admission step.
- `V0003`: This variant only includes initial ER flow and laboratory tests, without leading to any hospital admission.
- `V0004`: This variant administers IV antibiotics in the ER but does not proceed to admission.
- `V0005`: This variant stops at LacticAcid measurement in the ER without any inpatient admission.
- `V0006`: This variant covers ER treatment and IV antibiotics administration, but lacks an admission step.
- `V0007`: This variant consists of emergency diagnostics and IV antibiotics without an inpatient admission.
- `V0009`: This variant provides initial resuscitation and IV antibiotics in the ER, but results in no recorded admission.
- `V0010`: This variant involves ER evaluation and labs without progressing to admission.
- `V0011`: This variant ends with IV antibiotics in the emergency setting and does not include an admission.
- `V0012`: This variant covers ER care and IV antibiotics without an admission component.
- `V0013`: This variant stops at initial lab work within the emergency department.
- `V0017`: This variant concludes with ER Sepsis Triage and labs, with no admission taking place.
- `V0019`: This variant delivers treatment in the ER without subsequent admission.
- `V0020`: This variant is confined to emergency evaluation and lab testing.
- `V0025`: This variant covers ER diagnostics and IV antibiotics without proceeding to inpatient admission.
- `V0027`: The narrative ends at 'IV Antibiotics' without any admission activity, so it does not realize any of the admission categories.
- `V0029`: The narrative terminates at 'Leucocytes' without any admission step.
- `V0031`: The variant ends at 'LacticAcid' and lacks any admission event.
- `V0034`: The variant concludes at 'IV Liquid' and does not involve any patient admission category.
- `V0036`: The narrative ends at 'CRP' without any admission phase.
- `V0038`: The variant stops at 'IV Antibiotics' and has no admission activity.
- `V0043`: The narrative terminates at 'LacticAcid' and does not feature any admission category.
- `V0050`: The variant ends at 'CRP' without proceeding to any admission category.
- `V0056`: The narrative stops at IV Antibiotics and does not contain any admission activities.
- `V0062`: The variant ends at IV Antibiotics without reaching any hospital admission category.
- `V0081`: The narrative ends at 'IV Liquid' without any admission activity, so it does not realize any of the admission categories.
- `V0088`: The narrative ends at 'IV Antibiotics' without proceeding to any admission category.
- `V0092`: The narrative terminates at 'LacticAcid' without including any admission activity.
- `V0127`: The narrative does not contain any admission activity, terminating in LacticAcid, and therefore does not fit any of the admission categories.
- `V0132`: The variant ends at IV Antibiotics without any ward or ICU admission activities.
- `V0133`: The variant terminates at IV Antibiotics and contains no admission steps.
- `V0137`: The variant ends at LacticAcid and lacks any admission events.
- `V0146`: The variant ends at Leucocytes without an admission step.
- `V0148`: The variant ends at IV Antibiotics without containing any admission activities.
- `V0187`: The narrative terminates early at ER and diagnostic steps without any inpatient admission activity.
- `V0197`: The narrative stops at diagnostic tests in the ER and does not involve any admission category.
- `V0217`: The narrative does not contain any admission activity, ending at IV Antibiotics without realizing any admission category.
- `V0219`: The narrative stops at Leucocytes without including any admission activity, thus realizing no category.
- `V0232`: The narrative terminates at IV Antibiotics without any admission activity, so no admission category fits.
- `V0234`: Ends at Leucocytes without proceeding to any admission category.
- `V0260`: The process terminates at IV Antibiotics without any admission category occurring.
- `V0287`: The narrative does not contain any admission activities, so it does not realize any of the taxonomy categories.
- `V0292`: The narrative does not contain any admission activities, so it does not realize any of the taxonomy categories.
- `V0302`: The narrative ends at 'ER Sepsis Triage' without any inpatient admission activity.
- `V0305`: The narrative ends at 'IV Antibiotics' within the ER phase and does not show an inpatient admission.
- `V0322`: The narrative terminates at 'IV Antibiotics' without any inpatient admission.
- `V0325`: The narrative ends at 'IV Antibiotics' in the emergency phase without an admission step.
- `V0330`: The narrative ends at IV Liquid without any admission activity or transition to ward/ICU care.
- `V0342`: The narrative terminates early at CRP without any admission activity.
- `V0349`: The narrative ends at ER Sepsis Triage and does not proceed to any admission category.
- `V0378`: The narrative terminates at IV Antibiotics without any admission events, thus fitting the residual.
- `V0379`: The narrative ends at IV Antibiotics without involving any ward or intensive care admissions.
- `V0417`: The narrative lacks any admission event, terminating back at ER Triage, hence it belongs to the residual.
- `V0429`: The narrative ends at IV Antibiotics and does not contain any ward or intensive care admission steps.
- `V0488`: The narrative ends at IV Liquid without reaching any admission category.
- `V0492`: The narrative ends at IV Liquid without reaching any admission category.
- `V0495`: The narrative ends at IV Antibiotics without reaching any admission category.
- `V0507`: The narrative does not contain any admission events, ending at 'IV Antibiotics', so none of the admission categories fit.
- `V0510`: The narrative terminates at 'IV Antibiotics' without proceeding to any ward or ICU admission.
- `V0516`: The narrative represents an incomplete or abnormal sequence ending in 'Leucocytes' without any admission step.
- `V0517`: The narrative terminates early at 'ER Triage' and contains no admission events.
- `V0549`: The variant ends at IV Liquid and does not contain any admission activities to normal care, high-dependency, or intensive care.
- `V0575`: The narrative ends at Leucocytes without any admission event, making it part of the residual.
- `V0580`: The narrative ends at CRP testing without an inpatient admission activity.
- `V0584`: The narrative ends at IV Liquid without an inpatient admission step.
- `V0585`: The narrative ends at LacticAcid testing without an admission step.
- `V0587`: The narrative concludes after lab tests without any admission step.
- `V0592`: The narrative ends at IV Antibiotics without an admission step.
- `V0645`: The narrative only covers ER activities and diagnostics without any admission category.
- `V0664`: The narrative does not contain any admission category, ending at IV Liquid.
- `V0676`: The narrative ends at IV Antibiotics without involving any hospital admission activity.
- `V0679`: The narrative terminates at IV Antibiotics without any admission activity.
- `V0685`: The narrative terminates at IV Antibiotics without admission.
- `V0689`: The narrative terminates at IV Antibiotics without any admission step.
- `V0694`: The narrative terminates at ER Sepsis Triage without admission.
- `V0713`: Does not reach any inpatient admission activity, ending at IV Antibiotics in the ER phase.
- `V0750`: The narrative stops at IV Antibiotics without reaching any formal admission category.
- `V0759`: The process terminates at IV Antibiotics without any admission category being realized.
- `V0764`: The process terminates early at ER Sepsis Triage without reaching any admission phase.
- `V0774`: The process terminates at ER Sepsis Triage without reaching any admission category.
- `V0775`: The process terminates at CRP without reaching any admission category.
- `V0777`: The narrative ends at Leucocytes and lacks any admission activity to standard care, ICU, or high-dependency unit.
- `V0778`: The narrative terminates at Leucocytes without an admission step.
- `V0791`: Terminates at 'IV Antibiotics' without proceeding to an admission category.
- `V0816`: The narrative terminates before any admission activity occurs, ending at IV Antibiotics.
- `V0820`: The narrative ends at LacticAcid testing without proceeding to any patient admission.
- `V0832`: The narrative stops at IV Antibiotics and does not contain any ward or intensive care admission steps.
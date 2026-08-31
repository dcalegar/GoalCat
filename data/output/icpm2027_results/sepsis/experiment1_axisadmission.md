# Experiment 1 — sepsis (axis: admission)

## Variant scope (Task C7)

- Policy: `all`
- Variants: 846 of 846 extracted
- Cases: 1050 of 1050
- **Share of the full log's cases covered by this scope: 100.0%**

## Step 5a induction stability (Task C12)

Step 5a reproduced the same category and anchor set across all 5 identical-input reruns; sepsis's figures below are not subject to Task E7's qualification.

## Coverage and residual

| condition                    |   total_variants |   total_cases |   assigned_variants |   assigned_cases |   macro_coverage_C_V |   micro_coverage_C_C |   residual_variants |   residual_variants_pct |   residual_cases |   residual_cases_pct |
|:-----------------------------|-----------------:|--------------:|--------------------:|-----------------:|---------------------:|---------------------:|--------------------:|------------------------:|-----------------:|---------------------:|
| e1_guided_axisadmission_rep1 |              846 |          1050 |                 758 |              810 |             0.895981 |             0.771429 |                  88 |               10.4019   |              240 |             22.8571  |
| e1_guided_axisadmission_rep2 |              846 |          1050 |                 758 |              810 |             0.895981 |             0.771429 |                  88 |               10.4019   |              240 |             22.8571  |
| e1_open_rep1                 |              846 |          1050 |                 841 |             1045 |             0.99409  |             0.995238 |                   5 |                0.591017 |                5 |              0.47619 |
| e1_open_rep2                 |              846 |          1050 |                 835 |             1039 |             0.986998 |             0.989524 |                  11 |                1.30024  |               11 |              1.04762 |

_Higher coverage is not better categorization: a larger taxonomy or a broad catch-all category can trivially raise $C_V$/$C_C$ while carrying less semantic information (Task D2)._

## Declared-alternative coverage (guided arm)

|   anchor_id | declared_alternative   | category_id   |   variants |   cases | status   |
|------------:|:-----------------------|:--------------|-----------:|--------:|:---------|
|          15 | Admission NC           | admission_nc  |        685 |     737 | realized |
|          16 | Admission IC           | admission_ic  |         73 |      73 | realized |

2 of 2 declared alternatives are realized (2 named directly by a category, the rest through their descendants); 0 are realized but carry no variants.

## Contingency — guided vs. open

### Variant counts

| row_category   |   (residual) |   acute_medical_intervention |   chronic_rework_and_readmission |   rapid_triage_and_discharge |   short_inpatient_admission |
|:---------------|-------------:|-----------------------------:|---------------------------------:|-----------------------------:|----------------------------:|
| (residual)     |            2 |                           14 |                                0 |                           72 |                           0 |
| admission_ic   |            1 |                            2 |                               47 |                            3 |                          20 |
| admission_nc   |            2 |                           33 |                              310 |                           18 |                         322 |

### Case-weighted counts

| row_category   |   (residual) |   acute_medical_intervention |   chronic_rework_and_readmission |   rapid_triage_and_discharge |   short_inpatient_admission |
|:---------------|-------------:|-----------------------------:|---------------------------------:|-----------------------------:|----------------------------:|
| (residual)     |            2 |                           59 |                                0 |                          179 |                           0 |
| admission_ic   |            1 |                            2 |                               47 |                            3 |                          20 |
| admission_nc   |            2 |                           33 |                              339 |                           18 |                         345 |

### Merges and splits (§3 evidence item 5)

- Split: admission_ic -> chronic_rework_and_readmission (47), short_inpatient_admission (20), rapid_triage_and_discharge (3), acute_medical_intervention (2), (residual) (1)
- Split: admission_nc -> short_inpatient_admission (322), chronic_rework_and_readmission (310), acute_medical_intervention (33), rapid_triage_and_discharge (18), (residual) (2)
- Merge: admission_nc (33), (residual) (14), admission_ic (2) -> acute_medical_intervention
- Merge: admission_nc (310), admission_ic (47) -> chronic_rework_and_readmission
- Merge: (residual) (72), admission_nc (18), admission_ic (3) -> rapid_triage_and_discharge
- Merge: admission_nc (322), admission_ic (20) -> short_inpatient_admission

## Secondary — guided vs. structural (HDBSCAN) (Task C3)

| row_category   |   (residual) |   cluster_0 |   cluster_1 |   cluster_10 |   cluster_11 |   cluster_12 |   cluster_13 |   cluster_14 |   cluster_15 |   cluster_16 |   cluster_17 |   cluster_18 |   cluster_19 |   cluster_2 |   cluster_20 |   cluster_21 |   cluster_22 |   cluster_23 |   cluster_24 |   cluster_25 |   cluster_26 |   cluster_3 |   cluster_4 |   cluster_5 |   cluster_6 |   cluster_7 |   cluster_8 |   cluster_9 |
|:---------------|-------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|
| (residual)     |            6 |          12 |           8 |            0 |            0 |            0 |            0 |            0 |            0 |            0 |            0 |            0 |            0 |           0 |            0 |            0 |            0 |            0 |            0 |            0 |            0 |           6 |           7 |           0 |           0 |           0 |           0 |          49 |
| admission_ic   |           14 |           0 |           0 |            0 |            0 |            1 |            0 |            0 |            4 |            0 |            2 |            0 |            0 |           0 |            0 |            5 |            0 |            0 |            0 |           25 |           21 |           0 |           0 |           0 |           0 |           1 |           0 |           0 |
| admission_nc   |           35 |           0 |           0 |           10 |           23 |           14 |            6 |            9 |            6 |           29 |            5 |           18 |           12 |          21 |           16 |            3 |            5 |          243 |          173 |           13 |           10 |           0 |           0 |           5 |          10 |           5 |          14 |           0 |

## Replicate stability (Task C2)

rep1 vs. rep2 of each arm, same convention as the paired contrast below. Read the "guided vs. open" divergence against these: a cross-arm difference no larger than an arm's own rep1-rep2 movement is not separable from run-to-run variance. The open arm has no anchors, so this is its only stability check — Task C12 tests the guided taxonomy alone.

### guided rep1 vs. rep2

**guided_rep1 vs. guided_rep2** — partition divergence (Task D1)

| residual_handling   | weighting   |      AMI |      NMI |   n_observations | primary   |
|:--------------------|:------------|---------:|---------:|-----------------:|:----------|
| own_cluster         | variant     | 0.821851 | 0.822548 |              846 | True      |
| own_cluster         | case        | 0.88392  | 0.884211 |             1050 | False     |
| exclude             | variant     | 0.615008 | 0.615824 |              758 | False     |
| exclude             | case        | 0.619454 | 0.620246 |              810 | False     |

_AMI/NMI measure divergence between two partitions, not classification accuracy: neither partition is ground truth, so agreement between the arms is not evidence that either is correct._


### open rep1 vs. rep2

**open_rep1 vs. open_rep2** — partition divergence (Task D1)

| residual_handling   | weighting   |      AMI |      NMI |   n_observations | primary   |
|:--------------------|:------------|---------:|---------:|-----------------:|:----------|
| own_cluster         | variant     | 0.553473 | 0.557082 |              846 | True      |
| own_cluster         | case        | 0.617788 | 0.62006  |             1050 | False     |
| exclude             | variant     | 0.563113 | 0.565251 |              832 | False     |
| exclude             | case        | 0.630909 | 0.632179 |             1036 | False     |

_AMI/NMI measure divergence between two partitions, not classification accuracy: neither partition is ground truth, so agreement between the arms is not evidence that either is correct._


_Read on the D1-primary `own_cluster` convention. Where the open arm's rep1-rep2 AMI is lower than the guided arm's, every "guided vs. open" figure for this dataset should be reported with that band, and the open arm's instability noted as a limit on the strength of the paired contrast (Task E7, extended to the open arm)._

### Replicate residual-set Jaccard (§6)

Jaccard similarity of an arm's two replicate residual variant-sets, on this axis. A value near 1 means the arm puts the same variants outside every category across identical-input reruns; near 0 means it does not. §6 reads the guided-over-open gap as evidence that the declared frame stabilizes the residual boundary, not only the category set.

- guided: 1.00
- open: 0.14

## Partition divergence (optional, Task D1)

**guided vs. open** — partition divergence (Task D1)

| residual_handling   | weighting   |        AMI |       NMI |   n_observations | primary   |
|:--------------------|:------------|-----------:|----------:|-----------------:|:----------|
| own_cluster         | variant     | 0.269784   | 0.273773  |              846 | True      |
| own_cluster         | case        | 0.402372   | 0.40464   |             1050 | False     |
| exclude             | variant     | 0.0094643  | 0.0128    |              755 | False     |
| exclude             | case        | 0.00855873 | 0.0117629 |              807 | False     |

_AMI/NMI measure divergence between two partitions, not classification accuracy: neither partition is ground truth, so agreement between the arms is not evidence that either is correct._


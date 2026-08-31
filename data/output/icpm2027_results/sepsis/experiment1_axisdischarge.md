# Experiment 1 — sepsis (axis: discharge)

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
| e1_guided_axisdischarge_rep1 |              846 |          1050 |                 679 |              728 |             0.8026   |             0.693333 |                 167 |               19.74     |              322 |             30.6667  |
| e1_guided_axisdischarge_rep2 |              846 |          1050 |                 688 |              737 |             0.813239 |             0.701905 |                 158 |               18.6761   |              313 |             29.8095  |
| e1_open_rep1                 |              846 |          1050 |                 841 |             1045 |             0.99409  |             0.995238 |                   5 |                0.591017 |                5 |              0.47619 |
| e1_open_rep2                 |              846 |          1050 |                 835 |             1039 |             0.986998 |             0.989524 |                  11 |                1.30024  |               11 |              1.04762 |

_Higher coverage is not better categorization: a larger taxonomy or a broad catch-all category can trivially raise $C_V$/$C_C$ while carrying less semantic information (Task D2)._

## Declared-alternative coverage (guided arm)

|   anchor_id | declared_alternative   | category_id   |   variants |   cases | status   |
|------------:|:-----------------------|:--------------|-----------:|--------:|:---------|
|          17 | Release A              | release_a     |        569 |     617 | realized |
|          18 | Release B              | release_b     |         55 |      56 | realized |
|          19 | Release C              | release_c     |         25 |      25 | realized |
|          20 | Release D              | release_d     |         24 |      24 | realized |
|          21 | Release E              | release_e     |          6 |       6 | realized |

5 of 5 declared alternatives are realized (5 named directly by a category, the rest through their descendants); 0 are realized but carry no variants.

## Contingency — guided vs. open

### Variant counts

| row_category   |   (residual) |   acute_medical_intervention |   chronic_rework_and_readmission |   rapid_triage_and_discharge |   short_inpatient_admission |
|:---------------|-------------:|-----------------------------:|---------------------------------:|-----------------------------:|----------------------------:|
| (residual)     |            5 |                           19 |                               51 |                           86 |                           6 |
| release_a      |            0 |                           24 |                              269 |                            1 |                         275 |
| release_b      |            0 |                            2 |                                9 |                            6 |                          38 |
| release_c      |            0 |                            2 |                               11 |                            0 |                          12 |
| release_d      |            0 |                            2 |                               14 |                            0 |                           8 |
| release_e      |            0 |                            0 |                                3 |                            0 |                           3 |

### Case-weighted counts

| row_category   |   (residual) |   acute_medical_intervention |   chronic_rework_and_readmission |   rapid_triage_and_discharge |   short_inpatient_admission |
|:---------------|-------------:|-----------------------------:|---------------------------------:|-----------------------------:|----------------------------:|
| (residual)     |            5 |                           64 |                               51 |                          193 |                           9 |
| release_a      |            0 |                           24 |                              298 |                            1 |                         294 |
| release_b      |            0 |                            2 |                                9 |                            6 |                          39 |
| release_c      |            0 |                            2 |                               11 |                            0 |                          12 |
| release_d      |            0 |                            2 |                               14 |                            0 |                           8 |
| release_e      |            0 |                            0 |                                3 |                            0 |                           3 |

### Merges and splits (§3 evidence item 5)

- Split: release_a -> short_inpatient_admission (275), chronic_rework_and_readmission (269), acute_medical_intervention (24), rapid_triage_and_discharge (1)
- Split: release_b -> short_inpatient_admission (38), chronic_rework_and_readmission (9), rapid_triage_and_discharge (6), acute_medical_intervention (2)
- Split: release_c -> short_inpatient_admission (12), chronic_rework_and_readmission (11), acute_medical_intervention (2)
- Split: release_d -> chronic_rework_and_readmission (14), short_inpatient_admission (8), acute_medical_intervention (2)
- Split: release_e -> chronic_rework_and_readmission (3), short_inpatient_admission (3)
- Merge: release_a (24), (residual) (19), release_b (2), release_c (2), release_d (2) -> acute_medical_intervention
- Merge: release_a (269), (residual) (51), release_d (14), release_c (11), release_b (9), release_e (3) -> chronic_rework_and_readmission
- Merge: (residual) (86), release_b (6), release_a (1) -> rapid_triage_and_discharge
- Merge: release_a (275), release_b (38), release_c (12), release_d (8), (residual) (6), release_e (3) -> short_inpatient_admission

## Secondary — guided vs. structural (HDBSCAN) (Task C3)

| row_category   |   (residual) |   cluster_0 |   cluster_1 |   cluster_10 |   cluster_11 |   cluster_12 |   cluster_13 |   cluster_14 |   cluster_15 |   cluster_16 |   cluster_17 |   cluster_18 |   cluster_19 |   cluster_2 |   cluster_20 |   cluster_21 |   cluster_22 |   cluster_23 |   cluster_24 |   cluster_25 |   cluster_26 |   cluster_3 |   cluster_4 |   cluster_5 |   cluster_6 |   cluster_7 |   cluster_8 |   cluster_9 |
|:---------------|-------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|
| (residual)     |           13 |          12 |           8 |            0 |            0 |            0 |            0 |            0 |            0 |            0 |            0 |           18 |            0 |           0 |            3 |            0 |            0 |            0 |           38 |            9 |            0 |           6 |           7 |           1 |           3 |           0 |           0 |          49 |
| release_a      |           18 |           0 |           0 |           10 |           23 |            0 |            0 |            0 |            0 |            0 |            0 |            0 |           12 |          21 |           13 |            8 |            5 |          243 |          135 |           29 |           31 |           0 |           0 |           0 |           7 |           0 |          14 |           0 |
| release_b      |           13 |           0 |           0 |            0 |            0 |            0 |            0 |            0 |            0 |           29 |            7 |            0 |            0 |           0 |            0 |            0 |            0 |            0 |            0 |            0 |            0 |           0 |           0 |           0 |           0 |           6 |           0 |           0 |
| release_c      |            2 |           0 |           0 |            0 |            0 |           15 |            6 |            0 |            0 |            0 |            0 |            0 |            0 |           0 |            0 |            0 |            0 |            0 |            0 |            0 |            0 |           0 |           0 |           2 |           0 |           0 |           0 |           0 |
| release_d      |            4 |           0 |           0 |            0 |            0 |            0 |            0 |            9 |           10 |            0 |            0 |            0 |            0 |           0 |            0 |            0 |            0 |            0 |            0 |            0 |            0 |           0 |           0 |           1 |           0 |           0 |           0 |           0 |
| release_e      |            5 |           0 |           0 |            0 |            0 |            0 |            0 |            0 |            0 |            0 |            0 |            0 |            0 |           0 |            0 |            0 |            0 |            0 |            0 |            0 |            0 |           0 |           0 |           1 |           0 |           0 |           0 |           0 |

## Replicate stability (Task C2)

rep1 vs. rep2 of each arm, same convention as the paired contrast below. Read the "guided vs. open" divergence against these: a cross-arm difference no larger than an arm's own rep1-rep2 movement is not separable from run-to-run variance. The open arm has no anchors, so this is its only stability check — Task C12 tests the guided taxonomy alone.

### guided rep1 vs. rep2

**guided_rep1 vs. guided_rep2** — partition divergence (Task D1)

| residual_handling   | weighting   |      AMI |      NMI |   n_observations | primary   |
|:--------------------|:------------|---------:|---------:|-----------------:|:----------|
| own_cluster         | variant     | 0.788387 | 0.791498 |              846 | True      |
| own_cluster         | case        | 0.818056 | 0.820068 |             1050 | False     |
| exclude             | variant     | 1        | 1        |              659 | False     |
| exclude             | case        | 1        | 1        |              708 | False     |

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

- guided: 0.74
- open: 0.14

## Partition divergence (optional, Task D1)

**guided vs. open** — partition divergence (Task D1)

| residual_handling   | weighting   |       AMI |       NMI |   n_observations | primary   |
|:--------------------|:------------|----------:|----------:|-----------------:|:----------|
| own_cluster         | variant     | 0.219634  | 0.227958  |              846 | True      |
| own_cluster         | case        | 0.313441  | 0.318874  |             1050 | False     |
| exclude             | variant     | 0.034511  | 0.0452904 |              679 | False     |
| exclude             | case        | 0.0354463 | 0.0456386 |              728 | False     |

_AMI/NMI measure divergence between two partitions, not classification accuracy: neither partition is ground truth, so agreement between the arms is not evidence that either is correct._


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
| e1_guided_axisdischarge_rep1 |              846 |          1050 |                 698 |              747 |             0.825059 |             0.711429 |                 148 |               17.4941   |              303 |            28.8571   |
| e1_guided_axisdischarge_rep2 |              846 |          1050 |                 701 |              746 |             0.828605 |             0.710476 |                 145 |               17.1395   |              304 |            28.9524   |
| e1_guided_axisdischarge_rep3 |              846 |          1050 |                 701 |              750 |             0.828605 |             0.714286 |                 145 |               17.1395   |              300 |            28.5714   |
| e1_guided_axisdischarge_rep4 |              846 |          1050 |                 668 |              713 |             0.789598 |             0.679048 |                 178 |               21.0402   |              337 |            32.0952   |
| e1_guided_axisdischarge_rep5 |              846 |          1050 |                 694 |              739 |             0.820331 |             0.70381  |                 152 |               17.9669   |              311 |            29.619    |
| e1_open_rep1                 |              846 |          1050 |                 844 |             1048 |             0.997636 |             0.998095 |                   2 |                0.236407 |                2 |             0.190476 |
| e1_open_rep2                 |              846 |          1050 |                 828 |             1032 |             0.978723 |             0.982857 |                  18 |                2.12766  |               18 |             1.71429  |
| e1_open_rep3                 |              846 |          1050 |                 834 |             1038 |             0.985816 |             0.988571 |                  12 |                1.41844  |               12 |             1.14286  |
| e1_open_rep4                 |              846 |          1050 |                 839 |             1043 |             0.991726 |             0.993333 |                   7 |                0.827423 |                7 |             0.666667 |
| e1_open_rep5                 |              846 |          1050 |                 837 |             1041 |             0.989362 |             0.991429 |                   9 |                1.06383  |                9 |             0.857143 |

_Higher coverage is not better categorization: a larger taxonomy or a broad catch-all category can trivially raise $C_V$/$C_C$ while carrying less semantic information (Task D2)._

## Declared-alternative coverage (guided arm)

|   anchor_id | declared_alternative   | category_id   |   variants |   cases | status   |
|------------:|:-----------------------|:--------------|-----------:|--------:|:---------|
|          17 | Release A              | release_a     |        563 |     607 | realized |
|          18 | Release B              | release_b     |         77 |      82 | realized |
|          19 | Release C              | release_c     |         29 |      29 | realized |
|          20 | Release D              | release_d     |         23 |      23 | realized |
|          21 | Release E              | release_e     |          6 |       6 | realized |

5 of 5 declared alternatives are realized (5 named directly by a category, the rest through their descendants); 0 are realized but carry no variants.

## Contingency — guided vs. open

### Variant counts

| row_category   |   (residual) |   acute_iv_treatment |   chronic_rework_readmission |   fast_triage_only |   standard_admission_release |
|:---------------|-------------:|---------------------:|-----------------------------:|-------------------:|-----------------------------:|
| (residual)     |            2 |                   71 |                           33 |                 40 |                            2 |
| release_a      |            0 |                   14 |                          271 |                  0 |                          278 |
| release_b      |            0 |                    5 |                           35 |                  1 |                           36 |
| release_c      |            0 |                    1 |                           17 |                  0 |                           11 |
| release_d      |            0 |                    0 |                           16 |                  0 |                            7 |
| release_e      |            0 |                    0 |                            3 |                  0 |                            3 |

### Case-weighted counts

| row_category   |   (residual) |   acute_iv_treatment |   chronic_rework_readmission |   fast_triage_only |   standard_admission_release |
|:---------------|-------------:|---------------------:|-----------------------------:|-------------------:|-----------------------------:|
| (residual)     |            2 |                  121 |                           33 |                143 |                            4 |
| release_a      |            0 |                   14 |                          285 |                  0 |                          308 |
| release_b      |            0 |                    5 |                           39 |                  1 |                           37 |
| release_c      |            0 |                    1 |                           17 |                  0 |                           11 |
| release_d      |            0 |                    0 |                           16 |                  0 |                            7 |
| release_e      |            0 |                    0 |                            3 |                  0 |                            3 |

### Merges and splits (§3 evidence item 5)

- Split: release_a -> standard_admission_release (278), chronic_rework_readmission (271), acute_iv_treatment (14)
- Split: release_b -> standard_admission_release (36), chronic_rework_readmission (35), acute_iv_treatment (5), fast_triage_only (1)
- Split: release_c -> chronic_rework_readmission (17), standard_admission_release (11), acute_iv_treatment (1)
- Split: release_d -> chronic_rework_readmission (16), standard_admission_release (7)
- Split: release_e -> chronic_rework_readmission (3), standard_admission_release (3)
- Merge: (residual) (71), release_a (14), release_b (5), release_c (1) -> acute_iv_treatment
- Merge: release_a (271), release_b (35), (residual) (33), release_c (17), release_d (16), release_e (3) -> chronic_rework_readmission
- Merge: (residual) (40), release_b (1) -> fast_triage_only
- Merge: release_a (278), release_b (36), release_c (11), release_d (7), release_e (3), (residual) (2) -> standard_admission_release

## Secondary — guided vs. structural (HDBSCAN) (Task C3)

| row_category   |   (residual) |   cluster_0 |   cluster_1 |   cluster_10 |   cluster_11 |   cluster_12 |   cluster_13 |   cluster_14 |   cluster_15 |   cluster_16 |   cluster_17 |   cluster_18 |   cluster_19 |   cluster_2 |   cluster_20 |   cluster_21 |   cluster_22 |   cluster_23 |   cluster_24 |   cluster_25 |   cluster_26 |   cluster_3 |   cluster_4 |   cluster_5 |   cluster_6 |   cluster_7 |   cluster_8 |   cluster_9 |
|:---------------|-------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|
| (residual)     |           14 |          12 |           8 |            0 |            0 |            0 |            1 |            0 |            1 |            0 |            0 |           18 |            1 |           1 |            3 |            0 |            1 |            0 |           21 |            4 |            0 |           6 |           7 |           1 |           0 |           0 |           0 |          49 |
| release_a      |           18 |           0 |           0 |           10 |           23 |            0 |            0 |            0 |            0 |            0 |            0 |            0 |            9 |          20 |           11 |            8 |            4 |          243 |          137 |           26 |           30 |           0 |           0 |           0 |          10 |           0 |          14 |           0 |
| release_b      |           12 |           0 |           0 |            0 |            0 |            0 |            0 |            0 |            0 |           29 |            7 |            0 |            2 |           0 |            2 |            0 |            0 |            0 |           14 |            5 |            0 |           0 |           0 |           0 |           0 |           6 |           0 |           0 |
| release_c      |            2 |           0 |           0 |            0 |            0 |           15 |            5 |            0 |            0 |            0 |            0 |            0 |            0 |           0 |            0 |            0 |            0 |            0 |            1 |            3 |            1 |           0 |           0 |           2 |           0 |           0 |           0 |           0 |
| release_d      |            4 |           0 |           0 |            0 |            0 |            0 |            0 |            9 |            9 |            0 |            0 |            0 |            0 |           0 |            0 |            0 |            0 |            0 |            0 |            0 |            0 |           0 |           0 |           1 |           0 |           0 |           0 |           0 |
| release_e      |            5 |           0 |           0 |            0 |            0 |            0 |            0 |            0 |            0 |            0 |            0 |            0 |            0 |           0 |            0 |            0 |            0 |            0 |            0 |            0 |            0 |           0 |           0 |           1 |           0 |           0 |           0 |           0 |

## Replicate stability (Task C2)

rep1 vs. rep2 of each arm, same convention as the paired contrast below. Read the "guided vs. open" divergence against these: a cross-arm difference no larger than an arm's own rep1-rep2 movement is not separable from run-to-run variance. The open arm has no anchors, so this is its only stability check — Task C12 tests the guided taxonomy alone.

### guided rep1 vs. rep2

**guided_rep1 vs. guided_rep2** — partition divergence (Task D1)

| residual_handling   | weighting   |      AMI |      NMI |   n_observations | primary   |
|:--------------------|:------------|---------:|---------:|-----------------:|:----------|
| own_cluster         | variant     | 0.69327  | 0.697711 |              846 | True      |
| own_cluster         | case        | 0.731112 | 0.734022 |             1050 | False     |
| exclude             | variant     | 0.83495  | 0.837783 |              674 | False     |
| exclude             | case        | 0.836984 | 0.839692 |              719 | False     |

_AMI/NMI measure divergence between two partitions, not classification accuracy: neither partition is ground truth, so agreement between the arms is not evidence that either is correct._


### open rep1 vs. rep2

**open_rep1 vs. open_rep2** — partition divergence (Task D1)

| residual_handling   | weighting   |      AMI |      NMI |   n_observations | primary   |
|:--------------------|:------------|---------:|---------:|-----------------:|:----------|
| own_cluster         | variant     | 0.495115 | 0.499253 |              846 | True      |
| own_cluster         | case        | 0.600631 | 0.602945 |             1050 | False     |
| exclude             | variant     | 0.500825 | 0.503537 |              826 | False     |
| exclude             | case        | 0.618626 | 0.619985 |             1030 | False     |

_AMI/NMI measure divergence between two partitions, not classification accuracy: neither partition is ground truth, so agreement between the arms is not evidence that either is correct._


_Read on the D1-primary `own_cluster` convention. Where the open arm's rep1-rep2 AMI is lower than the guided arm's, every "guided vs. open" figure for this dataset should be reported with that band, and the open arm's instability noted as a limit on the strength of the paired contrast (Task E7, extended to the open arm)._

### Replicate residual-set Jaccard (§6)

Jaccard similarity of an arm's two replicate residual variant-sets, on this axis. A value near 1 means the arm puts the same variants outside every category across identical-input reruns; near 0 means it does not. §6 reads the guided-over-open gap as evidence that the declared frame stabilizes the residual boundary, not only the category set.

- guided: 0.70
- open: 0.00

## Partition divergence (optional, Task D1)

**guided vs. open** — partition divergence (Task D1)

| residual_handling   | weighting   |        AMI |       NMI |   n_observations | primary   |
|:--------------------|:------------|-----------:|----------:|-----------------:|:----------|
| own_cluster         | variant     | 0.23478    | 0.242548  |              846 | True      |
| own_cluster         | case        | 0.347363   | 0.352259  |             1050 | False     |
| exclude             | variant     | 0.00431386 | 0.0133934 |              698 | False     |
| exclude             | case        | 0.00493672 | 0.013476  |              747 | False     |

_AMI/NMI measure divergence between two partitions, not classification accuracy: neither partition is ground truth, so agreement between the arms is not evidence that either is correct._


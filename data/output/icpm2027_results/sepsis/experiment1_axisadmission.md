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
| e1_guided_axisadmission_rep1 |              846 |          1050 |                 758 |              810 |             0.895981 |             0.771429 |                  88 |               10.4019   |              240 |            22.8571   |
| e1_guided_axisadmission_rep2 |              846 |          1050 |                 758 |              810 |             0.895981 |             0.771429 |                  88 |               10.4019   |              240 |            22.8571   |
| e1_guided_axisadmission_rep3 |              846 |          1050 |                 758 |              810 |             0.895981 |             0.771429 |                  88 |               10.4019   |              240 |            22.8571   |
| e1_guided_axisadmission_rep4 |              846 |          1050 |                 758 |              810 |             0.895981 |             0.771429 |                  88 |               10.4019   |              240 |            22.8571   |
| e1_guided_axisadmission_rep5 |              846 |          1050 |                 758 |              810 |             0.895981 |             0.771429 |                  88 |               10.4019   |              240 |            22.8571   |
| e1_open_rep1                 |              846 |          1050 |                 844 |             1048 |             0.997636 |             0.998095 |                   2 |                0.236407 |                2 |             0.190476 |
| e1_open_rep2                 |              846 |          1050 |                 828 |             1032 |             0.978723 |             0.982857 |                  18 |                2.12766  |               18 |             1.71429  |
| e1_open_rep3                 |              846 |          1050 |                 834 |             1038 |             0.985816 |             0.988571 |                  12 |                1.41844  |               12 |             1.14286  |
| e1_open_rep4                 |              846 |          1050 |                 839 |             1043 |             0.991726 |             0.993333 |                   7 |                0.827423 |                7 |             0.666667 |
| e1_open_rep5                 |              846 |          1050 |                 837 |             1041 |             0.989362 |             0.991429 |                   9 |                1.06383  |                9 |             0.857143 |

_Higher coverage is not better categorization: a larger taxonomy or a broad catch-all category can trivially raise $C_V$/$C_C$ while carrying less semantic information (Task D2)._

## Declared-alternative coverage (guided arm)

|   anchor_id | declared_alternative   | category_id   |   variants |   cases | status   |
|------------:|:-----------------------|:--------------|-----------:|--------:|:---------|
|          15 | Admission NC           | admission_nc  |        669 |     721 | realized |
|          16 | Admission IC           | admission_ic  |         89 |      89 | realized |

2 of 2 declared alternatives are realized (2 named directly by a category, the rest through their descendants); 0 are realized but carry no variants.

## Contingency — guided vs. open

### Variant counts

| row_category   |   (residual) |   acute_iv_treatment |   chronic_rework_readmission |   fast_triage_only |   standard_admission_release |
|:---------------|-------------:|---------------------:|-----------------------------:|-------------------:|-----------------------------:|
| (residual)     |            0 |                   49 |                            0 |                 39 |                            0 |
| admission_ic   |            0 |                    5 |                           64 |                  0 |                           20 |
| admission_nc   |            2 |                   37 |                          311 |                  2 |                          317 |

### Case-weighted counts

| row_category   |   (residual) |   acute_iv_treatment |   chronic_rework_readmission |   fast_triage_only |   standard_admission_release |
|:---------------|-------------:|---------------------:|-----------------------------:|-------------------:|-----------------------------:|
| (residual)     |            0 |                   98 |                            0 |                142 |                            0 |
| admission_ic   |            0 |                    5 |                           64 |                  0 |                           20 |
| admission_nc   |            2 |                   38 |                          329 |                  2 |                          350 |

### Merges and splits (§3 evidence item 5)

- Split: admission_ic -> chronic_rework_readmission (64), standard_admission_release (20), acute_iv_treatment (5)
- Split: admission_nc -> standard_admission_release (317), chronic_rework_readmission (311), acute_iv_treatment (37), (residual) (2), fast_triage_only (2)
- Merge: (residual) (49), admission_nc (37), admission_ic (5) -> acute_iv_treatment
- Merge: admission_nc (311), admission_ic (64) -> chronic_rework_readmission
- Merge: (residual) (39), admission_nc (2) -> fast_triage_only
- Merge: admission_nc (317), admission_ic (20) -> standard_admission_release

## Secondary — guided vs. structural (HDBSCAN) (Task C3)

| row_category   |   (residual) |   cluster_0 |   cluster_1 |   cluster_10 |   cluster_11 |   cluster_12 |   cluster_13 |   cluster_14 |   cluster_15 |   cluster_16 |   cluster_17 |   cluster_18 |   cluster_19 |   cluster_2 |   cluster_20 |   cluster_21 |   cluster_22 |   cluster_23 |   cluster_24 |   cluster_25 |   cluster_26 |   cluster_3 |   cluster_4 |   cluster_5 |   cluster_6 |   cluster_7 |   cluster_8 |   cluster_9 |
|:---------------|-------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|
| (residual)     |            6 |          12 |           8 |            0 |            0 |            0 |            0 |            0 |            0 |            0 |            0 |            0 |            0 |           0 |            0 |            0 |            0 |            0 |            0 |            0 |            0 |           6 |           7 |           0 |           0 |           0 |           0 |          49 |
| admission_ic   |           18 |           0 |           0 |            0 |            0 |            0 |            0 |            0 |            5 |            0 |            6 |            0 |            0 |           0 |            0 |            8 |            0 |            0 |            0 |           26 |           25 |           0 |           0 |           0 |           0 |           1 |           0 |           0 |
| admission_nc   |           31 |           0 |           0 |           10 |           23 |           15 |            6 |            9 |            5 |           29 |            1 |           18 |           12 |          21 |           16 |            0 |            5 |          243 |          173 |           12 |            6 |           0 |           0 |           5 |          10 |           5 |          14 |           0 |

## Replicate stability (Task C2)

rep1 vs. rep2 of each arm, same convention as the paired contrast below. Read the "guided vs. open" divergence against these: a cross-arm difference no larger than an arm's own rep1-rep2 movement is not separable from run-to-run variance. The open arm has no anchors, so this is its only stability check — Task C12 tests the guided taxonomy alone.

### guided rep1 vs. rep2

**guided_rep1 vs. guided_rep2** — partition divergence (Task D1)

| residual_handling   | weighting   |      AMI |      NMI |   n_observations | primary   |
|:--------------------|:------------|---------:|---------:|-----------------:|:----------|
| own_cluster         | variant     | 0.842215 | 0.84278  |              846 | True      |
| own_cluster         | case        | 0.894428 | 0.894676 |             1050 | False     |
| exclude             | variant     | 0.687407 | 0.687961 |              758 | False     |
| exclude             | case        | 0.691635 | 0.692169 |              810 | False     |

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

- guided: 1.00
- open: 0.00

## Partition divergence (optional, Task D1)

**guided vs. open** — partition divergence (Task D1)

| residual_handling   | weighting   |       AMI |       NMI |   n_observations | primary   |
|:--------------------|:------------|----------:|----------:|-----------------:|:----------|
| own_cluster         | variant     | 0.291836  | 0.295502  |              846 | True      |
| own_cluster         | case        | 0.434322  | 0.436374  |             1050 | False     |
| exclude             | variant     | 0.0211195 | 0.0241595 |              756 | False     |
| exclude             | case        | 0.022048  | 0.0249107 |              808 | False     |

_AMI/NMI measure divergence between two partitions, not classification accuracy: neither partition is ground truth, so agreement between the arms is not evidence that either is correct._


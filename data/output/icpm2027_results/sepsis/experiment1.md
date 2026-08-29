# Experiment 1 — sepsis

## Variant scope (Task C7)

- Policy: `all`
- Variants: 846 of 846 extracted
- Cases: 1050 of 1050
- **Share of the full log's cases covered by this scope: 100.0%**

## Step 5a induction stability (Task C12)

Step 5a reproduced the same category and anchor set across all 5 identical-input reruns; sepsis's figures below are not subject to Task E7's qualification.

## Coverage and residual

| condition                |   total_variants |   total_cases |   assigned_variants |   assigned_cases |   macro_coverage_C_V |   micro_coverage_C_C |   residual_variants |   residual_variants_pct |   residual_cases |   residual_cases_pct |
|:-------------------------|-----------------:|--------------:|--------------------:|-----------------:|---------------------:|---------------------:|--------------------:|------------------------:|-----------------:|---------------------:|
| e1_guided_no_sample_rep1 |              846 |          1050 |                 756 |              808 |             0.893617 |             0.769524 |                  90 |                10.6383  |              242 |             23.0476  |
| e1_guided_no_sample_rep2 |              846 |          1050 |                 755 |              807 |             0.892435 |             0.768571 |                  91 |                10.7565  |              243 |             23.1429  |
| e1_guided_rep1           |              846 |          1050 |                 734 |              786 |             0.867612 |             0.748571 |                 112 |                13.2388  |              264 |             25.1429  |
| e1_guided_rep2           |              846 |          1050 |                 659 |              711 |             0.77896  |             0.677143 |                 187 |                22.104   |              339 |             32.2857  |
| e1_open_rep1             |              846 |          1050 |                 835 |             1039 |             0.986998 |             0.989524 |                  11 |                 1.30024 |               11 |              1.04762 |
| e1_open_rep2             |              846 |          1050 |                 819 |             1023 |             0.968085 |             0.974286 |                  27 |                 3.19149 |               27 |              2.57143 |

_Higher coverage is not better categorization: a larger taxonomy or a broad catch-all category can trivially raise $C_V$/$C_C$ while carrying less semantic information (Task D2)._

## Declared-alternative coverage (guided arm)

|   anchor_id | declared_alternative   | category_id   |   variants |   cases | status   |
|------------:|:-----------------------|:--------------|-----------:|--------:|:---------|
|          15 | Admission NC           | admission_nc  |         50 |      53 | realized |
|          16 | Admission IC           | admission_ic  |         31 |      31 | realized |
|          17 | Release A              | release_a     |        546 |     594 | realized |
|          18 | Release B              | release_b     |         54 |      55 | realized |
|          19 | Release C              | release_c     |         25 |      25 | realized |
|          20 | Release D              | release_d     |         22 |      22 | realized |
|          21 | Release E              | release_e     |          6 |       6 | realized |

7 of 7 declared alternatives are realized (7 named directly by a category, the rest through their descendants); 0 are realized but carry no variants.

## Contingency — guided vs. open

### Variant counts

| row_category   |   (residual) |   acute_iv_treatment |   chronic_rework_readmission |   fast_er_triage |   standard_admission_release |
|:---------------|-------------:|---------------------:|-----------------------------:|-----------------:|-----------------------------:|
| (residual)     |            7 |                   42 |                           17 |               46 |                            0 |
| admission_ic   |            0 |                    1 |                           21 |                0 |                            9 |
| admission_nc   |            4 |                    9 |                            4 |                1 |                           32 |
| release_a      |            0 |                    8 |                          164 |                0 |                          374 |
| release_b      |            0 |                    7 |                           10 |                1 |                           36 |
| release_c      |            0 |                    0 |                            7 |                0 |                           18 |
| release_d      |            0 |                    0 |                           12 |                0 |                           10 |
| release_e      |            0 |                    0 |                            3 |                0 |                            3 |

### Case-weighted counts

| row_category   |   (residual) |   acute_iv_treatment |   chronic_rework_readmission |   fast_er_triage |   standard_admission_release |
|:---------------|-------------:|---------------------:|-----------------------------:|-----------------:|-----------------------------:|
| (residual)     |            7 |                   90 |                           17 |              150 |                            0 |
| admission_ic   |            0 |                    1 |                           21 |                0 |                            9 |
| admission_nc   |            4 |                    9 |                            4 |                1 |                           35 |
| release_a      |            0 |                    8 |                          187 |                0 |                          399 |
| release_b      |            0 |                    7 |                           10 |                1 |                           37 |
| release_c      |            0 |                    0 |                            7 |                0 |                           18 |
| release_d      |            0 |                    0 |                           12 |                0 |                           10 |
| release_e      |            0 |                    0 |                            3 |                0 |                            3 |

### Merges and splits (§3 evidence item 5)

- Split: admission_ic -> chronic_rework_readmission (21), standard_admission_release (9), acute_iv_treatment (1)
- Split: admission_nc -> standard_admission_release (32), acute_iv_treatment (9), (residual) (4), chronic_rework_readmission (4), fast_er_triage (1)
- Split: release_a -> standard_admission_release (374), chronic_rework_readmission (164), acute_iv_treatment (8)
- Split: release_b -> standard_admission_release (36), chronic_rework_readmission (10), acute_iv_treatment (7), fast_er_triage (1)
- Split: release_c -> standard_admission_release (18), chronic_rework_readmission (7)
- Split: release_d -> chronic_rework_readmission (12), standard_admission_release (10)
- Split: release_e -> chronic_rework_readmission (3), standard_admission_release (3)
- Merge: (residual) (42), admission_nc (9), release_a (8), release_b (7), admission_ic (1) -> acute_iv_treatment
- Merge: release_a (164), admission_ic (21), (residual) (17), release_d (12), release_b (10), release_c (7), admission_nc (4), release_e (3) -> chronic_rework_readmission
- Merge: (residual) (46), admission_nc (1), release_b (1) -> fast_er_triage
- Merge: release_a (374), release_b (36), admission_nc (32), release_c (18), release_d (10), admission_ic (9), release_e (3) -> standard_admission_release

## Secondary — guided vs. structural (HDBSCAN) (Task C3)

| row_category   |   (residual) |   cluster_0 |   cluster_1 |   cluster_10 |   cluster_11 |   cluster_2 |   cluster_3 |   cluster_4 |   cluster_5 |   cluster_6 |   cluster_7 |   cluster_8 |   cluster_9 |
|:---------------|-------------:|------------:|------------:|-------------:|-------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|
| (residual)     |            7 |          12 |           8 |           16 |            0 |           7 |          53 |           0 |           0 |           0 |           1 |           8 |           0 |
| admission_ic   |            3 |           0 |           0 |           24 |            2 |           0 |           0 |           0 |           0 |           2 |           0 |           0 |           0 |
| admission_nc   |            5 |           0 |           0 |           24 |            0 |           0 |           2 |           6 |           0 |           0 |           3 |          10 |           0 |
| release_a      |            6 |           0 |           0 |          437 |            0 |           0 |           0 |          51 |           0 |           4 |          48 |           0 |           0 |
| release_b      |            2 |           0 |           0 |            0 |            0 |           0 |           0 |           0 |           7 |           1 |           0 |           0 |          44 |
| release_c      |            0 |           0 |           0 |           20 |            0 |           0 |           0 |           4 |           0 |           0 |           1 |           0 |           0 |
| release_d      |            2 |           0 |           0 |            0 |           17 |           0 |           0 |           3 |           0 |           0 |           0 |           0 |           0 |
| release_e      |            0 |           0 |           0 |            3 |            0 |           0 |           0 |           3 |           0 |           0 |           0 |           0 |           0 |

## Partition divergence (optional, Task D1)

**guided vs. open** — partition divergence (Task D1)

| residual_handling   | weighting   |       AMI |       NMI |   n_observations | primary   |
|:--------------------|:------------|----------:|----------:|-----------------:|:----------|
| own_cluster         | variant     | 0.252896  | 0.263848  |              846 | True      |
| own_cluster         | case        | 0.370895  | 0.377582  |             1050 | False     |
| exclude             | variant     | 0.0531526 | 0.0646805 |              730 | False     |
| exclude             | case        | 0.0522891 | 0.0631734 |              782 | False     |

_AMI/NMI measure divergence between two partitions, not classification accuracy: neither partition is ground truth, so agreement between the arms is not evidence that either is correct._


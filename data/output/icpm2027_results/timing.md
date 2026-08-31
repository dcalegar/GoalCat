**Pipeline timing (Task C9)** — feasibility/scalability characterization

Per-run summary:

| dataset   | run_id                                    | complete   |   n_steps |   total_duration_s |   total_llm_calls |   total_llm_latency_s |
|:----------|:------------------------------------------|:-----------|----------:|-------------------:|------------------:|----------------------:|
| rtfm      | icpm2027_base                             | True       |         4 |              67.91 |                 0 |                  0    |
| rtfm      | icpm2027_c12_guided_stability_rep1        | True       |         1 |              81.76 |                 1 |                 79.98 |
| rtfm      | icpm2027_c12_guided_stability_rep2        | True       |         1 |               4.74 |                 1 |                  2.97 |
| rtfm      | icpm2027_c12_guided_stability_rep3        | True       |         1 |              71.81 |                 1 |                 70.06 |
| rtfm      | icpm2027_c12_guided_stability_rep4        | True       |         1 |              49.21 |                 1 |                 47.5  |
| rtfm      | icpm2027_c12_guided_stability_rep5        | True       |         1 |               5.8  |                 1 |                  4.1  |
| rtfm      | icpm2027_e1_guided_no_sample_rep1         | True       |         3 |            1114.12 |                 6 |                 55.82 |
| rtfm      | icpm2027_e1_guided_no_sample_rep2         | True       |         3 |             237.85 |                 6 |                131.37 |
| rtfm      | icpm2027_e1_guided_rep1                   | True       |         3 |             464.55 |                 6 |                420.95 |
| rtfm      | icpm2027_e1_guided_rep2                   | True       |         3 |             337.37 |                 6 |                213.2  |
| rtfm      | icpm2027_e1_open_rep1                     | False      |         3 |             nan    |                 6 |                145.63 |
| rtfm      | icpm2027_e1_open_rep2                     | True       |         2 |              28.68 |                 6 |                 67.38 |
| rtfm      | icpm2027_e2_guided_pertA_remove_19_rep1   | True       |         3 |             333.67 |                 6 |                957.22 |
| rtfm      | icpm2027_e2_guided_pertB_merge_13_20_rep1 | True       |         3 |             131.57 |                 6 |                 77.45 |
| sepsis    | icpm2027_base                             | True       |         4 |              12.01 |                 0 |                  0    |
| sepsis    | icpm2027_c12_guided_stability_rep1        | True       |         2 |             769.35 |                 2 |                 62.9  |
| sepsis    | icpm2027_c12_guided_stability_rep2        | True       |         2 |             720.59 |                 2 |                116.43 |
| sepsis    | icpm2027_c12_guided_stability_rep3        | True       |         2 |             613.32 |                 2 |                 26.77 |
| sepsis    | icpm2027_c12_guided_stability_rep4        | True       |         2 |             244.16 |                 2 |                 10.61 |
| sepsis    | icpm2027_c12_guided_stability_rep5        | False      |         2 |             nan    |                 1 |                  5.33 |
| sepsis    | icpm2027_e1_guided_no_sample_rep1         | True       |         2 |              37.32 |                18 |                138.89 |
| sepsis    | icpm2027_e1_guided_no_sample_rep2         | True       |         2 |              35.76 |                18 |                136.55 |
| sepsis    | icpm2027_e1_guided_rep1                   | True       |         2 |              35.63 |                18 |                141.22 |
| sepsis    | icpm2027_e1_guided_rep2                   | True       |         2 |              54.8  |                18 |                141.93 |
| sepsis    | icpm2027_e1_open_rep1                     | True       |         2 |             126.82 |                18 |                451.6  |
| sepsis    | icpm2027_e1_open_rep2                     | True       |         2 |             105.85 |                18 |                402.98 |
| sepsis    | icpm2027_e2_guided_pertA_remove_21_rep1   | True       |         2 |              81.89 |                18 |                225.68 |
| sepsis    | icpm2027_e2_guided_pertB_merge_15_16_rep1 | True       |         2 |             247.59 |                18 |                824.5  |
| bpic2019  | icpm2027_base                             | True       |         4 |             290.65 |                 0 |                  0    |
| bpic2019  | icpm2027_c12_guided_stability_rep1        | True       |         1 |             116.01 |                 1 |                114.64 |
| bpic2019  | icpm2027_c12_guided_stability_rep2        | True       |         1 |             104.87 |                 1 |                103.86 |
| bpic2019  | icpm2027_c12_guided_stability_rep3        | True       |         1 |              38.03 |                 1 |                 37.04 |
| bpic2019  | icpm2027_c12_guided_stability_rep4        | True       |         1 |              34.6  |                 1 |                 33.59 |
| bpic2019  | icpm2027_c12_guided_stability_rep5        | True       |         1 |              25.01 |                 1 |                 24.02 |
| bpic2019  | icpm2027_e1_guided_no_sample_rep1         | True       |         2 |            1572.78 |               480 |               4987.53 |
| bpic2019  | icpm2027_e1_guided_no_sample_rep2         | False      |         3 |             nan    |               481 |               6339.21 |
| bpic2019  | icpm2027_e1_guided_rep1                   | True       |         2 |            1133.14 |               480 |               4180.76 |
| bpic2019  | icpm2027_e1_guided_rep2                   | True       |         2 |            1531.23 |               480 |               4652.4  |
| bpic2019  | icpm2027_e1_open_rep1                     | False      |         3 |             nan    |               481 |               5191.45 |
| bpic2019  | icpm2027_e1_open_rep2                     | True       |         2 |            2113.81 |               480 |               7327.68 |

Per-step detail:

| dataset   | run_id                                    | step   | started_at                 | complete   |   duration_s |   llm_calls |   llm_latency_total_s |   llm_latency_mean_s |   llm_latency_max_s |   peak_rss_mib |
|:----------|:------------------------------------------|:-------|:---------------------------|:-----------|-------------:|------------:|----------------------:|---------------------:|--------------------:|---------------:|
| rtfm      | icpm2027_base                             | 1      | 2026-08-28T21:09:11.470000 | True       |       19.121 |           0 |                       |                      |                     |         1145.9 |
| rtfm      | icpm2027_base                             | 2      | 2026-08-28T21:09:30.628000 | True       |       48.44  |           0 |                       |                      |                     |         1317.5 |
| rtfm      | icpm2027_base                             | 3      | 2026-08-28T21:10:19.071000 | True       |        0.289 |           0 |                       |                      |                     |         1317.5 |
| rtfm      | icpm2027_base                             | 4      | 2026-08-28T21:10:19.362000 | True       |        0.017 |           0 |                       |                      |                     |         1317.5 |
| rtfm      | icpm2027_c12_guided_stability_rep1        | 5a     | 2026-08-28T21:23:38.102000 | True       |       81.758 |           1 |                 79.98 |                79.98 |               79.98 |          383.4 |
| rtfm      | icpm2027_c12_guided_stability_rep2        | 5a     | 2026-08-28T21:25:02.074000 | True       |        4.74  |           1 |                  2.97 |                 2.97 |                2.97 |          380.4 |
| rtfm      | icpm2027_c12_guided_stability_rep3        | 5a     | 2026-08-28T21:25:08.900000 | True       |       71.813 |           1 |                 70.06 |                70.06 |               70.06 |          380.7 |
| rtfm      | icpm2027_c12_guided_stability_rep4        | 5a     | 2026-08-28T21:26:22.786000 | True       |       49.21  |           1 |                 47.5  |                47.5  |               47.5  |          380.3 |
| rtfm      | icpm2027_c12_guided_stability_rep5        | 5a     | 2026-08-28T21:27:14.177000 | True       |        5.805 |           1 |                  4.1  |                 4.1  |                4.1  |          380.5 |
| rtfm      | icpm2027_e1_guided_no_sample_rep1         | 5a     | 2026-08-28T22:49:33.368000 | True       |        5.565 |           1 |                  3.82 |                 3.82 |                3.82 |          380.6 |
| rtfm      | icpm2027_e1_guided_no_sample_rep1         | 6      | 2026-08-28T22:49:38.934000 | True       |       17.054 |           5 |                 52    |                10.4  |               16.82 |          403.9 |
| rtfm      | icpm2027_e1_guided_no_sample_rep1         | 7b     | 2026-08-28T22:49:55.989000 | True       |     1091.5   |           0 |                nan    |               nan    |              nan    |         1407.3 |
| rtfm      | icpm2027_e1_guided_no_sample_rep2         | 5a     | 2026-08-28T23:08:10.490000 | True       |       42.501 |           1 |                 40.41 |                40.41 |               40.41 |          380.5 |
| rtfm      | icpm2027_e1_guided_no_sample_rep2         | 6      | 2026-08-28T23:08:52.993000 | True       |       40.948 |           5 |                 90.96 |                18.19 |               40.71 |          407   |
| rtfm      | icpm2027_e1_guided_no_sample_rep2         | 7b     | 2026-08-28T23:09:33.942000 | True       |      154.395 |           0 |                nan    |               nan    |              nan    |         1396.7 |
| rtfm      | icpm2027_e1_guided_rep1                   | 5a     | 2026-08-28T22:29:59.079000 | True       |        7.21  |           1 |                  5.28 |                 5.28 |                5.28 |          383.3 |
| rtfm      | icpm2027_e1_guided_rep1                   | 6      | 2026-08-28T22:30:06.291000 | True       |      195.445 |           5 |                415.67 |                83.13 |              195.21 |          408.7 |
| rtfm      | icpm2027_e1_guided_rep1                   | 7b     | 2026-08-28T22:33:21.738000 | True       |      261.888 |           0 |                nan    |               nan    |              nan    |         1395.5 |
| rtfm      | icpm2027_e1_guided_rep2                   | 5a     | 2026-08-28T22:37:46.201000 | True       |       29.083 |           1 |                 27.15 |                27.15 |               27.15 |          383.3 |
| rtfm      | icpm2027_e1_guided_rep2                   | 6      | 2026-08-28T22:38:15.286000 | True       |      146.839 |           5 |                186.05 |                37.21 |              146.59 |          408.8 |
| rtfm      | icpm2027_e1_guided_rep2                   | 7b     | 2026-08-28T22:40:42.126000 | True       |      161.441 |           0 |                nan    |               nan    |              nan    |         1393.4 |
| rtfm      | icpm2027_e1_open_rep1                     | 5b     | 2026-08-28T22:43:26.281000 | False      |      nan     |           0 |                nan    |               nan    |              nan    |          nan   |
| rtfm      | icpm2027_e1_open_rep1                     | 5b     | 2026-08-28T22:47:14.862000 | True       |        5.714 |           1 |                  4.01 |                 4.01 |                4.01 |          373.6 |
| rtfm      | icpm2027_e1_open_rep1                     | 6      | 2026-08-28T22:47:20.578000 | True       |       99.747 |           5 |                141.62 |                28.32 |               99.52 |          396.8 |
| rtfm      | icpm2027_e1_open_rep2                     | 5b     | 2026-08-28T22:49:02.516000 | True       |        6.129 |           1 |                  4.41 |                 4.41 |                4.41 |          373.1 |
| rtfm      | icpm2027_e1_open_rep2                     | 6      | 2026-08-28T22:49:08.647000 | True       |       22.547 |           5 |                 62.97 |                12.59 |               22.35 |          399.8 |
| rtfm      | icpm2027_e2_guided_pertA_remove_19_rep1   | 5a     | 2026-08-29T09:24:44.637000 | True       |       25.281 |           1 |                 24.03 |                24.03 |               24.03 |          380   |
| rtfm      | icpm2027_e2_guided_pertA_remove_19_rep1   | 6      | 2026-08-29T09:25:09.920000 | True       |      219.973 |           5 |                933.19 |               186.64 |              219.81 |          410.6 |
| rtfm      | icpm2027_e2_guided_pertA_remove_19_rep1   | 7b     | 2026-08-29T09:28:49.894000 | True       |       88.41  |           0 |                nan    |               nan    |              nan    |         1423.8 |
| rtfm      | icpm2027_e2_guided_pertB_merge_13_20_rep1 | 5a     | 2026-08-29T09:30:19.866000 | True       |       31.619 |           1 |                 30.42 |                30.42 |               30.42 |          379.7 |
| rtfm      | icpm2027_e2_guided_pertB_merge_13_20_rep1 | 6      | 2026-08-29T09:30:51.487000 | True       |       11.645 |           5 |                 47.03 |                 9.41 |               11.48 |          406   |
| rtfm      | icpm2027_e2_guided_pertB_merge_13_20_rep1 | 7b     | 2026-08-29T09:31:03.133000 | True       |       88.301 |           0 |                nan    |               nan    |              nan    |         1395.8 |
| sepsis    | icpm2027_base                             | 1      | 2026-08-28T21:10:23.997000 | True       |        0.61  |           0 |                       |                      |                     |          295.7 |
| sepsis    | icpm2027_base                             | 2      | 2026-08-28T21:10:24.623000 | True       |       10.422 |           0 |                       |                      |                     |          301.7 |
| sepsis    | icpm2027_base                             | 3      | 2026-08-28T21:10:35.050000 | True       |        0.914 |           0 |                       |                      |                     |          301.7 |
| sepsis    | icpm2027_base                             | 4      | 2026-08-28T21:10:35.968000 | True       |        0.036 |           0 |                       |                      |                     |          301.7 |
| sepsis    | icpm2027_c12_guided_stability_rep1        | 5a     | 2026-08-28T21:29:05.324000 | True       |       55.667 |           1 |                 53.93 |                53.93 |               53.93 |          380.5 |
| sepsis    | icpm2027_c12_guided_stability_rep1        | 5a     | 2026-08-28T21:41:43.641000 | True       |       11.032 |           1 |                  8.97 |                 8.97 |                8.97 |          377.2 |
| sepsis    | icpm2027_c12_guided_stability_rep2        | 5a     | 2026-08-28T21:30:03.165000 | True       |      113.381 |           1 |                111.69 |               111.69 |              111.69 |          383.7 |
| sepsis    | icpm2027_c12_guided_stability_rep2        | 5a     | 2026-08-28T21:41:57.081000 | True       |        6.674 |           1 |                  4.74 |                 4.74 |                4.74 |          380.2 |
| sepsis    | icpm2027_c12_guided_stability_rep3        | 5a     | 2026-08-28T21:31:59.170000 | True       |      375.525 |           1 |                 21.97 |                21.97 |               21.97 |          379.3 |
| sepsis    | icpm2027_c12_guided_stability_rep3        | 5a     | 2026-08-28T21:42:05.922000 | True       |        6.564 |           1 |                  4.8  |                 4.8  |                4.8  |          380.8 |
| sepsis    | icpm2027_c12_guided_stability_rep4        | 5a     | 2026-08-28T21:38:17.337000 | True       |        7.939 |           1 |                  5.48 |                 5.48 |                5.48 |          386.6 |
| sepsis    | icpm2027_c12_guided_stability_rep4        | 5a     | 2026-08-28T21:42:14.652000 | True       |        6.843 |           1 |                  5.13 |                 5.13 |                5.13 |          380.5 |
| sepsis    | icpm2027_c12_guided_stability_rep5        | 5a     | 2026-08-28T21:38:27.430000 | False      |      nan     |           0 |                nan    |               nan    |              nan    |          nan   |
| sepsis    | icpm2027_c12_guided_stability_rep5        | 5a     | 2026-08-28T21:42:23.773000 | True       |        7.048 |           1 |                  5.33 |                 5.33 |                5.33 |          380.7 |
| sepsis    | icpm2027_e1_guided_no_sample_rep1         | 5a     | 2026-08-29T07:44:59.819000 | True       |        5.083 |           1 |                  3.83 |                 3.83 |                3.83 |          378.6 |
| sepsis    | icpm2027_e1_guided_no_sample_rep1         | 6      | 2026-08-29T07:45:04.903000 | True       |       32.24  |          17 |                135.06 |                 7.94 |               10.4  |          437   |
| sepsis    | icpm2027_e1_guided_no_sample_rep2         | 5a     | 2026-08-29T07:45:38.999000 | True       |        4.919 |           1 |                  3.45 |                 3.45 |                3.45 |          308.7 |
| sepsis    | icpm2027_e1_guided_no_sample_rep2         | 6      | 2026-08-29T07:45:43.919000 | True       |       30.842 |          17 |                133.1  |                 7.83 |               10.59 |          433.5 |
| sepsis    | icpm2027_e1_guided_rep1                   | 5a     | 2026-08-29T07:40:29.623000 | True       |        5.687 |           1 |                  4.32 |                 4.32 |                4.32 |          368.9 |
| sepsis    | icpm2027_e1_guided_rep1                   | 6      | 2026-08-29T07:40:35.312000 | True       |       29.945 |          17 |                136.9  |                 8.05 |               19.91 |          411.5 |
| sepsis    | icpm2027_e1_guided_rep2                   | 5a     | 2026-08-29T07:41:06.929000 | True       |       27.878 |           1 |                 26.64 |                26.64 |               26.64 |          378.5 |
| sepsis    | icpm2027_e1_guided_rep2                   | 6      | 2026-08-29T07:41:34.809000 | True       |       26.921 |          17 |                115.29 |                 6.78 |                8.2  |          378.5 |
| sepsis    | icpm2027_e1_open_rep1                     | 5b     | 2026-08-29T07:51:36.895000 | True       |        5.022 |           1 |                  3.8  |                 3.8  |                3.8  |          372.8 |
| sepsis    | icpm2027_e1_open_rep1                     | 6      | 2026-08-29T07:51:41.919000 | True       |      121.792 |          17 |                447.8  |                26.34 |              109.15 |          381.8 |
| sepsis    | icpm2027_e1_open_rep2                     | 5b     | 2026-08-29T07:43:12.208000 | True       |       26.333 |           1 |                 25.04 |                25.04 |               25.04 |          371.6 |
| sepsis    | icpm2027_e1_open_rep2                     | 6      | 2026-08-29T07:43:38.542000 | True       |       79.515 |          17 |                377.94 |                22.23 |               58.88 |          442.9 |
| sepsis    | icpm2027_e2_guided_pertA_remove_21_rep1   | 5a     | 2026-08-29T09:17:12.362000 | True       |       24.305 |           1 |                 23.13 |                23.13 |               23.13 |          379.5 |
| sepsis    | icpm2027_e2_guided_pertA_remove_21_rep1   | 6      | 2026-08-29T09:17:36.668000 | True       |       57.584 |          17 |                202.55 |                11.91 |               29.3  |          520.9 |
| sepsis    | icpm2027_e2_guided_pertB_merge_15_16_rep1 | 5a     | 2026-08-29T09:18:35.847000 | True       |       10.881 |           1 |                  9.69 |                 9.69 |                9.69 |          379.8 |
| sepsis    | icpm2027_e2_guided_pertB_merge_15_16_rep1 | 6      | 2026-08-29T09:18:46.729000 | True       |      236.706 |          17 |                814.81 |                47.93 |              143.26 |          519.9 |
| bpic2019  | icpm2027_base                             | 1      | 2026-08-29T09:34:10.174000 | True       |       52.279 |           0 |                       |                      |                     |         2605.6 |
| bpic2019  | icpm2027_base                             | 2      | 2026-08-29T09:35:02.626000 | True       |      230.144 |           0 |                       |                      |                     |         3558.9 |
| bpic2019  | icpm2027_base                             | 3      | 2026-08-29T09:38:52.802000 | True       |        7.555 |           0 |                       |                      |                     |         3558.9 |
| bpic2019  | icpm2027_base                             | 4      | 2026-08-29T09:39:00.388000 | True       |        0.44  |           0 |                       |                      |                     |         3558.9 |
| bpic2019  | icpm2027_c12_guided_stability_rep1        | 5a     | 2026-08-29T09:39:18.337000 | True       |      116.007 |           1 |                114.64 |               114.64 |              114.64 |          388.5 |
| bpic2019  | icpm2027_c12_guided_stability_rep2        | 5a     | 2026-08-29T09:41:15.722000 | True       |      104.866 |           1 |                103.86 |               103.86 |              103.86 |          388   |
| bpic2019  | icpm2027_c12_guided_stability_rep3        | 5a     | 2026-08-29T09:43:01.945000 | True       |       38.033 |           1 |                 37.04 |                37.04 |               37.04 |          388.5 |
| bpic2019  | icpm2027_c12_guided_stability_rep4        | 5a     | 2026-08-29T09:43:41.325000 | True       |       34.6   |           1 |                 33.59 |                33.59 |               33.59 |          388.4 |
| bpic2019  | icpm2027_c12_guided_stability_rep5        | 5a     | 2026-08-29T09:44:17.257000 | True       |       25.006 |           1 |                 24.02 |                24.02 |               24.02 |          388.6 |
| bpic2019  | icpm2027_e1_guided_no_sample_rep1         | 5a     | 2026-08-30T23:28:30.624000 | True       |        5.416 |           1 |                  3.42 |                 3.42 |                3.42 |          370.6 |
| bpic2019  | icpm2027_e1_guided_no_sample_rep1         | 6      | 2026-08-30T23:28:36.042000 | True       |     1567.36  |         479 |               4984.11 |                10.41 |               83.18 |         4595.8 |
| bpic2019  | icpm2027_e1_guided_no_sample_rep2         | 5a     | 2026-08-30T23:54:48.464000 | True       |       18.658 |           1 |                 16.62 |                16.62 |               16.62 |          380   |
| bpic2019  | icpm2027_e1_guided_no_sample_rep2         | 6      | 2026-08-30T23:55:07.124000 | False      |      nan     |         479 |               6318.56 |                13.19 |              134.14 |         4274.7 |
| bpic2019  | icpm2027_e1_guided_no_sample_rep2         | 6      | 2026-08-31T00:28:04.928000 | True       |      598.105 |           1 |                  4.03 |                 4.03 |                4.03 |         4390.8 |
| bpic2019  | icpm2027_e1_guided_rep1                   | 5a     | 2026-08-30T21:20:35.438000 | True       |       15.146 |           1 |                 13.16 |                13.16 |               13.16 |          378.7 |
| bpic2019  | icpm2027_e1_guided_rep1                   | 6      | 2026-08-30T21:20:50.585000 | True       |     1117.99  |         479 |               4167.6  |                 8.7  |               73.84 |         4376.2 |
| bpic2019  | icpm2027_e1_guided_rep2                   | 5a     | 2026-08-30T21:39:34.209000 | True       |       34.041 |           1 |                 31.97 |                31.97 |               31.97 |          392.8 |
| bpic2019  | icpm2027_e1_guided_rep2                   | 6      | 2026-08-30T21:40:08.252000 | True       |     1497.18  |         479 |               4620.43 |                 9.65 |               84.27 |         4032.1 |
| bpic2019  | icpm2027_e1_open_rep1                     | 5b     | 2026-08-30T22:05:10.442000 | True       |       50.922 |           1 |                 49.01 |                49.01 |               49.01 |          385.5 |
| bpic2019  | icpm2027_e1_open_rep1                     | 6      | 2026-08-30T22:06:01.366000 | False      |      nan     |         479 |               5140.61 |                10.73 |               83.66 |         4159.2 |
| bpic2019  | icpm2027_e1_open_rep1                     | 6      | 2026-08-30T22:34:26.033000 | True       |      747.125 |           1 |                  1.83 |                 1.83 |                1.83 |         3666.1 |
| bpic2019  | icpm2027_e1_open_rep2                     | 5b     | 2026-08-30T22:46:57.646000 | True       |       31.166 |           1 |                 29.2  |                29.2  |               29.2  |          384.1 |
| bpic2019  | icpm2027_e1_open_rep2                     | 6      | 2026-08-30T22:47:28.813000 | True       |     2082.65  |         479 |               7298.48 |                15.24 |              174.8  |         3516.3 |

_Step-by-step wall-clock and LLM-call latency figures characterize feasibility/scalability, not categorization quality; they are not evidence for RQ1's semantic-categorization claim (OVERVIEW.md, Task C9). Figures drawn from a non-frozen run are provisional and must not be cited in the paper — only figures from the frozen runs (§2.2) are reportable._

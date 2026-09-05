# Experiment 1 — rtfm (axis: resolution)

## Variant scope (Task C7)

- Policy: `all`
- Variants: 231 of 231 extracted
- Cases: 150370 of 150370
- **Share of the full log's cases covered by this scope: 100.0%**

## Step 5a induction stability (Task C12)

Step 5a reproduced the same anchor set across all 5 identical-input reruns for rtfm; category *labels* reworded cosmetically between some reruns (e.g. added qualifiers with no change in the anchored goal-model element), which is expected LLM phrasing variance, not induction instability (§4: categories are matched by anchor_ids, never by name). This dataset's figures below are not subject to Task E7's qualification.

## Coverage and residual

| condition      |   total_variants |   total_cases |   assigned_variants |   assigned_cases |   macro_coverage_C_V |   micro_coverage_C_C |   residual_variants |   residual_variants_pct |   residual_cases |   residual_cases_pct |
|:---------------|-----------------:|--------------:|--------------------:|-----------------:|---------------------:|---------------------:|--------------------:|------------------------:|-----------------:|---------------------:|
| e1_guided_rep1 |              231 |        150370 |                 224 |           129606 |             0.969697 |             0.861914 |                   7 |                3.0303   |            20764 |              13.8086 |
| e1_guided_rep2 |              231 |        150370 |                 228 |           129622 |             0.987013 |             0.86202  |                   3 |                1.2987   |            20748 |              13.798  |
| e1_guided_rep3 |              231 |        150370 |                 228 |           129619 |             0.987013 |             0.862    |                   3 |                1.2987   |            20751 |              13.8    |
| e1_guided_rep4 |              231 |        150370 |                 214 |           129596 |             0.926407 |             0.861847 |                  17 |                7.35931  |            20774 |              13.8153 |
| e1_guided_rep5 |              231 |        150370 |                 229 |           129623 |             0.991342 |             0.862027 |                   2 |                0.865801 |            20747 |              13.7973 |
| e1_open_rep1   |              231 |        150370 |                 229 |           129623 |             0.991342 |             0.862027 |                   2 |                0.865801 |            20747 |              13.7973 |
| e1_open_rep2   |              231 |        150370 |                 229 |           129623 |             0.991342 |             0.862027 |                   2 |                0.865801 |            20747 |              13.7973 |
| e1_open_rep3   |              231 |        150370 |                 225 |           129613 |             0.974026 |             0.86196  |                   6 |                2.5974   |            20757 |              13.804  |
| e1_open_rep4   |              231 |        150370 |                 227 |           129613 |             0.982684 |             0.86196  |                   4 |                1.7316   |            20757 |              13.804  |
| e1_open_rep5   |              231 |        150370 |                 226 |           129614 |             0.978355 |             0.861967 |                   5 |                2.1645   |            20756 |              13.8033 |

_Higher coverage is not better categorization: a larger taxonomy or a broad catch-all category can trivially raise $C_V$/$C_C$ while carrying less semantic information (Task D2)._

## Declared-alternative coverage (guided arm)

|   anchor_id | declared_alternative                                | category_id                |   variants |   cases | status                   |
|------------:|:----------------------------------------------------|:---------------------------|-----------:|--------:|:-------------------------|
|          12 | Resolve via timely payment                          | timely_payment             |          9 |   49612 | realized                 |
|           5 | Fine becomes enforceable and is resolved            | via 20, 19, 14, 13         |        215 |   79994 | realized via descendants |
|          13 | Resolve via delinquent payment                      | delinquent_payment         |         47 |   16977 | realized                 |
|           7 | Contested appeal is resolved                        | via 19, 14                 |        134 |    4336 | realized via descendants |
|          20 | Resolve via coercive credit collection              | coercive_credit_collection |         34 |   58681 | realized                 |
|          14 | Resolve via administrative appeal to the Prefecture | administrative_appeal      |         75 |    3842 | realized                 |
|          19 | Resolve via judicial appeal to the Judge            | judicial_appeal            |         59 |     494 | realized                 |

7 of 7 declared alternatives are realized (5 named directly by a category, the rest through their descendants); 0 are realized but carry no variants.

## Contingency — guided vs. open

### Variant counts

| row_category               |   (residual) |   appeal_and_legal_process |   direct_payment |   payment_rework_loops |   standard_fine_lifecycle |
|:---------------------------|-------------:|---------------------------:|-----------------:|-----------------------:|--------------------------:|
| (residual)                 |            2 |                          5 |                0 |                      0 |                         0 |
| administrative_appeal      |            0 |                         61 |                0 |                      8 |                         6 |
| coercive_credit_collection |            0 |                         14 |                0 |                      6 |                        14 |
| delinquent_payment         |            0 |                          8 |                0 |                     29 |                        10 |
| judicial_appeal            |            0 |                         40 |                0 |                     17 |                         2 |
| timely_payment             |            0 |                          1 |                3 |                      4 |                         1 |

### Case-weighted counts

| row_category               |   (residual) |   appeal_and_legal_process |   direct_payment |   payment_rework_loops |   standard_fine_lifecycle |
|:---------------------------|-------------:|---------------------------:|-----------------:|-----------------------:|--------------------------:|
| (residual)                 |        20747 |                         17 |                0 |                      0 |                         0 |
| administrative_appeal      |            0 |                       3810 |                0 |                     14 |                        18 |
| coercive_credit_collection |            0 |                         58 |                0 |                     18 |                     58605 |
| delinquent_payment         |            0 |                         58 |                0 |                   7348 |                      9571 |
| judicial_appeal            |            0 |                        456 |                0 |                     36 |                         2 |
| timely_payment             |            0 |                          2 |            49514 |                     95 |                         1 |

### Merges and splits (§3 evidence item 5)

- Split: administrative_appeal -> appeal_and_legal_process (61), payment_rework_loops (8), standard_fine_lifecycle (6)
- Split: coercive_credit_collection -> appeal_and_legal_process (14), standard_fine_lifecycle (14), payment_rework_loops (6)
- Split: delinquent_payment -> payment_rework_loops (29), standard_fine_lifecycle (10), appeal_and_legal_process (8)
- Split: judicial_appeal -> appeal_and_legal_process (40), payment_rework_loops (17), standard_fine_lifecycle (2)
- Split: timely_payment -> payment_rework_loops (4), direct_payment (3), appeal_and_legal_process (1), standard_fine_lifecycle (1)
- Merge: administrative_appeal (61), judicial_appeal (40), coercive_credit_collection (14), delinquent_payment (8), (residual) (5), timely_payment (1) -> appeal_and_legal_process
- Merge: delinquent_payment (29), judicial_appeal (17), administrative_appeal (8), coercive_credit_collection (6), timely_payment (4) -> payment_rework_loops
- Merge: coercive_credit_collection (14), delinquent_payment (10), administrative_appeal (6), judicial_appeal (2), timely_payment (1) -> standard_fine_lifecycle

## Secondary — guided vs. rule baseline (Task C4)

A deterministic activity-rule classifier (no LLM, no fit — `baselines/rule_based_rtfm.py`). Close agreement here means the guided arm's five declared alternatives are recoverable from a handful of hand-written rules on this log, which the paper must report as a bound on the guided arm's added value here.

| row_category               |   (residual) |   administrative_appeal |   coercive_credit_collection |   delinquent_payment |   judicial_appeal |   timely_payment |
|:---------------------------|-------------:|------------------------:|-----------------------------:|---------------------:|------------------:|-----------------:|
| (residual)                 |            1 |                       4 |                            0 |                    0 |                 1 |                1 |
| administrative_appeal      |            3 |                      54 |                            0 |                    8 |                10 |                0 |
| coercive_credit_collection |            0 |                      13 |                           15 |                    0 |                 6 |                0 |
| delinquent_payment         |            0 |                      19 |                            0 |                   14 |                 2 |               12 |
| judicial_appeal            |            0 |                       0 |                            0 |                    0 |                59 |                0 |
| timely_payment             |            0 |                       1 |                            0 |                    1 |                 1 |                6 |

| row_category               |   (residual) |   administrative_appeal |   coercive_credit_collection |   delinquent_payment |   judicial_appeal |   timely_payment |
|:---------------------------|-------------:|------------------------:|-----------------------------:|---------------------:|------------------:|-----------------:|
| (residual)                 |        20385 |                      14 |                            0 |                    0 |                 3 |              362 |
| administrative_appeal      |            4 |                    3811 |                            0 |                   14 |                13 |                0 |
| coercive_credit_collection |            0 |                      44 |                        58601 |                    0 |                36 |                0 |
| delinquent_payment         |            0 |                      88 |                            0 |                13384 |                 7 |             3498 |
| judicial_appeal            |            0 |                       0 |                            0 |                    0 |               494 |                0 |
| timely_payment             |            0 |                       1 |                            0 |                    2 |                 2 |            49607 |

- Split: administrative_appeal -> administrative_appeal (54), judicial_appeal (10), delinquent_payment (8), (residual) (3)
- Split: coercive_credit_collection -> coercive_credit_collection (15), administrative_appeal (13), judicial_appeal (6)
- Split: delinquent_payment -> administrative_appeal (19), delinquent_payment (14), timely_payment (12), judicial_appeal (2)
- Split: timely_payment -> timely_payment (6), administrative_appeal (1), delinquent_payment (1), judicial_appeal (1)
- Merge: administrative_appeal (54), delinquent_payment (19), coercive_credit_collection (13), (residual) (4), timely_payment (1) -> administrative_appeal
- Merge: delinquent_payment (14), administrative_appeal (8), timely_payment (1) -> delinquent_payment
- Merge: judicial_appeal (59), administrative_appeal (10), coercive_credit_collection (6), delinquent_payment (2), (residual) (1), timely_payment (1) -> judicial_appeal
- Merge: delinquent_payment (12), timely_payment (6), (residual) (1) -> timely_payment

## Indicator satisfaction (Task C13)

Guided arm only. Each goal-model indicator is *measured* from the log and converted through its own `KPIEvalValueSet`, then propagated up the goal model --- no LLM call. The measurement operator is therefore the one part of the pipeline not exposed to the LLM-dependence threat, but only the `whole log` row is free of it outright: every per-category row is measured over the sublog Step 6 assigned, so it inherits that step's variance even though computing it does not. Indicators with low applicability are reported as coverage, never as bad values.

Goal model: `rtfm_goal_model.jucm`

Satisfaction is on GRL's [-100, +100] scale, converted from the measured value by each indicator's own `KPIEvalValueSet`. The measured value is reported beside it in every row: a score against an illustrative threshold reads exactly like one against a statute, and only the provenance column separates them.

## Time to fine dispatch (days) (id 112)

- Value set: worst 360.0, threshold 90.0, target 30.0 days
- Provenance: `statutory` — threshold 90 d and worst 360 d: Art. 201 D.Lgs. 285/1992 (ordinary notification term; extended term for parties resident abroad). target 30 d: L. 241/1990 art. 2 c.2, the default term for concluding an administrative proceeding, applied by analogy as an operational aspiration -- the specific term in Art. 201 is what binds.

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 87.5 | +4 | 150370 | 103987 | 0 | 0 | 46383 | 69% |
| coercive_credit_collection | 84.2 | +9 | 58681 | 58681 | 0 | 0 | 0 | 100% |
| timely_payment | 66.8 | +38 | 49612 | 3229 | 0 | 0 | 46383 | 7% |
| delinquent_payment | 91.5 | +0 | 16977 | 16977 | 0 | 0 | 0 | 100% |
| administrative_appeal | 89.4 | +1 | 3842 | 3842 | 0 | 0 | 0 | 100% |
| judicial_appeal | 94.1 | -1 | 494 | 494 | 0 | 0 | 0 | 100% |

## Time to appeal filing, Prefecture (days) (id 113)

- Value set: worst 120.0, threshold 60.0, target 60.0 days
- Provenance: `statutory` — threshold 60 d: Art. 203 D.Lgs. 285/1992, the window for a ricorso al Prefetto; corroborated by the Delay Prefecture' < 60 days guard in Mannhardt et al. (2016, Fig. 8). target == threshold because an admissibility window is a boundary, not a gradient. worst 120 d illustrative (2x the window).
- **one-sided scale** (`target == threshold`: an admissibility boundary, not a gradient — every compliant value saturates at the same score)

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 48.6 | +100 | 150370 | 4036 | 146182 | 145 | 7 | 96% |
| coercive_credit_collection | 41.8 | +100 | 58681 | 59 | 58622 | 0 | 0 | 100% |
| timely_payment | 386.5 | -100 | 49612 | 2 | 49609 | 1 | 0 | 67% |
| delinquent_payment | 30.2 | +100 | 16977 | 115 | 16857 | 0 | 5 | 96% |
| administrative_appeal | 49.5 | +100 | 3842 | 3706 | 4 | 131 | 1 | 97% |
| judicial_appeal | 33.4 | +100 | 494 | 147 | 340 | 6 | 1 | 95% |

## Time to appeal filing, Judge (days) (id 175)

- Value set: worst 60.0, threshold 30.0, target 30.0 days
- Provenance: `statutory` — threshold 30 d: Art. 204-bis D.Lgs. 285/1992, the window for a ricorso al Giudice di Pace -- half the Prefecture window, which v1.1 collapsed into a single 60-day indicator taken from Mannhardt et al. (2016, Fig. 8)'s Delay Judge' guard rather than from the statute. worst 60 d illustrative (2x).
- **one-sided scale** (`target == threshold`: an admissibility boundary, not a gradient — every compliant value saturates at the same score)

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 95.9 | -100 | 150370 | 538 | 149815 | 17 | 0 | 97% |
| coercive_credit_collection | 134.5 | -100 | 58681 | 36 | 58645 | 0 | 0 | 100% |
| timely_payment | 108.0 | -100 | 49612 | 2 | 49610 | 0 | 0 | 100% |
| delinquent_payment | 112.1 | -100 | 16977 | 7 | 16970 | 0 | 0 | 100% |
| administrative_appeal | 147.3 | -100 | 3842 | 13 | 3829 | 0 | 0 | 100% |
| judicial_appeal | 91.3 | -100 | 494 | 480 | 0 | 14 | 0 | 97% |

## Average time to case closure (days) (id 114)

- Value set: worst 365.0, threshold 180.0, target 150.0 days
- Provenance: `external-by-analogy` — threshold 180 d: L. 241/1990 art. 2, which caps any administrative proceeding's term at 180 days. target 150 d: Art. 201's 90-day notification term plus Art. 203's 60-day payment/appeal window, i.e. the earliest lawful completion of an uncontested case. worst 365 d illustrative. Replaces v1.1's acknowledged invented placeholder.

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 378.7 | -100 | 150370 | 126840 | 0 | 0 | 23530 | 84% |
| coercive_credit_collection | 689.2 | -100 | 58681 | 58681 | 0 | 0 | 0 | 100% |
| timely_payment | 17.4 | +100 | 49612 | 49612 | 0 | 0 | 0 | 100% |
| delinquent_payment | 356.7 | -95 | 16977 | 16977 | 0 | 0 | 0 | 100% |
| administrative_appeal | 477.4 | -100 | 3842 | 750 | 0 | 0 | 3092 | 20% |
| judicial_appeal | 683.6 | -100 | 494 | 448 | 0 | 0 | 46 | 91% |

## Propagated softgoal satisfaction

Propagated from the measured indicators through the same decomposition and contribution graph Step 5a used as the taxonomy axis (`min` over And, `max` over Or/Xor, weighted-clamped sum over contributions).

Only softgoals carry a value: indicators are the sole seeds, and they reach the model through contribution links, so every goal and task in the decomposition tree evaluates to the default 0. Seeding a category's `anchor_ids` with full satisfaction would light the tree up, but it would also assert that a category existing *is* its goal being met — the confound this measure is supposed to expose, not commit.

| Softgoal | whole log | administrative_appeal | coercive_credit_collection | delinquent_payment | judicial_appeal | timely_payment |
|---|---|---|---|---|---|---|
| Maximize timely fine revenue | -48 | -50 | -46 | -48 | -50 | +69 |
| Minimize administrative & enforcement cost | -50 | -50 | -50 | -48 | -50 | +50 |
| Preserve offender's due-process rights | +0 | +0 | +0 | +0 | +0 | -100 |

## Secondary — guided vs. structural (HDBSCAN) (Task C3)

| row_category               |   (residual) |   cluster_0 |   cluster_1 |   cluster_10 |   cluster_11 |   cluster_12 |   cluster_13 |   cluster_14 |   cluster_2 |   cluster_3 |   cluster_4 |   cluster_5 |   cluster_6 |   cluster_7 |   cluster_8 |   cluster_9 |
|:---------------------------|-------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|-------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|
| (residual)                 |            2 |           1 |           2 |            0 |            0 |            0 |            0 |            0 |           0 |           0 |           0 |           0 |           2 |           0 |           0 |           0 |
| administrative_appeal      |           22 |           0 |           4 |           13 |            5 |            0 |            3 |            1 |           0 |           4 |           0 |           0 |          11 |           0 |           5 |           7 |
| coercive_credit_collection |            5 |           0 |           0 |            2 |           10 |            0 |            0 |            4 |           0 |           0 |          13 |           0 |           0 |           0 |           0 |           0 |
| delinquent_payment         |            2 |           0 |           0 |            5 |            0 |            1 |            0 |            0 |          21 |           3 |           0 |           0 |           9 |           1 |           5 |           0 |
| judicial_appeal            |           13 |           1 |           2 |            0 |            0 |           13 |            9 |            2 |           0 |           0 |           0 |          14 |           0 |           5 |           0 |           0 |
| timely_payment             |            3 |           4 |           1 |            0 |            0 |            0 |            0 |            0 |           0 |           0 |           0 |           1 |           0 |           0 |           0 |           0 |

## Notable findings

- **The residual boundary is stable; the open arm's category set is not (recomputed 2026-09-03).** Variant V0003 (`Create Fine -> Send Fine`, no further activity - an unresolved/still-open case) carries 20,385 cases, 13.56% of the log, and is left **residual in all nine RTFM Experiment 1 runs**: every guided replicate, every open replicate, and both `guided_no_sample` runs. Both arms therefore agree on the single variant that dominates the case-weighted residual, which is why RTFM's case-weighted residual is ~13.8% in both arms and does not separate them. Where the open arm is unstable is the category set itself: `e1_open_rep1` induces four categories and leaves 3 variants residual (1.3%), `e1_open_rep2` induces five and leaves 9 (3.9%), against a guided taxonomy of five categories in every replicate. Read RQ1 from the category set and the anchors, not from this log's case-weighted coverage.

## Replicate stability (Task C2)

rep1 vs. rep2 of each arm, same convention as the paired contrast below. Read the "guided vs. open" divergence against these: a cross-arm difference no larger than an arm's own rep1-rep2 movement is not separable from run-to-run variance. The open arm has no anchors, so this is its only stability check — Task C12 tests the guided taxonomy alone.

### guided rep1 vs. rep2

**guided_rep1 vs. guided_rep2** — partition divergence (Task D1)

| residual_handling   | weighting   |      AMI |      NMI |   n_observations | primary   |
|:--------------------|:------------|---------:|---------:|-----------------:|:----------|
| own_cluster         | variant     | 0.547408 | 0.564145 |              231 | True      |
| own_cluster         | case        | 0.987151 | 0.987152 |           150370 | False     |
| exclude             | variant     | 0.563985 | 0.575494 |              223 | False     |
| exclude             | case        | 0.982739 | 0.98274  |           129605 | False     |

_AMI/NMI measure divergence between two partitions, not classification accuracy: neither partition is ground truth, so agreement between the arms is not evidence that either is correct._


### open rep1 vs. rep2

**open_rep1 vs. open_rep2** — partition divergence (Task D1)

| residual_handling   | weighting   |      AMI |      NMI |   n_observations | primary   |
|:--------------------|:------------|---------:|---------:|-----------------:|:----------|
| own_cluster         | variant     | 0.51417  | 0.530093 |              231 | True      |
| own_cluster         | case        | 0.927206 | 0.927209 |           150370 | False     |
| exclude             | variant     | 0.497807 | 0.509378 |              229 | False     |
| exclude             | case        | 0.896176 | 0.89618  |           129623 | False     |

_AMI/NMI measure divergence between two partitions, not classification accuracy: neither partition is ground truth, so agreement between the arms is not evidence that either is correct._


_Read on the D1-primary `own_cluster` convention. Where the open arm's rep1-rep2 AMI is lower than the guided arm's, every "guided vs. open" figure for this dataset should be reported with that band, and the open arm's instability noted as a limit on the strength of the paired contrast (Task E7, extended to the open arm)._

### Replicate residual-set Jaccard (§6)

Jaccard similarity of an arm's two replicate residual variant-sets, on this axis. A value near 1 means the arm puts the same variants outside every category across identical-input reruns; near 0 means it does not. §6 reads the guided-over-open gap as evidence that the declared frame stabilizes the residual boundary, not only the category set.

- guided: 0.25
- open: 1.00

## Partition divergence (optional, Task D1)

**guided vs. open** — partition divergence (Task D1)

| residual_handling   | weighting   |      AMI |      NMI |   n_observations | primary   |
|:--------------------|:------------|---------:|---------:|-----------------:|:----------|
| own_cluster         | variant     | 0.175335 | 0.202116 |              231 | True      |
| own_cluster         | case        | 0.886052 | 0.886058 |           150370 | False     |
| exclude             | variant     | 0.163064 | 0.182041 |              224 | False     |
| exclude             | case        | 0.836485 | 0.836492 |           129606 | False     |

_AMI/NMI measure divergence between two partitions, not classification accuracy: neither partition is ground truth, so agreement between the arms is not evidence that either is correct._


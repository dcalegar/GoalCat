# Experiment 1 — rtfm

## Variant scope (Task C7)

- Policy: `all`
- Variants: 231 of 231 extracted
- Cases: 150370 of 150370
- **Share of the full log's cases covered by this scope: 100.0%**

## Step 5a induction stability (Task C12)

Step 5a reproduced the same anchor set across all 5 identical-input reruns for rtfm; category *labels* reworded cosmetically between some reruns (e.g. added qualifiers with no change in the anchored goal-model element), which is expected LLM phrasing variance, not induction instability (§4: categories are matched by anchor_ids, never by name). This dataset's figures below are not subject to Task E7's qualification.

## Coverage and residual

| condition                |   total_variants |   total_cases |   assigned_variants |   assigned_cases |   macro_coverage_C_V |   micro_coverage_C_C |   residual_variants |   residual_variants_pct |   residual_cases |   residual_cases_pct |
|:-------------------------|-----------------:|--------------:|--------------------:|-----------------:|---------------------:|---------------------:|--------------------:|------------------------:|-----------------:|---------------------:|
| e1_guided_no_sample_rep1 |              231 |        150370 |                 217 |           129601 |             0.939394 |             0.861881 |                  14 |                6.06061  |            20769 |          13.8119     |
| e1_guided_no_sample_rep2 |              231 |        150370 |                 218 |           129607 |             0.943723 |             0.861921 |                  13 |                5.62771  |            20763 |          13.8079     |
| e1_guided_rep1           |              231 |        150370 |                 227 |           129618 |             0.982684 |             0.861994 |                   4 |                1.7316   |            20752 |          13.8006     |
| e1_guided_rep2           |              231 |        150370 |                 227 |           129618 |             0.982684 |             0.861994 |                   4 |                1.7316   |            20752 |          13.8006     |
| e1_open_rep1             |              231 |        150370 |                 229 |           150363 |             0.991342 |             0.999953 |                   2 |                0.865801 |                7 |           0.00465518 |
| e1_open_rep2             |              231 |        150370 |                 229 |           129623 |             0.991342 |             0.862027 |                   2 |                0.865801 |            20747 |          13.7973     |

_Higher coverage is not better categorization: a larger taxonomy or a broad catch-all category can trivially raise $C_V$/$C_C$ while carrying less semantic information (Task D2)._

## Declared-alternative coverage (guided arm)

|   anchor_id | declared_alternative                                | category_id                |   variants |   cases | status                   |
|------------:|:----------------------------------------------------|:---------------------------|-----------:|--------:|:-------------------------|
|          12 | Resolve via timely payment                          | timely_payment             |         10 |   49619 | realized                 |
|           5 | Fine becomes enforceable and is resolved            | via 20, 19, 14, 13         |        217 |   79999 | realized via descendants |
|          13 | Resolve via delinquent payment                      | delinquent_payment         |         50 |   16947 | realized                 |
|           7 | Contested appeal is resolved                        | via 19, 14                 |        126 |    4042 | realized via descendants |
|          20 | Resolve via coercive credit collection              | coercive_credit_collection |         41 |   59010 | realized                 |
|          14 | Resolve via administrative appeal to the Prefecture | administrative_appeal      |         61 |    3645 | realized                 |
|          19 | Resolve via judicial appeal to the Judge            | judicial_appeal            |         65 |     397 | realized                 |

7 of 7 declared alternatives are realized (5 named directly by a category, the rest through their descendants); 0 are realized but carry no variants.

## Contingency — guided vs. open

### Variant counts

| row_category               |   (residual) |   appeal_and_litigation |   direct_payment |   payment_rework_loops |   standard_fine_lifecycle |
|:---------------------------|-------------:|------------------------:|-----------------:|-----------------------:|--------------------------:|
| (residual)                 |            1 |                       0 |                1 |                      1 |                         1 |
| administrative_appeal      |            0 |                      51 |                0 |                      7 |                         3 |
| coercive_credit_collection |            0 |                      24 |                0 |                      6 |                        11 |
| delinquent_payment         |            0 |                      11 |                0 |                     33 |                         6 |
| judicial_appeal            |            1 |                      46 |                0 |                     17 |                         1 |
| timely_payment             |            0 |                       4 |                1 |                      4 |                         1 |

### Case-weighted counts

| row_category               |   (residual) |   appeal_and_litigation |   direct_payment |   payment_rework_loops |   standard_fine_lifecycle |
|:---------------------------|-------------:|------------------------:|-----------------:|-----------------------:|--------------------------:|
| (residual)                 |            4 |                       0 |              362 |                      1 |                     20385 |
| administrative_appeal      |            0 |                    3634 |                0 |                      8 |                         3 |
| coercive_credit_collection |            0 |                     405 |                0 |                     18 |                     58587 |
| delinquent_payment         |            0 |                      50 |                0 |                   7357 |                      9540 |
| judicial_appeal            |            3 |                     356 |                0 |                     37 |                         1 |
| timely_payment             |            0 |                       9 |            46371 |                    108 |                      3131 |

### Merges and splits (§3 evidence item 5)

- Split: administrative_appeal -> appeal_and_litigation (51), payment_rework_loops (7), standard_fine_lifecycle (3)
- Split: coercive_credit_collection -> appeal_and_litigation (24), standard_fine_lifecycle (11), payment_rework_loops (6)
- Split: delinquent_payment -> payment_rework_loops (33), appeal_and_litigation (11), standard_fine_lifecycle (6)
- Split: judicial_appeal -> appeal_and_litigation (46), payment_rework_loops (17), (residual) (1), standard_fine_lifecycle (1)
- Split: timely_payment -> appeal_and_litigation (4), payment_rework_loops (4), direct_payment (1), standard_fine_lifecycle (1)
- Merge: administrative_appeal (51), judicial_appeal (46), coercive_credit_collection (24), delinquent_payment (11), timely_payment (4) -> appeal_and_litigation
- Merge: (residual) (1), timely_payment (1) -> direct_payment
- Merge: delinquent_payment (33), judicial_appeal (17), administrative_appeal (7), coercive_credit_collection (6), timely_payment (4), (residual) (1) -> payment_rework_loops
- Merge: coercive_credit_collection (11), delinquent_payment (6), administrative_appeal (3), (residual) (1), judicial_appeal (1), timely_payment (1) -> standard_fine_lifecycle

## Secondary — guided vs. rule baseline (Task C4)

A deterministic activity-rule classifier (no LLM, no fit — `baselines/rule_based_rtfm.py`). Close agreement here means the guided arm's five declared alternatives are recoverable from a handful of hand-written rules on this log, which the paper must report as a bound on the guided arm's added value here.

| row_category               |   (residual) |   administrative_appeal |   coercive_credit_collection |   delinquent_payment |   judicial_appeal |   timely_payment |
|:---------------------------|-------------:|------------------------:|-----------------------------:|---------------------:|------------------:|-----------------:|
| (residual)                 |            1 |                       1 |                            0 |                    0 |                 0 |                2 |
| administrative_appeal      |            3 |                      50 |                            0 |                    4 |                 4 |                0 |
| coercive_credit_collection |            0 |                      18 |                           15 |                    0 |                 8 |                0 |
| delinquent_payment         |            0 |                      18 |                            0 |                   19 |                 2 |               11 |
| judicial_appeal            |            0 |                       0 |                            0 |                    0 |                65 |                0 |
| timely_payment             |            0 |                       4 |                            0 |                    0 |                 0 |                6 |

| row_category               |   (residual) |   administrative_appeal |   coercive_credit_collection |   delinquent_payment |   judicial_appeal |   timely_payment |
|:---------------------------|-------------:|------------------------:|-----------------------------:|---------------------:|------------------:|-----------------:|
| (residual)                 |        20385 |                       4 |                            0 |                    0 |                 0 |              363 |
| administrative_appeal      |            4 |                    3619 |                            0 |                   16 |                 6 |                0 |
| coercive_credit_collection |            0 |                     264 |                        58601 |                    0 |               145 |                0 |
| delinquent_payment         |            0 |                      62 |                            0 |                13384 |                 7 |             3494 |
| judicial_appeal            |            0 |                       0 |                            0 |                    0 |               397 |                0 |
| timely_payment             |            0 |                       9 |                            0 |                    0 |                 0 |            49610 |

- Split: administrative_appeal -> administrative_appeal (50), delinquent_payment (4), judicial_appeal (4), (residual) (3)
- Split: coercive_credit_collection -> administrative_appeal (18), coercive_credit_collection (15), judicial_appeal (8)
- Split: delinquent_payment -> delinquent_payment (19), administrative_appeal (18), timely_payment (11), judicial_appeal (2)
- Split: timely_payment -> timely_payment (6), administrative_appeal (4)
- Merge: administrative_appeal (50), coercive_credit_collection (18), delinquent_payment (18), timely_payment (4), (residual) (1) -> administrative_appeal
- Merge: delinquent_payment (19), administrative_appeal (4) -> delinquent_payment
- Merge: judicial_appeal (65), coercive_credit_collection (8), administrative_appeal (4), delinquent_payment (2) -> judicial_appeal
- Merge: delinquent_payment (11), timely_payment (6), (residual) (2) -> timely_payment

## Indicator satisfaction (Task C13)

Guided arm only. Each goal-model indicator is *measured* from the log and converted through its own `KPIEvalValueSet`, then propagated up the goal model --- no LLM call. This is the one result not exposed to the LLM-dependence threat. Indicators with low applicability are reported as coverage, never as bad values.

Goal model: `rtfm_goal_model.jucm`

Satisfaction is on GRL's [-100, +100] scale, converted from the measured value by each indicator's own `KPIEvalValueSet`. The measured value is reported beside it in every row: a score against an illustrative threshold reads exactly like one against a statute, and only the provenance column separates them.

## Time to fine dispatch (days) (id 112)

- Value set: worst 360.0, threshold 90.0, target 30.0 days
- Provenance: `statutory` — threshold 90 d and worst 360 d: Art. 201 D.Lgs. 285/1992 (ordinary notification term; extended term for parties resident abroad). target 30 d: L. 241/1990 art. 2 c.2, the default term for concluding an administrative proceeding, applied by analogy as an operational aspiration -- the specific term in Art. 201 is what binds.

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 87.5 | +4 | 150370 | 103987 | 0 | 0 | 46383 | 69% |
| coercive_credit_collection | 84.1 | +9 | 59010 | 59010 | 0 | 0 | 0 | 100% |
| timely_payment | 66.8 | +38 | 49619 | 3236 | 0 | 0 | 46383 | 7% |
| delinquent_payment | 91.5 | +0 | 16947 | 16947 | 0 | 0 | 0 | 100% |
| administrative_appeal | 90.2 | +0 | 3645 | 3645 | 0 | 0 | 0 | 100% |
| judicial_appeal | 100.3 | -3 | 397 | 397 | 0 | 0 | 0 | 100% |

## Time to appeal filing, Prefecture (days) (id 113)

- Value set: worst 120.0, threshold 60.0, target 60.0 days
- Provenance: `statutory` — threshold 60 d: Art. 203 D.Lgs. 285/1992, the window for a ricorso al Prefetto; corroborated by the Delay Prefecture' < 60 days guard in Mannhardt et al. (2016, Fig. 8). target == threshold because an admissibility window is a boundary, not a gradient. worst 120 d illustrative (2x the window).
- **one-sided scale** (`target == threshold`: an admissibility boundary, not a gradient — every compliant value saturates at the same score)

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 48.6 | +100 | 150370 | 4036 | 146182 | 145 | 7 | 96% |
| coercive_credit_collection | 41.5 | +100 | 59010 | 280 | 58730 | 0 | 0 | 100% |
| timely_payment | 62.3 | -3 | 49619 | 6 | 49610 | 3 | 0 | 67% |
| delinquent_payment | 36.3 | +100 | 16947 | 88 | 16853 | 0 | 6 | 94% |
| administrative_appeal | 50.1 | +100 | 3645 | 3510 | 3 | 132 | 0 | 96% |
| judicial_appeal | 34.0 | +100 | 397 | 152 | 238 | 6 | 1 | 96% |

## Time to appeal filing, Judge (days) (id 175)

- Value set: worst 60.0, threshold 30.0, target 30.0 days
- Provenance: `statutory` — threshold 30 d: Art. 204-bis D.Lgs. 285/1992, the window for a ricorso al Giudice di Pace -- half the Prefecture window, which v1.1 collapsed into a single 60-day indicator taken from Mannhardt et al. (2016, Fig. 8)'s Delay Judge' guard rather than from the statute. worst 60 d illustrative (2x).
- **one-sided scale** (`target == threshold`: an admissibility boundary, not a gradient — every compliant value saturates at the same score)

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 95.9 | -100 | 150370 | 538 | 149815 | 17 | 0 | 97% |
| coercive_credit_collection | 58.6 | -95 | 59010 | 145 | 58865 | 0 | 0 | 100% |
| timely_payment | — | — | 49619 | 0 | 49619 | 0 | 0 | 0% |
| delinquent_payment | 112.1 | -100 | 16947 | 7 | 16940 | 0 | 0 | 100% |
| administrative_appeal | 96.0 | -100 | 3645 | 6 | 3639 | 0 | 0 | 100% |
| judicial_appeal | 109.8 | -100 | 397 | 380 | 0 | 17 | 0 | 96% |

## Average time to case closure (days) (id 114)

- Value set: worst 365.0, threshold 180.0, target 150.0 days
- Provenance: `external-by-analogy` — threshold 180 d: L. 241/1990 art. 2, which caps any administrative proceeding's term at 180 days. target 150 d: Art. 201's 90-day notification term plus Art. 203's 60-day payment/appeal window, i.e. the earliest lawful completion of an uncontested case. worst 365 d illustrative. Replaces v1.1's acknowledged invented placeholder.

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 378.7 | -100 | 150370 | 126840 | 0 | 0 | 23530 | 84% |
| coercive_credit_collection | 690.5 | -100 | 59010 | 59010 | 0 | 0 | 0 | 100% |
| timely_payment | 17.4 | +100 | 49619 | 49619 | 0 | 0 | 0 | 100% |
| delinquent_payment | 356.8 | -95 | 16947 | 16947 | 0 | 0 | 0 | 100% |
| administrative_appeal | 318.5 | -74 | 3645 | 554 | 0 | 0 | 3091 | 15% |
| judicial_appeal | 565.7 | -100 | 397 | 347 | 0 | 0 | 50 | 87% |

## Propagated softgoal satisfaction

Propagated from the measured indicators through the same decomposition and contribution graph Step 5a used as the taxonomy axis (`min` over And, `max` over Or/Xor, weighted-clamped sum over contributions).

Only softgoals carry a value: indicators are the sole seeds, and they reach the model through contribution links, so every goal and task in the decomposition tree evaluates to the default 0. Seeding a category's `anchor_ids` with full satisfaction would light the tree up, but it would also assert that a category existing *is* its goal being met — the confound this measure is supposed to expose, not commit.

| Softgoal | whole log | administrative_appeal | coercive_credit_collection | delinquent_payment | judicial_appeal | timely_payment |
|---|---|---|---|---|---|---|
| Maximize timely fine revenue | -48 | -37 | -46 | -48 | -52 | +69 |
| Minimize administrative & enforcement cost | -50 | -37 | -50 | -48 | -50 | +50 |
| Preserve offender's due-process rights | +0 | +0 | +2 | +0 | +0 | -2 |

## Secondary — guided vs. structural (HDBSCAN) (Task C3)

| row_category               |   (residual) |   cluster_0 |   cluster_1 |   cluster_10 |   cluster_11 |   cluster_12 |   cluster_13 |   cluster_14 |   cluster_2 |   cluster_3 |   cluster_4 |   cluster_5 |   cluster_6 |   cluster_7 |   cluster_8 |   cluster_9 |
|:---------------------------|-------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|-------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|
| (residual)                 |            1 |           2 |           1 |            0 |            0 |            0 |            0 |            0 |           0 |           0 |           0 |           0 |           0 |           0 |           0 |           0 |
| administrative_appeal      |           19 |           0 |           5 |           10 |            0 |            0 |            1 |            0 |           0 |           0 |           0 |           0 |          12 |           0 |           7 |           7 |
| coercive_credit_collection |            6 |           0 |           0 |            2 |           15 |            0 |            0 |            5 |           0 |           0 |          13 |           0 |           0 |           0 |           0 |           0 |
| delinquent_payment         |            3 |           0 |           0 |            6 |            0 |            1 |            0 |            0 |          20 |           7 |           0 |           0 |           9 |           1 |           3 |           0 |
| judicial_appeal            |           16 |           1 |           2 |            0 |            0 |           13 |           11 |            2 |           0 |           0 |           0 |          15 |           0 |           5 |           0 |           0 |
| timely_payment             |            2 |           3 |           1 |            2 |            0 |            0 |            0 |            0 |           1 |           0 |           0 |           0 |           1 |           0 |           0 |           0 |

## Notable findings

- **Open-mode replicate coverage swing traced to one ambiguous variant (2026-08-29).** `e1_open_rep1` and `e1_open_rep2` show identical variant-level coverage (229/231, 2 residual variants each) but a ~13.8-point gap in case-weighted coverage (99.995% vs. 86.2%). Root cause: variant V0003 (`Create Fine → Send Fine`, no further activity — an unresolved/still-open case) carries 20,385 cases (~13.6% of the whole log). Open-mode Step 6 classified it inconsistently across replicates — folded into the catch-all-like `standard_fine_lifecycle`/`standard_collection_or_payment` category in one replicate, left residual in the other — because open induction has no external criterion for "does not realize any category." **Guided mode classified the same variant as residual in both replicates**, with near-identical rationale each time ("does not resolve the case" / "remaining in the residual"): the goal model gives the LLM a stable boundary for what counts as resolved vs. residual that open induction lacks. This is a concrete, high-leverage illustration of exactly what Task C2's replicate design exists to catch — LLM-sampling noise can concentrate disproportionately in a single high-frequency variant, and case-weighted coverage is far more sensitive to it than variant-level coverage. Positive evidence for RQ1: the external semantic frame stabilizes the residual boundary, not only the category set.

## Replicate stability (Task C2)

rep1 vs. rep2 of each arm, same convention as the paired contrast below. Read the "guided vs. open" divergence against these: a cross-arm difference no larger than an arm's own rep1-rep2 movement is not separable from run-to-run variance. The open arm has no anchors, so this is its only stability check — Task C12 tests the guided taxonomy alone.

### guided rep1 vs. rep2

**guided_rep1 vs. guided_rep2** — partition divergence (Task D1)

| residual_handling   | weighting   |      AMI |      NMI |   n_observations | primary   |
|:--------------------|:------------|---------:|---------:|-----------------:|:----------|
| own_cluster         | variant     | 0.714197 | 0.72477  |              231 | True      |
| own_cluster         | case        | 0.996594 | 0.996594 |           150370 | False     |
| exclude             | variant     | 0.700476 | 0.708159 |              227 | False     |
| exclude             | case        | 0.995165 | 0.995165 |           129618 | False     |

_AMI/NMI measure divergence between two partitions, not classification accuracy: neither partition is ground truth, so agreement between the arms is not evidence that either is correct._


### open rep1 vs. rep2

**open_rep1 vs. open_rep2** — partition divergence (Task D1)

| residual_handling   | weighting   |      AMI |      NMI |   n_observations | primary   |
|:--------------------|:------------|---------:|---------:|-----------------:|:----------|
| own_cluster         | variant     | 0.670191 | 0.679625 |              231 | True      |
| own_cluster         | case        | 0.76151  | 0.761521 |           150370 | False     |
| exclude             | variant     | 0.689431 | 0.695243 |              227 | False     |
| exclude             | case        | 0.900656 | 0.900659 |           129616 | False     |

_AMI/NMI measure divergence between two partitions, not classification accuracy: neither partition is ground truth, so agreement between the arms is not evidence that either is correct._


_Read on the D1-primary `own_cluster` convention. Where the open arm's rep1-rep2 AMI is lower than the guided arm's, every "guided vs. open" figure for this dataset should be reported with that band, and the open arm's instability noted as a limit on the strength of the paired contrast (Task E7, extended to the open arm)._

## Partition divergence (optional, Task D1)

**guided vs. open** — partition divergence (Task D1)

| residual_handling   | weighting   |      AMI |      NMI |   n_observations | primary   |
|:--------------------|:------------|---------:|---------:|-----------------:|:----------|
| own_cluster         | variant     | 0.133977 | 0.162    |              231 | True      |
| own_cluster         | case        | 0.637371 | 0.637391 |           150370 | False     |
| exclude             | variant     | 0.121481 | 0.140011 |              226 | False     |
| exclude             | case        | 0.735382 | 0.735394 |           129615 | False     |

_AMI/NMI measure divergence between two partitions, not classification accuracy: neither partition is ground truth, so agreement between the arms is not evidence that either is correct._


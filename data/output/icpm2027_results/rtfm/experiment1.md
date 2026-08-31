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
| e1_guided_rep1 |              231 |        150370 |                 227 |           129618 |             0.982684 |             0.861994 |                   4 |                  1.7316 |            20752 |              13.8006 |
| e1_guided_rep2 |              231 |        150370 |                 223 |           129518 |             0.965368 |             0.861329 |                   8 |                  3.4632 |            20852 |              13.8671 |
| e1_open_rep1   |              231 |        150370 |                 228 |           129978 |             0.987013 |             0.864388 |                   3 |                  1.2987 |            20392 |              13.5612 |
| e1_open_rep2   |              231 |        150370 |                 222 |           129317 |             0.961039 |             0.859992 |                   9 |                  3.8961 |            21053 |              14.0008 |

_Higher coverage is not better categorization: a larger taxonomy or a broad catch-all category can trivially raise $C_V$/$C_C$ while carrying less semantic information (Task D2)._

## Declared-alternative coverage (guided arm)

|   anchor_id | declared_alternative                                | category_id                |   variants |   cases | status                   |
|------------:|:----------------------------------------------------|:---------------------------|-----------:|--------:|:-------------------------|
|          12 | Resolve via timely payment                          | timely_payment             |          6 |   49609 | realized                 |
|           5 | Fine becomes enforceable and is resolved            | via 20, 19, 14, 13         |        221 |   80009 | realized via descendants |
|          13 | Resolve via delinquent payment                      | delinquent_payment         |         42 |   16917 | realized                 |
|           7 | Contested appeal is resolved                        | via 19, 14                 |        136 |    4080 | realized via descendants |
|          20 | Resolve via coercive credit collection              | coercive_credit_collection |         43 |   59012 | realized                 |
|          14 | Resolve via administrative appeal to the Prefecture | administrative_appeal      |         72 |    3682 | realized                 |
|          19 | Resolve via judicial appeal to the Judge            | judicial_appeal            |         64 |     398 | realized                 |

7 of 7 declared alternatives are realized (5 named directly by a category, the rest through their descendants); 0 are realized but carry no variants.

## Contingency — guided vs. open

### Variant counts

| row_category               |   (residual) |   appeal_process |   direct_payment |   payment_rework |   standard_collection |
|:---------------------------|-------------:|-----------------:|-----------------:|-----------------:|----------------------:|
| (residual)                 |            2 |                0 |                2 |                0 |                     0 |
| administrative_appeal      |            0 |               60 |                0 |               10 |                     2 |
| coercive_credit_collection |            0 |                8 |                0 |                3 |                    32 |
| delinquent_payment         |            0 |                9 |                0 |               29 |                     4 |
| judicial_appeal            |            1 |               47 |                0 |               14 |                     2 |
| timely_payment             |            0 |                1 |                2 |                3 |                     0 |

### Case-weighted counts

| row_category               |   (residual) |   appeal_process |   direct_payment |   payment_rework |   standard_collection |
|:---------------------------|-------------:|-----------------:|-----------------:|-----------------:|----------------------:|
| (residual)                 |        20389 |                0 |              363 |                0 |                     0 |
| administrative_appeal      |            0 |             3666 |                0 |               14 |                     2 |
| coercive_credit_collection |            0 |              345 |                0 |               14 |                 58653 |
| delinquent_payment         |            0 |               29 |                0 |             7355 |                  9533 |
| judicial_appeal            |            3 |              359 |                0 |               34 |                     2 |
| timely_payment             |            0 |                3 |            49502 |              104 |                     0 |

### Merges and splits (§3 evidence item 5)

- Split: administrative_appeal -> appeal_process (60), payment_rework (10), standard_collection (2)
- Split: coercive_credit_collection -> standard_collection (32), appeal_process (8), payment_rework (3)
- Split: delinquent_payment -> payment_rework (29), appeal_process (9), standard_collection (4)
- Split: judicial_appeal -> appeal_process (47), payment_rework (14), standard_collection (2), (residual) (1)
- Split: timely_payment -> payment_rework (3), direct_payment (2), appeal_process (1)
- Merge: administrative_appeal (60), judicial_appeal (47), delinquent_payment (9), coercive_credit_collection (8), timely_payment (1) -> appeal_process
- Merge: (residual) (2), timely_payment (2) -> direct_payment
- Merge: delinquent_payment (29), judicial_appeal (14), administrative_appeal (10), coercive_credit_collection (3), timely_payment (3) -> payment_rework
- Merge: coercive_credit_collection (32), delinquent_payment (4), administrative_appeal (2), judicial_appeal (2) -> standard_collection

## Secondary — guided vs. rule baseline (Task C4)

A deterministic activity-rule classifier (no LLM, no fit — `baselines/rule_based_rtfm.py`). Close agreement here means the guided arm's five declared alternatives are recoverable from a handful of hand-written rules on this log, which the paper must report as a bound on the guided arm's added value here.

| row_category               |   (residual) |   administrative_appeal |   coercive_credit_collection |   delinquent_payment |   judicial_appeal |   timely_payment |
|:---------------------------|-------------:|------------------------:|-----------------------------:|---------------------:|------------------:|-----------------:|
| (residual)                 |            1 |                       1 |                            0 |                    0 |                 0 |                2 |
| administrative_appeal      |            3 |                      62 |                            0 |                    4 |                 3 |                0 |
| coercive_credit_collection |            0 |                      18 |                           15 |                    0 |                10 |                0 |
| delinquent_payment         |            0 |                       9 |                            0 |                   19 |                 2 |               12 |
| judicial_appeal            |            0 |                       0 |                            0 |                    0 |                64 |                0 |
| timely_payment             |            0 |                       1 |                            0 |                    0 |                 0 |                5 |

| row_category               |   (residual) |   administrative_appeal |   coercive_credit_collection |   delinquent_payment |   judicial_appeal |   timely_payment |
|:---------------------------|-------------:|------------------------:|-----------------------------:|---------------------:|------------------:|-----------------:|
| (residual)                 |        20385 |                       4 |                            0 |                    0 |                 0 |              363 |
| administrative_appeal      |            4 |                    3659 |                            0 |                   16 |                 3 |                0 |
| coercive_credit_collection |            0 |                     264 |                        58601 |                    0 |               147 |                0 |
| delinquent_payment         |            0 |                      28 |                            0 |                13384 |                 7 |             3498 |
| judicial_appeal            |            0 |                       0 |                            0 |                    0 |               398 |                0 |
| timely_payment             |            0 |                       3 |                            0 |                    0 |                 0 |            49606 |

- Split: administrative_appeal -> administrative_appeal (62), delinquent_payment (4), (residual) (3), judicial_appeal (3)
- Split: coercive_credit_collection -> administrative_appeal (18), coercive_credit_collection (15), judicial_appeal (10)
- Split: delinquent_payment -> delinquent_payment (19), timely_payment (12), administrative_appeal (9), judicial_appeal (2)
- Split: timely_payment -> timely_payment (5), administrative_appeal (1)
- Merge: administrative_appeal (62), coercive_credit_collection (18), delinquent_payment (9), (residual) (1), timely_payment (1) -> administrative_appeal
- Merge: delinquent_payment (19), administrative_appeal (4) -> delinquent_payment
- Merge: judicial_appeal (64), coercive_credit_collection (10), administrative_appeal (3), delinquent_payment (2) -> judicial_appeal
- Merge: delinquent_payment (12), timely_payment (5), (residual) (2) -> timely_payment

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
| coercive_credit_collection | 84.1 | +9 | 59012 | 59012 | 0 | 0 | 0 | 100% |
| timely_payment | 66.7 | +38 | 49609 | 3226 | 0 | 0 | 46383 | 6% |
| delinquent_payment | 91.5 | +0 | 16917 | 16917 | 0 | 0 | 0 | 100% |
| administrative_appeal | 90.0 | +0 | 3682 | 3682 | 0 | 0 | 0 | 100% |
| judicial_appeal | 99.9 | -3 | 398 | 398 | 0 | 0 | 0 | 100% |

## Time to appeal filing, Prefecture (days) (id 113)

- Value set: worst 120.0, threshold 60.0, target 60.0 days
- Provenance: `statutory` — threshold 60 d: Art. 203 D.Lgs. 285/1992, the window for a ricorso al Prefetto; corroborated by the Delay Prefecture' < 60 days guard in Mannhardt et al. (2016, Fig. 8). target == threshold because an admissibility window is a boundary, not a gradient. worst 120 d illustrative (2x the window).
- **one-sided scale** (`target == threshold`: an admissibility boundary, not a gradient — every compliant value saturates at the same score)

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 48.6 | +100 | 150370 | 4036 | 146182 | 145 | 7 | 96% |
| coercive_credit_collection | 41.9 | +100 | 59012 | 281 | 58731 | 0 | 0 | 100% |
| timely_payment | — | — | 49609 | 0 | 49606 | 3 | 0 | 0% |
| delinquent_payment | 52.3 | +100 | 16917 | 55 | 16858 | 0 | 4 | 93% |
| administrative_appeal | 49.7 | +100 | 3682 | 3546 | 2 | 132 | 2 | 96% |
| judicial_appeal | 33.9 | +100 | 398 | 154 | 237 | 6 | 1 | 96% |

## Time to appeal filing, Judge (days) (id 175)

- Value set: worst 60.0, threshold 30.0, target 30.0 days
- Provenance: `statutory` — threshold 30 d: Art. 204-bis D.Lgs. 285/1992, the window for a ricorso al Giudice di Pace -- half the Prefecture window, which v1.1 collapsed into a single 60-day indicator taken from Mannhardt et al. (2016, Fig. 8)'s Delay Judge' guard rather than from the statute. worst 60 d illustrative (2x).
- **one-sided scale** (`target == threshold`: an admissibility boundary, not a gradient — every compliant value saturates at the same score)

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 95.9 | -100 | 150370 | 538 | 149815 | 17 | 0 | 97% |
| coercive_credit_collection | 60.6 | -100 | 59012 | 147 | 58865 | 0 | 0 | 100% |
| timely_payment | — | — | 49609 | 0 | 49609 | 0 | 0 | 0% |
| delinquent_payment | 112.1 | -100 | 16917 | 7 | 16910 | 0 | 0 | 100% |
| administrative_appeal | 138.3 | -100 | 3682 | 3 | 3679 | 0 | 0 | 100% |
| judicial_appeal | 108.9 | -100 | 398 | 381 | 0 | 17 | 0 | 96% |

## Average time to case closure (days) (id 114)

- Value set: worst 365.0, threshold 180.0, target 150.0 days
- Provenance: `external-by-analogy` — threshold 180 d: L. 241/1990 art. 2, which caps any administrative proceeding's term at 180 days. target 150 d: Art. 201's 90-day notification term plus Art. 203's 60-day payment/appeal window, i.e. the earliest lawful completion of an uncontested case. worst 365 d illustrative. Replaces v1.1's acknowledged invented placeholder.

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 378.7 | -100 | 150370 | 126840 | 0 | 0 | 23530 | 84% |
| coercive_credit_collection | 690.5 | -100 | 59012 | 59012 | 0 | 0 | 0 | 100% |
| timely_payment | 17.3 | +100 | 49609 | 49609 | 0 | 0 | 0 | 100% |
| delinquent_payment | 356.8 | -95 | 16917 | 16917 | 0 | 0 | 0 | 100% |
| administrative_appeal | 320.9 | -76 | 3682 | 595 | 0 | 0 | 3087 | 16% |
| judicial_appeal | 560.5 | -100 | 398 | 344 | 0 | 0 | 54 | 86% |

## Propagated softgoal satisfaction

Propagated from the measured indicators through the same decomposition and contribution graph Step 5a used as the taxonomy axis (`min` over And, `max` over Or/Xor, weighted-clamped sum over contributions).

Only softgoals carry a value: indicators are the sole seeds, and they reach the model through contribution links, so every goal and task in the decomposition tree evaluates to the default 0. Seeding a category's `anchor_ids` with full satisfaction would light the tree up, but it would also assert that a category existing *is* its goal being met — the confound this measure is supposed to expose, not commit.

| Softgoal | whole log | administrative_appeal | coercive_credit_collection | delinquent_payment | judicial_appeal | timely_payment |
|---|---|---|---|---|---|---|
| Maximize timely fine revenue | -48 | -38 | -46 | -48 | -52 | +69 |
| Minimize administrative & enforcement cost | -50 | -38 | -50 | -48 | -50 | +50 |
| Preserve offender's due-process rights | +0 | +0 | +0 | +0 | +0 | +0 |

## Secondary — guided vs. structural (HDBSCAN) (Task C3)

| row_category               |   (residual) |   cluster_0 |   cluster_1 |   cluster_10 |   cluster_11 |   cluster_12 |   cluster_13 |   cluster_14 |   cluster_2 |   cluster_3 |   cluster_4 |   cluster_5 |   cluster_6 |   cluster_7 |   cluster_8 |   cluster_9 |
|:---------------------------|-------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|-------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|
| (residual)                 |            1 |           2 |           1 |            0 |            0 |            0 |            0 |            0 |           0 |           0 |           0 |           0 |           0 |           0 |           0 |           0 |
| administrative_appeal      |           16 |           0 |           5 |           14 |            0 |            0 |            2 |            0 |           0 |           1 |           0 |           0 |          18 |           0 |           9 |           7 |
| coercive_credit_collection |            7 |           0 |           0 |            2 |           15 |            0 |            0 |            6 |           0 |           0 |          13 |           0 |           0 |           0 |           0 |           0 |
| delinquent_payment         |            4 |           0 |           0 |            4 |            0 |            1 |            0 |            0 |          21 |           6 |           0 |           0 |           4 |           1 |           1 |           0 |
| judicial_appeal            |           17 |           1 |           2 |            0 |            0 |           13 |           10 |            1 |           0 |           0 |           0 |          15 |           0 |           5 |           0 |           0 |
| timely_payment             |            2 |           3 |           1 |            0 |            0 |            0 |            0 |            0 |           0 |           0 |           0 |           0 |           0 |           0 |           0 |           0 |

## Notable findings

- **Open-mode replicate coverage swing traced to one ambiguous variant (2026-08-29).** `e1_open_rep1` and `e1_open_rep2` show identical variant-level coverage (229/231, 2 residual variants each) but a ~13.8-point gap in case-weighted coverage (99.995% vs. 86.2%). Root cause: variant V0003 (`Create Fine → Send Fine`, no further activity — an unresolved/still-open case) carries 20,385 cases (~13.6% of the whole log). Open-mode Step 6 classified it inconsistently across replicates — folded into the catch-all-like `standard_fine_lifecycle`/`standard_collection_or_payment` category in one replicate, left residual in the other — because open induction has no external criterion for "does not realize any category." **Guided mode classified the same variant as residual in both replicates**, with near-identical rationale each time ("does not resolve the case" / "remaining in the residual"): the goal model gives the LLM a stable boundary for what counts as resolved vs. residual that open induction lacks. This is a concrete, high-leverage illustration of exactly what Task C2's replicate design exists to catch — LLM-sampling noise can concentrate disproportionately in a single high-frequency variant, and case-weighted coverage is far more sensitive to it than variant-level coverage. Positive evidence for RQ1: the external semantic frame stabilizes the residual boundary, not only the category set.

## Replicate stability (Task C2)

rep1 vs. rep2 of each arm, same convention as the paired contrast below. Read the "guided vs. open" divergence against these: a cross-arm difference no larger than an arm's own rep1-rep2 movement is not separable from run-to-run variance. The open arm has no anchors, so this is its only stability check — Task C12 tests the guided taxonomy alone.

### guided rep1 vs. rep2

**guided_rep1 vs. guided_rep2** — partition divergence (Task D1)

| residual_handling   | weighting   |      AMI |      NMI |   n_observations | primary   |
|:--------------------|:------------|---------:|---------:|-----------------:|:----------|
| own_cluster         | variant     | 0.74558  | 0.755101 |              231 | True      |
| own_cluster         | case        | 0.994337 | 0.994338 |           150370 | False     |
| exclude             | variant     | 0.773601 | 0.77966  |              222 | False     |
| exclude             | case        | 0.996118 | 0.996118 |           129514 | False     |

_AMI/NMI measure divergence between two partitions, not classification accuracy: neither partition is ground truth, so agreement between the arms is not evidence that either is correct._


### open rep1 vs. rep2

**open_rep1 vs. open_rep2** — partition divergence (Task D1)

| residual_handling   | weighting   |      AMI |      NMI |   n_observations | primary   |
|:--------------------|:------------|---------:|---------:|-----------------:|:----------|
| own_cluster         | variant     | 0.499121 | 0.515796 |              231 | True      |
| own_cluster         | case        | 0.875915 | 0.875922 |           150370 | False     |
| exclude             | variant     | 0.501641 | 0.512959 |              222 | False     |
| exclude             | case        | 0.844425 | 0.844432 |           129317 | False     |

_AMI/NMI measure divergence between two partitions, not classification accuracy: neither partition is ground truth, so agreement between the arms is not evidence that either is correct._


_Read on the D1-primary `own_cluster` convention. Where the open arm's rep1-rep2 AMI is lower than the guided arm's, every "guided vs. open" figure for this dataset should be reported with that band, and the open arm's instability noted as a limit on the strength of the paired contrast (Task E7, extended to the open arm)._

### Replicate residual-set Jaccard (§6)

Jaccard similarity of an arm's two replicate residual variant-sets, on this axis. A value near 1 means the arm puts the same variants outside every category across identical-input reruns; near 0 means it does not. §6 reads the guided-over-open gap as evidence that the declared frame stabilizes the residual boundary, not only the category set.

- guided: 0.33
- open: 0.33

## Partition divergence (optional, Task D1)

**guided vs. open** — partition divergence (Task D1)

| residual_handling   | weighting   |      AMI |      NMI |   n_observations | primary   |
|:--------------------|:------------|---------:|---------:|-----------------:|:----------|
| own_cluster         | variant     | 0.301698 | 0.32479  |              231 | True      |
| own_cluster         | case        | 0.871733 | 0.87174  |           150370 | False     |
| exclude             | variant     | 0.275661 | 0.291557 |              226 | False     |
| exclude             | case        | 0.829703 | 0.829711 |           129615 | False     |

_AMI/NMI measure divergence between two partitions, not classification accuracy: neither partition is ground truth, so agreement between the arms is not evidence that either is correct._


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

## Secondary — guided vs. structural (HDBSCAN) (Task C3)

| row_category               |   (residual) |   cluster_0 |   cluster_1 |   cluster_2 |   cluster_3 |   cluster_4 |   cluster_5 |   cluster_6 |   cluster_7 |   cluster_8 |   cluster_9 |
|:---------------------------|-------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|
| (residual)                 |            1 |           3 |           0 |           0 |           0 |           0 |           0 |           0 |           0 |           0 |           0 |
| administrative_appeal      |            3 |           0 |           0 |          19 |           2 |           0 |           2 |          12 |          21 |           1 |           1 |
| coercive_credit_collection |            3 |           0 |          12 |           0 |           0 |           1 |           2 |           0 |          18 |           5 |           0 |
| delinquent_payment         |            0 |           0 |          20 |          16 |           1 |           0 |           1 |           4 |           7 |           1 |           0 |
| judicial_appeal            |            9 |           0 |           0 |           0 |           8 |          16 |           0 |           0 |           0 |          28 |           4 |
| timely_payment             |            0 |           5 |           1 |           2 |           0 |           0 |           0 |           0 |           2 |           0 |           0 |

## Notable findings

- **Open-mode replicate coverage swing traced to one ambiguous variant (2026-08-29).** `e1_open_rep1` and `e1_open_rep2` show identical variant-level coverage (229/231, 2 residual variants each) but a ~13.8-point gap in case-weighted coverage (99.995% vs. 86.2%). Root cause: variant V0003 (`Create Fine → Send Fine`, no further activity — an unresolved/still-open case) carries 20,385 cases (~13.6% of the whole log). Open-mode Step 6 classified it inconsistently across replicates — folded into the catch-all-like `standard_fine_lifecycle`/`standard_collection_or_payment` category in one replicate, left residual in the other — because open induction has no external criterion for "does not realize any category." **Guided mode classified the same variant as residual in both replicates**, with near-identical rationale each time ("does not resolve the case" / "remaining in the residual"): the goal model gives the LLM a stable boundary for what counts as resolved vs. residual that open induction lacks. This is a concrete, high-leverage illustration of exactly what Task C2's replicate design exists to catch — LLM-sampling noise can concentrate disproportionately in a single high-frequency variant, and case-weighted coverage is far more sensitive to it than variant-level coverage. Positive evidence for RQ1: the external semantic frame stabilizes the residual boundary, not only the category set.

## Partition divergence (optional, Task D1)

**guided vs. open** — partition divergence (Task D1)

| residual_handling   | weighting   |      AMI |      NMI |   n_observations | primary   |
|:--------------------|:------------|---------:|---------:|-----------------:|:----------|
| own_cluster         | variant     | 0.133977 | 0.162    |              231 | True      |
| own_cluster         | case        | 0.637371 | 0.637391 |           150370 | False     |
| exclude             | variant     | 0.121481 | 0.140011 |              226 | False     |
| exclude             | case        | 0.735382 | 0.735394 |           129615 | False     |

_AMI/NMI measure divergence between two partitions, not classification accuracy: neither partition is ground truth, so agreement between the arms is not evidence that either is correct._


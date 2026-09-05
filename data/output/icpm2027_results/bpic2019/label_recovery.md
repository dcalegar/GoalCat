# Task C1 — held-out label recovery (bpic2019, `e1_guided_rep1`)

_Label recovery under an axis-aligned frame (Task C1): the goal model's declared alternatives and `case:Item Category` name the same distinction by construction, so agreement is not accuracy and neither labelling is ground truth. The attribute is excluded from the narrative by construction, so it is held out from Steps 5-6 but not independent of the goal model's design. Consignment (anchor 13 / task T9) has no distinguishing activity label and its figure is not comparable to the other three._

- Cases: 251,734 | Variants: 11,973
- Case-weighted agreement (labelled only / overall incl. residual as miss): **29.9%** / 24.9%
- Variant-weighted agreement (labelled only / overall): **54.2%** / 42.5%

## Per-label recovery (case-weighted)

| label                          |   truth_cases |   guided_cases |   recall_cases |   precision_cases | comparable   |
|:-------------------------------|--------------:|---------------:|---------------:|------------------:|:-------------|
| 3-way match, invoice after GR  |         15182 |         151650 |         0.5294 |            0.053  | True         |
| 3-way match, invoice before GR |        221010 |          57801 |         0.2475 |            0.9464 | True         |
| 2-way match                    |          1044 |             82 |         0      |            0      | True         |
| Consignment                    |         14498 |             28 |         0      |            0      | False        |

_`recall` = held-out-label cases the guided arm also gave that label; `precision` = guided-label cases whose held-out label matches. Rows marked `comparable = False` carry the Consignment caveat above._

## Confusion matrix — case-weighted (rows = guided label, cols = `case:Item Category`)

| guided                         |   3-way match, invoice after GR |   3-way match, invoice before GR |   2-way match |   Consignment |    All |
|:-------------------------------|--------------------------------:|---------------------------------:|--------------:|--------------:|-------:|
| 3-way match, invoice after GR  |                            8038 |                           143567 |            45 |             0 | 151650 |
| 3-way match, invoice before GR |                            2690 |                            54700 |           411 |             0 |  57801 |
| 2-way match                    |                              70 |                                3 |             0 |             9 |     82 |
| Consignment                    |                              28 |                                0 |             0 |             0 |     28 |
| (residual)                     |                            4356 |                            22740 |           588 |         14489 |  42173 |
| All                            |                           15182 |                           221010 |          1044 |         14498 | 251734 |

## Confusion matrix — variant-weighted

| guided                         |   3-way match, invoice after GR |   3-way match, invoice before GR |   2-way match |   Consignment |   All |
|:-------------------------------|--------------------------------:|---------------------------------:|--------------:|--------------:|------:|
| 3-way match, invoice after GR  |                            1407 |                             3553 |            36 |             0 |  4996 |
| 3-way match, invoice before GR |                             566 |                             3678 |            60 |             0 |  4304 |
| 2-way match                    |                              60 |                                3 |             0 |             4 |    67 |
| Consignment                    |                              22 |                                0 |             0 |             0 |    22 |
| (residual)                     |                            1840 |                              465 |            49 |           230 |  2584 |
| All                            |                            3895 |                             7699 |           145 |           234 | 11973 |


---

# Task C1 — held-out label recovery (bpic2019, `e1_guided_rep2`)

_Label recovery under an axis-aligned frame (Task C1): the goal model's declared alternatives and `case:Item Category` name the same distinction by construction, so agreement is not accuracy and neither labelling is ground truth. The attribute is excluded from the narrative by construction, so it is held out from Steps 5-6 but not independent of the goal model's design. Consignment (anchor 13 / task T9) has no distinguishing activity label and its figure is not comparable to the other three._

- Cases: 251,734 | Variants: 11,973
- Case-weighted agreement (labelled only / overall incl. residual as miss): **27.3%** / 22.9%
- Variant-weighted agreement (labelled only / overall): **46.1%** / 36.3%

## Per-label recovery (case-weighted)

| label                          |   truth_cases |   guided_cases |   recall_cases |   precision_cases | comparable   |
|:-------------------------------|--------------:|---------------:|---------------:|------------------:|:-------------|
| 3-way match, invoice after GR  |         15182 |         158521 |         0.5543 |            0.0531 | True         |
| 3-way match, invoice before GR |        221010 |          51881 |         0.2227 |            0.9486 | True         |
| 2-way match                    |          1044 |            716 |         0      |            0      | True         |
| Consignment                    |         14498 |             15 |         0      |            0      | False        |

_`recall` = held-out-label cases the guided arm also gave that label; `precision` = guided-label cases whose held-out label matches. Rows marked `comparable = False` carry the Consignment caveat above._

## Confusion matrix — case-weighted (rows = guided label, cols = `case:Item Category`)

| guided                         |   3-way match, invoice after GR |   3-way match, invoice before GR |   2-way match |   Consignment |    All |
|:-------------------------------|--------------------------------:|---------------------------------:|--------------:|--------------:|-------:|
| 3-way match, invoice after GR  |                            8416 |                           150044 |            59 |             2 | 158521 |
| 3-way match, invoice before GR |                            2187 |                            49213 |           481 |             0 |  51881 |
| 2-way match                    |                             713 |                                3 |             0 |             0 |    716 |
| Consignment                    |                              15 |                                0 |             0 |             0 |     15 |
| (residual)                     |                            3851 |                            21750 |           504 |         14496 |  40601 |
| All                            |                           15182 |                           221010 |          1044 |         14498 | 251734 |

## Confusion matrix — variant-weighted

| guided                         |   3-way match, invoice after GR |   3-way match, invoice before GR |   2-way match |   Consignment |   All |
|:-------------------------------|--------------------------------:|---------------------------------:|--------------:|--------------:|------:|
| 3-way match, invoice after GR  |                            1640 |                             4546 |            53 |             2 |  6241 |
| 3-way match, invoice before GR |                             348 |                             2705 |            30 |             0 |  3083 |
| 2-way match                    |                              78 |                                3 |             0 |             0 |    81 |
| Consignment                    |                              15 |                                0 |             0 |             0 |    15 |
| (residual)                     |                            1814 |                              445 |            62 |           232 |  2553 |
| All                            |                            3895 |                             7699 |           145 |           234 | 11973 |


---

# Task C1 — held-out label recovery (bpic2019, `e1_guided_rep3`)

_Label recovery under an axis-aligned frame (Task C1): the goal model's declared alternatives and `case:Item Category` name the same distinction by construction, so agreement is not accuracy and neither labelling is ground truth. The attribute is excluded from the narrative by construction, so it is held out from Steps 5-6 but not independent of the goal model's design. Consignment (anchor 13 / task T9) has no distinguishing activity label and its figure is not comparable to the other three._

- Cases: 251,734 | Variants: 11,973
- Case-weighted agreement (labelled only / overall incl. residual as miss): **17.5%** / 14.7%
- Variant-weighted agreement (labelled only / overall): **43.6%** / 35.2%

## Per-label recovery (case-weighted)

| label                          |   truth_cases |   guided_cases |   recall_cases |   precision_cases | comparable   |
|:-------------------------------|--------------:|---------------:|---------------:|------------------:|:-------------|
| 3-way match, invoice after GR  |         15182 |         180181 |         0.5956 |            0.0502 | True         |
| 3-way match, invoice before GR |        221010 |          30154 |         0.1268 |            0.9294 | True         |
| 2-way match                    |          1044 |            804 |         0      |            0      | True         |
| Consignment                    |         14498 |            195 |         0      |            0      | False        |

_`recall` = held-out-label cases the guided arm also gave that label; `precision` = guided-label cases whose held-out label matches. Rows marked `comparable = False` carry the Consignment caveat above._

## Confusion matrix — case-weighted (rows = guided label, cols = `case:Item Category`)

| guided                         |   3-way match, invoice after GR |   3-way match, invoice before GR |   2-way match |   Consignment |    All |
|:-------------------------------|--------------------------------:|---------------------------------:|--------------:|--------------:|-------:|
| 3-way match, invoice after GR  |                            9043 |                           171034 |            66 |            38 | 180181 |
| 3-way match, invoice before GR |                            1597 |                            28024 |           533 |             0 |  30154 |
| 2-way match                    |                             798 |                                3 |             0 |             3 |    804 |
| Consignment                    |                             195 |                                0 |             0 |             0 |    195 |
| (residual)                     |                            3549 |                            21949 |           445 |         14457 |  40400 |
| All                            |                           15182 |                           221010 |          1044 |         14498 | 251734 |

## Confusion matrix — variant-weighted

| guided                         |   3-way match, invoice after GR |   3-way match, invoice before GR |   2-way match |   Consignment |   All |
|:-------------------------------|--------------------------------:|---------------------------------:|--------------:|--------------:|------:|
| 3-way match, invoice after GR  |                            1727 |                             4770 |            22 |             8 |  6527 |
| 3-way match, invoice before GR |                             326 |                             2492 |            90 |             0 |  2908 |
| 2-way match                    |                             146 |                                3 |             0 |             3 |   152 |
| Consignment                    |                              79 |                                0 |             0 |             0 |    79 |
| (residual)                     |                            1617 |                              434 |            33 |           223 |  2307 |
| All                            |                            3895 |                             7699 |           145 |           234 | 11973 |

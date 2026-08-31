# Task C1 — held-out label recovery (BPIC 2019)

## Result summary

| condition | case-agreement (labelled) | case-agreement (overall) | variant-agreement (labelled) |
|---|---|---|---|
| `e1_guided_rep1` | 18.1% | 15.0% | 48.7% |
| `e1_guided_rep2` | 22.8% | 18.9% | 46.8% |
| `e1_guided_no_sample_rep1` | 24.5% | ~20% | 44.1% |

Agreement between the guided Step 6 partition and `case:Item Category` is **low and consistent
across replicates**, with a distinctive structure: the two large 3-way categories are largely
**inverted** (of 221,010 cases the attribute labels "3-way, invoice before GR", `e1_guided_rep1`
places ~169,020 in `matched_after_gr`), and `2-way match` (1,044 cases) and `Consignment` (14,498
cases) are essentially unrecovered — they fall in the residual.

## Interpretation — the disagreement is mostly a definitional axis mismatch, not purely LLM error

`case:Item Category` is an **SAP purchase-order-line configuration attribute** — it records the
matching regime the PO line was *set up for* at creation, not the order the events actually took.
The guided categories key on the **observed** order of `Record Goods Receipt` vs. the invoice
events in the trace (anchor 5/6 descriptions: "invoice *recorded* after / before goods receipt").
These answer different questions:

| variant | cases | trace order | `case:Item Category` | guided (`rep1`) |
|---|---|---|---|---|
| V0001 | 50,286 | `… Vendor creates invoice → Record GR → Record Invoice Receipt …` | 96% "before GR" | `matched_after_gr` |
| V0002 | 30,798 | `… Record GR → Vendor creates invoice → Record Invoice Receipt …` | 95% "before GR" | `matched_after_gr` |
| V0007 | 8,835 | `… Vendor creates invoice → Record Invoice Receipt → Record GR …` | 100% "before GR" | `matched_before_gr` |

- **V0002** is configured "before GR" yet records goods receipt *before* the invoice is created —
  the attribute and any observed-order categorisation must disagree here by construction. ~30k
  cases of this kind alone cap achievable agreement well below 100%.
- **V0001** is a genuine guided-arm error on the *observed-order* question: the invoice is created
  (pos 1) before GR (pos 2), but the guided rationale anchored on `Record Invoice Receipt` (pos 3,
  after GR). BPIC 2019 has two invoice events (`Vendor creates invoice`, `Record Invoice
  Receipt`); the goal model's distinction hinges on the first, the LLM used the second. This one
  variant is ~50k of the ~169k "before→after" mislabels.
- **Consignment** carries the pre-registered caveat (no distinguishing activity label). **2-way
  match** is a real non-recovery: those cases land in the residual.

**Reporting stance (per the plan's Task C1):** this is label recovery under an axis that is
aligned *by construction* but is not independent ground truth — `case:Item Category` answers
"how was this line configured", the guided partition answers "what order did the events take".
Report the figure with this framing; do not present it as accuracy, and do not read the low
number as the guided partition being wrong in an absolute sense.

---

# Task C1 — held-out label recovery (bpic2019, `e1_guided_rep1`)

_Label recovery under an axis-aligned frame (Task C1): the goal model's declared alternatives and `case:Item Category` name the same distinction by construction, so agreement is not accuracy and neither labelling is ground truth. The attribute is excluded from the narrative by construction, so it is held out from Steps 5-6 but not independent of the goal model's design. Consignment (anchor 13 / task T9) has no distinguishing activity label and its figure is not comparable to the other three._

- Cases: 251,734 | Variants: 11,973
- Case-weighted agreement (labelled only / overall incl. residual as miss): **18.1%** / 15.0%
- Variant-weighted agreement (labelled only / overall): **48.7%** / 38.2%

## Per-label recovery (case-weighted)

| label                          |   truth_cases |   guided_cases |   recall_cases |   precision_cases | comparable   |
|:-------------------------------|--------------:|---------------:|---------------:|------------------:|:-------------|
| 3-way match, invoice after GR  |         15182 |         178274 |         0.6068 |            0.0517 | True         |
| 3-way match, invoice before GR |        221010 |          30306 |         0.1291 |            0.9413 | True         |
| 2-way match                    |          1044 |             66 |         0      |            0      | True         |
| Consignment                    |         14498 |             14 |         0      |            0      | False        |

_`recall` = held-out-label cases the guided arm also gave that label; `precision` = guided-label cases whose held-out label matches. Rows marked `comparable = False` carry the Consignment caveat above._

## Confusion matrix — case-weighted (rows = guided label, cols = `case:Item Category`)

| guided                         |   3-way match, invoice after GR |   3-way match, invoice before GR |   2-way match |   Consignment |    All |
|:-------------------------------|--------------------------------:|---------------------------------:|--------------:|--------------:|-------:|
| 3-way match, invoice after GR  |                            9213 |                           169020 |            40 |             1 | 178274 |
| 3-way match, invoice before GR |                            1365 |                            28528 |           413 |             0 |  30306 |
| 2-way match                    |                              62 |                                1 |             0 |             3 |     66 |
| Consignment                    |                              14 |                                0 |             0 |             0 |     14 |
| (residual)                     |                            4528 |                            23461 |           591 |         14494 |  43074 |
| All                            |                           15182 |                           221010 |          1044 |         14498 | 251734 |

## Confusion matrix — variant-weighted

| guided                         |   3-way match, invoice after GR |   3-way match, invoice before GR |   2-way match |   Consignment |   All |
|:-------------------------------|--------------------------------:|---------------------------------:|--------------:|--------------:|------:|
| 3-way match, invoice after GR  |                            1628 |                             4284 |            32 |             1 |  5945 |
| 3-way match, invoice before GR |                             393 |                             2945 |            27 |             0 |  3365 |
| 2-way match                    |                              61 |                                1 |             0 |             3 |    65 |
| Consignment                    |                              14 |                                0 |             0 |             0 |    14 |
| (residual)                     |                            1799 |                              469 |            86 |           230 |  2584 |
| All                            |                            3895 |                             7699 |           145 |           234 | 11973 |


---

# Task C1 — held-out label recovery (bpic2019, `e1_guided_rep2`)

_Label recovery under an axis-aligned frame (Task C1): the goal model's declared alternatives and `case:Item Category` name the same distinction by construction, so agreement is not accuracy and neither labelling is ground truth. The attribute is excluded from the narrative by construction, so it is held out from Steps 5-6 but not independent of the goal model's design. Consignment (anchor 13 / task T9) has no distinguishing activity label and its figure is not comparable to the other three._

- Cases: 251,734 | Variants: 11,973
- Case-weighted agreement (labelled only / overall incl. residual as miss): **22.8%** / 18.9%
- Variant-weighted agreement (labelled only / overall): **46.8%** / 36.5%

## Per-label recovery (case-weighted)

| label                          |   truth_cases |   guided_cases |   recall_cases |   precision_cases | comparable   |
|:-------------------------------|--------------:|---------------:|---------------:|------------------:|:-------------|
| 3-way match, invoice after GR  |         15182 |         167044 |         0.5719 |            0.052  | True         |
| 3-way match, invoice before GR |        221010 |          41382 |         0.1762 |            0.9411 | True         |
| 2-way match                    |          1044 |             72 |         0.0134 |            0.1944 | True         |
| Consignment                    |         14498 |             45 |         0      |            0      | False        |

_`recall` = held-out-label cases the guided arm also gave that label; `precision` = guided-label cases whose held-out label matches. Rows marked `comparable = False` carry the Consignment caveat above._

## Confusion matrix — case-weighted (rows = guided label, cols = `case:Item Category`)

| guided                         |   3-way match, invoice after GR |   3-way match, invoice before GR |   2-way match |   Consignment |    All |
|:-------------------------------|--------------------------------:|---------------------------------:|--------------:|--------------:|-------:|
| 3-way match, invoice after GR  |                            8683 |                           158339 |            15 |             7 | 167044 |
| 3-way match, invoice before GR |                            1973 |                            38944 |           465 |             0 |  41382 |
| 2-way match                    |                              11 |                               40 |            14 |             7 |     72 |
| Consignment                    |                              45 |                                0 |             0 |             0 |     45 |
| (residual)                     |                            4470 |                            23687 |           550 |         14484 |  43191 |
| All                            |                           15182 |                           221010 |          1044 |         14498 | 251734 |

## Confusion matrix — variant-weighted

| guided                         |   3-way match, invoice after GR |   3-way match, invoice before GR |   2-way match |   Consignment |   All |
|:-------------------------------|--------------------------------:|---------------------------------:|--------------:|--------------:|------:|
| 3-way match, invoice after GR  |                            1663 |                             4464 |            13 |             6 |  6146 |
| 3-way match, invoice before GR |                             348 |                             2701 |            75 |             0 |  3124 |
| 2-way match                    |                              11 |                                7 |             7 |             1 |    26 |
| Consignment                    |                              43 |                                0 |             0 |             0 |    43 |
| (residual)                     |                            1830 |                              527 |            50 |           227 |  2634 |
| All                            |                            3895 |                             7699 |           145 |           234 | 11973 |


---

# Task C1 — held-out label recovery (bpic2019, `e1_guided_no_sample_rep1`)

_Label recovery under an axis-aligned frame (Task C1): the goal model's declared alternatives and `case:Item Category` name the same distinction by construction, so agreement is not accuracy and neither labelling is ground truth. The attribute is excluded from the narrative by construction, so it is held out from Steps 5-6 but not independent of the goal model's design. Consignment (anchor 13 / task T9) has no distinguishing activity label and its figure is not comparable to the other three._

- Cases: 251,734 | Variants: 11,973
- Case-weighted agreement (labelled only / overall incl. residual as miss): **24.5%** / 20.1%
- Variant-weighted agreement (labelled only / overall): **44.1%** / 34.1%

## Per-label recovery (case-weighted)

| label                          |   truth_cases |   guided_cases |   recall_cases |   precision_cases | comparable   |
|:-------------------------------|--------------:|---------------:|---------------:|------------------:|:-------------|
| 3-way match, invoice after GR  |         15182 |         162341 |         0.5665 |            0.053  | True         |
| 3-way match, invoice before GR |        221010 |          44153 |         0.1905 |            0.9535 | True         |
| 2-way match                    |          1044 |            680 |         0.0077 |            0.0118 | True         |
| Consignment                    |         14498 |            134 |         0      |            0      | False        |

_`recall` = held-out-label cases the guided arm also gave that label; `precision` = guided-label cases whose held-out label matches. Rows marked `comparable = False` carry the Consignment caveat above._

## Confusion matrix — case-weighted (rows = guided label, cols = `case:Item Category`)

| guided                         |   3-way match, invoice after GR |   3-way match, invoice before GR |   2-way match |   Consignment |    All |
|:-------------------------------|--------------------------------:|---------------------------------:|--------------:|--------------:|-------:|
| 3-way match, invoice after GR  |                            8600 |                           153712 |            28 |             1 | 162341 |
| 3-way match, invoice before GR |                            1581 |                            42098 |           474 |             0 |  44153 |
| 2-way match                    |                             672 |                                0 |             8 |             0 |    680 |
| Consignment                    |                             134 |                                0 |             0 |             0 |    134 |
| (residual)                     |                            4195 |                            25200 |           534 |         14497 |  44426 |
| All                            |                           15182 |                           221010 |          1044 |         14498 | 251734 |

## Confusion matrix — variant-weighted

| guided                         |   3-way match, invoice after GR |   3-way match, invoice before GR |   2-way match |   Consignment |   All |
|:-------------------------------|--------------------------------:|---------------------------------:|--------------:|--------------:|------:|
| 3-way match, invoice after GR  |                            1580 |                             4650 |            22 |             1 |  6253 |
| 3-way match, invoice before GR |                             337 |                             2499 |            51 |             0 |  2887 |
| 2-way match                    |                              47 |                                0 |             4 |             0 |    51 |
| Consignment                    |                              67 |                                0 |             0 |             0 |    67 |
| (residual)                     |                            1864 |                              550 |            68 |           233 |  2715 |
| All                            |                            3895 |                             7699 |           145 |           234 | 11973 |

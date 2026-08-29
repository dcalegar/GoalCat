# Step 7b — indicator satisfaction

Goal model: `sepsis_goal_model.jucm`

Satisfaction is on GRL's [-100, +100] scale, converted from the measured value by each indicator's own `KPIEvalValueSet`. The measured value is reported beside it in every row: a score against an illustrative threshold reads exactly like one against a statute, and only the provenance column separates them.

## Time to antibiotics (hours) (id 24)

- Value set: worst 3.0, threshold 1.8, target 1.0 hours
- Provenance: `guideline` — target 1 h or less, threshold 1.8 h, worst 3 h: the 1-hour antibiotic-administration window of the Surviving Sepsis Campaign 2016 international guideline (Rhodes et al., 2017), identified by Mannhardt & Blinde (2017, SS2) as the applicable rule for this exact log. worst/threshold/target reused verbatim from Ghasemi (2021, Ch.8, Table 19), set after physician consultation. See sepsisGM_description.md SS6.

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 1.9 | -4 | 1050 | 823 | 0 | 1 | 226 | 78% |
| release_a | 1.8 | +1 | 525 | 465 | 0 | 1 | 59 | 89% |
| admission_nc | 2.0 | -18 | 98 | 84 | 0 | 0 | 14 | 86% |
| release_b | 1.5 | +40 | 54 | 43 | 0 | 0 | 11 | 80% |
| admission_ic | 1.0 | +96 | 11 | 10 | 0 | 0 | 1 | 91% |
| release_c | 1.8 | +2 | 23 | 19 | 0 | 0 | 4 | 83% |
| release_d | 2.6 | -62 | 23 | 20 | 0 | 0 | 3 | 87% |
| release_e | 3.5 | -100 | 6 | 3 | 0 | 0 | 3 | 50% |

## Time to lactate measurement (hours) (id 25)

- Value set: worst 7.0, threshold 5.0, target 3.0 hours
- Provenance: `guideline` — target 3 h or less, threshold 5 h, worst 7 h: the 3-hour lactate-measurement window of the Surviving Sepsis Campaign 2016 guideline (Rhodes et al., 2017) via Mannhardt & Blinde (2017, SS2). worst/threshold/target reused verbatim from Ghasemi (2021, Ch.8, Table 19), physician-consulted. See sepsisGM_description.md SS6.

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 1.4 | +100 | 1050 | 739 | 0 | 1 | 310 | 70% |
| release_a | 2.1 | +100 | 525 | 415 | 0 | 1 | 109 | 79% |
| admission_nc | 0.3 | +100 | 98 | 70 | 0 | 0 | 28 | 71% |
| release_b | 0.8 | +100 | 54 | 42 | 0 | 0 | 12 | 78% |
| admission_ic | 2.0 | +100 | 11 | 11 | 0 | 0 | 0 | 100% |
| release_c | 0.2 | +100 | 23 | 19 | 0 | 0 | 4 | 83% |
| release_d | 0.3 | +100 | 23 | 18 | 0 | 0 | 5 | 78% |
| release_e | 0.2 | +100 | 6 | 4 | 0 | 0 | 2 | 67% |

## Post-discharge ER return (binary) (id 26)

- Value set: worst 1.0, threshold n/a, target 0.0 binary
- Provenance: `illustrative` — target 0 (no return), worst 1 (returned): reused from Ghasemi (2021, Ch.8) as a common healthcare-system goal, not traced to a guideline window and with no threshold defined in the source. Measured as the presence of Return ER anywhere in the case, over every case in scope; a case with no captured discharge counts as no return -- see sepsisGM_description.md SS6/SS7.

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 0.3 | -28 | 1050 | 1050 | 0 | 0 | 0 | 100% |
| release_a | 0.3 | -34 | 525 | 525 | 0 | 0 | 0 | 100% |
| admission_nc | 0.3 | -31 | 98 | 98 | 0 | 0 | 0 | 100% |
| release_b | 0.0 | +100 | 54 | 54 | 0 | 0 | 0 | 100% |
| admission_ic | 0.5 | -45 | 11 | 11 | 0 | 0 | 0 | 100% |
| release_c | 0.2 | -17 | 23 | 23 | 0 | 0 | 0 | 100% |
| release_d | 0.4 | -39 | 23 | 23 | 0 | 0 | 0 | 100% |
| release_e | 0.2 | -16 | 6 | 6 | 0 | 0 | 0 | 100% |

## Propagated softgoal satisfaction

Propagated from the measured indicators through the same decomposition and contribution graph Step 5a used as the taxonomy axis (`min` over And, `max` over Or/Xor, weighted-clamped sum over contributions).

Only softgoals carry a value: indicators are the sole seeds, and they reach the model through contribution links, so every goal and task in the decomposition tree evaluates to the default 0. Seeding a category's `anchor_ids` with full satisfaction would light the tree up, but it would also assert that a category existing *is* its goal being met — the confound this measure is supposed to expose, not commit.

| Softgoal | whole log | admission_ic | admission_nc | release_a | release_b | release_c | release_d | release_e |
|---|---|---|---|---|---|---|---|---|
| Avoid post-discharge deterioration | -14 | -22 | -16 | -17 | +50 | -8 | -20 | -8 |
| Minimize time-to-treatment | +48 | +98 | +41 | +50 | +70 | +51 | +19 | +0 |


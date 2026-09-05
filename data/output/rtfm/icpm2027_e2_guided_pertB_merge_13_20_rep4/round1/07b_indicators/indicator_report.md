# Step 7b — indicator satisfaction

Goal model: `rtfm_goal_model__pertB_merge_13_20.jucm`

Satisfaction is on GRL's [-100, +100] scale, converted from the measured value by each indicator's own `KPIEvalValueSet`. The measured value is reported beside it in every row: a score against an illustrative threshold reads exactly like one against a statute, and only the provenance column separates them.

## Time to fine dispatch (days) (id 112)

- Value set: worst 360.0, threshold 90.0, target 30.0 days
- Provenance: `statutory` — threshold 90 d and worst 360 d: Art. 201 D.Lgs. 285/1992 (ordinary notification term; extended term for parties resident abroad). target 30 d: L. 241/1990 art. 2 c.2, the default term for concluding an administrative proceeding, applied by analogy as an operational aspiration -- the specific term in Art. 201 is what binds.

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 87.5 | +4 | 150370 | 103987 | 0 | 0 | 46383 | 69% |
| enforced_case_closure | 84.1 | +9 | 58873 | 58873 | 0 | 0 | 0 | 100% |
| timely_payment | 87.6 | +3 | 66620 | 20237 | 0 | 0 | 46383 | 30% |
| administrative_appeal | 89.7 | +0 | 3618 | 3618 | 0 | 0 | 0 | 100% |
| judicial_appeal | 94.7 | -1 | 504 | 504 | 0 | 0 | 0 | 100% |

## Time to appeal filing, Prefecture (days) (id 113)

- Value set: worst 120.0, threshold 60.0, target 60.0 days
- Provenance: `statutory` — threshold 60 d: Art. 203 D.Lgs. 285/1992, the window for a ricorso al Prefetto; corroborated by the Delay Prefecture' < 60 days guard in Mannhardt et al. (2016, Fig. 8). target == threshold because an admissibility window is a boundary, not a gradient. worst 120 d illustrative (2x the window).
- **one-sided scale** (`target == threshold`: an admissibility boundary, not a gradient — every compliant value saturates at the same score)

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 48.6 | +100 | 150370 | 4036 | 146182 | 145 | 7 | 96% |
| enforced_case_closure | 41.6 | +100 | 58873 | 268 | 58605 | 0 | 0 | 100% |
| timely_payment | 67.1 | -11 | 66620 | 143 | 66468 | 4 | 5 | 94% |
| administrative_appeal | 48.9 | +100 | 3618 | 3479 | 4 | 134 | 1 | 96% |
| judicial_appeal | 35.0 | +100 | 504 | 146 | 354 | 3 | 1 | 97% |

## Time to appeal filing, Judge (days) (id 175)

- Value set: worst 60.0, threshold 30.0, target 30.0 days
- Provenance: `statutory` — threshold 30 d: Art. 204-bis D.Lgs. 285/1992, the window for a ricorso al Giudice di Pace -- half the Prefecture window, which v1.1 collapsed into a single 60-day indicator taken from Mannhardt et al. (2016, Fig. 8)'s Delay Judge' guard rather than from the statute. worst 60 d illustrative (2x).
- **one-sided scale** (`target == threshold`: an admissibility boundary, not a gradient — every compliant value saturates at the same score)

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 95.9 | -100 | 150370 | 538 | 149815 | 17 | 0 | 97% |
| enforced_case_closure | 135.5 | -100 | 58873 | 15 | 58858 | 0 | 0 | 100% |
| timely_payment | 89.1 | -100 | 66620 | 18 | 66602 | 0 | 0 | 100% |
| administrative_appeal | 128.3 | -100 | 3618 | 12 | 3603 | 3 | 0 | 80% |
| judicial_appeal | 94.1 | -100 | 504 | 493 | 0 | 11 | 0 | 98% |

## Average time to case closure (days) (id 114)

- Value set: worst 365.0, threshold 180.0, target 150.0 days
- Provenance: `external-by-analogy` — threshold 180 d: L. 241/1990 art. 2, which caps any administrative proceeding's term at 180 days. target 150 d: Art. 201's 90-day notification term plus Art. 203's 60-day payment/appeal window, i.e. the earliest lawful completion of an uncontested case. worst 365 d illustrative. Replaces v1.1's acknowledged invented placeholder.

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 378.7 | -100 | 150370 | 126840 | 0 | 0 | 23530 | 84% |
| enforced_case_closure | 689.6 | -100 | 58873 | 58873 | 0 | 0 | 0 | 100% |
| timely_payment | 104.2 | +100 | 66620 | 66620 | 0 | 0 | 0 | 100% |
| administrative_appeal | 311.3 | -70 | 3618 | 524 | 0 | 0 | 3094 | 14% |
| judicial_appeal | 701.8 | -100 | 504 | 460 | 0 | 0 | 44 | 91% |

## Propagated softgoal satisfaction

Propagated from the measured indicators through the same decomposition and contribution graph Step 5a used as the taxonomy axis (`min` over And, `max` over Or/Xor, weighted-clamped sum over contributions).

Only softgoals carry a value: indicators are the sole seeds, and they reach the model through contribution links, so every goal and task in the decomposition tree evaluates to the default 0. Seeding a category's `anchor_ids` with full satisfaction would light the tree up, but it would also assert that a category existing *is* its goal being met — the confound this measure is supposed to expose, not commit.

| Softgoal | whole log | administrative_appeal | enforced_case_closure | judicial_appeal | timely_payment |
|---|---|---|---|---|---|
| Maximize timely fine revenue | -48 | -35 | -46 | -50 | +52 |
| Minimize administrative & enforcement cost | -50 | -35 | -50 | -50 | +50 |
| Preserve offender's due-process rights | +0 | +0 | +0 | +0 | -56 |


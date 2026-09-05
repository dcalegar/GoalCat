# Step 7b — indicator satisfaction

Goal model: `rtfm_goal_model__pertB_merge_13_20.jucm`

Satisfaction is on GRL's [-100, +100] scale, converted from the measured value by each indicator's own `KPIEvalValueSet`. The measured value is reported beside it in every row: a score against an illustrative threshold reads exactly like one against a statute, and only the provenance column separates them.

## Time to fine dispatch (days) (id 112)

- Value set: worst 360.0, threshold 90.0, target 30.0 days
- Provenance: `statutory` — threshold 90 d and worst 360 d: Art. 201 D.Lgs. 285/1992 (ordinary notification term; extended term for parties resident abroad). target 30 d: L. 241/1990 art. 2 c.2, the default term for concluding an administrative proceeding, applied by analogy as an operational aspiration -- the specific term in Art. 201 is what binds.

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 87.5 | +4 | 150370 | 103987 | 0 | 0 | 46383 | 69% |
| timely_payment | 87.1 | +4 | 66878 | 20495 | 0 | 0 | 46383 | 31% |
| administrative_appeal | 89.3 | +1 | 3888 | 3888 | 0 | 0 | 0 | 100% |
| judicial_appeal | 95.0 | -1 | 536 | 536 | 0 | 0 | 0 | 100% |
| merged_closure | 81.2 | +14 | 76 | 76 | 0 | 0 | 0 | 100% |

## Time to appeal filing, Prefecture (days) (id 113)

- Value set: worst 120.0, threshold 60.0, target 60.0 days
- Provenance: `statutory` — threshold 60 d: Art. 203 D.Lgs. 285/1992, the window for a ricorso al Prefetto; corroborated by the Delay Prefecture' < 60 days guard in Mannhardt et al. (2016, Fig. 8). target == threshold because an admissibility window is a boundary, not a gradient. worst 120 d illustrative (2x the window).
- **one-sided scale** (`target == threshold`: an admissibility boundary, not a gradient — every compliant value saturates at the same score)

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 48.6 | +100 | 150370 | 4036 | 146182 | 145 | 7 | 96% |
| timely_payment | 46.7 | +100 | 66878 | 47 | 66823 | 3 | 5 | 85% |
| administrative_appeal | 49.6 | +100 | 3888 | 3740 | 12 | 135 | 1 | 96% |
| judicial_appeal | 34.6 | +100 | 536 | 164 | 365 | 6 | 1 | 96% |
| merged_closure | 30.9 | +100 | 76 | 57 | 18 | 1 | 0 | 98% |

## Time to appeal filing, Judge (days) (id 175)

- Value set: worst 60.0, threshold 30.0, target 30.0 days
- Provenance: `statutory` — threshold 30 d: Art. 204-bis D.Lgs. 285/1992, the window for a ricorso al Giudice di Pace -- half the Prefecture window, which v1.1 collapsed into a single 60-day indicator taken from Mannhardt et al. (2016, Fig. 8)'s Delay Judge' guard rather than from the statute. worst 60 d illustrative (2x).
- **one-sided scale** (`target == threshold`: an admissibility boundary, not a gradient — every compliant value saturates at the same score)

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 95.9 | -100 | 150370 | 538 | 149815 | 17 | 0 | 97% |
| timely_payment | 124.0 | -100 | 66878 | 8 | 66870 | 0 | 0 | 100% |
| administrative_appeal | 190.6 | -100 | 3888 | 10 | 3878 | 0 | 0 | 100% |
| judicial_appeal | 93.8 | -100 | 536 | 519 | 0 | 17 | 0 | 97% |
| merged_closure | — | — | 76 | 0 | 76 | 0 | 0 | 0% |

## Average time to case closure (days) (id 114)

- Value set: worst 365.0, threshold 180.0, target 150.0 days
- Provenance: `external-by-analogy` — threshold 180 d: L. 241/1990 art. 2, which caps any administrative proceeding's term at 180 days. target 150 d: Art. 201's 90-day notification term plus Art. 203's 60-day payment/appeal window, i.e. the earliest lawful completion of an uncontested case. worst 365 d illustrative. Replaces v1.1's acknowledged invented placeholder.

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 378.7 | -100 | 150370 | 126840 | 0 | 0 | 23530 | 84% |
| timely_payment | 103.2 | +100 | 66878 | 66878 | 0 | 0 | 0 | 100% |
| administrative_appeal | 485.5 | -100 | 3888 | 797 | 0 | 0 | 3091 | 20% |
| judicial_appeal | 706.8 | -100 | 536 | 482 | 0 | 0 | 54 | 90% |
| merged_closure | 420.9 | -100 | 76 | 76 | 0 | 0 | 0 | 100% |

## Propagated softgoal satisfaction

Propagated from the measured indicators through the same decomposition and contribution graph Step 5a used as the taxonomy axis (`min` over And, `max` over Or/Xor, weighted-clamped sum over contributions).

Only softgoals carry a value: indicators are the sole seeds, and they reach the model through contribution links, so every goal and task in the decomposition tree evaluates to the default 0. Seeding a category's `anchor_ids` with full satisfaction would light the tree up, but it would also assert that a category existing *is* its goal being met — the confound this measure is supposed to expose, not commit.

| Softgoal | whole log | administrative_appeal | judicial_appeal | merged_closure | timely_payment |
|---|---|---|---|---|---|
| Maximize timely fine revenue | -48 | -50 | -50 | -43 | +52 |
| Minimize administrative & enforcement cost | -50 | -50 | -50 | -50 | +50 |
| Preserve offender's due-process rights | +0 | +0 | +0 | +50 | +0 |


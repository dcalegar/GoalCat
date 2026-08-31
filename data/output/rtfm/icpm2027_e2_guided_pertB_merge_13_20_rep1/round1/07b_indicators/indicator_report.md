# Step 7b — indicator satisfaction

Goal model: `rtfm_goal_model__pertB_merge_13_20.jucm`

Satisfaction is on GRL's [-100, +100] scale, converted from the measured value by each indicator's own `KPIEvalValueSet`. The measured value is reported beside it in every row: a score against an illustrative threshold reads exactly like one against a statute, and only the provenance column separates them.

## Time to fine dispatch (days) (id 112)

- Value set: worst 360.0, threshold 90.0, target 30.0 days
- Provenance: `statutory` — threshold 90 d and worst 360 d: Art. 201 D.Lgs. 285/1992 (ordinary notification term; extended term for parties resident abroad). target 30 d: L. 241/1990 art. 2 c.2, the default term for concluding an administrative proceeding, applied by analogy as an operational aspiration -- the specific term in Art. 201 is what binds.

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 87.5 | +4 | 150370 | 103987 | 0 | 0 | 46383 | 69% |
| timely_payment | 87.6 | +4 | 66574 | 20191 | 0 | 0 | 46383 | 30% |
| administrative_appeal | 89.3 | +1 | 3904 | 3904 | 0 | 0 | 0 | 100% |
| judicial_appeal | 95.5 | -2 | 531 | 531 | 0 | 0 | 0 | 100% |
| merged_closure | 90.5 | +0 | 18 | 18 | 0 | 0 | 0 | 100% |

## Time to appeal filing, Prefecture (days) (id 113)

- Value set: worst 120.0, threshold 60.0, target 60.0 days
- Provenance: `statutory` — threshold 60 d: Art. 203 D.Lgs. 285/1992, the window for a ricorso al Prefetto; corroborated by the Delay Prefecture' < 60 days guard in Mannhardt et al. (2016, Fig. 8). target == threshold because an admissibility window is a boundary, not a gradient. worst 120 d illustrative (2x the window).
- **one-sided scale** (`target == threshold`: an admissibility boundary, not a gradient — every compliant value saturates at the same score)

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 48.6 | +100 | 150370 | 4036 | 146182 | 145 | 7 | 96% |
| timely_payment | 47.1 | +100 | 66574 | 92 | 66473 | 3 | 6 | 91% |
| administrative_appeal | 49.1 | +100 | 3904 | 3770 | 2 | 132 | 0 | 97% |
| judicial_appeal | 38.1 | +100 | 531 | 162 | 362 | 6 | 1 | 96% |
| merged_closure | 16.0 | +100 | 18 | 3 | 15 | 0 | 0 | 100% |

## Time to appeal filing, Judge (days) (id 175)

- Value set: worst 60.0, threshold 30.0, target 30.0 days
- Provenance: `statutory` — threshold 30 d: Art. 204-bis D.Lgs. 285/1992, the window for a ricorso al Giudice di Pace -- half the Prefecture window, which v1.1 collapsed into a single 60-day indicator taken from Mannhardt et al. (2016, Fig. 8)'s Delay Judge' guard rather than from the statute. worst 60 d illustrative (2x).
- **one-sided scale** (`target == threshold`: an admissibility boundary, not a gradient — every compliant value saturates at the same score)

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 95.9 | -100 | 150370 | 538 | 149815 | 17 | 0 | 97% |
| timely_payment | 109.6 | -100 | 66574 | 12 | 66562 | 0 | 0 | 100% |
| administrative_appeal | 111.1 | -100 | 3904 | 10 | 3894 | 0 | 0 | 100% |
| judicial_appeal | 95.4 | -100 | 531 | 514 | 0 | 17 | 0 | 97% |
| merged_closure | 26.0 | +100 | 18 | 1 | 17 | 0 | 0 | 100% |

## Average time to case closure (days) (id 114)

- Value set: worst 365.0, threshold 180.0, target 150.0 days
- Provenance: `external-by-analogy` — threshold 180 d: L. 241/1990 art. 2, which caps any administrative proceeding's term at 180 days. target 150 d: Art. 201's 90-day notification term plus Art. 203's 60-day payment/appeal window, i.e. the earliest lawful completion of an uncontested case. worst 365 d illustrative. Replaces v1.1's acknowledged invented placeholder.

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 378.7 | -100 | 150370 | 126840 | 0 | 0 | 23530 | 84% |
| timely_payment | 103.9 | +100 | 66574 | 66574 | 0 | 0 | 0 | 100% |
| administrative_appeal | 486.2 | -100 | 3904 | 812 | 0 | 0 | 3092 | 21% |
| judicial_appeal | 716.4 | -100 | 531 | 482 | 0 | 0 | 49 | 91% |
| merged_closure | 682.6 | -100 | 18 | 18 | 0 | 0 | 0 | 100% |

## Propagated softgoal satisfaction

Propagated from the measured indicators through the same decomposition and contribution graph Step 5a used as the taxonomy axis (`min` over And, `max` over Or/Xor, weighted-clamped sum over contributions).

Only softgoals carry a value: indicators are the sole seeds, and they reach the model through contribution links, so every goal and task in the decomposition tree evaluates to the default 0. Seeding a category's `anchor_ids` with full satisfaction would light the tree up, but it would also assert that a category existing *is* its goal being met — the confound this measure is supposed to expose, not commit.

| Softgoal | whole log | administrative_appeal | judicial_appeal | merged_closure | timely_payment |
|---|---|---|---|---|---|
| Maximize timely fine revenue | -48 | -50 | -51 | -50 | +52 |
| Minimize administrative & enforcement cost | -50 | -50 | -50 | -50 | +50 |
| Preserve offender's due-process rights | +0 | +0 | +0 | +100 | +0 |


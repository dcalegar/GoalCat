# Step 7b — indicator satisfaction

Goal model: `rtfm_mini_goal_model.jucm`

Satisfaction is on GRL's [-100, +100] scale, converted from the measured value by each indicator's own `KPIEvalValueSet`. The measured value is reported beside it in every row: a score against an illustrative threshold reads exactly like one against a statute, and only the provenance column separates them.

## Time to fine dispatch (days) (id 112)

- Value set: worst 360.0, threshold 90.0, target 30.0 days
- Provenance: `statutory` — threshold 90 d and worst 360 d: Art. 201 D.Lgs. 285/1992 (ordinary notification term; extended term for parties resident abroad). target 30 d: L. 241/1990 art. 2 c.2, the default term for concluding an administrative proceeding, applied by analogy as an operational aspiration -- the specific term in Art. 201 is what binds.

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 98.7 | -3 | 8 | 7 | 0 | 0 | 1 | 88% |
| coercive_credit_collection | 132.0 | -15 | 1 | 1 | 0 | 0 | 0 | 100% |
| delinquent_payment | 126.3 | -13 | 3 | 3 | 0 | 0 | 0 | 100% |
| timely_payment | — | — | 1 | 0 | 0 | 0 | 1 | 0% |
| judicial_appeal_judge | 46.0 | +73 | 1 | 1 | 0 | 0 | 0 | 100% |
| administrative_appeal_prefecture | 0.0 | +100 | 1 | 1 | 0 | 0 | 0 | 100% |

## Time to appeal filing, Prefecture (days) (id 113)

- Value set: worst 120.0, threshold 60.0, target 60.0 days
- Provenance: `statutory` — threshold 60 d: Art. 203 D.Lgs. 285/1992, the window for a ricorso al Prefetto; corroborated by the Delay Prefecture' < 60 days guard in Mannhardt et al. (2016, Fig. 8). target == threshold because an admissibility window is a boundary, not a gradient. worst 120 d illustrative (2x the window).
- **one-sided scale** (`target == threshold`: an admissibility boundary, not a gradient — every compliant value saturates at the same score)

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 5.0 | +100 | 8 | 1 | 7 | 0 | 0 | 100% |
| coercive_credit_collection | — | — | 1 | 0 | 1 | 0 | 0 | 0% |
| delinquent_payment | — | — | 3 | 0 | 3 | 0 | 0 | 0% |
| timely_payment | — | — | 1 | 0 | 1 | 0 | 0 | 0% |
| judicial_appeal_judge | — | — | 1 | 0 | 1 | 0 | 0 | 0% |
| administrative_appeal_prefecture | 5.0 | +100 | 1 | 1 | 0 | 0 | 0 | 100% |

## Time to appeal filing, Judge (days) (id 175)

- Value set: worst 60.0, threshold 30.0, target 30.0 days
- Provenance: `statutory` — threshold 30 d: Art. 204-bis D.Lgs. 285/1992, the window for a ricorso al Giudice di Pace -- half the Prefecture window, which v1.1 collapsed into a single 60-day indicator taken from Mannhardt et al. (2016, Fig. 8)'s Delay Judge' guard rather than from the statute. worst 60 d illustrative (2x).
- **one-sided scale** (`target == threshold`: an admissibility boundary, not a gradient — every compliant value saturates at the same score)

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 81.0 | -100 | 8 | 1 | 7 | 0 | 0 | 100% |
| coercive_credit_collection | — | — | 1 | 0 | 1 | 0 | 0 | 0% |
| delinquent_payment | — | — | 3 | 0 | 3 | 0 | 0 | 0% |
| timely_payment | — | — | 1 | 0 | 1 | 0 | 0 | 0% |
| judicial_appeal_judge | 81.0 | -100 | 1 | 1 | 0 | 0 | 0 | 100% |
| administrative_appeal_prefecture | — | — | 1 | 0 | 1 | 0 | 0 | 0% |

## Average time to case closure (days) (id 114)

- Value set: worst 365.0, threshold 180.0, target 150.0 days
- Provenance: `external-by-analogy` — threshold 180 d: L. 241/1990 art. 2, which caps any administrative proceeding's term at 180 days. target 150 d: Art. 201's 90-day notification term plus Art. 203's 60-day payment/appeal window, i.e. the earliest lawful completion of an uncontested case. worst 365 d illustrative. Replaces v1.1's acknowledged invented placeholder.

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 339.0 | -85 | 8 | 6 | 0 | 0 | 2 | 75% |
| coercive_credit_collection | 971.0 | -100 | 1 | 1 | 0 | 0 | 0 | 100% |
| delinquent_payment | 328.0 | -79 | 3 | 3 | 0 | 0 | 0 | 100% |
| timely_payment | 1.0 | +100 | 1 | 1 | 0 | 0 | 0 | 100% |
| judicial_appeal_judge | — | — | 1 | 0 | 0 | 0 | 1 | 0% |
| administrative_appeal_prefecture | 78.0 | +100 | 1 | 1 | 0 | 0 | 0 | 100% |

## Propagated softgoal satisfaction

Propagated from the measured indicators through the same decomposition and contribution graph Step 5a used as the taxonomy axis (`min` over And, `max` over Or/Xor, weighted-clamped sum over contributions).

Only softgoals carry a value: indicators are the sole seeds, and they reach the model through contribution links, so every goal and task in the decomposition tree evaluates to the default 0. Seeding a category's `anchor_ids` with full satisfaction would light the tree up, but it would also assert that a category existing *is* its goal being met — the confound this measure is supposed to expose, not commit.

| Softgoal | whole log | administrative_appeal_prefecture | coercive_credit_collection | delinquent_payment | judicial_appeal_judge | timely_payment |
|---|---|---|---|---|---|---|
| Maximize timely fine revenue | -44 | +100 | -58 | -46 | +36 | +50 |
| Minimize administrative & enforcement cost | -42 | +50 | -50 | -40 | +0 | +50 |
| Preserve offender's due-process rights | +0 | +50 | +0 | +0 | -50 | +0 |


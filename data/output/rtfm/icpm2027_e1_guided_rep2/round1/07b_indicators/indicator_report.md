# Step 7b — indicator satisfaction

Goal model: `rtfm_goal_model.jucm`

Satisfaction is on GRL's [-100, +100] scale, converted from the measured value by each indicator's own `KPIEvalValueSet`. The measured value is reported beside it in every row: a score against an illustrative threshold reads exactly like one against a statute, and only the provenance column separates them.

## Time to fine dispatch (days) (id 112)

- Value set: worst 360.0, threshold 90.0, target 30.0 days
- Provenance: `statutory` — threshold 90 d and worst 360 d: Art. 201 D.Lgs. 285/1992 (ordinary notification term; extended term for parties resident abroad). target 30 d: L. 241/1990 art. 2 c.2, the default term for concluding an administrative proceeding, applied by analogy as an operational aspiration -- the specific term in Art. 201 is what binds.

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 87.5 | +4 | 150370 | 103987 | 0 | 0 | 46383 | 69% |
| coercive_credit_collection | 84.1 | +9 | 59012 | 59012 | 0 | 0 | 0 | 100% |
| timely_payment | 66.8 | +38 | 49617 | 3234 | 0 | 0 | 46383 | 7% |
| delinquent_payment | 91.5 | +0 | 16889 | 16889 | 0 | 0 | 0 | 100% |
| administrative_appeal | 90.6 | +0 | 3596 | 3596 | 0 | 0 | 0 | 100% |
| judicial_appeal | 99.8 | -3 | 404 | 404 | 0 | 0 | 0 | 100% |

## Time to appeal filing, Prefecture (days) (id 113)

- Value set: worst 120.0, threshold 60.0, target 60.0 days
- Provenance: `statutory` — threshold 60 d: Art. 203 D.Lgs. 285/1992, the window for a ricorso al Prefetto; corroborated by the Delay Prefecture' < 60 days guard in Mannhardt et al. (2016, Fig. 8). target == threshold because an admissibility window is a boundary, not a gradient. worst 120 d illustrative (2x the window).
- **one-sided scale** (`target == threshold`: an admissibility boundary, not a gradient — every compliant value saturates at the same score)

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 48.6 | +100 | 150370 | 4036 | 146182 | 145 | 7 | 96% |
| coercive_credit_collection | 41.9 | +100 | 59012 | 281 | 58731 | 0 | 0 | 100% |
| timely_payment | — | — | 49617 | 0 | 49617 | 0 | 0 | 0% |
| delinquent_payment | 31.7 | +100 | 16889 | 36 | 16847 | 0 | 6 | 86% |
| administrative_appeal | 50.2 | +100 | 3596 | 3452 | 2 | 142 | 0 | 96% |
| judicial_appeal | 35.5 | +100 | 404 | 163 | 237 | 3 | 1 | 98% |

## Time to appeal filing, Judge (days) (id 175)

- Value set: worst 60.0, threshold 30.0, target 30.0 days
- Provenance: `statutory` — threshold 30 d: Art. 204-bis D.Lgs. 285/1992, the window for a ricorso al Giudice di Pace -- half the Prefecture window, which v1.1 collapsed into a single 60-day indicator taken from Mannhardt et al. (2016, Fig. 8)'s Delay Judge' guard rather than from the statute. worst 60 d illustrative (2x).
- **one-sided scale** (`target == threshold`: an admissibility boundary, not a gradient — every compliant value saturates at the same score)

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 95.9 | -100 | 150370 | 538 | 149815 | 17 | 0 | 97% |
| coercive_credit_collection | 60.6 | -100 | 59012 | 147 | 58865 | 0 | 0 | 100% |
| timely_payment | — | — | 49617 | 0 | 49617 | 0 | 0 | 0% |
| delinquent_payment | — | — | 16889 | 0 | 16889 | 0 | 0 | 0% |
| administrative_appeal | 268.0 | -100 | 3596 | 1 | 3592 | 3 | 0 | 25% |
| judicial_appeal | 108.7 | -100 | 404 | 390 | 0 | 14 | 0 | 97% |

## Average time to case closure (days) (id 114)

- Value set: worst 365.0, threshold 180.0, target 150.0 days
- Provenance: `external-by-analogy` — threshold 180 d: L. 241/1990 art. 2, which caps any administrative proceeding's term at 180 days. target 150 d: Art. 201's 90-day notification term plus Art. 203's 60-day payment/appeal window, i.e. the earliest lawful completion of an uncontested case. worst 365 d illustrative. Replaces v1.1's acknowledged invented placeholder.

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 378.7 | -100 | 150370 | 126840 | 0 | 0 | 23530 | 84% |
| coercive_credit_collection | 690.5 | -100 | 59012 | 59012 | 0 | 0 | 0 | 100% |
| timely_payment | 17.4 | +100 | 49617 | 49617 | 0 | 0 | 0 | 100% |
| delinquent_payment | 356.7 | -95 | 16889 | 16889 | 0 | 0 | 0 | 100% |
| administrative_appeal | 339.2 | -86 | 3596 | 502 | 0 | 0 | 3094 | 14% |
| judicial_appeal | 560.7 | -100 | 404 | 353 | 0 | 0 | 51 | 87% |

## Propagated softgoal satisfaction

Propagated from the measured indicators through the same decomposition and contribution graph Step 5a used as the taxonomy axis (`min` over And, `max` over Or/Xor, weighted-clamped sum over contributions).

Only softgoals carry a value: indicators are the sole seeds, and they reach the model through contribution links, so every goal and task in the decomposition tree evaluates to the default 0. Seeding a category's `anchor_ids` with full satisfaction would light the tree up, but it would also assert that a category existing *is* its goal being met — the confound this measure is supposed to expose, not commit.

| Softgoal | whole log | administrative_appeal | coercive_credit_collection | delinquent_payment | judicial_appeal | timely_payment |
|---|---|---|---|---|---|---|
| Maximize timely fine revenue | -48 | -43 | -46 | -48 | -52 | +69 |
| Minimize administrative & enforcement cost | -50 | -43 | -50 | -48 | -50 | +50 |
| Preserve offender's due-process rights | +0 | +0 | +0 | +50 | +0 | +0 |


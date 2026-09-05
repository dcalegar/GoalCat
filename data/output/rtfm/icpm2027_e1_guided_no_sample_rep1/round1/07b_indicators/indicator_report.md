# Step 7b — indicator satisfaction

Goal model: `rtfm_goal_model.jucm`

Satisfaction is on GRL's [-100, +100] scale, converted from the measured value by each indicator's own `KPIEvalValueSet`. The measured value is reported beside it in every row: a score against an illustrative threshold reads exactly like one against a statute, and only the provenance column separates them.

## Time to fine dispatch (days) (id 112)

- Value set: worst 360.0, threshold 90.0, target 30.0 days
- Provenance: `statutory` — threshold 90 d and worst 360 d: Art. 201 D.Lgs. 285/1992 (ordinary notification term; extended term for parties resident abroad). target 30 d: L. 241/1990 art. 2 c.2, the default term for concluding an administrative proceeding, applied by analogy as an operational aspiration -- the specific term in Art. 201 is what binds.

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 87.5 | +4 | 150370 | 103987 | 0 | 0 | 46383 | 69% |
| resolve_coercive_credit_collection | 84.1 | +9 | 58991 | 58991 | 0 | 0 | 0 | 100% |
| resolve_timely_payment | 67.2 | +38 | 49726 | 3343 | 0 | 0 | 46383 | 7% |
| resolve_delinquent_payment | 91.6 | +0 | 16848 | 16848 | 0 | 0 | 0 | 100% |
| resolve_administrative_appeal_prefecture | 90.1 | +0 | 3641 | 3641 | 0 | 0 | 0 | 100% |
| resolve_judicial_appeal_judge | 101.2 | -4 | 389 | 389 | 0 | 0 | 0 | 100% |

## Time to appeal filing, Prefecture (days) (id 113)

- Value set: worst 120.0, threshold 60.0, target 60.0 days
- Provenance: `statutory` — threshold 60 d: Art. 203 D.Lgs. 285/1992, the window for a ricorso al Prefetto; corroborated by the Delay Prefecture' < 60 days guard in Mannhardt et al. (2016, Fig. 8). target == threshold because an admissibility window is a boundary, not a gradient. worst 120 d illustrative (2x the window).
- **one-sided scale** (`target == threshold`: an admissibility boundary, not a gradient — every compliant value saturates at the same score)

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 48.6 | +100 | 150370 | 4036 | 146182 | 145 | 7 | 96% |
| resolve_coercive_credit_collection | 41.6 | +100 | 58991 | 276 | 58715 | 0 | 0 | 100% |
| resolve_timely_payment | 48.8 | +100 | 49726 | 17 | 49708 | 0 | 1 | 94% |
| resolve_delinquent_payment | 27.8 | +100 | 16848 | 78 | 16765 | 0 | 5 | 94% |
| resolve_administrative_appeal_prefecture | 50.0 | +100 | 3641 | 3503 | 3 | 135 | 0 | 96% |
| resolve_judicial_appeal_judge | 37.1 | +100 | 389 | 147 | 241 | 0 | 1 | 99% |

## Time to appeal filing, Judge (days) (id 175)

- Value set: worst 60.0, threshold 30.0, target 30.0 days
- Provenance: `statutory` — threshold 30 d: Art. 204-bis D.Lgs. 285/1992, the window for a ricorso al Giudice di Pace -- half the Prefecture window, which v1.1 collapsed into a single 60-day indicator taken from Mannhardt et al. (2016, Fig. 8)'s Delay Judge' guard rather than from the statute. worst 60 d illustrative (2x).
- **one-sided scale** (`target == threshold`: an admissibility boundary, not a gradient — every compliant value saturates at the same score)

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 95.9 | -100 | 150370 | 538 | 149815 | 17 | 0 | 97% |
| resolve_coercive_credit_collection | 46.6 | -55 | 58991 | 126 | 58865 | 0 | 0 | 100% |
| resolve_timely_payment | 110.0 | -100 | 49726 | 5 | 49720 | 1 | 0 | 83% |
| resolve_delinquent_payment | 69.3 | -100 | 16848 | 12 | 16836 | 0 | 0 | 100% |
| resolve_administrative_appeal_prefecture | 110.4 | -100 | 3641 | 5 | 3636 | 0 | 0 | 100% |
| resolve_judicial_appeal_judge | 112.6 | -100 | 389 | 382 | 0 | 7 | 0 | 98% |

## Average time to case closure (days) (id 114)

- Value set: worst 365.0, threshold 180.0, target 150.0 days
- Provenance: `external-by-analogy` — threshold 180 d: L. 241/1990 art. 2, which caps any administrative proceeding's term at 180 days. target 150 d: Art. 201's 90-day notification term plus Art. 203's 60-day payment/appeal window, i.e. the earliest lawful completion of an uncontested case. worst 365 d illustrative. Replaces v1.1's acknowledged invented placeholder.

| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| whole log | 378.7 | -100 | 150370 | 126840 | 0 | 0 | 23530 | 84% |
| resolve_coercive_credit_collection | 690.4 | -100 | 58991 | 58991 | 0 | 0 | 0 | 100% |
| resolve_timely_payment | 18.0 | +100 | 49726 | 49726 | 0 | 0 | 0 | 100% |
| resolve_delinquent_payment | 357.2 | -95 | 16848 | 16848 | 0 | 0 | 0 | 100% |
| resolve_administrative_appeal_prefecture | 321.8 | -76 | 3641 | 553 | 0 | 0 | 3088 | 15% |
| resolve_judicial_appeal_judge | 598.9 | -100 | 389 | 345 | 0 | 0 | 44 | 89% |

## Propagated softgoal satisfaction

Propagated from the measured indicators through the same decomposition and contribution graph Step 5a used as the taxonomy axis (`min` over And, `max` over Or/Xor, weighted-clamped sum over contributions).

Only softgoals carry a value: indicators are the sole seeds, and they reach the model through contribution links, so every goal and task in the decomposition tree evaluates to the default 0. Seeding a category's `anchor_ids` with full satisfaction would light the tree up, but it would also assert that a category existing *is* its goal being met — the confound this measure is supposed to expose, not commit.

| Softgoal | whole log | resolve_administrative_appeal_prefecture | resolve_coercive_credit_collection | resolve_delinquent_payment | resolve_judicial_appeal_judge | resolve_timely_payment |
|---|---|---|---|---|---|---|
| Maximize timely fine revenue | -48 | -38 | -46 | -48 | -52 | +69 |
| Minimize administrative & enforcement cost | -50 | -38 | -50 | -48 | -50 | +50 |
| Preserve offender's due-process rights | +0 | +0 | +22 | +0 | +0 | +0 |


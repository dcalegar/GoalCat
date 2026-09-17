# Step 7 — Per-category process discovery report

Run: `20260917_144500` | Log: `rtfm_mini` | Inductive Miner noise_threshold: `0.0`

5 categories. Residual (no discovery attempted): 1/8 variants, 1/8 cases.

## Resolved via timely payment (`timely_payment`)

The offender pays the fine directly after it is created, before any notification or penalty. The case closes at the first OR branch of 'Fine case is resolved' without entering enforcement. This alternative fully advances 'Maximize timely fine revenue' (Make +100) and helps 'Minimize administrative & enforcement cost' (+50); its performance is judged against 'Average time to case closure' (id 114).

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model: [`models/timely_payment.pnml`](models/timely_payment.pnml) (Petri net, Inductive Miner) · [`models/timely_payment.png`](models/timely_payment.png) (Directly-Follows Graph)

## Resolved via delinquent payment after enforcement (`delinquent_payment`)

The fine goes through the enforcement path (Insert Fine Notification, Add Penalty) and is then closed by the offender paying, possibly in more than one installment. This alternative helps 'Maximize timely fine revenue' (+50), while the mandatory Add Penalty step it contains slightly harms 'Preserve offender's due-process rights' (-25). Judged against 'Average time to case closure' (id 114).

**Coverage:** 3 variants, 3 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 0.952

Model: [`models/delinquent_payment.pnml`](models/delinquent_payment.pnml) (Petri net, Inductive Miner) · [`models/delinquent_payment.png`](models/delinquent_payment.png) (Directly-Follows Graph)

## Resolved via administrative appeal to the Prefecture (`administrative_appeal_prefecture`)

After notification the offender contests the fine administratively: the appeal date is inserted, the appeal is sent to the Prefecture, and the Prefecture's result is received (and notified to the offender). One of the two mutually exclusive branches of 'Contested appeal is resolved'. It helps 'Preserve offender's due-process rights' (+50) but slightly harms both 'Minimize administrative & enforcement cost' (-25) and 'Maximize timely fine revenue' (-25). Judged against 'Time to appeal filing, Prefecture' (id 113) and 'Average time to case closure' (id 114).

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model: [`models/administrative_appeal_prefecture.pnml`](models/administrative_appeal_prefecture.pnml) (Petri net, Inductive Miner) · [`models/administrative_appeal_prefecture.png`](models/administrative_appeal_prefecture.png) (Directly-Follows Graph)

## Resolved via judicial appeal to the Judge (`judicial_appeal_judge`)

After notification and penalty the offender takes the fine to a Judge. The other, mutually exclusive branch of 'Contested appeal is resolved'. It fully advances 'Preserve offender's due-process rights' (Make +100) while hurting 'Minimize administrative & enforcement cost' (-50) and slightly harming 'Maximize timely fine revenue' (-25). Judged against 'Time to appeal filing, Judge' (id 175) and 'Average time to case closure' (id 114).

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model: [`models/judicial_appeal_judge.pnml`](models/judicial_appeal_judge.pnml) (Petri net, Inductive Miner) · [`models/judicial_appeal_judge.png`](models/judicial_appeal_judge.png) (Directly-Follows Graph)

## Resolved via coercive credit collection (`coercive_credit_collection`)

The fine is notified and penalised but never paid or appealed, and the organization hands it to credit collection to enforce it. This alternative helps 'Maximize timely fine revenue' (+50) but hurts 'Minimize administrative & enforcement cost' (-50) and slightly harms 'Preserve offender's due-process rights' (-25). Judged against 'Average time to case closure' (id 114), against which it performs worst in the sample.

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model: [`models/coercive_credit_collection.pnml`](models/coercive_credit_collection.pnml) (Petri net, Inductive Miner) · [`models/coercive_credit_collection.png`](models/coercive_credit_collection.png) (Directly-Follows Graph)

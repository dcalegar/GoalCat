# Step 7 — Per-category process discovery report

Run: `20260825_215313` | Log: `rtfm_mini` | Inductive Miner noise_threshold: `0.0`

5 categories. Residual (no discovery attempted): 1/6 variants, 1/6 cases.

## Resolve via timely payment (`timely_payment`)

Resolution of the fine case through early payment before penalty or further enforcement steps. Advances Maximize timely fine revenue and Minimize administrative & enforcement cost.

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model: [`models/timely_payment.pnml`](models/timely_payment.pnml) (Petri net, Inductive Miner) · [`models/timely_payment.png`](models/timely_payment.png) (Directly-Follows Graph)

## Resolve via delinquent payment (`delinquent_payment`)

Resolution of the fine case through payment after notification and penalty have been applied. Helps Maximize timely fine revenue.

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model: [`models/delinquent_payment.pnml`](models/delinquent_payment.pnml) (Petri net, Inductive Miner) · [`models/delinquent_payment.png`](models/delinquent_payment.png) (Directly-Follows Graph)

## Resolve via administrative appeal to the Prefecture (`administrative_appeal_to_prefecture`)

Contested appeal resolved through administrative process via the Prefecture. Preserves offender's due-process rights while impacting costs and revenue.

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model: [`models/administrative_appeal_to_prefecture.pnml`](models/administrative_appeal_to_prefecture.pnml) (Petri net, Inductive Miner) · [`models/administrative_appeal_to_prefecture.png`](models/administrative_appeal_to_prefecture.png) (Directly-Follows Graph)

## Resolve via judicial appeal to the Judge (`judicial_appeal_to_the_judge`)

Contested appeal resolved through the judicial system. Makes a strong positive contribution to preserving offender's due-process rights while hurting administrative costs.

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model: [`models/judicial_appeal_to_the_judge.pnml`](models/judicial_appeal_to_the_judge.pnml) (Petri net, Inductive Miner) · [`models/judicial_appeal_to_the_judge.png`](models/judicial_appeal_to_the_judge.png) (Directly-Follows Graph)

## Resolve via coercive credit collection (`coercive_credit_collection`)

Resolution of the fine case through coercive credit collection procedures after notifications and penalties. Helps timely revenue while hurting enforcement costs.

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model: [`models/coercive_credit_collection.pnml`](models/coercive_credit_collection.pnml) (Petri net, Inductive Miner) · [`models/coercive_credit_collection.png`](models/coercive_credit_collection.png) (Directly-Follows Graph)

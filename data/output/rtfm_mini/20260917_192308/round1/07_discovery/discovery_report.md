# Step 7 — Per-category process discovery report

Run: `20260917_192308` | Log: `rtfm_mini` | Inductive Miner noise_threshold: `0.0`

5 categories. Residual (no discovery attempted): 1/8 variants, 1/8 cases.

## Resolve via timely payment (`timely_payment`)

Resolution of the fine through timely payment, advancing Maximize timely fine revenue and minimizing administrative and enforcement costs.

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model: [`models/timely_payment.pnml`](models/timely_payment.pnml) (Petri net, Inductive Miner) · [`models/timely_payment.png`](models/timely_payment.png) (Directly-Follows Graph)

## Resolve via delinquent payment (`delinquent_payment`)

Resolution of the case through payment after notification and penalty have been applied, contributing to timely fine revenue.

**Coverage:** 3 variants, 3 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 0.952

Model: [`models/delinquent_payment.pnml`](models/delinquent_payment.pnml) (Petri net, Inductive Miner) · [`models/delinquent_payment.png`](models/delinquent_payment.png) (Directly-Follows Graph)

## Resolve via administrative appeal to the Prefecture (`administrative_appeal_prefecture`)

Resolution via an administrative appeal process directed to the Prefecture, preserving due-process rights.

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model: [`models/administrative_appeal_prefecture.pnml`](models/administrative_appeal_prefecture.pnml) (Petri net, Inductive Miner) · [`models/administrative_appeal_prefecture.png`](models/administrative_appeal_prefecture.png) (Directly-Follows Graph)

## Resolve via judicial appeal to the Judge (`judicial_appeal_judge`)

Resolution through a judicial appeal brought before a judge, strongly making offender's due-process rights.

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model: [`models/judicial_appeal_judge.pnml`](models/judicial_appeal_judge.pnml) (Petri net, Inductive Miner) · [`models/judicial_appeal_judge.png`](models/judicial_appeal_judge.png) (Directly-Follows Graph)

## Resolve via coercive credit collection (`coercive_credit_collection`)

Resolution of the fine via coercive credit collection procedures, helping fine revenue while hurting administrative costs.

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model: [`models/coercive_credit_collection.pnml`](models/coercive_credit_collection.pnml) (Petri net, Inductive Miner) · [`models/coercive_credit_collection.png`](models/coercive_credit_collection.png) (Directly-Follows Graph)

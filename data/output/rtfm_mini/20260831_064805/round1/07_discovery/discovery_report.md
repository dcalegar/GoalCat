# Step 7 — Per-category process discovery report

Run: `20260831_064805` | Log: `rtfm_mini` | Inductive Miner noise_threshold: `0.0`

5 categories. Residual (no discovery attempted): 1/8 variants, 1/8 cases.

## Resolve via timely payment (`resolve_via_timely_payment`)

Represents the resolution of a fine via timely payment, advancing Maximize timely fine revenue and minimizing administrative and enforcement costs, evaluated against Average time to case closure.

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model: [`models/resolve_via_timely_payment.pnml`](models/resolve_via_timely_payment.pnml) (Petri net, Inductive Miner) · [`models/resolve_via_timely_payment.png`](models/resolve_via_timely_payment.png) (Directly-Follows Graph)

## Resolve via delinquent payment (`resolve_via_delinquent_payment`)

Represents the resolution of an enforceable fine via delinquent payment after notification and penalty addition, contributing to timely fine revenue.

**Coverage:** 3 variants, 3 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 0.952

Model: [`models/resolve_via_delinquent_payment.pnml`](models/resolve_via_delinquent_payment.pnml) (Petri net, Inductive Miner) · [`models/resolve_via_delinquent_payment.png`](models/resolve_via_delinquent_payment.png) (Directly-Follows Graph)

## Resolve via administrative appeal to the Prefecture (`resolve_via_administrative_appeal_to_the_prefecture`)

Represents handling the case through an administrative appeal to the Prefecture, preserving due-process rights while impacting administrative costs and revenue.

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model: [`models/resolve_via_administrative_appeal_to_the_prefecture.pnml`](models/resolve_via_administrative_appeal_to_the_prefecture.pnml) (Petri net, Inductive Miner) · [`models/resolve_via_administrative_appeal_to_the_prefecture.png`](models/resolve_via_administrative_appeal_to_the_prefecture.png) (Directly-Follows Graph)

## Resolve via judicial appeal to the Judge (`resolve_via_judicial_appeal_to_the_judge`)

Represents contesting the fine via a judicial appeal to the Judge, strongly supporting due-process rights but hurting administrative cost efficiency.

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model: [`models/resolve_via_judicial_appeal_to_the_judge.pnml`](models/resolve_via_judicial_appeal_to_the_judge.pnml) (Petri net, Inductive Miner) · [`models/resolve_via_judicial_appeal_to_the_judge.png`](models/resolve_via_judicial_appeal_to_the_judge.png) (Directly-Follows Graph)

## Resolve via coercive credit collection (`resolve_via_coercive_credit_collection`)

Represents resolving an enforceable fine through coercive credit collection, helping revenue but hurting administrative costs.

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model: [`models/resolve_via_coercive_credit_collection.pnml`](models/resolve_via_coercive_credit_collection.pnml) (Petri net, Inductive Miner) · [`models/resolve_via_coercive_credit_collection.png`](models/resolve_via_coercive_credit_collection.png) (Directly-Follows Graph)

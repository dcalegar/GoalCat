# Step 7 — Per-category process discovery report

Run: `20260828_171553` | Log: `rtfm_mini` | Inductive Miner noise_threshold: `0.0`

5 categories. Residual (no discovery attempted): 1/6 variants, 1/6 cases.

## Resolve via timely payment (`timely_payment`)

Resolution of the fine case through early payment by the offender, advancing the softgoal 'Maximize timely fine revenue' and helping 'Minimize administrative & enforcement cost', evaluated against indicator 'Average time to case closure'.

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model: [`models/timely_payment.pnml`](models/timely_payment.pnml) (Petri net, Inductive Miner) · [`models/timely_payment.png`](models/timely_payment.png) (Directly-Follows Graph)

## Resolve via delinquent payment (`delinquent_payment`)

Resolution of the fine case through payment after notifications and penalties have been added, helping 'Maximize timely fine revenue' and evaluated against 'Average time to case closure'.

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model: [`models/delinquent_payment.pnml`](models/delinquent_payment.pnml) (Petri net, Inductive Miner) · [`models/delinquent_payment.png`](models/delinquent_payment.png) (Directly-Follows Graph)

## Resolve via administrative appeal to the Prefecture (`administrative_appeal_prefecture`)

Resolution via an administrative appeal submitted to the Prefecture, preserving due-process rights while impacting administrative cost and fine revenue, measured against 'Time to appeal filing, Prefecture'.

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model: [`models/administrative_appeal_prefecture.pnml`](models/administrative_appeal_prefecture.pnml) (Petri net, Inductive Miner) · [`models/administrative_appeal_prefecture.png`](models/administrative_appeal_prefecture.png) (Directly-Follows Graph)

## Resolve via judicial appeal to the Judge (`judicial_appeal_judge`)

Resolution via a judicial appeal brought before a judge, strongly preserving offender due-process rights while hurting administrative cost, measured against 'Time to appeal filing, Judge'.

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model: [`models/judicial_appeal_judge.pnml`](models/judicial_appeal_judge.pnml) (Petri net, Inductive Miner) · [`models/judicial_appeal_judge.png`](models/judicial_appeal_judge.png) (Directly-Follows Graph)

## Resolve via coercive credit collection (`coercive_credit_collection`)

Resolution of the fine case through coercive credit collection steps after penalties are added, helping fine revenue and hurting administrative costs.

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model: [`models/coercive_credit_collection.pnml`](models/coercive_credit_collection.pnml) (Petri net, Inductive Miner) · [`models/coercive_credit_collection.png`](models/coercive_credit_collection.png) (Directly-Follows Graph)

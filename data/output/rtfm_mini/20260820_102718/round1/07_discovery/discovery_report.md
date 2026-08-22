# Step 7 — Per-category process discovery report

Run: `20260820_102718` | Log: `rtfm_mini` | Inductive Miner noise_threshold: `0.0`

5 categories. Residual (no discovery attempted): 1/6 variants, 1/6 cases.

## Resolve via timely payment (`timely_payment`)

Resolution of the fine via timely payment directly after issuance.

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model: [`models/timely_payment.pnml`](models/timely_payment.pnml) (Petri net, Inductive Miner) · [`models/timely_payment.png`](models/timely_payment.png) (Directly-Follows Graph)

## Resolve via delinquent payment (`delinquent_payment`)

Resolution of the fine via payment after notification and added penalty.

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model: [`models/delinquent_payment.pnml`](models/delinquent_payment.pnml) (Petri net, Inductive Miner) · [`models/delinquent_payment.png`](models/delinquent_payment.png) (Directly-Follows Graph)

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Resolution through administrative appeal steps involving the Prefecture.

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model: [`models/administrative_appeal.pnml`](models/administrative_appeal.pnml) (Petri net, Inductive Miner) · [`models/administrative_appeal.png`](models/administrative_appeal.png) (Directly-Follows Graph)

## Resolve via judicial appeal to the Judge (`judicial_appeal`)

Resolution via an appeal brought before a judge.

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model: [`models/judicial_appeal.pnml`](models/judicial_appeal.pnml) (Petri net, Inductive Miner) · [`models/judicial_appeal.png`](models/judicial_appeal.png) (Directly-Follows Graph)

## Resolve via coercive credit collection (`coercive_credit_collection`)

Resolution through coercive credit collection measures after penalties are applied.

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model: [`models/coercive_credit_collection.pnml`](models/coercive_credit_collection.pnml) (Petri net, Inductive Miner) · [`models/coercive_credit_collection.png`](models/coercive_credit_collection.png) (Directly-Follows Graph)

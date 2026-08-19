# Step 7 — Per-category process discovery report

Run: `20260818_203957` | Log: `rtfm_mini` | Inductive Miner noise_threshold: `0.0`

5 categories. Residual (no discovery attempted): 1/6 variants, 1/6 cases.

## Resolve via timely payment (`timely_payment`)

Fine is settled promptly by the offender without requiring enforcement steps like notification or added penalties.

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model: [`models/timely_payment.pnml`](models/timely_payment.pnml) (Petri net, Inductive Miner) · [`models/timely_payment.png`](models/timely_payment.png) (Directly-Follows Graph)

## Resolve via delinquent payment (`delinquent_payment`)

Fine is settled after formal notification and penalty addition have occurred in the enforced branch.

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model: [`models/delinquent_payment.pnml`](models/delinquent_payment.pnml) (Petri net, Inductive Miner) · [`models/delinquent_payment.png`](models/delinquent_payment.png) (Directly-Follows Graph)

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Case involves an administrative appeal process directed to the Prefecture following fine enforcement.

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model: [`models/administrative_appeal.pnml`](models/administrative_appeal.pnml) (Petri net, Inductive Miner) · [`models/administrative_appeal.png`](models/administrative_appeal.png) (Directly-Follows Graph)

## Resolve via judicial appeal to the Judge (`judicial_appeal`)

Case involves an appeal brought before a judicial judge after standard enforcement steps.

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model: [`models/judicial_appeal.pnml`](models/judicial_appeal.pnml) (Petri net, Inductive Miner) · [`models/judicial_appeal.png`](models/judicial_appeal.png) (Directly-Follows Graph)

## Resolve via coercive credit collection (`coercive_collection`)

Unresolved enforced fine is forwarded to a credit collection agent for coercive recovery.

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model: [`models/coercive_collection.pnml`](models/coercive_collection.pnml) (Petri net, Inductive Miner) · [`models/coercive_collection.png`](models/coercive_collection.png) (Directly-Follows Graph)

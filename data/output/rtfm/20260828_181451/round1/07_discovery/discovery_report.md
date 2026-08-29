# Step 7 — Per-category process discovery report

Run: `20260828_181451` | Log: `rtfm` | Inductive Miner noise_threshold: `0.0`

5 categories. Residual (no discovery attempted): 10/231 variants, 20859/150370 cases.

## Resolve via timely payment (`resolve_timely_payment`)

Fines resolved through prompt payment, maximizing timely fine revenue and helping minimize administrative and enforcement cost, judged against average time to case closure.

**Coverage:** 34 variants, 49658 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 0.904

Model files were removed after this run was accepted (kept out of the final deliverable to save disk space) — re-run Step 7 against this round's `assignments.csv`/`taxonomy.json` to regenerate them if needed.

## Resolve via delinquent payment (`resolve_delinquent_payment`)

Enforced cases resolved through delayed payment after notification and penalty additions, helping maximize timely fine revenue, judged against average time to case closure.

**Coverage:** 33 variants, 16875 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 0.379

Model files were removed after this run was accepted (kept out of the final deliverable to save disk space) — re-run Step 7 against this round's `assignments.csv`/`taxonomy.json` to regenerate them if needed.

## Resolve via administrative appeal to the Prefecture (`resolve_administrative_appeal`)

Contested cases resolved through the administrative appeal process involving the Prefecture, preserving due-process rights while potentially increasing costs and delaying revenue, judged against time to appeal filing, Prefecture.

**Coverage:** 64 variants, 3602 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 0.539

Model files were removed after this run was accepted (kept out of the final deliverable to save disk space) — re-run Step 7 against this round's `assignments.csv`/`taxonomy.json` to regenerate them if needed.

## Resolve via judicial appeal to the Judge (`resolve_judicial_appeal`)

Contested cases resolved via judicial appeal to a judge, strongly making offender due-process rights while hurting administrative costs, judged against time to appeal filing, Judge.

**Coverage:** 50 variants, 380 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 0.561

Model files were removed after this run was accepted (kept out of the final deliverable to save disk space) — re-run Step 7 against this round's `assignments.csv`/`taxonomy.json` to regenerate them if needed.

## Resolve via coercive credit collection (`resolve_coercive_credit_collection`)

Cases resolved via coercive credit collection actions after enforcement steps, helping revenue but hurting administrative costs, judged against average time to case closure.

**Coverage:** 40 variants, 58996 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 0.531

Model files were removed after this run was accepted (kept out of the final deliverable to save disk space) — re-run Step 7 against this round's `assignments.csv`/`taxonomy.json` to regenerate them if needed.

# Step 7 — Per-category process discovery report

Run: `20260917_152158` | Log: `rtfm` | Inductive Miner noise_threshold: `0.0`

5 categories. Residual (no discovery attempted): 1/231 variants, 20385/150370 cases.

## Resolved via timely payment (`timely_payment`)

The offender pays the fine before enforcement begins, that is before any Insert Fine Notification or Add Penalty, typically within days of creation and sometimes before or shortly after the fine is dispatched. The case closes at the first OR branch of 'Fine case is resolved' without entering the enforceable path. This alternative fully advances 'Maximize timely fine revenue' (Make +100) and helps 'Minimize administrative & enforcement cost' (+50); its performance is judged against 'Average time to case closure' (id 114).

**Coverage:** 7 variants, 49969 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model files were removed after this run was accepted (kept out of the final deliverable to save disk space) — re-run Step 7 against this round's `assignments.csv`/`taxonomy.json` to regenerate them if needed.

## Resolved via delinquent payment after enforcement (`delinquent_payment`)

The fine enters enforcement (Insert Fine Notification, Add Penalty) and is then closed by the offender paying, often late and often in several installments, without any appeal. This alternative helps 'Maximize timely fine revenue' (+50), while the mandatory Add Penalty step slightly harms 'Preserve offender's due-process rights' (-25). Judged against 'Average time to case closure' (id 114).

**Coverage:** 21 variants, 16851 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 0.741

Model files were removed after this run was accepted (kept out of the final deliverable to save disk space) — re-run Step 7 against this round's `assignments.csv`/`taxonomy.json` to regenerate them if needed.

## Resolved via administrative appeal to the Prefecture (`administrative_appeal_prefecture`)

The offender contests the fine administratively: the appeal date is inserted, the appeal is sent to the Prefecture, and the Prefecture's result is received and notified to the offender. One of the two mutually exclusive branches of 'Contested appeal is resolved'. It helps 'Preserve offender's due-process rights' (+50) but slightly harms both 'Minimize administrative & enforcement cost' (-25) and 'Maximize timely fine revenue' (-25). Judged against 'Time to appeal filing, Prefecture' (id 113) and 'Average time to case closure' (id 114).

**Coverage:** 129 variants, 4042 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 0.551

Model files were removed after this run was accepted (kept out of the final deliverable to save disk space) — re-run Step 7 against this round's `assignments.csv`/`taxonomy.json` to regenerate them if needed.

## Resolved via judicial appeal to the Judge (`judicial_appeal_judge`)

The offender takes the fine to a Judge, logged as Appeal to Judge, usually shortly after notification and before or around the penalty. The other, mutually exclusive branch of 'Contested appeal is resolved'. It fully advances 'Preserve offender's due-process rights' (Make +100) while hurting 'Minimize administrative & enforcement cost' (-50) and slightly harming 'Maximize timely fine revenue' (-25). Judged against 'Time to appeal filing, Judge' (id 175) and 'Average time to case closure' (id 114).

**Coverage:** 60 variants, 525 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 0.542

Model files were removed after this run was accepted (kept out of the final deliverable to save disk space) — re-run Step 7 against this round's `assignments.csv`/`taxonomy.json` to regenerate them if needed.

## Resolved via coercive credit collection (`coercive_credit_collection`)

The fine is notified and penalised and, with no payment in full and no successful appeal, the organization hands it to credit collection to enforce it, typically more than a year after the penalty. This alternative helps 'Maximize timely fine revenue' (+50) but hurts 'Minimize administrative & enforcement cost' (-50) and slightly harms 'Preserve offender's due-process rights' (-25). Judged against 'Average time to case closure' (id 114).

**Coverage:** 13 variants, 58598 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model files were removed after this run was accepted (kept out of the final deliverable to save disk space) — re-run Step 7 against this round's `assignments.csv`/`taxonomy.json` to regenerate them if needed.

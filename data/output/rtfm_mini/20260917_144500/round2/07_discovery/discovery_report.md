# Step 7 — Per-category process discovery report

Run: `20260917_144500` | Log: `rtfm_mini` | Inductive Miner noise_threshold: `0.0`

4 categories. Residual (no discovery attempted): 1/8 variants, 1/8 cases.

## Resolved via timely payment (`timely_payment`)

The offender pays the fine directly after it is created, before any notification or penalty. The case closes at the first OR branch of 'Fine case is resolved' without entering enforcement. This alternative fully advances 'Maximize timely fine revenue' (Make +100) and helps 'Minimize administrative & enforcement cost' (+50); its performance is judged against 'Average time to case closure' (id 114).

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model files were removed after this run was accepted (kept out of the final deliverable to save disk space) — re-run Step 7 against this round's `assignments.csv`/`taxonomy.json` to regenerate them if needed.

## Enforced case closed without appeal (delinquent payment or credit collection) (`uncontested_enforcement_closure`)

The fine goes through the enforcement path (Insert Fine Notification, Add Penalty) and is then closed without any appeal, either by the offender eventually paying, possibly in more than one installment, or by the organization handing the unpaid fine to coercive credit collection. Both routes help 'Maximize timely fine revenue' (+50); credit collection additionally hurts 'Minimize administrative & enforcement cost' (-50) and slightly harms 'Preserve offender's due-process rights' (-25), as does the mandatory Add Penalty step on either route (-25). Judged against 'Average time to case closure' (id 114).

**Coverage:** 4 variants, 4 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 0.906

Model files were removed after this run was accepted (kept out of the final deliverable to save disk space) — re-run Step 7 against this round's `assignments.csv`/`taxonomy.json` to regenerate them if needed.

## Resolved via administrative appeal to the Prefecture (`administrative_appeal_prefecture`)

After notification the offender contests the fine administratively: the appeal date is inserted, the appeal is sent to the Prefecture, and the Prefecture's result is received (and notified to the offender). One of the two mutually exclusive branches of 'Contested appeal is resolved'. It helps 'Preserve offender's due-process rights' (+50) but slightly harms both 'Minimize administrative & enforcement cost' (-25) and 'Maximize timely fine revenue' (-25). Judged against 'Time to appeal filing, Prefecture' (id 113) and 'Average time to case closure' (id 114).

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model files were removed after this run was accepted (kept out of the final deliverable to save disk space) — re-run Step 7 against this round's `assignments.csv`/`taxonomy.json` to regenerate them if needed.

## Resolved via judicial appeal to the Judge (`judicial_appeal_judge`)

After notification and penalty the offender takes the fine to a Judge. The other, mutually exclusive branch of 'Contested appeal is resolved'. It fully advances 'Preserve offender's due-process rights' (Make +100) while hurting 'Minimize administrative & enforcement cost' (-50) and slightly harming 'Maximize timely fine revenue' (-25). Judged against 'Time to appeal filing, Judge' (id 175) and 'Average time to case closure' (id 114).

**Coverage:** 1 variants, 1 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 1.000

Model files were removed after this run was accepted (kept out of the final deliverable to save disk space) — re-run Step 7 against this round's `assignments.csv`/`taxonomy.json` to regenerate them if needed.

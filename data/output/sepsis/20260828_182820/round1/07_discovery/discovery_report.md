# Step 7 — Per-category process discovery report

Run: `20260828_182820` | Log: `sepsis` | Inductive Miner noise_threshold: `0.0`

7 categories. Residual (no discovery attempted): 158/846 variants, 310/1050 cases.

## Admission to Normal Care (`admission_nc`)

Patient is admitted to a normal care inpatient ward (Admission NC), advancing treatment goals but subject to normal ward management and discharge pathways.

**Coverage:** 85 variants, 98 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 0.343

Model files were removed after this run was accepted (kept out of the final deliverable to save disk space) — re-run Step 7 against this round's `assignments.csv`/`taxonomy.json` to regenerate them if needed.

## Admission to Intensive Care (`admission_ic`)

Patient is admitted to an intensive care inpatient ward (Admission IC). This option incurs some negative impact on minimizing time-to-treatment due to transfer overhead, but is required for critical stabilization.

**Coverage:** 11 variants, 11 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 0.171

Model files were removed after this run was accepted (kept out of the final deliverable to save disk space) — re-run Step 7 against this round's `assignments.csv`/`taxonomy.json` to regenerate them if needed.

## Release Pathway A (`release_a`)

Captured discharge representing standard release pathway A, helping to avoid post-discharge deterioration.

**Coverage:** 487 variants, 525 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 0.300

Model files were removed after this run was accepted (kept out of the final deliverable to save disk space) — re-run Step 7 against this round's `assignments.csv`/`taxonomy.json` to regenerate them if needed.

## Release Pathway B (`release_b`)

Captured discharge representing release pathway B, helping to avoid post-discharge deterioration.

**Coverage:** 53 variants, 54 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 0.283

Model files were removed after this run was accepted (kept out of the final deliverable to save disk space) — re-run Step 7 against this round's `assignments.csv`/`taxonomy.json` to regenerate them if needed.

## Release Pathway C (`release_c`)

Captured discharge representing release pathway C for specific patient recovery profiles.

**Coverage:** 23 variants, 23 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 0.245

Model files were removed after this run was accepted (kept out of the final deliverable to save disk space) — re-run Step 7 against this round's `assignments.csv`/`taxonomy.json` to regenerate them if needed.

## Release Pathway D (`release_d`)

Captured discharge representing release pathway D.

**Coverage:** 23 variants, 23 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 0.239

Model files were removed after this run was accepted (kept out of the final deliverable to save disk space) — re-run Step 7 against this round's `assignments.csv`/`taxonomy.json` to regenerate them if needed.

## Release Pathway E (`release_e`)

Captured discharge representing release pathway E.

**Coverage:** 6 variants, 6 cases.

**Conformance (token-based replay):** log fitness 1.000, average trace fitness 1.000, 100.0% fit traces, precision 0.201

Model files were removed after this run was accepted (kept out of the final deliverable to save disk space) — re-run Step 7 against this round's `assignments.csv`/`taxonomy.json` to regenerate them if needed.

# `experimentation.icpm2027`

Replication package for the ICPM 2027 submission (*Goal-driven variant categorization*): every
run behind the paper's reported results lives here, under a frozen, versioned experimental
protocol — not in `experimentation/examples/`, which holds illustrative per-log demos with no
experimental-freeze guarantees.

**Status: scaffold.** Populated as the protocol is finalized. Expected shape, one subdirectory
per dataset in the paired within-log design, mirroring `experimentation/examples/`'s
one-directory-per-log convention:

```
icpm2027/
├── rtfm/          # paired guided/open runs + goal-model perturbations
├── sepsis/        # paired guided/open runs
├── bpic2019/      # paired guided/open runs
└── analysis/       # cross-dataset analysis: contingency matrices, coverage comparison
```

Each dataset subdirectory should keep its own frozen config(s) and driver script(s), and record
provenance for anything the protocol requires to be auditable (goal-model version, prompt/model
versions, freeze timestamps).

BPIC 2020 Travel Permit is out of scope for the main evaluation and is not expected to gain a
subdirectory here unless that changes.

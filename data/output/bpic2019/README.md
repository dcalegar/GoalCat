# `data/output/bpic2019/` — tracked contents and omissions

These are the ICPM 2027 replication runs for BPIC 2019. Two classes of file are
withheld from version control because the full run directory is ~5 GB; both are
recoverable without re-executing the LLM-backed steps.

## Compressed files — decompress before use

`profiles.json` (Step 2) and `lupin_input.json` (Step 3) are committed only in
gzipped form. The raw files are listed in the repository `.gitignore`.

| Tracked file | Raw file | Raw size | Present in |
|---|---|---|---|
| `*/02_profiling/profiles.json.gz` | `profiles.json` | ~79 MB | every run |
| `*/03_textualization/lupin_input.json.gz` | `lupin_input.json` | ~54 MB | `icpm2027_base`, `20260829_080358` |

Restore them in place before the pipeline or the analysis scripts read a run
directory:

```bash
find data/output/bpic2019 \( -name 'profiles.json.gz' -o -name 'lupin_input.json.gz' \) \
  -exec gunzip -k {} +
```

`gunzip -k` keeps the `.gz` alongside the restored file, so the working tree
still matches what is tracked.

## Cached derived files — committed directly

| Tracked file | Produced by | Purpose |
|---|---|---|
| `heldout_case_Item_Category.parquet` | `analysis/heldout.py`'s `extract_heldout_series()` | Per-case `case:Item Category` values, extracted from the full XES log. Parsing the log takes ~90s, so the result is cached here; Task C1 reads this file instead of re-parsing on every run. |

## Omitted files — not in this repository

The Step 6 pairwise distance matrices are **not committed** in any form:

| File | Size per run | Runs affected |
|---|---|---|
| `*/round1/06_assignment/profile_distances.parquet` | ~721 MB | `icpm2027_e1_guided_rep1`, `icpm2027_e1_guided_rep2`, `icpm2027_e1_open_rep1`, `20260829_080358` |
| `*/round1/06_assignment/structural_distances.parquet` | ~202 MB | same four |
| `*/round1/06_assignment/{profile,structural}_distances.csv` | — | redundant CSV twins, ignored repo-wide |

Each parquet file exceeds GitHub's 100 MB per-file limit; their size grows as
*n(n−1)/2* over the 11,973-variant scope. They are derived data. Consequences of
their absence:

- The cohesion and divergence sections of `assignment_report.md` and the
  nearest-neighbor columns of `assignments.csv` cannot be regenerated from the
  tracked files alone.
- Regenerate by re-running Step 6 for the affected run, or run with
  `skip_pairwise_distances` if the derived sections are not needed. See the root
  `README.md` "Resource usage" section.

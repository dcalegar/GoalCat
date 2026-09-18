# `data/output/bpic2019/` — tracked contents and omissions

These are the BPIC 2019 runs: the ICPM 2027 replication runs (`icpm2027_*`) and one example run
(`20260829_080358`, stopped after Step 6). The full directory is ~5 GB, so two classes of file are
withheld from version control. Both are recoverable without re-running any LLM-backed step.

## Compressed inputs — restore before use

`profiles.json` (Step 2, ~79 MB) and `lupin_input.json` (Step 3, ~54 MB) are ignored by
`.gitignore` in raw form. Some runs commit them gzipped:

| Tracked file | Present in |
|---|---|
| `*/02_profiling/profiles.json.gz` | `icpm2027_base`, `20260829_080358`, the five `c12` stability runs, `e1_guided_rep{1,2}`, `e1_open_rep{1,2}` |
| `*/03_textualization/lupin_input.json.gz` | `icpm2027_base`, `20260829_080358` |

Every `icpm2027_*` condition copies Steps 1–4 from `icpm2027_base` without recomputing them
(`inputs.py`), so each condition's `profiles.json` is byte-identical to the base's. Restore all
of them before the pipeline or an analysis script reads a run directory:

```bash
# 1. decompress every tracked copy in place (-k keeps the .gz, so the tree still matches git)
find data/output/bpic2019 \( -name 'profiles.json.gz' -o -name 'lupin_input.json.gz' \) \
  -exec gunzip -kf {} +

# 2. fill in the conditions that commit no copy, from the shared base
for d in data/output/bpic2019/icpm2027_*/02_profiling; do
  [ -f "$d/profiles.json" ] || cp data/output/bpic2019/icpm2027_base/02_profiling/profiles.json "$d/"
done
```

## Cached derived file — committed directly

| Tracked file | Produced by | Purpose |
|---|---|---|
| `heldout_case_Item_Category.parquet` | `experimentation/icpm2027/analysis/heldout.py`'s `extract_heldout_series()` | Per-case `case:Item Category` values from the full XES log. Parsing the log takes ~90 s, so Task C1 reads this cache instead. |

## Omitted files — not in this repository

Step 6's pairwise distance matrices, `*/round*/06_assignment/{structural,profile}_distances.parquet`
(~202 MB and ~721 MB per run), are **not committed** in any form: each exceeds GitHub's 100 MB
per-file limit, since their size grows as *n(n−1)/2* over the 11,973-variant scope. Their CSV twins
are ignored repository-wide. Without them:

- `assignment_report.md`'s cohesion/divergence sections and `assignments.csv`'s nearest-neighbor
  columns cannot be regenerated from the tracked files, and a Step 9 rename cannot re-render the
  reports.
- To regenerate them, re-run Step 6 for the run; `skip_pairwise_distances` avoids them when those
  sections are not needed. See the root README's
  [Resource usage](../../../README.md#resource-usage) section.

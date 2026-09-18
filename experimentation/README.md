# `experimentation`

Case-study drivers that run the `goalcat` pipeline library against real event logs. Both
subpackages import `goalcat`; `goalcat` never imports either. The package sits at the repository
root rather than under `src/` because it consumes the pipeline without being part of it.

| Subpackage | Purpose | Entry point |
|---|---|---|
| `examples/` | One runnable illustration per log (`rtfm_mini`, `rtfm`, `bpic2019`, `sepsis`): a config plus an `example_run.py`. Shows that the pipeline runs end to end and is the fastest way to exercise a change. Not evidence for any research claim. | `python -m experimentation.examples.<log>.example_run` |
| `icpm2027/` | Replication package for the ICPM 2027 submission: every run under a frozen, versioned protocol. Kept apart from `examples/` because its runs carry freeze and versioning obligations a demo does not. | `python -m experimentation.icpm2027.run_experiment` — see [`icpm2027/README.md`](icpm2027/README.md) |

Installation, LLM-backend setup, and what each example driver decides at Step 9 are in the root
[`README.md`](../README.md#running-the-pipeline).

## Resource cost before running an example

Every example makes real, billed LLM calls and writes a full run directory under `data/output/`.
The committed example runs are:

| Example | Committed run | Status |
|---|---|---|
| `rtfm_mini` | `data/output/rtfm_mini/20260917_192308` (plus two older runs kept for comparison) | accepted, round 2 |
| `rtfm` | `data/output/rtfm/20260828_181451` | accepted, round 1 |
| `sepsis` | `data/output/sepsis/20260828_182820` | accepted, round 1 |
| `bpic2019` | `data/output/bpic2019/20260829_080358` | stopped after Step 6, no `final/`; distance files not committed (see [`data/output/bpic2019/README.md`](../data/output/bpic2019/README.md)) |

`.gitignore` does not exclude these four log directories, so a new example run appears as
untracked output; delete it or commit it deliberately. Cost grows with variant count, and one
output grows quadratically:

| Example | Variants | Step 6 distance files | LLM calls (Steps 5/6/8) |
|---|---|---|---|
| `rtfm_mini` | 6 | ~1 KB | a handful |
| `rtfm` | 231 | ~0.53 MB | tens |
| `sepsis` | 846 | ~7.0 MB | tens |
| `bpic2019` | 11,973 | ~1.37 GB | by far the most |

**`bpic2019` needs particular care before an unattended run.** Its ~14× more variants than
`sepsis` produce ~200× larger distance files, and it has the highest wall-clock time, LLM spend,
and peak memory (logged per step in `pipeline.log`) of the four. Two flags in
`examples/bpic2019/config_bpic2019.yaml` trade information for speed:

- `skip_precision` — skips Step 7's single-threaded precision computation.
- `skip_pairwise_distances` — skips Step 6's quadratic distance computation, losing
  `assignment_report.md`'s cohesion/divergence sections and `assignments.csv`'s nearest-neighbor
  columns.

`prune_pairwise_distances_on_finalize` instead frees the disk after a run is accepted. The root
README's [Resource usage](../README.md#resource-usage) section details all three.

## If a run stops in Step 6

On a large log, a provider-side 429/503 will eventually lose an assignment batch. Step 6 then saves
what it assigned and raises `IncompleteAssignmentError` instead of passing a partial assignment to
Steps 7–9. Re-running Step 6 with the same `run_id` resumes, sending only the missing narratives;
Steps 7, 7b, 8 and 9 then run as usual. See the root
[`README.md`](../README.md#when-a-step-cannot-finish-incompleteassignmenterror), and the GUI's
Diagnostics page for any run's warnings and stopping point.

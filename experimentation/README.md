# `experimentation`

Case-study drivers that run the `goalcat` pipeline library against a real event log. Both
subpackages import `goalcat`; `goalcat` never imports either of them. This package lives at the
repository root rather than under `src/`: it consumes the pipeline but is not part of the
implemented core, unlike `src/goalcat/` (the library) and `src/gui/` (a Streamlit app over it).

- **`examples/`** — one self-contained, runnable illustration per supported log (`rtfm_mini`,
  `rtfm`, `bpic2019`, `sepsis`): a config file plus an `example_run.py` driver.
  These demonstrate that the pipeline executes end to end (including, for `rtfm_mini`, a scripted
  Step 9 rework round) and are the fastest way to exercise a change locally. They are not evidence
  for any research claim on their own.
- **`icpm2027/`** — the replication package for the ICPM 2027 submission: every run under a
  frozen, versioned experimental protocol. Distinct from `examples/` because these replication runs
  must stay under explicit freeze/versioning conditions that an illustrative demo does not need,
  and because a reader running the replication package should not have to pick the right script
  out of a directory mixed with unrelated demos.

`examples/` scripts are invoked directly, as a module, from the repository root:

```bash
python -m experimentation.examples.rtfm_mini.example_run
```

`icpm2027/`'s protocol is driven programmatically rather than through one `example_run.py` per
condition — see [`experimentation/icpm2027/README.md`](icpm2027/README.md) for its module
inventory, current status, and the pre-registration gate that must be resolved before any frozen
run executes.

See the top-level [`README.md`](../README.md) for installation and LLM-backend setup.

## Resource cost before running an example

Every `examples/` script makes real, billed LLM calls and writes a full run directory under
`data/output/`. Only `rtfm_mini`'s output is committed to this repository, as a complete
end-to-end reference (its 6-variant fixture keeps time/cost/disk negligible); the other three
examples reproduce locally but are `.gitignore`d, since their outputs do not scale linearly with
log size — see the root [`README.md`](../README.md#resource-usage) "Resource usage" section for
the full explanation of what drives that growth.

**`bpic2019` is the outlier and deserves particular caution before running it unattended:**

| Example | Variants | Pairwise distance files (Step 6) | LLM calls (Steps 5/6/8) |
|---|---|---|---|
| `rtfm_mini` | 6 | ~1 KB | a handful |
| `rtfm` | 231 | ~0.53 MB | ~tens |
| `sepsis` | 846 | ~7.0 MB | ~tens |
| `bpic2019` | 11,973 | ~1.37 GB | proportionally the most of the four |

Pairwise distance file size grows quadratically with variant count (`n(n-1)/2`), not linearly, so
`bpic2019`'s ~14x larger variant count than `sepsis` produces a ~200x larger combined
`structural_distances`/`profile_distances` file — budget disk, wall-clock time, and LLM spend
accordingly, and expect its peak memory (logged per step in `pipeline.log`) to be the largest of
the five as well.

Two config flags trade information for speed on a large run — set them in
`examples/bpic2019/config_bpic2019.yaml` before running it if the tradeoff is acceptable for your
purpose (see the root README's "Resource usage" section for what each gives up):

- `skip_precision` — skips Step 7's single-threaded, GIL-bound precision computation.
- `skip_pairwise_distances` — skips Step 6's quadratic structural/profile distance computation
  entirely, avoiding the disk cost above (at the cost of `assignment_report.md`'s
  cohesion/divergence sections and `assignments.csv`'s nearest-neighbor columns).

`prune_pairwise_distances_on_finalize` (also in the root README's "Resource usage" section) frees
the disk these two files occupy after a run is accepted, once you no longer need it.

## If a run stops in Step 6

On a log this size a provider-side 429/503 will eventually lose an assignment batch. Step 6 saves
what it assigned and raises `IncompleteAssignmentError` rather than carrying a partial assignment
into Steps 7-9; re-running Step 6 with the same `run_id` resumes and retries only the missing
narratives, after which Steps 7, 7b, 8 and 9 run as usual. See the root
[`README.md`](../README.md#when-a-step-cannot-finish-incompleteassignmenterror), and the GUI's
Diagnostics page for any run's warnings and where it stopped.

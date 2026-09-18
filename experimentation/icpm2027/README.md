# `experimentation.icpm2027`

Replication package for the ICPM 2027 submission: the frozen, versioned experimental protocol, as
opposed to the illustrative, unfrozen demos in `experimentation/examples/`.

## Modules

| Module | Purpose |
|---|---|
| `configs/protocol.yaml` | Frozen freeze-table values (sampling, LLM parameters, batch size, steps) shared by every dataset and arm |
| `configs/preregistration.yaml` | Pre-registered decisions (C5, C6, C7, C10, C13, D1, D6, D7, degenerate-OR policy), gated *before* execution |
| `configs/{rtfm,sepsis,bpic2019}.yaml` | Per-dataset specs: log and goal-model filenames, keys, role, variant scope, declared axes |
| `configs/label_lists/<dataset>.yaml` | Task C5's label lists, each with its own provenance header |
| `protocol.py` | Merges protocol, dataset spec, and pre-registration into one condition's executable config; the pre-registration gate |
| `inputs.py` | Runs Steps 1–4 **once** per dataset into a shared base (`icpm2027_base`); Task C7's variant-scope policies; copies, never recomputes, into each condition |
| `conditions.py` | Executes one condition end to end (inputs → config → launch → manifest); Task C5's `label_list` control and its `label_list_strict` companion |
| `run_condition.py` | Subprocess entry point for one condition: Steps 5–8 only, Step 9 refused |
| `manifest.py` | Per-run manifest: hashes, resolved model version, seed (documented as unavailable), everything Task D4 requires |
| `freeze.py` | Verifies the freeze table row by row from the manifests after the fact, not only by construction |
| `goalmodel/perturb.py` | Experiment 2's perturbations (A remove, B merge, C distractor), built on `goalcat.grl.GRLModel`; writes to `data/goals/perturbed/` |
| `baselines/structural_clustering.py` | Task C3: boolean activity vectors + HDBSCAN, no LLM |
| `baselines/rule_based_rtfm.py` | Task C4: hand-written activity rules for RTFM's five declared alternatives, no LLM |
| `analysis/coverage.py` | Macro/micro coverage and residual (Task D2's caveat) |
| `analysis/contingency.py` | Contingency matrices and merge/split identification between any two conditions |
| `analysis/divergence.py` | AMI/NMI under all four residual-handling × weighting conventions, D1's pre-registered one flagged; never reported as accuracy |
| `analysis/aggregate_tables.py` | k-replicate aggregation across every frozen run on disk: the paper's setup and divergence tables. Row-count-checks each `assignments.csv`, so a run left short by a provider outage is never aggregated silently |
| `analysis/heldout.py` | Task C1: BPIC 2019 held-out label recovery against `case:Item Category` |
| `analysis/timing.py` | Task C9: step wall-clock, LLM-call latency, and peak RSS, parsed from each `pipeline.log` |
| `analysis/cost.py` | Task C15: hosted-LLM spend summed over every `*_run_metadata.json` |
| `analysis/report.py` | Assembles one dataset's evidence into Markdown: scope, coverage, declared-alternative coverage, contingency, divergence, baselines, and Task E7's instability qualification |
| `run_experiment.py` | **The driver**: one experiment on one dataset, end to end |

Every module has been exercised against the real `data/goals/*.jucm` files and real logs, not
fixtures only. **[`RUNS.md`](RUNS.md)** inventories every run directory under
`data/output/{rtfm,sepsis,bpic2019}/icpm2027_*` and every artifact under
`data/output/icpm2027_results/`: what each is, which paper number it feeds, and what was deleted
as superseded.

## Before running

1. **Re-read the pre-registration.** Every decision in `configs/preregistration.yaml` is
   `status: decided`, so `prereg.require()` passes for all three datasets. Several were amended
   before the runs they govern (C5's label-list arms, extended to `label_list_strict` and to BPIC
   2019; C6, enabling Experiment 2 on Sepsis; C10, the batch size). A decision is never edited
   after its run has executed: supersede it, or amend only the unexecuted portion with a dated
   `amended_on` note.
2. **Use a paid-tier `GEMINI_API_KEY`.** `assignment_batch_size` is `25` on all three datasets
   (`protocol_version` 1.1.0), so the full 11,973-variant BPIC 2019 scope costs roughly 480 Step 6
   calls per condition. `--dry-run` prints each condition's estimated call count before anything
   is billed.
3. **Run `--experiment stability` (Task C12) first**, especially on a goal model that is mostly
   AND-decomposed above the leaf level. It is the cheapest check, an unstable result changes how
   every other number from that dataset is reported (Task E7), and it disqualifies the dataset from
   Experiment 2.

## Running

```bash
# Task C12 — is Step 5a stable on this dataset? (k reruns, one LLM call each)
python -m experimentation.icpm2027.run_experiment --dataset rtfm --experiment stability

# Experiment 1 — paired guided/open arms, with replicates and the C3/C4 baselines
python -m experimentation.icpm2027.run_experiment --dataset rtfm --experiment e1

# ... adding Task C11a's ablation as a third arm
python -m experimentation.icpm2027.run_experiment --dataset rtfm --experiment e1 \
    --arms guided,open,guided_no_sample

# ... or Task C5's label-list control (needs configs/label_lists/<dataset>.yaml)
python -m experimentation.icpm2027.run_experiment --dataset rtfm --experiment e1 \
    --arms guided,label_list,label_list_strict

# Experiment 2 — perturbations (refused on a dataset C12 found unstable)
python -m experimentation.icpm2027.run_experiment --dataset rtfm --experiment e2

# Cross-run analyses (no LLM calls)
python -m experimentation.icpm2027.analysis.aggregate_tables
python -m experimentation.icpm2027.analysis.heldout --dataset bpic2019
python -m experimentation.icpm2027.analysis.timing
python -m experimentation.icpm2027.analysis.cost
```

| Flag | Effect |
|---|---|
| `--axis <name>` | Run one declared axis from `configs/<dataset>.yaml`. Omitted, every axis runs in turn (Sepsis declares two: `admission`, `discharge`). |
| `--dry-run` | Resolve and log every condition with its call estimate; launch nothing. Still builds the shared base if absent, because the estimate depends on the variant count Steps 1–4 produce. |
| `--force` | Clear a condition's round directory and re-run it from Step 5a. |
| `--allow-pending-decisions` | Run despite unresolved pre-registration; manifests are stamped NOT pre-registered. |

**Resuming.** A condition whose directory holds both `05_taxonomy/taxonomy.json` and
`06_assignment/assignments.csv` is skipped. An incomplete one resumes in place: `run_condition`
skips Step 5a whenever `taxonomy.json` exists, so Step 6 retries only the pending narratives
against the same taxonomy. Re-inducing would regenerate the `category_id` slugs and corrupt the
partial `assignments.csv`, which is why only `--force` does so.

**Replicate counts.** One `run_experiment` invocation runs the number of E1 replicates that
`protocol.yaml`'s `replicates.unperturbed` held at that time. The guided and open arms were later
extended over separate invocations (the count raised, `--arms` scoped to one arm, then reverted,
as `protocol.yaml` documents). Final counts:

| Arm | RTFM | Sepsis | BPIC 2019 |
|---|---|---|---|
| `guided` | 5 | 5 per axis | 3 (bounded for cost) |
| `open` | 5 | 5 | 3 |
| `guided_no_sample` | 2 | 2 per axis | 2 |
| `label_list`, `label_list_strict` | 2 | 2 | 2 |

The guided arms run once per declared axis; `open` and the label-list arms induce their own
categories and have no axis.

`aggregate_tables` discovers whatever replicates exist on disk, so the `n` it prints is what was
executed. It writes `data/output/icpm2027_results/aggregate_tables.{json,md,tex}` and
`aggregate_tables_label_list.tex`.

## Status

All planned tasks are executed; their outputs are in `data/output/icpm2027_results/`.

| Task | Output | Note |
|---|---|---|
| C1 — held-out label recovery | `bpic2019/label_recovery.md` | Low agreement (case-weighted 18–25%), mostly from an axis mismatch: `case:Item Category` is an SAP PO-line *configuration* attribute, while the guided categories key on *observed* goods-receipt/invoice order. Report with that framing, never as accuracy. |
| C4 — RTFM rule baseline | the RTFM Experiment 1 report | Run automatically by `--experiment e1` on RTFM. |
| C8 — boolean-vector collapse | `rtfm_mini/c8_boolean_vector_collapse.md` | Two real installment-payment cases (`A10009`, `A10798`) share an activity set with the single-payment case `A10000`: one structural cluster, three distinct narratives. The same work fixed a `build_activity_vectors` defect (it vectorized characters, not activities, when given a raw `read_csv` frame); the Task C3 baseline in all three E1 reports was regenerated. |
| C9, C15 — timing, cost, feasibility | `timing.md`, `cost.md` | The feasibility write-up, including the local `qwen2.5:3b` (Ollama) Step 6 comparison, is `project/FEASIBILITY_CHARACTERIZATION.md` in the paper repository. Unlike the other tasks it may draw on non-frozen runs. |

**Tests.** `tests/test_icpm2027_regression.py` (`python -m pytest tests/ -q`, needs the `test`
extra) guards the four rules every reported number rests on: the axis frontier Step 5a must cover,
the blocking partition check, coverage/residual arithmetic, and the target/collateral
reassignment split. Each case comes from a real defect or a frozen artifact. The LLM steps are not
asserted on, and the rest of the repository is covered only by having been run against real logs
and `.jucm` files.

## The `.jucm`/`.md` split

Every goal model's pipeline input is `data/goals/<log>_goal_model.jucm`, read through `goalcat.grl`.
`data/goals/<log>GM_description.md` documents how the `.jucm` was authored and is parsed by no code
in this repository. `configs/*.yaml`'s `goal_model_filename`, `goalmodel/perturb.py`, and every
condition here point at `.jucm` files only.

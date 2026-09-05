# `experimentation.icpm2027`

Replication package for the ICPM 2027 submission: the frozen, versioned experimental protocol,
as opposed to `experimentation/examples/`'s illustrative per-log demos with no freeze guarantees.

## What's implemented

| Module | Purpose |
|---|---|
| `configs/protocol.yaml` | Frozen freeze-table values (sampling, LLM params, batch size, steps) shared by every dataset/arm |
| `configs/preregistration.yaml` | Pre-registered decisions (C5, C6, C7, C10, C13, D1, D6, D7, degenerate-OR policy), gated *before* execution |
| `configs/{rtfm,sepsis,bpic2019}.yaml` | Per-dataset specs (log/goal-model filenames, keys, role, variant scope) |
| `protocol.py` | Merges protocol + dataset spec + preregistration into one condition's executable config; the pre-registration gate |
| `inputs.py` | Runs Steps 1-4 **once** per dataset into a shared base; Task C7 variant-scope policies; copies (never recomputes) into each condition |
| `conditions.py` | Executes one condition end to end (materialize inputs → render config → launch → manifest); Task C5's label-list control and its label\_list\_strict companion |
| `run_condition.py` | The actual subprocess entrypoint (Steps 5-8 only; Step 9 refused outright) |
| `manifest.py` | Per-run manifest — hashes, resolved model version, seed (documented as unavailable), everything Task D4 asks for |
| `freeze.py` | Verifies the freeze table row-by-row from manifests after the fact, not just by construction |
| `goalmodel/perturb.py` | Experiment 2's perturbations (A/B/C), built on `goalcat.grl.GRLModel` |
| `baselines/structural_clustering.py` | Task C3 — boolean activity-vector + HDBSCAN, zero LLM cost |
| `analysis/coverage.py` | Macro/micro coverage, residual (Task D2's caveat) |
| `analysis/contingency.py` | Contingency matrices + merge/split identification, for any two conditions |
| `analysis/divergence.py` | AMI/NMI over all four (residual-handling x weighting) conventions, with D1's pre-registered one flagged; never reported as accuracy |
| `analysis/aggregate_tables.py` | k-replicate aggregation across every frozen run — the paper's setup and divergence tables (residual mean [min-max] over n replicates; AMI over all within- and cross-arm pairs, both weightings), including `guided_no_sample`, `label_list`, and `label_list_strict`. Row-count-checks `assignments.csv` before trusting a run, so a provider outage that leaves one short is never silently aggregated. Reads run directories only; no LLM call |
| `analysis/report.py` | Assembles one dataset's evidence into Markdown — scope framing, coverage, declared-alternative coverage, contingency, divergence, and Task E7's instability qualification |
| `run_experiment.py` | **The driver.** `--experiment stability\|e1\|e2` for one dataset, end to end |

Every piece above has been exercised against the real `data/goals/*.jucm` files and/or the real
RTFM log (`data/logs/rtfm.xes.gz`) during development — not run against fixtures only.

**[`RUNS.md`](RUNS.md)** inventories every run directory that currently exists under
`data/output/{rtfm,sepsis,bpic2019}/icpm2027_*` and every cross-run artifact under
`data/output/icpm2027_results/` — what each one is, which paper number it feeds, and what was
deleted as superseded. The paper reports aggregates only; this is the map back to the run that
produced them.

## How to run it

```bash
# Task C12 first — is this dataset's Step 5a taxonomy even stable? (k reruns, 1 LLM call each)
python -m experimentation.icpm2027.run_experiment --dataset rtfm --experiment stability

# Experiment 1 — paired guided/open, with replicates and the structural baseline
python -m experimentation.icpm2027.run_experiment --dataset rtfm --experiment e1

# ... adding Task C11a's ablation as a third arm
python -m experimentation.icpm2027.run_experiment --dataset rtfm --experiment e1 \
    --arms guided,open,guided_no_sample

# ... or Task C5's label-list control and its label_list_strict companion (needs
# configs/label_lists/<dataset>.yaml authored first — see conditions.py's load_label_list)
python -m experimentation.icpm2027.run_experiment --dataset rtfm --experiment e1 \
    --arms guided,label_list,label_list_strict

# Experiment 2 — perturbations (refuses on a dataset C12 showed unstable)
python -m experimentation.icpm2027.run_experiment --dataset rtfm --experiment e2

# The paper's two aggregate tables, recomputed across every replicate on disk (no LLM call)
python -m experimentation.icpm2027.analysis.aggregate_tables
```

`aggregate_tables` is the k-replicate complement to `run_experiment`: a single invocation's E1 loop
is fixed at `protocol.yaml`'s `unperturbed` replicate count at the time it runs and reports only
the reps it was asked to cover, whereas the guided and open arms were extended beyond that count
over several separate invocations (`replicates.unperturbed` bumped, `--arms` scoped to the one arm
being extended, then reverted — the mechanism `protocol.yaml`'s own comment documents): guided and
open both reached five replicates on RTFM and both Sepsis axes, and three on BPIC 2019 (which never
ran at five, to bound its per-replicate cost); `label_list`/`label_list_strict` were not extended
and stay at two replicates everywhere. `aggregate_tables` discovers whatever replicates exist on
disk regardless of which invocation produced them, so the `n` it prints is what was executed, and
writes `data/output/icpm2027_results/aggregate_tables.{json,md,tex}` plus
`aggregate_tables_label_list.tex` for the label-list control's own table.

`--dry-run` resolves and logs every condition, with its LLM-call estimate, and launches nothing.
It still builds the shared base if absent (Steps 1-4 are deterministic and LLM-free), because the
call estimate depends on the variant count they produce. Re-running resumes: a condition whose run
directory is already complete (holds both `05_taxonomy/taxonomy.json` and
`06_assignment/assignments.csv`) is skipped unless `--force`. An *incomplete* condition is resumed
in place — `run_condition` skips Step 5a whenever `05_taxonomy/taxonomy.json` already exists, so the
resumed Step 6 retries only its still-pending narratives against the same frozen taxonomy rather than
re-inducing one (re-induction regenerates the `category_id` slugs and would corrupt the partial
`assignments.csv`). `--force` clears the round directory first, so it does re-induce.

Run `stability` before `e1` on any dataset whose goal model is mostly AND-decomposed above the leaf
level. It is the cheapest check here and a negative result changes how every other number from that
dataset must be reported (Task E7) and disqualifies it from Experiment 2.

## What's still open

Not yet built, in roughly the following priority order:

- **Task C4** — RTFM's rule-based baseline (terminal-activity rule reproducing {TP,TA,TB,TC,TD}).
- ~~**Task C1**~~ — **done, 2026-08-31.** `analysis/heldout.py` + `configs/bpic2019.yaml`'s
  `heldout_label_map`; run with `python -m experimentation.icpm2027.analysis.heldout --dataset bpic2019`.
  Report at `data/output/icpm2027_results/bpic2019/label_recovery.md`. Low agreement (case-weighted
  18–25%), driven mostly by a definitional axis mismatch — `case:Item Category` is an SAP PO-line
  *configuration* attribute, the guided categories key on *observed* GR/invoice order — plus a
  residual LLM-ordering error. Report with that framing, never as accuracy.
- ~~**`rtfm_mini`'s Task C8 demonstration**~~ — **done, 2026-08-31.** Two real installment-payment
  cases (`A10009`, `A10798`) added to `data/logs/rtfm_mini.xes.gz`; they share an activity set with
  the single-payment case `A10000`, so all three map to one boolean activity-presence vector and
  one structural cluster while their narratives stay distinct. Artifact:
  `data/output/icpm2027_results/rtfm_mini/c8_boolean_vector_collapse.md`. This run also fixed a
  `build_activity_vectors` defect (it vectorized characters, not activities, when handed a raw
  `read_csv` frame) — the Task C3 structural baseline in all three E1 reports was regenerated.
- **Task C15** — the feasibility & resource-characterization report (`project/FEASIBILITY_CHARACTERIZATION.md`
  in the paper repo): execution environment, approximate wall-clock/cost, and a sensitivity analysis
  over model choice, hardware, and configuration for industrial adoption. Builds on `analysis/timing.py`
  plus the `estimated_cost_usd` roll-up in `goalcat.llm.usage_summary`; generated after the last frozen
  run and, unlike Task C9, may draw on non-frozen runs. Its terminal item is one local-LLM (Ollama) run
  for RTFM and Sepsis, Step 6 only, for a measured cheap-model comparison point.
- **Tests.** `tests/test_icpm2027_regression.py` (run: `python -m pytest tests/ -q`, needs the
  `test` extra) guards the four rules every reported number rests on --- the axis frontier Step 5a
  must cover, the blocking partition check, coverage/residual arithmetic, and the target/collateral
  reassignment split --- each case drawn from a real defect or a frozen artifact. That is the whole
  of it: the pipeline's LLM steps are not asserted on, and the rest of the repository is still
  covered only by having been exercised against real logs and real `.jucm` files.

## The `.jucm`/`.md` split

Every goal model's actual pipeline input is `data/goals/<log>_goal_model.jucm` — read via
`goalcat.grl` (see that package's docstring), never `data/goals/<log>GM_description.md`, which is
documentation about how the `.jucm` was authored and is never parsed by any code in this
repository. `configs/*.yaml`'s `goal_model_filename` fields, `goalmodel/perturb.py`'s
perturbations, and every condition this package runs all point at `.jucm` files exclusively.

## Before running anything for real

1. **Pre-registration is now resolved** — C5, C6, C7, C10, C13, D1, D6, D7 and the degenerate-OR
   policy are all `status: decided`, so `prereg.require()` passes for all three datasets. Re-read
   them before running: `C5_label_list_control` was adopted for RTFM/Sepsis on 2026-09-04, extended
   the same day to a `label_list_strict` companion (the criterion-wording factor, isolated from the
   list's content), and extended again to BPIC 2019 in a third same-day amendment — all three logs
   now carry both arms (`data/output/{rtfm,sepsis,bpic2019}/icpm2027_e1_label_list*`), authored per
   `configs/label_lists/<dataset>.yaml`'s own provenance header;
   `C6_sepsis_perturbations` was flipped to `true` on 2026-08-29 after Sepsis's Step 5a induction
   was re-verified stable, so Experiment 2 now runs on Sepsis as well as RTFM (its runs already
   exist under `data/output/sepsis/icpm2027_e2_*`); and `C10_assignment_batch_size` carries a
   2026-08-29 BPIC 2019 amendment (batch size 50 → 25) later retired on 2026-09-04 in favor of one
   uniform value across all three datasets under `protocol_version` 1.1.0. Do not edit a decision
   after the run it governs has executed — supersede it, or amend only an as-yet-unexecuted portion
   with a dated `amended_on` note (as C5 and C10 both did, repeatedly).
2. Confirm `GEMINI_API_KEY` is exported and the account is off the free tier before a full-scale
   run. `assignment_batch_size` is `25`, uniform across all three datasets since the 2026-09-04
   `protocol_version` 1.1.0 amendment retired the earlier per-dataset exception (batch `50` proved
   unreliable at BPIC 2019's longer narratives — ~5-15% of Step 6 batches exceeded the 120 s
   timeout and aborted the condition — so `25` became the one value every log tolerates rather than
   a BPIC-2019-only carve-out). At 25 the full 11,973-variant BPIC 2019 scope is roughly 480 Step-6
   calls per condition. Use
   `--dry-run` to see `conditions.estimated_llm_calls()` for every condition before anything is billed.
3. Run `--experiment stability` (Task C12) before committing a dataset's budget to `e1`.

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
| `conditions.py` | Executes one condition end to end (materialize inputs → render config → launch → manifest); Task C5's label-list control |
| `run_condition.py` | The actual subprocess entrypoint (Steps 5-8 only; Step 9 refused outright) |
| `manifest.py` | Per-run manifest — hashes, resolved model version, seed (documented as unavailable), everything Task D4 asks for |
| `freeze.py` | Verifies the freeze table row-by-row from manifests after the fact, not just by construction |
| `goalmodel/perturb.py` | Experiment 2's perturbations (A/B/C), built on `goalcat.grl.GRLModel` |
| `baselines/structural_clustering.py` | Task C3 — boolean activity-vector + HDBSCAN, zero LLM cost |
| `analysis/coverage.py` | Macro/micro coverage, residual (Task D2's caveat) |
| `analysis/contingency.py` | Contingency matrices + merge/split identification, for any two conditions |
| `analysis/divergence.py` | AMI/NMI over all four (residual-handling x weighting) conventions, with D1's pre-registered one flagged; never reported as accuracy |
| `analysis/report.py` | Assembles one dataset's evidence into Markdown — scope framing, coverage, declared-alternative coverage, contingency, divergence, and Task E7's instability qualification |
| `run_experiment.py` | **The driver.** `--experiment stability\|e1\|e2` for one dataset, end to end |

Every piece above has been exercised against the real `data/goals/*.jucm` files and/or the real
RTFM log (`data/logs/rtfm.xes.gz`) during development — not run against fixtures only.

## How to run it

```bash
# Task C12 first — is this dataset's Step 5a taxonomy even stable? (k reruns, 1 LLM call each)
python -m experimentation.icpm2027.run_experiment --dataset rtfm --experiment stability

# Experiment 1 — paired guided/open, with replicates and the structural baseline
python -m experimentation.icpm2027.run_experiment --dataset rtfm --experiment e1

# ... adding Task C11a's ablation as a third arm
python -m experimentation.icpm2027.run_experiment --dataset rtfm --experiment e1 \
    --arms guided,open,guided_no_sample

# Experiment 2 — perturbations (refuses on a dataset C12 showed unstable)
python -m experimentation.icpm2027.run_experiment --dataset rtfm --experiment e2
```

`--dry-run` resolves and logs every condition, with its LLM-call estimate, and launches nothing.
It still builds the shared base if absent (Steps 1-4 are deterministic and LLM-free), because the
call estimate depends on the variant count they produce. Re-running resumes: a condition whose run
directory is already complete is skipped unless `--force`.

Run `stability` before `e1` on any dataset whose goal model is mostly AND-decomposed above the leaf
level. It is the cheapest check here and a negative result changes how every other number from that
dataset must be reported (Task E7) and disqualifies it from Experiment 2.

## What's still open

Not yet built, in roughly the following priority order:

- **Task C4** — RTFM's rule-based baseline (terminal-activity rule reproducing {TP,TA,TB,TC,TD}).
- **Task C1** — the BPIC 2019 label-recovery comparison (`case:Item Category` vs. Step 6's guided
  assignment). Report it as label recovery under an axis-aligned frame, not as independent ground
  truth: the goal model's organizing axis and that attribute carry the same four labels by
  construction, and T9 (Consignment) has no activity label at all, so its agreement figure is not
  comparable to the other three.
- **`rtfm_mini`'s Task C8 demonstration** (boolean-vector collapse of two rework variants) —
  `baselines/structural_clustering.py` makes this immediate to produce once wanted.
- **Tests.** There are none, here or anywhere in the repository. The modules have been exercised
  against real logs and real `.jucm` files, which is not the same thing as a regression suite.

## The `.jucm`/`.md` split

Every goal model's actual pipeline input is `data/goals/<log>_goal_model.jucm` — read via
`goalcat.grl` (see that package's docstring), never `data/goals/<log>GM_description.md`, which is
documentation about how the `.jucm` was authored and is never parsed by any code in this
repository. `configs/*.yaml`'s `goal_model_filename` fields, `goalmodel/perturb.py`'s
perturbations, and every condition this package runs all point at `.jucm` files exclusively.

## Before running anything for real

1. **Pre-registration is now resolved** — C5, C6, C7, C10, C13, D1, D6, D7 and the degenerate-OR
   policy are all `status: decided` as of 2026-08-25, so `prereg.require()` passes for all three
   datasets. Re-read them before running: `C5_label_list_control` is the one deliberately marked as
   the most revisitable (the label-list arm is supported in code and costs only budget to enable),
   and `C6_sepsis_perturbations` is set to `false` partly on a validity ground that would change if
   Sepsis's Step 5a induction ever became stable. Do not edit a decision after the run it governs
   has executed — supersede it with a new `protocol_version`.
2. Confirm `GEMINI_API_KEY` is exported and the account is off the free tier before a full-scale
   run. At the pre-registered `assignment_batch_size=50`, the full 11,973-variant BPIC 2019 scope
   is roughly 240 Step-6 calls per condition. Use `--dry-run` to see
   `conditions.estimated_llm_calls()` for every condition before anything is billed.
3. Run `--experiment stability` (Task C12) before committing a dataset's budget to `e1`.

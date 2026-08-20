# `experimentation.icpm2027`

Replication package for the ICPM 2027 submission (*Goal-driven variant categorization*): the
frozen, versioned experimental protocol behind EXPERIMENTATION_PLAN.md, as opposed to
`experimentation/examples/`'s illustrative per-log demos with no freeze guarantees.

## What's implemented

| Module | Purpose | Plan reference |
|---|---|---|
| `configs/protocol.yaml` | Frozen freeze-table values (sampling, LLM params, batch size, steps) shared by every dataset/arm | §2.2 |
| `configs/preregistration.yaml` | Open decisions (Task C7's BPIC 2019 scope, C10's batch size, C5/C6/D6), gated *before* execution | §12, §13 |
| `configs/{rtfm,sepsis,bpic2019}.yaml` | Per-dataset specs (log/goal-model filenames, keys, role, variant scope) | §5, §8 |
| `protocol.py` | Merges protocol + dataset spec + preregistration into one condition's executable config; the pre-registration gate | §2.2, §12 |
| `inputs.py` | Runs Steps 1-4 **once** per dataset into a shared base; Task C7 variant-scope policies; copies (never recomputes) into each condition | §2.1, Task C7 |
| `conditions.py` | Executes one condition end to end (materialize inputs → render config → launch → manifest); Task C5's label-list control | §2, Task C5 |
| `run_condition.py` | The actual subprocess entrypoint (Steps 5-8 only; Step 9 refused outright) | §3 step 7 |
| `manifest.py` | Per-run manifest — hashes, resolved model version, seed (documented as unavailable), everything Task D4 asks for | §2.2, Task D4 |
| `freeze.py` | Verifies the freeze table row-by-row from manifests after the fact, not just by construction | §2.2 |
| `goalmodel/perturb.py` | Experiment 2's perturbations (A/B/C), built on `goalcat.grl.GRLModel` | §4 |
| `baselines/structural_clustering.py` | Task C3 — boolean activity-vector + HDBSCAN, zero LLM cost | §2.3, Task C3 |
| `analysis/coverage.py` | Macro/micro coverage, residual (§3 evidence item 3, Task D2's caveat) | §3, §7 |
| `analysis/contingency.py` | Contingency matrices + merge/split identification, for any two conditions (§3 evidence items 4-5) | §3, §7 |

Every piece above has been exercised against the real `data/goals/*.jucm` files and/or the real
RTFM log (`data/logs/rtfm.xes.gz`) during development — not run against fixtures only.

## What's still open

Not yet built, in roughly the order §10/§13 prioritizes them:

- **A single per-dataset driver** tying `protocol.py`/`inputs.py`/`conditions.py` into one
  "run Experiment 1 for RTFM" command (guided + open + replicates + structural baseline). Every
  piece it would call already exists; this is orchestration, not new capability.
- **Task C4** — RTFM's rule-based baseline (terminal-activity rule reproducing {TP,TA,TB,TC,TD}).
- **Task C1** — the BPIC 2019 held-out validation (`case:Item Category` vs. Step 6's guided
  assignment) — needs the BPIC 2019 frozen run to exist first.
- **Task D1** — AMI/NMI divergence (optional; convention is fixed in `configs/preregistration.yaml`,
  computation itself isn't written).
- **Experiment 2's measurement** — `TargetReassignment`/`CollateralReassignment` computed from a
  pair of contingency matrices (before/after a perturbation); `goalmodel/perturb.py` produces the
  perturbed model, `analysis/contingency.py` can already build the matrices, but nothing yet
  chains "run guided on `G_0`, run guided on the perturbed model, diff the two" into one call.
- **`rtfm_mini`'s Task C8 demonstration** (boolean-vector collapse of two rework variants) —
  `baselines/structural_clustering.py` makes this immediate to produce once wanted.

## The `.jucm`/`.md` split

Every goal model's actual pipeline input is `data/goals/<log>_goal_model.jucm` — read via
`goalcat.grl` (see that package's docstring), never `data/goals/<log>GM_description.md`, which is
documentation about how the `.jucm` was authored and is never parsed by any code in this
repository. `configs/*.yaml`'s `goal_model_filename` fields, `goalmodel/perturb.py`'s
perturbations, and every condition this package runs all point at `.jucm` files exclusively.

## Before running anything for real

1. **Resolve `configs/preregistration.yaml`'s pending decisions** (C7, C10, C5, C6, D6) — `protocol.require()`
   refuses a frozen run while any decision governing its dataset is still `status: pending`.
2. Confirm `GEMINI_API_KEY` is exported and the account is off the free tier before a full-scale
   run — Task C7's ~24k-call BPIC 2019 estimate is real; `conditions.estimated_llm_calls()` reports
   the count for whatever scope is chosen before anything is billed.

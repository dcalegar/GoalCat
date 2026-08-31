# Run inventory

What every directory under `data/output/{rtfm,sepsis,bpic2019}/icpm2027_*` and
`data/output/icpm2027_results/` actually is. The paper reports aggregate numbers only; this file
is the map from those numbers back to the run that produced them, since nothing else does. Update
it whenever a run is added, superseded, or deleted — an inventory that lags the directory listing
is worse than none.

## Naming convention

A run directory is `icpm2027_<condition_id>`, and `condition_id` (`protocol.py`'s
`ConditionSpec.condition_id`) is built as:

```
<experiment>_<arm>[_axis<axis>][_<tag>]_rep<replicate>
```

- `experiment` — `c12` (Task C12 stability), `e1` (Experiment 1), or `e2` (Experiment 2).
- `arm` — `guided`, `open`, `guided_no_sample`, or `label_list`.
- `_axis<axis>` — present **only** when the dataset declares more than one axis (Sepsis). A
  single-axis dataset's directories carry no axis segment even though the condition still has one
  internally (recorded in its manifest's `axis`/`axis_root` fields) — this keeps RTFM's and BPIC
  2019's paths stable across the axis-declaration change. The open arm never carries an axis
  segment on any dataset: it reads no goal model, so one open run serves every axis.
- `_<tag>` — a perturbation id (`pertA_remove_<id>`, `pertB_merge_<id1>_<id2>`) or `stability`.
- `rep<replicate>` — 1-based replicate index.

`icpm2027_base` is Steps 1-4's shared output (variant extraction, profiling, textualization,
narrative sample) — computed once per dataset and copied, never recomputed, into every condition,
per the freeze table's identical-inputs rows (`inputs.py`).

Cross-run artifacts live in `data/output/icpm2027_results/<dataset>/`, with the same
axis-conditional suffix: `experiment1<suffix>.md`, `experiment2<suffix>.json`,
`stability<suffix>.json`, `freeze_e1<suffix>.md`/`.json`, `freeze_e2<suffix>.md`/`.json`, where
`<suffix>` is `_axis<axis>` on Sepsis and empty on RTFM/BPIC 2019.

## Why Sepsis has an axis and the others don't

Sepsis's root goal is AND-decomposed over two independent Or frontiers — admission (`5` →
Admission NC/IC) and discharge (`6` → Release A-E) — so it declares no single categorization
axis (`goalcat.grl.GRLModel.axis_frontier()` raises `AxisError` on it without one). Each frontier
is run as its own axis, `admission` and `discharge`, declared in `configs/sepsis.yaml`'s `axes:`
map. RTFM (`resolution`) and BPIC 2019 (`matching_regime`) each declare exactly one axis and are
unaffected by this beyond carrying the axis in their manifests. See `paperICPM27.tex`
§Discussion/Threats ("The approach presupposes an axis a goal model may not declare") for the
paper-facing explanation, and `data/goals/sepsisGM_description.md` §4 for the goal-model-level one.

## RTFM (`data/output/rtfm/`, axis: `resolution`)

| Run | Purpose | Result file |
|---|---|---|
| `base` | Steps 1-4, shared by every condition below | — |
| `c12_guided_stability_rep1`–`5` | Task C12: 5 identical-input Step 5a-only reruns | `stability.json` |
| `e1_guided_rep1`, `rep2` | Experiment 1, guided arm, the paired replicates | `experiment1.md` |
| `e1_guided_rep3`–`5` | Extra guided replicates, **not part of E1's pair** — exist solely to give Experiment 2's `CollateralReassignmentNull` five replicates ($\binom{5}{2}=10$ pairs) instead of one | `experiment2.json`'s `CollateralReassignmentNull` |
| `e1_guided_no_sample_rep1`, `rep2` | Task C11a ablation (Step 5a run with an empty narrative sample) | `experiment1.md` |
| `e1_open_rep1`, `rep2` | Experiment 1, open arm | `experiment1.md` |
| `e2_guided_pertA_remove_20_rep1` | Experiment 2A: remove *coercive credit collection* (leaf `20`) | `experiment2.json` |
| `e2_guided_pertB_merge_13_20_rep1` | Experiment 2B: merge *delinquent payment* (`13`) + *coercive collection* (`20`) | `experiment2.json` |

Freeze verification: `freeze_e1.md`/`.json` (all E1 conditions), `freeze_e2.md`/`.json` (baseline +
both perturbations). Both pass every row as of the 2026-08-31 re-run.

## Sepsis (`data/output/sepsis/`, axes: `admission`, `discharge`)

Every condition below runs twice — once per axis — except the open arm, which is axis-free and
shared. Directory names carry the `axisadmission`/`axisdischarge` segment.

| Run (both axes unless noted) | Purpose | Result file |
|---|---|---|
| `base` | Steps 1-4, shared by every condition on both axes | — |
| `c12_guided_axis{admission,discharge}_stability_rep1`–`5` | Task C12 per axis | `stability_axisadmission.json`, `stability_axisdischarge.json` |
| `e1_guided_axis{admission,discharge}_rep1`, `rep2` | Experiment 1, guided arm, paired replicates | `experiment1_axisadmission.md`, `experiment1_axisdischarge.md` |
| `e1_guided_axis{admission,discharge}_rep3`–`5` | Extra guided replicates for the E2 null (same reason as RTFM's rep3-5) | `experiment2_axis*.json`'s `CollateralReassignmentNull` |
| `e1_guided_no_sample_axis{admission,discharge}_rep1`, `rep2` | Task C11a ablation, per axis | `experiment1_axis*.md` |
| `e1_open_rep1`, `rep2` | Experiment 1, open arm — **no axis segment**, shared by both axes' contingency/divergence analysis | `experiment1_axis*.md` (both reference it) |
| `e2_guided_axisadmission_pertA_remove_16_rep1` | Experiment 2A on admission: remove *Admission IC* (`16`). No non-degenerate merge exists on this axis — its Or point has only two children, so `merge_alternatives()` refuses (`run_e2` logs this and reports Perturbation A only) | `experiment2_axisadmission.json` |
| `e2_guided_axisdischarge_pertA_remove_21_rep1` | Experiment 2A on discharge: remove *Release E* (`21`) | `experiment2_axisdischarge.json` |
| `e2_guided_axisdischarge_pertB_merge_17_18_rep1` | Experiment 2B on discharge: merge *Release A* (`17`) + *Release B* (`18`) | `experiment2_axisdischarge.json` |

Freeze verification: `freeze_e1_axisadmission.md`/`.json`, `freeze_e1_axisdischarge.md`/`.json`,
`freeze_e2_axisadmission.md`/`.json`, `freeze_e2_axisdischarge.md`/`.json`. All pass every row as
of the 2026-08-31 re-run (`icpm2027_e1_guided_axisadmission_rep3`'s pipeline.log shows one
transient `litellm.ServiceUnavailableError` retried and recovered within the same run — not a
freeze failure, and the resulting `assignments.csv` is complete).

## BPIC 2019 (`data/output/bpic2019/`, axis: `matching_regime`)

Untouched by the 2026-08-31 axis/RQ2 fix — its goal model declares one Or frontier
(`4` → 3-way-after-GR / 3-way-before-GR / 2-way / consignment) and its E1 conditions already
shared one `prompt_assignment_batch.txt` hash, so nothing here needed re-running.

| Run | Purpose | Result file |
|---|---|---|
| `base` | Steps 1-4 | — |
| `c12_guided_stability_rep1`–`5` | Task C12 | `stability.json` |
| `e1_guided_rep1`, `rep2` | Experiment 1, guided arm | `experiment1.md` |
| `e1_guided_no_sample_rep1`, `rep2` | Task C11a ablation | `experiment1.md` |
| `e1_open_rep1`, `rep2` | Experiment 1, open arm | `experiment1.md` |

**No Experiment 2 on BPIC 2019** — by design, not omission: the perturbation study (§4 of the
paper) targets RTFM and Sepsis only; BPIC 2019's role is the large-scale/high-cardinality
replication and the held-out-label check below.

Additional artifact: `label_recovery.md` — Task C1's held-out `Item Category` agreement check
(`analysis/heldout.py`), independent of the E1/E2/C12 conditions above.

## `rtfm_mini` (`data/output/rtfm_mini/`) — illustrative fixture, not part of the frozen design

Not run through `run_experiment.py` at all; it's the 8-case fixture behind the paper's running
example (Table `tab:rtfm-mini`, Fig. `fig:rtfm-mini`) and Task C8's structural-vector-collapse
demonstration, run directly through the base pipeline. Its single timestamped directory
(`20260831_064805/`) holds one full Steps 1-9 execution including a real Step 9 merge-revision
round (the *timely* + *delinquent payment* merge the paper's running-example text describes).
Result: `data/output/icpm2027_results/rtfm_mini/c8_boolean_vector_collapse.md`.

## Superseded and deleted runs

The 2026-08-31 axis/RQ2 fix (see `paperICPM27.tex` §Discussion/Threats and the `fix/axis-partition-and-rq2`
branch) invalidated and replaced the following, which have been **deleted** rather than kept
alongside their replacements:

- **RTFM** `e2_guided_pertA_remove_19_rep1` — removed *judicial appeal* (`19`), whose parent
  (Xor `7`, two children) went degenerate on removal. Superseded by `pertA_remove_20`, whose
  parent (Or `6`, three children) does not.
- **Sepsis, single-axis** `c12_guided_stability_rep1`–`5`, `e1_guided_rep1`/`rep2`,
  `e1_guided_no_sample_rep1`/`rep2`, `e2_guided_pertA_remove_21_rep1`,
  `e2_guided_pertB_merge_15_16_rep1` — induced one taxonomy spanning both the admission and
  discharge frontiers at once, which is not a partition (see "Why Sepsis has an axis" above). Both
  Experiment 2 conditions among these also re-anchored their taxonomy onto the AND-decomposed
  parents `5`/`6` instead of the perturbed leaves, a failure `check_axis_partition()` now rejects
  before a run can be reported. Superseded by the `axisadmission`/`axisdischarge` runs above.
- Corresponding perturbed goal-model files under `data/goals/perturbed/` for both of the above
  (`rtfm_goal_model__pertA_remove_19.*`, `sepsis_goal_model__pertA_remove_21.*`,
  `sepsis_goal_model__pertB_merge_15_16.*`).

If you need the discredited numbers for comparison (e.g. to show what the review caught), they are
in the paper repo's git history (`ICPM2027-GoalCat`, commit `945e2e8` and earlier) and in this
repo's git history for `data/output/icpm2027_results/*/experiment2*.json` before the
`fix/axis-partition-and-rq2` branch — not on disk.

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
- `arm` — `guided`, `open`, `guided_no_sample`, `label_list`, or `label_list_strict`.
- `_axis<axis>` — present **only** when the dataset declares more than one axis (Sepsis). A
  single-axis dataset's directories carry no axis segment even though the condition still has one
  internally (recorded in its manifest's `axis`/`axis_root` fields) — this keeps RTFM's and BPIC
  2019's paths stable across the axis-declaration change. The open arm never carries an axis
  segment on any dataset: it reads no goal model, so one open run serves every axis.
- `_<tag>` — a perturbation id (`pertA_remove_<id>`, `pertB_merge_<id1>_<id2>`,
  `pertC_distractor_<parent_id>_<id>`) or `stability`. Perturbation C's id folds in the axis's
  parent element because the distractor's own id is freshly allocated from the base model's id
  counter on every load — two axes of one dataset loading the same base model would otherwise
  allocate the same id and collide on one output file.
- `rep<replicate>` — 1-based replicate index.

`icpm2027_base` is Steps 1-4's shared output (variant extraction, profiling, textualization,
narrative sample) — computed once per dataset and copied, never recomputed, into every condition,
per the freeze table's identical-inputs rows (`inputs.py`).

Cross-run artifacts live in `data/output/icpm2027_results/<dataset>/`, with the same
axis-conditional suffix: `experiment1<suffix>.md`, `experiment2<suffix>.json`,
`stability<suffix>.json`, `freeze_e1<suffix>.md`/`.json`, `freeze_e2<suffix>.md`/`.json`, where
`<suffix>` is `_axis<axis>` on Sepsis and empty on RTFM/BPIC 2019.

Three artifacts sit one level up, in `data/output/icpm2027_results/` itself, because they aggregate
*across* datasets or replicates: `cost.md`, `timing.md`, and
`aggregate_tables.{json,md,tex}` (plus `aggregate_tables_label_list.tex`, the label-list/
label-list-strict control's own LaTeX table). The `aggregate_tables.*` files are the paper's setup
and divergence tables, recomputed by `analysis/aggregate_tables.py` over every replicate on disk —
they are the only artifacts reporting the guided/open arms' $n=5$ (RTFM/Sepsis) or $n=3$
(BPIC 2019) ranges, the resulting $\binom{5}{2}=10$ or $\binom{3}{2}=3$ within-arm AMI pairs, and
the `guided_no_sample`/`label_list`/`label_list_strict` arms, none of which the per-dataset
`experiment1<suffix>.md` covers (its driver is fixed at `protocol.yaml`'s `unperturbed` replicate
count at the time it ran and reports only the reps present in that invocation's `--arms`).
`_load_run()` in that module row-count-checks `assignments.csv` against `variants.csv` before
trusting a run — a provider outage that outlasts Step 6's own retries drops the unresolved
variant(s) from `assignments.csv` entirely, and a short file must never be silently aggregated
(hit twice in practice: Sepsis's `icpm2027_e1_open_rep1`, 2026-08-29; BPIC 2019's
`icpm2027_e1_label_list_rep1`, 2026-09-04 — both resumed and completed before being aggregated).

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
| `e1_guided_rep3`–`5` | Extra guided replicates, **not part of E1's pair** — they give Experiment 2's `CollateralReassignmentNull` five replicates ($\binom{5}{2}=10$ pairs) instead of one, and the paper's tables their $n=5$ ranges | `experiment2.json`'s `CollateralReassignmentNull`, `aggregate_tables.*` |
| `e1_guided_no_sample_rep1`, `rep2` | Task C11a ablation (Step 5a run with an empty narrative sample) | `aggregate_tables.*` (the per-dataset `experiment1.md` covers the guided/open pair only) |
| `e1_open_rep1`, `rep2` | Experiment 1, open arm | `experiment1.md` |
| `e1_open_rep3`–`5` | Extra open replicates, added 2026-09-04 — give the open arm's own replicate-agreement floor the same $n=5$ standing as guided's ($\binom{5}{2}=10$ pairs) rather than resting on a single pair (`paperICPM27.tex` §Threats/Conclusion validity) | `aggregate_tables.*` |
| `e1_label_list_rep1`, `rep2` | Task C5 control: fixed, externally authored 5-category list (`configs/label_lists/rtfm.yaml`), run under `open`'s assignment criterion | `aggregate_tables.*`, `aggregate_tables_label_list.tex` |
| `e1_label_list_strict_rep1`, `rep2` | Task C5 control companion: the identical supplied list run under `guided`'s assignment criterion instead — isolates the criterion-wording factor from the list's content | `aggregate_tables.*`, `aggregate_tables_label_list.tex` |
| `e2_guided_pertA_remove_20_rep1`–`5` | Experiment 2A: remove *coercive credit collection* (leaf `20`), $k=5$ replicates (added 2026-09-04, same reason as `e1_guided_rep3`–`5`: a single perturbed run read against a five-replicate $C^\emptyset$ was asymmetric) | `experiment2.json` |
| `e2_guided_pertB_merge_13_20_rep1`–`5` | Experiment 2B: merge *delinquent payment* (`13`) + *coercive collection* (`20`), $k=5$ replicates | `experiment2.json` |
| `e2_guided_pertC_distractor_6_187_rep1`–`5` | Experiment 2C: add *fine annulment*, a prospectively named, plausible-but-unrealized alternative under Or `6` (parent-id-qualified name — see note below), $k=5$ replicates | `experiment2.json` |

Freeze verification: `freeze_e1.md`/`.json` (all E1 conditions), `freeze_e2.md`/`.json` (baseline +
all perturbations, all replicates). Both pass every row as of the 2026-08-31 re-run, again as of the
2026-09-04 `protocol_version` 1.1.0 re-run (C10's batch-size exception retired: every RTFM condition
above was re-executed at `assignment_batch_size=25`, matching BPIC 2019's value instead of the
earlier default of 50 — see `preregistration.yaml`'s C10 amendment), again once `label_list`/
`label_list_strict` and the `open_rep3`–`5` extension landed the same day, and again once E2's
perturbations were extended from one run each to $k=5$ replicates plus Perturbation C, same day
(all under 1.1.0, so no further protocol-version churn).

**Two bugs surfaced and were fixed while extending E2 to replicates + Perturbation C (2026-09-04):**
`freeze.py`'s "Goal model" row for `perturbed=True` originally required every guided condition's
goal-model hash to be pairwise distinct, which is correct for one run per perturbation but rejects
legitimate replicates of the *same* perturbation (which must share a hash). It now checks hash
consistency *within* a perturbation's own replicates (stripped of the trailing `_repN`) and
distinctness *across* perturbations. Separately, `perturb.add_distractor()` named its output file
from `model.new_id()` alone, which allocates from the same counter on every fresh model load — so
two different axes of one dataset (Sepsis admission and discharge, both loaded from
`sepsis_goal_model.jucm`) independently allocated the same id and collided on one output file,
each overwriting the other's mid-run. The perturbation id now folds in the axis's parent element id
(`pertC_distractor_<parent_id>_<distractor_id>`), which is always axis-specific. RTFM's distractor
carries the same qualified naming even though it has only one axis (no collision risk there), simply
because both datasets share the same `add_distractor()` code path.

## Sepsis (`data/output/sepsis/`, axes: `admission`, `discharge`)

Every condition below runs twice — once per axis — except the open arm, which is axis-free and
shared. Directory names carry the `axisadmission`/`axisdischarge` segment.

| Run (both axes unless noted) | Purpose | Result file |
|---|---|---|
| `base` | Steps 1-4, shared by every condition on both axes | — |
| `c12_guided_axis{admission,discharge}_stability_rep1`–`5` | Task C12 per axis | `stability_axisadmission.json`, `stability_axisdischarge.json` |
| `e1_guided_axis{admission,discharge}_rep1`, `rep2` | Experiment 1, guided arm, paired replicates | `experiment1_axisadmission.md`, `experiment1_axisdischarge.md` |
| `e1_guided_axis{admission,discharge}_rep3`–`5` | Extra guided replicates for the E2 null (same reason as RTFM's rep3-5) | `experiment2_axis*.json`'s `CollateralReassignmentNull` |
| `e1_guided_no_sample_axis{admission,discharge}_rep1`, `rep2` | Task C11a ablation, per axis | `aggregate_tables.*` (the per-dataset `experiment1_axis*.md` covers the guided/open pair only) |
| `e1_open_rep1`, `rep2` | Experiment 1, open arm — **no axis segment**, shared by both axes' contingency/divergence analysis | `experiment1_axis*.md` (both reference it) |
| `e1_open_rep3`–`5` | Extra open replicates, added 2026-09-04, same reason as RTFM's — **no axis segment**, shared by both axes | `aggregate_tables.*` |
| `e1_label_list_rep1`, `rep2` | Task C5 control (`configs/label_lists/sepsis.yaml`, 5 categories — matches the discharge axis's $\|T^G\|$, not admission's ($\|T^G\|=2$), so the admission-axis row is a coarser-vs-finer comparison) — **no axis segment**, shared by both axes | `aggregate_tables.*`, `aggregate_tables_label_list.tex` |
| `e1_label_list_strict_rep1`, `rep2` | Task C5 control companion, identical list under guided's assignment criterion — **no axis segment**, shared by both axes | `aggregate_tables.*`, `aggregate_tables_label_list.tex` |
| `e2_guided_axisadmission_pertA_remove_16_rep1`–`5` | Experiment 2A on admission: remove *Admission IC* (`16`), $k=5$ replicates. No non-degenerate merge exists on this axis — its Or point has only two children, so `merge_alternatives()` refuses (`run_e2` logs this and reports Perturbations A/C only) | `experiment2_axisadmission.json` |
| `e2_guided_axisadmission_pertC_distractor_5_112_rep1`–`5` | Experiment 2C on admission: add *Admission to High-Dependency Unit*, a prospectively named, plausible-but-unrealized ward category under Or `5`, $k=5$ replicates | `experiment2_axisadmission.json` |
| `e2_guided_axisdischarge_pertA_remove_21_rep1`–`5` | Experiment 2A on discharge: remove *Release E* (`21`), $k=5$ replicates | `experiment2_axisdischarge.json` |
| `e2_guided_axisdischarge_pertB_merge_17_18_rep1`–`5` | Experiment 2B on discharge: merge *Release A* (`17`) + *Release B* (`18`), $k=5$ replicates | `experiment2_axisdischarge.json` |
| `e2_guided_axisdischarge_pertC_distractor_6_112_rep1`–`5` | Experiment 2C on discharge: add *Release F*, a prospectively named, plausible-but-unrealized discharge code under Or `6` mirroring the log's own A-E lettering, $k=5$ replicates | `experiment2_axisdischarge.json` |

Freeze verification: `freeze_e1_axisadmission.md`/`.json`, `freeze_e1_axisdischarge.md`/`.json`,
`freeze_e2_axisadmission.md`/`.json`, `freeze_e2_axisdischarge.md`/`.json`. All pass every row as
of the 2026-08-31 re-run (`icpm2027_e1_guided_axisadmission_rep3`'s pipeline.log shows one
transient `litellm.ServiceUnavailableError` retried and recovered within the same run — not a
freeze failure, and the resulting `assignments.csv` is complete), and again as of the 2026-09-04
re-run under `protocol_version` 1.1.0 (every condition above, both axes, re-executed at
`assignment_batch_size=25`; the open arm's shared run was re-executed once and serves both axes as
before), again once `label_list`/`label_list_strict` and the `open_rep3`–`5` extension landed the
same day, and again once E2's perturbations were extended from one run each to $k=5$ replicates
plus Perturbation C on both axes, same day (2026-09-04, all under 1.1.0).

## BPIC 2019 (`data/output/bpic2019/`, axis: `matching_regime`)

Untouched by the 2026-08-31 axis/RQ2 fix — its goal model declares one Or frontier
(`4` → 3-way-after-GR / 3-way-before-GR / 2-way / consignment) and its E1 conditions already
shared one `prompt_assignment_batch.txt` hash, so nothing here needed re-running. Also untouched by
the 2026-09-04 batch-size-uniformity fix itself: BPIC 2019 was already at
`assignment_batch_size=25` (the value the other two logs now share), so that specific parameter
never changed. It was **not**, however, left alone for the rest of that day: `guided_rep1`/`rep2`
and `open_rep1`/`rep2` were re-executed under `protocol_version` 1.1.0 anyway (fresh LLM calls, not
merely re-stamped), to fix a genuine freeze-row failure once `label_list`/`label_list_strict`
(stamped 1.1.0 from the start, since they were authored that day) were compared against a
`guided` baseline still stamped 1.0.0. One accidental extra replicate (`guided_rep3`, from a
`replicates.unperturbed` bump meant for `open` alone catching `guided` too — `protocol.yaml`'s own
2026-09-04 note) was completed and kept rather than discarded, and `open` was extended to match at
three for symmetry with RTFM/Sepsis's guided=open=5, rather than leaving BPIC 2019 at an unequal
3-vs-5. **Re-running `guided` changed real numbers**, not just a version stamp: it picked up the
axis-root/frontier prompt block that did not exist when BPIC 2019's original guided pair ran (the
mechanism post-dates them; `paperICPM27.tex` §Setup), so the fresh `guided_rep1`–`3` are not
directly comparable to the discredited-numbers caveat below, and every BPIC 2019 number in the
paper that reads from `guided` (Tables setup/divergence/labellist, the `Item Category` comparison,
and the frontier-recovery discussion) was recomputed from these fresh runs, not the original pair.

| Run | Purpose | Result file |
|---|---|---|
| `base` | Steps 1-4 | — |
| `c12_guided_stability_rep1`–`5` | Task C12 — predates the axis-block mechanism, unchanged | `stability.json` |
| `e1_guided_rep1`, `rep2` | Experiment 1, guided arm — **re-executed 2026-09-04** under 1.1.0, now with the axis-block prompt | `experiment1.md` |
| `e1_guided_rep3` | Extra guided replicate, added 2026-09-04 (see note above); brings `guided` to $n=3$, matching `open`'s extension | `aggregate_tables.*` |
| `e1_guided_no_sample_rep1`, `rep2` | Task C11a ablation — predates the axis-block mechanism, unchanged | `aggregate_tables.*` (the per-dataset `experiment1.md` covers the guided/open pair only) |
| `e1_open_rep1`, `rep2` | Experiment 1, open arm — **re-executed 2026-09-04** under 1.1.0 (protocol-version parity with the refreshed `guided`, not a taxonomy-mechanism change: open reads no goal model) | `experiment1.md` |
| `e1_open_rep3` | Extra open replicate, added 2026-09-04; brings `open` to $n=3$ | `aggregate_tables.*` |
| `e1_label_list_rep1`, `rep2` | Task C5 control (`configs/label_lists/bpic2019.yaml`, 4 categories — matches $T^G$ exactly, the only one of the three logs where the control's cardinality is matched rather than approximate), added 2026-09-04 | `aggregate_tables.*`, `aggregate_tables_label_list.tex` |
| `e1_label_list_strict_rep1`, `rep2` | Task C5 control companion, added 2026-09-04 | `aggregate_tables.*`, `aggregate_tables_label_list.tex` |

Freeze verification: `freeze_e1.md`/`.json`. Passed 14/14 as of the 2026-09-04 re-run once `guided`
and `open` were both brought to `protocol_version` 1.1.0 and `n=3`; two intermediate invocations
that session failed the "Protocol version" and "Goal model" rows respectively before that (see
`preregistration.yaml`'s C5 third amendment) — neither wrote a paired report, so nothing
inconsistent was ever aggregated.

**No Experiment 2 on BPIC 2019** — by design, not omission: the perturbation study (§4 of the
paper) targets RTFM and Sepsis only; BPIC 2019's role is the large-scale/high-cardinality
replication and the held-out-label check below.

Additional artifact: `label_recovery.md` — Task C1's held-out `Item Category` agreement check
(`analysis/heldout.py`), independent of the E1/E2/C12 conditions above. Recomputed 2026-09-04
against all three `guided` replicates (`--conditions e1_guided_rep1,e1_guided_rep2,e1_guided_rep3`;
the default only covers two).

## `rtfm_mini` (`data/output/rtfm_mini/`) — illustrative fixture, not part of the frozen design

Not run through `run_experiment.py` at all; it's the 8-case fixture behind the paper's running
example (Table `tab:rtfm-mini`, Fig. `fig:rtfm-mini`) and Task C8's structural-vector-collapse
demonstration, run directly through the base pipeline.

Three timestamped directories, each a full Steps 1-9 execution:

- `20260917_192308/` — **the current one.** Gemini 3.5 Flash Lite, produced by the example script
  as it now stands. Its Step 9 merge is *delinquent payment* + *coercive credit collection*
  (ids 13 and 20, siblings under Or point 6).
- `20260831_064805/` — predates `check_axis_partition` (commit `b016cb9`, the same day). Its Step
  9 merge is *timely* + *delinquent payment*, ids 12 and 13, which sit under Or points 4 and 6
  respectively. The current code rejects that merge, so this run is not reproducible.
- `20260917_144500/` — the same fixture driven by Claude Fable 5.1 through the `manual/` provider;
  see its `PROVENANCE.md`. Not a Gemini run and not part of any reported result.

**Consequence for the paper.** The running-example text describes the *timely* + *delinquent
payment* merge, and `data/output/icpm2027_results/rtfm_mini/c8_boolean_vector_collapse.md` names
the category `resolve_via_timely_or_delinquent_payment` that merge produced. Neither is
reproducible: that merge combines alternatives under two different Or points, which the axis
check now rejects, and rightly — it is not a merge within one decomposition. C8's substance is
unaffected (V0003, V0007 and V0008 still share one activity vector and still land in one
category, `delinquent_payment` in round 1 of the current run), but the category name and the
running example's merge both need updating in the text. Result:
`data/output/icpm2027_results/rtfm_mini/c8_boolean_vector_collapse.md`.

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

The 2026-09-04 BPIC 2019 refresh (see that section above) is a second case of this kind, though
narrower: `e1_guided_rep1`/`rep2` and `e1_open_rep1`/`rep2` were overwritten in place via
`run_experiment.py --force`, not renamed and kept, so their pre-1.1.0 content (no axis-block
prompt for `guided`; `protocol_version` 1.0.0 for both) is not on disk either. It is in this repo's
git history at the same paths, and in `ICPM2027-GoalCat`'s history for every paper number that read
from them (Tables setup/divergence/labellist's BPIC 2019 rows, the `Item Category` comparison, and
the frontier-recovery count in §Discussion) before the commit that lands this refresh.

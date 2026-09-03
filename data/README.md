# Data

This directory holds the event logs, goal models, prompt templates, and generated pipeline output
that GoalCat operates on. See the [repository root README](../README.md) for the pipeline itself and
how to run it; this document covers two things specific to `data/`: the study cases available and
their references, and how to read a pipeline output-run directory under `data/output/`.

## Study cases

Each study case pairs one public event log (`data/logs/`) with an authored goal model
(`data/goals/`) — a GRL/URN declaration of what the process is for, authored from the organization's
published process documentation and frozen before any categorization runs against it. Every log
currently has a goal model in both its editable jUCMNav form (`.jucm`) and a rendered Markdown form
(`.md`). Only the `.jucm` is a pipeline input, and even it is never sent to an LLM verbatim: Step 5a
receives a task-scoped text projection of it — see "What the LLM actually sees of the goal model" in
[`../README.md`](../README.md). The `.md` form is documentation for human readers only.

| Log | Domain | Scale | Log file | Goal model | Status |
|---|---|---|---|---|---|
| RTFM (Road Traffic Fine Management Process) | Lifecycle of a road traffic fine, from issuance to closure, at an Italian local police force (*Polizia Locale*) | 150,370 cases, 561,470 events, 231 variants (Jan. 2000 – Jun. 2013) | `logs/rtfm.xes.gz` (+ `logs/rtfm_mini.xes.gz`, a 6-case fixture) | `goals/rtfm_goal_model.jucm` (+ `goals/rtfmGM_description.md`); the `rtfm_mini` fixture has its own structurally identical copy, `goals/rtfm_mini_goal_model.jucm` (+ `goals/rtfm_miniGM_description.md`) | Only log with a completed, accepted pipeline run through analyst review — see the `rtfm_mini` reference run in `output/rtfm_mini/`. The full log carries the ICPM 2027 Experiment 1 and 2 run set (five guided replicates, two open, two `guided_no_sample`, and the perturbations). |
| BPIC 2019 | Purchase-order handling across 60 subsidiaries of a multinational coatings-and-paints company | 251,734 cases, 1,595,923 events, 42 activities | `logs/bpic2019.xes.gz` | `goals/bpic2019_goal_model.jucm` (+ `goals/bpic2019GM_description.md`) | Main evaluation dataset. ICPM 2027 Experiment 1 complete (guided, open, and `guided_no_sample` arms, two replicates each), plus the Task C1 held-out label recovery against `case:Item Category`. Experiment 2's perturbations were scoped to RTFM and later extended to Sepsis (Task C6); this log carries none. |
| Sepsis | Hospital pathway of sepsis patients, recorded by the institution's ERP system | ~1,000 cases, ~15,000 events, 16 activities | `logs/sepsis.xes.gz` | `goals/sepsis_goal_model.jucm` (+ `goals/sepsisGM_description.md`) | Main evaluation dataset. ICPM 2027 Experiments 1 and 2 complete on both declared axes (admission, discharge). Note: an earlier report of Step 5a taxonomy-induction instability on this log **did not reproduce** — the Task C12 rerun (k=5), after a prompt defect was fixed, reproduces each axis's own anchor set with zero variance (`stability_axis*.json`); the live reproducibility question is Step 6 assignment variance, which the replicate ranges report. |

Publisher references (BibTeX):

```bibtex
@misc{deleoni2015rtfm,
  author       = {de Leoni, Massimiliano and Mannhardt, Felix},
  title        = {Road Traffic Fine Management Process},
  year         = {2015},
  publisher    = {4TU.ResearchData},
  doi          = {10.4121/uuid:270fd440-1057-4fb9-89a9-b699b47990f5}
}

@misc{vandongen2019bpic,
  author       = {van Dongen, Boudewijn F.},
  title        = {BPI Challenge 2019},
  year         = {2019},
  publisher    = {4TU.ResearchData},
  doi          = {10.4121/uuid:d06aff4b-79f0-45e6-8ec8-e19730c248f1}
}

@misc{mannhardt2016sepsis,
  author       = {Mannhardt, Felix},
  title        = {Sepsis Cases - Event Log},
  year         = {2016},
  publisher    = {4TU.ResearchData},
  doi          = {10.4121/uuid:915d2bfb-7e84-49ad-a286-dc35f063a460}
}
```

`data/templates/` holds the LLM prompt templates shared across logs (taxonomy induction, revision,
assignment, and the Step 9 review-decision schema) — these are prompt structure, not per-log content,
and apply uniformly regardless of which study case is running.

## Reading an output run directory

Every pipeline execution writes to its own timestamped directory,
`data/output/<log_stem>/<run_id>/` (e.g. `data/output/rtfm_mini/20260819_074233/`), where `<log_stem>`
matches the log's filename stem and `<run_id>` is a `YYYYMMDD_HHMMSS` timestamp assigned when the run
starts. A run directory has this shape:

```
<log_stem>/<run_id>/
├── run_config_snapshot.json   # the resolved PipelineConfig this run executed with
├── pipeline.log                # combined log for every step of this run
├── review_index.md             # human-facing index of Step 9 review reports, all rounds
├── 01_variants/variants.csv
├── 02_profiling/
│   ├── profiles.csv
│   └── profiles.json
├── 03_textualization/
│   ├── lupin_input.json        # per-variant profile handed to the vendored LUPIN subprocess
│   ├── lupin_output.json       # rendered narratives, as returned by that subprocess
│   └── narratives.csv
├── 04_sampling/narrative_sample.csv
├── round1/                     # Steps 5-9 for review round 1
│   ├── 05_taxonomy/            # taxonomy.json, taxonomy_prompt.txt, taxonomy_run_metadata.json
│   ├── 06_assignment/          # assignments.csv, assignment_report.md, *_distances.parquet, ...
│   │                              # (*_distances.parquet empty if skip_pairwise_distances=true)
│   ├── 07_discovery/           # discovery_metrics.csv, discovery_report.md, models/
│   │                              # (precision column NaN throughout if skip_precision=true)
│   ├── 07b_indicators/         # indicator_satisfaction.csv, goal_satisfaction.csv,
│   │                              # indicator_report.md, <goal_model>_measured.jucm
│   │                              # (absent if skip_indicators=true, or a no-op on a goal model
│   │                              #  whose indicators carry no measurement binding)
│   ├── 08_description/         # descriptions.csv, description_report.md, description_prompt.txt
│   └── 09_review/              # review_decisions.yaml (or *_processed_<ts>.yaml once acted on)
├── round2/                     # only present if round 1 was revised (merge/split at Step 9)
│   └── ...                     # same subdirectories as round1/
└── final/                      # only present once a round is accepted at Step 9
    ├── README.md                # this run's own summary of its accepted categories
    ├── taxonomy.json
    ├── assignments.csv          # copy of the accepted round's assignments.csv (variant_id ->
    │                              # category_id, distances, rationale) — kept here so other tools
    │                              # can re-filter/re-partition without the round dir surviving
    ├── pipeline_usage_summary.json
    └── sublogs/
        ├── <category_id>.xes.gz  # one per accepted category — the log, partitioned
        └── residual.xes.gz       # cases that fit no category
```

Notes on reading this structure:
- **Steps 1-4 run once** per run directory, shared by every review round — they do not depend on
  the taxonomy, so a revision (merge/split) never re-executes them.
- **`round<N>/` starts at 1** and a new round is added only when Step 9 records a merge or split
  decision; a rename decision is applied in place, with no LLM call and no new round. A run that was
  accepted on its first pass therefore has only `round1/` plus `final/`.
- **`models/` inside `07_discovery/`** holds the rendered Directly-Follows Graph per category for that
  round's reviewer. It is deleted once a round is accepted — the discovered models are directly
  regenerable from the accepted taxonomy and assignments, so `final/` does not duplicate them.
- **`final/` appearing at all** is itself the signal that a run reached an accepted outcome; a run
  still in progress, or abandoned mid-review, has only its numbered stages and `round<N>/`
  directories.
- The `final/README.md` inside each accepted run is auto-generated per run and describes that run's
  own accepted categories — it is a report on one execution, not project documentation.
- **`final/assignments.csv`** is a copy, not the source of truth — the accepted round's
  `round<N>/06_assignment/assignments.csv` remains the canonical copy. It is duplicated into
  `final/` purely so a self-contained `(taxonomy.json, assignments.csv)` pair is available to
  downstream tools without depending on the round directory still existing.
- **`07b_indicators/`** is Step 7b's output — optional (`skip_indicators`, default `false`) and a
  no-op on any goal model that does not bind its indicators to the log, which today is every model
  except RTFM's (both `rtfm_goal_model.jucm` and `rtfm_mini_goal_model.jucm`). Directory absent
  entirely, rather than present-and-empty, when the step did not run for a round.
- **`skip_precision`/`skip_pairwise_distances`** (opt-in config flags, both default `false` — see
  root README's "Resource usage" section) leave the corresponding output *files* in place but
  empty of the data they'd normally hold: `structural_distances.parquet`/`profile_distances.parquet`
  are written schema-valid but zero-row, and `discovery_metrics.csv`'s `precision` column is `NaN`
  for every category. `assignment_report.md`/`discovery_report.md` both note explicitly when this
  is why a section is empty, rather than leaving it ambiguous with a genuine timeout or singleton
  category.

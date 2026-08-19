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
(`.md`); see [`../project/OVERVIEW.md`](../project/OVERVIEW.md) (local, not tracked in git) for the
full architecture this data feeds.

| Log | Domain | Scale | Log file | Goal model | Status |
|---|---|---|---|---|---|
| RTFM (Road Traffic Fine Management Process) | Lifecycle of a road traffic fine, from issuance to closure, at an Italian local police force (*Polizia Locale*) | 150,370 cases, 561,470 events, 231 variants (Jan. 2000 – Jun. 2013) | `logs/rtfm.xes.gz` (+ `logs/rtfm_mini.xes.gz`, a 6-case fixture) | `goals/rtfm_goal_model.md` / `.jucm` | Only log with a completed, accepted pipeline run — see the `rtfm_mini` reference run in `output/rtfm_mini/`. The full log has been taken through intent-guided taxonomy induction and assignment (Step 5a → 6); see `project/PROGRESS.md` for how far the latest full-log run has progressed. |
| BPIC 2019 | Purchase-order handling across 60 subsidiaries of a multinational coatings-and-paints company | 251,734 cases, 1,595,923 events, 42 activities | `logs/bpic2019.xes.gz` | `goals/bpic2019_goal_model.md` / `.jucm` | Case-study driver and config staged (`src/goalcat/experimentation/bpic2019/`); not yet run end-to-end — Step 3 textualization requires a per-log template in `third_party/lupin/log_templates.py`, authored so far only for `rtfm`/`rtfm_mini`. |
| BPIC 2020 (Travel Permit Data) | Travel-permit requests and their approval chain at a university — one of five BPIC 2020 sub-logs, the only one staged here | 7,065 cases, 86,581 events (2017–2018) | `logs/bpic2020_permit.xes.gz` | `goals/bpic2020_goal_model.md` / `.jucm` (shared across BPIC 2020 sub-logs) | Case-study driver and config staged (`src/goalcat/experimentation/bpic2020_permit/`); same textualization-template gap as BPIC 2019. |
| Sepsis | Hospital pathway of sepsis patients, recorded by the institution's ERP system | ~1,000 cases, ~15,000 events, 16 activities | `logs/sepsis.xes.gz` | `goals/sepsis_goal_model.md` / `.jucm` | Case-study driver and config staged (`src/goalcat/experimentation/sepsis/`); same textualization-template gap. |

Publisher references (BibTeX, reused from `project/OVERVIEW.md`):

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

@misc{vandongen2020bpic,
  author       = {van Dongen, Boudewijn F.},
  title        = {BPI Challenge 2020: Travel Permit Data},
  year         = {2020},
  publisher    = {4TU.ResearchData},
  doi          = {10.4121/uuid:ea03d361-a7cd-4f5e-83d8-5fbdf0362550}
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
│   ├── 06_assignment/          # assignments.csv, assignment_report.md, *_distances.csv, ...
│   ├── 07_discovery/           # discovery_metrics.csv, discovery_report.md, models/
│   ├── 08_description/         # descriptions.csv, description_report.md, description_prompt.txt
│   └── 09_review/              # review_decisions.yaml (or *_processed_<ts>.yaml once acted on)
├── round2/                     # only present if round 1 was revised (merge/split at Step 9)
│   └── ...                     # same five subdirectories as round1/
└── final/                      # only present once a round is accepted at Step 9
    ├── README.md                # this run's own summary of its accepted categories
    ├── taxonomy.json
    ├── <category_id>.xes.gz     # one per accepted category — the log, partitioned
    ├── residual.xes.gz          # cases that fit no category
    └── ...
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

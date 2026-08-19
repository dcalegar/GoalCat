# GoalCat

GoalCat is a goal-driven process-variant categorization pipeline. Process discovery on real
event logs typically yields unreadable "spaghetti" models; the conventional fix clusters variants
on their structure first and attaches a business-meaning label afterward. GoalCat inverts that
order. A goal model (GRL/URN), authored from an organization's published process documentation and
frozen before any assignment runs, declares what the process is for; its decomposition into
alternative tasks *is* the taxonomy. Each process variant is rendered as a natural-language
narrative — preserving order, waiting times, rework, and outcome — and an LLM matches each narrative
against the goal model's declared alternatives rather than inventing categories from scratch. What
matches nothing is not discarded: it is reported as a residual, evidence that the declared goal
model does not yet cover something the process actually does. When no goal model can be authored for
a log, the same pipeline falls back to open taxonomy induction, proposing categories directly from
the narratives.

## Pipeline at a glance

| Step | Name | What it does |
|---|---|---|
| G | Goal model authoring (prerequisite) | The organization authors a GRL/URN goal model — goals, alternative tasks, actors — versioned and frozen before assignment. |
| 1 | Variant extraction | Groups traces of the event log that share the same activity sequence. |
| 2 | Multi-view profiling | Computes order, duration, rework, outcome, resource, and frequency per variant. |
| 3 | Textualization | Renders each variant's profile as a natural-language narrative (via the vendored LUPIN module). |
| 4 | Narrative sampling | Draws a representative subset (frequent, rare, extreme) to calibrate taxonomy granularity. |
| 5a / 5b | Taxonomy induction | An LLM subdivides the goal model's declared axis (5a, `intent_guided`) or proposes categories directly from the sample (5b, `open`), depending on `taxonomy_mode`. |
| 6 | Narrative assignment | An LLM assigns every narrative to a category, or leaves it in the residual. |
| 7 | Per-category discovery | Applies the Inductive Miner to each category and computes fitness/precision. |
| 8 | High-level description generation | Combines deterministic conformance metrics with one prose-generation prompt per category. |
| 9 | Business review | A human reviewer accepts, renames, merges, or splits categories; merge/split starts a new round through Steps 5-8. |

The two taxonomy-induction modes share every other step. With a goal model (`intent_guided`), the
residual is non-conforming behavior — evidence to revise the goal model. Without one (`open`), it is
the equivalent of clustering noise, reported as an "other/unclassifiable" bucket. Full architecture,
related-work positioning, and evaluation plan are documented in `project/OVERVIEW.md` (local,
gitignored — see [Further documentation](#further-documentation)).

## Repository structure

```
GoalCat/
├── LICENSE                # AGPL-3.0-or-later, matching pyproject.toml's declaration
├── pyproject.toml, requirements-lock.txt, .python-version
├── data/
│   ├── README.md          # study cases, references, how to read an output run — see below
│   ├── goals/               # one goal model per log (GRL/URN): <log>_goal_model.md (+ .jucm)
│   ├── logs/                 # XES.gz event logs: RTFM, BPIC 2019, BPIC 2020, Sepsis
│   ├── templates/            # LLM prompt templates, shared across logs
│   └── output/                # generated pipeline run artifacts, one dir per run
├── scripts/
│   └── setup_local_llm.sh # optional local Ollama backend bootstrap
├── src/
│   ├── goalcat/              # the pipeline library — core execution, no case-study or GUI code
│   │   ├── config.py, config.yaml, config_local.yaml   # PipelineConfig + default/local-LLM configs
│   │   ├── pipeline.py       # orchestrator: run_step1_variants ... run_step9_review
│   │   ├── discovery.py      # Step 7: per-category process discovery
│   │   ├── review.py          # Step 9: business review loop
│   │   ├── run_logging.py
│   │   ├── extraction/        # Steps 1-2: log I/O, variants, profiling, similarity
│   │   ├── narrative/          # Steps 3-4: textualization, sampling
│   │   └── llm/                 # Steps 5a/5b, 6, 8: LLM backend, taxonomy, assignment, description
│   └── gui/                   # local Streamlit GUI over the pipeline (imports goalcat) — see
│                               # "Running the GUI" below
├── experimentation/          # case-study drivers (imports goalcat) — see experimentation/README.md
│   ├── examples/               # one self-contained subdirectory per illustrative case study
│   │   ├── rtfm_mini/           # config_mini.yaml + example_run.py (6-case fixture)
│   │   ├── rtfm/                 # config_rtfm.yaml + example_run.py (full RTFM log)
│   │   ├── bpic2019/
│   │   ├── bpic2020_permit/
│   │   └── sepsis/
│   └── icpm2027/               # replication package for the ICPM 2027 paper (RQ1 protocol runs)
└── third_party/lupin/      # vendored CC BY-NC-SA 4.0 textualization module (subprocess-isolated)
```

`goalcat`, `gui`, and `experimentation` are three separate top-level Python packages —
`experimentation` and `gui` both import `goalcat` as a library, never the reverse. `goalcat` and
`gui` live under `src/`; `experimentation` lives at the repository root instead, since it only
consumes the pipeline and isn't part of the implemented core.

`project/` (deeper architecture/research documentation) and `.claude/` (assistant configuration) are
listed in `.gitignore` and are not part of the git repository — see
[Further documentation](#further-documentation).

## Installation

Requires Python `>=3.11` (`pyproject.toml`'s floor; `.python-version` pins the verified `3.14.6`).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[llm]"
```

Add `gui` to that extras list (`pip install -e ".[llm,gui]"`) to also install the local Streamlit
GUI — see [Running the GUI](#running-the-gui).

For exact reproducibility of the verified environment instead of resolving against
`pyproject.toml`'s version ranges, use the lockfile:

```bash
pip install -r requirements-lock.txt
```

GoalCat is licensed `AGPL-3.0-or-later` (see [LICENSE](LICENSE)) — inherited from its PM4Py
dependency, not an independent choice.

### LLM backend

Steps 5a/5b, 6, and 8 call an LLM through a provider-agnostic adapter
(`src/goalcat/llm/llm_backend.py`). Pick one of two backends; both work with the same pipeline code,
switched only by which config file you pass.

**Option A — hosted (default).** Export `GEMINI_API_KEY` in your shell profile (e.g.
`~/.bash_profile`) before running the pipeline. This key is deliberately **never** read from a file
inside the repository — no `.env` convention is used here. Default model:
`gemini/gemini-3.5-flash-lite`, configured in `src/goalcat/config.yaml`.

**Option B — local (Ollama), no API key or per-call cost.**

```bash
./scripts/setup_local_llm.sh
```

This installs Ollama via Homebrew, starts it as a background service, and pulls the pinned model
(`qwen2.5:3b`, verified on an Apple M3 with 8 GB unified memory). Every step is a no-op if already
done, so it is safe to re-run. Then point the pipeline at `src/goalcat/config_local.yaml` instead of
`config.yaml` to route the LLM steps through it. Local models can produce weaker categorization
judgments inside a still schema-valid response — spot-check Step 5/6 output against the hosted
baseline before relying on this beyond quick local iteration.

## Running the pipeline

There is no packaged CLI. `src/goalcat/pipeline.py` exposes each step as a library function —
`run_step1_variants()` through `run_step9_review()` — not a `__main__` entry point.

Each study case under `experimentation/examples/` is a self-contained, illustrative,
runnable example (its own config alongside its driver script), invoked as a module:

```bash
python -m experimentation.examples.rtfm_mini.example_run       # 6-case fixture, scripted rework round
python -m experimentation.examples.rtfm.example_run             # full RTFM log
python -m experimentation.examples.bpic2019.example_run
python -m experimentation.examples.bpic2020_permit.example_run
python -m experimentation.examples.sepsis.example_run
```

Each requires `GEMINI_API_KEY` (or `config_local.yaml` for the local backend) and makes real LLM
calls — billed ones, under the hosted backend.

The runs behind the ICPM 2027 paper's reported results live separately, under
`experimentation/icpm2027/` — see [`experimentation/README.md`](experimentation/README.md)
for the distinction and that subpackage's own README for its (currently scaffolded) layout.

For a custom run against any config, call the `run_stepN_*()` functions directly with a shared
`run_id`:

```python
from goalcat.config import new_run_id
from goalcat.pipeline import (
    run_step1_variants, run_step2_profiling, run_step3_textualization, run_step4_sampling,
    run_step5_taxonomy, run_step6_assignment, run_step7_discovery, run_step8_description,
    run_step9_review,
)

run_id = new_run_id()
run_step1_variants(run_id=run_id)
run_step2_profiling(run_id=run_id)
# ... run_step3_textualization() through run_step9_review(), same run_id=
```

against `src/goalcat/config.yaml` (the default) or any other `config_path=`.

## Running the GUI

`src/gui/` is a local Streamlit app over the same pipeline library — no YAML hand-editing, no
`review_decisions.yaml` hand-editing. Install its extra and launch it:

```bash
pip install -e ".[llm,gui]"
export GEMINI_API_KEY=...        # or the local Ollama backend — see "LLM backend" above
streamlit run src/gui/app.py
```

This opens `http://localhost:8501` in your browser. Everything runs on your machine — there is no
hosted/paid Streamlit service involved. Four pages, in the sidebar:

- **Nueva corrida** — pick a log (`data/logs/`) and goal model (`data/goals/`), a form pre-filled
  from the matching case study's config (or the top-level default) for everything else
  (`case_id_key`/`activity_key`/..., sample sizes, `taxonomy_mode`, LLM model/temperature/
  concurrency/rate-limit), and a button that launches Steps 1-8 with a live progress checklist and
  a `pipeline.log` tail — useful during Step 6/8, which can take several minutes against real LLM
  calls.
- **Resultados** — browse any past run's variants, profiles, narratives, taxonomy, per-category
  reports, discovered process models (DFG images + downloadable `.pnml`), and — once a round is
  accepted — the final partitioned `.xes.gz` logs.
- **Revisión** — the Step 9 business review, without touching `review_decisions.yaml` directly:
  per category, keep / rename / merge / split, backed by the same `ReviewDecisions` validation the
  library already enforces.
- **Historial** — every run under `data/output/`, with its round count, latest status, and config
  summary, with a shortcut into Resultados/Revisión for any of them.

Each run/round the GUI launches executes in its own subprocess (`python -m gui.worker`), not
inside the Streamlit process itself — `goalcat.run_logging.get_logger()` caches its file handler
per process, so a long-lived GUI session launching many runs needs one fresh process per run to
give each its own `pipeline.log`. See `src/gui/run_control.py`'s module docstring for the full
rationale.

## Data

Four public event logs (RTFM, BPIC 2019, BPIC 2020 Travel Permit, Sepsis) live in `data/logs/`, each
paired with an authored goal model in `data/goals/`. See [`data/README.md`](data/README.md) for the
full study-case writeup with publisher references, and for how to read a pipeline output-run
directory under `data/output/`.

## License and third-party components

GoalCat is licensed `AGPL-3.0-or-later` — see [LICENSE](LICENSE). The vendored
`third_party/lupin/` module (textualization) is reused from LUPIN (Pasquadibisceglie, Appice &
Malerba, 2024) under CC BY-NC-SA 4.0, isolated from the rest of the codebase via `subprocess`
invocation only; see [`third_party/lupin/README.md`](third_party/lupin/README.md) for the full
isolation contract. Its NonCommercial term is satisfied by this project's non-commercial research
scope.

## Further documentation

Deeper architecture, research framing, and an implementation decision log — `OVERVIEW.md`,
`SETUP.md`, `PROGRESS.md` — live in a local `project/` directory that is listed in `.gitignore` and
is not part of the git repository. Ask the project maintainer for access if you need it.

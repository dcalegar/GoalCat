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
| 7b | Indicator satisfaction *(optional)* | Measures each goal-model KPI indicator over each category's sublog, converts it through the indicator's own `KPIEvalValueSet`, and propagates the result up the goal model. Deterministic; a no-op unless the goal model binds its indicators to the log. |
| 8 | High-level description generation | Combines deterministic conformance metrics with one prose-generation prompt per category. Cites Step 7b's measurements when that step ran. |
| 9 | Business review | A human reviewer accepts, renames, merges, or splits categories; merge/split starts a new round through Steps 5-8. |

**On the lettered steps.** The two letters mean different things, deliberately:

- **5a / 5b are mutually exclusive modes** of one step. `taxonomy_mode` selects exactly one; they never both run. They are not two steps and are not numbered as such, because doing so would assert a sequence that does not exist.
- **7b is a sequential, optional step.** It runs after 7 and before 8 — Step 8 reads its output — but the pipeline is complete without it, and it is a no-op on any goal model that does not bind its indicators to the log. The letter marks it as an insertion rather than a renumbering: the architecture's claim is nine steps, and 7b is an enrichment of that architecture, not a tenth stage of it.

The two taxonomy-induction modes share every other step. With a goal model (`intent_guided`), the
residual is non-conforming behavior — evidence to revise the goal model. Without one (`open`), it is
the equivalent of clustering noise, reported as an "other/unclassifiable" bucket. Full architecture,
related-work positioning, and evaluation plan are documented in `project/OVERVIEW.md` (local,
gitignored — see [Further documentation](#further-documentation)).

## What the LLM actually sees of the goal model

The `.jucm` file is jUCMNav's XMI serialization: it interleaves the GRL specification with a diagram
layer (`urndef`, `refs`/`contRef`, x/y coordinates), KPI indicators, and file provenance. That file
is never sent to an LLM, and neither is the prose `<log>GM_description.md`. A single function —
`goalcat.grl.render_excerpt()` ([`src/goalcat/grl/prompt.py`](src/goalcat/grl/prompt.py)) — renders a
task-scoped plain-text projection of the parsed model, and that projection is the only place a
prompt ever states the goal model. It is substituted into Step 5a's induction and revision prompts
(`{goal_model_excerpt}`); no later step re-sends the model. Step 6's assignment prompt carries the
induced categories alone, and Step 8's description prompt carries only the deterministically
resolved anchor labels of `grl.resolve_anchor_labels()` (`id (type): name`), never an LLM's
restatement of what the model says.

The RTFM goal model renders as follows (abridged; `data/goals/rtfm_goal_model.jucm` is 19 KB of
XMI, the full excerpt 52 lines):

```
Goal model: RTFM Goal Model

Actors:
  - id=1: Traffic Police Back-Office

Goal-task decomposition (id, type, name, decomposition operator; indentation = parent/child):
- id=2 [Goal] Every issued fine reaches a lawful, documented closure (AND)
  - id=3 [Goal] Fine is issued and formally communicated (AND)
    - id=8 [Task] Create Fine (leaf)
    - id=9 [Task] Send Fine (leaf)
  - id=4 [Goal] Fine case is resolved (OR)
    - id=12 [Task] Resolve via timely payment (leaf)
    - id=5 [Goal] Fine becomes enforceable and is resolved (AND)
      - id=10 [Task] Insert Fine Notification (leaf)
    …

Indicators (how the organization measures whether a goal is met; id, name, unit, and the value set converting a measurement to satisfaction):
  - id=112 [Indicator] Time to fine dispatch (days) (target 30, threshold 90, worst 360 days) [provenance: statutory]
  - id=114 [Indicator] Average time to case closure (days) (target 150, threshold 180, worst 365 days) [provenance: external-by-analogy]
  …

Softgoals and contribution links (source -> effect on softgoal):
  - id=12 Resolve via timely payment --[Make (+100)]--> Maximize timely fine revenue
  - id=20 Resolve via coercive credit collection --[Hurt (-50)]--> Minimize administrative & enforcement cost
  …
```

| Aspect | `.jucm` (XMI) | Rendered excerpt |
|---|---|---|
| Decomposition | flat list of `<links xsi:type="grl:Decomposition" src="…" dest="…"/>` | indented parent/child tree |
| Decomposition operator | `decompositionType` on the *parent* element, stored apart from the links | printed inline per node as `(AND)`/`(OR)`/`(XOR)`/`(leaf)` |
| Contribution links | `contribution="Help" quantitativeContribution="50"` attributes | `--[Help (+50)]-->` with the target softgoal resolved by name |
| Element ids | present | preserved verbatim, shown as `id=12` next to each name |
| Diagram layer | `urndef`, `refs`, `contRef`, coordinates, `ActorRef`, `IntentionalElementRef` | omitted |
| KPIs | `grl.kpimodel:Indicator` elements, their `groups`, and their `KPIEvalValueSet` | name, unit, `target`/`threshold`/`worst` and provenance rendered; the `goalcat:from`/`goalcat:to` activity-label binding **never** rendered |
| Provenance | `author`, `created`, `modified`, `nextGlobalID` | omitted |

The projection is a semantic subset chosen for the task, not a summary written for readability. Four
reasons drive it:

- **The prompts' decision rules depend on structure the XMI does not present directly.**
  `prompt_taxonomy_intent_guided.txt` instructs the model to "check the AND/OR/XOR operators shown in
  the decomposition — never combine alternatives the goal model marks XOR". Recovering that from XMI
  requires joining `intElements[@decompositionType]` against `links[@src]` and reconstructing
  parenthood transitively; delegating that reconstruction to the LLM would put the intent-guided
  condition's central constraint at the mercy of a graph-traversal error.
- **Identifier grounding stays mechanically checkable.** Every proposed category must carry
  `anchor_ids` referencing native `.jucm` element ids; the excerpt shows each id beside its name, and
  `grl.grounding_problems()` validates the returned ids against `grl.declared_ids()`. The mnemonic
  codes used in the prose descriptions (`G0`, `TP`, …) are prose-only and are not part of the model,
  so rendering the prose form instead would invite unresolvable anchors.
- **Everything omitted is irrelevant to the task.** Layout is presentation and file provenance is
  metadata. Indicators were omitted on the same grounds until 2026-08-25, reasoning that they "are
  not an axis to subdivide" — true, but that conflated *anchoring to* an element with *reasoning
  from* it. They are now rendered as context, and both intent-guided prompts state the rule
  `grl.declared_ids()` enforces: an indicator measures whether a goal is achieved, so a category
  anchors to that goal, never to the measurement.

  One carve-out survives, and it is a hard constraint rather than a budget decision: the indicator's
  `goalcat:from`/`goalcat:to` measurement binding is **never** rendered. Those values are activity
  labels, and every goal model's §7 forbids the activity-label table from reaching Steps 5a/6, since
  categorization there must be semantic rather than a lexical pre-match. The conversion arithmetic
  is declared intent and belongs in the prompt; the label binding is a measurement mechanism and
  stays in Step 7b.
- **Determinism, required by the experimental protocol.** `render_excerpt()` iterates in the `.jucm`
  file's own element order, so a frozen goal model always renders byte-identical prompt text — the
  "Prompts: versioned" requirement of the freeze table (`project/EXPERIMENTATION_PLAN.md` §2.2,
  local and gitignored — see [Further documentation](#further-documentation)).
  `experimentation/icpm2027/goalmodel/perturb.py` hashes exactly this text as the provenance record
  for perturbation conditions.

Two properties of the model are not carried into the excerpt, neither of which affects the goal
models currently in `data/goals/`:

- **Element-to-actor membership.** Actors are listed, but the excerpt does not state which elements
  belong to which actor. All five goal models declare exactly one actor and carry no element-level
  `actor` attribute in `grlspec` (ownership exists only in the diagram layer), so nothing is lost
  today; a multi-actor goal model would need this rendered.
- **Softgoals with no incoming contribution link** are never printed, since the softgoal block is
  emitted only when both softgoals and contribution links exist and it iterates the links. No goal
  model in `data/goals/` has one.

## What the LLM actually sees of a narrative

Each variant's narrative — the object Step 5a/5b/6 actually read — is rendered by the vendored
LUPIN module (`third_party/lupin/`, [`log_templates.py`](third_party/lupin/log_templates.py)) as a
sequence of `activity (+waiting)` clauses, e.g. `Create Fine, Send Fine (+90d), Insert Fine
Notification (+15d), ...`, followed by a `rework_summary` clause when the variant repeats an
activity. This is a compact rendering, adopted 2026-08-25 as the pipeline's single default,
superseding an earlier form that spelled out each wait as its own sentence (`", 7776000 seconds
after the previous step."`) and repeated the header's frequency/duration/outcome fields a second
time in prose. `_format_waiting_display()`
([`src/goalcat/extraction/profiling.py`](src/goalcat/extraction/profiling.py)) computes the
human-scale suffix (`+90d`, `+3h`, `+45m`, `+12s`, or nothing for the always-zero-wait first
event); the vendored module only lays it out, keeping unit conversion out of the CC BY-NC-SA-licensed
`third_party/` boundary.

Measured directly on the five committed Step 5a prompts, the compact form cuts the narrative block
by 32–60% (largest on sepsis and bpic2019, where per-event wait clauses — not the header
restatement — dominate token count). Verified end to end on three logs (`rtfm_mini`, `rtfm`,
`sepsis`) by re-running the full pipeline before and after the change at `temperature=0`: fitness
and precision were unchanged throughout, and the induced taxonomies and Step 6 partitions matched
within the same run-to-run variance observed between two identical-format reruns — this rendering
change is not a confound on the categorization results reported elsewhere. One reproducible,
narrower effect surfaced on `rtfm_mini`: an `anchor_ids` citation for one category shifted from a
mandatory AND-decomposition parent's full child list to the parent alone, which is arguably the
more correct citation and affects only the reviewer-facing "goal-model linkage" line in the
generated reports, not Step 6's assignment or Step 7's discovered models.

That same comparison surfaced a separate, pre-existing issue worth stating plainly: Step 5a's
taxonomy induction is not reproducible on the Sepsis log at `temperature=0` — two runs with
byte-identical prompts induced structurally different taxonomies (15 leaf-level categories in one
run, 4 coarse top-level categories in the other). This is independent of the narrative-rendering
change above; it is a property of the LLM call itself on that log.

## Repository structure

```
GoalCat/
├── LICENSE                # AGPL-3.0-or-later, matching pyproject.toml's declaration
├── pyproject.toml, requirements-lock.txt, .python-version
├── data/
│   ├── README.md          # study cases, references, how to read an output run — see below
│   ├── goals/               # one goal model per log (GRL/URN): <log>_goal_model.jucm — the sole
│   │                          # pipeline input; <log>GM_description.md is documentation only
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
│   │   ├── indicators.py     # Step 7b (optional): measured goal satisfaction per category
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

**Throughput tuning (`llm:` block, hosted backend only).** Four knobs control call volume and
pacing for Steps 5/6/8; every config under `src/goalcat/` and `experimentation/examples/*/` sets
them the same way, so change them together if you change them at all:

| Key | Current value | Meaning |
|---|---|---|
| `concurrency` | `5` | Parallel in-flight LLM calls. |
| `requests_per_minute` | `null` | Proactive request pacing; `null` disables it and relies on litellm's own retry backoff to absorb the rare `429`. |
| `assignment_batch_size` | `50` | Narratives per Step 6 call — e.g. a 231-variant run costs ~5 calls instead of 231. Larger batches trade away per-narrative failure isolation: a failed/invalid batch response leaves every narrative in it pending, retried on the next call against the same `run_id`. |
| `max_retries` | `3` | litellm retries per call before failing the batch. |

These values assume Gemini's **paid tier** is active on the Google AI Studio project behind
`GEMINI_API_KEY` (aistudio.google.com — billing is an account action, done outside this repo).
Verified paid-tier limits as of 2026-08-19: **4,000 RPM / 4M TPM** for both
`gemini-2.5-flash-lite` and `gemini-3.5-flash-lite`, plus a **150K RPD** cap specific to
`gemini-3.5-flash-lite` — check aistudio.google.com/rate-limit for the current numbers on your own
account rather than assuming these hold. On the **free tier**, `gemini-3.5-flash-lite` is capped
at 15 requests/minute; at that cap, set `concurrency: 1` and `requests_per_minute: 12` (per-call
latency alone is faster than 15/min, so concurrency=1 without pacing still overruns it) to avoid
`RateLimitError`.

Gemini Batch is not an option here: litellm's `create_batch` only routes Google calls through
`custom_llm_provider="vertex_ai"` (a separate GCP project/billing/quota from the `gemini` provider
these configs use), so switching provider families just for batching was judged not worth it.

**Cost tracking.** Google AI Studio's own GUI (and the linked GCP Billing console) only reports
aggregate spend per project/day — it cannot attribute cost to a specific run or pipeline step. Every
LLM call already records exact token counts in its `*_run_metadata.json` (`RunMetadata.input_tokens`
/ `output_tokens`, read from the provider's response, not estimated). The `llm.pricing_usd_per_million_tokens`
map in each config (keyed by the same model string as `taxonomy_model`/`assignment_model`/
`description_model`) turns those into an `estimated_cost_usd` per call —
`taxonomy_run_metadata.json` and `description_run_metadata.json` each carry one, and
`assignment_run_metadata.json` carries one per batch call plus a `total_estimated_cost_usd`. A model
absent from the map logs `estimated_cost_usd: null` rather than a fabricated `0.0`. Rates are USD per
1M tokens, standard (non-batch) tier; re-check `ai.google.dev/gemini-api/docs/pricing` before trusting
these figures for a paper's cost accounting if a run postdates the "Verified" date next to the map in
`config.yaml` by long enough for pricing to have moved. Every call's `RunMetadata` also carries
`prompt_chars`/`response_chars` (`len()` of the rendered prompt / raw response — a tokenizer-
independent size measure, since the same text tokenizes to different counts depending on language,
content, and model family) alongside `latency_seconds`.

**Usage rollups (`src/goalcat/llm/usage_summary.py`).** Individual `*_run_metadata.json` files are
per-call/per-step; two coarser views combine them for reporting:

- **Per round** — `roundN/round_usage_summary.json`, written every time Step 9 runs against that
  round (awaiting-review or accept alike), combining whichever of Steps 5/6/8 already ran in it.
- **Per execution** — `final/pipeline_usage_summary.json`, written once at accept time
  (`review.finalize_run`), combining every round of the run (a revision chain may span several).
  This is the one place the *whole run's* cost/latency/token/char total lives; `pipeline.log` gets
  a matching one-line summary at the same point, pointing at this file rather than duplicating its
  detail.

Both files nest per-step (round summary) or per-round (execution summary) breakdowns under a
`totals` key with the same shape: `call_count`, `total_input_tokens`, `total_output_tokens`,
`total_prompt_chars`, `total_response_chars`, `total_latency_seconds`, `total_estimated_cost_usd`
(`null` if any included call's cost is unknown, never a misleading `0.0`).

## Resource usage

Two pipeline outputs do not scale linearly with log size and are worth planning disk/memory
around before a large run.

**Memory.** Every step logs its peak resident set size (RSS) so far to `pipeline.log`
(`log_peak_memory()` in `src/goalcat/run_logging.py`), normalized to MiB regardless of platform.
It is a running maximum since process start, not a per-step delta — read it as "how big has this
process gotten by now," and look at which step's line shows the jump to identify the driver.

**Disk — `structural_distances.parquet` / `profile_distances.parquet`.** Step 6's pairwise
variant-distance files (`src/goalcat/extraction/similarity.py`) are the only pipeline artifacts
computed over every variant *pair* (`n(n-1)/2`) rather than once per variant — every other
CSV/JSON in the run scales linearly with variant, case, or narrative count instead. They are
written as Parquet, not CSV: `_pair_frame()`'s `variant_id_a`/`variant_id_b` columns are already
`pd.Categorical` in memory (dictionary-encoded to avoid duplicating each id string once per pair),
and Parquet preserves that dictionary encoding on disk instead of re-expanding it into ASCII text
the way `to_csv()` did — measured on the datasets below, this alone cuts the combined
structural+profile file size to roughly a third of the equivalent CSV (individual files range
wider, from ~6% for `structural_distances`'s single int32 column down to ~46% for
`profile_distances`'s four float32 columns, where there is less redundant-string encoding to
recover), and both write (Step 6) and read (Step 9's re-render) are faster too, since neither has
to format/parse float32 values as text. In practice:

| Dataset | Variants | Combined distance-file size (Parquet) | Equivalent CSV size |
|---|---|---|---|
| RTFM (mini fixture) | 6 | ~1 KB | ~1 KB |
| RTFM (full) | 231 | ~0.53 MB | ~1.5 MB (35%) |
| Sepsis | 846 | ~7.0 MB | ~20.7 MB (34%) |
| BPIC 2019 (full) | 11,973 | ~1.37 GB | ~4.18 GB (33%) |

Growth is quadratic, not linear, regardless of format: BPIC 2019's ~14x larger variant count than
Sepsis still produces a ~200x larger combined distance-file size. Budget disk accordingly before
running against a log with several thousand variants — doubling the variant count roughly
quadruples these two files. Full memory/timing/disk figures for all four runs above are reported
in the ICPM 2027 paper's Feasibility and runtime evaluation (predating the Parquet migration; that
paper's disk figures are the pre-migration CSV sizes shown above).

Existing run directories from before this change still have `structural_distances.csv`/
`profile_distances.csv`; convert them with `scripts/convert_distance_files_to_parquet.py` (verifies
each conversion by reading the Parquet back and comparing it against the source CSV before
deleting the CSV). New runs write `.parquet` directly.

These two files are **not safely deletable** once Step 6 finishes, in general: Step 9 re-reads
them from disk whenever a category rename triggers a report re-render
(`rerender_reports_after_rename()` in `src/goalcat/review.py`), without recomputing Step 6/7. Keep
them until a run's revision chain is fully accepted (`review.finalize_run`).

**`prune_pairwise_distances_on_finalize`** (`config.yaml` / GUI "New run" form, default `false`):
on accept, deletes both files from *every* round of the run, not just the accepted one — including
superseded rounds from earlier merge/split revisions. Trades traceability for disk: a superseded
round's copies are exactly what `rerender_reports_after_rename()` needs if that round is ever
re-reviewed with a rename, and there is no cheaper way to regenerate them than re-running Step 6's
full O(n²) computation. Leave this off unless disk pressure at BPIC-2019-like scale outweighs that
risk; the raw pairwise rows are unrecoverable once pruned, though the aggregate statistics they fed
into `assignment_report.md` remain. Set once per run — it cannot be changed mid-run without
tripping the config-drift check in `run_logging.py`.

**Compute — `skip_precision` / `skip_pairwise_distances`** (`config.yaml` / GUI "New Run" form's
"Performance" section, both default `false`): two independent opt-in flags that skip the pipeline's
two confirmed computational cost drivers, trading information for speed. Neither is automatic —
whether the tradeoff is worth it on a given run is a decision for the human reviewer/domain expert,
not the pipeline.

- `skip_indicators` turns off Step 7b, the optional measured-satisfaction step. Step 7b measures each
  goal-model indicator over each category's sublog, converts it through the indicator's own
  `KPIEvalValueSet`, and propagates the result up the goal model, writing `indicator_satisfaction.csv`,
  `goal_satisfaction.csv`, and a copy of the `.jucm` carrying one `EvaluationStrategy` per category —
  openable in jUCMNav. It is deterministic (no LLM call, no alignment computation) and cheap, and it is
  a no-op on a goal model whose indicators carry no `goalcat:*` measurement binding, which today means
  every model except RTFM's. `scripts/verify_kpi_evaluation.py` checks the conversion and propagation
  arithmetic against jUCMNav's reference behaviour.
- `skip_precision` skips Step 7's precision computation (`pm4py.precision_token_based_replay`), the
  only single-threaded, GIL-bound step in the pipeline — its cost scales with a category's unique
  *prefix* count, not its variant count (observed on BPIC 2019: one category's 6,082 variants
  produced 88,241 unique prefixes), and pm4py's own optional threading does not help (benchmarked:
  ~26s vs ~28s on a 500-variant slice). Fitness is still computed. `discovery_metrics.csv`'s
  `precision` column is `NaN` throughout, `discovery_report.md` notes it was skipped by config
  rather than timed out, and Step 9's automated low-precision review flag has nothing to flag.
- `skip_pairwise_distances` skips Step 6's structural/profile distance computation described above
  — `structural_distances.parquet`/`profile_distances.parquet` are still written (empty,
  schema-valid, so Step 9's rename re-render keeps working), but `assignment_report.md`'s
  per-category cohesion/divergence sections and `assignments.csv`'s nearest-neighbor columns carry
  no data for the round. Moot to also set `prune_pairwise_distances_on_finalize` in the same run —
  there is nothing left to prune.

Both are ordinary `PipelineConfig` fields: set once per run, and changing either mid-run trips the
same config-drift check as every other field.

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
for the distinction and that subpackage's own README for its module inventory and current status.

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
hosted/paid Streamlit service involved. Five pages, in the sidebar:

- **Setup** — check which LLM API key (`GEMINI_API_KEY`/`OPENAI_API_KEY`/`ANTHROPIC_API_KEY`) is
  already in the environment, or paste one in for the session (kept in the server process's memory
  only — never written to a file, per the "LLM backend" convention above).
- **New Run** — upload a new log/goal model if needed, pick a log (`data/logs/`) and goal model
  (`data/goals/`), a form pre-filled from the matching case study's config (or the top-level
  default) for everything else (`case_id_key`/`activity_key`/..., sample sizes, `taxonomy_mode`,
  a "Performance" section for `skip_precision`/`skip_pairwise_distances`/
  `prune_pairwise_distances_on_finalize` (see "Resource usage" above), LLM model/temperature/
  concurrency/rate-limit), and a button that launches Steps 1-8 with a live progress checklist, a
  stop control, and a `pipeline.log` tail — useful during Step 6/8, which can take several minutes
  against real LLM calls. Launching directly works with no further action; an optional "Inspect
  log" step (`src/goalcat/log_inspector.py`) sits in between for a form-and-inspect workflow
  instead:
  - Parses the log once — key validation, exact variant/prefix counts, a calibrated
    `skip_pairwise_distances` disk estimate, and Step 6's LLM call count/cost — before any run
    starts. Repeat inspections of the same log (same path/size/mtime and column keys) reuse the
    cached parse instead of re-reading the XES file.
  - Reports a *suggested* `skip_pairwise_distances` value from a disclosed, deliberately
    unvalidated heuristic threshold on the predicted disk estimate, and a descriptive-only signal
    for `skip_precision` against four reference logs (never a suggested boolean for that flag —
    its true per-category cost isn't computable before Step 6 runs). Nothing is applied on its
    own authority: an "Apply suggestion" button flips the `skip_pairwise_distances` checkbox only
    on explicit click.
  - If the log was inspected before "Run pipeline" was clicked, `log_inspection.json` (the
    report, the suggestion, and whether it was accepted) is written into the run directory
    alongside `gui_run_config.yaml` — a record of which of the two workflows produced this run,
    absent when the operator launched directly.
- **Results** — browse any past run's variants, profiles, narratives, taxonomy, per-category
  reports, discovered process models (DFG images + downloadable `.pnml`), Step 7b's indicator
  satisfaction (when that step ran — measured value, propagated softgoal scores, and a
  downloadable `.jucm` carrying one `EvaluationStrategy` per category, openable in jUCMNav),
  and — once a round is accepted — the final partitioned `.xes.gz` logs.
- **Review** — the Step 9 business review, without touching `review_decisions.yaml` directly: per
  category, keep / rename / merge / split, backed by the same `ReviewDecisions` validation the
  library already enforces.
- **History** — every run under `data/output/`, with its round count, latest status, and config
  summary, with a shortcut into Results/Review for any of them.

Each run/round the GUI launches executes in its own subprocess (`python -m gui.worker`), not
inside the Streamlit process itself — `goalcat.run_logging.get_logger()` caches its file handler
per process, so a long-lived GUI session launching many runs needs one fresh process per run to
give each its own `pipeline.log`. See `src/gui/run_control.py`'s module docstring for the full
rationale.

### Deploying the GUI as a shared web server (not currently supported)

The GUI above is designed and tested for a single local user only; hosting it on a public or
shared web server was not considered in its design and needs adaptation first:

- **No auth or session isolation.** `src/gui/run_control.py` and `src/gui/worker.py` distinguish
  concurrent runs only by `run_id`, not by requester identity — any visitor to a shared deployment
  could trigger runs, read another user's `data/output/`, or burn the host's LLM API budget.
- **Local-machine assumptions.** Runs are launched via `subprocess.Popen(..., cwd=REPO_ROOT)` and
  poll plain files (`gui_status.json`, `pipeline.log`) on the local filesystem. A host needs to
  both permit arbitrary subprocess spawning and persist `data/output/` across restarts/redeploys —
  ruling out fully managed/stateless Streamlit hosting.
- **Server-side secret handling.** `GEMINI_API_KEY` (see "LLM backend" above) would need to be
  injected as a server-side secret, never exposed to the client, with usage/cost controls if
  multiple untrusted users can trigger LLM-backed steps (5a/5b, 6, 8).

Adding these (containerized deployment with persistent storage, an auth layer, and per-user run
scoping/queueing in place of the bare subprocess model) is required before exposing this GUI beyond
a single trusted user.

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

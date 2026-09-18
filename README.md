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
the equivalent of clustering noise, reported as an "other/unclassifiable" bucket.

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
  file's own element order, so a frozen goal model always renders byte-identical prompt text — a
  "Prompts: versioned" requirement of the replication package's freeze table.
  `experimentation/icpm2027/goalmodel/perturb.py` hashes exactly this text as the provenance record
  for perturbation conditions.

Two properties of the model are not carried into the excerpt, neither of which affects the goal
models currently in `data/goals/`:

- **Element-to-actor membership.** Actors are listed, but the excerpt does not state which elements
  belong to which actor. All four goal models declare exactly one actor and carry no element-level
  `actor` attribute in `grlspec` (ownership exists only in the diagram layer), so nothing is lost
  today; a multi-actor goal model would need this rendered.
- **Softgoals with no incoming contribution link** are never printed, since the softgoal block is
  emitted only when both softgoals and contribution links exist and it iterates the links. No goal
  model in `data/goals/` has one.

## What the LLM actually sees of a narrative

Each variant's narrative — the object Steps 5a/5b/6 read — is rendered by the vendored LUPIN
module ([`third_party/lupin/log_templates.py`](third_party/lupin/log_templates.py)) as a sequence of
`activity (+waiting)` clauses, followed by a `rework_summary` clause when the variant repeats an
activity:

```
Create Fine, Send Fine (+90d), Insert Fine Notification (+15d), ...
```

`_format_waiting_display()` ([`src/goalcat/extraction/profiling.py`](src/goalcat/extraction/profiling.py))
computes the human-scale suffix (`+90d`, `+3h`, `+45m`, `+12s`, or nothing for the first event);
the vendored module only lays it out, which keeps unit conversion outside the CC BY-NC-SA
`third_party/` boundary.

This compact form replaced, on 2026-08-25, a verbose one that spelled out each wait as its own
sentence (`", 7776000 seconds after the previous step."`) and restated the header's
frequency/duration/outcome fields in prose. On the committed Step 5a prompts it shortens the
narrative block by 32–60% (most on Sepsis and BPIC 2019, where per-event wait clauses dominate).
Re-running `rtfm_mini`, `rtfm` and `sepsis` end to end before and after the change at
`temperature=0` left fitness and precision unchanged, and the induced taxonomies and Step 6
partitions differed only within the run-to-run variance of two identical-format reruns. The
rendering change is therefore not a confound on the categorization results. Its one reproducible
effect is narrower: on `rtfm_mini`, one category's `anchor_ids` moved from an AND parent's full
child list to the parent alone, which changes only the "goal-model linkage" line of the generated
reports, not Step 6 or Step 7.

That comparison also produced an apparent Step 5a instability on Sepsis (15 leaf-level categories
in one run, 4 top-level ones in the other, from byte-identical prompts). It did **not** survive the
later Task C12 check: after a prompt defect was fixed, k=5 identical-input reruns reproduced a
single anchor set on each of Sepsis's two axes
(`data/output/icpm2027_results/sepsis/stability_axis{admission,discharge}.json`). The remaining
reproducibility question is Step 6 assignment variance, which the replicate ranges report.

## Repository structure

```
GoalCat/
├── LICENSE                # AGPL-3.0-or-later, matching pyproject.toml's declaration
├── CITATION.cff           # software citation metadata (GitHub "Cite this repository", Zenodo)
├── pyproject.toml, requirements-lock.txt, .python-version
├── data/
│   ├── README.md          # study cases, references, how to read an output run — see below
│   ├── goals/             # one goal model per log (GRL/URN): <log>_goal_model.jucm — the sole
│   │                      #   pipeline input; <log>GM_description.md is documentation only;
│   │                      #   perturbed/ holds Experiment 2's generated variants
│   ├── logs/              # XES.gz event logs: RTFM (+ the rtfm_mini fixture), BPIC 2019, Sepsis
│   └── output/            # generated pipeline run artifacts, one dir per run
├── scripts/               # standalone utilities, none of them pipeline steps
│   ├── setup_local_llm.sh                 # optional local Ollama backend bootstrap
│   ├── convert_distance_files_to_parquet.py
│   ├── verify_kpi_evaluation.py           # checks Step 7b against jUCMNav's reference behaviour
│   └── aggregate_actor_satisfaction.py
├── src/
│   ├── goalcat/           # the pipeline library — core execution, no case-study or GUI code
│   │   ├── config.py, config.yaml, config_local.yaml  # PipelineConfig + default/local-LLM configs
│   │   ├── pipeline.py    # orchestrator: run_step1_variants ... run_step9_review
│   │   ├── discovery.py   # Step 7: per-category process discovery
│   │   ├── indicators.py  # Step 7b (optional): measured goal satisfaction per category
│   │   ├── review.py      # Step 9: business review loop
│   │   ├── log_inspector.py, run_logging.py, atomic_io.py
│   │   ├── templates/     # LLM prompt templates, shared across logs
│   │   ├── grl/           # GRL/URN goal models: .jucm I/O, the prompt excerpt, KPI evaluation
│   │   ├── extraction/    # Steps 1-2: log I/O, variants, profiling, similarity
│   │   ├── narrative/     # Steps 3-4: textualization, sampling
│   │   └── llm/           # Steps 5a/5b, 6, 8: LLM backend, taxonomy, assignment, description
│   └── gui/               # local Streamlit GUI over the pipeline (imports goalcat) — see
│                          #   "Running the GUI" below; gui/diagnostics.py explains a run's
│                          #   warnings and where it stopped
├── experimentation/       # case-study drivers (imports goalcat) — see experimentation/README.md
│   ├── examples/          # one self-contained subdirectory per illustrative case study
│   │   ├── rtfm_mini/     # config_mini.yaml + example_run.py (6-case fixture)
│   │   ├── rtfm/          # config_rtfm.yaml + example_run.py (full RTFM log)
│   │   ├── bpic2019/
│   │   └── sepsis/
│   └── icpm2027/          # replication package for the ICPM 2027 submission
├── tests/                 # test_icpm2027_regression.py — the rules the reported numbers rest on
└── third_party/
    ├── lupin/             # vendored CC BY-NC-SA 4.0 textualization module (subprocess-isolated)
    └── jucmnav/           # vendored EPL-1.0 GRL/URN .ecore schemas (read by grl/jucm_io.py)
```

`goalcat`, `gui`, and `experimentation` are separate top-level packages: `gui` and
`experimentation` import `goalcat`, never the reverse. `experimentation` sits at the repository
root rather than under `src/` because it consumes the pipeline without being part of it.

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

**Windows behind TLS-intercepting software** (antivirus web shields, corporate proxies). Verified
on 2026-09-17 on Windows 11 with Avast Web Shield: `import litellm` fails with
`SSL: CERTIFICATE_VERIFY_FAILED`, because `tiktoken` downloads an encoding on first import and the
interceptor re-signs the connection with a root CA that is in the Windows store but not in
`certifi`. Python 3.13+ also rejects that CA under its default `VERIFY_X509_STRICT` flag. `pip`
uses the system store, which is why installation succeeds and the import does not. The fix does
not touch the security software:

```bash
py -3.12 -m venv .venv                 # 3.12: VERIFY_X509_STRICT is not on by default
.venv/Scripts/python -m pip install -e ".[llm]" pip-system-certs
```

`pip-system-certs` makes `requests`/`urllib3` trust the Windows store. `scripts/setup_local_llm.sh`
is Homebrew-based; on Windows, install Ollama from its own installer.

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

**Option C — manual, no LLM at all.** A model string with the `manual/` prefix (e.g.
`taxonomy_model: "manual/reviewer"`) routes Step 5a/5b, 6, and 8 calls to the filesystem instead of
litellm, so that a person, or an external agent acting as the LLM, can drive the whole pipeline,
rework loop included, with no API key and no local model. Per call, in the directory named by
`GOALCAT_MANUAL_LLM_DIR`:

1. The adapter writes `<seq>_<prompt-hash>.prompt.txt` (the rendered prompt) and, for structured
   calls, `<seq>_<prompt-hash>.schema.json` (the pydantic JSON schema the reply must satisfy).
2. It polls every 2 s until a non-empty `<seq>_<prompt-hash>.response.txt` appears, for at most
   `GOALCAT_MANUAL_LLM_TIMEOUT_SECONDS` (default one hour; `0` waits indefinitely). The
   `llm.timeout_seconds` config knob does not apply here. An unanswered call fails naming the file
   it expected rather than hanging.
3. The reply passes through the same schema validation and retry loop as a model's; a malformed
   reply is re-requested as a new prompt file.

Set `concurrency: 1` so prompts arrive one at a time (Step 6 still batches
`assignment_batch_size` narratives per prompt). `RunMetadata` records `backend: manual`, `None`
token counts, and `null` for `estimated_cost_usd` and `temperature`, since nothing was metered or
sampled. The committed run `data/output/rtfm_mini/20260917_144500` was produced this way from
within Claude Code, with Claude Fable 5.1 writing every Step 5a/6/8 reply (see its
`PROVENANCE.md`). Its round 1 matched the Gemini run `20260831_064805` exactly (same five
categories, anchors, assignments, fitness and precision), differing only in category slugs and in
Step 8's prose.

**Throughput tuning (`llm:` block, hosted backend only).** Four knobs control call volume and
pacing for Steps 5/6/8. `src/goalcat/config.yaml` and every `experimentation/examples/*/` config
set them identically, so change them together if you change them at all:

| Key | Value in these configs | Meaning |
|---|---|---|
| `concurrency` | `5` | Parallel in-flight LLM calls. |
| `requests_per_minute` | `null` | Proactive request pacing; `null` disables it and relies on litellm's own retry backoff to absorb the rare `429`. |
| `assignment_batch_size` | `50` | Narratives per Step 6 call — a 231-variant run costs ~5 calls instead of 231. Larger batches trade away per-narrative failure isolation: a failed/invalid batch response leaves every narrative in it pending, retried on the next call against the same `run_id`. |
| `max_retries` | `3` | litellm retries per call before failing the batch. |

The ICPM 2027 replication package does **not** inherit these: its frozen protocol
(`experimentation/icpm2027/configs/protocol.yaml`, `protocol_version` 1.1.0) pins
`assignment_batch_size: 25` for all three datasets, because batch `50` timed out and aborted Step 6
at BPIC 2019's ~1,285-character mean narrative. `25` is the one value every log there tolerates,
adopted uniformly rather than as a per-dataset exception.

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

**Cost tracking.** Google AI Studio and the GCP Billing console report spend per project and day
only; they cannot attribute cost to a run or a step. GoalCat therefore records it per call. Each
`*_run_metadata.json` holds the provider-reported `input_tokens`/`output_tokens`, the
tokenizer-independent `prompt_chars`/`response_chars`, `latency_seconds`, and an
`estimated_cost_usd` computed from the config's `llm.pricing_usd_per_million_tokens` map (USD per
1M tokens, standard tier, keyed by model string). Step 6's `assignment_run_metadata.json` holds one
entry per batch plus a `total_estimated_cost_usd`. A model absent from the pricing map yields
`null`, never a fabricated `0.0`. The rates carry a "Verified" date in `config.yaml`; re-check
[ai.google.dev/gemini-api/docs/pricing](https://ai.google.dev/gemini-api/docs/pricing) before
using them for a publication's cost figures.

**Usage rollups** (`src/goalcat/llm/usage_summary.py`) aggregate those files at two levels:

| File | Written | Covers |
|---|---|---|
| `roundN/round_usage_summary.json` | every time Step 9 runs against the round | the Steps 5/6/8 calls made so far in that round |
| `final/pipeline_usage_summary.json` | once, at accept (`review.finalize_run`) | every round of the run — the only whole-run total |

Both share a `totals` shape: `call_count`, `total_input_tokens`, `total_output_tokens`,
`total_prompt_chars`, `total_response_chars`, `total_latency_seconds`, and
`total_estimated_cost_usd` (`null` if any included call's cost is unknown).

## Resource usage

Two pipeline outputs do not scale linearly with log size; plan disk and memory around them before
a large run.

**Memory.** Every step logs the process's peak resident set size (RSS) to `pipeline.log`
(`log_peak_memory()` in `src/goalcat/run_logging.py`), in MiB on every platform. The value is a
running maximum since process start, not a per-step delta: the step whose line shows the jump is
the driver.

**Disk — `structural_distances.parquet` / `profile_distances.parquet`.** Step 6's pairwise
variant-distance files (`src/goalcat/extraction/similarity.py`) are the only artifacts computed
over every variant *pair* (`n(n-1)/2`); every other file scales linearly with variant, case, or
narrative count. They are written as Parquet because it preserves the dictionary encoding of the
`pd.Categorical` id columns built by `_pair_frame()`, which CSV would expand into one string per
pair. The combined size is roughly a third of the CSV equivalent, and both writing (Step 6) and
reading (Step 9's re-render) are faster.

| Dataset | Variants | Combined distance files (Parquet) | CSV equivalent |
|---|---|---|---|
| RTFM (mini fixture) | 6 | ~1 KB | ~1 KB |
| RTFM (full) | 231 | ~0.53 MB | ~1.5 MB |
| Sepsis | 846 | ~7.0 MB | ~20.7 MB |
| BPIC 2019 (full) | 11,973 | ~1.37 GB | ~4.18 GB |

Growth is quadratic regardless of format: BPIC 2019 has ~14× Sepsis's variants and ~200× its
distance-file size, and doubling the variant count roughly quadruples both files. Run directories
from before the Parquet switch still hold `.csv` versions; `scripts/convert_distance_files_to_parquet.py`
converts them, reading each Parquet back and comparing it with the source before deleting the CSV.

Do not delete these files while a run is still under review: Step 9 re-reads them whenever a
rename triggers a report re-render (`rerender_reports_after_rename()` in `src/goalcat/review.py`),
without recomputing Step 6/7. Keep them until the run is accepted (`review.finalize_run`).

**Opt-in flags.** Four `PipelineConfig` fields (all default `false`, all also exposed in the GUI's
"New Run" form) trade information for speed or disk. None is applied automatically — whether the
trade-off is acceptable is the reviewer's decision. Like every other field, each is set once per
run; changing one mid-run trips the config-drift check in `run_logging.py`.

| Flag | Effect | What is lost |
|---|---|---|
| `skip_precision` | Skips Step 7's precision (`pm4py.precision_token_based_replay`), the only single-threaded, GIL-bound step. Its cost scales with a category's unique *prefix* count, not its variant count (on BPIC 2019, one category's 6,082 variants yielded 88,241 prefixes), and pm4py's optional threading does not help (~26 s vs ~28 s on a 500-variant slice). | `discovery_metrics.csv`'s `precision` is `NaN` throughout; Step 9's low-precision flag has nothing to flag. Fitness is still computed, and `discovery_report.md` states the skip. |
| `skip_pairwise_distances` | Skips Step 6's quadratic distance computation. Both files are still written, empty but schema-valid, so Step 9's rename re-render keeps working. | `assignment_report.md`'s cohesion/divergence sections and `assignments.csv`'s nearest-neighbor columns. |
| `prune_pairwise_distances_on_finalize` | On accept, deletes both distance files from *every* round, superseded ones included. Moot if `skip_pairwise_distances` is set. | The raw pairwise rows, which only a full O(n²) Step 6 re-run can regenerate; a later rename in a superseded round cannot re-render. The aggregates already in `assignment_report.md` remain. |
| `skip_indicators` | Turns off Step 7b. Not a cost lever: Step 7b is deterministic and cheap (see below). | `07b_indicators/` and Step 8's citations of measured satisfaction. |

Step 7b measures each goal-model indicator over each category's sublog, converts it through the
indicator's own `KPIEvalValueSet`, and propagates the result up the goal model, writing
`indicator_satisfaction.csv`, `goal_satisfaction.csv`, and a copy of the `.jucm` with one
`EvaluationStrategy` per category, openable in jUCMNav. It is a no-op on a goal model whose
indicators carry no `goalcat:*` measurement binding; all four goal models in `data/goals/` carry
one. `scripts/verify_kpi_evaluation.py` checks the conversion and propagation arithmetic against
jUCMNav's reference behaviour.

## Running the pipeline

There is no packaged CLI. `src/goalcat/pipeline.py` exposes each step as a library function,
`run_step1_variants()` through `run_step9_review()`.

### The example drivers

Each case study under `experimentation/examples/` pairs a config with an `example_run.py` driver,
run as a module from the repository root:

```bash
python -m experimentation.examples.rtfm_mini.example_run   # 6-case fixture, scripted rework round
python -m experimentation.examples.rtfm.example_run        # full RTFM log
python -m experimentation.examples.bpic2019.example_run
python -m experimentation.examples.sepsis.example_run
```

Each makes real LLM calls (billed ones, under the hosted backend) and needs one of the three
backends in [LLM backend](#llm-backend). Each runs Steps 1–8 and then plays the Step 9 reviewer
itself by writing `review_decisions.yaml`:

| Driver | Scripted Step 9 decision |
|---|---|
| `rtfm`, `sepsis`, `bpic2019` | `accept` on round 1 |
| `rtfm_mini` | `merge` on round 1 (exercising the revision path), then `accept` on round 2 |

The `rtfm_mini` merge is chosen by `_mergeable_pair()`: the first pair, in taxonomy order, whose
anchors are all siblings under one OR-decomposed parent. Step 5a's `check_axis_partition` rejects
any other merge (anchors under different decomposition points, or under an XOR point) and aborts
the revision round, and the LLM returns categories in arbitrary order, so the driver cannot simply
merge the first two. On the RTFM goal model the qualifying pair is the two enforcement closures
under id 6. If no pair qualifies, the driver fails with an explicit error.

**Reference run.** `data/output/rtfm_mini/20260917_192308` is this driver's output under the
current code: a Gemini run of Steps 1–9, accepted on round 2, 6 LLM calls, USD 0.0125. Its round-1
merge is `delinquent_payment` + `coercive_credit_collection` (ids 13 and 20). Two caveats before
citing it:

- In round 2, Step 6 assigned `V0001` (`Create Fine > Send Fine`, the fixture's deliberately
  still-open case, with no `Payment` event) to `timely_payment`, after correctly leaving it in the
  residual in round 1; its own rationale concedes that "the narrative ends with Send Fine". This is
  a Step 6 misassignment, recorded rather than re-rolled, since re-running until the residual
  survives would select a draw for its output. Cite round 1 when the residual path is the point;
  the paper's running example does, and round 1 reproduces its table on all eight rows.
- The other two committed `rtfm_mini` runs are kept for comparison, not as current output.
  `20260831_064805` predates the partition check (commit `b016cb9`) and merged ids 12 and 13, a
  merge the current code rejects, so its driver can no longer regenerate it. `20260917_144500` was
  produced through the `manual/` backend (see [LLM backend](#llm-backend)).

The ICPM 2027 replication runs are driven separately, by `experimentation/icpm2027/` — see
[`experimentation/README.md`](experimentation/README.md).

### A custom run

Call the step functions directly with a shared `run_id`, against `src/goalcat/config.yaml` (the
default) or any other `config_path`:

```python
from goalcat.config import new_run_id
from goalcat.pipeline import (
    run_step1_variants, run_step2_profiling, run_step3_textualization, run_step4_sampling,
    run_step5_taxonomy, run_step6_assignment, run_step7_discovery, run_step7b_indicators,
    run_step8_description, run_step9_review,
)

config_path = "src/goalcat/config.yaml"
run_id = new_run_id()
run_step1_variants(config_path, run_id)
run_step2_profiling(config_path, run_id)
run_step3_textualization(config_path, run_id)
run_step4_sampling(config_path, run_id)
run_step5_taxonomy(config_path, run_id)
run_step6_assignment(config_path, run_id)
run_step7_discovery(config_path, run_id)
run_step7b_indicators(config_path, run_id)   # optional; a no-op without an indicator binding
run_step8_description(config_path, run_id)
run_step9_review(config_path, run_id, 1)     # returns {"status": "awaiting_review", ...}
```

Step 9 acts only on a decision already on disk. The first call writes a template to
`round1/09_review/review_decisions.yaml` and returns `awaiting_review`. Set `decision: accept`, or
`decision: revise` with at least one rename, merge, or split filled in (the untouched template is
deliberately invalid, so nothing is accepted by default), then call `run_step9_review()` again. The
GUI's Review page writes the same file. A rename-only revision applies in place, returns
`renamed`, and writes a fresh template for the same round; a merge or split returns
`{"status": "revised", "round": 2}` after re-running Steps 5–8 under `round2/`, which is then
reviewed the same way.

### When a step cannot finish: `IncompleteAssignmentError`

Every variant must leave Step 6 with an outcome — a category or an explicit residual — or the
partition claim does not hold, which is why `review.finalize_run()` refuses to accept such a round.
That refusal is enforced as early as it is knowable: when an assignment batch is lost (an LLM call
exhausting `llm.max_retries` against a 429/503, or a response omitting variants), Step 6 saves what
it did assign and then raises `goalcat.pipeline.IncompleteAssignmentError` instead of returning a
partial assignment — so Steps 7, 7b and 8 never compute, or bill, against a partition Step 9 must
reject. Step 6 also refuses on entry if Step 3 left a profiled variant without a narrative, and
Step 7 re-checks the invariant, since it is often invoked on its own.

**Recovery: re-run Step 6 with the same `run_id`.** It resumes — the assignments already on disk
are kept and only the missing ones are sent to the LLM — then continue with Steps 7-9. The
exception subclasses `ValueError`, so a driver can retry on it precisely without catching
unrelated failures. The GUI's Diagnostics page reports the condition as a `blocking` warning.

## Running the GUI

`src/gui/` is a local Streamlit app over the same pipeline library, replacing hand-edited config
and `review_decisions.yaml` files with forms. Install its extra and launch it:

```bash
pip install -e ".[llm,gui]"
export GEMINI_API_KEY=...        # or the local Ollama backend — see "LLM backend" above
streamlit run src/gui/app.py
```

This opens `http://localhost:8501`; everything runs locally. The sidebar has six pages:

- **Setup** — check which LLM API key (`GEMINI_API_KEY`/`OPENAI_API_KEY`/`ANTHROPIC_API_KEY`) is
  already in the environment, or paste one in for the session (kept in the server process's memory
  only — never written to a file, per the "LLM backend" convention above).
- **New Run** — pick (or upload) a log from `data/logs/` and a goal model from `data/goals/`, adjust
  a form pre-filled from the matching case study's config (keys, sample sizes, `taxonomy_mode`,
  LLM settings, and a "Performance" section with the four opt-in flags of
  [Resource usage](#resource-usage)), and launch Steps 1–8 with a live progress checklist, a stop
  control, and a `pipeline.log` tail. An optional "Inspect log" panel
  (`src/goalcat/log_inspector.py`) parses the log once beforehand and reports key validity, exact
  variant/prefix counts, the predicted distance-file size, and Step 6's call count and cost. It
  *suggests* a `skip_pairwise_distances` value from a deliberately unvalidated disk threshold (and
  only a descriptive signal for `skip_precision`, whose cost is not computable before Step 6); the
  suggestion is applied only by clicking "Apply suggestion". When an inspection preceded the
  launch, `log_inspection.json` records it in the run directory beside `gui_run_config.yaml`.
- **Results** — browse any past run's variants, profiles, narratives, taxonomy, per-category
  reports, discovered process models (DFG images + downloadable `.pnml`), Step 7b's indicator
  satisfaction (when that step ran — measured value, propagated softgoal scores, and a
  downloadable `.jucm` carrying one `EvaluationStrategy` per category, openable in jUCMNav),
  and — once a round is accepted — the final partitioned `.xes.gz` logs.
- **Review** — the Step 9 business review, without touching `review_decisions.yaml` directly: per
  category, keep / rename / merge / split, backed by the same `ReviewDecisions` validation the
  library already enforces.
- **History** — every run under `data/output/`, with its reconstructed outcome, warning counts by
  severity, round count, latest status, and config summary, with a shortcut into
  Results/Review/Diagnostics for any of them.
- **Diagnostics** — where a run stopped and what its warnings mean: a step timeline plus every
  `WARNING`/`ERROR` in `pipeline.log`, grouped by kind, explained, and graded `blocking` (no round
  can be accepted), `quality` (a result is weaker than it looks), `transient` (a retried API
  hiccup), `benign`, or `unclassified`. It reads only the run directory, so it also covers runs
  launched outside the GUI, and it is the only page that can report a run that died before
  producing a round.

Each run the GUI launches executes in its own subprocess (`python -m gui.worker`), because
`goalcat.run_logging.get_logger()` caches its file handler per process and each run needs its own
`pipeline.log` (see `src/gui/run_control.py`).

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

Three public event logs (RTFM, BPIC 2019, Sepsis) live in `data/logs/`, each paired with an authored 
goal model in `data/goals/`. See [`data/README.md`](data/README.md) for the full study-case writeup 
with publisher references, and for how to read a pipeline output-run directory under `data/output/`.

## License and third-party components

GoalCat is licensed `AGPL-3.0-or-later` (see [LICENSE](LICENSE)), inherited from its PM4Py
dependency. The vendored
`third_party/lupin/` module (textualization) is reused from LUPIN (Pasquadibisceglie, Appice &
Malerba, 2024) under CC BY-NC-SA 4.0, isolated from the rest of the codebase via `subprocess`
invocation only; see [`third_party/lupin/README.md`](third_party/lupin/README.md) for the full
isolation contract. Its NonCommercial term is satisfied by this project's non-commercial research
scope. The vendored `third_party/jucmnav/` schemas (GRL/URN `.ecore` metamodel definitions, loaded
by `src/goalcat/grl/jucm_io.py` via `pyecore` to parse and serialize `.jucm` files against the real
schema) are reused from jUCMNav/jUCMNavPlus under the Eclipse Public License, version 1.0 — data
consumed at runtime, not executable code linked into GoalCat's own codebase; see
[`third_party/jucmnav/README.md`](third_party/jucmnav/README.md) for the full provenance and
license rationale.
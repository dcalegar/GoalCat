# third_party/lupin

Vendored component from LUPIN (Pasquadibisceglie, Appice & Malerba, 2024), reused directly
rather than reimplemented. See `project/OVERVIEW.md`, Tools, and NOTICE / LICENSE in this
directory.

## Source

https://github.com/vinspdb/LUPIN — `preprocessing/log_to_history.py` and
`utility/log_config.py`. License: CC BY-NC-SA 4.0.

## What is reused

Only the trace-to-narrative textualization mechanism: the Jinja2 `event_template` /
`trace_template` rendering loop in `log_to_history.py`'s `__gen_prefix_history` — for each
event in a case, render `event_template` with that event's attributes and append it to a
running text; render `trace_template` once with the case-level attributes and append it at
the end. LUPIN calls this once per prefix length (to train a suffix predictor on growing
histories); this project generalizes it to a single call over the complete variant.

Nothing from `neural_network/` (`llamp_multiout.py`, `llamp_multiout_wrapper.py`,
`HistoryDataset.py`), `main.py`, `eval_model.py`, or `explain_example.py` — LUPIN's
suffix-prediction model, its training loop, evaluation, and explainability code — is used.
This project has no suffix-prediction step.

## What is NOT reused

LUPIN's six per-dataset template strings in `log_config.py` (helpdesk, sepsis, bpic2020,
BPIC15_1, bpic2017_o, mip) do not match this project's event logs (`data/logs/`). This
project's own `event_template` / `trace_template` strings, one set per log, are original
content authored for its own attribute schema, following the same Jinja2 pattern.

## Isolation contract — read before touching this directory

- Code here MUST NOT be imported by `src/goalcat` or any other AGPL-3.0-licensed module in
  this repository. Importing merges this CC BY-NC-SA 4.0 code and the AGPL-3.0 codebase into
  one combined work, which cannot simultaneously satisfy both licenses' relicensing terms.
- The only permitted call boundary is `subprocess` invocation: the pipeline writes the
  input (a variant's multi-view profile) to a file, launches this directory's script as an
  independent process, and reads the rendered narrative back from a file or stdout. This
  keeps the two components under GPLv3 §5's aggregation exception (incorporated into
  AGPL-3.0) instead of forming a combined work.
- The adapted mechanism only needs `jinja2` — LUPIN's own `pandas`/`numpy`/`torch` dependencies
  were for raw-log feature extraction and ML tensors, neither of which is reused (Step 2 of the
  pipeline already produces everything `render_narratives.py` needs as plain JSON). `jinja2` is
  declared in the root `pyproject.toml` and installed in the shared `.venv` — not a separate
  environment — since the isolation that matters (no `import` of this directory's code into
  `src/goalcat`) is enforced by the subprocess-only call boundary above, not by venv separation.
- Non-commercial use only. CC BY-NC-SA 4.0's NonCommercial term is satisfied by this
  project's research-only scope (confirmed 2026-08-17). Any future commercial deployment
  must first remove or relicense this directory — see `project/OVERVIEW.md`, Tools.

## Status

`render_narratives.py` (the adapted rendering loop) and `log_templates.py` (this project's own
`event_template` / `trace_template` definitions) are implemented. Two template sets exist —
`_RTFM` (`rtfm`, `rtfm_mini`) and `_DEFAULT` (`sepsis`, `bpic2019`, `bpic2020_permit`), which keeps
a guarded `resource` clause for a future multi-actor goal model — since Step 2 profiling emits the
same event/trace attribute schema regardless of the source log, the difference is template wording
only, not per-dataset vocabulary. Invoked from `src/goalcat/narrative/textualization.py` via
`subprocess`, per the isolation contract above.

Waiting time is rendered as a compact inline suffix on the activity (e.g. `"Send Fine (+90d)"`),
computed by `src/goalcat/extraction/profiling.py::_format_waiting_display` and passed in as
`waiting_display` — adopted as the pipeline's single default narrative rendering (2026-08-25).

# `third_party/lupin`

Vendored component from LUPIN (Pasquadibisceglie, Appice & Malerba, 2024), reused rather than
reimplemented. See `NOTICE` and `LICENSE` in this directory.

## Source

<https://github.com/vinspdb/LUPIN>: `preprocessing/log_to_history.py` and `utility/log_config.py`.
License: CC BY-NC-SA 4.0.

## What is reused, and what is not

**Reused:** only the trace-to-narrative textualization mechanism, the Jinja2
`event_template`/`trace_template` loop in `log_to_history.py`'s `__gen_prefix_history`. For each
event of a case it renders `event_template` with the event's attributes and appends the result to
a running text; it then renders `trace_template` once with the case-level attributes and appends
it. LUPIN runs this once per prefix length, to train a suffix predictor on growing histories;
this project runs it once over the complete variant.

**Not reused:**

- LUPIN's suffix-prediction model, training, evaluation, and explainability code
  (`neural_network/`, `main.py`, `eval_model.py`, `explain_example.py`). This project has no
  suffix-prediction step.
- LUPIN's per-dataset template strings in `log_config.py`, which do not fit this project's logs.
  The templates in `log_templates.py` are original content following the same Jinja2 pattern.

## Isolation contract — read before touching this directory

- Code here **must not** be imported by `src/goalcat` or any other AGPL-3.0-licensed module in
  this repository. An import would merge this CC BY-NC-SA 4.0 code and the AGPL-3.0 codebase into
  one combined work, which cannot satisfy both licenses' relicensing terms at once.
- The only permitted call boundary is a subprocess. Step 3
  (`src/goalcat/narrative/textualization.py`) writes each variant's multi-view profile to
  `lupin_input.json`, runs `render_narratives.py` as an independent process, and reads the
  narratives back from `lupin_output.json`. This keeps the two components under the aggregation
  exception of GPLv3 §5 (incorporated into AGPL-3.0) instead of forming a combined work.
- The adapted mechanism needs only `jinja2`; LUPIN's `pandas`/`numpy`/`torch` dependencies served
  raw-log feature extraction and ML tensors, neither of which is reused. `jinja2` is declared in
  the root `pyproject.toml` and installed in the shared `.venv`: the isolation that matters is the
  subprocess boundary, not a separate environment.
- **Non-commercial use only.** CC BY-NC-SA 4.0's NonCommercial term is satisfied by this project's
  research-only scope (confirmed 2026-08-17). A commercial deployment must first remove or
  relicense this directory.

## Files

| File | Content |
|---|---|
| `render_narratives.py` | The adapted rendering loop |
| `log_templates.py` | This project's templates: `_RTFM` (for `rtfm`, `rtfm_mini`) and `_DEFAULT` (for `sepsis`, `bpic2019`) |

Step 2 emits the same attribute schema for every log, so the two template sets differ in wording
only. `_DEFAULT` keeps a guarded `resource` clause, silent on today's logs, for a future multi-actor
goal model. Waiting time arrives precomputed as `waiting_display` (e.g. `Send Fine (+90d)`), from
`_format_waiting_display()` in `src/goalcat/extraction/profiling.py`, so no unit conversion
happens inside this directory.

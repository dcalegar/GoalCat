# `experimentation`

Case-study drivers that run the `goalcat` pipeline library against a real event log. Both
subpackages import `goalcat`; `goalcat` never imports either of them. This package lives at the
repository root rather than under `src/`: it consumes the pipeline but is not part of the
implemented core, unlike `src/goalcat/` (the library) and `src/gui/` (a Streamlit app over it).

- **`examples/`** — one self-contained, runnable illustration per supported log (`rtfm_mini`,
  `rtfm`, `bpic2019`, `bpic2020_permit`, `sepsis`): a config file plus an `example_run.py` driver.
  These demonstrate that the pipeline executes end to end (including, for `rtfm_mini`, a scripted
  Step 9 rework round) and are the fastest way to exercise a change locally. They are not evidence
  for any research claim on their own.
- **`icpm2027/`** — the replication package for the ICPM 2027 submission: every run behind the
  paper's reported results, under a frozen, versioned experimental protocol. Distinct from
  `examples/` because the paper's runs must stay under explicit freeze/versioning conditions that
  an illustrative demo does not need, and because a reader reproducing the paper should not have
  to pick the right script out of a directory mixed with unrelated demos.

Invoke either as a module, from the repository root, e.g.:

```bash
python -m experimentation.examples.rtfm_mini.example_run
python -m experimentation.icpm2027.rtfm.guided_run   # once the icpm2027 protocol scripts exist
```

See the top-level [`README.md`](../README.md) for installation and LLM-backend setup.

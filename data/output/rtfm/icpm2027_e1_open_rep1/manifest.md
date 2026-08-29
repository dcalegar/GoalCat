# Run manifest — `e1_open_rep1`

Experiment `e1` · dataset `rtfm` · arm `open` · replicate 1

Protocol version `1.0.0` · steps [5, 6] · 2026-08-29T01:47:13.396800+00:00 → 2026-08-29T01:49:00.956117+00:00

## Inputs

| Element | Path | SHA-256 (first 16) |
|---|---|---|
| Event log | `data/logs/rtfm.xes.gz` | `dc9e0e65c964c8ce` |
| Goal model | *(absent by design — open arm)* | — |
| Condition config | `data/output/rtfm/icpm2027_e1_open_rep1/condition_config.yaml` | `c58b680ff1a03c9a` |

**Prompt templates:** `prompt_assignment_batch.txt`=`523c0b39823d`, `prompt_description.txt`=`7683ed3205c4`, `prompt_taxonomy_intent_guided.txt`=`c3fe7d89554d`, `prompt_taxonomy_intent_guided_revision.txt`=`604be767fe9c`, `prompt_taxonomy_open.txt`=`d32f3f34b809`, `prompt_taxonomy_open_revision.txt`=`cf4eefe924c8`

**Shared Steps 1-4 base:** "icpm2027_base" — `01_variants/variants.csv`=`a1d36af90468`, `02_profiling/profiles.csv`=`cdcc6d2f6946`, `02_profiling/profiles.json`=`8266af382b39`, `03_textualization/narratives.csv`=`57ceea507f36`, `04_sampling/narrative_sample.csv`=`3f5a257c7709`

## Variant scope

```json
{
  "policy": "all",
  "source": "configs/rtfm.yaml",
  "applied_policy": "all",
  "variants_total": 231,
  "variants_kept": 231,
  "cases_total": 150370,
  "cases_kept": 150370,
  "case_coverage_of_full_log": 1.0
}
```

## LLM

Seed: null — no seed is exposed by PipelineConfig.llm or by the Gemini path through litellm; temperature=0 is the only sampling constraint applied. See Task C2's replicate runs for the empirical noise floor.

```json
{
  "taxonomy": {
    "distinct_call_configurations": [
      {
        "model": "gemini/gemini-3.5-flash-lite",
        "resolved_model": null,
        "provider": "gemini",
        "backend": "remote",
        "temperature": 0.0
      }
    ],
    "call_count": 1
  },
  "assignment": {
    "distinct_call_configurations": [
      {
        "model": "gemini/gemini-3.5-flash-lite",
        "resolved_model": null,
        "provider": "gemini",
        "backend": "remote",
        "temperature": 0.0
      }
    ],
    "call_count": 5
  },
  "description": null
}
```

## Outputs

| Artifact | Path | SHA-256 (first 16) |
|---|---|---|
| taxonomy | `data/output/rtfm/icpm2027_e1_open_rep1/round1/05_taxonomy/taxonomy.json` | `c0150ec267751103` |
| assignments | `data/output/rtfm/icpm2027_e1_open_rep1/round1/06_assignment/assignments.csv` | `852312ecb377225b` |
| discovery_metrics | *(not produced)* | — |
| descriptions | *(not produced)* | — |

## Environment

`192.168.68.56` · macOS-26.5.2-arm64-arm-64bit-Mach-O · Python 3.14.6 · git `e46965fd78bf` **(working tree dirty)**

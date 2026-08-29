# Run manifest — `e1_guided_no_sample_rep2`

Experiment `e1` · dataset `rtfm` · arm `guided_no_sample` · replicate 2

Protocol version `1.0.0` · steps [5, 6] · 2026-08-29T02:08:08.374322+00:00 → 2026-08-29T02:12:09.000915+00:00

## Inputs

| Element | Path | SHA-256 (first 16) |
|---|---|---|
| Event log | `data/logs/rtfm.xes.gz` | `dc9e0e65c964c8ce` |
| Goal model | `data/goals/rtfm_goal_model.jucm` | `0b2a7ea87d75967f` |
| Condition config | `data/output/rtfm/icpm2027_e1_guided_no_sample_rep2/condition_config.yaml` | `b86b18864dace6fd` |

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
| taxonomy | `data/output/rtfm/icpm2027_e1_guided_no_sample_rep2/round1/05_taxonomy/taxonomy.json` | `119ef08bb1f12aee` |
| assignments | `data/output/rtfm/icpm2027_e1_guided_no_sample_rep2/round1/06_assignment/assignments.csv` | `25cf1b0846f0984d` |
| discovery_metrics | *(not produced)* | — |
| descriptions | *(not produced)* | — |

## Environment

`192.168.68.56` · macOS-26.5.2-arm64-arm-64bit-Mach-O · Python 3.14.6 · git `e46965fd78bf` **(working tree dirty)**

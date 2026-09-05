# Run manifest — `e2_guided_axisdischarge_pertC_distractor_6_112_rep5`

Experiment `e2` · dataset `sepsis` · arm `guided` · replicate 5 · tag `pertC_distractor_6_112`

Protocol version `1.1.0` · steps [5, 6] · 2026-09-04T23:21:36.114516+00:00 → 2026-09-04T23:22:10.178076+00:00

## Inputs

| Element | Path | SHA-256 (first 16) |
|---|---|---|
| Event log | `data/logs/sepsis.xes.gz` | `709c523403064159` |
| Goal model | `data/goals/perturbed/sepsis_goal_model__pertC_distractor_6_112.jucm` | `05b55207ae694929` |
| Condition config | `data/output/sepsis/icpm2027_e2_guided_axisdischarge_pertC_distractor_6_112_rep5/condition_config.yaml` | `8d006148ce3ebd97` |

**Prompt templates:** `prompt_assignment_batch.txt`=`4fe1d4fb8ac2`, `prompt_description.txt`=`7683ed3205c4`, `prompt_taxonomy_intent_guided.txt`=`c3fe7d89554d`, `prompt_taxonomy_intent_guided_revision.txt`=`604be767fe9c`, `prompt_taxonomy_open.txt`=`d32f3f34b809`, `prompt_taxonomy_open_revision.txt`=`cf4eefe924c8`

**Shared Steps 1-4 base:** "icpm2027_base" — `01_variants/variants.csv`=`c24e38b68ca5`, `02_profiling/profiles.csv`=`d6d892a366e1`, `02_profiling/profiles.json`=`f77eee194fb0`, `03_textualization/narratives.csv`=`9d56dd7efb09`, `04_sampling/narrative_sample.csv`=`04449085030b`

## Variant scope

```json
{
  "policy": "all",
  "source": "configs/sepsis.yaml",
  "applied_policy": "all",
  "variants_total": 846,
  "variants_kept": 846,
  "cases_total": 1050,
  "cases_kept": 1050,
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
    "call_count": 34
  },
  "description": null
}
```

## Outputs

| Artifact | Path | SHA-256 (first 16) |
|---|---|---|
| taxonomy | `data/output/sepsis/icpm2027_e2_guided_axisdischarge_pertC_distractor_6_112_rep5/round1/05_taxonomy/taxonomy.json` | `7239f350062aac82` |
| assignments | `data/output/sepsis/icpm2027_e2_guided_axisdischarge_pertC_distractor_6_112_rep5/round1/06_assignment/assignments.csv` | `8b3286661e1f0c74` |
| discovery_metrics | *(not produced)* | — |
| descriptions | *(not produced)* | — |

## Environment

`192.168.68.64` · macOS-26.6.2-arm64-arm-64bit-Mach-O · Python 3.14.6 · git `7d93545a98f0` **(working tree dirty)**

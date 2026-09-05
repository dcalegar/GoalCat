# Run manifest — `e1_open_rep2`

Experiment `e1` · dataset `bpic2019` · arm `open` · replicate 2

Protocol version `1.1.0` · steps [5, 6] · 2026-09-04T22:27:36.950808+00:00 → 2026-09-04T22:37:28.372988+00:00

## Inputs

| Element | Path | SHA-256 (first 16) |
|---|---|---|
| Event log | `data/logs/bpic2019.xes.gz` | `131dedcb49f305c8` |
| Goal model | *(absent by design — open arm)* | — |
| Condition config | `data/output/bpic2019/icpm2027_e1_open_rep2/condition_config.yaml` | `937a72dd48b31f6a` |

**Prompt templates:** `prompt_assignment_batch.txt`=`4fe1d4fb8ac2`, `prompt_description.txt`=`7683ed3205c4`, `prompt_taxonomy_intent_guided.txt`=`c3fe7d89554d`, `prompt_taxonomy_intent_guided_revision.txt`=`604be767fe9c`, `prompt_taxonomy_open.txt`=`d32f3f34b809`, `prompt_taxonomy_open_revision.txt`=`cf4eefe924c8`

**Shared Steps 1-4 base:** "icpm2027_base" — `01_variants/variants.csv`=`b4809e646489`, `02_profiling/profiles.csv`=`b24e8b1d46bf`, `02_profiling/profiles.json`=`fafa559c1d0a`, `03_textualization/narratives.csv`=`b843c4019787`, `04_sampling/narrative_sample.csv`=`4bb68f9caaff`

## Variant scope

```json
{
  "policy": "all",
  "top_n": 1000,
  "min_case_coverage": 0.8,
  "source": "preregistration.yaml:C7_bpic2019_variant_scope",
  "preregistered": true,
  "decided_on": "2026-08-25",
  "applied_policy": "all",
  "variants_total": 11973,
  "variants_kept": 11973,
  "cases_total": 251734,
  "cases_kept": 251734,
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
    "call_count": 479
  },
  "description": null
}
```

## Outputs

| Artifact | Path | SHA-256 (first 16) |
|---|---|---|
| taxonomy | `data/output/bpic2019/icpm2027_e1_open_rep2/round1/05_taxonomy/taxonomy.json` | `a53d60169153bc42` |
| assignments | `data/output/bpic2019/icpm2027_e1_open_rep2/round1/06_assignment/assignments.csv` | `794c05706d5a2c32` |
| discovery_metrics | *(not produced)* | — |
| descriptions | *(not produced)* | — |

## Environment

`192.168.68.64` · macOS-26.6.2-arm64-arm-64bit-Mach-O · Python 3.14.6 · git `7d93545a98f0` **(working tree dirty)**

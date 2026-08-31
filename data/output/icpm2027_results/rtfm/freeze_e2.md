# Freeze verification — rtfm Experiment 2 (axis resolution)

The frozen protocol's freeze table, verified against the conditions' manifests rather than against the driver's intent.

**14/14 rows pass.**

| Element | Requirement | Verdict |
|---|---|---|
| XES | identical | PASS |
| Variant extraction | identical | PASS |
| Multi-view profiles | identical | PASS |
| Narratives | identical | PASS |
| Narrative sample | IDENTICAL (bolded in §2.2) | PASS |
| LLM / provider / model | same | PASS |
| LLM parameters (temperature, seed) | same | PASS |
| Assignment mechanism | same | PASS |
| Assignment batch size (Task C10) | same | PASS |
| Categorization axis | same across guided conditions (absent in open, by design) | PASS |
| Variant scope (Task C7) | same | PASS |
| Protocol version | same | PASS |
| Goal model | present, and distinct per perturbation | PASS |
| Pre-registration (§12) | all conditions pre-registered | PASS |

## Per-row detail

### XES — PASS

Requirement: *identical*

```json
{
  "baseline": "dc9e0e65c964c8ce2a720687ecf17d8204a5cced5db2267c717ed39ada665da8",
  "e2_guided_pertA_remove_20_rep1": "dc9e0e65c964c8ce2a720687ecf17d8204a5cced5db2267c717ed39ada665da8",
  "e2_guided_pertB_merge_13_20_rep1": "dc9e0e65c964c8ce2a720687ecf17d8204a5cced5db2267c717ed39ada665da8"
}
```

### Variant extraction — PASS

Requirement: *identical*

Hash of the shared base's variants.csv, inherited by copy (inputs.py).

```json
{
  "baseline": "a1d36af90468dd294c0ccafe0b79501804e46c9338a520068db1e47ad68f0ddc",
  "e2_guided_pertA_remove_20_rep1": "a1d36af90468dd294c0ccafe0b79501804e46c9338a520068db1e47ad68f0ddc",
  "e2_guided_pertB_merge_13_20_rep1": "a1d36af90468dd294c0ccafe0b79501804e46c9338a520068db1e47ad68f0ddc"
}
```

### Multi-view profiles — PASS

Requirement: *identical*

```json
{
  "baseline": [
    "cdcc6d2f6946d48ebf0008060387613cdd9bf515bc478376361bf58aa54b75e7",
    "8266af382b3999c3f9e1e74fe076ff8300a2f475d53233ba24e48f20e8c63b78"
  ],
  "e2_guided_pertA_remove_20_rep1": [
    "cdcc6d2f6946d48ebf0008060387613cdd9bf515bc478376361bf58aa54b75e7",
    "8266af382b3999c3f9e1e74fe076ff8300a2f475d53233ba24e48f20e8c63b78"
  ],
  "e2_guided_pertB_merge_13_20_rep1": [
    "cdcc6d2f6946d48ebf0008060387613cdd9bf515bc478376361bf58aa54b75e7",
    "8266af382b3999c3f9e1e74fe076ff8300a2f475d53233ba24e48f20e8c63b78"
  ]
}
```

### Narratives — PASS

Requirement: *identical*

```json
{
  "baseline": "57ceea507f36b3690abb6e81c2059d261c76bfedf6bc690e8bcdbff68c8e75dc",
  "e2_guided_pertA_remove_20_rep1": "57ceea507f36b3690abb6e81c2059d261c76bfedf6bc690e8bcdbff68c8e75dc",
  "e2_guided_pertB_merge_13_20_rep1": "57ceea507f36b3690abb6e81c2059d261c76bfedf6bc690e8bcdbff68c8e75dc"
}
```

### Narrative sample — PASS

Requirement: *IDENTICAL (bolded in §2.2)*

The row the design turns on: both arms consume one Step 4 output, copied, not recomputed.

```json
{
  "baseline": "3f5a257c7709dcc3fb21d8a063d67a1fd987d4b66f226979fc7b6dc570d4427b",
  "e2_guided_pertA_remove_20_rep1": "3f5a257c7709dcc3fb21d8a063d67a1fd987d4b66f226979fc7b6dc570d4427b",
  "e2_guided_pertB_merge_13_20_rep1": "3f5a257c7709dcc3fb21d8a063d67a1fd987d4b66f226979fc7b6dc570d4427b"
}
```

### LLM / provider / model — PASS

Requirement: *same*

Read from the provider's own per-call echo.

```json
{
  "baseline": [
    {
      "role": "assignment",
      "model": "gemini/gemini-3.5-flash-lite",
      "resolved_model": null,
      "provider": "gemini",
      "temperature": 0.0
    },
    {
      "role": "taxonomy",
      "model": "gemini/gemini-3.5-flash-lite",
      "resolved_model": null,
      "provider": "gemini",
      "temperature": 0.0
    }
  ],
  "e2_guided_pertA_remove_20_rep1": [
    {
      "role": "assignment",
      "model": "gemini/gemini-3.5-flash-lite",
      "resolved_model": null,
      "provider": "gemini",
      "temperature": 0.0
    },
    {
      "role": "taxonomy",
      "model": "gemini/gemini-3.5-flash-lite",
      "resolved_model": null,
      "provider": "gemini",
      "temperature": 0.0
    }
  ],
  "e2_guided_pertB_merge_13_20_rep1": [
    {
      "role": "assignment",
      "model": "gemini/gemini-3.5-flash-lite",
      "resolved_model": null,
      "provider": "gemini",
      "temperature": 0.0
    },
    {
      "role": "taxonomy",
      "model": "gemini/gemini-3.5-flash-lite",
      "resolved_model": null,
      "provider": "gemini",
      "temperature": 0.0
    }
  ]
}
```

### LLM parameters (temperature, seed) — PASS

Requirement: *same*

Seed is null throughout — no seed is exposed by this provider path (see manifest.py).

```json
{
  "baseline": {
    "temperature": [
      0.0,
      0.0
    ],
    "seed": null
  },
  "e2_guided_pertA_remove_20_rep1": {
    "temperature": [
      0.0,
      0.0
    ],
    "seed": null
  },
  "e2_guided_pertB_merge_13_20_rep1": {
    "temperature": [
      0.0,
      0.0
    ],
    "seed": null
  }
}
```

### Assignment mechanism — PASS

Requirement: *same*

Prompt-template set hashed as a whole; a wording change to any template fails this row.

```json
{
  "baseline": [
    [
      "prompt_assignment_batch.txt",
      "4fe1d4fb8ac2bc1152959faf72df606da66c2a4b9bdedbf6e0ced6fc575ff40d"
    ],
    [
      "prompt_description.txt",
      "7683ed3205c4d156a7ce67966e12562cc729f2655d39bbeaef8b66167a4f9588"
    ],
    [
      "prompt_taxonomy_intent_guided.txt",
      "c3fe7d89554df52d5c08eb4d47c61a66895ff533ab7c4afb2dec69291bf65ac3"
    ],
    [
      "prompt_taxonomy_intent_guided_revision.txt",
      "604be767fe9c5f8f790a09644deb5ef7929d0831369245cda5dc184f3b896444"
    ],
    [
      "prompt_taxonomy_open.txt",
      "d32f3f34b8095ea9f88c2dd15e0a26a486a42295eed8c5002caafedd0292134c"
    ],
    [
      "prompt_taxonomy_open_revision.txt",
      "cf4eefe924c81ce739a7260a8ba605c19530652fd1ad4b52e963f518674931ce"
    ]
  ],
  "e2_guided_pertA_remove_20_rep1": [
    [
      "prompt_assignment_batch.txt",
      "4fe1d4fb8ac2bc1152959faf72df606da66c2a4b9bdedbf6e0ced6fc575ff40d"
    ],
    [
      "prompt_description.txt",
      "7683ed3205c4d156a7ce67966e12562cc729f2655d39bbeaef8b66167a4f9588"
    ],
    [
      "prompt_taxonomy_intent_guided.txt",
      "c3fe7d89554df52d5c08eb4d47c61a66895ff533ab7c4afb2dec69291bf65ac3"
    ],
    [
      "prompt_taxonomy_intent_guided_revision.txt",
      "604be767fe9c5f8f790a09644deb5ef7929d0831369245cda5dc184f3b896444"
    ],
    [
      "prompt_taxonomy_open.txt",
      "d32f3f34b8095ea9f88c2dd15e0a26a486a42295eed8c5002caafedd0292134c"
    ],
    [
      "prompt_taxonomy_open_revision.txt",
      "cf4eefe924c81ce739a7260a8ba605c19530652fd1ad4b52e963f518674931ce"
    ]
  ],
  "e2_guided_pertB_merge_13_20_rep1": [
    [
      "prompt_assignment_batch.txt",
      "4fe1d4fb8ac2bc1152959faf72df606da66c2a4b9bdedbf6e0ced6fc575ff40d"
    ],
    [
      "prompt_description.txt",
      "7683ed3205c4d156a7ce67966e12562cc729f2655d39bbeaef8b66167a4f9588"
    ],
    [
      "prompt_taxonomy_intent_guided.txt",
      "c3fe7d89554df52d5c08eb4d47c61a66895ff533ab7c4afb2dec69291bf65ac3"
    ],
    [
      "prompt_taxonomy_intent_guided_revision.txt",
      "604be767fe9c5f8f790a09644deb5ef7929d0831369245cda5dc184f3b896444"
    ],
    [
      "prompt_taxonomy_open.txt",
      "d32f3f34b8095ea9f88c2dd15e0a26a486a42295eed8c5002caafedd0292134c"
    ],
    [
      "prompt_taxonomy_open_revision.txt",
      "cf4eefe924c81ce739a7260a8ba605c19530652fd1ad4b52e963f518674931ce"
    ]
  ]
}
```

### Assignment batch size (Task C10) — PASS

Requirement: *same*

```json
{
  "baseline": 50,
  "e2_guided_pertA_remove_20_rep1": 50,
  "e2_guided_pertB_merge_13_20_rep1": 50
}
```

### Categorization axis — PASS

Requirement: *same across guided conditions (absent in open, by design)*

Two guided conditions that induce against different Or frontiers partition different things and are not a paired comparison. The open arm carries no axis for the same reason it carries no goal model, and one open run serves every axis. Null throughout on a dataset declaring a single axis.

```json
{
  "baseline": "resolution",
  "e2_guided_pertA_remove_20_rep1": "resolution",
  "e2_guided_pertB_merge_13_20_rep1": "resolution"
}
```

### Variant scope (Task C7) — PASS

Requirement: *same*

```json
{
  "baseline": 231,
  "e2_guided_pertA_remove_20_rep1": 231,
  "e2_guided_pertB_merge_13_20_rep1": 231
}
```

### Protocol version — PASS

Requirement: *same*

```json
{
  "baseline": "1.0.0",
  "e2_guided_pertA_remove_20_rep1": "1.0.0",
  "e2_guided_pertB_merge_13_20_rep1": "1.0.0"
}
```

### Goal model — PASS

Requirement: *present, and distinct per perturbation*

Experiment 2's one intended difference. Every guided condition must read a distinct, present goal model: two conditions sharing a file means a perturbation did not write the edit it claims to test.

```json
{
  "baseline": {
    "arm": "guided",
    "sha256": "0b2a7ea87d75967f3aacf6dbfd42808afac879cab66fca93e2baa7d61086d423",
    "absent_by_design": false
  },
  "e2_guided_pertA_remove_20_rep1": {
    "arm": "guided",
    "sha256": "75260074ac4eecba65ee87de8bfc6764fe2fed592f76b24a56d6a743b2776e09",
    "absent_by_design": false
  },
  "e2_guided_pertB_merge_13_20_rep1": {
    "arm": "guided",
    "sha256": "7367d6b3f478d945fe6c84f93390f701a325f1d60c91b12c089d9f67f7c3f511",
    "absent_by_design": false
  }
}
```

### Pre-registration (§12) — PASS

Requirement: *all conditions pre-registered*

False means the run was launched with --allow-pending-decisions.

```json
{
  "baseline": true,
  "e2_guided_pertA_remove_20_rep1": true,
  "e2_guided_pertB_merge_13_20_rep1": true
}
```

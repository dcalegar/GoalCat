# Freeze verification — bpic2019 Experiment 1 (axis matching_regime)

The frozen protocol's freeze table, verified against the conditions' manifests rather than against the driver's intent.

**14/14 rows pass.**

| Element | Requirement | Verdict |
|---|---|---|
| XES | identical | PASS |
| Variant extraction | identical | PASS |
| Multi-view profiles | identical | PASS |
| Narratives | identical | PASS |
| Narrative sample | IDENTICAL (bolded in §2.2) | PASS |
| LLM / provider / model | same per role, among conditions that make that role's call | PASS |
| LLM parameters (temperature, seed) | same per role, among conditions that make that role's call | PASS |
| Assignment mechanism | same | PASS |
| Assignment batch size (Task C10) | same | PASS |
| Categorization axis | same across guided conditions (absent in open, by design) | PASS |
| Variant scope (Task C7) | same | PASS |
| Protocol version | same | PASS |
| Goal model | present and frozen (guided) / absent (open) | PASS |
| Pre-registration (§12) | all conditions pre-registered | PASS |

## Per-row detail

### XES — PASS

Requirement: *identical*

```json
{
  "e1_guided_rep1": "131dedcb49f305c8f1d036bf94acd8f5c92e2da189c81a20aa350358afbe45ed",
  "e1_guided_rep2": "131dedcb49f305c8f1d036bf94acd8f5c92e2da189c81a20aa350358afbe45ed",
  "e1_label_list_rep1": "131dedcb49f305c8f1d036bf94acd8f5c92e2da189c81a20aa350358afbe45ed",
  "e1_label_list_rep2": "131dedcb49f305c8f1d036bf94acd8f5c92e2da189c81a20aa350358afbe45ed",
  "e1_label_list_strict_rep1": "131dedcb49f305c8f1d036bf94acd8f5c92e2da189c81a20aa350358afbe45ed",
  "e1_label_list_strict_rep2": "131dedcb49f305c8f1d036bf94acd8f5c92e2da189c81a20aa350358afbe45ed"
}
```

### Variant extraction — PASS

Requirement: *identical*

Hash of the shared base's variants.csv, inherited by copy (inputs.py).

```json
{
  "e1_guided_rep1": "b4809e646489a3149f19318476c2a000ec4e59db193396c68974f02c6adde59a",
  "e1_guided_rep2": "b4809e646489a3149f19318476c2a000ec4e59db193396c68974f02c6adde59a",
  "e1_label_list_rep1": "b4809e646489a3149f19318476c2a000ec4e59db193396c68974f02c6adde59a",
  "e1_label_list_rep2": "b4809e646489a3149f19318476c2a000ec4e59db193396c68974f02c6adde59a",
  "e1_label_list_strict_rep1": "b4809e646489a3149f19318476c2a000ec4e59db193396c68974f02c6adde59a",
  "e1_label_list_strict_rep2": "b4809e646489a3149f19318476c2a000ec4e59db193396c68974f02c6adde59a"
}
```

### Multi-view profiles — PASS

Requirement: *identical*

```json
{
  "e1_guided_rep1": [
    "b24e8b1d46bf055d888953c042553b2ccdb464da98453fbedfa6b1e933b8f2be",
    "fafa559c1d0a68f668ada6fff053dd766ff24efbc2e97c2008af87d92d7302a2"
  ],
  "e1_guided_rep2": [
    "b24e8b1d46bf055d888953c042553b2ccdb464da98453fbedfa6b1e933b8f2be",
    "fafa559c1d0a68f668ada6fff053dd766ff24efbc2e97c2008af87d92d7302a2"
  ],
  "e1_label_list_rep1": [
    "b24e8b1d46bf055d888953c042553b2ccdb464da98453fbedfa6b1e933b8f2be",
    "fafa559c1d0a68f668ada6fff053dd766ff24efbc2e97c2008af87d92d7302a2"
  ],
  "e1_label_list_rep2": [
    "b24e8b1d46bf055d888953c042553b2ccdb464da98453fbedfa6b1e933b8f2be",
    "fafa559c1d0a68f668ada6fff053dd766ff24efbc2e97c2008af87d92d7302a2"
  ],
  "e1_label_list_strict_rep1": [
    "b24e8b1d46bf055d888953c042553b2ccdb464da98453fbedfa6b1e933b8f2be",
    "fafa559c1d0a68f668ada6fff053dd766ff24efbc2e97c2008af87d92d7302a2"
  ],
  "e1_label_list_strict_rep2": [
    "b24e8b1d46bf055d888953c042553b2ccdb464da98453fbedfa6b1e933b8f2be",
    "fafa559c1d0a68f668ada6fff053dd766ff24efbc2e97c2008af87d92d7302a2"
  ]
}
```

### Narratives — PASS

Requirement: *identical*

```json
{
  "e1_guided_rep1": "b843c401978701261f7518abc2896ecff8fab73eb1fbaeedd21ed58cd3d269c9",
  "e1_guided_rep2": "b843c401978701261f7518abc2896ecff8fab73eb1fbaeedd21ed58cd3d269c9",
  "e1_label_list_rep1": "b843c401978701261f7518abc2896ecff8fab73eb1fbaeedd21ed58cd3d269c9",
  "e1_label_list_rep2": "b843c401978701261f7518abc2896ecff8fab73eb1fbaeedd21ed58cd3d269c9",
  "e1_label_list_strict_rep1": "b843c401978701261f7518abc2896ecff8fab73eb1fbaeedd21ed58cd3d269c9",
  "e1_label_list_strict_rep2": "b843c401978701261f7518abc2896ecff8fab73eb1fbaeedd21ed58cd3d269c9"
}
```

### Narrative sample — PASS

Requirement: *IDENTICAL (bolded in §2.2)*

The row the design turns on: both arms consume one Step 4 output, copied, not recomputed.

```json
{
  "e1_guided_rep1": "4bb68f9caaff6fcb2ffe7002730d4beabd7ec26aabad2ee0ac4ac2f2732f85a1",
  "e1_guided_rep2": "4bb68f9caaff6fcb2ffe7002730d4beabd7ec26aabad2ee0ac4ac2f2732f85a1",
  "e1_label_list_rep1": "4bb68f9caaff6fcb2ffe7002730d4beabd7ec26aabad2ee0ac4ac2f2732f85a1",
  "e1_label_list_rep2": "4bb68f9caaff6fcb2ffe7002730d4beabd7ec26aabad2ee0ac4ac2f2732f85a1",
  "e1_label_list_strict_rep1": "4bb68f9caaff6fcb2ffe7002730d4beabd7ec26aabad2ee0ac4ac2f2732f85a1",
  "e1_label_list_strict_rep2": "4bb68f9caaff6fcb2ffe7002730d4beabd7ec26aabad2ee0ac4ac2f2732f85a1"
}
```

### LLM / provider / model — PASS

Requirement: *same per role, among conditions that make that role's call*

Read from the provider's own per-call echo. The label-list arm (Task C5) makes no Step 5 (taxonomy) call by design, so that role is compared only among the conditions that do call it — the same treatment as the Categorization-axis row above.

```json
{
  "e1_guided_rep1": {
    "by_role": {
      "assignment": [
        {
          "role": "assignment",
          "model": "gemini/gemini-3.5-flash-lite",
          "resolved_model": null,
          "provider": "gemini",
          "temperature": 0.0
        }
      ],
      "taxonomy": [
        {
          "role": "taxonomy",
          "model": "gemini/gemini-3.5-flash-lite",
          "resolved_model": null,
          "provider": "gemini",
          "temperature": 0.0
        }
      ]
    }
  },
  "e1_guided_rep2": {
    "by_role": {
      "assignment": [
        {
          "role": "assignment",
          "model": "gemini/gemini-3.5-flash-lite",
          "resolved_model": null,
          "provider": "gemini",
          "temperature": 0.0
        }
      ],
      "taxonomy": [
        {
          "role": "taxonomy",
          "model": "gemini/gemini-3.5-flash-lite",
          "resolved_model": null,
          "provider": "gemini",
          "temperature": 0.0
        }
      ]
    }
  },
  "e1_label_list_rep1": {
    "by_role": {
      "assignment": [
        {
          "role": "assignment",
          "model": "gemini/gemini-3.5-flash-lite",
          "resolved_model": null,
          "provider": "gemini",
          "temperature": 0.0
        }
      ]
    }
  },
  "e1_label_list_rep2": {
    "by_role": {
      "assignment": [
        {
          "role": "assignment",
          "model": "gemini/gemini-3.5-flash-lite",
          "resolved_model": null,
          "provider": "gemini",
          "temperature": 0.0
        }
      ]
    }
  },
  "e1_label_list_strict_rep1": {
    "by_role": {
      "assignment": [
        {
          "role": "assignment",
          "model": "gemini/gemini-3.5-flash-lite",
          "resolved_model": null,
          "provider": "gemini",
          "temperature": 0.0
        }
      ]
    }
  },
  "e1_label_list_strict_rep2": {
    "by_role": {
      "assignment": [
        {
          "role": "assignment",
          "model": "gemini/gemini-3.5-flash-lite",
          "resolved_model": null,
          "provider": "gemini",
          "temperature": 0.0
        }
      ]
    }
  }
}
```

### LLM parameters (temperature, seed) — PASS

Requirement: *same per role, among conditions that make that role's call*

Seed is null throughout — no seed is exposed by this provider path (see manifest.py). Temperature is compared per role for the same reason as the row above.

```json
{
  "e1_guided_rep1": {
    "by_role": {
      "assignment": [
        {
          "temperature": 0.0
        }
      ],
      "taxonomy": [
        {
          "temperature": 0.0
        }
      ]
    },
    "seed": null
  },
  "e1_guided_rep2": {
    "by_role": {
      "assignment": [
        {
          "temperature": 0.0
        }
      ],
      "taxonomy": [
        {
          "temperature": 0.0
        }
      ]
    },
    "seed": null
  },
  "e1_label_list_rep1": {
    "by_role": {
      "assignment": [
        {
          "temperature": 0.0
        }
      ]
    },
    "seed": null
  },
  "e1_label_list_rep2": {
    "by_role": {
      "assignment": [
        {
          "temperature": 0.0
        }
      ]
    },
    "seed": null
  },
  "e1_label_list_strict_rep1": {
    "by_role": {
      "assignment": [
        {
          "temperature": 0.0
        }
      ]
    },
    "seed": null
  },
  "e1_label_list_strict_rep2": {
    "by_role": {
      "assignment": [
        {
          "temperature": 0.0
        }
      ]
    },
    "seed": null
  }
}
```

### Assignment mechanism — PASS

Requirement: *same*

Prompt-template set hashed as a whole; a wording change to any template fails this row.

```json
{
  "e1_guided_rep1": [
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
  "e1_guided_rep2": [
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
  "e1_label_list_rep1": [
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
  "e1_label_list_rep2": [
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
  "e1_label_list_strict_rep1": [
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
  "e1_label_list_strict_rep2": [
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
  "e1_guided_rep1": 25,
  "e1_guided_rep2": 25,
  "e1_label_list_rep1": 25,
  "e1_label_list_rep2": 25,
  "e1_label_list_strict_rep1": 25,
  "e1_label_list_strict_rep2": 25
}
```

### Categorization axis — PASS

Requirement: *same across guided conditions (absent in open, by design)*

Two guided conditions that induce against different Or frontiers partition different things and are not a paired comparison. The open arm carries no axis for the same reason it carries no goal model, and one open run serves every axis. Null throughout on a dataset declaring a single axis.

```json
{
  "e1_guided_rep1": "matching_regime",
  "e1_guided_rep2": "matching_regime",
  "e1_label_list_rep1": null,
  "e1_label_list_rep2": null,
  "e1_label_list_strict_rep1": null,
  "e1_label_list_strict_rep2": null
}
```

### Variant scope (Task C7) — PASS

Requirement: *same*

```json
{
  "e1_guided_rep1": 11973,
  "e1_guided_rep2": 11973,
  "e1_label_list_rep1": 11973,
  "e1_label_list_rep2": 11973,
  "e1_label_list_strict_rep1": 11973,
  "e1_label_list_strict_rep2": 11973
}
```

### Protocol version — PASS

Requirement: *same*

```json
{
  "e1_guided_rep1": "1.1.0",
  "e1_guided_rep2": "1.1.0",
  "e1_label_list_rep1": "1.1.0",
  "e1_label_list_rep2": "1.1.0",
  "e1_label_list_strict_rep1": "1.1.0",
  "e1_label_list_strict_rep2": "1.1.0"
}
```

### Goal model — PASS

Requirement: *present and frozen (guided) / absent (open)*

Guided arms must all read one identical goal-model file; open and label-list arms must have none configured at all — not merely be set to ignore one.

```json
{
  "e1_guided_rep1": {
    "arm": "guided",
    "sha256": "68c8d4d4a42e5f45f4b8e46c24b3e80c69f52d10a7ff8fdae95fae255a85be3f",
    "absent_by_design": false
  },
  "e1_guided_rep2": {
    "arm": "guided",
    "sha256": "68c8d4d4a42e5f45f4b8e46c24b3e80c69f52d10a7ff8fdae95fae255a85be3f",
    "absent_by_design": false
  },
  "e1_label_list_rep1": {
    "arm": "label_list",
    "sha256": null,
    "absent_by_design": true
  },
  "e1_label_list_rep2": {
    "arm": "label_list",
    "sha256": null,
    "absent_by_design": true
  },
  "e1_label_list_strict_rep1": {
    "arm": "label_list_strict",
    "sha256": null,
    "absent_by_design": true
  },
  "e1_label_list_strict_rep2": {
    "arm": "label_list_strict",
    "sha256": null,
    "absent_by_design": true
  }
}
```

### Pre-registration (§12) — PASS

Requirement: *all conditions pre-registered*

False means the run was launched with --allow-pending-decisions.

```json
{
  "e1_guided_rep1": true,
  "e1_guided_rep2": true,
  "e1_label_list_rep1": true,
  "e1_label_list_rep2": true,
  "e1_label_list_strict_rep1": true,
  "e1_label_list_strict_rep2": true
}
```

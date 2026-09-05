# Freeze verification — sepsis Experiment 1 (axis discharge)

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
  "e1_guided_axisdischarge_rep1": "709c52340306415952811b9b9c5dc6bcc8f8d47d583eba39df9a538459dc543a",
  "e1_guided_axisdischarge_rep2": "709c52340306415952811b9b9c5dc6bcc8f8d47d583eba39df9a538459dc543a",
  "e1_guided_axisdischarge_rep3": "709c52340306415952811b9b9c5dc6bcc8f8d47d583eba39df9a538459dc543a",
  "e1_guided_axisdischarge_rep4": "709c52340306415952811b9b9c5dc6bcc8f8d47d583eba39df9a538459dc543a",
  "e1_guided_axisdischarge_rep5": "709c52340306415952811b9b9c5dc6bcc8f8d47d583eba39df9a538459dc543a",
  "e1_open_rep1": "709c52340306415952811b9b9c5dc6bcc8f8d47d583eba39df9a538459dc543a",
  "e1_open_rep2": "709c52340306415952811b9b9c5dc6bcc8f8d47d583eba39df9a538459dc543a",
  "e1_open_rep3": "709c52340306415952811b9b9c5dc6bcc8f8d47d583eba39df9a538459dc543a",
  "e1_open_rep4": "709c52340306415952811b9b9c5dc6bcc8f8d47d583eba39df9a538459dc543a",
  "e1_open_rep5": "709c52340306415952811b9b9c5dc6bcc8f8d47d583eba39df9a538459dc543a"
}
```

### Variant extraction — PASS

Requirement: *identical*

Hash of the shared base's variants.csv, inherited by copy (inputs.py).

```json
{
  "e1_guided_axisdischarge_rep1": "c24e38b68ca586fea68066929d0eb94ef4626dcc4fec511a04dc84a44c7462af",
  "e1_guided_axisdischarge_rep2": "c24e38b68ca586fea68066929d0eb94ef4626dcc4fec511a04dc84a44c7462af",
  "e1_guided_axisdischarge_rep3": "c24e38b68ca586fea68066929d0eb94ef4626dcc4fec511a04dc84a44c7462af",
  "e1_guided_axisdischarge_rep4": "c24e38b68ca586fea68066929d0eb94ef4626dcc4fec511a04dc84a44c7462af",
  "e1_guided_axisdischarge_rep5": "c24e38b68ca586fea68066929d0eb94ef4626dcc4fec511a04dc84a44c7462af",
  "e1_open_rep1": "c24e38b68ca586fea68066929d0eb94ef4626dcc4fec511a04dc84a44c7462af",
  "e1_open_rep2": "c24e38b68ca586fea68066929d0eb94ef4626dcc4fec511a04dc84a44c7462af",
  "e1_open_rep3": "c24e38b68ca586fea68066929d0eb94ef4626dcc4fec511a04dc84a44c7462af",
  "e1_open_rep4": "c24e38b68ca586fea68066929d0eb94ef4626dcc4fec511a04dc84a44c7462af",
  "e1_open_rep5": "c24e38b68ca586fea68066929d0eb94ef4626dcc4fec511a04dc84a44c7462af"
}
```

### Multi-view profiles — PASS

Requirement: *identical*

```json
{
  "e1_guided_axisdischarge_rep1": [
    "d6d892a366e1566759173979fd27ddf6dc474b065c07ce7fef8fbf2c36c5382c",
    "f77eee194fb01b7bb04d067d9cde9b01597db90179b3e5215270919805cac3eb"
  ],
  "e1_guided_axisdischarge_rep2": [
    "d6d892a366e1566759173979fd27ddf6dc474b065c07ce7fef8fbf2c36c5382c",
    "f77eee194fb01b7bb04d067d9cde9b01597db90179b3e5215270919805cac3eb"
  ],
  "e1_guided_axisdischarge_rep3": [
    "d6d892a366e1566759173979fd27ddf6dc474b065c07ce7fef8fbf2c36c5382c",
    "f77eee194fb01b7bb04d067d9cde9b01597db90179b3e5215270919805cac3eb"
  ],
  "e1_guided_axisdischarge_rep4": [
    "d6d892a366e1566759173979fd27ddf6dc474b065c07ce7fef8fbf2c36c5382c",
    "f77eee194fb01b7bb04d067d9cde9b01597db90179b3e5215270919805cac3eb"
  ],
  "e1_guided_axisdischarge_rep5": [
    "d6d892a366e1566759173979fd27ddf6dc474b065c07ce7fef8fbf2c36c5382c",
    "f77eee194fb01b7bb04d067d9cde9b01597db90179b3e5215270919805cac3eb"
  ],
  "e1_open_rep1": [
    "d6d892a366e1566759173979fd27ddf6dc474b065c07ce7fef8fbf2c36c5382c",
    "f77eee194fb01b7bb04d067d9cde9b01597db90179b3e5215270919805cac3eb"
  ],
  "e1_open_rep2": [
    "d6d892a366e1566759173979fd27ddf6dc474b065c07ce7fef8fbf2c36c5382c",
    "f77eee194fb01b7bb04d067d9cde9b01597db90179b3e5215270919805cac3eb"
  ],
  "e1_open_rep3": [
    "d6d892a366e1566759173979fd27ddf6dc474b065c07ce7fef8fbf2c36c5382c",
    "f77eee194fb01b7bb04d067d9cde9b01597db90179b3e5215270919805cac3eb"
  ],
  "e1_open_rep4": [
    "d6d892a366e1566759173979fd27ddf6dc474b065c07ce7fef8fbf2c36c5382c",
    "f77eee194fb01b7bb04d067d9cde9b01597db90179b3e5215270919805cac3eb"
  ],
  "e1_open_rep5": [
    "d6d892a366e1566759173979fd27ddf6dc474b065c07ce7fef8fbf2c36c5382c",
    "f77eee194fb01b7bb04d067d9cde9b01597db90179b3e5215270919805cac3eb"
  ]
}
```

### Narratives — PASS

Requirement: *identical*

```json
{
  "e1_guided_axisdischarge_rep1": "9d56dd7efb09156846cb58681311f18e96667b9d4cd9d21459308a13d4ca2b2b",
  "e1_guided_axisdischarge_rep2": "9d56dd7efb09156846cb58681311f18e96667b9d4cd9d21459308a13d4ca2b2b",
  "e1_guided_axisdischarge_rep3": "9d56dd7efb09156846cb58681311f18e96667b9d4cd9d21459308a13d4ca2b2b",
  "e1_guided_axisdischarge_rep4": "9d56dd7efb09156846cb58681311f18e96667b9d4cd9d21459308a13d4ca2b2b",
  "e1_guided_axisdischarge_rep5": "9d56dd7efb09156846cb58681311f18e96667b9d4cd9d21459308a13d4ca2b2b",
  "e1_open_rep1": "9d56dd7efb09156846cb58681311f18e96667b9d4cd9d21459308a13d4ca2b2b",
  "e1_open_rep2": "9d56dd7efb09156846cb58681311f18e96667b9d4cd9d21459308a13d4ca2b2b",
  "e1_open_rep3": "9d56dd7efb09156846cb58681311f18e96667b9d4cd9d21459308a13d4ca2b2b",
  "e1_open_rep4": "9d56dd7efb09156846cb58681311f18e96667b9d4cd9d21459308a13d4ca2b2b",
  "e1_open_rep5": "9d56dd7efb09156846cb58681311f18e96667b9d4cd9d21459308a13d4ca2b2b"
}
```

### Narrative sample — PASS

Requirement: *IDENTICAL (bolded in §2.2)*

The row the design turns on: both arms consume one Step 4 output, copied, not recomputed.

```json
{
  "e1_guided_axisdischarge_rep1": "04449085030b572397081b439745b73c13d7ac5e980959cf7b3e56bb877d169a",
  "e1_guided_axisdischarge_rep2": "04449085030b572397081b439745b73c13d7ac5e980959cf7b3e56bb877d169a",
  "e1_guided_axisdischarge_rep3": "04449085030b572397081b439745b73c13d7ac5e980959cf7b3e56bb877d169a",
  "e1_guided_axisdischarge_rep4": "04449085030b572397081b439745b73c13d7ac5e980959cf7b3e56bb877d169a",
  "e1_guided_axisdischarge_rep5": "04449085030b572397081b439745b73c13d7ac5e980959cf7b3e56bb877d169a",
  "e1_open_rep1": "04449085030b572397081b439745b73c13d7ac5e980959cf7b3e56bb877d169a",
  "e1_open_rep2": "04449085030b572397081b439745b73c13d7ac5e980959cf7b3e56bb877d169a",
  "e1_open_rep3": "04449085030b572397081b439745b73c13d7ac5e980959cf7b3e56bb877d169a",
  "e1_open_rep4": "04449085030b572397081b439745b73c13d7ac5e980959cf7b3e56bb877d169a",
  "e1_open_rep5": "04449085030b572397081b439745b73c13d7ac5e980959cf7b3e56bb877d169a"
}
```

### LLM / provider / model — PASS

Requirement: *same per role, among conditions that make that role's call*

Read from the provider's own per-call echo. The label-list arm (Task C5) makes no Step 5 (taxonomy) call by design, so that role is compared only among the conditions that do call it — the same treatment as the Categorization-axis row above.

```json
{
  "e1_guided_axisdischarge_rep1": {
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
  "e1_guided_axisdischarge_rep2": {
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
  "e1_guided_axisdischarge_rep3": {
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
  "e1_guided_axisdischarge_rep4": {
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
  "e1_guided_axisdischarge_rep5": {
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
  "e1_open_rep1": {
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
  "e1_open_rep2": {
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
  "e1_open_rep3": {
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
  "e1_open_rep4": {
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
  "e1_open_rep5": {
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
  }
}
```

### LLM parameters (temperature, seed) — PASS

Requirement: *same per role, among conditions that make that role's call*

Seed is null throughout — no seed is exposed by this provider path (see manifest.py). Temperature is compared per role for the same reason as the row above.

```json
{
  "e1_guided_axisdischarge_rep1": {
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
  "e1_guided_axisdischarge_rep2": {
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
  "e1_guided_axisdischarge_rep3": {
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
  "e1_guided_axisdischarge_rep4": {
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
  "e1_guided_axisdischarge_rep5": {
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
  "e1_open_rep1": {
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
  "e1_open_rep2": {
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
  "e1_open_rep3": {
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
  "e1_open_rep4": {
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
  "e1_open_rep5": {
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
  }
}
```

### Assignment mechanism — PASS

Requirement: *same*

Prompt-template set hashed as a whole; a wording change to any template fails this row.

```json
{
  "e1_guided_axisdischarge_rep1": [
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
  "e1_guided_axisdischarge_rep2": [
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
  "e1_guided_axisdischarge_rep3": [
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
  "e1_guided_axisdischarge_rep4": [
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
  "e1_guided_axisdischarge_rep5": [
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
  "e1_open_rep1": [
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
  "e1_open_rep2": [
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
  "e1_open_rep3": [
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
  "e1_open_rep4": [
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
  "e1_open_rep5": [
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
  "e1_guided_axisdischarge_rep1": 25,
  "e1_guided_axisdischarge_rep2": 25,
  "e1_guided_axisdischarge_rep3": 25,
  "e1_guided_axisdischarge_rep4": 25,
  "e1_guided_axisdischarge_rep5": 25,
  "e1_open_rep1": 25,
  "e1_open_rep2": 25,
  "e1_open_rep3": 25,
  "e1_open_rep4": 25,
  "e1_open_rep5": 25
}
```

### Categorization axis — PASS

Requirement: *same across guided conditions (absent in open, by design)*

Two guided conditions that induce against different Or frontiers partition different things and are not a paired comparison. The open arm carries no axis for the same reason it carries no goal model, and one open run serves every axis. Null throughout on a dataset declaring a single axis.

```json
{
  "e1_guided_axisdischarge_rep1": "discharge",
  "e1_guided_axisdischarge_rep2": "discharge",
  "e1_guided_axisdischarge_rep3": "discharge",
  "e1_guided_axisdischarge_rep4": "discharge",
  "e1_guided_axisdischarge_rep5": "discharge",
  "e1_open_rep1": null,
  "e1_open_rep2": null,
  "e1_open_rep3": null,
  "e1_open_rep4": null,
  "e1_open_rep5": null
}
```

### Variant scope (Task C7) — PASS

Requirement: *same*

```json
{
  "e1_guided_axisdischarge_rep1": 846,
  "e1_guided_axisdischarge_rep2": 846,
  "e1_guided_axisdischarge_rep3": 846,
  "e1_guided_axisdischarge_rep4": 846,
  "e1_guided_axisdischarge_rep5": 846,
  "e1_open_rep1": 846,
  "e1_open_rep2": 846,
  "e1_open_rep3": 846,
  "e1_open_rep4": 846,
  "e1_open_rep5": 846
}
```

### Protocol version — PASS

Requirement: *same*

```json
{
  "e1_guided_axisdischarge_rep1": "1.1.0",
  "e1_guided_axisdischarge_rep2": "1.1.0",
  "e1_guided_axisdischarge_rep3": "1.1.0",
  "e1_guided_axisdischarge_rep4": "1.1.0",
  "e1_guided_axisdischarge_rep5": "1.1.0",
  "e1_open_rep1": "1.1.0",
  "e1_open_rep2": "1.1.0",
  "e1_open_rep3": "1.1.0",
  "e1_open_rep4": "1.1.0",
  "e1_open_rep5": "1.1.0"
}
```

### Goal model — PASS

Requirement: *present and frozen (guided) / absent (open)*

Guided arms must all read one identical goal-model file; open and label-list arms must have none configured at all — not merely be set to ignore one.

```json
{
  "e1_guided_axisdischarge_rep1": {
    "arm": "guided",
    "sha256": "749aa9e234ca70c7b4de2e39c0d3d8d28b4de8c0e5110418a199b62c63462135",
    "absent_by_design": false
  },
  "e1_guided_axisdischarge_rep2": {
    "arm": "guided",
    "sha256": "749aa9e234ca70c7b4de2e39c0d3d8d28b4de8c0e5110418a199b62c63462135",
    "absent_by_design": false
  },
  "e1_guided_axisdischarge_rep3": {
    "arm": "guided",
    "sha256": "749aa9e234ca70c7b4de2e39c0d3d8d28b4de8c0e5110418a199b62c63462135",
    "absent_by_design": false
  },
  "e1_guided_axisdischarge_rep4": {
    "arm": "guided",
    "sha256": "749aa9e234ca70c7b4de2e39c0d3d8d28b4de8c0e5110418a199b62c63462135",
    "absent_by_design": false
  },
  "e1_guided_axisdischarge_rep5": {
    "arm": "guided",
    "sha256": "749aa9e234ca70c7b4de2e39c0d3d8d28b4de8c0e5110418a199b62c63462135",
    "absent_by_design": false
  },
  "e1_open_rep1": {
    "arm": "open",
    "sha256": null,
    "absent_by_design": true
  },
  "e1_open_rep2": {
    "arm": "open",
    "sha256": null,
    "absent_by_design": true
  },
  "e1_open_rep3": {
    "arm": "open",
    "sha256": null,
    "absent_by_design": true
  },
  "e1_open_rep4": {
    "arm": "open",
    "sha256": null,
    "absent_by_design": true
  },
  "e1_open_rep5": {
    "arm": "open",
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
  "e1_guided_axisdischarge_rep1": true,
  "e1_guided_axisdischarge_rep2": true,
  "e1_guided_axisdischarge_rep3": true,
  "e1_guided_axisdischarge_rep4": true,
  "e1_guided_axisdischarge_rep5": true,
  "e1_open_rep1": true,
  "e1_open_rep2": true,
  "e1_open_rep3": true,
  "e1_open_rep4": true,
  "e1_open_rep5": true
}
```

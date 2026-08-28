# `third_party/jucmnav`

Vendored GRL/URN metamodel definitions (`.ecore` files), fetched from
[JUCMNAV/jUCMNavPlus](https://github.com/JUCMNAV/jUCMNavPlus) — the jUCMNav Eclipse project's
"attempted resurrection", the de facto reference implementation for the User Requirements Notation
(URN, ITU-T Z.151) and its Goal-oriented Requirement Language (GRL). Used by
`src/goalcat/grl/jucm_io.py` to load the real schema through `pyecore` (a Python EMF
implementation), so `.jucm` files are parsed and serialized against the actual metamodel rather
than a hand-derived re-implementation of it.

## What's here and why

Only the `.ecore` schema files, at the same relative paths they occupy inside jUCMNavPlus (`grl`
and `urncore`/`urn` cross-reference each other, `.ecore`, and several other schemas, via relative
paths baked into the files themselves — `../../../../../ca.mcgill.sel.core/model/CORE.ecore` and
similar — so this directory mirrors that structure rather than flattening it):

```
jucmnav/
├── ca.mcgill.sel.core/model/CORE.ecore
└── seg.jUCMNav/src/seg/jUCMNav/emf/
    ├── grl.ecore          # Goal-oriented Requirement Language (this project's actual target)
    ├── urncore.ecore       # shared URN base types (URNmodelElement, GRLmodelElement, ...)
    ├── urn.ecore            # URNspec root, combines grlspec + ucmspec + asdspec
    ├── ucm.ecore              # Use Case Maps (unused by this project — loaded only because
    ├── ucmscenarios.ecore      # urn.ecore references it structurally, so it must resolve)
    └── asd.ecore                # aspect-oriented scenario definitions (same — unused, must resolve)
```

No Java source, no generated code, no build tooling — just the schema definitions themselves.
This project never edits them; they are read-only reference data for `pyecore` to load.

## Why this content, not the `pm4py_ucm` PyPI package

`pm4py_ucm` (a separate dependency of `experimentation/icpm2027`, for the UCM/process-mining
side unrelated to goal models) was investigated first and confirmed to have **no GRL support** —
its `.jucm` importer explicitly skips `grlspec` and its exporter writes an empty one (see
`src/goalcat/grl/__init__.py`'s module docstring, and `pm4py_ucm`'s own documentation, which
documented GRL synthesis as an unimplemented design proposal at the time these files were
vendored). There is nothing to reuse from it for GRL specifically.

## License

jUCMNav is licensed under the **Eclipse Public License, version 1.0** (per
`seg.jUCMNav/about.html` in the source repository: *"usecasemaps.org makes available all content
in this plug-in ... under the terms and conditions of the Eclipse Public License Version 1.0"*).
Only schema/metamodel definitions are vendored here — data consumed at runtime to validate and
serialize `.jucm` documents, not executable code linked into GoalCat's own AGPL-3.0-or-later
codebase — mirroring the isolation approach `third_party/lupin/` already takes for a
differently-licensed vendored component (see that directory's own README for its contract).

## Provenance

Fetched 2026-08-19 from `https://github.com/JUCMNAV/jUCMNavPlus` (branch `master`) via the GitHub
API, at the commit current when `src/goalcat/grl/` was built. Not kept in sync automatically —
re-fetch manually if the upstream schema changes and this project needs to track it.

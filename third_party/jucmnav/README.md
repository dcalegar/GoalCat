# `third_party/jucmnav`

Vendored GRL/URN metamodel definitions (`.ecore` files) from
[JUCMNAV/jUCMNavPlus](https://github.com/JUCMNAV/jUCMNavPlus), the continuation of jUCMNav, the
reference tool for the User Requirements Notation (URN, ITU-T Z.151) and its Goal-oriented
Requirement Language (GRL). `src/goalcat/grl/jucm_io.py` loads them through `pyecore` (a Python
EMF implementation), so `.jucm` files are parsed and serialized against the actual metamodel
rather than a hand-derived re-implementation of it.

## Contents

Only the `.ecore` schemas, at the relative paths they occupy in jUCMNavPlus. The files
cross-reference each other through relative paths baked into them (e.g.
`../../../../../ca.mcgill.sel.core/model/CORE.ecore`), so the directory mirrors that layout
instead of flattening it:

```
jucmnav/
├── ca.mcgill.sel.core/model/CORE.ecore   # referenced by the jUCMNav schemas; must resolve
└── seg.jUCMNav/src/seg/jUCMNav/emf/
    ├── grl.ecore            # Goal-oriented Requirement Language — this project's target
    ├── urncore.ecore        # shared URN base types (URNmodelElement, GRLmodelElement, ...)
    ├── urn.ecore            # URNspec root: combines grlspec, ucmspec, and asdspec
    ├── ucm.ecore            # Use Case Maps           ┐
    ├── ucmscenarios.ecore   # UCM scenario definitions │ unused; loaded only so that
    ├── asd.ecore            # aspect-oriented scenarios│ urn.ecore / grl.ecore resolve
    └── fm.ecore             # feature models          ┘
```

No Java source, generated code, or build tooling. The files are read-only reference data for
`pyecore` and are never edited here.

## Why not the `pm4py_ucm` package

`pm4py_ucm` (process mining over Use Case Maps; not declared in `pyproject.toml` and imported by no
module here) was evaluated first and has **no GRL support**: its `.jucm` importer skips `grlspec` and its exporter
writes an empty one. Its documentation described GRL synthesis as an unimplemented design proposal
when these files were vendored (see `src/goalcat/grl/__init__.py`'s module docstring).

## License

jUCMNav is licensed under the **Eclipse Public License, version 1.0** (`seg.jUCMNav/about.html` in
the source repository: *"usecasemaps.org makes available all content in this plug-in ... under the
terms and conditions of the Eclipse Public License Version 1.0"*). Only schema definitions are
vendored: data read at runtime to validate and serialize `.jucm` documents, not executable code
linked into GoalCat's AGPL-3.0-or-later codebase. This mirrors the isolation of the other
differently-licensed vendored component, [`third_party/lupin/`](../lupin/README.md).

## Provenance

Fetched on 2026-08-19 from `https://github.com/JUCMNAV/jUCMNavPlus` (branch `master`) through the
GitHub API, at the commit current when `src/goalcat/grl/` was built. Not synchronized
automatically; re-fetch manually if the upstream schema changes and this project needs to follow.

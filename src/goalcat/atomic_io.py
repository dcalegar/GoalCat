"""Crash-safe file writing: every pipeline artifact is written to a temp file in its own target
directory, then atomically renamed into place via `os.replace()` — a process killed mid-write
leaves either the complete prior file (if any) or nothing at the real path, never a truncated one.

Without this, a process killed while `to_csv()`/`write_text()` is still running leaves a partial
file at the real path; `pandas.read_csv()` in particular does not detect this — it silently drops
an incomplete trailing row instead of raising, so a later run resuming against the same run
directory (`pipeline.py`'s `_get_or_build_*()`, `llm/assignment.py`'s `load_prior_assignments()`)
would load a silently short table instead of failing loudly (verified directly: sweeping 33
truncation points on a real 846-row `variants.csv` produced 33/33 silent partial loads, zero
exceptions). `os.replace()` is used, not `Path.rename()`, because it overwrites an existing
destination atomically on both POSIX and Windows; `Path.rename()`'s Windows behavior on an
existing destination is platform-dependent.
"""

from __future__ import annotations

import contextlib
import json
import os
import secrets
from pathlib import Path
from typing import Any, Iterator

import pandas as pd


@contextlib.contextmanager
def atomic_output_path(path: Path) -> Iterator[Path]:
    """Yields a temp path in `path`'s own directory (so the final `os.replace()` is same-
    filesystem and therefore atomic); on a clean exit, replaces `path` with what was written to
    it. On an exception, the temp file is removed and `path` is left exactly as it was before —
    for a caller that needs to write through a library function taking a plain path string (e.g.
    `pm4py.write_pnml`), not just text/CSV/JSON.

    The temp name keeps `path`'s full filename intact as its own suffix (`.{token}.{path.name}`,
    e.g. `.a1b2c3d4.residual.xes.gz`) rather than appending a generic `.tmp` — several pm4py
    writers (`write_pnml`, `write_xes`, `save_vis_dfg`) infer their output format by checking
    `file_path.lower().endswith(...)` and silently append their own expected extension when that
    check fails, which would have made them write to a *different*, wrong path (e.g.
    `...tmp.pnml`) than the one this context manager renames from.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.parent / f".{secrets.token_hex(8)}.{path.name}"
    try:
        yield tmp_path
    except BaseException:
        tmp_path.unlink(missing_ok=True)
        raise
    else:
        os.replace(tmp_path, path)


def atomic_write_text(path: Path, content: str, encoding: str = "utf-8") -> None:
    with atomic_output_path(path) as tmp:
        tmp.write_text(content, encoding=encoding)


def atomic_write_json(path: Path, obj: Any, *, indent: int = 2, **json_kwargs: Any) -> None:
    atomic_write_text(path, json.dumps(obj, indent=indent, **json_kwargs), encoding="utf-8")


def atomic_write_csv(df: pd.DataFrame, path: Path, **to_csv_kwargs: Any) -> None:
    with atomic_output_path(path) as tmp:
        df.to_csv(tmp, **to_csv_kwargs)


def atomic_write_parquet(df: pd.DataFrame, path: Path, **to_parquet_kwargs: Any) -> None:
    with atomic_output_path(path) as tmp:
        df.to_parquet(tmp, **to_parquet_kwargs)

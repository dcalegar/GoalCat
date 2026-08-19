"""Read-only access to already-produced pipeline artifacts under data/output/, for the
"Resultados"/"Revisión"/"Historial" pages. No pipeline logic here — every path is derived from
goalcat.config's own dirname constants, and every load is a plain file read."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from goalcat.config import REPO_ROOT, ROUND_PREFIX, REVIEW_DIRNAME
from goalcat.llm.taxonomy import Taxonomy

OUTPUT_ROOT = REPO_ROOT / "data" / "output"


def list_log_stems() -> list[str]:
    if not OUTPUT_ROOT.is_dir():
        return []
    return sorted(p.name for p in OUTPUT_ROOT.iterdir() if p.is_dir())


def list_run_ids(log_stem: str) -> list[str]:
    log_dir = OUTPUT_ROOT / log_stem
    if not log_dir.is_dir():
        return []
    return sorted((p.name for p in log_dir.iterdir() if p.is_dir()), reverse=True)


def run_output_dir(log_stem: str, run_id: str) -> Path:
    return OUTPUT_ROOT / log_stem / run_id


def round_dir(run_dir: Path, round_num: int) -> Path:
    return run_dir / f"{ROUND_PREFIX}{round_num}"


def list_rounds(run_dir: Path) -> list[dict]:
    """Same round_info.json scan as goalcat.review.list_rounds(), keyed off a bare
    run_output_dir Path instead of a full PipelineConfig — the GUI browses runs it never created
    itself (e.g. from an experimentation/examples/*/example_run.py script), which don't necessarily carry
    every PipelineConfig field needed to construct one."""
    if not run_dir.is_dir():
        return []
    round_numbers = []
    for entry in run_dir.iterdir():
        if entry.is_dir() and entry.name.startswith(ROUND_PREFIX):
            suffix = entry.name[len(ROUND_PREFIX):]
            if suffix.isdigit():
                round_numbers.append(int(suffix))
    rounds = []
    for n in sorted(round_numbers):
        info_path = run_dir / f"{ROUND_PREFIX}{n}" / REVIEW_DIRNAME / "round_info.json"
        if info_path.exists():
            rounds.append(json.loads(info_path.read_text(encoding="utf-8")))
    return rounds


def read_json(path: Path) -> dict | None:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def read_text(path: Path) -> str | None:
    return path.read_text(encoding="utf-8") if path.exists() else None


def read_csv(path: Path) -> pd.DataFrame | None:
    return pd.read_csv(path) if path.exists() else None


def read_taxonomy(path: Path) -> Taxonomy | None:
    if not path.exists():
        return None
    return Taxonomy.model_validate_json(path.read_text(encoding="utf-8"))


def config_snapshot(run_dir: Path) -> dict | None:
    return read_json(run_dir / "run_config_snapshot.json")

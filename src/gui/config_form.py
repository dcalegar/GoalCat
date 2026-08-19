"""Config-building helpers for the "Nueva corrida" page — no Streamlit imports here, so this
stays testable/reusable independent of the widget layer."""

from __future__ import annotations

from pathlib import Path

import yaml

from goalcat.config import REPO_ROOT

LOGS_DIR = REPO_ROOT / "data" / "logs"
GOALS_DIR = REPO_ROOT / "data" / "goals"
EXPERIMENTATION_DIR = REPO_ROOT / "experimentation" / "examples"
DEFAULT_CONFIG_PATH = REPO_ROOT / "src" / "goalcat" / "config.yaml"
OUTPUT_DIR_NAME = "data/output"


def list_log_filenames() -> list[str]:
    if not LOGS_DIR.is_dir():
        return []
    return sorted(p.name for p in LOGS_DIR.glob("*.xes.gz"))


def list_goal_model_filenames() -> list[str]:
    if not GOALS_DIR.is_dir():
        return []
    return sorted(p.name for p in GOALS_DIR.glob("*.md"))


def find_default_config_for_log(log_filename: str) -> Path:
    """Looks for a case-study config under experimentation/examples/<case>/config*.yaml whose
    log_filename matches, so the form starts from a known-good config instead of bare defaults.
    Falls back to the top-level src/goalcat/config.yaml (rtfm.xes.gz) otherwise. Does not search
    experimentation/icpm2027/ — that package holds the paper's frozen protocol runs, not
    illustrative per-log defaults."""
    if EXPERIMENTATION_DIR.is_dir():
        for case_dir in sorted(EXPERIMENTATION_DIR.iterdir()):
            if not case_dir.is_dir():
                continue
            for candidate in sorted(case_dir.glob("config*.yaml")):
                try:
                    raw = yaml.safe_load(candidate.read_text(encoding="utf-8"))
                except yaml.YAMLError:
                    continue
                if isinstance(raw, dict) and raw.get("log_filename") == log_filename:
                    return candidate
    return DEFAULT_CONFIG_PATH


def load_config_dict(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def log_stem_of(log_filename: str) -> str:
    """Mirrors goalcat.config's own (private) log-stem stripping, so run_output_dir is
    computable here before load_config() ever runs — the GUI needs the destination path to write
    gui_run_config.yaml into it, before that file exists."""
    for suffix in (".xes.gz", ".xes"):
        if log_filename.endswith(suffix):
            return log_filename[: -len(suffix)]
    return Path(log_filename).stem


def run_output_dir_for(log_filename: str, run_id: str) -> Path:
    return REPO_ROOT / OUTPUT_DIR_NAME / log_stem_of(log_filename) / run_id


def build_config_dict(
    *,
    log_filename: str,
    goal_model_filename: str | None,
    case_id_key: str,
    activity_key: str,
    timestamp_key: str,
    resource_key: str,
    sample_frequent_n: int,
    sample_rare_n: int,
    sample_extreme_n: int,
    taxonomy_mode: str,
    discovery_noise_threshold: float,
    llm: dict,
) -> dict:
    return {
        "log_filename": log_filename,
        "goal_model_filename": goal_model_filename,
        "output_dir": OUTPUT_DIR_NAME,
        "run_id": None,
        "round": None,
        "case_id_key": case_id_key,
        "activity_key": activity_key,
        "timestamp_key": timestamp_key,
        "resource_key": resource_key,
        "sample_frequent_n": sample_frequent_n,
        "sample_rare_n": sample_rare_n,
        "sample_extreme_n": sample_extreme_n,
        "taxonomy_mode": taxonomy_mode,
        "discovery_noise_threshold": discovery_noise_threshold,
        "llm": llm,
    }


def write_run_config(config_dict: dict, path: Path) -> None:
    """Writes a fresh YAML for this run only — never overwrites a versioned config.yaml."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(config_dict, sort_keys=False), encoding="utf-8")

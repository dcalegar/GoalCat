from __future__ import annotations

import json
import logging
import subprocess
import sys
from pathlib import Path

import pandas as pd

from ..config import REPO_ROOT, PipelineConfig

_LUPIN_SCRIPT = REPO_ROOT / "third_party" / "lupin" / "render_narratives.py"


def build_lupin_input(profiles_df: pd.DataFrame, config: PipelineConfig) -> list[dict]:
    """Translate the Step 2 profile table into the vendored renderer's generic JSON contract."""
    records = []
    for _, row in profiles_df.iterrows():
        events = [
            {
                "activity": event["activity"],
                "resource": event["resource"],
                "waiting_seconds": round(event["waiting_seconds"]),
            }
            for event in row["events"]
        ]
        trace_attrs = {
            "outcome": row["outcome"],
            "frequency": int(row["frequency"]),
            "frequency_pct_display": round(row["frequency_pct"] * 100, 1),
            "duration_seconds_median": round(row["duration_seconds_median"]),
            "rework_summary": _format_rework(row["rework"]),
        }
        records.append({"variant_id": row["variant_id"], "events": events, "trace_attrs": trace_attrs})
    return records


def _format_rework(rework: dict) -> str:
    if not rework:
        return ""
    parts = [f"{activity} was repeated (seen in {count} cases)" for activity, count in rework.items()]
    return "Rework observed: " + "; ".join(parts) + "."


def render_narratives(profiles_df: pd.DataFrame, config: PipelineConfig, logger: logging.Logger) -> pd.DataFrame:
    """Invoke the vendored LUPIN renderer as a subprocess (pipeline Step 3)."""
    input_path = config.textualization_dir / "lupin_input.json"
    output_path = config.textualization_dir / "lupin_output.json"
    input_path.parent.mkdir(parents=True, exist_ok=True)

    with open(input_path, "w", encoding="utf-8") as f:
        json.dump(build_lupin_input(profiles_df, config), f, indent=2)

    result = subprocess.run(
        [
            sys.executable,
            str(_LUPIN_SCRIPT),
            "--input",
            str(input_path),
            "--output",
            str(output_path),
            "--log",
            config.log_stem,
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        logger.error("LUPIN textualization subprocess failed: %s", result.stderr)
        result.check_returncode()

    with open(output_path, "r", encoding="utf-8") as f:
        narratives = json.load(f)

    return pd.DataFrame(narratives)


def save_narratives(narratives_df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    narratives_df.to_csv(path, index=False)


def load_narratives(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, dtype={"variant_id": str})

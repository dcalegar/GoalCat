"""Runs pipeline steps in a fresh process, on behalf of the GUI. Invoked as
`python -m gui.worker`, never imported — see gui/run_control.py's module docstring for why this
needs to be a subprocess rather than an in-process call.

Steps 1-8 are chained exactly like experimentation/examples/*/example_run.py: one shared run_id, each
step's DataFrame passed into the next. "9" runs Step 9 alone (a merge/split decision re-runs
Steps 6-8 internally, via goalcat.review.start_revision_round — this process's own gui_status.json
only tracks Step 9 itself; progress during that internal re-run is only visible via pipeline.log).
"""

from __future__ import annotations

import argparse
import json
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, TypeVar

from goalcat.config import load_config
from goalcat.pipeline import (
    run_step1_variants,
    run_step2_profiling,
    run_step3_textualization,
    run_step4_sampling,
    run_step5_taxonomy,
    run_step6_assignment,
    run_step7_discovery,
    run_step7b_indicators,
    run_step8_description,
    run_step9_review,
)

from gui.run_control import STEP_NAMES, STATUS_FILENAME

T = TypeVar("T")


def _write_status(path: Path, state: dict) -> None:
    """Atomic write (temp file + replace) so a concurrent reader (the Streamlit process polling
    this file) never observes a half-written JSON document."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, indent=2), encoding="utf-8")
    tmp.replace(path)


def _run_step(step: int | str, fn: Callable[[], T], state: dict, status_path: Path) -> T:
    def mark(phase: str, error: str | None = None) -> None:
        state["steps"][str(step)] = {
            "name": STEP_NAMES[step],
            "state": phase,
            "at": datetime.now(timezone.utc).isoformat(),
            "error": error,
        }
        _write_status(status_path, state)

    mark("running")
    try:
        result = fn()
    except Exception as exc:  # noqa: BLE001 — surfaced verbatim to the GUI, not reinterpreted
        mark("error", error=str(exc))
        raise
    mark("done")
    return result


def run_pipeline_steps_1_8(config_path: Path, run_id: str, status_path: Path) -> None:
    """Steps 1 through 8, plus the optional Step 7b between 7 and 8. The name keeps saying "1_8"
    because 7b is not a step of its own in the numbering — it is skipped silently on a goal model
    with no measurable indicator, and turned off entirely by `skip_indicators`."""
    state: dict = {"run_id": run_id, "steps": {}}

    variants_df = _run_step(1, lambda: run_step1_variants(config_path, run_id), state, status_path)
    profiles_df = _run_step(2, lambda: run_step2_profiling(config_path, run_id, variants_df), state, status_path)
    narratives_df = _run_step(
        3, lambda: run_step3_textualization(config_path, run_id, profiles_df), state, status_path
    )
    _run_step(4, lambda: run_step4_sampling(config_path, run_id, profiles_df, narratives_df), state, status_path)
    _run_step(5, lambda: run_step5_taxonomy(config_path, run_id), state, status_path)
    _run_step(6, lambda: run_step6_assignment(config_path, run_id), state, status_path)
    _run_step(7, lambda: run_step7_discovery(config_path, run_id), state, status_path)
    # Step 7b is optional and a no-op on a goal model with no measurable indicator, so it is
    # always in the chain rather than conditioned here; skip_indicators turns it off.
    _run_step("7b", lambda: run_step7b_indicators(config_path, run_id), state, status_path)
    _run_step(8, lambda: run_step8_description(config_path, run_id), state, status_path)

    # Steps 5-8 alone never write round_info.json — only process_review() does, the first time
    # Step 9 runs for a round (see goalcat/review.py's _load_or_init_round_info). Without this
    # call, the GUI's own Results/Review pages (which key off round_info.json existing) would show
    # nothing for a round that in fact just finished Steps 1-8. Called with no review_decisions.yaml
    # present yet, this only writes review_index.md + the decision template (goalcat/review.py's
    # process_review, "awaiting_review" branch) — no LLM call, so it can't introduce a new failure
    # mode here. Not tracked as its own numbered step: it's "opening" the round for review, not the
    # human's Step 9 decision, which stays a separate, explicit action on the GUI's Review page.
    run_step9_review(config_path, run_id, 1)


def run_pipeline_step_9(config_path: Path, run_id: str, round_: int, status_path: Path) -> None:
    state: dict = {"run_id": run_id, "round": round_, "steps": {}}
    _run_step(9, lambda: run_step9_review(config_path, run_id, round_), state, status_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="GoalCat GUI pipeline worker (internal use).")
    parser.add_argument("--config", required=True, help="Path to a config.yaml-shaped file.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--round", type=int, default=None)
    parser.add_argument("--steps", required=True, choices=["1-8", "9"])
    args = parser.parse_args()

    config_path = Path(args.config)

    try:
        if args.steps == "1-8":
            config = load_config(config_path, args.run_id)
            status_path = config.run_output_dir / STATUS_FILENAME
            run_pipeline_steps_1_8(config_path, args.run_id, status_path)
        else:
            config = load_config(config_path, args.run_id, args.round)
            status_path = config.round_dir / STATUS_FILENAME
            run_pipeline_step_9(config_path, args.run_id, config.round, status_path)
    except Exception:
        # Already recorded in gui_status.json by _run_step()'s mark("error", ...) — this
        # traceback goes to gui_worker_stdout.log (this process's stdout, redirected by
        # run_control.launch_worker) as a fallback for whatever _run_step() couldn't capture
        # (e.g. load_config() itself failing, before any step runs).
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

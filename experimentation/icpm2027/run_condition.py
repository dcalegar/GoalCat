"""MAIN — executes the pipeline steps of exactly one frozen condition, in its own process.

Invoked by conditions.py as a subprocess:

    python -m experimentation.icpm2027.run_condition \
        --config data/output/rtfm/icpm2027_e1_guided_rep1/condition_config.yaml \
        --run-id icpm2027_e1_guided_rep1 --steps 5,6

One process per condition, for the reason `src/gui/run_control.py` already documents:
`goalcat.run_logging.get_logger()` caches the "goalcat" logger and its file handler at process
scope, so a single driver process running several conditions in sequence would funnel every
condition's `pipeline.log` into the first condition's run directory. For a replication package
that is not a cosmetic problem — Task C9 reads per-step timings and per-call latencies straight
out of `pipeline.log`, and those numbers have to be attributable to one condition.

Runnable directly, too: re-running a single condition after a transport failure is just this
command against the same `--run-id`, which resumes from that run directory's partial
`assignments.csv` (see `load_prior_assignments` in `goalcat/llm/assignment.py`).

Step 9 is rejected outright — §3's paired comparison is defined to run *before* any analyst
merge/split/rename, so no frozen condition may reach it.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from goalcat.config import load_config
from goalcat.pipeline import (
    run_step5_taxonomy,
    run_step6_assignment,
    run_step7_discovery,
    run_step7b_indicators,
    run_step8_description,
)
from goalcat.run_logging import get_logger

#: Steps this entrypoint is allowed to run. 1-4 are excluded because a frozen condition inherits
#: them from the shared base (inputs.py) and must never recompute them; 9 is excluded by protocol.
#:
#: Step 7b is deliberately NOT in this table and is not selectable through `--steps`. It is not a
#: free choice: Task C13 pre-registers it as guided-arm-only (open categories carry no anchor_ids,
#: so there is nothing to attach an indicator to) and RTFM-only (no other goal model declares a
#: measurable indicator). It is therefore driven by its own `--indicators` flag, which the driver
#: sets from the resolved C13 decision rather than from a step list anyone could edit.
_STEP_FUNCTIONS = {
    5: run_step5_taxonomy,
    6: run_step6_assignment,
    7: run_step7_discovery,
    8: run_step8_description,
}


def parse_steps(spec: str) -> list[int]:
    steps = [int(part) for part in spec.split(",") if part.strip()]
    invalid = [s for s in steps if s not in _STEP_FUNCTIONS]
    if invalid:
        raise SystemExit(
            f"Steps {invalid} cannot run in a frozen condition. Allowed: "
            f"{sorted(_STEP_FUNCTIONS)} — Steps 1-4 are inherited from the shared base "
            "(experimentation/icpm2027/inputs.py) and Step 9 is excluded by protocol "
            "(the comparison runs before any analyst refinement)."
        )
    return sorted(steps)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--config", required=True, type=Path, help="Generated condition_config.yaml")
    parser.add_argument("--run-id", required=True, help="Run directory name under data/output/<log_stem>/")
    parser.add_argument("--steps", default="5,6", help="Comma-separated subset of 5,6,7,8 (default: 5,6)")
    parser.add_argument("--round", type=int, default=1, help="Round to write into (frozen runs use 1)")
    parser.add_argument(
        "--indicators",
        action="store_true",
        help="Also run Step 7b (indicator satisfaction) after Step 6 — Task C13, guided arm only",
    )
    args = parser.parse_args(argv)

    steps = parse_steps(args.steps)
    config = load_config(args.config, args.run_id, args.round)
    logger = get_logger(config)
    logger.info(
        "ICPM 2027 condition run starting: run_id=%s, steps=%s, taxonomy_mode=%s, goal_model=%s",
        args.run_id, steps, config.taxonomy_mode, config.goal_model_filename,
    )

    for step in steps:
        _STEP_FUNCTIONS[step](args.config, args.run_id, round=args.round)

    if args.indicators:
        if config.taxonomy_mode != "intent_guided":
            # Belt and braces: the driver already refuses this, but a hand-run subprocess must not
            # be able to produce an "indicator" result for an arm that has no anchors to measure.
            raise SystemExit(
                "Step 7b requires taxonomy_mode=intent_guided (Task C13): open-mode categories "
                f"carry no anchor_ids to attach an indicator to, but this run is {config.taxonomy_mode!r}."
            )
        logger.info("Task C13: running Step 7b (indicator satisfaction) for run_id=%s", args.run_id)
        run_step7b_indicators(args.config, args.run_id, round=args.round)

    logger.info("ICPM 2027 condition run complete: run_id=%s", args.run_id)
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Runnable case study: the full GoalCat pipeline (Steps 1-9) against bpic2020_permit.

Unlike experimentation/examples/rtfm_mini/example_run.py, this script does not script a rework loop
through Step 9's revise path — it stands in for a business expert who accepts the induced
taxonomy outright, on the first round, with no edits. Step 9 is designed for a human reviewer
reading review_index.md and hand-editing review_decisions.yaml (see review.py's process_review
docstring); here that decision is written directly as decision="accept" and Step 9 is invoked
once.

Uses its own config_bpic2020_permit.yaml, alongside this script under
experimentation/examples/bpic2020_permit/ — one subdirectory per log in data/logs/, so each case study is
self-contained. Invoke it as a module, not as a loose script: `python -m experimentation.examples.bpic2020_permit.example_run` (experimentation.examples is its
a subpackage of experimentation (itself a top-level package living at the repository root, alongside src/ — see README.md's repository layout). Requires
GEMINI_API_KEY in the environment (see llm/llm_backend.py).
"""

from __future__ import annotations

from pathlib import Path

import yaml

from goalcat.config import load_config, new_run_id
from goalcat.pipeline import (
    run_step1_variants,
    run_step2_profiling,
    run_step3_textualization,
    run_step4_sampling,
    run_step5_taxonomy,
    run_step6_assignment,
    run_step7_discovery,
    run_step8_description,
    run_step9_review,
)
from goalcat.review import ReviewDecisions
from goalcat.run_logging import get_logger

CONFIG_PATH = Path(__file__).with_name("config_bpic2020_permit.yaml")


def _write_accept_decision(config_path: Path, run_id: str, round_num: int, logger) -> None:
    """Direct expert acceptance: writes decision="accept" for the round just reached, no
    renames/merges/splits — the taxonomy Step 5-8 produced is taken as final on the first pass."""
    config = load_config(config_path, run_id, round_num)
    decisions = ReviewDecisions(decision="accept")

    decisions_path = config.review_dir / "review_decisions.yaml"
    decisions_path.parent.mkdir(parents=True, exist_ok=True)
    decisions_path.write_text(yaml.safe_dump(decisions.model_dump(mode="json"), sort_keys=False), encoding="utf-8")
    logger.info("Round %d: wrote direct-acceptance decision.", round_num)


def main() -> None:
    run_id = new_run_id()
    config = load_config(CONFIG_PATH, run_id)
    logger = get_logger(config)
    logger.info("example_run: starting full pipeline for bpic2020_permit, run_id=%s", run_id)

    variants_df = run_step1_variants(CONFIG_PATH, run_id)
    profiles_df = run_step2_profiling(CONFIG_PATH, run_id, variants_df)
    narratives_df = run_step3_textualization(CONFIG_PATH, run_id, profiles_df)
    run_step4_sampling(CONFIG_PATH, run_id, profiles_df, narratives_df)

    run_step5_taxonomy(CONFIG_PATH, run_id)
    run_step6_assignment(CONFIG_PATH, run_id)
    run_step7_discovery(CONFIG_PATH, run_id)
    run_step8_description(CONFIG_PATH, run_id)

    _write_accept_decision(CONFIG_PATH, run_id, round_num=1, logger=logger)
    result = run_step9_review(CONFIG_PATH, run_id, 1)
    if result["status"] != "accepted":
        raise RuntimeError(f"Expected Step 9 to accept on round 1, got status {result['status']!r}.")

    logger.info("example_run complete. run_id=%s, accepted on round 1.", run_id)


if __name__ == "__main__":
    main()

"""Runnable case study: the full GoalCat pipeline (Steps 1-9) against rtfm_mini, including a
scripted rework loop through Step 9's revise -> new round -> Steps 5-8 re-run mechanism.

Step 9 is designed for a human reviewer reading review_index.md and hand-editing
review_decisions.yaml (see review.py's process_review docstring) — this script stands in for
that reviewer so the whole case study can run unattended: it always writes a real, schema-valid
decision for the round it just reached, then calls run_step9_review() to process it. It never
relies on the auto-written default template (decision: revise with no edits) being valid on its
own — it isn't, by ReviewDecisions' own model validator.

Uses its own config_mini.yaml — moved here from src/goalcat/, since the tiny rtfm_mini fixture
configuration belongs to this case study rather than to the library — so the study is
self-contained. Invoke it as a module, not as a loose script: the imports above are relative to
the goalcat package (`python -m goalcat.experimentation.example_run`). Requires GEMINI_API_KEY in
the environment (see llm/llm_backend.py).
"""

from __future__ import annotations

from pathlib import Path

import yaml

from ..config import load_config, new_run_id
from ..llm.taxonomy import Taxonomy
from ..pipeline import (
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
from ..review import MergeDecision, ReviewDecisions
from ..run_logging import get_logger

CONFIG_PATH = Path(__file__).with_name("config_mini.yaml")
MAX_REWORK_ROUNDS = 5


def _write_scripted_decision(config_path: Path, run_id: str, round_num: int, round_index: int, logger) -> None:
    """round_index 0 (first round reached) requests a merge of the taxonomy's first two
    categories, to genuinely exercise the revise path end-to-end; every later round accepts, so
    the loop converges in exactly two rounds."""
    config = load_config(config_path, run_id, round_num)
    taxonomy = Taxonomy.model_validate_json((config.taxonomy_dir / "taxonomy.json").read_text(encoding="utf-8"))

    if round_index == 0:
        if len(taxonomy.categories) < 2:
            raise RuntimeError(
                f"Rework-loop demo needs >=2 induced categories to request a merge, got "
                f"{len(taxonomy.categories)} in run {run_id} round {round_num}."
            )
        a, b = taxonomy.categories[0].category_id, taxonomy.categories[1].category_id
        decisions = ReviewDecisions(
            decision="revise",
            merges=[
                MergeDecision(
                    category_ids=[a, b],
                    reason=(
                        "Scripted rework-loop demonstration (experimentation/example_run.py): "
                        f"merging the first two induced categories ({a}, {b}) to exercise Step 9's "
                        "revise path end-to-end (new round, Steps 5-8 re-run)."
                    ),
                )
            ],
        )
    else:
        decisions = ReviewDecisions(decision="accept")

    decisions_path = config.review_dir / "review_decisions.yaml"
    decisions_path.parent.mkdir(parents=True, exist_ok=True)
    decisions_path.write_text(yaml.safe_dump(decisions.model_dump(mode="json"), sort_keys=False), encoding="utf-8")
    logger.info("Rework loop round %d: wrote scripted decision (%s)", round_num, decisions.decision)


def run_rework_loop(config_path: Path, run_id: str, logger) -> int:
    """Drives Step 9 to convergence: writes a scripted decision for the current round, invokes
    Step 9 to process it, and follows into any newly created round until one is accepted."""
    current_round = 1
    for round_index in range(MAX_REWORK_ROUNDS):
        _write_scripted_decision(config_path, run_id, current_round, round_index, logger)
        result = run_step9_review(config_path, run_id, current_round)

        if result["status"] == "accepted":
            logger.info("Rework loop converged: run %s round %d accepted.", run_id, current_round)
            return current_round
        if result["status"] == "revised":
            current_round = result["round"]
            continue
        raise RuntimeError(f"Unexpected Step 9 status: {result['status']!r} (run {run_id}, round {current_round})")

    raise RuntimeError(
        f"Rework loop did not converge within {MAX_REWORK_ROUNDS} rounds "
        f"(stuck at run {run_id}, round {current_round})."
    )


def main() -> None:
    run_id = new_run_id()
    config = load_config(CONFIG_PATH, run_id)
    logger = get_logger(config)
    logger.info("example_run: starting full pipeline for rtfm_mini, run_id=%s", run_id)

    variants_df = run_step1_variants(CONFIG_PATH, run_id)
    profiles_df = run_step2_profiling(CONFIG_PATH, run_id, variants_df)
    narratives_df = run_step3_textualization(CONFIG_PATH, run_id, profiles_df)
    run_step4_sampling(CONFIG_PATH, run_id, profiles_df, narratives_df)

    run_step5_taxonomy(CONFIG_PATH, run_id)
    run_step6_assignment(CONFIG_PATH, run_id)
    run_step7_discovery(CONFIG_PATH, run_id)
    run_step8_description(CONFIG_PATH, run_id)

    final_round = run_rework_loop(CONFIG_PATH, run_id, logger)
    logger.info("example_run complete. run_id=%s, final accepted round=%d", run_id, final_round)


if __name__ == "__main__":
    main()

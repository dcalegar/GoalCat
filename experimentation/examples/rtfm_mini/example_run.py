"""Runnable case study: the full GoalCat pipeline (Steps 1-9) against rtfm_mini, including a
scripted rework loop through Step 9's revise -> new round -> Steps 5-8 re-run mechanism.

Step 9 is designed for a human reviewer reading review_index.md and hand-editing
review_decisions.yaml (see review.py's process_review docstring) — this script stands in for
that reviewer so the whole case study can run unattended: it always writes a real, schema-valid
decision for the round it just reached, then calls run_step9_review() to process it. It never
relies on the auto-written default template (decision: revise with no edits) being valid on its
own — it isn't, by ReviewDecisions' own model validator.

Uses its own config_mini.yaml, alongside this script under experimentation/examples/rtfm_mini/ — one
subdirectory per log in data/logs/, so each case study is self-contained. Invoke it as a module,
not as a loose script: `python -m experimentation.examples.rtfm_mini.example_run` (experimentation.examples is its
a subpackage of experimentation (itself a top-level package living at the repository root, alongside src/ — see README.md's repository layout). Requires GEMINI_API_KEY in the
environment (see llm/llm_backend.py).
"""

from __future__ import annotations

from pathlib import Path

import yaml

from goalcat import grl
from goalcat.config import load_config, new_run_id
from goalcat.llm.taxonomy import Taxonomy
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
from goalcat.review import MergeDecision, ReviewDecisions
from goalcat.run_logging import get_logger

CONFIG_PATH = Path(__file__).with_name("config_mini.yaml")
MAX_REWORK_ROUNDS = 5


def _mergeable_pair(taxonomy: Taxonomy, model: grl.GRLModel) -> tuple[str, str, str] | None:
    """First pair of categories (in taxonomy order) that Step 5a's `check_axis_partition` will
    accept as one merged category: every anchor of both categories must be a child of the *same*
    Or-decomposed parent. Anchors under different decomposition points, or under an Xor point
    (mutually exclusive by ITU-T Z.151), are rejected by that check and would abort the revision
    round — the RTFM goal model's `Resolve via timely payment` (id 12, under Or 4) can never be
    merged with the enforcement closures (ids 13/20, under Or 6), and the two appeals (14/19)
    are Xor siblings. Returns (category_id_a, category_id_b, parent_id), or None if no such pair
    exists."""
    for i, a in enumerate(taxonomy.categories):
        for b in taxonomy.categories[i + 1 :]:
            anchors = list(a.anchor_ids) + list(b.anchor_ids)
            if not anchors:
                continue
            parents = {model.parent_of(anchor) for anchor in anchors}
            if len(parents) != 1:
                continue
            parent_id = next(iter(parents))
            parent = model.elements.get(parent_id) if parent_id is not None else None
            if parent is not None and parent.decomposition_type == "Or":
                return a.category_id, b.category_id, parent_id
    return None


def _write_scripted_decision(config_path: Path, run_id: str, round_num: int, round_index: int, logger) -> None:
    """round_index 0 (first round reached) requests a merge of two induced categories, to
    genuinely exercise the revise path end-to-end; every later round accepts, so the loop
    converges in exactly two rounds. The pair is not simply the first two categories: the LLM
    returns categories in an arbitrary order, and Step 5a rejects a merge whose anchors span two
    decomposition points, so the pair is chosen by `_mergeable_pair()` against the goal model."""
    config = load_config(config_path, run_id, round_num)
    taxonomy = Taxonomy.model_validate_json((config.taxonomy_dir / "taxonomy.json").read_text(encoding="utf-8"))

    if round_index == 0:
        if len(taxonomy.categories) < 2:
            raise RuntimeError(
                f"Rework-loop demo needs >=2 induced categories to request a merge, got "
                f"{len(taxonomy.categories)} in run {run_id} round {round_num}."
            )
        model = grl.read_jucm(config.goal_model_path)
        pair = _mergeable_pair(taxonomy, model)
        if pair is None:
            raise RuntimeError(
                f"Rework-loop demo found no pair of categories whose anchors share one Or-decomposed "
                f"parent in run {run_id} round {round_num}; a merge of any two would be rejected by "
                "Step 5a's axis-partition check."
            )
        a, b, parent_id = pair
        decisions = ReviewDecisions(
            decision="revise",
            merges=[
                MergeDecision(
                    category_ids=[a, b],
                    reason=(
                        "Scripted rework-loop demonstration (experimentation/examples/rtfm_mini/example_run.py): "
                        f"merging {a} and {b}, whose anchors are siblings under Or point id={parent_id} "
                        "(the first such pair in taxonomy order, so the merge passes Step 5a's "
                        "axis-partition check), to exercise Step 9's revise path end-to-end "
                        "(new round, Steps 5-8 re-run)."
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
    run_step7b_indicators(CONFIG_PATH, run_id)
    run_step8_description(CONFIG_PATH, run_id)

    final_round = run_rework_loop(CONFIG_PATH, run_id, logger)
    logger.info("example_run complete. run_id=%s, final accepted round=%d", run_id, final_round)


if __name__ == "__main__":
    main()

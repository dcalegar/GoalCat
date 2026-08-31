"""MAIN — the per-dataset driver: runs one dataset's whole experiment from one command.

    python -m experimentation.icpm2027.run_experiment --dataset rtfm --experiment e1
    python -m experimentation.icpm2027.run_experiment --dataset rtfm --experiment e1 --dry-run
    python -m experimentation.icpm2027.run_experiment --dataset rtfm --experiment stability
    python -m experimentation.icpm2027.run_experiment --dataset rtfm --experiment e2

This is orchestration only. Every decision it acts on is resolved from `configs/protocol.yaml` and
`configs/preregistration.yaml`, never from a command-line flag — the one exception being
`--allow-pending-decisions`, which exists so an exploratory run is *possible* but stamps its
manifests as not pre-registered so it can never be mistaken for a frozen result.

Three experiments:

  ``stability``  Task C12, and the cheapest thing here. Re-runs Step 5a alone k times on identical
                 inputs (`replicates.taxonomy_induction`) and reports whether the category and
                 anchor sets reproduce. **Run this first on any dataset whose goal model is mostly
                 AND-decomposed above the leaf level.** If it fails, §4 forbids Experiment 2 on that
                 dataset and Task E7 governs how its Experiment 1 numbers are reported.

  ``e1``         Experiment 1 — the paired guided/open comparison (§3), plus Task C2's replicates,
                 Task C3's structural baseline, and Task C11a's `guided_no_sample` ablation when the
                 arm is requested. Emits the §3 evidence report.

  ``e2``         Experiment 2 — controlled goal-model perturbations (§4). Runs the guided arm once
                 per perturbed model and computes TargetReassignment/CollateralReassignment against
                 the unperturbed guided partition, matching categories by `anchor_ids` rather than
                 by name, since Step 5a is re-run for every perturbation.

Steps 1-4 run exactly once per dataset into a shared base and are copied — never recomputed — into
each condition, which is what makes the freeze table's identical-inputs rows assertable rather than
merely intended. Re-running the driver resumes: a condition whose run directory is already complete
is skipped unless `--force`.

Note that `--dry-run` still builds the shared base if it does not exist. Steps 1-4 are
deterministic and involve no LLM call, and the per-condition call estimate the dry run exists to
report is a function of the variant count they produce. Nothing billable happens in a dry run.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from collections.abc import Collection
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from goalcat.config import REPO_ROOT

from .analysis import report as report_mod
from .analysis.contingency import contingency_matrix
from .analysis.coverage import compute_coverage
from .analysis.divergence import compute_divergence
from .baselines.rule_based_rtfm import run_rule_baseline
from .baselines.structural_clustering import run_structural_clustering
from .conditions import ConditionResult, execute_condition, round_dir_of
from .freeze import check_run_dirs, write_freeze_report
from .goalmodel import perturb
from .inputs import prepare_shared_base
from .protocol import (
    ConditionSpec,
    DatasetSpec,
    PreRegistration,
    PreRegistrationError,
    Protocol,
    shared_base_dir,
)

RESULTS_DIR = REPO_ROOT / "data" / "output" / "icpm2027_results"


def _logger() -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)-7s %(name)s | %(message)s", stream=sys.stdout
    )
    return logging.getLogger("icpm2027.driver")


def _read_assignments(result: ConditionResult) -> pd.DataFrame | None:
    """A condition's Step 6 output, or None if it did not get that far (a dry run, or a
    stability-only condition that ran Step 5 alone)."""
    path = result.round_dir / "06_assignment" / "assignments.csv"
    if not path.exists():
        return None
    return pd.read_csv(path, dtype={"variant_id": str})


def _read_taxonomy(result: ConditionResult) -> dict[str, Any] | None:
    path = result.round_dir / "05_taxonomy" / "taxonomy.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _taxonomy_shape(taxonomy: dict[str, Any]) -> tuple[frozenset[str], frozenset[tuple[str, ...]]]:
    """(category ids, category->anchors grouping) — the two sets Task C12 asks to be reproduced.

    The grouping is the sharper of the two: Sepsis's unstable runs differ in which *level of the
    goal tree* they anchor at, which shows up here even where category names happen to look
    similar. It is a set of sorted anchor tuples, one per category, rather than the flat union over
    all categories this returned previously — a union cannot tell `{A:[15], B:[16]}` from
    `{A:[15,16], B:[]}`, so it would have called a run that collapsed two alternatives into one
    category stable. The frozen artifacts do reproduce a 1:1 mapping on all three logs; the point
    is that the check now demonstrates that rather than assuming it.
    """
    categories = taxonomy.get("categories", [])
    return (
        frozenset(c["category_id"] for c in categories),
        frozenset(tuple(sorted(c.get("anchor_ids") or ())) for c in categories),
    )


def verify_freeze(
    title: str,
    results: dict[str, ConditionResult],
    dataset_id: str,
    stem: str,
    logger: logging.Logger,
    *,
    perturbed: bool = False,
) -> bool:
    """Verifies the freeze table against what the conditions' manifests actually record.

    `protocol.py` makes a pair identical *by construction*; this checks that claim against the
    artifacts afterwards, which is the half that had never run. `freeze.py` was fully implemented
    and never called, and the gap was not hypothetical: Sepsis's `e1_open_rep1` was executed
    against an uncommitted edit to `prompt_assignment_batch.txt` and paired against a `guided_rep1`
    that used the previous wording, so the arms differed in two things rather than one. The
    "Assignment mechanism" row here is exactly the row that catches it.

    Returns whether every row passed. Failing rows are logged as errors and the report is written
    either way — a failed verification is evidence, not a reason to produce no record of it.
    """
    run_dirs = {label: result.run_dir for label, result in results.items() if not result.skipped}
    if len(run_dirs) < 2:
        logger.info("Freeze verification skipped for %s: needs at least two conditions.", title)
        return True
    checks = check_run_dirs(run_dirs, perturbed=perturbed)
    path = write_freeze_report(title, checks, RESULTS_DIR / dataset_id, stem)
    failed = [c for c in checks if not c.passed]
    for check in failed:
        logger.error("Freeze row FAILED (%s): %s — %s", title, check.element, check.values)
    if failed:
        logger.error(
            "%d of %d freeze rows failed for %s; see %s. These conditions do not differ in exactly "
            "one step and must not be reported as a paired comparison.",
            len(failed), len(checks), title, path,
        )
    else:
        logger.info("Freeze verification passed %d/%d rows for %s: %s", len(checks), len(checks), title, path)
    return not failed


# --------------------------------------------------------------------------------------------
# Task C12 — Step 5a induction stability
# --------------------------------------------------------------------------------------------


def run_stability(
    dataset: DatasetSpec,
    protocol: Protocol,
    prereg: PreRegistration,
    logger: logging.Logger,
    *,
    pending: list[str],
    dry_run: bool,
    force: bool,
    axis: str | None = None,
) -> report_mod.InductionStability | None:
    """Re-runs Step 5a alone k times on identical inputs (Task C12).

    Deliberately not folded into `run_e1()`: this must be answerable *before* committing a dataset's
    LLM budget to a full paired design, because a negative answer changes how every subsequent
    number from that dataset is reported (Task E7) and disqualifies it from Experiment 2 (§4).
    """
    k = protocol.replicates.get("taxonomy_induction", 5)
    base = prepare_shared_base(dataset, protocol, prereg, logger)
    logger.info("Task C12: %d Step-5a-only reruns for %s", k, dataset.dataset_id)

    shapes: list[tuple[frozenset[str], frozenset[tuple[str, ...]]]] = []
    for replicate in range(1, k + 1):
        condition = ConditionSpec(
            dataset=dataset,
            arm="guided",
            replicate=replicate,
            tag="stability",
            steps=(5,),
            experiment="c12",
            axis=axis,
        )
        result = execute_condition(
            condition, base, protocol, prereg, logger,
            pending_decisions=pending, dry_run=dry_run, force=force,
        )
        taxonomy = _read_taxonomy(result)
        if taxonomy is not None:
            shapes.append(_taxonomy_shape(taxonomy))

    if not shapes:
        return None

    stability = report_mod.InductionStability(
        k=len(shapes),
        category_sets=tuple(s[0] for s in shapes),
        anchor_sets=tuple(s[1] for s in shapes),
    )
    logger.info("Task C12 result for %s: %s", dataset.dataset_id, stability.qualification(dataset.dataset_id))
    return stability


# --------------------------------------------------------------------------------------------
# Experiment 1 — paired guided/open
# --------------------------------------------------------------------------------------------


@dataclass
class Experiment1Result:
    dataset_id: str
    conditions: dict[str, ConditionResult]
    report: report_mod.DatasetReport


def run_e1(
    dataset: DatasetSpec,
    protocol: Protocol,
    prereg: PreRegistration,
    logger: logging.Logger,
    *,
    pending: list[str],
    dry_run: bool,
    force: bool,
    arms: tuple[str, ...],
    stability: report_mod.InductionStability | None,
    axis: str | None = None,
) -> Experiment1Result:
    base = prepare_shared_base(dataset, protocol, prereg, logger)
    replicates = protocol.replicates.get("unperturbed", 2)

    results: dict[str, ConditionResult] = {}
    for arm in arms:
        for replicate in range(1, replicates + 1):
            condition = ConditionSpec(
                dataset=dataset, arm=arm, replicate=replicate, experiment="e1", axis=axis
            )
            results[condition.condition_id] = execute_condition(
                condition, base, protocol, prereg, logger,
                pending_decisions=pending, dry_run=dry_run, force=force,
            )

    dataset_report = report_mod.DatasetReport(
        dataset_id=dataset.dataset_id,
        scope_record=base.scope,
        stability=stability,
        notes=report_mod.KNOWN_FINDINGS.get(dataset.dataset_id, []),
    )
    if dry_run:
        return Experiment1Result(dataset.dataset_id, results, dataset_report)

    axis_suffix = f"_axis{axis}" if axis else ""
    if not verify_freeze(
        f"{dataset.dataset_id} Experiment 1{f' (axis {axis})' if axis else ''}",
        results, dataset.dataset_id, f"freeze_e1{axis_suffix}", logger,
    ):
        raise RuntimeError(
            f"Freeze verification failed for {dataset.dataset_id} Experiment 1 — the conditions do "
            f"not differ in exactly one step. See "
            f"{RESULTS_DIR / dataset.dataset_id / f'freeze_e1{axis_suffix}.md'}. Re-run the "
            "offending condition with --force at a clean commit rather than reporting it."
        )

    variants_df = pd.read_csv(base.run_dir / "01_variants" / "variants.csv", dtype={"variant_id": str})
    assignments = {cid: _read_assignments(r) for cid, r in results.items()}
    assignments = {cid: df for cid, df in assignments.items() if df is not None}

    dataset_report.coverage_reports = [
        compute_coverage(df, variants_df, cid) for cid, df in sorted(assignments.items())
    ]

    guided_id, open_id = "e1_guided_rep1", "e1_open_rep1"
    if guided_id in assignments and open_id in assignments:
        dataset_report.contingency = contingency_matrix(
            assignments[guided_id], assignments[open_id], variants_df, "guided", "open"
        )
        d1 = (
            prereg.get("D1_divergence_convention").value or {}
            if "D1_divergence_convention" in prereg.decisions
            else {}
        )
        dataset_report.divergence = compute_divergence(
            assignments[guided_id], assignments[open_id], variants_df, "guided", "open",
            primary_residual_handling=d1.get("residual_handling", "own_cluster"),
            primary_weighting=d1.get("weighting", "variant"),
        )

    # Task C2 — replicate noise floor. rep1 vs rep2 of each arm, same convention as the paired
    # contrast, so "guided vs open" divergence can be read against how far each arm moves between
    # identical-input runs. The open arm carries no anchors, so this is the only stability signal
    # it has (Task C12 tests the guided taxonomy only).
    d1_resid = d1.get("residual_handling", "own_cluster") if (guided_id in assignments and open_id in assignments) else "own_cluster"
    d1_weight = d1.get("weighting", "variant") if (guided_id in assignments and open_id in assignments) else "variant"
    for arm, attr in (("guided", "guided_replicate_divergence"), ("open", "open_replicate_divergence")):
        r1, r2 = f"e1_{arm}_rep1", f"e1_{arm}_rep2"
        if r1 in assignments and r2 in assignments:
            setattr(dataset_report, attr, compute_divergence(
                assignments[r1], assignments[r2], variants_df, f"{arm}_rep1", f"{arm}_rep2",
                primary_residual_handling=d1_resid, primary_weighting=d1_weight,
            ))

    # Task C3 — the structural baseline. No LLM cost, so it always runs when the guided arm exists.
    if guided_id in assignments:
        structural = run_structural_clustering(variants_df)
        dataset_report.structural_contingency = contingency_matrix(
            assignments[guided_id], structural.as_assignments_df(), variants_df, "guided", "structural (HDBSCAN)"
        )

    # Task C4 — RTFM-only deterministic activity-rule baseline. No LLM cost.
    if guided_id in assignments and dataset.dataset_id == "rtfm":
        rule = run_rule_baseline(variants_df)
        dataset_report.rule_contingency = contingency_matrix(
            assignments[guided_id], rule.as_assignments_df(), variants_df, "guided", "rule baseline"
        )

    # Task C13 — surface Step 7b's indicator-satisfaction report (guided arm; RTFM only per C13).
    _guided = results.get(guided_id)
    if _guided is not None:
        step7b_path = _guided.round_dir / "07b_indicators" / "indicator_report.md"
        if step7b_path.exists():
            dataset_report.step7b_report = step7b_path.read_text(encoding="utf-8")

    # Declared-alternative coverage — guided arm only; open categories have no anchors.
    guided_result = results.get(guided_id)
    if guided_id in assignments and guided_result is not None and dataset.goal_model_filename:
        taxonomy_path = guided_result.round_dir / "05_taxonomy" / "taxonomy.json"
        if taxonomy_path.exists():
            dataset_report.declared_coverage = report_mod.declared_alternative_coverage(
                REPO_ROOT / "data" / "goals" / dataset.goal_model_filename,
                taxonomy_path,
                assignments[guided_id],
                variants_df,
            )

    path = dataset_report.write(RESULTS_DIR / dataset.dataset_id / "experiment1.md")
    logger.info("Wrote Experiment 1 report: %s", path)
    return Experiment1Result(dataset.dataset_id, results, dataset_report)


# --------------------------------------------------------------------------------------------
# Experiment 2 — controlled perturbations
# --------------------------------------------------------------------------------------------


def reassignment_rates(
    baseline: pd.DataFrame,
    perturbed: pd.DataFrame,
    baseline_anchors: dict[str, frozenset[str]],
    perturbed_anchors: dict[str, frozenset[str]],
    target_anchors: Collection[str],
    variants_df: pd.DataFrame,
) -> dict[str, Any]:
    """TargetReassignment and CollateralReassignment (§4), with categories matched by `anchor_ids`.

    Matching by anchor rather than by category id or name is required, not stylistic: §4 re-runs
    Step 5a for every perturbation, so the perturbed taxonomy's category ids are freshly generated
    and may coincide with the baseline's by accident or differ from it while meaning the same thing.
    A variant "changes" if the anchor set behind its category differs, or if it crosses into or out
    of the residual.

    `target_anchors` is every alternative the perturbation touched, which for a merge is **two**.
    Taking only the first (as this function's scalar predecessor did, fed `result.targets[0]`) puts
    every variant realizing the second target into the collateral population, where it is
    guaranteed to move because its element no longer exists — so the second target's movement was
    reported as damage to bystanders. On RTFM's merge that single substitution accounted for 41 of
    the 59 "collateral" variants and inflated the rate from 12.9% to 32.6%.
    """
    target_anchors = set(target_anchors)
    if not target_anchors:
        raise ValueError("reassignment_rates() needs at least one target anchor")
    base_by_variant = dict(zip(baseline["variant_id"], baseline["category_id"]))
    pert_by_variant = dict(zip(perturbed["variant_id"], perturbed["category_id"]))
    freq = dict(zip(variants_df["variant_id"], variants_df["frequency"]))

    def anchors_of(category_id: Any, table: dict[str, frozenset[str]]) -> frozenset[str]:
        if not isinstance(category_id, str):
            return frozenset()  # residual
        return table.get(category_id, frozenset())

    target_variants, other_variants = [], []
    for variant_id, category_id in base_by_variant.items():
        if anchors_of(category_id, baseline_anchors) & target_anchors:
            target_variants.append(variant_id)
        else:
            other_variants.append(variant_id)

    def changed(variant_id: str) -> bool:
        before = anchors_of(base_by_variant.get(variant_id), baseline_anchors)
        after = anchors_of(pert_by_variant.get(variant_id), perturbed_anchors)
        return before != after

    def rate(variants: list[str]) -> dict[str, Any]:
        changed_ids = [v for v in variants if changed(v)]
        return {
            "n": len(variants),
            "changed": len(changed_ids),
            "rate": len(changed_ids) / len(variants) if variants else float("nan"),
            "cases_changed": sum(int(freq.get(v, 0)) for v in changed_ids),
        }

    return {
        "target_anchors": sorted(target_anchors),
        "TargetReassignment": rate(target_variants),
        "CollateralReassignment": rate(other_variants),
        "note": (
            "CollateralReassignment is interpretable only against the replicate noise floor from "
            "Task C2 — without it, collateral change cannot be distinguished from ordinary "
            "run-to-run variance (Experiment 2's design constraint)."
        ),
    }


def replicate_reassignment_null(
    replicates: list[tuple[pd.DataFrame, dict[str, frozenset[str]]]],
    target_anchors: Collection[str],
    variants_df: pd.DataFrame,
) -> dict[str, Any]:
    """The null distribution CollateralReassignment has to be read against.

    §4 reports collateral reassignment as a percentage of variants that moved, then argues it is
    "at or below the replicate noise floor" — but the only noise floor the paper computes is an
    AMI between replicates. A percentage and a mutual-information score are not commensurable, so
    that comparison established nothing. This measures the floor in the *same* unit: how much the
    identical, unperturbed condition moves between two replicate runs, over the same collateral
    population, under the same anchor-based matching rule.

    Every unordered pair of `replicates` contributes one observation, so k replicates give
    k(k-1)/2. Returns the observations plus their range, which is what a claim of "no larger than
    run-to-run variance" needs in place of a single point.
    """
    observations: list[float] = []
    pairs: list[dict[str, Any]] = []
    for i in range(len(replicates)):
        for j in range(i + 1, len(replicates)):
            (asg_i, anch_i), (asg_j, anch_j) = replicates[i], replicates[j]
            rates = reassignment_rates(asg_i, asg_j, anch_i, anch_j, target_anchors, variants_df)
            collateral = rates["CollateralReassignment"]
            observations.append(collateral["rate"])
            pairs.append({"pair": [i + 1, j + 1], **collateral})
    if not observations:
        return {"k": len(replicates), "pairs": [], "note": "fewer than two replicates — no null"}
    ordered = sorted(observations)
    return {
        "k": len(replicates),
        "n_pairs": len(observations),
        "mean": sum(observations) / len(observations),
        "min": ordered[0],
        "max": ordered[-1],
        "pairs": pairs,
    }


def _axis_problems_for_run(result: ConditionResult, goal_model_path: Path, axis_root: str | None) -> list[str]:
    """Whether a perturbed run's Step 5a stayed on the perturbed model's axis.

    Step 5a raises on this itself now (`goalcat.pipeline.run_step5a_taxonomy`), so in a fresh run
    this should never fire; it is kept as an independent gate here because §4's whole argument
    rests on the perturbed taxonomy anchoring to the same frontier as the baseline, and a run
    reused from disk (`force=False`) may predate that gate.
    """
    from goalcat.grl import read_jucm
    from goalcat.llm.taxonomy import Taxonomy, check_axis_partition

    taxonomy = _read_taxonomy(result)
    if taxonomy is None:
        return ["no taxonomy written"]
    return check_axis_partition(Taxonomy(**taxonomy), read_jucm(goal_model_path), axis_root)


def _anchor_table(taxonomy: dict[str, Any]) -> dict[str, frozenset[str]]:
    return {c["category_id"]: frozenset(c.get("anchor_ids") or []) for c in taxonomy.get("categories", [])}


def run_e2(
    dataset: DatasetSpec,
    protocol: Protocol,
    prereg: PreRegistration,
    logger: logging.Logger,
    *,
    pending: list[str],
    dry_run: bool,
    force: bool,
    stability: report_mod.InductionStability | None,
    axis: str | None = None,
    null_replicates: int = 5,
) -> dict[str, Any]:
    """Perturbations A and B on one axis of one dataset, against its unperturbed guided partition.

    `axis` names which declared axis to perturb; a dataset declaring several (Sepsis) must be run
    once per axis, since each frontier is its own partition. `null_replicates` unperturbed guided
    replicates are also run, to give CollateralReassignment the same-unit noise floor §4's AMI
    comparison could not supply (`replicate_reassignment_null`).
    """
    if dataset.dataset_id == "sepsis":
        adopted = (
            "C6_sepsis_perturbations" in prereg.decisions
            and bool(prereg.get("C6_sepsis_perturbations").value)
        )
        if not adopted:
            raise PreRegistrationError(
                "Experiment 2 is not adopted for Sepsis (Task C6, decided 2026-08-25): the design "
                "forbids perturbations on a dataset whose Step 5a induction is unstable, because "
                "Target/CollateralReassignment cannot be read through induction variance."
            )
    if stability is not None and not stability.is_stable:
        raise PreRegistrationError(
            f"Experiment 2 refused for {dataset.dataset_id}: Task C12 shows Step 5a induction is "
            f"unstable ({stability.distinct_shapes} distinct anchor sets across {stability.k} "
            "identical-input reruns), so a perturbation contrast is confounded by induction "
            "variance (Experiment 2's design constraint)."
        )

    base = prepare_shared_base(dataset, protocol, prereg, logger)
    baseline_condition = ConditionSpec(
        dataset=dataset, arm="guided", replicate=1, experiment="e1", axis=axis
    )
    baseline_result = execute_condition(
        baseline_condition, base, protocol, prereg, logger,
        pending_decisions=pending, dry_run=dry_run, force=False,
    )

    goal_model_path = REPO_ROOT / "data" / "goals" / dataset.goal_model_filename
    from goalcat.grl import declared_alternatives, read_jucm

    model = read_jucm(goal_model_path)
    axis_root = dataset.axis_root(axis)
    or_points = declared_alternatives(model)
    # Perturb only what is on *this* axis. `declared_alternatives()` pools every Or/Xor point in
    # the model, which on Sepsis spans two independent frontiers; perturbing an element of the
    # other frontier would move a partition this run does not measure.
    frontier = model.axis_frontier(axis_root)
    # A declared alternative is a leaf only if it is not itself decomposed further — neither an
    # OR-point (a key in `or_points`) nor the source of any Decomposition link (an AND-decomposed
    # sub-tree, e.g. rtfm's element 5). Perturbation B may only merge true leaves; merging a
    # decomposed alternative would orphan its children and perturb.merge_alternatives() refuses.
    _decomposed = {link.src for link in model.decompositions}

    def _is_leaf(element_id: str) -> bool:
        return element_id not in or_points and element_id not in _decomposed

    leaves = [element_id for element_id in frontier if _is_leaf(element_id)]

    def _leaves_degenerate_parent(element_id: str) -> bool:
        """Would removing `element_id` leave its Or/Xor parent with a single child?

        Same pathology `merge_alternatives` refuses: a decomposition point with one child declares
        no choice, and Step 5a answers it by anchoring above the point instead. RTFM's published
        removal condition took element 19, the second of Xor 7's two children, and so ran against a
        degenerate Xor; `remove_alternative` recorded that in its notes but nothing acted on it.
        Preferring a leaf whose parent keeps at least two children removes the confound.
        """
        parent_id = model.parent_of(element_id)
        parent = model.elements.get(parent_id) if parent_id else None
        return (
            parent is not None
            and parent.decomposition_type in ("Or", "Xor")
            and len(model.children_of(parent_id)) <= 2
        )

    perturbations = []
    removable = [element_id for element_id in leaves if not _leaves_degenerate_parent(element_id)]
    if removable:
        perturbations.append(("A", perturb.remove_alternative(model, removable[-1])))
    elif leaves:
        logger.warning(
            "Every leaf on %s's %s axis has a two-child Or/Xor parent, so any removal leaves a "
            "degenerate decomposition point. Removing %s and reporting the degeneracy.",
            dataset.dataset_id, axis or "sole", leaves[-1],
        )
        perturbations.append(("A", perturb.remove_alternative(model, leaves[-1])))
    on_axis = set(frontier)
    for parent, children in or_points.items():
        # merge_alternatives() refuses a parent with fewer than three children, because collapsing
        # two of two leaves a degenerate Or point that declares no choice at all — the shape that
        # made Sepsis's pertB_merge_15_16 re-anchor its whole taxonomy onto And-decomposed parents.
        candidates = [c for c in children if _is_leaf(c) and c in on_axis]
        if len(children) >= 3 and len(candidates) >= 2:
            merged = candidates[:2]
            perturbations.append(
                ("B", perturb.merge_alternatives(model, tuple(merged), f"Merged {merged[0]}+{merged[1]}"))
            )
            break
    if not any(kind == "B" for kind, _ in perturbations):
        logger.warning(
            "No non-degenerate merge exists on %s's %s axis: no Or/Xor point on the frontier has "
            "three or more leaf alternatives. Reporting Perturbation A only.",
            dataset.dataset_id, axis or "sole",
        )

    findings: list[dict[str, Any]] = []
    if dry_run:
        logger.info("Dry run: %d perturbation(s) prepared, no conditions launched", len(perturbations))
        return {"dataset": dataset.dataset_id, "perturbations": [p.perturbation_id for _, p in perturbations]}

    variants_df = pd.read_csv(base.run_dir / "01_variants" / "variants.csv", dtype={"variant_id": str})
    baseline_assignments = _read_assignments(baseline_result)
    baseline_taxonomy = _read_taxonomy(baseline_result)
    if baseline_assignments is None or baseline_taxonomy is None:
        raise RuntimeError("Experiment 2 needs the unperturbed guided condition's Step 5/6 output first.")

    # The same-unit noise floor (`replicate_reassignment_null`): identical, unperturbed guided
    # conditions, run before the perturbations so a failure here stops the experiment rather than
    # leaving perturbed numbers with nothing to be read against.
    null_runs: list[tuple[pd.DataFrame, dict[str, frozenset[str]]]] = [
        (baseline_assignments, _anchor_table(baseline_taxonomy))
    ]
    for replicate in range(2, null_replicates + 1):
        replicate_run = execute_condition(
            ConditionSpec(
                dataset=dataset, arm="guided", replicate=replicate, experiment="e1", axis=axis
            ),
            base, protocol, prereg, logger,
            pending_decisions=pending, dry_run=False, force=False,
        )
        replicate_assignments = _read_assignments(replicate_run)
        replicate_taxonomy = _read_taxonomy(replicate_run)
        if replicate_assignments is not None and replicate_taxonomy is not None:
            null_runs.append((replicate_assignments, _anchor_table(replicate_taxonomy)))

    perturbed_results: list[ConditionResult] = []
    for kind, result in perturbations:
        condition = ConditionSpec(
            dataset=dataset,
            arm="guided",
            replicate=1,
            tag=result.perturbation_id,
            goal_model_filename=str(result.output_path.relative_to(REPO_ROOT / "data" / "goals")),
            experiment="e2",
            axis=axis,
        )
        run = execute_condition(
            condition, base, protocol, prereg, logger,
            pending_decisions=pending, dry_run=False, force=force,
        )
        perturbed_results.append(run)
        perturbed_assignments = _read_assignments(run)
        perturbed_taxonomy = _read_taxonomy(run)
        if perturbed_assignments is None or perturbed_taxonomy is None:
            continue

        # The perturbed taxonomy must anchor to the perturbed model's own frontier. When it does
        # not — when Step 5a answers the perturbation by re-anchoring to an And-decomposed parent —
        # the perturbed alternative's id is simply absent, TargetReassignment reads 100% because
        # the anchor vanished rather than because variants moved, and the collateral figure
        # measures induction collapse. Both frozen merge runs failed exactly this way and were
        # reported; this refuses to report them.
        axis_problems = _axis_problems_for_run(run, result.output_path, axis_root)
        if axis_problems:
            for problem in axis_problems:
                logger.error("Perturbation %s rejected: %s", result.perturbation_id, problem)
            findings.append(
                {
                    "kind": kind,
                    "perturbation_id": result.perturbation_id,
                    "targets": list(result.targets),
                    "valid": False,
                    "axis_problems": axis_problems,
                    "note": (
                        "Step 5a did not anchor to the perturbed model's axis frontier, so this "
                        "perturbation measures induction collapse rather than sensitivity to the "
                        "edit. Not reportable."
                    ),
                }
            )
            continue

        findings.append(
            {
                "kind": kind,
                "perturbation_id": result.perturbation_id,
                "targets": list(result.targets),
                "valid": True,
                **reassignment_rates(
                    baseline_assignments,
                    perturbed_assignments,
                    _anchor_table(baseline_taxonomy),
                    _anchor_table(perturbed_taxonomy),
                    result.targets,
                    variants_df,
                ),
                "CollateralReassignmentNull": replicate_reassignment_null(
                    null_runs, result.targets, variants_df
                ),
            }
        )

    suffix = f"_axis{axis}" if axis else ""
    if not verify_freeze(
        f"{dataset.dataset_id} Experiment 2{f' (axis {axis})' if axis else ''}",
        {"baseline": baseline_result, **{r.condition.condition_id: r for r in perturbed_results}},
        dataset.dataset_id, f"freeze_e2{suffix}", logger, perturbed=True,
    ):
        raise RuntimeError(
            f"Freeze verification failed for {dataset.dataset_id} Experiment 2. A perturbed run "
            "that differs from its baseline in anything besides the goal model confounds the "
            "perturbation with that difference — which is what happened when every E2 run used a "
            "newer prompt_assignment_batch.txt than the E1 baseline it was measured against."
        )
    out = RESULTS_DIR / dataset.dataset_id / f"experiment2{suffix}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(
            {"dataset": dataset.dataset_id, "axis": axis, "axis_root": axis_root, "findings": findings},
            indent=2,
        ),
        encoding="utf-8",
    )
    logger.info("Wrote Experiment 2 results: %s", out)
    return {"dataset": dataset.dataset_id, "axis": axis, "findings": findings}


# --------------------------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dataset", required=True, choices=["rtfm", "sepsis", "bpic2019"])
    parser.add_argument("--experiment", default="e1", choices=["e1", "e2", "stability"])
    parser.add_argument(
        "--arms",
        default="guided,open",
        help="Comma-separated arms for e1 (guided, open, guided_no_sample, label_list)",
    )
    parser.add_argument(
        "--axis",
        default=None,
        help="Which declared axis to run (configs/<dataset>.yaml `axes`). Omit to run every "
        "declared axis in turn — required for a dataset like Sepsis whose goal model declares "
        "two independent Or frontiers, each of which is its own partition.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Resolve and log everything; launch nothing")
    parser.add_argument("--force", action="store_true", help="Re-run conditions that are already complete")
    parser.add_argument(
        "--allow-pending-decisions",
        action="store_true",
        help="Run despite unresolved pre-registration; manifests are stamped NOT pre-registered",
    )
    args = parser.parse_args(argv)

    logger = _logger()
    protocol = Protocol.load()
    prereg = PreRegistration.load()
    dataset = DatasetSpec.load(args.dataset)

    pending = [d.task for d in prereg.pending_for(args.dataset)]
    if pending and not args.allow_pending_decisions:
        raise SystemExit(
            f"Refusing to run {args.dataset}: decisions {pending} are still pending in "
            "configs/preregistration.yaml. Resolve them, or pass --allow-pending-decisions to "
            "produce an exploratory run whose manifests are stamped NOT pre-registered."
        )
    if pending:
        logger.warning("Running with %s still pending — manifests will record this run as NOT pre-registered.", pending)

    axes: list[str | None] = [args.axis] if args.axis else (dataset.axis_labels or [None])
    if len(axes) > 1:
        logger.info(
            "%s declares %d axes (%s); running each in turn. They are separate partitions, not "
            "alternatives within one.", args.dataset, len(axes), ", ".join(str(a) for a in axes)
        )

    def _stability_path(axis: str | None) -> Path:
        suffix = f"_axis{axis}" if axis else ""
        return RESULTS_DIR / args.dataset / f"stability{suffix}.json"

    def _load_stability(axis: str | None) -> report_mod.InductionStability | None:
        path = _stability_path(axis)
        if not path.exists():
            return None
        raw = json.loads(path.read_text(encoding="utf-8"))
        return report_mod.InductionStability(
            k=raw["k"],
            category_sets=tuple(frozenset(entry) for entry in raw["category_sets"]),
            # Each entry is one run's list of per-category anchor lists; the inner lists become
            # tuples again so the set is hashable and comparable the way `_taxonomy_shape` built it.
            anchor_sets=tuple(frozenset(tuple(a) for a in entry) for entry in raw["anchor_sets"]),
        )

    if args.experiment == "stability":
        for axis in axes:
            stability = run_stability(
                dataset, protocol, prereg, logger,
                pending=pending, dry_run=args.dry_run, force=args.force, axis=axis,
            )
            if stability is None:
                continue
            path = _stability_path(axis)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                json.dumps(
                    {
                        "k": stability.k,
                        "axis": axis,
                        "stable": stability.is_stable,
                        "distinct_anchor_sets": stability.distinct_shapes,
                        "category_sets": [sorted(entry) for entry in stability.category_sets],
                        "anchor_sets": [sorted(list(a) for a in entry) for entry in stability.anchor_sets],
                        "qualification": stability.qualification(dataset.dataset_id),
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
            logger.info("Wrote %s", path)
        return 0

    if args.experiment == "e1":
        for axis in axes:
            stability = _load_stability(axis)
            if stability is None:
                logger.warning(
                    "No Task C12 stability result for %s (axis %s) — run `--experiment stability` "
                    "first. Without it, this dataset's category count, coverage, and residual "
                    "cannot be qualified per Task E7.",
                    args.dataset, axis or "sole",
                )
            run_e1(
                dataset, protocol, prereg, logger,
                pending=pending, dry_run=args.dry_run, force=args.force,
                arms=tuple(a.strip() for a in args.arms.split(",") if a.strip()),
                stability=stability, axis=axis,
            )
        return 0

    for axis in axes:
        run_e2(
            dataset, protocol, prereg, logger,
            pending=pending, dry_run=args.dry_run, force=args.force,
            stability=_load_stability(axis), axis=axis,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

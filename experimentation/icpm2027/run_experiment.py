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
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from goalcat.config import REPO_ROOT

from .analysis import report as report_mod
from .analysis.contingency import contingency_matrix
from .analysis.coverage import compute_coverage
from .analysis.divergence import compute_divergence
from .baselines.structural_clustering import run_structural_clustering
from .conditions import ConditionResult, execute_condition, round_dir_of
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


def _taxonomy_shape(taxonomy: dict[str, Any]) -> tuple[frozenset[str], frozenset[str]]:
    """(category ids, anchor ids) — the two sets Task C12 asks to be reproduced. Anchors are the
    sharper of the two: Sepsis's unstable runs differ in which *level of the goal tree* they anchor
    at, which shows up in the anchor set even where category names happen to look similar."""
    categories = taxonomy.get("categories", [])
    return (
        frozenset(c["category_id"] for c in categories),
        frozenset(anchor for c in categories for anchor in (c.get("anchor_ids") or [])),
    )


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
) -> report_mod.InductionStability | None:
    """Re-runs Step 5a alone k times on identical inputs (Task C12).

    Deliberately not folded into `run_e1()`: this must be answerable *before* committing a dataset's
    LLM budget to a full paired design, because a negative answer changes how every subsequent
    number from that dataset is reported (Task E7) and disqualifies it from Experiment 2 (§4).
    """
    k = protocol.replicates.get("taxonomy_induction", 5)
    base = prepare_shared_base(dataset, protocol, prereg, logger)
    logger.info("Task C12: %d Step-5a-only reruns for %s", k, dataset.dataset_id)

    shapes: list[tuple[frozenset[str], frozenset[str]]] = []
    for replicate in range(1, k + 1):
        condition = ConditionSpec(
            dataset=dataset,
            arm="guided",
            replicate=replicate,
            tag="stability",
            steps=(5,),
            experiment="c12",
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
) -> Experiment1Result:
    base = prepare_shared_base(dataset, protocol, prereg, logger)
    replicates = protocol.replicates.get("unperturbed", 2)

    results: dict[str, ConditionResult] = {}
    for arm in arms:
        for replicate in range(1, replicates + 1):
            condition = ConditionSpec(dataset=dataset, arm=arm, replicate=replicate, experiment="e1")
            results[condition.condition_id] = execute_condition(
                condition, base, protocol, prereg, logger,
                pending_decisions=pending, dry_run=dry_run, force=force,
            )

    dataset_report = report_mod.DatasetReport(dataset_id=dataset.dataset_id, scope_record=base.scope, stability=stability)
    if dry_run:
        return Experiment1Result(dataset.dataset_id, results, dataset_report)

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

    # Task C3 — the structural baseline. No LLM cost, so it always runs when the guided arm exists.
    if guided_id in assignments:
        structural = run_structural_clustering(variants_df)
        dataset_report.structural_contingency = contingency_matrix(
            assignments[guided_id], structural.as_assignments_df(), variants_df, "guided", "structural (HDBSCAN)"
        )

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
    target_anchor: str,
    variants_df: pd.DataFrame,
) -> dict[str, Any]:
    """TargetReassignment and CollateralReassignment (§4), with categories matched by `anchor_ids`.

    Matching by anchor rather than by category id or name is required, not stylistic: §4 re-runs
    Step 5a for every perturbation, so the perturbed taxonomy's category ids are freshly generated
    and may coincide with the baseline's by accident or differ from it while meaning the same thing.
    A variant "changes" if the anchor set behind its category differs, or if it crosses into or out
    of the residual.
    """
    base_by_variant = dict(zip(baseline["variant_id"], baseline["category_id"]))
    pert_by_variant = dict(zip(perturbed["variant_id"], perturbed["category_id"]))
    freq = dict(zip(variants_df["variant_id"], variants_df["frequency"]))

    def anchors_of(category_id: Any, table: dict[str, frozenset[str]]) -> frozenset[str]:
        if not isinstance(category_id, str):
            return frozenset()  # residual
        return table.get(category_id, frozenset())

    target_variants, other_variants = [], []
    for variant_id, category_id in base_by_variant.items():
        if target_anchor in anchors_of(category_id, baseline_anchors):
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
        "target_anchor": target_anchor,
        "TargetReassignment": rate(target_variants),
        "CollateralReassignment": rate(other_variants),
        "note": (
            "CollateralReassignment is interpretable only against the replicate noise floor from "
            "Task C2 — without it, collateral change cannot be distinguished from ordinary "
            "run-to-run variance (Experiment 2's design constraint)."
        ),
    }


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
) -> dict[str, Any]:
    """Perturbations A and B on one dataset, measured against its unperturbed guided partition."""
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
    baseline_condition = ConditionSpec(dataset=dataset, arm="guided", replicate=1, experiment="e1")
    baseline_result = execute_condition(
        baseline_condition, base, protocol, prereg, logger,
        pending_decisions=pending, dry_run=dry_run, force=False,
    )

    goal_model_path = REPO_ROOT / "data" / "goals" / dataset.goal_model_filename
    from goalcat.grl import declared_alternatives, read_jucm

    model = read_jucm(goal_model_path)
    or_points = declared_alternatives(model)
    leaves = [child for children in or_points.values() for child in children if child not in or_points]

    perturbations = []
    if leaves:
        perturbations.append(("A", perturb.remove_alternative(model, leaves[-1])))
    for parent, children in or_points.items():
        if len(children) >= 2:
            merged = [c for c in children if c not in or_points][:2]
            if len(merged) == 2:
                perturbations.append(
                    ("B", perturb.merge_alternatives(model, merged, f"Merged {merged[0]}+{merged[1]}"))
                )
                break

    findings: list[dict[str, Any]] = []
    if dry_run:
        logger.info("Dry run: %d perturbation(s) prepared, no conditions launched", len(perturbations))
        return {"dataset": dataset.dataset_id, "perturbations": [p.perturbation_id for _, p in perturbations]}

    variants_df = pd.read_csv(base.run_dir / "01_variants" / "variants.csv", dtype={"variant_id": str})
    baseline_assignments = _read_assignments(baseline_result)
    baseline_taxonomy = _read_taxonomy(baseline_result)
    if baseline_assignments is None or baseline_taxonomy is None:
        raise RuntimeError("Experiment 2 needs the unperturbed guided condition's Step 5/6 output first.")

    for kind, result in perturbations:
        condition = ConditionSpec(
            dataset=dataset,
            arm="guided",
            replicate=1,
            tag=result.perturbation_id,
            goal_model_filename=str(result.output_path.relative_to(REPO_ROOT / "data" / "goals")),
            experiment="e2",
        )
        run = execute_condition(
            condition, base, protocol, prereg, logger,
            pending_decisions=pending, dry_run=False, force=force,
        )
        perturbed_assignments = _read_assignments(run)
        perturbed_taxonomy = _read_taxonomy(run)
        if perturbed_assignments is None or perturbed_taxonomy is None:
            continue
        findings.append(
            {
                "kind": kind,
                "perturbation_id": result.perturbation_id,
                "targets": list(result.targets),
                **reassignment_rates(
                    baseline_assignments,
                    perturbed_assignments,
                    _anchor_table(baseline_taxonomy),
                    _anchor_table(perturbed_taxonomy),
                    result.targets[0],
                    variants_df,
                ),
            }
        )

    out = RESULTS_DIR / dataset.dataset_id / "experiment2.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"dataset": dataset.dataset_id, "findings": findings}, indent=2), encoding="utf-8")
    logger.info("Wrote Experiment 2 results: %s", out)
    return {"dataset": dataset.dataset_id, "findings": findings}


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

    stability: report_mod.InductionStability | None = None
    stability_path = RESULTS_DIR / args.dataset / "stability.json"
    if stability_path.exists():
        raw = json.loads(stability_path.read_text(encoding="utf-8"))
        stability = report_mod.InductionStability(
            k=raw["k"],
            category_sets=tuple(frozenset(s) for s in raw["category_sets"]),
            anchor_sets=tuple(frozenset(s) for s in raw["anchor_sets"]),
        )

    if args.experiment == "stability":
        stability = run_stability(
            dataset, protocol, prereg, logger, pending=pending, dry_run=args.dry_run, force=args.force
        )
        if stability is not None:
            stability_path.parent.mkdir(parents=True, exist_ok=True)
            stability_path.write_text(
                json.dumps(
                    {
                        "k": stability.k,
                        "stable": stability.is_stable,
                        "distinct_anchor_sets": stability.distinct_shapes,
                        "category_sets": [sorted(s) for s in stability.category_sets],
                        "anchor_sets": [sorted(s) for s in stability.anchor_sets],
                        "qualification": stability.qualification(dataset.dataset_id),
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
            logger.info("Wrote %s", stability_path)
        return 0

    if args.experiment == "e1":
        if stability is None:
            logger.warning(
                "No Task C12 stability result for %s — run `--experiment stability` first. "
                "Without it, this dataset's category count, coverage, and residual cannot be "
                "qualified per Task E7.",
                args.dataset,
            )
        run_e1(
            dataset, protocol, prereg, logger,
            pending=pending, dry_run=args.dry_run, force=args.force,
            arms=tuple(a.strip() for a in args.arms.split(",") if a.strip()),
            stability=stability,
        )
        return 0

    run_e2(
        dataset, protocol, prereg, logger,
        pending=pending, dry_run=args.dry_run, force=args.force, stability=stability,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Regression guards for the four arithmetic and structural rules every reported number rests on.

Scope is deliberate and narrow. These are not unit tests of the pipeline: Steps 5a/6 call a hosted
LLM and cannot be asserted on. What can be asserted, and what nothing guarded before, is the
machinery *between* the LLM and the paper --- the axis the goal model declares, the partition check
that decides whether an induced taxonomy is reportable at all, and the two arithmetic definitions
(coverage/residual, and target/collateral reassignment) that every table is computed through. Each
case below is drawn from a real defect or a real frozen artifact, and every expected value is
stated literally rather than recomputed by the code under test.

Run with `python -m pytest tests/ -q` (pytest is in the `test` optional-dependency group).
"""

from __future__ import annotations

import pandas as pd
import pytest

from goalcat import grl
from goalcat.config import REPO_ROOT
from goalcat.llm.taxonomy import Category, Taxonomy, check_axis_partition

from experimentation.icpm2027.analysis.aggregate_tables import _fmt, _spread
from experimentation.icpm2027.analysis.coverage import compute_coverage
from experimentation.icpm2027.run_experiment import reassignment_rates

GOALS = REPO_ROOT / "data" / "goals"


# --------------------------------------------------------------------------------------------
# axis_frontier — the set Step 5a must cover exactly and Step 6 projects onto


def test_rtfm_frontier_is_the_five_leaf_alternatives():
    """The descent stops at `14` (administrative appeal), which is And-decomposed into four
    mandatory sub-steps: an alternative decomposed into obligations is still one alternative.
    This is the frontier the paper's |T^G| = 5 and the C12 anchor set {12,13,14,19,20} rest on."""
    model = grl.read_jucm(GOALS / "rtfm_goal_model.jucm")
    assert set(model.axis_frontier()) == {"12", "13", "14", "19", "20"}


def test_sepsis_declares_no_single_axis_and_each_root_declares_its_own():
    """Sepsis's root And-joins two independent Or frontiers, so no single label describes a case.
    The model must refuse rather than pool them --- pooling is what made an admission report read
    '2 of 7 declared alternatives realized'."""
    model = grl.read_jucm(GOALS / "sepsis_goal_model.jucm")
    with pytest.raises(grl.AxisError):
        model.axis_frontier()
    assert set(model.axis_frontier("5")) == {"15", "16"}
    assert set(model.axis_frontier("6")) == {"17", "18", "19", "20", "21"}


# --------------------------------------------------------------------------------------------
# check_axis_partition — the blocking check on whether a run is reportable at all


def _taxonomy(*anchor_sets: list[str]) -> Taxonomy:
    return Taxonomy(
        categories=[
            Category(
                category_id=f"c{index}",
                name=f"Category {index}",
                description="irrelevant to the structural check",
                anchor_ids=anchors,
                rationale="irrelevant to the structural check",
                evidence_variant_ids=[],
            )
            for index, anchors in enumerate(anchor_sets)
        ]
    )


def test_complete_disjoint_cover_of_the_frontier_passes():
    model = grl.read_jucm(GOALS / "rtfm_goal_model.jucm")
    taxonomy = _taxonomy(["12"], ["13"], ["14"], ["19"], ["20"])
    assert check_axis_partition(taxonomy, model) == []


@pytest.mark.parametrize(
    "anchor_sets, defect",
    [
        ((["12"], ["13"], ["14"], ["19"]), "an uncovered frontier alternative (20 dropped)"),
        ((["12"], ["12"], ["13"], ["14"], ["19"], ["20"]), "two categories on one alternative"),
        ((["12"], ["13"], ["14"], ["19"], ["20"], ["5"]), "an off-axis anchor (the And parent)"),
        ((["12"], ["13"], ["14"], ["19"], ["20"], []), "an anchorless category"),
        ((["12"], ["13"], ["14", "15"], ["19"], ["20"]), "a category absorbing its And children"),
    ],
)
def test_every_structural_defect_is_reported(anchor_sets, defect):
    """Each row is a defect actually observed in a frozen run or its precursor --- notably the
    last, `14` absorbing its And-decomposed child `15`, which was the operative Step 5a prompt
    defect behind the retracted 'three Sepsis taxonomies' finding."""
    model = grl.read_jucm(GOALS / "rtfm_goal_model.jucm")
    assert check_axis_partition(_taxonomy(*anchor_sets), model), f"not reported: {defect}"


# --------------------------------------------------------------------------------------------
# Coverage arithmetic — Table 1's two residual columns


def _frames():
    assignments = pd.DataFrame(
        {
            "variant_id": ["V1", "V2", "V3", "V4"],
            "category_id": ["a", "b", None, "a"],
        }
    )
    variants = pd.DataFrame({"variant_id": ["V1", "V2", "V3"], "frequency": [10, 5, 85]})
    return assignments, variants


def test_coverage_is_variant_and_case_weighted_independently():
    """V3 is one variant of three in scope (33.3% of variants) but 85 of 100 cases: the two
    residual columns must diverge. This is RTFM's V0003 in miniature, the variant that makes
    RTFM's variant-weighted residual 1.9% and its case-weighted residual 13.8%."""
    assignments, variants = _frames()
    report = compute_coverage(assignments, variants, "test")
    assert report.total_variants == 3
    assert report.total_cases == 100
    assert report.residual_variant_ids == ("V3",)
    assert report.residual_variant_count / report.total_variants == pytest.approx(1 / 3)
    assert report.residual_case_count / report.total_cases == pytest.approx(0.85)


def test_out_of_scope_variants_are_not_counted_as_residual():
    """V4 is assigned but absent from `variants.csv` (Task C7's variant-scope policy). It is
    outside the condition's population, not uncategorized behavior, and must not enter either
    denominator --- counting it as residual would inflate every coverage figure on BPIC 2019."""
    assignments, variants = _frames()
    report = compute_coverage(assignments, variants, "test")
    assert "V4" not in report.residual_variant_ids
    assert report.total_variants == 3


# --------------------------------------------------------------------------------------------
# Reassignment arithmetic — Table 5's two rates


def _reassignment_case():
    """Baseline: V1,V2 realize the target alternative `20`; V3,V4 are bystanders. The perturbation
    removes `20`, so its variants must move; V3 also moves, one bystander in two."""
    baseline = pd.DataFrame(
        {"variant_id": ["V1", "V2", "V3", "V4"], "category_id": ["coercive", "coercive", "timely", "delinquent"]}
    )
    perturbed = pd.DataFrame(
        {"variant_id": ["V1", "V2", "V3", "V4"], "category_id": ["delinquent", None, "delinquent", "delinquent"]}
    )
    variants = pd.DataFrame({"variant_id": ["V1", "V2", "V3", "V4"], "frequency": [1, 1, 1, 1]})
    baseline_anchors = {"coercive": frozenset({"20"}), "timely": frozenset({"12"}), "delinquent": frozenset({"13"})}
    perturbed_anchors = {"delinquent": frozenset({"13"})}
    return baseline, perturbed, baseline_anchors, perturbed_anchors, variants


def test_target_and_collateral_populations_are_disjoint_and_correctly_rated():
    baseline, perturbed, ba, pa, variants = _reassignment_case()
    rates = reassignment_rates(baseline, perturbed, ba, pa, ["20"], variants)
    assert rates["TargetReassignment"]["n"] == 2
    assert rates["TargetReassignment"]["rate"] == 1.0  # including V2's move into the residual
    assert rates["CollateralReassignment"]["n"] == 2
    assert rates["CollateralReassignment"]["rate"] == pytest.approx(0.5)  # V3 moved, V4 did not


def test_a_merge_scores_against_both_targets():
    """Feeding only the first target of a merge puts the second target's variants into the
    collateral population, where they move by construction. On RTFM's merge that substitution
    turned 12.9% collateral into 32.6%; the guard is that both targets leave the denominator."""
    baseline, perturbed, ba, pa, variants = _reassignment_case()
    both = reassignment_rates(baseline, perturbed, ba, pa, ["20", "13"], variants)
    assert both["TargetReassignment"]["n"] == 3  # V1, V2 (anchor 20) and V4 (anchor 13)
    assert both["CollateralReassignment"]["n"] == 1  # V3 alone
    first_only = reassignment_rates(baseline, perturbed, ba, pa, ["20"], variants)
    assert first_only["CollateralReassignment"]["n"] > both["CollateralReassignment"]["n"]


def test_reassignment_needs_at_least_one_target():
    baseline, perturbed, ba, pa, variants = _reassignment_case()
    with pytest.raises(ValueError):
        reassignment_rates(baseline, perturbed, ba, pa, [], variants)


# --------------------------------------------------------------------------------------------
# Table rendering — the caption's own collapse rule


def test_range_collapses_only_when_it_vanishes_at_the_printed_precision():
    """Both captions promise 'a bracket is omitted where minimum and maximum agree to two
    decimals'. Sepsis admission's cross-arm cell spans 0.2666--0.2746 and must print bare; the
    manuscript printed `0.27 [0.27--0.28]` by rounding the maximum up a step (review item R8)."""
    assert _fmt(_spread([0.2666, 0.2693, 0.2746]), 2) == "0.27"
    discharge_pairs = [0.7148, 0.7434, 0.7503, 0.7513, 0.7862, 0.7884, 0.7939, 0.8155, 0.8277, 0.9207]
    assert _fmt(_spread(discharge_pairs), 2) == "0.79 [0.71--0.92]"  # printed `[0.72--0.92]`
    assert _spread([0.1, 0.3])["mean"] == pytest.approx(0.2)

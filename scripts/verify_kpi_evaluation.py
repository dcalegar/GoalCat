"""Conformance check: does `goalcat.grl.evaluation` agree with jUCMNav?

`evaluation.py` re-states two algorithms that jUCMNav owns — the KPI conversion in
`EvaluationStrategyManager.calculateIndicatorEvalLevel()` and the quantitative propagation in
`QuantitativeGRLStrategyAlgorithm.getEvaluation()`. The Java is not vendored (see that module's
docstring for the licence reasoning), so nothing in the repository would catch a drift between the
two implementations. This script is that catch: every case below is derived from a specific branch
of the reference source, named in its own comment, so a reader can check the expectation against
jUCMNav rather than against this project's opinion of it.

Run: `python scripts/verify_kpi_evaluation.py` (exit status 0 = all cases agree).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from goalcat.grl.evaluation import (  # noqa: E402
    MIN_RANGE_POSITIVE,
    indicator_evaluation,
    propagate,
)
from goalcat.grl.model import (  # noqa: E402
    ContributionLink,
    DecompositionLink,
    GRLModel,
    IntentionalElement,
    KPIEvalPoint,
)

# (measured, target, threshold, worst, expected, which branch of calculateIndicatorEvalLevel)
CONVERSION_CASES = [
    # target < worst: the "lower is better" arm, tested top to bottom.
    (10, 30, 90, 360, 100, "newValue <= targetValue -> 100"),
    (30, 30, 90, 360, 100, "boundary: measurement exactly at target still saturates"),
    (400, 30, 90, 360, -100, "newValue >= worstValue -> -100"),
    (60, 30, 90, 360, 50, "|60-90| / |30-90| * 100 = 50"),
    (46, 30, 90, 360, 73, "|46-90| / |30-90| * 100 = 73.3, truncated to int by Evaluation's EInt"),
    (90, 30, 90, 360, 0, "measurement exactly at threshold is the scale's zero"),
    (134, 30, 90, 360, -16, "|134-90| / |90-360| * -100 = -16.3"),
    # target == threshold: the degenerate value set a statutory boundary produces. The saturating
    # test precedes the interpolating one, so the zero-width segment is never divided by.
    (46, 90, 90, 360, 100, "one-sided: anything at or better than the boundary saturates"),
    (134, 90, 90, 360, -16, "one-sided: the penalty arm is unaffected"),
    # target > worst: the "higher is better" arm.
    (95, 90, 60, 0, 100, "newValue >= targetValue -> 100"),
    (0, 90, 60, 0, -100, "newValue <= worstValue -> -100"),
    (75, 90, 60, 0, 50, "|75-60| / |90-60| * 100 = 50"),
    (30, 90, 60, 0, -50, "|30-60| / |60-0| * -100 = -50"),
    # A threshold-less binary indicator (sepsis' third KPI): EMF defaults the unset double to 0.0,
    # which lands on the target == threshold == 0 case rather than raising.
    (0.5, 0, 0, 1, -50, "unset threshold defaults to 0: |0.5-0| / |0-1| * -100 = -50"),
]

# Same conversions, read on URN's positive-only [0, 100] range (evalLevel / 2 + 50).
POSITIVE_RANGE_CASES = [
    (10, 30, 90, 360, 100, "+100 remaps to the top of [0, 100]"),
    (90, 30, 90, 360, 50, "the zero point remaps to the midpoint"),
    (400, 30, 90, 360, 0, "-100 remaps to the bottom"),
]


def _model() -> GRLModel:
    """A three-level model exercising every propagation rule at once: an And over two children, an
    Or under it, and a softgoal fed only by contributions."""
    model = GRLModel(source_path="<verify>", name="verify", author=None, urn_version=None,
                     spec_version=None, next_global_id=100)
    for element_id, name, kind, decomposition in [
        ("1", "root", "Goal", "And"),
        ("2", "left", "Goal", "Or"),
        ("3", "right", "Task", None),
        ("4", "left-a", "Task", None),
        ("5", "left-b", "Task", None),
        ("6", "softgoal", "Softgoal", None),
    ]:
        model.elements[element_id] = IntentionalElement(id=element_id, name=name, type=kind,
                                                       decomposition_type=decomposition)
    model.decompositions = [
        DecompositionLink(id="10", src="1", dest="2"),
        DecompositionLink(id="11", src="1", dest="3"),
        DecompositionLink(id="12", src="2", dest="4"),
        DecompositionLink(id="13", src="2", dest="5"),
    ]
    model.contributions = [
        ContributionLink(id="20", src="3", dest="6", contribution="Help", quantitative=50),
        ContributionLink(id="21", src="4", dest="6", contribution="SomeNegative", quantitative=-25),
    ]
    return model


PROPAGATION_CASES = [
    ({"4": 100, "5": 20, "3": 60},
     {"2": 100, "1": 60, "6": 5},
     "Or takes max(100, 20); And takes min(100, 60); softgoal sums 50*60/100 + -25*100/100 = 5"),
    ({"4": -100, "5": -100, "3": 100},
     {"2": -100, "1": -100, "6": 75},
     "Or over two denied children stays denied; contributions sum 50 + 25 = 75"),
    ({"4": 0, "5": 0, "3": 0},
     {"2": 0, "1": 0, "6": 0},
     "zero contributions are dropped before summing, exactly as evaluateContribution drops them"),
]


def main() -> int:
    failures = []

    for measured, target, threshold, worst, expected, why in CONVERSION_CASES:
        point = KPIEvalPoint(target=target, threshold=threshold, worst=worst, unit="days",
                             qualitative_evaluation_value=None)
        actual = indicator_evaluation(measured, point)
        if actual != expected:
            failures.append(f"conversion({measured}, t={target}, th={threshold}, w={worst}): "
                            f"expected {expected}, got {actual} — {why}")

    for measured, target, threshold, worst, expected, why in POSITIVE_RANGE_CASES:
        point = KPIEvalPoint(target=target, threshold=threshold, worst=worst, unit="days",
                             qualitative_evaluation_value=None)
        actual = indicator_evaluation(measured, point, min_range=MIN_RANGE_POSITIVE)
        if actual != expected:
            failures.append(f"conversion[0..100]({measured}): expected {expected}, got {actual} — {why}")

    model = _model()
    for seeds, expected, why in PROPAGATION_CASES:
        actual = propagate(model, seeds).evaluations
        for element_id, want in expected.items():
            if actual[element_id] != want:
                failures.append(f"propagate({seeds})[{element_id}]: expected {want}, "
                                f"got {actual[element_id]} — {why}")

    total = len(CONVERSION_CASES) + len(POSITIVE_RANGE_CASES) + sum(len(e) for _s, e, _w in PROPAGATION_CASES)
    if failures:
        print(f"FAIL — {len(failures)} of {total} checks disagree with the jUCMNav reference:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"OK — all {total} checks match the jUCMNav reference behaviour.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

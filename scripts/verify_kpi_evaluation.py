"""Conformance check: does `goalcat.grl.evaluation` agree with jUCMNav?

`evaluation.py` re-states two algorithms that jUCMNav owns — the KPI conversion in
`EvaluationStrategyManager.calculateIndicatorEvalLevel()` and the quantitative propagation in
`QuantitativeGRLStrategyAlgorithm.getEvaluation()`. The Java is not vendored (see that module's
docstring for the licence reasoning), so nothing in the repository would catch a drift between the
two implementations. This script is that catch: every case below is derived from a specific branch
of the reference source, named in its own comment, so a reader can check the expectation against
jUCMNav rather than against this project's opinion of it.

The KPI conversion has a second, independent statement in the literature: Eqs. 8 and 9 of Fan,
Anda and Amyot's arithmetic semantics for GRL [fan2018arithmetic], given on URN's positive-only
[0, 100] range. Those equations are transcribed literally in `_paper_conversion()` and compared
against this project's conversion over a grid of measurements, so that agreement is established
differentially rather than at points someone chose. Two references disagreeing would localise the
error; both agreeing is worth more than either table alone.

That comparison covers three tiers, kept apart because they support different claims and it would
overstate the result to report them as one number:

1. **Inside the paper's domain** (`IN_DOMAIN_VALUE_SETS`) -- target, threshold and worst pairwise
   distinct, as Sect. 3.2 requires. Agreement here is conformance in the strict sense.
2. **Outside it, but still arm-selectable** (`RELAXED_VALUE_SETS`) -- `target == threshold` or
   `threshold == worst`, which the paper's precondition excludes ("the target, threshold, and worst
   values cannot be equal") and which both formulations nonetheless evaluate identically, because
   the saturating clamps make the zero-width segment unreachable. Agreement here says the stated
   precondition is stricter than the equations need, which is what lets this project treat a
   statutory `target == threshold` indicator as well defined.
3. **Outside it and not arm-selectable** (`UNDEFINED_TIE_VALUE_SET`) -- `target == worst`. Eq. 8 is
   stated for target > worst and Eq. 9 for target < worst, so at equality the paper selects no arm
   and defines nothing. `_paper_conversion()` therefore refuses this input rather than silently
   breaking the tie: an `else` that swept equality into Eq. 9 would manufacture a disagreement the
   paper never expresses. What is pinned here is only this project's own behaviour -- jUCMNav's
   higher-is-better arm -- so that a change to it fails loudly. No value set in `data/goals/` has
   `target == worst`, and an indicator whose best and worst values coincide measures nothing.

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


class OutsidePaperDomain(Exception):
    """Raised when a value set selects neither Eq. 8 nor Eq. 9, so the paper defines no result."""


def _paper_conversion(measured: float, target: float, threshold: float, worst: float) -> float:
    """Eqs. 8 (target > worst) and 9 (target < worst) of [fan2018arithmetic], transcribed literally,
    on the [0, 100] range they are stated over. Kept deliberately close to the printed equations --
    including the `Abs()` calls that the branch guards already make redundant -- so that a reader
    can check this against the paper line by line rather than against a simplification of it.

    Equality of target and worst raises rather than falling through to either arm. The paper gives
    Eq. 8 for target > worst and Eq. 9 for target < worst and says nothing about the tie; resolving
    it here with an `else` would attribute a choice to the paper that it does not make, and any
    disagreement that followed would be this helper's, not the literature's."""
    if target == worst:
        raise OutsidePaperDomain(
            f"target == worst ({target}): Eq. 8 requires target > worst, Eq. 9 target < worst")
    if target > worst:  # Eq. 8
        if measured >= target:
            return 100.0
        if measured <= worst:
            return 0.0
        if threshold <= measured < target:
            return abs((measured - threshold) / (target - threshold)) * 50 + 50
        return -abs((measured - threshold) / (worst - threshold)) * 50 + 50
    # Eq. 9
    if measured <= target:
        return 100.0
    if measured >= worst:
        return 0.0
    if target < measured <= threshold:
        return abs((measured - threshold) / (threshold - target)) * 50 + 50
    return -abs((measured - threshold) / (threshold - worst)) * 50 + 50


# Tier 1: target, threshold and worst pairwise distinct -- the paper's stated domain.
IN_DOMAIN_VALUE_SETS = [
    (30, 90, 360),    # lower is better -- RTFM's "time to fine dispatch"
    (150, 180, 365),  # lower is better -- RTFM's "average time to case closure"
    (90, 60, 0),      # higher is better
    (100, 50, 10),    # higher is better
]

# Tier 2: excluded by the paper's precondition, yet both formulations agree because the clamps make
# the zero-width segment unreachable. These are the value sets this project actually relies on --
# a statutory boundary is a target that equals its threshold.
RELAXED_VALUE_SETS = [
    (60, 60, 120),    # target == threshold -- RTFM's statutory appeal window (one-sided)
    (30, 30, 60),     # target == threshold -- the Judge appeal window
    (30, 90, 90),     # threshold == worst
    (0, 0, 1),        # unset threshold defaulting to 0, as EMF leaves it
]

# Tier 3: target == worst, where the paper selects no arm. Only this project's behaviour is pinned
# -- jUCMNav's higher-is-better reading -- together with the fact that the paper declines the input.
# (measured, expected here, why)
UNDEFINED_TIE_VALUE_SET = (50, 50, 50)
UNDEFINED_TIE_CASES = [
    (49.0, 0, "below the common value: the higher-is-better arm clamps to worst"),
    (50.0, 100, "at the common value the saturating test for target fires first"),
    (51.0, 100, "above it: still the target clamp, since target and worst coincide"),
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


def _sweep(value_sets: list[tuple[int, int, int]], tier: str) -> tuple[int, list[str]]:
    """Sweeps each value set from below its minimum to above its maximum, comparing this project's
    conversion against the paper's closed form at every step. `indicator_evaluation` truncates to
    int after the remap onto [0, 100], so the paper's real-valued result is truncated the same way
    before comparison -- the question is whether the two functions agree, not whether one rounds."""
    checks = 0
    failures: list[str] = []
    for target, threshold, worst in value_sets:
        point = KPIEvalPoint(target=float(target), threshold=float(threshold), worst=float(worst),
                             unit="days", qualitative_evaluation_value=None)
        low, high = min(target, threshold, worst), max(target, threshold, worst)
        span = (high - low) or 1.0
        for step in range(-30, 431):  # 400 steps across the value set, overshooting both clamps
            measured = low + span * step / 400.0
            ours = indicator_evaluation(measured, point, min_range=MIN_RANGE_POSITIVE)
            theirs = int(_paper_conversion(measured, float(target), float(threshold), float(worst)))
            checks += 1
            if ours != theirs:
                failures.append(f"{tier}({measured:.4f}, t={target}, th={threshold}, "
                                f"w={worst}): this project gives {ours}, Eqs. 8/9 give {theirs}")
    return checks, failures


def _undefined_tie_checks() -> tuple[int, list[str]]:
    """Pins the two facts about `target == worst` worth pinning: the paper declines to define it,
    and this project answers with jUCMNav's higher-is-better arm. Neither is a disagreement between
    the two references -- there is nothing on the paper's side to disagree with."""
    target, threshold, worst = UNDEFINED_TIE_VALUE_SET
    point = KPIEvalPoint(target=float(target), threshold=float(threshold), worst=float(worst),
                         unit="days", qualitative_evaluation_value=None)
    failures: list[str] = []
    checks = 0

    try:
        _paper_conversion(50.0, float(target), float(threshold), float(worst))
        failures.append("undefined tie: _paper_conversion() returned a value for target == worst, "
                        "but Eqs. 8 and 9 are stated only for target > worst and target < worst")
    except OutsidePaperDomain:
        pass
    checks += 1

    for measured, expected_here, why in UNDEFINED_TIE_CASES:
        ours = indicator_evaluation(measured, point, min_range=MIN_RANGE_POSITIVE)
        checks += 1
        if ours != expected_here:
            failures.append(f"undefined tie({measured}): this project gives {ours}, "
                            f"expected {expected_here} — {why}")
    return checks, failures


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

    in_domain_checks, in_domain_failures = _sweep(IN_DOMAIN_VALUE_SETS, "in-domain")
    failures.extend(in_domain_failures)
    relaxed_checks, relaxed_failures = _sweep(RELAXED_VALUE_SETS, "relaxed")
    failures.extend(relaxed_failures)
    tie_checks, tie_failures = _undefined_tie_checks()
    failures.extend(tie_failures)

    total = (len(CONVERSION_CASES) + len(POSITIVE_RANGE_CASES)
             + sum(len(e) for _s, e, _w in PROPAGATION_CASES)
             + in_domain_checks + relaxed_checks + tie_checks)
    if failures:
        print(f"FAIL — {len(failures)} of {total} checks disagree with a reference:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"OK — all {total} checks match their reference.")
    print(f"  jUCMNav behaviour: {len(CONVERSION_CASES) + len(POSITIVE_RANGE_CASES)} conversion "
          f"cases, {sum(len(e) for _s, e, _w in PROPAGATION_CASES)} propagation cases.")
    print(f"  [fan2018arithmetic] Eqs. 8/9, inside the paper's stated domain: {in_domain_checks} "
          f"measurements over {len(IN_DOMAIN_VALUE_SETS)} pairwise-distinct value sets.")
    print(f"  [fan2018arithmetic] Eqs. 8/9, outside it but arm-selectable: {relaxed_checks} "
          f"measurements over {len(RELAXED_VALUE_SETS)} degenerate value sets.")
    print(f"  target == worst: {tie_checks} checks — the paper defines nothing there, and this "
          f"project's jUCMNav reading is pinned.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

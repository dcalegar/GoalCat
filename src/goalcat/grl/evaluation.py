"""GRL satisfaction arithmetic: KPI conversion and quantitative propagation.

This module answers one question — *given a measured real-world value, what satisfaction level does
the goal model assign to every element above it?* — and answers it the way jUCMNav does, so a
`.jucm` file this project writes and a human opening that same file in jUCMNav read the same
numbers off it.

**Provenance and why this is a re-implementation, not a port.** The reference behaviour is
jUCMNav's own, in two classes of the Eclipse plug-in (`JUCMNAV/LEGACY_seg.jUCMNav`, EPL-1.0):

| Concern | jUCMNav reference |
|---|---|
| KPI conversion | `seg.jUCMNav.strategies.EvaluationStrategyManager.calculateIndicatorEvalLevel(Evaluation)` |
| Propagation | `seg.jUCMNav.strategies.QuantitativeGRLStrategyAlgorithm.getEvaluation(IntentionalElement)` and its `evaluateDecomposition` / `evaluateContribution` / `ensureEvaluationWithinRange` helpers |

Those classes were read to fix the semantics — the branch order, the clamping, the treatment of
degenerate value sets — and the behaviour here is intended to match them exactly. The Java is *not*
vendored and not transliterated: jUCMNav is EPL-1.0 and GoalCat is AGPL-3.0-or-later, two licences
whose combination is contested, so `third_party/jucmnav/` deliberately holds schema definitions
only ("No Java source", per its README) and this module states the algorithm — which is the URN
standard's [itu2018urn], not jUCMNav's invention — in this project's own terms. Behavioural
equivalence is the contract; `scripts/verify_kpi_evaluation.py` pins it to a table of cases derived
from the branch structure above.

**Two ranges.** URN defines the satisfaction scale as either [-100, 100] (the default, and what
every `data/goals/*.jucm` file uses) or [0, 100]. `min_range` selects between them exactly as
jUCMNav's `StrategyEvaluationRangeHelper` does, including the `evalLevel / 2 + 50` remap the
conversion applies in the positive-only range.

**Degenerate KPI value sets are not an error.** `worstValue`/`thresholdValue`/`targetValue` need
not be strictly ordered. A statutory indicator legitimately has `target == threshold` — the law
defines one boundary, not a gradient toward an ideal — and jUCMNav handles it by construction: the
saturating `<= target` / `>= worst` tests precede the two interpolating branches, so the zero-width
segment is never divided by. The result is a one-sided compliance scale: full satisfaction at or
beyond the boundary, linear penalty past it. `indicator_evaluation()` reproduces that, and
`is_one_sided()` lets a caller report it rather than mistake saturation for measurement.
"""

from __future__ import annotations

from dataclasses import dataclass

from .model import CONTRIBUTION_WEIGHT, GRLModel, KPIEvalPoint

#: URN's two satisfaction ranges, as `min_range` values (the maximum is always 100).
MIN_RANGE_FULL = -100
MIN_RANGE_POSITIVE = 0


def is_one_sided(eval_point: KPIEvalPoint) -> bool:
    """True when this value set collapses one half of the scale — `target == threshold`, so the
    segment between them has zero width. Not a defect (see this module's docstring), but a caller
    reporting satisfaction should say so, because every measurement on the collapsed side
    saturates at the same value and carries no gradient."""
    return eval_point.target is not None and eval_point.target == eval_point.threshold


def indicator_evaluation(
    measured_value: float, eval_point: KPIEvalPoint, *, min_range: int = MIN_RANGE_FULL
) -> int:
    """Converts one measured real-world value to a GRL satisfaction level, per the `KPIEvalValueSet`
    attached to the indicator.

    The map is piecewise-linear with `thresholdValue` pinned at 0, `targetValue` at +100 and
    `worstValue` at the range minimum, clamped outside [worst, target]. Direction is inferred from
    the value set itself rather than declared: `target < worst` means lower measurements are better
    (a duration), `target > worst` means higher are (a yield). Degenerate sets are handled by the
    clamps, which are tested first — see this module's docstring.

    Returns an `int`, matching jUCMNav's own truncation to `Evaluation.evaluation` (an EInt); a
    caller wanting the undegraded number should keep the raw measurement beside it, which
    `goalcat.indicators` does.
    """
    target = eval_point.target or 0.0
    threshold = eval_point.threshold or 0.0
    worst = eval_point.worst or 0.0

    if target < worst:  # lower is better
        if measured_value <= target:
            level = 100.0
        elif measured_value >= worst:
            level = -100.0
        elif measured_value < threshold:
            level = abs(measured_value - threshold) / abs(target - threshold) * 100.0
        else:
            level = abs(measured_value - threshold) / abs(threshold - worst) * -100.0
    else:  # higher is better (also the path taken when target == worst)
        if measured_value >= target:
            level = 100.0
        elif measured_value <= worst:
            level = -100.0
        elif measured_value >= threshold:
            level = abs(measured_value - threshold) / abs(target - threshold) * 100.0
        else:
            level = abs(measured_value - threshold) / abs(threshold - worst) * -100.0

    if min_range == MIN_RANGE_POSITIVE:
        level = level / 2 + 50
    return int(level)


@dataclass(frozen=True)
class PropagationResult:
    """One propagation run's outcome: a satisfaction level per intentional element, plus the seeds
    it started from (kept so a report can distinguish a *measured* element from a *derived* one
    without re-deriving which ids were seeded)."""

    evaluations: dict[str, int]
    seeds: dict[str, int]

    def derived(self) -> dict[str, int]:
        return {k: v for k, v in self.evaluations.items() if k not in self.seeds}


def propagate(
    model: GRLModel,
    seeds: dict[str, int],
    *,
    min_range: int = MIN_RANGE_FULL,
    tolerance: int = 0,
    default: int = 0,
) -> PropagationResult:
    """Propagates `seeds` (element id -> satisfaction level, normally indicator conversions) up
    through `model`'s decomposition and contribution links, returning a level for every element.

    The rules, per element, in jUCMNav's own order:

    1. **Decomposition.** `min` over children for an `And`, `max` for an `Or`/`Xor`. An element
       with no children contributes no decomposition value at all (not a zero — the distinction
       matters, since step 2 *adds* to whatever step 1 produced).
    2. **Contributions.** Each incoming contribution yields `quantitative * source / 100`, rounded;
       zero-valued ones are dropped, exactly as `evaluateContribution` drops them. Their sum is
       added to the decomposition value and the total is clamped into the range.
    3. **Tolerance.** jUCMNav exposes a preference that stops a total from *reaching* a boundary
       unless some single input already sat on it — an element is only fully satisfied if something
       fully satisfied it. `tolerance=0` (the default here) makes those two branches no-ops; pass
       the value configured in jUCMNav to reproduce a specific installation.

    Cycles are broken by evaluating a revisited element as `default` rather than recursing, so a
    malformed model yields a number instead of a `RecursionError`. `Dependency` links are absent
    from every `data/goals/*.jucm` file and are not evaluated (`model.py` parses only
    `Decomposition` and `Contribution`).
    """
    children_by_parent: dict[str, list[str]] = {}
    for link in model.decompositions:
        children_by_parent.setdefault(link.src, []).append(link.dest)

    contributions_to: dict[str, list[tuple[str, int]]] = {}
    for link in model.contributions:
        weight = link.quantitative if link.quantitative is not None else CONTRIBUTION_WEIGHT[link.contribution]
        contributions_to.setdefault(link.dest, []).append((link.src, weight))

    evaluations: dict[str, int] = {}

    def evaluate(element_id: str, in_progress: frozenset[str]) -> int:
        if element_id in evaluations:
            return evaluations[element_id]
        if element_id in in_progress:
            return default
        if element_id in seeds:
            evaluations[element_id] = _clamp(seeds[element_id], min_range)
            return evaluations[element_id]

        visiting = in_progress | {element_id}
        children = children_by_parent.get(element_id, [])
        decomposition_value: int | None = None
        if children:
            child_values = [evaluate(child_id, visiting) for child_id in children]
            operator = model.elements[element_id].decomposition_type or "And"
            decomposition_value = min(child_values) if operator == "And" else max(child_values)

        contribution_values = []
        for source_id, weight in contributions_to.get(element_id, []):
            contribution = round(weight * evaluate(source_id, visiting) / 100)
            if contribution != 0:
                contribution_values.append(int(contribution))

        result = decomposition_value if decomposition_value is not None else default
        if contribution_values:
            has_satisfy = result == 100 or 100 in contribution_values
            has_deny = result == min_range or min_range in contribution_values
            total = sum(contribution_values)
            result = _clamp(result + total, min_range)
            if result >= 100 - tolerance and not has_satisfy:
                floor = decomposition_value if total > 0 and decomposition_value is not None else result
                result = max(floor, 100 - tolerance)
            elif result <= min_range + tolerance and not has_deny:
                ceiling = decomposition_value if total < 0 and decomposition_value is not None else result
                result = min(ceiling, min_range + tolerance)

        evaluations[element_id] = _clamp(result, min_range)
        return evaluations[element_id]

    for element_id in model.elements:
        evaluate(element_id, frozenset())
    return PropagationResult(evaluations=evaluations, seeds=dict(seeds))


def _clamp(value: int, min_range: int) -> int:
    return max(min_range, min(100, int(value)))

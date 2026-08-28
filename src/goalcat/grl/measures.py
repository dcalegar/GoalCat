r"""Measuring a goal model's KPI indicators against a real event log.

An `Indicator` in `grl.kpimodel` carries the *conversion* from a measured value to a satisfaction
level (`KPIEvalValueSet`), but nothing that says how to obtain the measurement — that binding lives
in `KPIInformationElement`/`KPIModelLink`, which none of this project's goal models encode and whose
§6 "Formula" columns are documentary prose. This module supplies the missing binding, declaratively
and inside the `.jucm` file itself.

**Why URN `Metadata` and not a side-car file.** `urncore.ecore` gives every `URNmodelElement` a
containment list of `Metadata` (a `name`/`value` pair) precisely so tools can attach their own
annotations; jUCMNav itself uses it to stamp `_numEval`/`_qualEval` onto elements after a strategy
runs. Putting the measure specification there keeps the whole goal model in one artifact, survives
a round trip through jUCMNav untouched, and needs no schema extension. Keys are namespaced
`goalcat:*` so they cannot collide with jUCMNav's own.

| Key | Meaning | Example |
|---|---|---|
| `goalcat:measure` | measurement kind: `duration_days`, `duration_hours`, `trace_contains`, or `case_fraction` | `duration_hours` |
| `goalcat:from` | `\|`-separated activity labels; the clock starts at the first occurrence of any (duration kinds only) | `Record Invoice Receipt` |
| `goalcat:to` | `\|`-separated activity labels that stop the clock, or -- for `trace_contains` -- whose presence anywhere in the case scores 1 | `Payment\|Send for Credit Collection` |
| `goalcat:to_occurrence` | which stopping event counts, `first` or `last` (duration kinds only) | `first` |
| `goalcat:applies_when` | `\|`-separated labels; a case lacking all of them is *out of scope* | `Appeal to Judge` |
| `goalcat:aggregate` | how per-case values combine, `mean` or `median` | `mean` |
| `goalcat:among` | `case_fraction` denominator: `\|`-separated labels, a case lacking all of them is out of scope (default: every case) | `Clear Invoice` |
| `goalcat:numerator` | `case_fraction` per-case predicate -- `has:`, `lacks:`, `attr:`, or `before:` (see below) | `lacks:Record Goods Receipt` |
| `goalcat:scale` | `case_fraction` output: `percent` (rate ×100, the default) or `fraction` | `percent` |
| `goalcat:provenance` | where the value set's bounds come from | `statutory` |
| `goalcat:source` | the citation backing them | `Art. 201 D.Lgs. 285/1992` |

**`goalcat:numerator` predicate forms** (the case is in the numerator when the predicate holds):

- `has:A\|B\|C` -- the case contains at least one of these activity labels.
- `lacks:A\|B\|C` -- the case contains none of them.
- `attr:Key=Value` -- the case attribute `case:Key` equals `Value` (string compare, case-insensitive).
- `before:A\|B >> C\|D` -- some `A`/`B` label occurs, and a `C`/`D` label occurs after it.

**Activity labels here are a measurement binding, never a matching rule.** Every goal model's §7
states that its activity-label table must not be used to pre-filter or lexically pre-match
narratives, because Step 6's matching is semantic. That constraint is about *categorization*.
Locating a clock's endpoints -- or evaluating a per-case predicate -- is a different operation,
performed after categorization, and nothing in this module feeds Steps 5a/6. `goalcat.grl.prompt`
renders an indicator's value set and provenance into the Step 5a excerpt but never its
`goalcat:from`/`goalcat:to`/`goalcat:numerator`/`goalcat:among` binding, for exactly this reason.

**Three ways a case can fail to produce a number, and they are not the same.** Collapsing them into
one value — or worse, into a zero — is a construct error, so they are reported separately:

- `not_applicable`: the case never entered the branch the indicator measures (no appeal was filed,
  so "time to appeal filing" has nothing to say about it). Excluding it is correct.
- `no_start` / `no_end`: the clock has an endpoint missing. In RTFM this is load-bearing — a case
  paid the day after issuance never reaches `Send Fine`, so its dispatch time is undefined *because
  the outcome was good*, and scoring it as a bad value would invert the measurement.
- Right-censoring is the `no_end` case for a still-open case, and is reported with the excluded N
  so a reader can see how much of the log the aggregate actually covers.

A `trace_contains` indicator has no clock, so it only ever yields `measured` (1 when a marker label
appears in the case, 0 otherwise) or, when `applies_when` is set, `not_applicable`. A `case_fraction`
indicator is the same shape with a richer per-case predicate and an explicit denominator: a case
outside `goalcat:among` is `not_applicable`, every other case scores 1 or 0, and the reported value
is their mean (×100 when `goalcat:scale` is `percent`) -- a rate, with `coverage` 1.0 by construction.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Literal

import pandas as pd

from goalcat.config import PipelineConfig

from .model import GRLModel

MEASURE_NAMESPACE = "goalcat:"
DURATION_DAYS = "duration_days"
DURATION_HOURS = "duration_hours"
TRACE_CONTAINS = "trace_contains"
CASE_FRACTION = "case_fraction"

#: Seconds-per-unit divisor for each duration kind: a `pd.Timedelta` is measured in seconds, and
#: the value set declares its bounds in the unit this maps to (`days` / `hours`).
DURATION_DIVISOR = {DURATION_DAYS: 86400.0, DURATION_HOURS: 3600.0}

#: Every `goalcat:measure` value this module knows how to apply.
KNOWN_MEASURES = (*DURATION_DIVISOR, TRACE_CONTAINS, CASE_FRACTION)

#: `goalcat:numerator` predicate prefixes recognised by `_compile_numerator`.
NUMERATOR_PREFIXES = ("has", "lacks", "attr", "before")

CaseStatus = Literal["measured", "not_applicable", "no_start", "no_end"]

#: Value-set provenance classes, worst-grounded last. Carried into every output row so a reader
#: never sees a satisfaction score without knowing what its thresholds rest on. `guideline` sits
#: below `statutory` but above a borrowed norm: a published professional/clinical standard applied
#: to the process it was written for (e.g. the Surviving Sepsis Campaign windows for the Sepsis log).
PROVENANCE_CLASSES = ("statutory", "guideline", "external-by-analogy", "illustrative")


@dataclass(frozen=True)
class MeasureSpec:
    """One indicator's measurement binding, read off its `goalcat:*` metadata. `start_activity`
    holds the raw `goalcat:from` (which may be a `|`-separated set of start labels); `applies_when`
    doubles as the `case_fraction` denominator (`goalcat:among`); `numerator`/`scale` apply only to
    `case_fraction`."""

    indicator_id: str
    indicator_name: str
    kind: str
    start_activity: str
    end_activities: tuple[str, ...]
    end_occurrence: Literal["first", "last"] = "first"
    applies_when: tuple[str, ...] = ()
    aggregate: Literal["mean", "median"] = "mean"
    numerator: str | None = None
    scale: Literal["percent", "fraction"] = "percent"
    provenance: str | None = None
    source: str | None = None


@dataclass(frozen=True)
class MeasureOutcome:
    """An indicator's measurement over one sublog: the aggregate, plus the case bookkeeping that
    makes it interpretable."""

    spec: MeasureSpec
    value: float | None
    n_cases: int
    n_measured: int
    n_not_applicable: int
    n_no_start: int
    n_no_end: int
    per_case: pd.DataFrame = field(repr=False, default_factory=pd.DataFrame)

    @property
    def coverage(self) -> float:
        """Share of in-scope cases that produced a number — 1.0 when nothing was censored. Reported
        beside every aggregate, since an aggregate over 2 of 6 cases is a different claim than one
        over 6 of 6."""
        in_scope = self.n_cases - self.n_not_applicable
        return self.n_measured / in_scope if in_scope else 0.0


def measure_specs(model: GRLModel) -> dict[str, MeasureSpec]:
    """Every indicator in `model` that carries a complete `goalcat:*` binding, keyed by indicator
    id. Indicators without one are skipped silently: a goal model is free to declare an indicator
    it has no way to measure yet, and most of this project's goal models still do. A duration kind
    needs `goalcat:from` and `goalcat:to`; `trace_contains` needs only `goalcat:to` (the marker
    labels); `case_fraction` needs only `goalcat:numerator`."""
    specs: dict[str, MeasureSpec] = {}
    for indicator_id, indicator in model.indicators.items():
        element = model.elements.get(indicator_id)
        metadata = dict(element.metadata) if element is not None else {}
        kind = metadata.get(f"{MEASURE_NAMESPACE}measure")
        if not kind:
            continue
        if kind not in KNOWN_MEASURES:
            raise ValueError(
                f"{model.source_path}: indicator {indicator_id} declares unknown "
                f"{MEASURE_NAMESPACE}measure={kind!r} (known kinds: {', '.join(map(repr, KNOWN_MEASURES))})"
            )

        if kind == CASE_FRACTION:
            numerator = metadata.get(f"{MEASURE_NAMESPACE}numerator")
            if not numerator:
                continue
            _check_numerator(model.source_path, indicator_id, numerator)
            specs[indicator_id] = MeasureSpec(
                indicator_id=indicator_id,
                indicator_name=indicator.name,
                kind=kind,
                start_activity="",
                end_activities=(),
                applies_when=tuple(
                    part.strip() for part in (metadata.get(f"{MEASURE_NAMESPACE}among") or "").split("|") if part.strip()
                ),
                numerator=numerator,
                scale=metadata.get(f"{MEASURE_NAMESPACE}scale", "percent"),  # type: ignore[arg-type]
                provenance=metadata.get(f"{MEASURE_NAMESPACE}provenance"),
                source=metadata.get(f"{MEASURE_NAMESPACE}source"),
            )
            continue

        start = metadata.get(f"{MEASURE_NAMESPACE}from")
        end = metadata.get(f"{MEASURE_NAMESPACE}to")
        if not end:
            continue
        if kind in DURATION_DIVISOR and not start:
            continue
        specs[indicator_id] = MeasureSpec(
            indicator_id=indicator_id,
            indicator_name=indicator.name,
            kind=kind,
            start_activity=start or "",
            end_activities=tuple(part for part in end.split("|") if part),
            end_occurrence=metadata.get(f"{MEASURE_NAMESPACE}to_occurrence", "first"),  # type: ignore[arg-type]
            applies_when=tuple(
                part for part in (metadata.get(f"{MEASURE_NAMESPACE}applies_when") or "").split("|") if part
            ),
            aggregate=metadata.get(f"{MEASURE_NAMESPACE}aggregate", "mean"),  # type: ignore[arg-type]
            provenance=metadata.get(f"{MEASURE_NAMESPACE}provenance"),
            source=metadata.get(f"{MEASURE_NAMESPACE}source"),
        )
    return specs


def measure_sublog(spec: MeasureSpec, sub_df: pd.DataFrame, config: PipelineConfig) -> MeasureOutcome:
    """Applies one `MeasureSpec` to one sublog, case by case.

    For a duration kind the clock starts at the *first* `start_activity` in the case and stops at
    the first or last (per `end_occurrence`) event whose label is in `end_activities` and which is
    not earlier than the start — a stopping label occurring before the clock started belongs to an
    earlier cycle, not to this measurement — and the elapsed time is reported in the unit the kind
    names (`days` or `hours`). For `trace_contains` there is no clock: the per-case value is 1 when
    any `end_activities` label appears in the case and 0 otherwise, so a `mean` aggregate is that
    label's rate of occurrence across the sublog. `case_fraction` is the same 1/0 shape with a
    richer predicate (`spec.numerator`) and an explicit denominator (`spec.applies_when`, from
    `goalcat:among`); the mean is multiplied by 100 unless `spec.scale` is `fraction`.
    """
    if sub_df.empty:
        return MeasureOutcome(spec=spec, value=None, n_cases=0, n_measured=0, n_not_applicable=0, n_no_start=0, n_no_end=0)

    rows: list[dict] = []
    ordered = sub_df.sort_values([config.case_id_key, config.timestamp_key], kind="stable")
    for case_id, case_df in ordered.groupby(config.case_id_key, sort=True):
        rows.append(_measure_case(spec, str(case_id), case_df, config))

    per_case = pd.DataFrame(rows)
    measured = per_case[per_case["status"] == "measured"]
    aggregate = None
    if not measured.empty:
        aggregate = float(measured["value"].mean() if spec.aggregate == "mean" else measured["value"].median())
    if aggregate is not None and spec.kind == CASE_FRACTION and spec.scale == "percent":
        aggregate *= 100.0

    return MeasureOutcome(
        spec=spec,
        value=aggregate,
        n_cases=len(per_case),
        n_measured=int((per_case["status"] == "measured").sum()),
        n_not_applicable=int((per_case["status"] == "not_applicable").sum()),
        n_no_start=int((per_case["status"] == "no_start").sum()),
        n_no_end=int((per_case["status"] == "no_end").sum()),
        per_case=per_case,
    )


def _measure_case(spec: MeasureSpec, case_id: str, case_df: pd.DataFrame, config: PipelineConfig) -> dict:
    activities = case_df[config.activity_key].tolist()
    timestamps = case_df[config.timestamp_key].tolist()

    if spec.applies_when and not any(activity in spec.applies_when for activity in activities):
        return {"case_id": case_id, "status": "not_applicable", "value": None}

    if spec.kind == TRACE_CONTAINS:
        hit = any(activity in spec.end_activities for activity in activities)
        return {"case_id": case_id, "status": "measured", "value": 1.0 if hit else 0.0}

    if spec.kind == CASE_FRACTION:
        predicate = _compile_numerator(spec.numerator or "")
        return {"case_id": case_id, "status": "measured", "value": 1.0 if predicate(activities, case_df) else 0.0}

    start_labels = _split_labels(spec.start_activity)
    start_index = next((i for i, activity in enumerate(activities) if activity in start_labels), None)
    if start_index is None:
        return {"case_id": case_id, "status": "no_start", "value": None}

    end_indices = [i for i in range(start_index, len(activities)) if activities[i] in spec.end_activities]
    if not end_indices:
        return {"case_id": case_id, "status": "no_end", "value": None}

    end_index = end_indices[0] if spec.end_occurrence == "first" else end_indices[-1]
    delta = pd.Timestamp(timestamps[end_index]) - pd.Timestamp(timestamps[start_index])
    return {"case_id": case_id, "status": "measured", "value": delta.total_seconds() / DURATION_DIVISOR[spec.kind]}


CasePredicate = Callable[[list[str], pd.DataFrame], bool]


@lru_cache(maxsize=None)
def _split_labels(value: str) -> tuple[str, ...]:
    """A `|`-separated activity-label list, trimmed and with empties dropped. Cached because
    `_measure_case` asks for the same `goalcat:from` split once per case."""
    return tuple(part.strip() for part in value.split("|") if part.strip())


def _check_numerator(source_path: str, indicator_id: str, numerator: str) -> None:
    """Compiles `numerator` once at spec-build time so a malformed predicate fails loudly here
    rather than silently scoring every case 0."""
    try:
        _compile_numerator(numerator)
    except ValueError as exc:
        raise ValueError(
            f"{source_path}: indicator {indicator_id} has a malformed "
            f"{MEASURE_NAMESPACE}numerator={numerator!r}: {exc}"
        ) from exc


@lru_cache(maxsize=None)
def _compile_numerator(numerator: str) -> CasePredicate:
    """Compiles a `goalcat:numerator` predicate string into a `(activities, case_df) -> bool`
    callable. Raises `ValueError` on an unknown prefix or a malformed body. Cached so the parse
    cost is paid once per distinct predicate, not once per case."""
    prefix, _, rest = numerator.partition(":")
    prefix, rest = prefix.strip(), rest.strip()
    if not rest:
        raise ValueError("empty predicate body")

    if prefix in ("has", "lacks"):
        labels = frozenset(_split_labels(rest))
        if not labels:
            raise ValueError("no activity labels")
        want_hit = prefix == "has"
        return lambda activities, _case_df: any(a in labels for a in activities) == want_hit

    if prefix == "attr":
        key, sep, value = rest.partition("=")
        if not sep:
            raise ValueError("attr predicate needs 'Key=Value'")
        column = f"case:{key.strip()}"
        wanted = value.strip().lower()

        def _attr(_activities: list[str], case_df: pd.DataFrame) -> bool:
            if case_df.empty or column not in case_df.columns:
                return False
            return str(case_df[column].iloc[0]).strip().lower() == wanted

        return _attr

    if prefix == "before":
        left_raw, sep, right_raw = rest.partition(">>")
        if not sep:
            raise ValueError("before predicate needs 'LEFT >> RIGHT'")
        left = frozenset(_split_labels(left_raw))
        right = frozenset(_split_labels(right_raw))
        if not left or not right:
            raise ValueError("before predicate needs labels on both sides of '>>'")

        def _before(activities: list[str], _case_df: pd.DataFrame) -> bool:
            first_left = next((i for i, a in enumerate(activities) if a in left), None)
            return first_left is not None and any(a in right for a in activities[first_left + 1:])

        return _before

    raise ValueError(f"unknown predicate prefix {prefix!r} (known: {NUMERATOR_PREFIXES})")

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
| `goalcat:measure` | measurement kind; only `duration_days` exists today | `duration_days` |
| `goalcat:from` | activity label starting the clock | `Create Fine` |
| `goalcat:to` | `\|`-separated activity labels that can stop it | `Payment\|Send for Credit Collection` |
| `goalcat:to_occurrence` | which stopping event counts, `first` or `last` | `first` |
| `goalcat:applies_when` | `\|`-separated labels; a case lacking all of them is *out of scope* | `Appeal to Judge` |
| `goalcat:aggregate` | how per-case values combine, `mean` or `median` | `mean` |
| `goalcat:provenance` | where the value set's bounds come from | `statutory` |
| `goalcat:source` | the citation backing them | `Art. 201 D.Lgs. 285/1992` |

**Activity labels here are a measurement binding, never a matching rule.** Every goal model's §7
states that its activity-label table must not be used to pre-filter or lexically pre-match
narratives, because Step 6's matching is semantic. That constraint is about *categorization*.
Locating a clock's endpoints in a trace is a different operation, performed after categorization,
and nothing in this module feeds Steps 5a/6.

**Three ways a case can fail to produce a number, and they are not the same.** Collapsing them into
one value — or worse, into a zero — is a construct error, so they are reported separately:

- `not_applicable`: the case never entered the branch the indicator measures (no appeal was filed,
  so "time to appeal filing" has nothing to say about it). Excluding it is correct.
- `no_start` / `no_end`: the clock has an endpoint missing. In RTFM this is load-bearing — a case
  paid the day after issuance never reaches `Send Fine`, so its dispatch time is undefined *because
  the outcome was good*, and scoring it as a bad value would invert the measurement.
- Right-censoring is the `no_end` case for a still-open case, and is reported with the excluded N
  so a reader can see how much of the log the aggregate actually covers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

import pandas as pd

from goalcat.config import PipelineConfig

from .model import GRLModel

MEASURE_NAMESPACE = "goalcat:"
DURATION_DAYS = "duration_days"

CaseStatus = Literal["measured", "not_applicable", "no_start", "no_end"]

#: Value-set provenance classes, worst-grounded last. Carried into every output row so a reader
#: never sees a satisfaction score without knowing what its thresholds rest on.
PROVENANCE_CLASSES = ("statutory", "external-by-analogy", "illustrative")


@dataclass(frozen=True)
class MeasureSpec:
    """One indicator's measurement binding, read off its `goalcat:*` metadata."""

    indicator_id: str
    indicator_name: str
    kind: str
    start_activity: str
    end_activities: tuple[str, ...]
    end_occurrence: Literal["first", "last"] = "first"
    applies_when: tuple[str, ...] = ()
    aggregate: Literal["mean", "median"] = "mean"
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
    it has no way to measure yet, and that is what every model outside RTFM currently does."""
    specs: dict[str, MeasureSpec] = {}
    for indicator_id, indicator in model.indicators.items():
        element = model.elements.get(indicator_id)
        metadata = dict(element.metadata) if element is not None else {}
        kind = metadata.get(f"{MEASURE_NAMESPACE}measure")
        start = metadata.get(f"{MEASURE_NAMESPACE}from")
        end = metadata.get(f"{MEASURE_NAMESPACE}to")
        if not (kind and start and end):
            continue
        if kind != DURATION_DAYS:
            raise ValueError(
                f"{model.source_path}: indicator {indicator_id} declares unknown "
                f"{MEASURE_NAMESPACE}measure={kind!r} (known kinds: {DURATION_DAYS!r})"
            )
        specs[indicator_id] = MeasureSpec(
            indicator_id=indicator_id,
            indicator_name=indicator.name,
            kind=kind,
            start_activity=start,
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

    The clock starts at the *first* `start_activity` in the case and stops at the first or last
    (per `end_occurrence`) event whose label is in `end_activities` and which is not earlier than
    the start — a stopping label occurring before the clock started belongs to an earlier cycle,
    not to this measurement. Duration is reported in fractional days, matching the `unit="days"`
    the value sets declare.
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
        aggregate = float(measured["value_days"].mean() if spec.aggregate == "mean" else measured["value_days"].median())

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
        return {"case_id": case_id, "status": "not_applicable", "value_days": None}

    start_index = next((i for i, activity in enumerate(activities) if activity == spec.start_activity), None)
    if start_index is None:
        return {"case_id": case_id, "status": "no_start", "value_days": None}

    end_indices = [i for i in range(start_index, len(activities)) if activities[i] in spec.end_activities]
    if not end_indices:
        return {"case_id": case_id, "status": "no_end", "value_days": None}

    end_index = end_indices[0] if spec.end_occurrence == "first" else end_indices[-1]
    delta = pd.Timestamp(timestamps[end_index]) - pd.Timestamp(timestamps[start_index])
    return {"case_id": case_id, "status": "measured", "value_days": delta.total_seconds() / 86400.0}

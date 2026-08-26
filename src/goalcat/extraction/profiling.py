from __future__ import annotations

import json
import statistics
from pathlib import Path

import pandas as pd
import pm4py

from ..atomic_io import atomic_write_csv, atomic_write_json
from ..config import PipelineConfig


def select_representative_case(subdf: pd.DataFrame, config: PipelineConfig) -> str:
    """Return the case id whose duration is closest to the median duration in this variant."""
    case_durations = {
        case_id: (case_df[config.timestamp_key].max() - case_df[config.timestamp_key].min()).total_seconds()
        for case_id, case_df in subdf.groupby(config.case_id_key)
    }
    median = statistics.median(case_durations.values())
    return min(case_durations, key=lambda case_id: abs(case_durations[case_id] - median))


def format_duration_display(seconds: float) -> str:
    """Compact rendering of a duration ("90d", "3h", "45m", "12s"), picking the coarsest unit that
    keeps the value >= 1. Shared by the narrative's inter-event waits (via
    `_format_waiting_display`, which only prefixes "+") and by the Step 5a/6 prompt header's
    variant duration, so a reader comparing the two reads one scale rather than converting raw
    seconds in their head. Returns "0s" for a zero duration -- a real measurement, unlike the
    zero *wait* of a trace's first event, which `_format_waiting_display` suppresses instead.
    """
    total = round(seconds)
    if total == 0:
        return "0s"
    if total >= 86400:
        return f"{round(total / 86400)}d"
    if total >= 3600:
        hours = round(total / 3600)
        return "1d" if hours == 24 else f"{hours}h"
    if total >= 60:
        minutes = round(total / 60)
        return "1h" if minutes == 60 else f"{minutes}m"
    return "1m" if total == 60 else f"{total}s"


def _format_waiting_display(seconds: float) -> str:
    """Compact suffix rendering of a waiting duration ("+90d", "+3h", "+45m", "+12s"), picking
    the coarsest unit that keeps the value >= 1 (seconds/minutes/hours/days). RTFM's statutory
    indicators are all whole-day thresholds (90/60/120/180/360/365 days,
    data/goals/rtfmGM_description.md:197-199), so day-level rounding on day-scale waits is
    lossless; short waits keep finer resolution.

    Rounds to the nearest whole unit within a tier, carrying into the next tier when that
    rounds up to it (e.g. 86399s -> "+1d", not "+24h"). Returns "" for a zero wait (always the
    first event in a trace, which has no prior step to wait on); the caller's template omits
    the suffix entirely rather than rendering an uninformative "+0s".

    Compact form adopted as the pipeline's default narrative rendering (2026-08-25).
    """
    if round(seconds) == 0:
        return ""
    return "+" + format_duration_display(seconds)


#: Resource values that mean "no resource recorded" despite being present as a non-null string.
#: bpic2019 stores the literal "NONE" in its resource column, which is truthy in the narrative
#: template's `{% if resource %}` guard, so every event of every sampled variant rendered a
#: "(handled by resource NONE)" clause -- 2,039 occurrences and 10.6% of that log's Step 5a prompt.
#: Normalising here rather than in the template keeps the sentinel list out of the CC BY-NC-SA
#: `third_party/` boundary, alongside the unit conversion already kept out for the same reason.
_RESOURCE_SENTINELS = {"none", "nan", "null", "unknown", "n/a", "na", "-", ""}


def _normalize_resource(resource) -> str | None:
    """None for a missing resource, including the sentinel strings above. Comparison is
    case-insensitive on the stripped value; the original string is returned otherwise, never a
    normalised form, so a genuine resource id reaches the narrative exactly as the log spells it."""
    if pd.isna(resource):
        return None
    return None if str(resource).strip().lower() in _RESOURCE_SENTINELS else resource


def build_event_profile(rep_case_df: pd.DataFrame, config: PipelineConfig) -> list[dict]:
    """Render the representative case's events, ordered, with waiting time since the prior event."""
    ordered = rep_case_df.sort_values(config.timestamp_key)
    has_resource = config.resource_key in ordered.columns

    events = []
    previous_timestamp = None
    for _, row in ordered.iterrows():
        timestamp = row[config.timestamp_key]
        waiting_seconds = (timestamp - previous_timestamp).total_seconds() if previous_timestamp is not None else 0.0
        resource = row[config.resource_key] if has_resource else None
        events.append(
            {
                "activity": row[config.activity_key],
                "timestamp": timestamp.isoformat(),
                "resource": _normalize_resource(resource),
                "waiting_seconds": waiting_seconds,
                "waiting_display": _format_waiting_display(waiting_seconds),
            }
        )
        previous_timestamp = timestamp
    return events


def profile_variant(subdf: pd.DataFrame, activity_sequence: tuple[str, ...], config: PipelineConfig) -> dict:
    """Compute the multi-view profile (duration, rework, outcome, resource) for one variant."""
    durations = pm4py.stats.get_all_case_durations(
        subdf,
        activity_key=config.activity_key,
        timestamp_key=config.timestamp_key,
        case_id_key=config.case_id_key,
    )
    rework = pm4py.stats.get_rework_cases_per_activity(
        subdf,
        activity_key=config.activity_key,
        timestamp_key=config.timestamp_key,
        case_id_key=config.case_id_key,
    )
    resource_distribution = (
        pm4py.stats.get_event_attribute_values(subdf, config.resource_key, case_id_key=config.case_id_key)
        if config.resource_key in subdf.columns
        else {}
    )

    representative_case_id = select_representative_case(subdf, config)
    rep_case_df = subdf[subdf[config.case_id_key] == representative_case_id]

    return {
        "representative_case_id": representative_case_id,
        "duration_seconds_mean": statistics.mean(durations),
        "duration_seconds_median": statistics.median(durations),
        "duration_seconds_min": min(durations),
        "duration_seconds_max": max(durations),
        "outcome": activity_sequence[-1],
        "rework": rework,
        "resource_distribution": resource_distribution,
        "events": build_event_profile(rep_case_df, config),
    }


def profile_variants(df: pd.DataFrame, variants_df: pd.DataFrame, config: PipelineConfig) -> pd.DataFrame:
    """Enrich the variants table with a multi-view profile per variant (pipeline Step 2)."""
    profiles = []
    for _, variant_row in variants_df.iterrows():
        subdf = df[df[config.case_id_key].isin(variant_row["case_ids"])]
        profiles.append(profile_variant(subdf, variant_row["activity_sequence"], config))

    return pd.concat([variants_df.reset_index(drop=True), pd.DataFrame(profiles)], axis=1)


def save_profiles(profiles_df: pd.DataFrame, csv_path: Path, json_path: Path) -> None:
    """Write the flat summary as CSV and the nested representative-case events as JSON."""
    csv_columns = [
        "variant_id",
        "activity_sequence",
        "trace_length",
        "frequency",
        "frequency_pct",
        "representative_case_id",
        "duration_seconds_mean",
        "duration_seconds_median",
        "duration_seconds_min",
        "duration_seconds_max",
        "outcome",
        "rework",
        "resource_distribution",
    ]
    export_df = profiles_df[csv_columns].copy()
    export_df["activity_sequence"] = export_df["activity_sequence"].apply(">".join)
    export_df["rework"] = export_df["rework"].apply(_join_counts)
    export_df["resource_distribution"] = export_df["resource_distribution"].apply(_join_counts)
    atomic_write_csv(export_df, csv_path, index=False)

    json_records = [
        {
            "variant_id": row["variant_id"],
            "activity_sequence": list(row["activity_sequence"]),
            "representative_case_id": row["representative_case_id"],
            "events": row["events"],
        }
        for _, row in profiles_df.iterrows()
    ]
    atomic_write_json(json_path, json_records)


def _parse_counts(joined: str) -> dict[str, int]:
    if not isinstance(joined, str) or not joined:
        return {}
    return json.loads(joined)


def load_profiles(csv_path: Path, json_path: Path) -> pd.DataFrame:
    """Inverse of save_profiles: reconstructs activity_sequence as a tuple, rework/
    resource_distribution as dicts, and events from the JSON sidecar — the same shape
    profile_variants() produces in-memory, minus case_ids (save_profiles never persists it;
    nothing downstream of a loaded profiles_df currently needs it)."""
    profiles_df = pd.read_csv(csv_path, dtype={"variant_id": str, "representative_case_id": str})
    profiles_df["activity_sequence"] = profiles_df["activity_sequence"].apply(lambda s: tuple(s.split(">")))
    profiles_df["rework"] = profiles_df["rework"].apply(_parse_counts)
    profiles_df["resource_distribution"] = profiles_df["resource_distribution"].apply(_parse_counts)

    with open(json_path, "r", encoding="utf-8") as f:
        json_records = json.load(f)
    events_by_variant = {record["variant_id"]: record["events"] for record in json_records}
    profiles_df["events"] = profiles_df["variant_id"].map(events_by_variant)
    return profiles_df


def _join_counts(counts: dict) -> str:
    return json.dumps(counts)

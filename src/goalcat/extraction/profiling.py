from __future__ import annotations

import json
import statistics
from pathlib import Path

import pandas as pd
import pm4py

from ..config import PipelineConfig


def select_representative_case(subdf: pd.DataFrame, config: PipelineConfig) -> str:
    """Return the case id whose duration is closest to the median duration in this variant."""
    case_durations = {
        case_id: (case_df[config.timestamp_key].max() - case_df[config.timestamp_key].min()).total_seconds()
        for case_id, case_df in subdf.groupby(config.case_id_key)
    }
    median = statistics.median(case_durations.values())
    return min(case_durations, key=lambda case_id: abs(case_durations[case_id] - median))


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
                "resource": None if pd.isna(resource) else resource,
                "waiting_seconds": waiting_seconds,
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
    csv_path.parent.mkdir(parents=True, exist_ok=True)

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
    export_df.to_csv(csv_path, index=False)

    json_records = [
        {
            "variant_id": row["variant_id"],
            "activity_sequence": list(row["activity_sequence"]),
            "representative_case_id": row["representative_case_id"],
            "events": row["events"],
        }
        for _, row in profiles_df.iterrows()
    ]
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_records, f, indent=2)


def _parse_counts(joined: str) -> dict[str, int]:
    if not isinstance(joined, str) or not joined:
        return {}
    return {key: int(value) for key, value in (pair.split(":", 1) for pair in joined.split(","))}


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
    return ",".join(f"{key}:{value}" for key, value in counts.items())

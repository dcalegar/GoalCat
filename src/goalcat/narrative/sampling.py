from __future__ import annotations

from pathlib import Path

import pandas as pd

from ..config import PipelineConfig

_PROFILE_COLUMNS = [
    "variant_id",
    "frequency",
    "frequency_pct",
    "trace_length",
    "duration_seconds_median",
    "outcome",
]


def sample_narratives(profiles_df: pd.DataFrame, narratives_df: pd.DataFrame, config: PipelineConfig) -> pd.DataFrame:
    """Draw a frequent/rare/extreme narrative sample to calibrate taxonomy granularity (Step 4).

    Deterministic by construction: profiles_df's row order already comes from Step 1's stable
    sort by frequency, so nlargest/nsmallest (keep="first") break ties the same way every run.
    """
    merged = profiles_df[_PROFILE_COLUMNS].merge(narratives_df, on="variant_id", how="inner")

    buckets = {
        "frequent": merged.nlargest(config.sample_frequent_n, "frequency"),
        "rare": merged.nsmallest(config.sample_rare_n, "frequency"),
        "duration_high": merged.nlargest(config.sample_extreme_n, "duration_seconds_median"),
        "duration_low": merged.nsmallest(config.sample_extreme_n, "duration_seconds_median"),
        "length_high": merged.nlargest(config.sample_extreme_n, "trace_length"),
        "length_low": merged.nsmallest(config.sample_extreme_n, "trace_length"),
    }

    reasons_by_variant: dict[str, list[str]] = {}
    for reason, bucket_df in buckets.items():
        for variant_id in bucket_df["variant_id"]:
            reasons_by_variant.setdefault(variant_id, []).append(reason)

    sample_df = merged[merged["variant_id"].isin(reasons_by_variant)].copy()
    sample_df["sample_reasons"] = sample_df["variant_id"].map(lambda vid: ",".join(reasons_by_variant[vid]))
    sample_df = sample_df.sort_values("frequency", ascending=False).reset_index(drop=True)

    columns = ["variant_id", "sample_reasons"] + _PROFILE_COLUMNS[1:] + ["narrative"]
    return sample_df[columns]


def save_narrative_sample(sample_df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    sample_df.to_csv(path, index=False)


def load_narrative_sample(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, dtype={"variant_id": str})

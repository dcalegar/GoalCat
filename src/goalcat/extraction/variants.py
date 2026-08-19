from __future__ import annotations

from pathlib import Path

import pandas as pd
import pm4py

from ..config import PipelineConfig


def extract_variants(df: pd.DataFrame, config: PipelineConfig) -> pd.DataFrame:
    """Group traces that share the same activity sequence (pipeline Step 1)."""
    records = []
    for activity_sequence, subdf in pm4py.split_by_process_variant(
        df,
        activity_key=config.activity_key,
        timestamp_key=config.timestamp_key,
        case_id_key=config.case_id_key,
    ):
        case_ids = subdf[config.case_id_key].unique().tolist()
        records.append(
            {
                "activity_sequence": tuple(activity_sequence),
                "trace_length": len(activity_sequence),
                "case_ids": case_ids,
                "frequency": len(case_ids),
            }
        )

    total_cases = sum(record["frequency"] for record in records)
    for record in records:
        record["frequency_pct"] = record["frequency"] / total_cases

    variants_df = pd.DataFrame.from_records(records)
    # kind="stable" (mergesort), not the pandas default (quicksort, not stable for ties):
    # V#### is assigned by row position right after this sort, and RTFM alone has ~100
    # equal-frequency (singleton) variants — without a stable sort, which physical variant
    # gets "V0001" among a tied group can drift between runs on the identical log, even
    # though sampling.py's own docstring already claims Steps 1-4 are "deterministic by
    # construction." Verified: pandas 3.0.5's default quicksort does reorder an all-tied frame.
    variants_df = variants_df.sort_values("frequency", ascending=False, kind="stable").reset_index(drop=True)
    variants_df.insert(0, "variant_id", [f"V{i + 1:04d}" for i in range(len(variants_df))])
    return variants_df


def save_variants(variants_df: pd.DataFrame, path: Path) -> None:
    """Write the variants table as a CSV, joining list-typed fields into delimited strings."""
    path.parent.mkdir(parents=True, exist_ok=True)
    export_df = variants_df.copy()
    export_df["activity_sequence"] = export_df["activity_sequence"].apply(">".join)
    export_df["case_ids"] = export_df["case_ids"].apply(",".join)
    export_df.to_csv(path, index=False)


def load_variants(path: Path) -> pd.DataFrame:
    """Inverse of save_variants: reconstructs activity_sequence as a tuple and case_ids as a
    list, so a run directory's variants.csv round-trips to the same shape extract_variants()
    produces in-memory."""
    # keep_default_na=False: every column here is always populated (a variant always has a
    # non-empty case_ids/activity_sequence), and pandas' default na_values list includes "NA" —
    # a real case ID in the Sepsis Cases log, which would otherwise round-trip through
    # save_variants/load_variants as a float NaN instead of the string "NA".
    variants_df = pd.read_csv(path, dtype={"variant_id": str}, keep_default_na=False)
    variants_df["activity_sequence"] = variants_df["activity_sequence"].apply(lambda s: tuple(s.split(">")))
    variants_df["case_ids"] = variants_df["case_ids"].apply(lambda s: s.split(","))
    return variants_df

from __future__ import annotations

import itertools
import math

import pandas as pd
from pm4py.util import string_distance

_PROFILE_COMPONENTS = ["outcome_mismatch", "duration_log_distance", "rework_jaccard"]


def compute_structural_distances(profiles_df: pd.DataFrame) -> pd.DataFrame:
    """Pairwise control-flow distance between every pair of variants (Levenshtein edit distance
    on activity_sequence, via pm4py's own implementation, preferred over a hand-rolled distance
    per this project's standing practice of using a PM4Py primitive when one exists). Measures
    control-flow proximity only, not business equivalence: two variants realizing business-
    distinct outcomes can still have near-identical activity sequences (RTFM's TP/TA distinction,
    documented in its frozen goal model, is exactly this case), so this is reported alongside
    compute_profile_distances(), never in place of it.
    """
    rows = []
    for (id_a, seq_a), (id_b, seq_b) in itertools.combinations(
        zip(profiles_df["variant_id"], profiles_df["activity_sequence"]), 2
    ):
        distance = string_distance.levenshtein_distance(seq_a, seq_b)
        rows.append({"variant_id_a": id_a, "variant_id_b": id_b, "distance": distance})
    return pd.DataFrame(rows, columns=["variant_id_a", "variant_id_b", "distance"])


def compute_profile_distances(profiles_df: pd.DataFrame) -> pd.DataFrame:
    """Pairwise business-profile distance between every pair of variants, combining outcome,
    duration, and rework (three of Step 2's multi-view profile dimensions). Each component is
    reported as its own column, not silently averaged away, plus profile_distance_mean as an
    unweighted (not fitted) convenience summary — see similarity design note in PROGRESS.md.
    """
    durations = profiles_df["duration_seconds_median"].tolist()
    log_durations = [math.log(max(d, 1.0)) for d in durations]
    log_span = max(log_durations) - min(log_durations) if log_durations else 0.0

    records = list(
        zip(
            profiles_df["variant_id"],
            log_durations,
            profiles_df["outcome"],
            profiles_df["rework"],
        )
    )

    rows = []
    for (id_a, dur_a, outcome_a, rework_a), (id_b, dur_b, outcome_b, rework_b) in itertools.combinations(
        records, 2
    ):
        outcome_mismatch = 0.0 if outcome_a == outcome_b else 1.0

        duration_log_distance = abs(dur_a - dur_b) / log_span if log_span > 0 else 0.0

        keys_a, keys_b = set(rework_a), set(rework_b)
        union = keys_a | keys_b
        rework_jaccard = 1.0 - len(keys_a & keys_b) / len(union) if union else 0.0

        profile_distance_mean = (outcome_mismatch + duration_log_distance + rework_jaccard) / 3

        rows.append(
            {
                "variant_id_a": id_a,
                "variant_id_b": id_b,
                "outcome_mismatch": outcome_mismatch,
                "duration_log_distance": duration_log_distance,
                "rework_jaccard": rework_jaccard,
                "profile_distance_mean": profile_distance_mean,
            }
        )
    return pd.DataFrame(
        rows,
        columns=["variant_id_a", "variant_id_b", *_PROFILE_COMPONENTS, "profile_distance_mean"],
    )


def nearest_variants(
    variant_id: str,
    distances_df: pd.DataFrame,
    distance_column: str = "distance",
    k: int = 5,
    exclude_ids: set[str] | None = None,
) -> pd.DataFrame:
    """The k closest other variants to variant_id, by distance_column, ascending.

    Returns columns [variant_id, distance_column]. Works with either compute_structural_distances'
    or compute_profile_distances' long-form output (pass distance_column="profile_distance_mean"
    for the latter).
    """
    exclude_ids = exclude_ids or set()

    as_a = distances_df[distances_df["variant_id_a"] == variant_id][["variant_id_b", distance_column]]
    as_a = as_a.rename(columns={"variant_id_b": "variant_id"})
    as_b = distances_df[distances_df["variant_id_b"] == variant_id][["variant_id_a", distance_column]]
    as_b = as_b.rename(columns={"variant_id_a": "variant_id"})

    combined = pd.concat([as_a, as_b], ignore_index=True)
    combined = combined[~combined["variant_id"].isin(exclude_ids | {variant_id})]
    return combined.sort_values(distance_column, ascending=True).head(k).reset_index(drop=True)

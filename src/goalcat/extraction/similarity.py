from __future__ import annotations

import numpy as np
import pandas as pd
from rapidfuzz import process
from rapidfuzz.distance import Levenshtein
from scipy import sparse

_PROFILE_COMPONENTS = ["outcome_mismatch", "duration_log_distance", "rework_jaccard"]

_EMPTY_STRUCTURAL_COLUMNS = ["variant_id_a", "variant_id_b", "distance"]
_EMPTY_PROFILE_COLUMNS = ["variant_id_a", "variant_id_b", *_PROFILE_COMPONENTS, "profile_distance_mean"]


def empty_structural_distances() -> pd.DataFrame:
    """Schema-valid, zero-row structural-distance table — the n<2 shape compute_structural_distances()
    already returns, reused by callers that skip the O(n^2) computation outright (config.skip_pairwise_distances)
    rather than duplicating the column list."""
    return pd.DataFrame(columns=_EMPTY_STRUCTURAL_COLUMNS)


def empty_profile_distances() -> pd.DataFrame:
    """Schema-valid, zero-row profile-distance table — see empty_structural_distances()."""
    return pd.DataFrame(columns=_EMPTY_PROFILE_COLUMNS)


def _pair_frame(variant_ids: list[str], n: int) -> tuple[np.ndarray, np.ndarray, pd.Categorical, pd.Categorical]:
    """The (i, j) index pairs for every i<j combination, plus the corresponding variant_id_a/b
    columns as pandas Categoricals rather than plain object/string columns: at BPIC 2019 scale
    (11,973 variants, ~71.7M pairs) a Categorical stores each id once and every row as a 2-byte
    code, instead of ~71.7M duplicated Python string objects — the difference between the
    resulting DataFrame fitting in a few hundred MB and the tens-of-GB `rows.append({...})`
    pattern this replaced (measured: ~19-25 GB for the two distance tables at this scale, before
    a single CSV was written)."""
    idx_a, idx_b = np.triu_indices(n, k=1)
    codes_a = idx_a.astype(np.int32, copy=False)
    codes_b = idx_b.astype(np.int32, copy=False)
    return (
        idx_a,
        idx_b,
        pd.Categorical.from_codes(codes_a, categories=variant_ids),
        pd.Categorical.from_codes(codes_b, categories=variant_ids),
    )


def compute_structural_distances(profiles_df: pd.DataFrame) -> pd.DataFrame:
    """Pairwise control-flow distance between every pair of variants (Levenshtein edit distance
    on activity_sequence). Measures control-flow proximity only, not business equivalence: two
    variants realizing business-distinct outcomes can still have near-identical activity
    sequences (RTFM's TP/TA distinction, documented in its frozen goal model, is exactly this
    case), so this is reported alongside compute_profile_distances(), never in place of it.

    Uses rapidfuzz's process.cdist (a multi-threaded C implementation), not pm4py's own
    string_distance.levenshtein_distance — verified byte-identical against it on real data, but
    ~25x faster per pair, and cdist computes the whole n x n matrix in one multi-threaded call
    rather than n*(n-1)/2 individual Python-level calls. At BPIC 2019 scale this is the
    difference between ~2s and ~1h of wall clock (the itertools.combinations loop this replaced
    would also OOM well before finishing, independent of its speed — see _pair_frame's docstring).
    """
    variant_ids = profiles_df["variant_id"].tolist()
    sequences = profiles_df["activity_sequence"].tolist()
    n = len(variant_ids)
    if n < 2:
        return empty_structural_distances()

    distance_matrix = process.cdist(sequences, sequences, scorer=Levenshtein.distance, workers=-1, dtype=np.int32)

    idx_a, idx_b, variant_id_a, variant_id_b = _pair_frame(variant_ids, n)
    return pd.DataFrame(
        {
            "variant_id_a": variant_id_a,
            "variant_id_b": variant_id_b,
            "distance": distance_matrix[idx_a, idx_b],
        }
    )


def compute_profile_distances(profiles_df: pd.DataFrame) -> pd.DataFrame:
    """Pairwise business-profile distance between every pair of variants, combining outcome,
    duration, and rework (three of Step 2's multi-view profile dimensions). Each component is
    reported as its own column, not silently averaged away, plus profile_distance_mean as an
    unweighted (not fitted) convenience summary.

    Vectorized over the full n x n pair space (outcome/duration via NumPy broadcasting, rework
    via a sparse binary variant-by-rework-key matrix whose Gram matrix gives pairwise
    intersection sizes) rather than a per-pair Python loop — same formulas as before, verified
    equivalent, but the earlier itertools.combinations loop is what made this and
    compute_structural_distances() together OOM on BPIC 2019's ~71.7M pairs.
    """
    variant_ids = profiles_df["variant_id"].tolist()
    n = len(variant_ids)
    if n < 2:
        return empty_profile_distances()

    idx_a, idx_b, variant_id_a, variant_id_b = _pair_frame(variant_ids, n)

    durations = profiles_df["duration_seconds_median"].to_numpy(dtype=np.float64)
    log_durations = np.log(np.maximum(durations, 1.0))
    log_span = float(log_durations.max() - log_durations.min())
    if log_span > 0:
        duration_log_distance = (np.abs(log_durations[idx_a] - log_durations[idx_b]) / log_span).astype(np.float32)
    else:
        duration_log_distance = np.zeros(len(idx_a), dtype=np.float32)

    outcome_codes = pd.factorize(profiles_df["outcome"].to_numpy())[0]
    outcome_mismatch = (outcome_codes[idx_a] != outcome_codes[idx_b]).astype(np.float32)

    rework_list = profiles_df["rework"].tolist()
    rework_keys = sorted({key for rework in rework_list for key in rework})
    key_index = {key: col for col, key in enumerate(rework_keys)}
    rows_, cols_ = [], []
    for row, rework in enumerate(rework_list):
        for key in rework:
            rows_.append(row)
            cols_.append(key_index[key])
    rework_matrix = sparse.csr_matrix(
        (np.ones(len(rows_), dtype=np.float32), (rows_, cols_)), shape=(n, len(rework_keys))
    )
    rework_sizes = np.asarray(rework_matrix.sum(axis=1)).ravel()
    # Gram matrix: (rework_matrix @ rework_matrix.T)[i, j] is |rework_keys_i & rework_keys_j|
    # for binary rows. Dense only transiently — same n x n footprint as the structural distance
    # matrix (≈573 MB at BPIC 2019 scale), immediately reduced to the upper-triangle pair vector.
    intersection = np.asarray((rework_matrix @ rework_matrix.T).todense())[idx_a, idx_b]
    union = rework_sizes[idx_a] + rework_sizes[idx_b] - intersection
    rework_jaccard = np.where(union > 0, 1.0 - intersection / np.maximum(union, 1), 0.0).astype(np.float32)

    profile_distance_mean = ((outcome_mismatch + duration_log_distance + rework_jaccard) / 3).astype(np.float32)

    return pd.DataFrame(
        {
            "variant_id_a": variant_id_a,
            "variant_id_b": variant_id_b,
            "outcome_mismatch": outcome_mismatch,
            "duration_log_distance": duration_log_distance,
            "rework_jaccard": rework_jaccard,
            "profile_distance_mean": profile_distance_mean,
        }
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

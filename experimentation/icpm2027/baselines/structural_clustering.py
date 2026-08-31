"""Task C3 — structural (boolean activity-vector + HDBSCAN) clustering baseline.

A boolean activity-vector representation of the same variants, clustered with HDBSCAN (the
representation used by Amling et al., 2025, the architecture's most direct antecedent in the
Related Work), fed into the same contingency-matrix and coverage machinery as T^G and T^O. No
LLM cost. This is the one baseline the Related Work argues against but the current design never
runs.

Deliberately the simplest possible representation of "what the Related Work does instead":
one boolean column per distinct activity label observed anywhere in the log, one row per variant,
no order/duration/rework/resource information at all — the exact structural-only signal GoalCat's
own narrative-based Step 5/6 is positioned against (the Related Work, and the
`rtfm_mini` PoC's own two-rework-variants-collapse-to-one-vector demonstration, Task C8).

HDBSCAN's own noise label (`-1`) becomes this baseline's residual, directly comparable to the
guided/open arms' own "no category fits" residual — both are "this variant did not fit any
category," just produced by a different mechanism (density vs. semantic judgment).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from sklearn.cluster import HDBSCAN


@dataclass(frozen=True)
class StructuralClusteringResult:
    """One HDBSCAN run's output, in the same (variant_id -> category_id-or-None) shape
    `analysis.contingency` expects from any partition — guided, open, or this baseline."""

    assignments: dict[str, str | None]  # variant_id -> "cluster_{n}" or None (HDBSCAN noise)
    cluster_sizes: dict[str, int]  # cluster_id -> variant count
    n_clusters: int
    n_noise: int
    min_cluster_size: int
    activity_vocabulary: tuple[str, ...]

    def as_assignments_df(self) -> pd.DataFrame:
        """Same two-column shape as `goalcat`'s own `assignments.csv` (`variant_id`,
        `category_id`), so every existing coverage/contingency helper written against a real
        Step 6 output works against this baseline unmodified."""
        return pd.DataFrame(
            {"variant_id": list(self.assignments), "category_id": list(self.assignments.values())}
        )


def build_activity_vectors(variants_df: pd.DataFrame) -> tuple[np.ndarray, tuple[str, ...], list[str]]:
    """One boolean row per variant, one column per distinct activity label observed anywhere in
    the (scoped) log — the representation itself, decoupled from clustering so it can be unit
    tested and reused (e.g. for a future non-HDBSCAN comparison) on its own.

    `variants_df` needs a `variant_id` column and an `activity_sequence` column, either as tuples
    (the shape `goalcat.extraction.variants.load_variants()` produces) or as the `>`-joined string
    the raw `01_variants/variants.csv` stores — a plain `pd.read_csv` of that file gives the
    latter, and iterating it without splitting would vectorize *characters*, not activities.
    """

    def _activities(sequence) -> list[str]:
        if isinstance(sequence, str):
            return [a.strip() for a in sequence.split(">")]
        return list(sequence)

    vocabulary = sorted({activity for sequence in variants_df["activity_sequence"] for activity in _activities(sequence)})
    index = {activity: position for position, activity in enumerate(vocabulary)}

    matrix = np.zeros((len(variants_df), len(vocabulary)), dtype=bool)
    for row, sequence in enumerate(variants_df["activity_sequence"]):
        for activity in set(_activities(sequence)):
            matrix[row, index[activity]] = True

    return matrix, tuple(vocabulary), list(variants_df["variant_id"])


def run_structural_clustering(
    variants_df: pd.DataFrame, min_cluster_size: int = 5, min_samples: int | None = None
) -> StructuralClusteringResult:
    """Runs HDBSCAN over the boolean activity-vector representation. `min_cluster_size` is the
    one hyperparameter this baseline exposes — scikit-learn's own HDBSCAN default (5) is kept as
    this function's default too, per the same "uniform hyperparameters, no per-case tuning"
    discipline the project applies to Step 7's `discovery_noise_threshold`: this value is fixed
    once per dataset in the analysis driver, never chosen after inspecting the resulting clusters.
    """
    matrix, vocabulary, variant_ids = build_activity_vectors(variants_df)

    # Jaccard distance on boolean vectors: the natural metric for a presence/absence
    # representation (Euclidean/cosine would treat "both activities absent" as agreement, which
    # is not informative for a sparse activity vocabulary — most variants use a small subset of
    # the log's total activity set).
    clusterer = HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_samples, metric="jaccard")
    labels = clusterer.fit_predict(matrix)

    assignments: dict[str, str | None] = {}
    cluster_sizes: dict[str, int] = {}
    for variant_id, label in zip(variant_ids, labels):
        if label == -1:
            assignments[variant_id] = None
            continue
        cluster_id = f"cluster_{label}"
        assignments[variant_id] = cluster_id
        cluster_sizes[cluster_id] = cluster_sizes.get(cluster_id, 0) + 1

    n_noise = int(np.sum(labels == -1))
    return StructuralClusteringResult(
        assignments=assignments,
        cluster_sizes=cluster_sizes,
        n_clusters=len(cluster_sizes),
        n_noise=n_noise,
        min_cluster_size=min_cluster_size,
        activity_vocabulary=vocabulary,
    )


def summarize(result: StructuralClusteringResult) -> dict[str, Any]:
    """A JSON-serializable summary for a manifest/report — cluster count, sizes, residual, and
    the activity vocabulary size the vectors were built over (not the vectors themselves, which
    are large and reconstructible from `variants.csv` alone)."""
    total = len(result.assignments)
    return {
        "n_variants": total,
        "n_clusters": result.n_clusters,
        "n_noise": result.n_noise,
        "noise_pct": (result.n_noise / total * 100) if total else 0.0,
        "min_cluster_size": result.min_cluster_size,
        "activity_vocabulary_size": len(result.activity_vocabulary),
        "cluster_sizes": result.cluster_sizes,
    }

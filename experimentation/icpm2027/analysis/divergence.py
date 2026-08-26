"""Label-independent partition divergence — AMI/NMI (EXPERIMENTATION_PLAN.md §7, Task D1).

Task D1 requires the convention to be fixed *before* any number is computed, along two axes that
change the result:

  - **residual handling** — is the residual its own cluster, or excluded from the comparison?
  - **weighting** — is each variant one observation, or `frequency` observations?

This module computes **all four combinations** and marks the one `configs/preregistration.yaml`
names as primary, so the pre-registered choice is visible next to the three it was chosen over
rather than being the only number anyone ever sees. That is the whole point of fixing a convention
in advance: the alternatives stay auditable.

`AMI(P^G, P^O)` is a measure of *divergence between two partitions*. It is never accuracy — neither
partition is ground truth (§1), so a high value means the two arms agree, not that either is right.
`interpretation_caveat()` returns that sentence for embedding in generated reports, so no table can
be produced without it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import pandas as pd
from sklearn.metrics import adjusted_mutual_info_score, normalized_mutual_info_score

from .contingency import RESIDUAL_LABEL

ResidualHandling = Literal["own_cluster", "exclude"]
Weighting = Literal["variant", "case"]

CAVEAT = (
    "AMI/NMI measure divergence between two partitions, not classification accuracy: neither "
    "partition is ground truth, so agreement between the arms is not evidence that either is "
    "correct (EXPERIMENTATION_PLAN.md §1, §7)."
)


def interpretation_caveat() -> str:
    """The sentence §7 requires alongside any AMI/NMI figure."""
    return CAVEAT


@dataclass(frozen=True)
class DivergenceScore:
    residual_handling: ResidualHandling
    weighting: Weighting
    ami: float
    nmi: float
    n_observations: int
    is_primary: bool

    def as_dict(self) -> dict:
        return {
            "residual_handling": self.residual_handling,
            "weighting": self.weighting,
            "AMI": self.ami,
            "NMI": self.nmi,
            "n_observations": self.n_observations,
            "primary": self.is_primary,
        }


@dataclass(frozen=True)
class DivergenceResult:
    row_label: str
    col_label: str
    scores: tuple[DivergenceScore, ...]

    @property
    def primary(self) -> DivergenceScore:
        for score in self.scores:
            if score.is_primary:
                return score
        raise ValueError("No score marked primary — the D1 convention was not resolved")

    def to_frame(self) -> pd.DataFrame:
        return pd.DataFrame([s.as_dict() for s in self.scores])

    def to_markdown(self) -> str:
        header = f"**{self.row_label} vs. {self.col_label}** — partition divergence (Task D1)\n\n"
        return header + self.to_frame().to_markdown(index=False) + f"\n\n_{CAVEAT}_\n"


def _paired_labels(
    row_assignments: pd.DataFrame,
    col_assignments: pd.DataFrame,
    variants_df: pd.DataFrame,
    residual_handling: ResidualHandling,
    weighting: Weighting,
) -> tuple[list[str], list[str]]:
    """The two aligned label vectors one (residual_handling, weighting) combination scores.

    Only variants present in both partitions are compared, matching `contingency_matrix()`'s own
    rule: a variant outside one condition's population (Task C7 scoping) is excluded, never coded
    as a phantom category.
    """
    row_series = row_assignments.set_index("variant_id")["category_id"].fillna(RESIDUAL_LABEL)
    col_series = col_assignments.set_index("variant_id")["category_id"].fillna(RESIDUAL_LABEL)
    shared = row_series.index.intersection(col_series.index)

    row_series = row_series.loc[shared]
    col_series = col_series.loc[shared]

    if residual_handling == "exclude":
        keep = (row_series != RESIDUAL_LABEL) & (col_series != RESIDUAL_LABEL)
        row_series, col_series = row_series[keep], col_series[keep]

    if weighting == "variant":
        return list(row_series), list(col_series)

    # Case weighting: each variant contributes `frequency` identical observations, which is what
    # makes the score comparable to the contingency table's case-weighted half rather than to its
    # variant-count half.
    freq_by_variant = dict(zip(variants_df["variant_id"], variants_df["frequency"]))
    rows: list[str] = []
    cols: list[str] = []
    for variant_id, row_label, col_label in zip(row_series.index, row_series, col_series):
        repeats = int(freq_by_variant.get(variant_id, 0))
        rows.extend([row_label] * repeats)
        cols.extend([col_label] * repeats)
    return rows, cols


def compute_divergence(
    row_assignments: pd.DataFrame,
    col_assignments: pd.DataFrame,
    variants_df: pd.DataFrame,
    row_label: str,
    col_label: str,
    primary_residual_handling: ResidualHandling = "own_cluster",
    primary_weighting: Weighting = "variant",
) -> DivergenceResult:
    """All four (residual_handling, weighting) combinations, with the pre-registered one flagged.

    The defaults match `configs/preregistration.yaml`'s `D1_divergence_convention`; the driver
    passes the resolved decision explicitly rather than relying on them, so a change to the
    pre-registration cannot silently disagree with this module's defaults.
    """
    scores: list[DivergenceScore] = []
    for residual_handling in ("own_cluster", "exclude"):
        for weighting in ("variant", "case"):
            rows, cols = _paired_labels(
                row_assignments, col_assignments, variants_df, residual_handling, weighting
            )
            if len(rows) < 2 or len(set(rows)) < 2 or len(set(cols)) < 2:
                # Degenerate comparison (one label on either side): mutual information is
                # undefined in the sense that matters here, so report it as such rather than as 0.
                ami = nmi = float("nan")
            else:
                ami = float(adjusted_mutual_info_score(rows, cols))
                nmi = float(normalized_mutual_info_score(rows, cols))
            scores.append(
                DivergenceScore(
                    residual_handling=residual_handling,
                    weighting=weighting,
                    ami=ami,
                    nmi=nmi,
                    n_observations=len(rows),
                    is_primary=(
                        residual_handling == primary_residual_handling and weighting == primary_weighting
                    ),
                )
            )

    return DivergenceResult(row_label=row_label, col_label=col_label, scores=tuple(scores))

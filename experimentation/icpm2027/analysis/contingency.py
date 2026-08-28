"""Contingency matrices between two partitions of the same variant set — the guided-open
contingency matrix (variant counts and, where feasible, case-weighted counts).

Rows = the first partition's categories, columns = the second's, by the reporting convention: $G_1, G_2
\\to O_1$ reads as a merge, $G_1 \\to O_1, O_2$ reads as a split. The residual is always included
as its own row/column labeled `(residual)` — Task D1's convention, adopted here unconditionally
(not just for AMI/NMI): a variant the guided arm couldn't place is itself a fact about that arm's
partition, not missing data to drop before comparing.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

RESIDUAL_LABEL = "(residual)"


@dataclass(frozen=True)
class ContingencyResult:
    row_label: str
    col_label: str
    variant_counts: pd.DataFrame  # index=row categories, columns=col categories, values=variant counts
    case_counts: pd.DataFrame  # same shape, case-weighted

    def splits_of(self, row_category: str) -> dict[str, int]:
        """Which column categories a given row category's variants ended up spread across —
        `{row_category} -> col_a, col_b` reads as a split if len(...) > 1."""
        row = self.variant_counts.loc[row_category]
        return {col: int(count) for col, count in row.items() if count > 0}

    def merges_into(self, col_category: str) -> dict[str, int]:
        """The reverse view: which row categories contributed to one column category —
        `row_a, row_b -> {col_category}` reads as a merge if len(...) > 1."""
        col = self.variant_counts[col_category]
        return {row: int(count) for row, count in col.items() if count > 0}

    def to_markdown(self, counts: str = "variant") -> str:
        table = self.variant_counts if counts == "variant" else self.case_counts
        return table.to_markdown()


def _with_residual(assignments_df: pd.DataFrame) -> pd.Series:
    """`category_id`, with NaN/None replaced by the shared residual label — a plain merge key,
    not a real category, so it is never treated as one anywhere else (coverage.py, freeze.py)."""
    return assignments_df.set_index("variant_id")["category_id"].fillna(RESIDUAL_LABEL)


def contingency_matrix(
    row_assignments: pd.DataFrame,
    col_assignments: pd.DataFrame,
    variants_df: pd.DataFrame,
    row_label: str,
    col_label: str,
) -> ContingencyResult:
    """Builds both the variant-count and case-weighted contingency tables between two partitions
    of the same variant set. `row_assignments`/`col_assignments`: variant_id, category_id — any
    two conditions' assignments.csv-shaped frames (guided vs. open, guided vs. structural
    baseline, ...). Only variants present in *both* inputs are compared — a Task C7 out-of-scope
    variant present in neither, or a variant unique to one condition's population, is excluded
    rather than silently coded as a phantom category.
    """
    row_series = _with_residual(row_assignments)
    col_series = _with_residual(col_assignments)
    shared_variants = row_series.index.intersection(col_series.index)

    freq_by_variant = dict(zip(variants_df["variant_id"], variants_df["frequency"]))
    frame = pd.DataFrame(
        {
            "row_category": row_series.loc[shared_variants],
            "col_category": col_series.loc[shared_variants],
            "frequency": [freq_by_variant.get(vid, 0) for vid in shared_variants],
        }
    )

    variant_counts = pd.crosstab(frame["row_category"], frame["col_category"])
    case_counts = pd.crosstab(frame["row_category"], frame["col_category"], values=frame["frequency"], aggfunc="sum").fillna(0).astype(int)

    return ContingencyResult(row_label=row_label, col_label=col_label, variant_counts=variant_counts, case_counts=case_counts)


def declared_distinction_changes(result: ContingencyResult) -> dict[str, list[str]]:
    """Explicit identification of merges and splits (§3's required evidence item 5), read off the
    contingency table: a row category is 'split' if its variants land in more than one column
    category; a column category is a 'merge target' if variants from more than one row category
    land in it. Returns {"splits": [...], "merges": [...]} as human-readable strings."""
    splits = []
    for row_category in result.variant_counts.index:
        targets = result.splits_of(row_category)
        if len(targets) > 1 and row_category != RESIDUAL_LABEL:
            targets_str = ", ".join(f"{col} ({count})" for col, count in sorted(targets.items(), key=lambda kv: -kv[1]))
            splits.append(f"{row_category} -> {targets_str}")

    merges = []
    for col_category in result.variant_counts.columns:
        sources = result.merges_into(col_category)
        if len(sources) > 1 and col_category != RESIDUAL_LABEL:
            sources_str = ", ".join(f"{row} ({count})" for row, count in sorted(sources.items(), key=lambda kv: -kv[1]))
            merges.append(f"{sources_str} -> {col_category}")

    return {"splits": splits, "merges": merges}

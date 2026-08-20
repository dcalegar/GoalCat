"""Coverage/residual (EXPERIMENTATION_PLAN.md §3, §7's metrics reference).

Macro (variant-level) coverage $C_V$ = assigned variants / total variants; micro (case-weighted)
coverage $C_C$ = case-weighted assigned / total cases. Both are always reported together per §7's
own caveat: "a few residual variants can carry a large case share, or vice versa." Task D2's
caveat — a larger taxonomy or a broad catch-all category can trivially raise coverage — is
structural to this module too: nothing here ranks conditions by coverage, only reports it.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class CoverageReport:
    condition_label: str
    total_variants: int
    total_cases: int
    assigned_variants: int
    assigned_cases: int
    residual_variant_ids: tuple[str, ...]

    @property
    def macro_coverage(self) -> float:
        """$C_V$ — assigned variants / total variants."""
        return self.assigned_variants / self.total_variants if self.total_variants else 0.0

    @property
    def micro_coverage(self) -> float:
        """$C_C$ — case-weighted assigned / total cases."""
        return self.assigned_cases / self.total_cases if self.total_cases else 0.0

    @property
    def residual_variant_count(self) -> int:
        return len(self.residual_variant_ids)

    @property
    def residual_case_count(self) -> int:
        return self.total_cases - self.assigned_cases

    def as_dict(self) -> dict:
        return {
            "condition": self.condition_label,
            "total_variants": self.total_variants,
            "total_cases": self.total_cases,
            "assigned_variants": self.assigned_variants,
            "assigned_cases": self.assigned_cases,
            "macro_coverage_C_V": self.macro_coverage,
            "micro_coverage_C_C": self.micro_coverage,
            "residual_variants": self.residual_variant_count,
            "residual_variants_pct": (self.residual_variant_count / self.total_variants * 100)
            if self.total_variants
            else 0.0,
            "residual_cases": self.residual_case_count,
            "residual_cases_pct": (self.residual_case_count / self.total_cases * 100) if self.total_cases else 0.0,
        }


def compute_coverage(
    assignments_df: pd.DataFrame, variants_df: pd.DataFrame, condition_label: str
) -> CoverageReport:
    """`assignments_df`: variant_id, category_id (NaN/None = residual). `variants_df`: variant_id,
    frequency (case count) — used for the case-weighted (micro) figure. A variant present in
    `variants_df` but absent from `assignments_df` (e.g. Task C7's BPIC 2019 out-of-scope variants)
    is *not* silently counted as residual — it is out of this condition's population entirely, and
    Task C7's own `variant_scope` record is what documents that population's size.
    """
    freq_by_variant = dict(zip(variants_df["variant_id"], variants_df["frequency"]))
    in_scope = assignments_df[assignments_df["variant_id"].isin(freq_by_variant)]

    total_variants = len(in_scope)
    total_cases = sum(freq_by_variant[vid] for vid in in_scope["variant_id"])

    assigned = in_scope[in_scope["category_id"].notna()]
    residual = in_scope[in_scope["category_id"].isna()]

    return CoverageReport(
        condition_label=condition_label,
        total_variants=total_variants,
        total_cases=total_cases,
        assigned_variants=len(assigned),
        assigned_cases=sum(freq_by_variant[vid] for vid in assigned["variant_id"]),
        residual_variant_ids=tuple(residual["variant_id"]),
    )


def coverage_table(reports: list[CoverageReport]) -> pd.DataFrame:
    """One row per condition — the table §3 asks each dataset to report (|T|, coverage, residual
    per condition, side by side)."""
    return pd.DataFrame([r.as_dict() for r in reports])

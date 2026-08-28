"""Assembles one dataset's Experiment 1 evidence into a single Markdown report
(the "Evidence reported per dataset" set).

Three of those required items are computed nowhere else and live here:

  - **Scope framing (Task C7).** Every coverage and residual figure is reported against the scoped
    population *and* against the whole log. `configs/preregistration.yaml`'s C7 rationale promises
    exactly this: whatever variant scope is chosen, the share of the full log's cases it covers is
    stated, so a truncated population cannot be mistaken for the log.
  - **Declared-alternative coverage (guided arm).** How many of the goal model's declared
    alternatives received a category at all, and how many of those received a non-empty variant
    set. A declared alternative that Step 5a drops, or that Step 6 leaves empty, is direct RQ1
    evidence and is invisible in $C_V$/$C_C$ — BPIC 2019's `two_way_matched` (13 variants against
    another category's 6,096) is the motivating case.
  - **Step 5a induction stability (Task C12).** Whether the k reruns reproduced the category and
    anchor sets. A dataset that fails this has its figures reported per Task E7 — as one draw from
    a demonstrably unstable process — and this module emits that qualification into the report
    itself rather than leaving it to the writer to remember.

Nothing here ranks conditions. Task D2's caveat (a larger taxonomy or a broad catch-all category
trivially raises coverage) is reproduced in the generated output, and no "better"/"worse" verdict
is computed anywhere in this package.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pandas as pd

from goalcat.grl import declared_alternatives, read_jucm

from .contingency import ContingencyResult, declared_distinction_changes
from .coverage import CoverageReport, coverage_table
from .divergence import DivergenceResult, interpretation_caveat

COVERAGE_CAVEAT = (
    "Higher coverage is not better categorization: a larger taxonomy or a broad catch-all "
    "category can trivially raise $C_V$/$C_C$ while carrying less semantic information "
    "(Task D2)."
)


@dataclass(frozen=True)
class DeclaredAlternativeCoverage:
    """One row per declared OR-alternative in the goal model (guided arm only — open-mode
    categories carry no `anchor_ids` to trace back to a declaration).

    An OR-alternative is not always a leaf. RTFM declares `Contested appeal is resolved` as an
    alternative at one level and decomposes it into the administrative/judicial appeals at the
    next, and Step 5a anchors its categories at the leaves. Such an intermediate alternative is
    realized *through its descendants*, so counting it as "unrealized" because no category names it
    directly would be an artifact of where the taxonomy chose to anchor, not a finding. `covered_by`
    records which anchors actually carry it, and `variant_count`/`case_count` aggregate over them.
    """

    anchor_id: str
    name: str
    category_id: str | None
    variant_count: int
    case_count: int
    is_decomposed: bool = False
    covered_by: tuple[str, ...] = ()

    @property
    def has_category(self) -> bool:
        """Directly named by a category's `anchor_ids`, or realized through a descendant."""
        return self.category_id is not None or bool(self.covered_by)

    @property
    def is_empty(self) -> bool:
        return self.has_category and self.variant_count == 0

    @property
    def status(self) -> str:
        if not self.has_category:
            return "unrealized"
        if self.is_empty:
            return "empty"
        if self.category_id is None:
            return "realized via descendants"
        return "realized"

    def as_dict(self) -> dict:
        return {
            "anchor_id": self.anchor_id,
            "declared_alternative": self.name,
            "category_id": self.category_id
            or (f"via {', '.join(self.covered_by)}" if self.covered_by else "(no category induced)"),
            "variants": self.variant_count,
            "cases": self.case_count,
            "status": self.status,
        }


@dataclass(frozen=True)
class InductionStability:
    """Task C12's result for one dataset: did k identical-input Step 5a reruns reproduce the
    taxonomy? `category_sets`/`anchor_sets` hold one frozenset per rerun."""

    k: int
    category_sets: tuple[frozenset[str], ...]
    anchor_sets: tuple[frozenset[str], ...]

    @property
    def categories_stable(self) -> bool:
        return len(set(self.category_sets)) <= 1

    @property
    def anchors_stable(self) -> bool:
        return len(set(self.anchor_sets)) <= 1

    @property
    def is_stable(self) -> bool:
        return self.categories_stable and self.anchors_stable

    @property
    def distinct_shapes(self) -> int:
        return len(set(self.anchor_sets))

    def qualification(self, dataset_id: str) -> str:
        """The sentence Task E7 requires whenever a dataset's induction is unstable."""
        if self.is_stable:
            return (
                f"Step 5a reproduced the same category and anchor set across all {self.k} "
                f"identical-input reruns; {dataset_id}'s figures below are not subject to Task E7's "
                "qualification."
            )
        return (
            f"**Task E7 qualification.** Step 5a did NOT reproduce a stable taxonomy on "
            f"{dataset_id}: {self.k} identical-input reruns produced {self.distinct_shapes} "
            "distinct anchor sets. Every category count, coverage figure, and residual below is "
            "one draw from a demonstrably unstable process, not a fixed property of the method, "
            "and must not be reported without this statement."
        )


def declared_alternative_coverage(
    goal_model_path: Path,
    taxonomy_path: Path,
    assignments_df: pd.DataFrame,
    variants_df: pd.DataFrame,
) -> list[DeclaredAlternativeCoverage]:
    """Joins the goal model's declared OR-alternatives to the induced taxonomy and the resulting
    assignment, so an alternative that never became a category — or became an empty one — is
    visible as its own row rather than as an absence."""
    model = read_jucm(goal_model_path)
    names = {element_id: element.name for element_id, element in model.elements.items()}
    alternatives: list[str] = []
    for children in declared_alternatives(model).values():
        for child in children:
            if child not in alternatives:
                alternatives.append(child)

    taxonomy = json.loads(taxonomy_path.read_text(encoding="utf-8"))
    category_by_anchor: dict[str, str] = {}
    for category in taxonomy.get("categories", []):
        for anchor in category.get("anchor_ids") or []:
            category_by_anchor.setdefault(anchor, category["category_id"])

    children: dict[str, list[str]] = {}
    for link in model.decompositions:
        children.setdefault(link.src, []).append(link.dest)

    def descendants(element_id: str) -> list[str]:
        """Every element below `element_id`, over decomposition links of any type — an OR
        alternative may be reached through an intervening AND node, as RTFM's `5 -> 6 -> 7` chain
        is."""
        seen: list[str] = []
        stack = list(children.get(element_id, []))
        while stack:
            current = stack.pop()
            if current in seen:
                continue
            seen.append(current)
            stack.extend(children.get(current, []))
        return seen

    freq_by_variant = dict(zip(variants_df["variant_id"], variants_df["frequency"]))
    variants_by_category = assignments_df.groupby("category_id")["variant_id"].apply(list).to_dict()

    rows: list[DeclaredAlternativeCoverage] = []
    for anchor_id in alternatives:
        category_id = category_by_anchor.get(anchor_id)
        covering_anchors: list[str] = []
        if category_id is not None:
            categories = [category_id]
        else:
            # Realized through descendants, if any of them carry a category.
            categories = []
            for descendant in descendants(anchor_id):
                descendant_category = category_by_anchor.get(descendant)
                if descendant_category is not None and descendant_category not in categories:
                    categories.append(descendant_category)
                    covering_anchors.append(descendant)

        assigned = [vid for category in categories for vid in variants_by_category.get(category, [])]
        rows.append(
            DeclaredAlternativeCoverage(
                anchor_id=anchor_id,
                name=names.get(anchor_id, "(unnamed)"),
                category_id=category_id,
                variant_count=len(assigned),
                case_count=sum(int(freq_by_variant.get(vid, 0)) for vid in assigned),
                is_decomposed=bool(children.get(anchor_id)),
                covered_by=tuple(covering_anchors),
            )
        )
    return rows


@dataclass
class DatasetReport:
    """Everything §3 asks to be reported for one dataset. Optional pieces stay `None` when the
    corresponding condition has not been run, so a partial report is honest about what is missing
    rather than silently omitting a required item."""

    dataset_id: str
    scope_record: dict[str, Any]
    coverage_reports: list[CoverageReport] = field(default_factory=list)
    contingency: ContingencyResult | None = None
    divergence: DivergenceResult | None = None
    declared_coverage: list[DeclaredAlternativeCoverage] = field(default_factory=list)
    stability: InductionStability | None = None
    structural_contingency: ContingencyResult | None = None

    def _scope_section(self) -> str:
        record = self.scope_record
        policy = record.get("applied_policy", "all")
        lines = [
            "## Variant scope (Task C7)",
            "",
            f"- Policy: `{policy}`",
            f"- Variants: {record.get('variants_kept')} of {record.get('variants_total')} extracted",
            f"- Cases: {record.get('cases_kept')} of {record.get('cases_total')}",
            f"- **Share of the full log's cases covered by this scope: "
            f"{record.get('case_coverage_of_full_log', 0.0) * 100:.1f}%**",
        ]
        if policy != "all":
            lines += [
                "",
                "Every coverage and residual figure below is computed over the scoped population. "
                "Read them against the case share above, not against the whole log.",
            ]
        return "\n".join(lines)

    def _missing(self) -> list[str]:
        missing = []
        if not self.coverage_reports:
            missing.append("coverage (§3 evidence items 2-3)")
        if self.contingency is None:
            missing.append("guided-open contingency matrix (§3 evidence items 4-5)")
        if not self.declared_coverage:
            missing.append("declared-alternative coverage (§3, guided arm)")
        if self.stability is None:
            missing.append("Step 5a induction stability (Task C12)")
        if self.structural_contingency is None:
            missing.append("guided-vs-structural-baseline contingency (Task C3)")
        return missing

    def to_markdown(self) -> str:
        parts = [f"# Experiment 1 — {self.dataset_id}", "", self._scope_section(), ""]

        if self.stability is not None:
            parts += ["## Step 5a induction stability (Task C12)", "", self.stability.qualification(self.dataset_id), ""]

        if self.coverage_reports:
            parts += [
                "## Coverage and residual",
                "",
                coverage_table(self.coverage_reports).to_markdown(index=False),
                "",
                f"_{COVERAGE_CAVEAT}_",
                "",
            ]

        if self.declared_coverage:
            frame = pd.DataFrame([row.as_dict() for row in self.declared_coverage])
            unrealized = [r for r in self.declared_coverage if not r.has_category]
            empty = [r for r in self.declared_coverage if r.is_empty]
            parts += ["## Declared-alternative coverage (guided arm)", "", frame.to_markdown(index=False), ""]
            direct = [r for r in self.declared_coverage if r.category_id is not None]
            parts.append(
                f"{len(self.declared_coverage) - len(unrealized)} of {len(self.declared_coverage)} "
                f"declared alternatives are realized ({len(direct)} named directly by a category, "
                f"the rest through their descendants); {len(empty)} are realized but carry no "
                "variants."
            )
            if unrealized:
                names = ", ".join(f"{r.anchor_id} ({r.name})" for r in unrealized)
                parts.append(f"**Unrealized declared alternatives:** {names}.")
            parts.append("")

        if self.contingency is not None:
            changes = declared_distinction_changes(self.contingency)
            parts += [
                f"## Contingency — {self.contingency.row_label} vs. {self.contingency.col_label}",
                "",
                "### Variant counts",
                "",
                self.contingency.to_markdown("variant"),
                "",
                "### Case-weighted counts",
                "",
                self.contingency.to_markdown("case"),
                "",
                "### Merges and splits (§3 evidence item 5)",
                "",
            ]
            parts += [f"- Split: {s}" for s in changes["splits"]] or ["- No splits identified."]
            parts += [f"- Merge: {m}" for m in changes["merges"]] or ["- No merges identified."]
            parts.append("")

        if self.structural_contingency is not None:
            parts += [
                f"## Secondary — {self.structural_contingency.row_label} vs. "
                f"{self.structural_contingency.col_label} (Task C3)",
                "",
                self.structural_contingency.to_markdown("variant"),
                "",
            ]

        if self.divergence is not None:
            parts += ["## Partition divergence (optional, Task D1)", "", self.divergence.to_markdown(), ""]
        else:
            parts += ["## Partition divergence (optional, Task D1)", "", "Not computed.", "", f"_{interpretation_caveat()}_", ""]

        missing = self._missing()
        if missing:
            parts += ["## Not yet available", ""] + [f"- {item}" for item in missing] + [""]

        return "\n".join(parts)

    def write(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.to_markdown(), encoding="utf-8")
        return path

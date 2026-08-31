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
    taxonomy? `category_sets`/`anchor_sets` hold one frozenset per rerun.

    An `anchor_sets` entry is the run's *category->anchors grouping* — one sorted tuple of anchor
    ids per category — not the flat union of every anchor the run used. The union cannot
    distinguish two categories anchored to one alternative each from a single category that
    swallowed both, so it would have scored a run that collapsed the axis as stable.
    """

    k: int
    category_sets: tuple[frozenset[str], ...]
    anchor_sets: tuple[frozenset[tuple[str, ...]], ...]

    @property
    def categories_stable(self) -> bool:
        """Diagnostic only — literal `category_id` string agreement. Step 5a's induced ids are
        LLM-generated slugs (e.g. `administrative_appeal` vs. `administrative_appeal_prefecture`)
        that can reword between identical-input reruns with no change in meaning. Per §4's own
        matching rule ("categories are matched across runs by anchor_ids, never by category name
        or id"), this must never gate `is_stable` — only `anchors_stable` does."""
        return len(set(self.category_sets)) <= 1

    @property
    def anchors_stable(self) -> bool:
        """Every rerun produced the same set of categories-with-their-anchors."""
        return len(set(self.anchor_sets)) <= 1

    @property
    def is_stable(self) -> bool:
        """Task C12's stability verdict — `anchor_ids` reproduction alone, per §4's anchor-based
        matching rule. Label rewording across reruns (`categories_stable` false while this is
        true) is expected LLM phrasing variance, not induction instability, and must not trip
        Task E7's qualification or the §4 gate on Experiment 2."""
        return self.anchors_stable

    @property
    def distinct_shapes(self) -> int:
        return len(set(self.anchor_sets))

    def qualification(self, dataset_id: str) -> str:
        """The sentence Task E7 requires whenever a dataset's induction is unstable."""
        if self.is_stable and self.categories_stable:
            return (
                f"Step 5a reproduced the same category and anchor set across all {self.k} "
                f"identical-input reruns; {dataset_id}'s figures below are not subject to Task E7's "
                "qualification."
            )
        if self.is_stable:
            return (
                f"Step 5a reproduced the same anchor set across all {self.k} identical-input "
                f"reruns for {dataset_id}; category *labels* reworded cosmetically between some "
                "reruns (e.g. added qualifiers with no change in the anchored goal-model element), "
                "which is expected LLM phrasing variance, not induction instability (§4: categories "
                "are matched by anchor_ids, never by name). This dataset's figures below are not "
                "subject to Task E7's qualification."
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


KNOWN_FINDINGS: dict[str, list[str]] = {
    "rtfm": [
        (
            "**Open-mode replicate coverage swing traced to one ambiguous variant (2026-08-29).** "
            "`e1_open_rep1` and `e1_open_rep2` show identical variant-level coverage (229/231, 2 "
            "residual variants each) but a ~13.8-point gap in case-weighted coverage (99.995% vs. "
            "86.2%). Root cause: variant V0003 (`Create Fine → Send Fine`, no further activity — an "
            "unresolved/still-open case) carries 20,385 cases (~13.6% of the whole log). Open-mode "
            "Step 6 classified it inconsistently across replicates — folded into the catch-all-like "
            "`standard_fine_lifecycle`/`standard_collection_or_payment` category in one replicate, "
            "left residual in the other — because open induction has no external criterion for "
            "\"does not realize any category.\" **Guided mode classified the same variant as "
            "residual in both replicates**, with near-identical rationale each time (\"does not "
            "resolve the case\" / \"remaining in the residual\"): the goal model gives the LLM a "
            "stable boundary for what counts as resolved vs. residual that open induction lacks. "
            "This is a concrete, high-leverage illustration of exactly what Task C2's replicate "
            "design exists to catch — LLM-sampling noise can concentrate disproportionately in a "
            "single high-frequency variant, and case-weighted coverage is far more sensitive to it "
            "than variant-level coverage. Positive evidence for RQ1: the external semantic frame "
            "stabilizes the residual boundary, not only the category set."
        ),
    ],
}


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
    #: Task C2 replicate noise floor — rep1 vs rep2 of each arm, same convention as `divergence`.
    #: The open arm's is the only stability signal it has (Task C12 covers the guided taxonomy only).
    guided_replicate_divergence: DivergenceResult | None = None
    open_replicate_divergence: DivergenceResult | None = None
    declared_coverage: list[DeclaredAlternativeCoverage] = field(default_factory=list)
    stability: InductionStability | None = None
    structural_contingency: ContingencyResult | None = None
    #: Task C4 — RTFM-only deterministic activity-rule baseline vs. the guided partition.
    rule_contingency: ContingencyResult | None = None
    #: Task C13 — RTFM-only Step 7b indicator-satisfaction report (the markdown Step 7b already
    #: writes), embedded so the one LLM-independent result is visible in the dataset report.
    step7b_report: str | None = None
    notes: list[str] = field(default_factory=list)
    """Curated qualitative findings for this dataset (Markdown, one entry per finding), rendered
    verbatim under '## Notable findings'. Populated from `KNOWN_FINDINGS` below — hand-investigated
    observations that the automated tables don't surface on their own (e.g. a replicate-to-replicate
    coverage swing traced to one ambiguous high-frequency variant), kept here rather than hand-edited
    into the generated .md so they survive the next `write()` instead of being silently overwritten."""

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

        if self.rule_contingency is not None:
            changes = declared_distinction_changes(self.rule_contingency)
            parts += [
                f"## Secondary — {self.rule_contingency.row_label} vs. "
                f"{self.rule_contingency.col_label} (Task C4)",
                "",
                "A deterministic activity-rule classifier (no LLM, no fit — "
                "`baselines/rule_based_rtfm.py`). Close agreement here means the guided arm's five "
                "declared alternatives are recoverable from a handful of hand-written rules on this "
                "log, which the paper must report as a bound on the guided arm's added value here.",
                "",
                self.rule_contingency.to_markdown("variant"),
                "",
                self.rule_contingency.to_markdown("case"),
                "",
            ]
            parts += [f"- Split: {s}" for s in changes["splits"]] or ["- No splits identified."]
            parts += [f"- Merge: {m}" for m in changes["merges"]] or ["- No merges identified."]
            parts.append("")

        if self.step7b_report is not None:
            body = self.step7b_report.split("\n", 1)[1] if self.step7b_report.startswith("# ") else self.step7b_report
            parts += [
                "## Indicator satisfaction (Task C13)",
                "",
                "Guided arm only. Each goal-model indicator is *measured* from the log and converted "
                "through its own `KPIEvalValueSet`, then propagated up the goal model --- no LLM call. "
                "This is the one result not exposed to the LLM-dependence threat. Indicators with low "
                "applicability are reported as coverage, never as bad values.",
                "",
                body.strip(),
                "",
            ]

        if self.structural_contingency is not None:
            parts += [
                f"## Secondary — {self.structural_contingency.row_label} vs. "
                f"{self.structural_contingency.col_label} (Task C3)",
                "",
                self.structural_contingency.to_markdown("variant"),
                "",
            ]

        if self.notes:
            parts += ["## Notable findings", ""]
            parts += [f"- {note}" for note in self.notes]
            parts.append("")

        if self.guided_replicate_divergence is not None or self.open_replicate_divergence is not None:
            parts += [
                "## Replicate stability (Task C2)",
                "",
                "rep1 vs. rep2 of each arm, same convention as the paired contrast below. Read the "
                "\"guided vs. open\" divergence against these: a cross-arm difference no larger than "
                "an arm's own rep1-rep2 movement is not separable from run-to-run variance. The open "
                "arm has no anchors, so this is its only stability check — Task C12 tests the guided "
                "taxonomy alone.",
                "",
            ]
            if self.guided_replicate_divergence is not None:
                parts += ["### guided rep1 vs. rep2", "", self.guided_replicate_divergence.to_markdown(), ""]
            if self.open_replicate_divergence is not None:
                parts += ["### open rep1 vs. rep2", "", self.open_replicate_divergence.to_markdown(), ""]
            if self.open_replicate_divergence is not None and self.guided_replicate_divergence is not None:
                parts += [
                    "_Read on the D1-primary `own_cluster` convention. Where the open arm's rep1-rep2 "
                    "AMI is lower than the guided arm's, every \"guided vs. open\" figure for this "
                    "dataset should be reported with that band, and the open arm's instability noted "
                    "as a limit on the strength of the paired contrast (Task E7, extended to the open "
                    "arm)._",
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

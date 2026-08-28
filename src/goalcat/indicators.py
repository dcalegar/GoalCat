"""Step 7b: measured goal satisfaction per category, via the goal model's own KPI indicators.

Steps 7 and 8 characterize a discovered category by how well a *process model* fits it (fitness,
precision) and by an LLM's prose judgment of goal alignment. Neither is a statement about whether
the category achieved anything the goal model actually wants. This step is: it measures each
indicator over each category's sublog, converts the measurement to a GRL satisfaction level through
the indicator's own `KPIEvalValueSet`, and propagates that level up the same decomposition and
contribution graph Step 5a used as the taxonomy axis. The goal model is thus used twice — forward
as the axis, backward as the evaluation frame — and the resulting number is the only
goal-satisfaction signal in the pipeline that no language model produces.

**What this measure is, and is not.** It *characterizes* the discovered partition; it does not
validate it. A category defined as "judicial appeal" mechanically shows long closure times, so a
satisfaction difference across categories restates the partition rather than testing it — the same
trap partition granularity already sets for fitness and precision. Nor can it enter a guided-vs-open
comparison: open-mode categories carry no `anchor_ids` and no goal model, so there is nothing to
propagate through. Report it as a descriptive enrichment of the guided arm.

**Three rules that keep the numbers honest**, all enforced here rather than left to the reader:

1. The raw measured value travels beside every satisfaction score, always. A score computed against
   an invented threshold looks exactly like one computed against a statute.
2. Every row carries the provenance of the value set it was scored against
   (`goalcat.grl.measures.PROVENANCE_CLASSES`) and a `one_sided` flag when `target == threshold`
   collapsed half the scale.
3. Cases that could not be measured are counted and classified, never silently folded into an
   aggregate — `coverage` states what share of in-scope cases the aggregate actually rests on.

**Cost.** Deterministic, no LLM, and no alignment computation: measurement points are located by
activity label in a sublog Step 7 already built, which is why this runs in seconds on the full RTFM
log while Step 7's precision replay dominates that step's runtime. Locating measurement points by
model position instead — through alignments, which would distinguish "the anchor activity never
occurred" from "it occurred late" for deviating traces — is deliberately out of scope here; the
`no_start`/`no_end` counts are what make that limitation visible.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path

import pandas as pd

from .atomic_io import atomic_write_csv, atomic_write_text
from .config import PipelineConfig
from .discovery import build_category_sublogs
from .grl.evaluation import indicator_evaluation, is_one_sided, propagate
from .grl.measures import MeasureOutcome, measure_specs, measure_sublog
from .grl.model import GRLModel
from .llm.taxonomy import Taxonomy

#: Scope id for the whole log, measured alongside the categories so every per-category number has a
#: baseline to be read against. Not a valid `Category.category_id` (which must match
#: `^[a-z][a-z0-9_]*$`), so it can never collide with one.
BASELINE_SCOPE = "__baseline__"


def compute_indicator_satisfaction(
    df: pd.DataFrame,
    variants_df: pd.DataFrame,
    assignments_df: pd.DataFrame,
    taxonomy: Taxonomy,
    model: GRLModel,
    config: PipelineConfig,
    logger: logging.Logger,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Measures, converts, and propagates for every category plus the whole-log baseline.

    Returns `(indicator_df, goal_df)`: one row per (scope, indicator) with the measurement and its
    conversion, and one row per (scope, intentional element) with the propagated satisfaction.
    Both are empty (with their columns declared) when the goal model carries no measurable
    indicator — i.e. no `Indicator` carries a `goalcat:*` measurement binding.
    """
    specs = measure_specs(model)
    if not specs:
        logger.warning(
            "Goal model %s declares no measurable indicator (no goalcat:* metadata binding) — "
            "Step 7b has nothing to compute.", model.source_path,
        )
        return _empty_indicator_df(), _empty_goal_df()

    sublogs: dict[str, pd.DataFrame] = {BASELINE_SCOPE: df}
    sublogs.update(build_category_sublogs(df, variants_df, assignments_df, config))
    category_names = {c.category_id: c.name for c in taxonomy.categories}

    indicator_rows: list[dict] = []
    goal_rows: list[dict] = []
    for scope, sub_df in sublogs.items():
        seeds: dict[str, int] = {}
        for indicator_id, spec in specs.items():
            outcome = measure_sublog(spec, sub_df, config)
            eval_point = model.indicators[indicator_id].eval_point
            satisfaction = None
            if outcome.value is not None and eval_point is not None:
                satisfaction = indicator_evaluation(outcome.value, eval_point)
                seeds[indicator_id] = satisfaction
            indicator_rows.append(_indicator_row(scope, category_names, outcome, eval_point, satisfaction))

        result = propagate(model, seeds)
        for element_id, element in model.elements.items():
            goal_rows.append(
                {
                    "scope": scope,
                    "scope_kind": "baseline" if scope == BASELINE_SCOPE else "category",
                    "category_name": category_names.get(scope, ""),
                    "element_id": element_id,
                    "element_type": element.type,
                    "element_name": element.name,
                    "satisfaction": result.evaluations[element_id],
                    "is_measured_seed": element_id in result.seeds,
                }
            )
        logger.info(
            "Step 7b: scope %s — %d/%d indicators measured, %d cases",
            scope, len(seeds), len(specs), sub_df[config.case_id_key].nunique() if not sub_df.empty else 0,
        )

    return pd.DataFrame(indicator_rows), pd.DataFrame(goal_rows)


def _indicator_row(scope, category_names, outcome: MeasureOutcome, eval_point, satisfaction) -> dict:
    spec = outcome.spec
    return {
        "scope": scope,
        "scope_kind": "baseline" if scope == BASELINE_SCOPE else "category",
        "category_name": category_names.get(scope, ""),
        "indicator_id": spec.indicator_id,
        "indicator_name": spec.indicator_name,
        "unit": eval_point.unit if eval_point else None,
        "measured_value": outcome.value,
        "satisfaction": satisfaction,
        "target": eval_point.target if eval_point else None,
        "threshold": eval_point.threshold if eval_point else None,
        "worst": eval_point.worst if eval_point else None,
        "one_sided": is_one_sided(eval_point) if eval_point else None,
        "provenance": spec.provenance,
        "n_cases": outcome.n_cases,
        "n_measured": outcome.n_measured,
        "n_not_applicable": outcome.n_not_applicable,
        "n_no_start": outcome.n_no_start,
        "n_no_end": outcome.n_no_end,
        "coverage": round(outcome.coverage, 4),
        "source": spec.source,
    }


def _empty_indicator_df() -> pd.DataFrame:
    return pd.DataFrame(
        columns=[
            "scope", "scope_kind", "category_name", "indicator_id", "indicator_name", "unit",
            "measured_value", "satisfaction", "target", "threshold", "worst", "one_sided",
            "provenance", "n_cases", "n_measured", "n_not_applicable", "n_no_start", "n_no_end",
            "coverage", "source",
        ]
    )


def _empty_goal_df() -> pd.DataFrame:
    return pd.DataFrame(
        columns=["scope", "scope_kind", "category_name", "element_id", "element_type",
                 "element_name", "satisfaction", "is_measured_seed"]
    )


# ------------------------------------------------------------------------------------------
# Write-back: one EvaluationStrategy per scope, into a copy of the goal model
# ------------------------------------------------------------------------------------------


def write_measured_jucm(
    source_path: Path, indicator_df: pd.DataFrame, goal_df: pd.DataFrame, destination: Path, run_label: str
) -> Path:
    """Writes a copy of the goal model carrying one `EvaluationStrategy` per scope, so an analyst
    opens it in jUCMNav and reads the colored models side by side, one per discovered category.

    Injected textually into the source file rather than regenerated through `grl.write_jucm()`:
    that path rebuilds the `urndef` diagram layer from a generic grid layout, which would discard
    these goal models' hand-placed coordinates for content this step does not change. Everything
    outside the inserted `<groups>`/`<strategies>` block is byte-identical to the source.

    Each strategy stores both halves of what jUCMNav needs to agree with the numbers in
    `indicator_satisfaction.csv`: `Evaluation.evaluation`, the satisfaction level, on every
    element; and `KPIEvalValueSet.evaluationValue`, the measured real-world value, on every
    measured indicator, so jUCMNav's own `calculateIndicatorEvalLevel()` re-derives the same
    conversion from the same input rather than trusting a number it cannot check.
    """
    from xml.sax.saxutils import quoteattr as q

    text = source_path.read_text(encoding="utf-8")
    next_id = int(re.search(r'nextGlobalID="(\d+)"', text).group(1))

    scopes = list(dict.fromkeys(goal_df["scope"].tolist()))
    group_id, next_id = str(next_id), next_id + 1
    strategy_ids = {}
    for scope in scopes:
        strategy_ids[scope], next_id = str(next_id), next_id + 1

    group_name = "GoalCat measured ({})".format(run_label)
    blocks = [f'    <groups name={q(group_name)} id={q(group_id)} '
              f'strategies={q(" ".join(strategy_ids[s] for s in scopes))}/>']
    for scope in scopes:
        scope_goals = goal_df[goal_df["scope"] == scope]
        scope_indicators = indicator_df[indicator_df["scope"] == scope].set_index("indicator_id")
        label = "whole log (baseline)" if scope == BASELINE_SCOPE else scope
        lines = [
            f'    <strategies name={q("measured: " + label)} id={q(strategy_ids[scope])} '
            f'author={q("goalcat Step 7b (" + run_label + ")")} type="Private" group={q(group_id)}>'
        ]
        for row in scope_goals.itertuples():
            measured = scope_indicators.loc[row.element_id] if row.element_id in scope_indicators.index else None
            if measured is None or pd.isna(measured["measured_value"]):
                lines.append(f'      <evaluations intElement={q(row.element_id)} '
                             f'evaluation={q(str(int(row.satisfaction)))}/>')
                continue
            # Kept out of the f-strings below: nesting a same-quoted f-string inside another is
            # only legal from Python 3.12 (PEP 701), and this package supports 3.11.
            measured_value = "{:.4f}".format(measured["measured_value"])
            coverage_note = "measured over {} of {} cases".format(
                int(measured["n_measured"]), int(measured["n_cases"])
            )
            # `thresholdValue` is optional in grl.kpimodel and some value sets legitimately omit it
            # (a binary/one-target indicator like Sepsis KPI3); emit the attribute only when set.
            threshold_attr = (
                "" if pd.isna(measured["threshold"]) else f'thresholdValue={q(str(measured["threshold"]))} '
            )
            lines.append(f'      <evaluations intElement={q(row.element_id)} '
                         f'evaluation={q(str(int(row.satisfaction)))}>')
            lines.append(
                f'        <kpiEvalValueSet targetValue={q(str(measured["target"]))} '
                f'{threshold_attr}worstValue={q(str(measured["worst"]))} '
                f'evaluationValue={q(measured_value)} unit={q(str(measured["unit"] or ""))} '
                f'qualitativeEvaluationValue={q(coverage_note)}/>'
            )
            lines.append("      </evaluations>")
        lines.append("    </strategies>")
        blocks.append("\n".join(lines))

    injected = "\n".join(blocks) + "\n"
    text = text.replace("    <impactModel/>", injected + "    <impactModel/>", 1)
    text = re.sub(r'nextGlobalID="\d+"', f'nextGlobalID="{next_id}"', text, count=1)
    atomic_write_text(destination, text)
    return destination


# ------------------------------------------------------------------------------------------
# Report and persistence
# ------------------------------------------------------------------------------------------


def build_indicator_report(indicator_df: pd.DataFrame, goal_df: pd.DataFrame, model: GRLModel) -> str:
    """A reviewer-facing summary: one measurement table per indicator across scopes, then the
    propagated satisfaction of the model's softgoals. Raw value and satisfaction always appear in
    the same row, and every caveat that applies to a row is printed on it rather than in a
    footnote a reader can skip."""
    if indicator_df.empty:
        return "# Step 7b — indicator satisfaction\n\nGoal model declares no measurable indicator.\n"

    lines = ["# Step 7b — indicator satisfaction", "",
             f"Goal model: `{Path(model.source_path).name}`", "",
             "Satisfaction is on GRL's [-100, +100] scale, converted from the measured value by each "
             "indicator's own `KPIEvalValueSet`. The measured value is reported beside it in every "
             "row: a score against an illustrative threshold reads exactly like one against a "
             "statute, and only the provenance column separates them.", ""]

    for indicator_id, group in indicator_df.groupby("indicator_id", sort=False):
        first = group.iloc[0]
        flags = []
        if first["one_sided"]:
            flags.append("**one-sided scale** (`target == threshold`: an admissibility boundary, not "
                         "a gradient — every compliant value saturates at the same score)")
        threshold_txt = "n/a" if pd.isna(first["threshold"]) else f"{first['threshold']}"
        lines += [f"## {first['indicator_name']} (id {indicator_id})", "",
                  f"- Value set: worst {first['worst']}, threshold {threshold_txt}, "
                  f"target {first['target']} {first['unit']}",
                  f"- Provenance: `{first['provenance']}` — {first['source']}"]
        for flag in flags:
            lines.append(f"- {flag}")
        lines += ["",
                  "| Scope | Measured | Satisfaction | Cases | Measured | Not applicable | No start | No end | Coverage |",
                  "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
        for row in group.itertuples():
            measured = "—" if pd.isna(row.measured_value) else f"{row.measured_value:.1f}"
            satisfaction = "—" if pd.isna(row.satisfaction) else f"{int(row.satisfaction):+d}"
            scope = "whole log" if row.scope == BASELINE_SCOPE else row.scope
            lines.append(
                f"| {scope} | {measured} | {satisfaction} | {row.n_cases} | {row.n_measured} | "
                f"{row.n_not_applicable} | {row.n_no_start} | {row.n_no_end} | {row.coverage:.0%} |"
            )
        lines.append("")

    softgoals = goal_df[goal_df["element_type"] == "Softgoal"]
    if not softgoals.empty:
        lines += ["## Propagated softgoal satisfaction", "",
                  "Propagated from the measured indicators through the same decomposition and "
                  "contribution graph Step 5a used as the taxonomy axis (`min` over And, `max` over "
                  "Or/Xor, weighted-clamped sum over contributions).", "",
                  "Only softgoals carry a value: indicators are the sole seeds, and they reach the "
                  "model through contribution links, so every goal and task in the decomposition "
                  "tree evaluates to the default 0. Seeding a category's `anchor_ids` with full "
                  "satisfaction would light the tree up, but it would also assert that a category "
                  "existing *is* its goal being met — the confound this measure is supposed to "
                  "expose, not commit.", ""]
        pivot = softgoals.pivot_table(index="element_name", columns="scope", values="satisfaction", aggfunc="first")
        header = list(pivot.columns)
        lines.append("| Softgoal | " + " | ".join("whole log" if c == BASELINE_SCOPE else c for c in header) + " |")
        lines.append("|---" * (len(header) + 1) + "|")
        for name, row in pivot.iterrows():
            lines.append(f"| {name} | " + " | ".join(f"{int(row[c]):+d}" for c in header) + " |")
        lines.append("")

    return "\n".join(lines) + "\n"


def save_indicator_outputs(
    indicator_df: pd.DataFrame,
    goal_df: pd.DataFrame,
    report_markdown: str,
    goal_model_path: Path,
    destination_dir: Path,
    run_label: str,
) -> None:
    destination_dir.mkdir(parents=True, exist_ok=True)
    atomic_write_csv(indicator_df, destination_dir / "indicator_satisfaction.csv", index=False)
    atomic_write_csv(goal_df, destination_dir / "goal_satisfaction.csv", index=False)
    atomic_write_text(destination_dir / "indicator_report.md", report_markdown)
    if not goal_df.empty:
        write_measured_jucm(
            goal_model_path, indicator_df, goal_df,
            destination_dir / f"{goal_model_path.stem}_measured.jucm", run_label,
        )

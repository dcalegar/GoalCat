from __future__ import annotations

import asyncio
import json
import logging
from pathlib import Path

import pandas as pd
import pm4py
from pydantic import BaseModel, Field, model_validator

from ..config import PipelineConfig, load_prompt_template
from ..discovery import build_category_sublogs
from .llm_backend import LLMBackend, RunMetadata
from .taxonomy import Category, Taxonomy, _resolve_anchor_labels

# Fixed thresholds, applied uniformly across every category -- same "fixed hyperparameters"
# philosophy as PipelineConfig.discovery_noise_threshold, not tuned per category.
_FITNESS_OK = 0.8
_PRECISION_OK = 0.7

# Coefficient-of-variation cutoffs for timing variability, likewise fixed across categories.
_CV_LOW = 0.3
_CV_HIGH = 1.0

# Top-variant share cutoffs for concentration, likewise fixed across categories.
_SHARE_DOMINANT = 0.7
_SHARE_FRAGMENTED = 0.2


def compute_model_looseness(log_fitness: float, precision: float) -> str:
    """Deterministic translation of Step 7's conformance numbers into words -- a pure function
    of two numbers, no semantic judgment, so a fixed threshold table is exact and reproducible
    where an LLM would only add hallucination risk for no benefit."""
    if log_fitness < _FITNESS_OK:
        return (
            f"The discovered model does not fit its own assigned cases well "
            f"(log fitness {log_fitness:.2f}) -- the model structure may not accurately "
            f"represent this category's real behavior."
        )
    if precision >= _PRECISION_OK:
        return (
            f"Tightly bounded: the model fits the observed cases well (log fitness "
            f"{log_fitness:.2f}) and permits little behavior beyond what was actually seen "
            f"(precision {precision:.2f})."
        )
    return (
        f"Loosely bounded: the model fits the observed cases well (log fitness "
        f"{log_fitness:.2f}) but permits substantially more behavior than was actually "
        f"observed (precision {precision:.2f}) -- consistent with a category that groups "
        f"together several distinct real paths."
    )


def _concentration_clause(assigned_variant_ids: list[str], variants_df: pd.DataFrame) -> str:
    freq_by_variant = dict(zip(variants_df["variant_id"], variants_df["frequency"]))
    frequencies = [freq_by_variant[vid] for vid in assigned_variant_ids]
    total_cases = sum(frequencies)
    num_variants = len(assigned_variant_ids)

    if num_variants == 1:
        return f"This category has a single variant, so all {total_cases} cases follow the exact same path."

    top_share = max(frequencies) / total_cases if total_cases else 0.0
    if top_share >= _SHARE_DOMINANT:
        return (
            f"A single dominant path accounts for {top_share * 100:.0f}% of this category's "
            f"cases, out of {num_variants} distinct variants."
        )
    if top_share <= _SHARE_FRAGMENTED:
        return (
            f"No single path dominates: the most frequent of {num_variants} distinct variants "
            f"accounts for only {top_share * 100:.0f}% of cases -- behavior is spread widely "
            f"across many distinct paths."
        )
    return (
        f"Moderate concentration: the most frequent of {num_variants} distinct variants "
        f"accounts for {top_share * 100:.0f}% of cases."
    )


def _timing_clause(sub_df: pd.DataFrame, config: PipelineConfig) -> str:
    num_cases = sub_df[config.case_id_key].nunique()
    if num_cases <= 1:
        # pm4py.discover_temporal_profile over a single case gives every (mean, std) pair a
        # zero std (one sample per activity pair), so avg_cv would land under _CV_LOW and
        # generate "...across cases" wording that overclaims a comparison that never happened —
        # caught here rather than computed and mis-described (mirrors _concentration_clause's
        # own num_variants == 1 special case, just for the timing half instead of concentration).
        return "Only one case in this category -- no cross-case waiting-time variability to characterize."

    profile = pm4py.discover_temporal_profile(
        sub_df,
        activity_key=config.activity_key,
        timestamp_key=config.timestamp_key,
        case_id_key=config.case_id_key,
    )
    ratios = [std / mean for mean, std in profile.values() if mean > 0]
    if not ratios:
        return "No inter-activity waiting time to characterize (cases here have at most one event)."

    avg_cv = sum(ratios) / len(ratios)
    if avg_cv < _CV_LOW:
        return "Waiting times between activities are consistent and predictable across cases."
    if avg_cv > _CV_HIGH:
        return (
            "Waiting times between activities are highly variable across cases -- worth "
            "checking whether this masks a hidden sub-behavior."
        )
    return "Waiting times between activities show moderate variability across cases."


def compute_discovered_pattern(
    assigned_variant_ids: list[str], sub_df: pd.DataFrame, variants_df: pd.DataFrame, config: PipelineConfig
) -> str:
    """Deterministic summary of a category's real cases: variant-frequency concentration (from
    variants_df, already computed by Step 1) + timing variability (from
    pm4py.discover_temporal_profile's raw (mean, std) pairs, read as numbers -- not through
    pm4py.llm.abstract_temporal_profile, which formats text for an LLM prompt, not for numeric
    parsing). Pure function of already-computed data, no semantic judgment."""
    return f"{_concentration_clause(assigned_variant_ids, variants_df)} {_timing_clause(sub_df, config)}"


class CategoryGoalAlignment(BaseModel):
    category_id: str = Field(description="Must exactly match one of the category_ids given in the prompt.")
    goal_alignment: str = Field(
        description="Does the discovered evidence (pattern + model looseness) support this "
        "category achieving the specific goal-model task/goal it is anchored to? Compare "
        "against the category's own declared description/rationale instead when there is no "
        "goal-model linkage (open induction)."
    )


class GoalAlignmentBatch(BaseModel):
    assessments: list[CategoryGoalAlignment]

    @model_validator(mode="after")
    def _unique_category_ids(self) -> "GoalAlignmentBatch":
        ids = [a.category_id for a in self.assessments]
        if len(ids) != len(set(ids)):
            raise ValueError(f"Duplicate category_id values in goal alignment batch: {ids}")
        return self


def _resolve_goal_linkage(category: Category, goal_model_text: str | None) -> str:
    """Same guard pattern build_assignment_report() already uses: a missing goal-model file
    (no goal model at all for this log) and an anchored category with no goal model both need
    distinct handling from _resolve_anchor_labels(), which assumes a real markdown string."""
    return _resolve_anchor_labels(goal_model_text, category.anchor_ids) if goal_model_text else "(no goal model)"


def _format_category_block(
    category: Category, deterministic: dict[str, str], metrics_row: dict, goal_model_text: str | None
) -> str:
    return (
        f"- category_id={category.category_id} | name={category.name}\n"
        f"  declared (Step 5): {category.description}\n"
        f"  goal-model linkage: {_resolve_goal_linkage(category, goal_model_text)}\n"
        f"  coverage: {metrics_row['num_variants']} variants, {metrics_row['num_cases']} cases\n"
        f"  discovered pattern: {deterministic['discovered_pattern']}\n"
        f"  model looseness: {deterministic['model_looseness']}"
    )


def build_goal_alignment_prompt(
    categories: list[Category],
    deterministic_by_category: dict[str, dict[str, str]],
    metrics_by_category: dict[str, dict],
    goal_model_text: str | None,
) -> str:
    blocks = "\n".join(
        _format_category_block(
            category, deterministic_by_category[category.category_id], metrics_by_category[category.category_id], goal_model_text
        )
        for category in categories
    )
    template = load_prompt_template("prompt_description.txt")
    return template.format(category_count=len(categories), category_blocks=blocks)


def check_goal_alignment_coverage(batch: GoalAlignmentBatch, categories: list[Category]) -> list[str]:
    """Flags missing or unexpected category_ids in the batch response. Warn-only, same rationale
    as check_taxonomy_grounding/check_assignment_grounding: Step 9's human review is the real
    correctness gate, not this check."""
    expected_ids = {c.category_id for c in categories}
    got_ids = {a.category_id for a in batch.assessments}

    problems = []
    missing = expected_ids - got_ids
    if missing:
        problems.append(f"missing goal_alignment for categories: {sorted(missing)}")
    unexpected = got_ids - expected_ids
    if unexpected:
        problems.append(f"goal_alignment given for unknown category_ids: {sorted(unexpected)}")
    return problems


def generate_descriptions_8(
    df: pd.DataFrame,
    variants_df: pd.DataFrame,
    assignments_df: pd.DataFrame,
    metrics_df: pd.DataFrame,
    taxonomy: Taxonomy,
    config: PipelineConfig,
    logger: logging.Logger,
) -> tuple[pd.DataFrame, RunMetadata | None, str]:
    """Step 8 orchestration: deterministic discovered_pattern/model_looseness per category (no
    LLM), then one batched LLM call for goal_alignment across the whole taxonomy. Categories with
    zero assigned variants (already reported as such by Step 7 -- no discovered model exists to
    describe) are skipped entirely, mirroring discover_all_categories()'s own skip-and-warn.

    Returns (descriptions_df, metadata, prompt). metadata is None and prompt is "" when every
    category was skipped (no LLM call made at all).
    """
    sublogs = build_category_sublogs(df, variants_df, assignments_df, config)
    category_of = dict(zip(assignments_df["variant_id"], assignments_df["category_id"]))
    metrics_by_category = metrics_df.set_index("category_id").to_dict(orient="index")
    goal_model_text = config.goal_model_path.read_text(encoding="utf-8") if config.goal_model_path else None

    active_categories = [c for c in taxonomy.categories if c.category_id in sublogs]
    for category in taxonomy.categories:
        if category.category_id not in sublogs:
            logger.warning("Category %s has no assigned variants -- skipping description.", category.category_id)

    if not active_categories:
        return pd.DataFrame(columns=["category_id", "discovered_pattern", "model_looseness", "goal_alignment"]), None, ""

    deterministic_by_category: dict[str, dict[str, str]] = {}
    for category in active_categories:
        assigned_variant_ids = [vid for vid, cat in category_of.items() if cat == category.category_id]
        sub_df = sublogs[category.category_id]
        metrics_row = metrics_by_category[category.category_id]
        deterministic_by_category[category.category_id] = {
            "discovered_pattern": compute_discovered_pattern(assigned_variant_ids, sub_df, variants_df, config),
            "model_looseness": compute_model_looseness(metrics_row["log_fitness"], metrics_row["precision"]),
        }
        logger.info("Computed deterministic description fields for category %s", category.category_id)

    prompt = build_goal_alignment_prompt(active_categories, deterministic_by_category, metrics_by_category, goal_model_text)

    backend = LLMBackend(config.llm.description_model, config.llm, logger)
    batch, metadata = asyncio.run(backend.generate_structured(prompt, GoalAlignmentBatch))

    problems = check_goal_alignment_coverage(batch, active_categories)
    for problem in problems:
        logger.warning("Goal alignment coverage check: %s", problem)
    if not problems:
        logger.info("Goal alignment coverage check: no problems found.")

    alignment_by_id = {a.category_id: a.goal_alignment for a in batch.assessments}
    rows = [
        {
            "category_id": category.category_id,
            "discovered_pattern": deterministic_by_category[category.category_id]["discovered_pattern"],
            "model_looseness": deterministic_by_category[category.category_id]["model_looseness"],
            "goal_alignment": alignment_by_id.get(category.category_id, "(missing from LLM response)"),
        }
        for category in active_categories
    ]
    descriptions_df = pd.DataFrame(rows, columns=["category_id", "discovered_pattern", "model_looseness", "goal_alignment"])
    return descriptions_df, metadata, prompt


def build_description_report(
    taxonomy: Taxonomy,
    descriptions_df: pd.DataFrame,
    metrics_df: pd.DataFrame,
    config: PipelineConfig,
    stale_goal_alignment_category_ids: frozenset[str] = frozenset(),
) -> str:
    """The lean, standalone Step 8 report: per category, a brief cross-reference to Step 5's
    declared description + resolved goal-model linkage (not a restatement) + coverage read from
    discovery_metrics.csv + the three generated fields. Links out to discovery_report.md for the
    full conformance table and model file links rather than duplicating them -- same
    minimal-context-plus-own-content idiom build_assignment_report()/build_discovery_report()
    already use.

    stale_goal_alignment_category_ids (review.py's rename path only; every other caller leaves
    this empty): category_ids whose declared description changed since goal_alignment below was
    generated -- that judgment was made against the *prior* description, so it's flagged rather
    than presented as still current.
    """
    goal_model_text = config.goal_model_path.read_text(encoding="utf-8") if config.goal_model_path else None
    metrics_by_category = metrics_df.set_index("category_id").to_dict(orient="index")
    descriptions_by_category = descriptions_df.set_index("category_id").to_dict(orient="index")

    lines = [
        "# Step 8 — High-level description generation report",
        "",
        f"Run: `{config.run_id}` | Log: `{config.log_stem}` | Description model: `{config.llm.description_model}`",
        "",
        "Full conformance metrics and model files are in "
        "[`discovery_report.md`](../07_discovery/discovery_report.md) (Step 7) -- not duplicated here.",
        "",
    ]

    for category in taxonomy.categories:
        stats = metrics_by_category.get(category.category_id, {})
        num_variants = stats.get("num_variants", 0)
        num_cases = stats.get("num_cases", 0)
        anchor_labels = (
            _resolve_anchor_labels(goal_model_text, category.anchor_ids) if goal_model_text else "(no goal model)"
        )

        lines += [
            f"## {category.name} (`{category.category_id}`)",
            "",
            f"**Declared (Step 5):** {category.description}",
            "",
            f"**Goal-model linkage:** {anchor_labels}",
            "",
            f"**Coverage:** {num_variants} variants, {num_cases} cases.",
            "",
        ]

        desc = descriptions_by_category.get(category.category_id)
        if desc is None:
            lines += ["No description generated -- no variants assigned to this category.", ""]
            continue

        lines += [
            f"**Discovered pattern:** {desc['discovered_pattern']}",
            "",
            f"**Model looseness:** {desc['model_looseness']}",
            "",
            f"**Goal alignment:** {desc['goal_alignment']}",
            "",
        ]
        if category.category_id in stale_goal_alignment_category_ids:
            lines += [
                "> **Stale:** this category's declared description changed via a Step 9 rename "
                "after the goal alignment above was generated -- it was judged against the "
                "*prior* description, not the one shown above. Re-run Step 8 against this round "
                "for an up-to-date judgment.",
                "",
            ]

    return "\n".join(lines)


def save_description_outputs(
    descriptions_df: pd.DataFrame, metadata: RunMetadata | None, prompt: str, report_markdown: str, output_dir: Path
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    descriptions_df.to_csv(output_dir / "descriptions.csv", index=False)
    (output_dir / "description_report.md").write_text(report_markdown, encoding="utf-8")
    if prompt:
        (output_dir / "description_prompt.txt").write_text(prompt, encoding="utf-8")

    metadata_payload = {"call": metadata.model_dump() if metadata is not None else None}
    (output_dir / "description_run_metadata.json").write_text(json.dumps(metadata_payload, indent=2), encoding="utf-8")

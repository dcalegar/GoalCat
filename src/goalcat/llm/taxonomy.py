from __future__ import annotations

import asyncio
import logging
from pathlib import Path

import pandas as pd
from pydantic import BaseModel, Field, model_validator

from .. import grl
from ..atomic_io import atomic_write_json, atomic_write_text
from ..config import PipelineConfig, load_prompt_template
from .llm_backend import LLMBackend, RunMetadata, estimate_cost_usd


class Category(BaseModel):
    """One taxonomy category. Anchored to the goal model's declared decomposition when one exists
    (Step 5a, intent-guided); anchor_ids is empty when none exists (Step 5b, open induction)."""

    category_id: str = Field(pattern=r"^[a-z][a-z0-9_]*$", description="Short stable slug, e.g. 'timely_payment'.")
    name: str
    description: str
    anchor_ids: list[str] = Field(
        description="Goal-model element ids (a Goal or Task's native .jucm id, e.g. ['20']) this "
        "category is traceable to — leave this empty if no goal model was provided "
        "(open/unsupervised induction, no declared axis to trace to)."
    )
    rationale: str = Field(description="Why this granularity was chosen, grounded in the narrative sample.")
    evidence_variant_ids: list[str] = Field(description="Sampled variant_ids supporting this category.")


class Taxonomy(BaseModel):
    categories: list[Category]

    @model_validator(mode="after")
    def _unique_category_ids(self) -> "Taxonomy":
        ids = [c.category_id for c in self.categories]
        if len(ids) != len(set(ids)):
            raise ValueError(f"Duplicate category_id values in taxonomy: {ids}")
        return self


def _render_goal_model_excerpt(jucm_text: str) -> str:
    """Renders the `.jucm` goal model's actors, decomposition tree, and contribution links —
    the same content the markdown-era `_extract_sections()` sliced out of §1-§5 (purpose, actors,
    decomposition, contributions), now read from the model directly rather than sliced out of
    prose. KPIs, activity-label traceability, and any narrative documentation are excluded by
    construction: `goalcat.grl.render_excerpt()` never renders them (see that function's
    docstring) — none of it helps subdividing the declared axis.

    This rendered excerpt — not the `.jucm` file, and not the prose `<log>GM_description.md` — is
    the only place any prompt states the goal model, and only Step 5a's two prompts contain it.
    `goalcat.grl.prompt`'s module docstring gives the four reasons for projecting rather than
    forwarding the XMI; the README's "What the LLM actually sees of the goal model" section states
    the same rationale for readers who never open the code.
    """
    return grl.render_excerpt(grl.parse_jucm(jucm_text))


def _format_narrative_block(row: pd.Series) -> str:
    return (
        f"- variant_id={row['variant_id']} | sample_reasons={row['sample_reasons']} | "
        f"frequency={row['frequency']} ({row['frequency_pct'] * 100:.1f}%) | "
        f"trace_length={row['trace_length']} | "
        f"duration_seconds_median={row['duration_seconds_median']:.0f} | "
        f"outcome={row['outcome']}\n"
        f"  narrative: {row['narrative']}"
    )


def _format_prior_category_block(category: Category) -> str:
    return (
        f"- category_id={category.category_id} | name={category.name}\n"
        f"  description: {category.description}\n"
        f"  anchor_ids={category.anchor_ids}\n"
        f"  rationale: {category.rationale}"
    )


def _format_prior_taxonomy_block(prior_taxonomy: Taxonomy) -> str:
    return "\n".join(_format_prior_category_block(c) for c in prior_taxonomy.categories)


def build_taxonomy_prompt(sample_df: pd.DataFrame, goal_model_text: str) -> str:
    excerpt = _render_goal_model_excerpt(goal_model_text)
    blocks = "\n".join(_format_narrative_block(row) for _, row in sample_df.iterrows())
    template = load_prompt_template("prompt_taxonomy_intent_guided.txt")
    return template.format(
        goal_model_excerpt=excerpt,
        sample_size=len(sample_df),
        narrative_blocks=blocks,
    )


def build_taxonomy_revision_prompt(
    sample_df: pd.DataFrame, goal_model_text: str, prior_taxonomy: Taxonomy, revision_instructions: str
) -> str:
    excerpt = _render_goal_model_excerpt(goal_model_text)
    blocks = "\n".join(_format_narrative_block(row) for _, row in sample_df.iterrows())
    template = load_prompt_template("prompt_taxonomy_intent_guided_revision.txt")
    return template.format(
        goal_model_excerpt=excerpt,
        sample_size=len(sample_df),
        narrative_blocks=blocks,
        prior_taxonomy_block=_format_prior_taxonomy_block(prior_taxonomy),
        revision_instructions=revision_instructions,
    )


def induce_taxonomy_5a(
    sample_df: pd.DataFrame,
    config: PipelineConfig,
    logger: logging.Logger,
    prior_taxonomy: Taxonomy | None = None,
    revision_instructions: str | None = None,
) -> tuple[Taxonomy, RunMetadata, str]:
    """Intent-guided taxonomy induction (Step 5a): a single LLM call, no concurrency needed.

    prior_taxonomy/revision_instructions (Step 9's merge/split revision round): when both are set,
    builds the revision prompt (existing taxonomy + the reviewer's requested change) instead of
    inducing fresh from the sample. Both default to None so every existing call site is unaffected.
    """
    if config.goal_model_path is None:
        raise ValueError(
            "induce_taxonomy_5a() (intent-guided induction) needs config.goal_model_filename "
            "set — got None. Either set it, or use taxonomy_mode='open' (induce_taxonomy_5b) "
            "for a log with no authored goal model."
        )
    goal_model_text = config.goal_model_path.read_text(encoding="utf-8")
    if prior_taxonomy is not None:
        prompt = build_taxonomy_revision_prompt(sample_df, goal_model_text, prior_taxonomy, revision_instructions)
    else:
        prompt = build_taxonomy_prompt(sample_df, goal_model_text)

    backend = LLMBackend(config.llm.taxonomy_model, config.llm, logger)
    taxonomy, metadata = asyncio.run(backend.generate_structured(prompt, Taxonomy))
    return taxonomy, metadata, prompt


def save_taxonomy(
    taxonomy: Taxonomy,
    metadata: RunMetadata,
    prompt: str,
    output_dir: Path,
    pricing_usd_per_million_tokens: dict[str, dict[str, float]],
) -> None:
    atomic_write_json(output_dir / "taxonomy.json", taxonomy.model_dump())
    atomic_write_text(output_dir / "taxonomy_prompt.txt", prompt)
    metadata_payload = {
        **metadata.model_dump(),
        "estimated_cost_usd": estimate_cost_usd(metadata, pricing_usd_per_million_tokens),
    }
    atomic_write_json(output_dir / "taxonomy_run_metadata.json", metadata_payload)


def overwrite_taxonomy_json(taxonomy: Taxonomy, output_dir: Path) -> None:
    """Writes only taxonomy.json — used by Step 9's rename path, which edits an existing taxonomy
    without a new LLM call, so taxonomy_prompt.txt/taxonomy_run_metadata.json (which describe that
    call) must stay untouched rather than being overwritten by save_taxonomy()."""
    atomic_write_json(output_dir / "taxonomy.json", taxonomy.model_dump())


def build_open_taxonomy_prompt(sample_df: pd.DataFrame) -> str:
    blocks = "\n".join(_format_narrative_block(row) for _, row in sample_df.iterrows())
    template = load_prompt_template("prompt_taxonomy_open.txt")
    return template.format(sample_size=len(sample_df), narrative_blocks=blocks)


def build_open_taxonomy_revision_prompt(
    sample_df: pd.DataFrame, prior_taxonomy: Taxonomy, revision_instructions: str
) -> str:
    blocks = "\n".join(_format_narrative_block(row) for _, row in sample_df.iterrows())
    template = load_prompt_template("prompt_taxonomy_open_revision.txt")
    return template.format(
        sample_size=len(sample_df),
        narrative_blocks=blocks,
        prior_taxonomy_block=_format_prior_taxonomy_block(prior_taxonomy),
        revision_instructions=revision_instructions,
    )


def induce_taxonomy_5b(
    sample_df: pd.DataFrame,
    config: PipelineConfig,
    logger: logging.Logger,
    prior_taxonomy: Taxonomy | None = None,
    revision_instructions: str | None = None,
) -> tuple[Taxonomy, RunMetadata, str]:
    """Open taxonomy induction (Step 5b): a single LLM call, no external axis to anchor to.

    prior_taxonomy/revision_instructions: see induce_taxonomy_5a's docstring — same revision-round
    mechanism, minus the goal model.
    """
    if prior_taxonomy is not None:
        prompt = build_open_taxonomy_revision_prompt(sample_df, prior_taxonomy, revision_instructions)
    else:
        prompt = build_open_taxonomy_prompt(sample_df)

    backend = LLMBackend(config.llm.taxonomy_model, config.llm, logger)
    taxonomy, metadata = asyncio.run(backend.generate_structured(prompt, Taxonomy))
    return taxonomy, metadata, prompt


def _extract_declared_ids(jucm_text: str) -> set[str]:
    """The set of valid goal-model element ids Step 5a's `anchor_ids` may reference — every
    `.jucm` `intElements` id (Goal/Task/Softgoal/Ressource/Indicator), read through the real
    GRL/URN metamodel (see `goalcat.grl`), not derived from a markdown table. Delegates to
    `goalcat.grl.declared_ids()`; kept as a same-named module function since
    `goalcat.pipeline.run_step5a_taxonomy()` imports it directly.
    """
    return grl.declared_ids(grl.parse_jucm(jucm_text))


def _resolve_anchor_labels(jucm_text: str, anchor_ids: list[str]) -> str:
    """Resolves anchor_ids to their real `id (type): name` label, e.g. '20 (Task): Resolve via
    coercive credit collection.' Deterministic lookup against the frozen goal model, not
    LLM-restated prose — used to explain a category's goal-model linkage in Step 6's assignment
    report without risking a hallucinated restatement of what the model already says.

    Returns a fixed placeholder for anchor_ids=[] (Step 5b, open induction — no goal model).
    Delegates to `goalcat.grl.resolve_anchor_labels()`; kept as a same-named module function
    since `goalcat.llm.description` imports it directly.
    """
    if not anchor_ids:
        return "(open induction — no goal model)"
    return grl.resolve_anchor_labels(grl.parse_jucm(jucm_text), anchor_ids)


def check_taxonomy_grounding(
    taxonomy: Taxonomy, sample_df: pd.DataFrame, valid_anchor_ids: set[str] | None = None
) -> list[str]:
    """Flags categories whose anchor_ids/evidence_variant_ids don't reference anything real.

    Warn-only by design, not raised: a hallucinated ID under temperature=0 would likely reproduce
    on retry, and Step 9's human review is this prototype's actual correctness gate, not this
    check. valid_anchor_ids=None means no goal model exists (Step 5b) — every category's
    anchor_ids must then be empty; a real ID set (Step 5a) means every anchor_ids entry must be
    in it. evidence_variant_ids is always checked against the sample's real variant_ids.
    """
    problems: list[str] = []
    valid_variant_ids = set(sample_df["variant_id"])

    for category in taxonomy.categories:
        bad_evidence = set(category.evidence_variant_ids) - valid_variant_ids
        if bad_evidence:
            problems.append(
                f"{category.category_id}: evidence_variant_ids not in sample: {sorted(bad_evidence)}"
            )

        if valid_anchor_ids is not None:
            bad_anchors = set(category.anchor_ids) - valid_anchor_ids
            if bad_anchors:
                problems.append(f"{category.category_id}: anchor_ids not in goal model: {sorted(bad_anchors)}")
            if not category.anchor_ids:
                # The Category schema itself permits an empty anchor_ids list unconditionally
                # (no min_length — 5b needs to allow it), so nothing structurally stops 5a from
                # producing an "anchored" category traceable to nothing. OVERVIEW.md's "every
                # category is traceable to a declared alternative" is a prompted constraint, not
                # a schema-enforced one — this is what actually checks it, warn-only like every
                # other check in this function.
                problems.append(
                    f"{category.category_id}: anchor_ids is empty under intent-guided induction — "
                    "not traceable to any declared goal-model alternative"
                )
        elif category.anchor_ids:
            problems.append(
                f"{category.category_id}: anchor_ids non-empty in open mode (no goal model): "
                f"{category.anchor_ids}"
            )

    return problems

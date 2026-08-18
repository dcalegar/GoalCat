from __future__ import annotations

import asyncio
import json
import logging
from pathlib import Path

import pandas as pd
from pydantic import BaseModel, Field, model_validator

from ..config import PipelineConfig, load_prompt_template
from .llm_backend import LLMBackend, RunMetadata

_SECTION_START = "## 1."
_SECTION_END = "## 6."


class Category(BaseModel):
    """One taxonomy category. Anchored to the goal model's declared decomposition when one exists
    (Step 5a, intent-guided); anchor_ids is empty when none exists (Step 5b, open induction)."""

    category_id: str = Field(pattern=r"^[a-z][a-z0-9_]*$", description="Short stable slug, e.g. 'timely_payment'.")
    name: str
    description: str
    anchor_ids: list[str] = Field(
        description="Goal-model element IDs (task or goal, from the §4 decomposition table) this "
        "category is traceable to, e.g. ['TP'] — leave this empty if no goal model was provided "
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


def _extract_sections(markdown_text: str, start: str = _SECTION_START, end: str = _SECTION_END) -> str:
    """Slices the goal-model markdown down to §1-§5 (purpose, actors, decomposition, contributions).

    Excludes §6 (KPIs — irrelevant to task categories), §7 (activity-label traceability table —
    the document itself warns against using it to pre-match narratives lexically) and §8/§9
    (limitations note, bibliography) — none of it helps subdividing the declared axis.
    """
    start_idx = markdown_text.index(start)
    end_idx = markdown_text.index(end, start_idx)
    return markdown_text[start_idx:end_idx].strip()


def _format_narrative_block(row: pd.Series) -> str:
    return (
        f"- variant_id={row['variant_id']} | sample_reasons={row['sample_reasons']} | "
        f"frequency={row['frequency']} ({row['frequency_pct'] * 100:.1f}%) | "
        f"trace_length={row['trace_length']} | "
        f"duration_seconds_median={row['duration_seconds_median']:.0f} | "
        f"outcome={row['outcome']}\n"
        f"  narrative: {row['narrative']}"
    )


def build_taxonomy_prompt(sample_df: pd.DataFrame, goal_model_text: str) -> str:
    excerpt = _extract_sections(goal_model_text)
    blocks = "\n".join(_format_narrative_block(row) for _, row in sample_df.iterrows())
    template = load_prompt_template("taxonomy_intent_guided.txt")
    return template.format(
        goal_model_excerpt=excerpt,
        sample_size=len(sample_df),
        narrative_blocks=blocks,
    )


def induce_taxonomy_5a(
    sample_df: pd.DataFrame, config: PipelineConfig, logger: logging.Logger
) -> tuple[Taxonomy, RunMetadata, str]:
    """Intent-guided taxonomy induction (Step 5a): a single LLM call, no concurrency needed."""
    goal_model_text = config.goal_model_path.read_text(encoding="utf-8")
    prompt = build_taxonomy_prompt(sample_df, goal_model_text)

    backend = LLMBackend(config.llm.taxonomy_model, config.llm, logger)
    taxonomy, metadata = asyncio.run(backend.generate_structured(prompt, Taxonomy))
    return taxonomy, metadata, prompt


def save_taxonomy(taxonomy: Taxonomy, metadata: RunMetadata, prompt: str, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "taxonomy.json").write_text(json.dumps(taxonomy.model_dump(), indent=2), encoding="utf-8")
    (output_dir / "taxonomy_prompt.txt").write_text(prompt, encoding="utf-8")
    (output_dir / "taxonomy_run_metadata.json").write_text(
        json.dumps(metadata.model_dump(), indent=2), encoding="utf-8"
    )


def build_open_taxonomy_prompt(sample_df: pd.DataFrame) -> str:
    blocks = "\n".join(_format_narrative_block(row) for _, row in sample_df.iterrows())
    template = load_prompt_template("taxonomy_open.txt")
    return template.format(sample_size=len(sample_df), narrative_blocks=blocks)


def induce_taxonomy_5b(
    sample_df: pd.DataFrame, config: PipelineConfig, logger: logging.Logger
) -> tuple[Taxonomy, RunMetadata, str]:
    """Open taxonomy induction (Step 5b): a single LLM call, no external axis to anchor to."""
    prompt = build_open_taxonomy_prompt(sample_df)

    backend = LLMBackend(config.llm.taxonomy_model, config.llm, logger)
    taxonomy, metadata = asyncio.run(backend.generate_structured(prompt, Taxonomy))
    return taxonomy, metadata, prompt


def _extract_declared_ids(markdown_text: str) -> set[str]:
    """Parses §4's decomposition table for the set of valid goal-model element IDs (G0-G5,
    T1-T4, TP/TA/TB/TC/TD for RTFM) — used only to ground-check Step 5a's anchor_ids."""
    start_idx = markdown_text.index("## 4.")
    end_idx = markdown_text.index("## 5.", start_idx)
    table_text = markdown_text[start_idx:end_idx]

    ids: set[str] = set()
    for line in table_text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if not cells:
            continue
        candidate = cells[0]
        if candidate == "ID" or set(candidate) <= {"-"}:
            continue
        ids.add(candidate)
    return ids


def _parse_decomposition_row(line: str) -> list[str] | None:
    line = line.strip()
    if not line.startswith("|"):
        return None
    cells = [cell.strip() for cell in line.strip("|").split("|")]
    if not cells or cells[0] == "ID" or set(cells[0]) <= {"-"}:
        return None
    return cells


def _resolve_anchor_labels(markdown_text: str, anchor_ids: list[str]) -> str:
    """Resolves anchor_ids to their real §4 Type/Label, e.g. 'TD (Task): Resolve via coercive
    credit collection.' Deterministic lookup against the frozen goal model, not LLM-restated
    prose — used to explain a category's goal-model linkage in Step 6's assignment report
    without risking a hallucinated restatement of what the document already says.

    Returns a fixed placeholder for anchor_ids=[] (Step 5b, open induction — no goal model).
    """
    if not anchor_ids:
        return "(open induction — no goal model)"

    start_idx = markdown_text.index("## 4.")
    end_idx = markdown_text.index("## 5.", start_idx)
    table_text = markdown_text[start_idx:end_idx]

    labels: dict[str, str] = {}
    for line in table_text.splitlines():
        cells = _parse_decomposition_row(line)
        if cells is None or len(cells) < 3:
            continue
        element_id, element_type, label = cells[0], cells[1], cells[2]
        labels[element_id] = f"{element_id} ({element_type}): {label}"

    resolved = [labels.get(anchor_id, f"{anchor_id} (not found in §4)") for anchor_id in anchor_ids]
    return "; ".join(resolved)


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
        elif category.anchor_ids:
            problems.append(
                f"{category.category_id}: anchor_ids non-empty in open mode (no goal model): "
                f"{category.anchor_ids}"
            )

    return problems

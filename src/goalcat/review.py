from __future__ import annotations

import json
import logging
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

import pandas as pd
import pm4py
import yaml
from pydantic import BaseModel, Field, ValidationError, model_validator

from .atomic_io import atomic_output_path, atomic_write_csv, atomic_write_json, atomic_write_text
from .config import (
    ASSIGNMENT_DIRNAME,
    DESCRIPTION_DIRNAME,
    DISCOVERY_DIRNAME,
    FINAL_DIRNAME,
    REVIEW_DIRNAME,
    REVIEW_INDEX_FILENAME,
    ROUND_PREFIX,
    SUBLOGS_DIRNAME,
    TAXONOMY_DIRNAME,
    PipelineConfig,
    load_config,
    load_prompt_template,
)
from .discovery import build_category_sublogs, build_discovery_report, build_residual_sublog, flag_low_precision_categories
from .extraction.log_io import load_event_log
from .extraction.variants import load_variants
from .llm.assignment import build_assignment_report, check_assignment_grounding
from .llm.description import build_description_report
from .llm.taxonomy import Taxonomy, overwrite_taxonomy_json
from .llm.usage_summary import save_execution_usage_summary, save_round_usage_summary
from .run_logging import get_logger


class RenameDecision(BaseModel):
    """Free/local: changes only a category's label, never which variants belong to it — applied
    directly, no LLM call, no new round (see apply_renames)."""

    category_id: str
    new_name: str | None = None
    new_description: str | None = None
    reason: str

    @model_validator(mode="after")
    def _has_a_change(self) -> "RenameDecision":
        if self.new_name is None and self.new_description is None:
            raise ValueError(f"rename for {self.category_id!r} must set new_name and/or new_description")
        return self


class MergeDecision(BaseModel):
    category_ids: list[str] = Field(min_length=2)
    reason: str

    @model_validator(mode="after")
    def _distinct_ids(self) -> "MergeDecision":
        if len(set(self.category_ids)) != len(self.category_ids):
            raise ValueError(f"merge category_ids must be distinct: {self.category_ids}")
        return self


class SplitDecision(BaseModel):
    category_id: str
    reason: str
    # No "into how many" field: granularity stays Step 5's authority, same as fresh induction —
    # the human states what and why, the LLM proposes the boundary.


class ReviewDecisions(BaseModel):
    decision: Literal["accept", "revise"]
    notes: str | None = None
    renames: list[RenameDecision] = Field(default_factory=list)
    merges: list[MergeDecision] = Field(default_factory=list)
    splits: list[SplitDecision] = Field(default_factory=list)

    @model_validator(mode="after")
    def _consistent(self) -> "ReviewDecisions":
        has_edits = bool(self.renames or self.merges or self.splits)
        if self.decision == "accept" and has_edits:
            raise ValueError("decision=accept requires renames/merges/splits to all be empty")
        if self.decision == "revise" and not has_edits:
            raise ValueError("decision=revise requires at least one of renames/merges/splits")

        seen: dict[str, str] = {}

        def claim(category_id: str, kind: str) -> None:
            if category_id in seen:
                raise ValueError(
                    f"category_id {category_id!r} appears in both {seen[category_id]!r} and "
                    f"{kind!r} — each category may only appear in one decision"
                )
            seen[category_id] = kind

        for r in self.renames:
            claim(r.category_id, "renames")
        for m in self.merges:
            for cid in m.category_ids:
                claim(cid, "merges")
        for s in self.splits:
            claim(s.category_id, "splits")

        return self


def validate_decisions_against_taxonomy(decisions: ReviewDecisions, taxonomy: Taxonomy) -> None:
    """Cross-checks category_ids against the real taxonomy — a model_validator alone can't do
    this, since ReviewDecisions has no taxonomy in scope. Raises loudly, same convention as
    LLMBackend's retry-on-ValidationError: a malformed human decision should fail fast, not
    silently misapply."""
    valid_ids = {c.category_id for c in taxonomy.categories}
    bad: list[str] = []
    for r in decisions.renames:
        if r.category_id not in valid_ids:
            bad.append(r.category_id)
    for m in decisions.merges:
        bad.extend(cid for cid in m.category_ids if cid not in valid_ids)
    for s in decisions.splits:
        if s.category_id not in valid_ids:
            bad.append(s.category_id)
    if bad:
        raise ValueError(f"review_decisions.yaml references unknown category_id(s): {sorted(set(bad))}")


def _quality_flags_comment(config: PipelineConfig) -> str:
    """Renders Step 7's low-precision categories (see flag_low_precision_categories) as a comment
    block for the review_decisions.yaml template — advisory only, never a decision: the reviewer
    reads it alongside discovery_report.md and still writes the actual merges/splits by hand.
    Empty string (no comment, just the template's existing blank line) if discovery_metrics.csv
    doesn't exist yet for this round or nothing is flagged."""
    metrics_path = config.discovery_dir / "discovery_metrics.csv"
    if not metrics_path.exists():
        return ""
    metrics_df = pd.read_csv(metrics_path)
    flagged = flag_low_precision_categories(metrics_df, config.review_precision_flag_threshold)
    if not flagged:
        return ""
    lines = [
        "#",
        f"# AUTOMATED SIGNAL (heuristic, precision < {config.review_precision_flag_threshold}, not a "
        "decision — read discovery_report.md before acting): low precision under a "
        "fitness-preserving discovery method can mean a category's sublog still spans multiple "
        "distinct behavioral patterns. Consider whether a split is warranted for:",
    ]
    for f in flagged:
        lines.append(f"#   {f['category_id']} ({f['name']}): precision={f['precision']:.3f}, log_fitness={f['log_fitness']:.3f}")
    return "\n".join(lines)


def write_review_template(taxonomy: Taxonomy, config: PipelineConfig, logger: logging.Logger) -> Path:
    """Writes review_decisions.yaml if absent; never overwrites an existing one, so in-progress
    human edits are never clobbered. Body lives in src/goalcat/templates/decisions_review.yaml —
    data, not code, same convention as every prompt template."""
    path = config.review_dir / "review_decisions.yaml"
    if path.exists():
        return path
    template = load_prompt_template("decisions_review.yaml")
    body = template.format(
        run_id=config.run_id,
        log_stem=config.log_stem,
        taxonomy_mode=config.taxonomy_mode,
        round=config.round,
        category_ids=", ".join(c.category_id for c in taxonomy.categories),
        quality_flags=_quality_flags_comment(config),
    )
    atomic_write_text(path, body)
    logger.info("Wrote review decisions template: %s", path)
    return path


def load_review_decisions(path: Path) -> ReviewDecisions:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    return ReviewDecisions.model_validate(raw)


def apply_renames(taxonomy: Taxonomy, renames: list[RenameDecision]) -> tuple[Taxonomy, list[dict]]:
    """Pure function: only name/description change; category_id/anchor_ids/rationale/
    evidence_variant_ids never do. Returns the new Taxonomy plus a before/after ledger for
    round_info.json's renames_applied (the full record, so no separate taxonomy backup file is
    needed)."""
    by_index = {c.category_id: i for i, c in enumerate(taxonomy.categories)}
    new_categories = list(taxonomy.categories)
    applied: list[dict] = []

    for r in renames:
        idx = by_index[r.category_id]
        category = new_categories[idx]
        before = {"name": category.name, "description": category.description}
        updates = {}
        if r.new_name is not None:
            updates["name"] = r.new_name
        if r.new_description is not None:
            updates["description"] = r.new_description
        updated = category.model_copy(update=updates)
        new_categories[idx] = updated
        applied.append(
            {
                "category_id": r.category_id,
                "before": before,
                "after": {"name": updated.name, "description": updated.description},
                "reason": r.reason,
            }
        )

    return Taxonomy(categories=new_categories), applied


def rerender_reports_after_rename(
    config: PipelineConfig,
    taxonomy: Taxonomy,
    logger: logging.Logger,
    stale_goal_alignment_category_ids: frozenset[str] = frozenset(),
) -> None:
    """Re-renders assignment_report.md/discovery_report.md/description_report.md from
    already-saved CSVs against the renamed taxonomy — confirmed a pure re-render (no LLM/
    discovery call): each build_*_report() needs only taxonomy + on-disk CSVs + config.

    stale_goal_alignment_category_ids: category_ids whose *description* (not just name) changed
    in this rename — descriptions.csv's goal_alignment prose for these was generated by Step 8's
    LLM call against the *prior* description, so the re-rendered report would otherwise pair a
    new declared description with a judgment made against the old one. Flagged in the report
    rather than silently left to look consistent (see process_review()'s caller for how this
    set is computed).
    """
    required = {
        "assignments.csv": config.assignment_dir / "assignments.csv",
        "structural_distances.parquet": config.assignment_dir / "structural_distances.parquet",
        "profile_distances.parquet": config.assignment_dir / "profile_distances.parquet",
        "profiles.csv": config.profiling_dir / "profiles.csv",
        "variants.csv": config.variants_dir / "variants.csv",
        "discovery_metrics.csv": config.discovery_dir / "discovery_metrics.csv",
    }
    missing = {name: path for name, path in required.items() if not path.exists()}
    if missing:
        raise ValueError(
            "Cannot apply a rename yet: Step 9 needs Steps 6 and 7 to have already produced "
            f"{', '.join(missing)} in this round before rerendering their reports (checked: "
            f"{', '.join(str(p) for p in missing.values())}). Run Steps 6-7 (and 8, if a "
            "description-changing rename is intended) against this round before reviewing it."
        )

    assignments_df = pd.read_csv(required["assignments.csv"], dtype={"variant_id": str})
    # Parquet round-trips variant_id_a/b as the pd.Categorical they were written as
    # (extraction/similarity.py's _pair_frame()); cast back to str here to match the CSV-era
    # dtype contract every downstream consumer (merges, comparisons in similarity.py) already
    # assumes, rather than auditing each of them for Categorical compatibility.
    structural_df = pd.read_parquet(required["structural_distances.parquet"]).astype(
        {"variant_id_a": str, "variant_id_b": str}
    )
    profile_df = pd.read_parquet(required["profile_distances.parquet"]).astype(
        {"variant_id_a": str, "variant_id_b": str}
    )
    profiles_df = pd.read_csv(required["profiles.csv"], dtype={"variant_id": str})
    variants_df = load_variants(required["variants.csv"])
    metrics_df = pd.read_csv(required["discovery_metrics.csv"])

    # Keep the raw CSV in sync too, not just the rendered report: build_discovery_report()
    # already reads category.name from the live `taxonomy` argument, not metrics_df's own
    # "name" column, so the *report* was never actually stale — but a consumer reading
    # discovery_metrics.csv directly would still see the pre-rename name without this.
    name_by_id = {c.category_id: c.name for c in taxonomy.categories}
    metrics_df["name"] = metrics_df["category_id"].map(name_by_id).fillna(metrics_df["name"])
    atomic_write_csv(metrics_df, required["discovery_metrics.csv"], index=False)

    assignment_report = build_assignment_report(
        taxonomy, assignments_df, profiles_df[["variant_id", "frequency"]], structural_df, profile_df, config
    )
    atomic_write_text(config.assignment_dir / "assignment_report.md", assignment_report)

    discovery_report = build_discovery_report(metrics_df, assignments_df, variants_df, taxonomy, config)
    atomic_write_text(config.discovery_dir / "discovery_report.md", discovery_report)

    descriptions_path = config.description_dir / "descriptions.csv"
    if descriptions_path.exists():
        descriptions_df = pd.read_csv(descriptions_path)
        description_report = build_description_report(
            taxonomy, descriptions_df, metrics_df, config, stale_goal_alignment_category_ids
        )
        atomic_write_text(config.description_dir / "description_report.md", description_report)

    logger.info("Re-rendered assignment/discovery/description reports after rename.")


def format_revision_instructions(decisions: ReviewDecisions) -> str:
    """Renders only merges/splits (with their reason) for the LLM revision prompt — renames are
    excluded because they're applied to the taxonomy *before* it becomes prior_taxonomy, so the
    LLM already sees the reviewer's chosen names."""
    blocks: list[str] = []
    for m in decisions.merges:
        blocks.append(f"MERGE these categories into one: {', '.join(m.category_ids)}.\n  Reason: {m.reason.strip()}")
    for s in decisions.splits:
        blocks.append(f"SPLIT this category: {s.category_id}.\n  Reason: {s.reason.strip()}")
    if decisions.notes:
        blocks.append(f"General reviewer notes: {decisions.notes.strip()}")
    return "\n\n".join(blocks)


def check_revision_grounding(prior_taxonomy: Taxonomy, new_taxonomy: Taxonomy, decisions: ReviewDecisions) -> list[str]:
    """Warn-only sanity check (same philosophy as check_taxonomy_grounding): did the revised
    taxonomy actually apply the requested merge/split, and did any untouched category vanish
    unexpectedly."""
    prior_ids = {c.category_id for c in prior_taxonomy.categories}
    new_ids = {c.category_id for c in new_taxonomy.categories}
    problems: list[str] = []

    merged_away_ids: set[str] = set()
    for m in decisions.merges:
        merged_away_ids.update(m.category_ids)
        if set(m.category_ids) <= new_ids:
            problems.append(
                f"merge requested for {m.category_ids}, but all of them are still present as "
                "separate categories in the revised taxonomy"
            )

    split_ids = {s.category_id for s in decisions.splits}
    for s in decisions.splits:
        if s.category_id in new_ids:
            problems.append(
                f"split requested for {s.category_id!r}, but it is still present unchanged in "
                "the revised taxonomy"
            )

    untouched_ids = prior_ids - merged_away_ids - split_ids
    missing_untouched = untouched_ids - new_ids
    if missing_untouched:
        problems.append(
            f"categories not mentioned in the revision request disappeared from the revised "
            f"taxonomy: {sorted(missing_untouched)}"
        )

    return problems


def _round_info_path(review_dir: Path) -> Path:
    return review_dir / "round_info.json"


def _load_or_init_round_info(config: PipelineConfig) -> dict:
    """Round 1's fresh-start case only — a later round's round_info.json is always written by
    start_revision_round() before this would ever be called for it."""
    path = _round_info_path(config.review_dir)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    info = {
        "round": config.round,
        "decision_summary": [],
        "status": "pending_review",
        "decided_at": None,
        "renames_applied": [],
    }
    _save_round_info(config.review_dir, info)
    return info


def _save_round_info(review_dir: Path, info: dict) -> None:
    atomic_write_json(_round_info_path(review_dir), info)


def list_rounds(config: PipelineConfig) -> list[dict]:
    """Lists every round of this execution, oldest first, by reading each round's own
    round_info.json. Round lineage is entirely implicit in directory nesting/numbering — no
    parent/child pointers needed, unlike the earlier per-run_id-per-round design."""
    run_output_dir = config.run_output_dir
    if not run_output_dir.is_dir():
        return []
    round_numbers = []
    for entry in run_output_dir.iterdir():
        if entry.is_dir() and entry.name.startswith(ROUND_PREFIX):
            suffix = entry.name[len(ROUND_PREFIX) :]
            if suffix.isdigit():
                round_numbers.append(int(suffix))
    rounds = []
    for n in sorted(round_numbers):
        info_path = run_output_dir / f"{ROUND_PREFIX}{n}" / REVIEW_DIRNAME / "round_info.json"
        if info_path.exists():
            rounds.append(json.loads(info_path.read_text(encoding="utf-8")))
    return rounds


def write_review_index(config: PipelineConfig) -> None:
    """The one artifact Step 9 maintains for the reviewer to read — a single, execution-level
    index (not one per round), regenerated on every Step 9 call. Determines "current round"
    itself via list_rounds() rather than trusting a caller-supplied value, so it stays correct
    even when called immediately after a new round was just created. No restated content —
    matches description_report.md's own link-out-rather-than-duplicate convention.
    """
    rounds = list_rounds(config)
    if not rounds:
        return
    current = rounds[-1]
    current_round = current["round"]
    status = current["status"]
    round_prefix = f"{ROUND_PREFIX}{current_round}"

    if status == "accepted":
        taxonomy_path = config.final_dir / "taxonomy.json"
        taxonomy_link = f"{FINAL_DIRNAME}/taxonomy.json"
    else:
        taxonomy_path = config.run_output_dir / round_prefix / TAXONOMY_DIRNAME / "taxonomy.json"
        taxonomy_link = f"{round_prefix}/{TAXONOMY_DIRNAME}/taxonomy.json"
    num_categories = len(Taxonomy.model_validate_json(taxonomy_path.read_text(encoding="utf-8")).categories)

    lines = [
        "# Step 9 — Business review index",
        "",
        f"Run: `{config.run_id}` | Log: `{config.log_stem}` | Taxonomy mode: `{config.taxonomy_mode}` "
        f"| Status: **{status.replace('_', ' ')}** (round {current_round})",
        "",
    ]

    if len(rounds) > 1:
        lines += ["## Rounds", ""]
        for r in rounds:
            summary = "; ".join(r["decision_summary"]) if r["decision_summary"] else "(initial induction)"
            marker = " **(current)**" if r["round"] == current_round else ""
            lines.append(f"- Round {r['round']}: {summary} — {r['status'].replace('_', ' ')}{marker}")
        lines.append("")

    a_report = f"{round_prefix}/{ASSIGNMENT_DIRNAME}/assignment_report.md"
    d_report = f"{round_prefix}/{DISCOVERY_DIRNAME}/discovery_report.md"
    desc_report = f"{round_prefix}/{DESCRIPTION_DIRNAME}/description_report.md"
    lines += [
        f"Read these before deciding, in this order (round {current_round}):",
        f"1. [`{a_report}`]({a_report}) — per-category coverage, cohesion, divergence, residual",
        f"2. [`{d_report}`]({d_report}) — per-category process model, fitness, precision",
        f"3. [`{desc_report}`]({desc_report}) — per-category prose description, goal alignment",
        "",
        f"Taxonomy: [`{taxonomy_link}`]({taxonomy_link}) ({num_categories} categories)",
        "",
    ]

    if status == "accepted":
        lines += [
            "## Accepted — final output",
            "",
            f"This run is the accepted final output. See [`{FINAL_DIRNAME}/README.md`]({FINAL_DIRNAME}/README.md).",
            "",
        ]
    else:
        decisions_link = f"{round_prefix}/{REVIEW_DIRNAME}/review_decisions.yaml"
        lines += [
            "## Your decision",
            "",
            f"Fill in [`{decisions_link}`]({decisions_link}) and re-run Step 9 against this run_id.",
            "",
        ]

    atomic_write_text(config.review_index_path, "\n".join(lines))


def save_partitioned_log(
    df: pd.DataFrame,
    variants_df: pd.DataFrame,
    assignments_df: pd.DataFrame,
    taxonomy: Taxonomy,
    config: PipelineConfig,
    logger: logging.Logger,
) -> None:
    """Accept/finalize: writes one partitioned .xes.gz per category into config.sublogs_dir
    (the pipeline's "partitioned log" — nothing else in the pipeline persists this), plus
    residual.xes.gz, always written even if empty, matching discover_all_categories()'s "explicit
    0, not silently absent" convention. .xes.gz (not .csv) matches the original log's own format
    and structurally resolves case:concept:name trailing as a flat column — pm4py.write_xes()
    correctly promotes it to each <trace> tag instead (verified directly before adopting this).

    Kept in their own sublogs/ subfolder of final/, not alongside taxonomy.json/README.md/
    pipeline_usage_summary.json, so a directory listing of final/ doesn't mix one-per-execution
    metadata files with the (potentially many) per-category log files."""
    sublogs = build_category_sublogs(df, variants_df, assignments_df, config)
    for category in taxonomy.categories:
        sub_df = sublogs.get(category.category_id, df.iloc[0:0])
        with atomic_output_path(config.sublogs_dir / f"{category.category_id}.xes.gz") as tmp:
            pm4py.write_xes(
                sub_df,
                str(tmp),
                case_id_key=config.case_id_key,
                activity_key=config.activity_key,
                timestamp_key=config.timestamp_key,
            )

    residual_df = build_residual_sublog(df, variants_df, assignments_df, config)
    with atomic_output_path(config.sublogs_dir / "residual.xes.gz") as tmp:
        pm4py.write_xes(
            residual_df,
            str(tmp),
            case_id_key=config.case_id_key,
            activity_key=config.activity_key,
            timestamp_key=config.timestamp_key,
        )

    logger.info("Saved partitioned log to: %s", config.sublogs_dir)


def write_final_manifest(config: PipelineConfig, taxonomy: Taxonomy, logger: logging.Logger) -> None:
    """The one new artifact final/ needs — links out to what stays in place (the reports) rather
    than duplicating them, same convention used throughout."""
    round_prefix = f"{ROUND_PREFIX}{config.round}"
    a_report = f"../{round_prefix}/{ASSIGNMENT_DIRNAME}/assignment_report.md"
    d_report = f"../{round_prefix}/{DISCOVERY_DIRNAME}/discovery_report.md"
    desc_report = f"../{round_prefix}/{DESCRIPTION_DIRNAME}/description_report.md"
    category_lines = "\n".join(f"- `{SUBLOGS_DIRNAME}/{c.category_id}.xes.gz`" for c in taxonomy.categories)

    body = (
        f"# Final output — accepted taxonomy (round {config.round})\n\n"
        f"This is the accepted, final deliverable of the GoalCat pipeline for `{config.log_stem}` "
        f"(run `{config.run_id}`).\n\n"
        f"- `taxonomy.json` — the accepted category taxonomy.\n"
        f"- `assignments.csv` — the full per-variant assignment (`variant_id` -> `category_id`, "
        f"plus distances and rationale) that produced `{SUBLOGS_DIRNAME}/`. A copy of "
        f"`{round_prefix}/{ASSIGNMENT_DIRNAME}/assignments.csv`, kept here so this taxonomy can be "
        f"re-filtered or re-partitioned by other tools without depending on the round directory "
        f"still existing.\n"
        f"- `{SUBLOGS_DIRNAME}/` — one `<category_id>.xes.gz` per category, the raw event log "
        f"partitioned per category:\n"
        f"{category_lines}\n"
        f"- `{SUBLOGS_DIRNAME}/residual.xes.gz` — cases that fit no category.\n\n"
        f"Process-model visualizations (Petri net + DFG renders) were not kept as part of this "
        f"deliverable to save disk space — re-run Step 7 against `assignments.csv` and this "
        f"taxonomy to regenerate them if needed.\n\n"
        f"For per-category coverage/cohesion, see [`{a_report}`]({a_report}).\n"
        f"For conformance metrics, see [`{d_report}`]({d_report}).\n"
        f"For prose descriptions and goal alignment, see [`{desc_report}`]({desc_report}).\n\n"
        f"Full revision history: [`../{REVIEW_INDEX_FILENAME}`](../{REVIEW_INDEX_FILENAME}).\n"
    )
    atomic_write_text(config.final_dir / "README.md", body)
    logger.info("Wrote final manifest: %s", config.final_dir / "README.md")


def _prune_pairwise_distances(config: PipelineConfig, logger: logging.Logger) -> None:
    """Deletes structural_distances.parquet/profile_distances.parquet from every roundN/ of this
    execution, not just the round being accepted — see config.yaml's
    prune_pairwise_distances_on_finalize for why this is opt-in: a superseded round's copies are
    what rerender_reports_after_rename() reads back if that round is ever re-reviewed with a
    rename, and Step 6 has no reuse guard for either table, so pruning them trades that (rare)
    re-review path's cost for disk space now."""
    freed_bytes = 0
    deleted_paths: list[Path] = []
    for entry in sorted(config.run_output_dir.iterdir()):
        if not (entry.is_dir() and entry.name.startswith(ROUND_PREFIX)):
            continue
        assignment_dir = entry / ASSIGNMENT_DIRNAME
        for filename in ("structural_distances.parquet", "profile_distances.parquet"):
            path = assignment_dir / filename
            if path.exists():
                freed_bytes += path.stat().st_size
                path.unlink()
                deleted_paths.append(path)

    if deleted_paths:
        logger.info(
            "Pruned %d pairwise variant-distance Parquet file(s) across all rounds of run %s (%.1f MB freed): %s",
            len(deleted_paths),
            config.run_id,
            freed_bytes / (1024 * 1024),
            ", ".join(str(p) for p in deleted_paths),
        )


def finalize_run(
    config: PipelineConfig,
    variants_df: pd.DataFrame,
    assignments_df: pd.DataFrame,
    taxonomy: Taxonomy,
    round_info: dict,
    logger: logging.Logger,
) -> None:
    """Accept path: writes the partitioned log + moves taxonomy.json into final/, deletes this
    round's rendered models (per user direction — not necessary to keep; the data to regenerate
    them stays in this round's own assignments.csv/taxonomy.json history), re-renders this
    round's discovery_report.md so it doesn't dangle-link to the deleted files, and marks the
    round accepted.

    Refuses to finalize (raises) rather than silently producing an incomplete partition:
    the pipeline's "exhaustive partition + coverage + an explicit residual" claim depends on
    every variant landing in assignments_df with either a real category_id or a residual (NaN)
    one, but two things can violate that silently otherwise — a variant whose Step 6 LLM call
    never succeeded is never written into assignments.csv at all (assign_narratives_6() reports
    it via failed_variant_ids, not a row), and a hallucinated category_id that names no real
    category counts as neither a category member nor a residual under build_category_sublogs()/
    build_residual_sublog()'s pd.notna()/pd.isna() split — both cases mean the variant simply
    never appears in final/sublogs/ (no category .xes.gz, not in residual.xes.gz either), caught here
    before that happens rather than discovered later by someone doing the arithmetic."""
    missing_ids = set(variants_df["variant_id"]) - set(assignments_df["variant_id"])
    if missing_ids:
        raise ValueError(
            f"Cannot accept round {config.round}: {len(missing_ids)} variant(s) have no Step 6 "
            "outcome at all (not categorized, not residual — their LLM call never succeeded and "
            f"never got resumed): {sorted(missing_ids)}. Re-run Step 6 against this run/round to "
            "retry them before accepting — accepting now would silently drop them from every "
            "final/ output, category files and residual.xes.gz alike."
        )
    grounding_problems = check_assignment_grounding(assignments_df, taxonomy)
    if grounding_problems:
        raise ValueError(
            f"Cannot accept round {config.round}: {len(grounding_problems)} assignment(s) name a "
            "category_id that isn't in this taxonomy: " + "; ".join(grounding_problems) + ". Such "
            "a variant is neither a category member nor a residual under build_category_sublogs()/"
            "build_residual_sublog()'s pd.notna()/pd.isna() split, so it would silently vanish "
            "from final/ entirely. Fix the offending row(s) in assignments.csv (or re-run Step 6 "
            "for just those narratives) before accepting."
        )

    df = load_event_log(config)
    save_partitioned_log(df, variants_df, assignments_df, taxonomy, config, logger)

    config.final_dir.mkdir(parents=True, exist_ok=True)
    shutil.move(str(config.taxonomy_dir / "taxonomy.json"), str(config.final_dir / "taxonomy.json"))
    shutil.copy(str(config.assignment_dir / "assignments.csv"), str(config.final_dir / "assignments.csv"))

    models_dir = config.discovery_dir / "models"
    if models_dir.is_dir():
        shutil.rmtree(models_dir)

    if config.prune_pairwise_distances_on_finalize:
        _prune_pairwise_distances(config, logger)

    metrics_df = pd.read_csv(config.discovery_dir / "discovery_metrics.csv")
    discovery_report = build_discovery_report(
        metrics_df, assignments_df, variants_df, taxonomy, config, models_present=False
    )
    atomic_write_text(config.discovery_dir / "discovery_report.md", discovery_report)

    write_final_manifest(config, taxonomy, logger)

    round_info["status"] = "accepted"
    round_info["decided_at"] = datetime.now(timezone.utc).isoformat()
    _save_round_info(config.review_dir, round_info)

    write_review_index(config)

    # Execution-wide LLM usage/cost, combining every round of this run_id — the one place that
    # knows the run is actually done (see llm.usage_summary's module docstring for why neither
    # AI Studio's GUI nor GCP Billing can attribute this to a single run). The full breakdown
    # (per round, per step) lives in final/pipeline_usage_summary.json; this log line is just a
    # human-readable pointer to it, next to every other per-call line pipeline.log already has.
    usage = save_execution_usage_summary(config)["totals"]
    cost = "unknown" if usage["total_estimated_cost_usd"] is None else f"${usage['total_estimated_cost_usd']:.4f}"
    logger.info(
        "Run %s LLM usage total: %d calls, %d input + %d output tokens, %d prompt + %d response "
        "chars, %.1fs latency, %s — full breakdown in %s",
        config.run_id,
        usage["call_count"],
        usage["total_input_tokens"],
        usage["total_output_tokens"],
        usage["total_prompt_chars"],
        usage["total_response_chars"],
        usage["total_latency_seconds"],
        cost,
        config.final_dir / "pipeline_usage_summary.json",
    )
    logger.info("Run %s finalized (accepted, round %d).", config.run_id, config.round)


def start_revision_round(
    config_path: str | Path | None,
    config: PipelineConfig,
    decisions: ReviewDecisions,
    renamed_taxonomy: Taxonomy,
    source_decisions_filename: str,
) -> int:
    """Merge/split path: advances to a new round nested in the same execution directory — no new
    run_id, no file copying. Steps 1-4 outputs are read directly from their execution-scoped
    folders by every round (see pipeline.py's _get_or_build_* helpers), so nothing needs
    "carrying forward." Re-derives the taxonomy via Step 5a/5b with the reviewer's revision
    instructions, then re-runs Steps 6-8 fresh under the new round. round_info.json for the new
    round is written only *after* the taxonomy call succeeds — a failure there leaves no trace of
    the new round on disk at all (save_taxonomy() never runs), so a retry's round auto-detection
    isn't misled by a half-written round. Returns the new round number.
    """
    # Deferred import: pipeline.py imports review.py at module level (to delegate
    # run_step9_review's body), so a module-level import here would be circular. This is the
    # only place review.py needs to call back into the step orchestration.
    from .pipeline import (
        run_step5_taxonomy,
        run_step6_assignment,
        run_step7_discovery,
        run_step7b_indicators,
        run_step8_description,
        run_step9_review,
    )

    new_round = config.round + 1
    logger = get_logger(config)
    logger.info(
        "Step 9 revision round started: round %d -> round %d (run %s)", config.round, new_round, config.run_id
    )

    revision_instructions = format_revision_instructions(decisions)
    taxonomy = run_step5_taxonomy(
        config_path,
        config.run_id,
        round=new_round,
        prior_taxonomy=renamed_taxonomy,
        revision_instructions=revision_instructions,
    )

    problems = check_revision_grounding(renamed_taxonomy, taxonomy, decisions)
    for problem in problems:
        logger.warning("Revision grounding check: %s", problem)
    if not problems:
        logger.info("Revision grounding check: no problems found.")

    summary_lines = [f"merge: {m.category_ids} -> reason: {m.reason.strip()}" for m in decisions.merges]
    summary_lines += [f"split: {s.category_id} -> reason: {s.reason.strip()}" for s in decisions.splits]
    new_review_dir = config.run_output_dir / f"{ROUND_PREFIX}{new_round}" / REVIEW_DIRNAME
    _save_round_info(
        new_review_dir,
        {
            "round": new_round,
            "decision_summary": summary_lines,
            "status": "pending_review",
            "decided_at": None,
            "renames_applied": [],
            "source_decisions_file": f"../{ROUND_PREFIX}{config.round}/{REVIEW_DIRNAME}/{source_decisions_filename}",
        },
    )

    run_step6_assignment(config_path, config.run_id, round=new_round)
    run_step7_discovery(config_path, config.run_id, round=new_round)
    run_step7b_indicators(config_path, config.run_id, round=new_round)
    run_step8_description(config_path, config.run_id, round=new_round)
    run_step9_review(config_path, config.run_id, round=new_round)

    logger.info("Step 9 revision round complete. Run %s now at round %d.", config.run_id, new_round)
    return new_round


def process_review(config_path: str | Path | None, config: PipelineConfig, logger: logging.Logger) -> dict:
    """Step 9's orchestration body (called by pipeline.run_step9_review). Like Steps 6-8, does
    NOT implicitly recompute a missing taxonomy/assignments — both must already be on disk for
    the current round.
    """
    # round_info is checked before taxonomy_path/assignments_path: an accepted round has already
    # had its taxonomy.json *moved* into final/ (see finalize_run()), so requiring it to still
    # exist in taxonomy_dir before allowing the accepted short-circuit would make re-invoking
    # Step 9 against an already-accepted round raise instead of idempotently no-op.
    round_info = _load_or_init_round_info(config)

    if round_info["status"] == "accepted":
        logger.info("Run %s already accepted — nothing to do.", config.run_id)
        return {"status": "accepted", "run_id": config.run_id, "round": config.round}

    taxonomy_path = config.taxonomy_dir / "taxonomy.json"
    assignments_path = config.assignment_dir / "assignments.csv"
    if not taxonomy_path.exists() or not assignments_path.exists():
        raise ValueError(
            "run_step9_review() needs a taxonomy and assignments already on disk: point "
            "run_id/round (arguments, or config.yaml's fields) at a round directory that "
            f"already has both taxonomy.json and assignments.csv in it (checked: "
            f"{taxonomy_path}, {assignments_path})."
        )
    taxonomy = Taxonomy.model_validate_json(taxonomy_path.read_text(encoding="utf-8"))

    # Refreshed every time Step 9 runs against this round (not just on accept) — round_dir /
    # round_usage_summary.json rolls up Steps 5/6/8's own *_run_metadata.json (see
    # llm.usage_summary), tolerating Step 8 not having run yet. finalize_run() later combines
    # every round's copy of this file into the execution-wide total.
    save_round_usage_summary(config)

    decisions_path = config.review_dir / "review_decisions.yaml"
    if not decisions_path.exists():
        write_review_template(taxonomy, config, logger)
        write_review_index(config)
        logger.info("Step 9: awaiting review — fill in %s", decisions_path)
        return {"status": "awaiting_review", "run_id": config.run_id, "round": config.round}

    try:
        decisions = load_review_decisions(decisions_path)
    except ValidationError as exc:
        # write_review_template()'s own scaffold (decision: revise, every section empty) does
        # not itself validate — deliberately, so a reviewer can't accidentally accept-by-doing-
        # nothing (see its own comment block) — but re-running Step 9 against the untouched
        # template, or a partially-edited file, must not surface as a raw pydantic traceback.
        raise ValueError(
            f"{decisions_path} is not a valid decision yet — either it's still the auto-written "
            "template (decision: revise with every section empty, which is deliberately "
            "invalid) or an edit left it inconsistent. Set decision: accept with every section "
            "empty, or decision: revise with at least one rename/merge/split filled in, then "
            f"re-run Step 9. Validation error: {exc}"
        ) from exc
    validate_decisions_against_taxonomy(decisions, taxonomy)

    if decisions.decision == "accept":
        variants_path = config.variants_dir / "variants.csv"
        metrics_path = config.discovery_dir / "discovery_metrics.csv"
        if not variants_path.exists() or not metrics_path.exists():
            raise ValueError(
                "Cannot accept: finalize_run() also needs Step 1's variants.csv and Step 7's "
                f"discovery_metrics.csv already on disk (checked: {variants_path}, "
                f"{metrics_path}) — run Steps 1 and 7 against this round before accepting."
            )
        assignments_df = pd.read_csv(assignments_path, dtype={"variant_id": str})
        variants_df = load_variants(variants_path)
        finalize_run(config, variants_df, assignments_df, taxonomy, round_info, logger)
        logger.info("Step 9: run %s accepted (round %d).", config.run_id, config.round)
        return {"status": "accepted", "run_id": config.run_id, "round": config.round}

    # decision == "revise": renames (if any) apply first, in place, against this same round.
    renamed_taxonomy = taxonomy
    if decisions.renames:
        renamed_taxonomy, applied = apply_renames(taxonomy, decisions.renames)
        overwrite_taxonomy_json(renamed_taxonomy, config.taxonomy_dir)
        stale_ids = frozenset(
            a["category_id"] for a in applied if a["before"]["description"] != a["after"]["description"]
        )
        rerender_reports_after_rename(config, renamed_taxonomy, logger, stale_ids)
        round_info["renames_applied"].extend(applied)
        _save_round_info(config.review_dir, round_info)
        logger.info("Step 9: applied %d rename(s) to run %s round %d.", len(applied), config.run_id, config.round)

    processed_name = f"review_decisions_processed_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.yaml"

    if not decisions.merges and not decisions.splits:
        # Rename-only: doesn't end the round — archive the processed file, write a fresh
        # template so the human can look again.
        decisions_path.rename(config.review_dir / processed_name)
        write_review_template(renamed_taxonomy, config, logger)
        write_review_index(config)
        return {"status": "renamed", "run_id": config.run_id, "round": config.round}

    # merge/split: ends this round, starts a new one. The decisions file is archived only
    # *after* the new round succeeds — if start_revision_round() raises (e.g. a transient LLM
    # failure), review_decisions.yaml stays in place with the reviewer's original request
    # intact, so a plain re-invocation retries cleanly instead of silently losing it.
    new_round = start_revision_round(config_path, config, decisions, renamed_taxonomy, processed_name)
    decisions_path.rename(config.review_dir / processed_name)

    round_info["status"] = "revised"
    _save_round_info(config.review_dir, round_info)
    write_review_index(config)

    return {"status": "revised", "run_id": config.run_id, "round": new_round}

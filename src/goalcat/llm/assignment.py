from __future__ import annotations

import asyncio
import json
import logging
from pathlib import Path

import pandas as pd
from pydantic import BaseModel, Field, model_validator

from ..config import PipelineConfig, load_prompt_template
from .llm_backend import LLMBackend, RunMetadata
from .taxonomy import Taxonomy, _resolve_anchor_labels


class VariantAssignment(BaseModel):
    """One narrative's classification within a batched call. variant_id is part of the schema —
    unlike a single-item call, one response here covers several narratives, so the caller needs
    the LLM's own echo to map each judgment back to the narrative it belongs to."""

    variant_id: str = Field(description="Must exactly match one of the variant_ids given in the prompt.")
    category_id: str | None = Field(
        description="A category_id from the taxonomy this narrative realizes, or null if none "
        "of the categories fit (the narrative becomes part of the residual)."
    )
    rationale: str = Field(description="Why this narrative does, or does not, realize the chosen category.")


class AssignmentBatch(BaseModel):
    assignments: list[VariantAssignment]

    @model_validator(mode="after")
    def _unique_variant_ids(self) -> "AssignmentBatch":
        ids = [a.variant_id for a in self.assignments]
        if len(ids) != len(set(ids)):
            raise ValueError(f"Duplicate variant_id values in assignment batch: {ids}")
        return self


_MODE_CLAUSES = {
    "intent_guided": (
        "by subdividing a declared goal-model axis — every category is traceable to specific "
        "goal-model elements, so 'realize' means the narrative satisfies that declared alternative"
    ),
    "open": (
        "directly from a narrative sample, with no external declaration to anchor to — 'realize' "
        "means the narrative matches the recurring pattern the category describes"
    ),
}


def _format_category_block(category) -> str:
    return f"- category_id={category.category_id} | name={category.name}\n  description: {category.description}"


def _format_narrative_block(narrative_row: pd.Series) -> str:
    return (
        f"- variant_id={narrative_row['variant_id']} | frequency={narrative_row['frequency']} "
        f"({narrative_row['frequency_pct'] * 100:.1f}%) | "
        f"duration_seconds_median={narrative_row['duration_seconds_median']:.0f} | "
        f"outcome={narrative_row['outcome']}\n"
        f"  narrative: {narrative_row['narrative']}"
    )


def _build_assignment_batch_prompt(batch_df: pd.DataFrame, taxonomy: Taxonomy, taxonomy_mode: str) -> str:
    if taxonomy_mode not in _MODE_CLAUSES:
        raise ValueError(f"Unknown taxonomy_mode={taxonomy_mode!r} (expected 'intent_guided' or 'open')")
    category_blocks = "\n".join(_format_category_block(c) for c in taxonomy.categories)
    narrative_blocks = "\n".join(_format_narrative_block(row) for _, row in batch_df.iterrows())
    template = load_prompt_template("prompt_assignment_batch.txt")
    return template.format(
        mode_clause=_MODE_CLAUSES[taxonomy_mode],
        category_blocks=category_blocks,
        narrative_count=len(batch_df),
        narrative_blocks=narrative_blocks,
    )


class _RateLimiter:
    """Paces call starts to at most requests_per_minute, independent of concurrency.

    concurrency alone bounds how many calls run *simultaneously*; it does not bound *rate* when
    individual calls are fast — Step 6's first live run against Gemini's free tier (15
    requests/minute for gemini-3.5-flash-lite) hit this exactly: concurrency=1 still ran at
    roughly one call/second, ~4x over the cap, since nothing paced successive call starts.
    requests_per_minute=None disables pacing (paid tier / other providers).
    """

    def __init__(self, requests_per_minute: int | None) -> None:
        self._interval = 60.0 / requests_per_minute if requests_per_minute else 0.0
        self._lock = asyncio.Lock()
        self._next_allowed = 0.0

    async def wait(self) -> None:
        if self._interval <= 0:
            return
        async with self._lock:
            loop = asyncio.get_event_loop()
            now = loop.time()
            if now < self._next_allowed:
                await asyncio.sleep(self._next_allowed - now)
                now = self._next_allowed
            self._next_allowed = now + self._interval


async def _assign_batch(
    backend: LLMBackend,
    semaphore: asyncio.Semaphore,
    rate_limiter: _RateLimiter,
    batch_df: pd.DataFrame,
    taxonomy: Taxonomy,
    taxonomy_mode: str,
    logger: logging.Logger,
) -> tuple[dict[str, VariantAssignment], RunMetadata | None, list[str]]:
    """One LLM call per batch of up to config.llm.assignment_batch_size narratives. Catches its
    own failures rather than letting them propagate to asyncio.gather, same rationale as the
    original per-narrative version (see PROGRESS.md): one persistent transport failure must not
    discard every other batch's already-completed work. Batching trades away per-narrative
    isolation for call-count reduction, though — a failed/invalid response here leaves every
    narrative in this batch pending, not just one."""
    variant_ids = list(batch_df["variant_id"])
    prompt = _build_assignment_batch_prompt(batch_df, taxonomy, taxonomy_mode)
    async with semaphore:
        await rate_limiter.wait()
        try:
            batch, metadata = await backend.generate_structured(prompt, AssignmentBatch)
        except Exception as exc:
            logger.warning(
                "Assignment batch call failed for %d narratives, will remain pending: %s", len(variant_ids), exc
            )
            return {}, None, variant_ids

    by_id = {a.variant_id: a for a in batch.assignments}
    unexpected = set(by_id) - set(variant_ids)
    for variant_id in unexpected:
        logger.warning("Assignment batch response returned unexpected variant_id %s — discarded", variant_id)
        del by_id[variant_id]
    missing = [variant_id for variant_id in variant_ids if variant_id not in by_id]
    if missing:
        logger.warning(
            "Assignment batch response missing %d/%d narratives, will remain pending: %s",
            len(missing), len(variant_ids), missing,
        )
    return by_id, metadata, missing


def _build_batches(pending_df: pd.DataFrame, batch_size: int) -> list[pd.DataFrame]:
    return [pending_df.iloc[i : i + batch_size] for i in range(0, len(pending_df), batch_size)]


async def _assign_all(
    batches: list[pd.DataFrame], taxonomy: Taxonomy, config: PipelineConfig, logger: logging.Logger
) -> list[tuple[dict[str, VariantAssignment], RunMetadata | None, list[str]]]:
    backend = LLMBackend(config.llm.assignment_model, config.llm, logger)
    semaphore = asyncio.Semaphore(config.llm.concurrency)
    rate_limiter = _RateLimiter(config.llm.requests_per_minute)
    tasks = [
        _assign_batch(backend, semaphore, rate_limiter, batch_df, taxonomy, config.taxonomy_mode, logger)
        for batch_df in batches
    ]
    return await asyncio.gather(*tasks)


def assign_narratives_6(
    merged_df: pd.DataFrame, taxonomy: Taxonomy, config: PipelineConfig, logger: logging.Logger
) -> tuple[pd.DataFrame, list[RunMetadata], list[tuple[str, str, str]], list[str]]:
    """Narrative assignment (Step 6): one LLM call per batch of config.llm.assignment_batch_size
    narratives (default 20), with up to config.llm.concurrency batch calls in flight at once —
    the first pipeline step needing more than one concurrent call.

    Returns (assignments_df, metadata_list, batch_prompts, failed_variant_ids). batch_prompts is
    one (first_variant_id, last_variant_id, prompt_text) entry per batch actually sent this call,
    in call order — every prompt this run submitted, not just a sample of the first one, so
    save_assignment_outputs() can persist the full set for traceability. A narrative whose batch
    call failed, or whose batch response omitted it, is reported in failed_variant_ids, not
    silently dropped or treated as a residual (a residual means the LLM decided no category fits,
    a substantively different outcome from an infrastructure failure). The caller decides how to
    handle retrying failures.
    """
    batches = _build_batches(merged_df, config.llm.assignment_batch_size)
    batch_prompts = [
        (
            str(batch_df["variant_id"].iloc[0]),
            str(batch_df["variant_id"].iloc[-1]),
            _build_assignment_batch_prompt(batch_df, taxonomy, config.taxonomy_mode),
        )
        for batch_df in batches
    ]

    results = asyncio.run(_assign_all(batches, taxonomy, config, logger))

    rows = []
    metadata_list = []
    failed_variant_ids = []
    for by_id, metadata, missing in results:
        failed_variant_ids.extend(missing)
        if metadata is not None:
            metadata_list.append(metadata)
        for variant_id, assignment in by_id.items():
            rows.append({"variant_id": variant_id, "category_id": assignment.category_id, "rationale": assignment.rationale})

    assignments_df = pd.DataFrame(rows, columns=["variant_id", "category_id", "rationale"])
    return assignments_df, metadata_list, batch_prompts, failed_variant_ids


def load_prior_assignments(output_dir: Path) -> tuple[pd.DataFrame, list[RunMetadata]]:
    """Reads back a previous (possibly partial) run's assignments.csv and
    assignment_run_metadata.json, for resuming an interrupted Step 6 call against the same run
    directory — retrying only the narratives that never got a successful assignment, instead of
    re-sending (and re-billing) every batch call after a single transient failure.

    Returns empty results if either file is missing (nothing to resume from).
    """
    assignments_path = output_dir / "assignments.csv"
    metadata_path = output_dir / "assignment_run_metadata.json"

    if not assignments_path.exists():
        return pd.DataFrame(columns=["variant_id", "category_id", "rationale"]), []

    # category_id is left as pandas' own missing-value representation for a residual row
    # (pd.isna(x) == True) rather than forced to Python None — pandas' string-dtype inference
    # (default since pandas 3) silently re-coerces None back to it on any DataFrame construction
    # anyway, so every category_id check in this module uses pd.isna()/pd.notna(), never `is None`.
    prior_df = pd.read_csv(assignments_path, dtype={"variant_id": str})
    prior_df = prior_df[["variant_id", "category_id", "rationale"]]

    metadata_list: list[RunMetadata] = []
    if metadata_path.exists():
        payload = json.loads(metadata_path.read_text(encoding="utf-8"))
        metadata_list = [RunMetadata.model_validate(call) for call in payload.get("calls", [])]

    return prior_df, metadata_list


def check_assignment_grounding(assignments_df: pd.DataFrame, taxonomy: Taxonomy) -> list[str]:
    """Flags any category_id that is neither None nor a real category id. Warn-only, same
    rationale as check_taxonomy_grounding: Step 9's human review is the real correctness gate.
    """
    valid_ids = {c.category_id for c in taxonomy.categories}
    problems = []
    for variant_id, category_id in zip(assignments_df["variant_id"], assignments_df["category_id"]):
        if pd.notna(category_id) and category_id not in valid_ids:
            problems.append(f"{variant_id}: category_id {category_id!r} not in taxonomy")
    return problems


def _build_distance_lookup(distances_df: pd.DataFrame, distance_column: str) -> dict[tuple[str, str], float]:
    lookup: dict[tuple[str, str], float] = {}
    for a, b, d in zip(distances_df["variant_id_a"], distances_df["variant_id_b"], distances_df[distance_column]):
        lookup[(a, b)] = d
        lookup[(b, a)] = d
    return lookup


def _distance(lookup: dict[tuple[str, str], float], a: str, b: str) -> float:
    return 0.0 if a == b else lookup[(a, b)]


def _category_medoid(members: list[str], lookup: dict[tuple[str, str], float]) -> str:
    if len(members) == 1:
        return members[0]
    return min(members, key=lambda cand: sum(_distance(lookup, cand, other) for other in members if other != cand))


def _per_variant_distance_stats(
    assignments_df: pd.DataFrame, distances_df: pd.DataFrame, distance_column: str
) -> pd.DataFrame:
    """Per variant: distance to its own category's medoid (NaN for residual, 0.0 for a
    singleton category) and the nearest variant outside its category, with that variant's
    category id and distance — computed for residual variants too, against every categorized
    variant, since 'which category is this leftover narrative closest to' is itself a useful
    diagnostic for the report's residual section.
    """
    # category_of values come straight from a DataFrame column: missing category_id round-trips
    # as pandas' own NA sentinel (pd.isna() == True), not Python None — pandas 3's string-dtype
    # inference silently converts None to it on DataFrame construction, so every "is this a
    # residual" check here must use pd.isna()/pd.notna(), never `is None`.
    lookup = _build_distance_lookup(distances_df, distance_column)
    category_of = dict(zip(assignments_df["variant_id"], assignments_df["category_id"]))
    members_by_category: dict[str, list[str]] = {}
    for variant_id, category_id in category_of.items():
        if pd.notna(category_id):
            members_by_category.setdefault(category_id, []).append(variant_id)
    medoid_by_category = {cat: _category_medoid(members, lookup) for cat, members in members_by_category.items()}

    rows = []
    for variant_id, own_category in category_of.items():
        if pd.notna(own_category):
            medoid_distance = _distance(lookup, variant_id, medoid_by_category[own_category])
        else:
            medoid_distance = float("nan")

        candidates = [
            other_id
            for other_id, other_category in category_of.items()
            if pd.notna(other_category) and other_category != own_category and other_id != variant_id
        ]
        if candidates:
            nearest_id = min(candidates, key=lambda cand: _distance(lookup, variant_id, cand))
            nearest_category = category_of[nearest_id]
            nearest_distance = _distance(lookup, variant_id, nearest_id)
        else:
            nearest_category = None
            nearest_distance = float("nan")

        rows.append(
            {
                "variant_id": variant_id,
                "distance_to_category_medoid": medoid_distance,
                "nearest_other_category_id": nearest_category,
                "nearest_other_category_distance": nearest_distance,
            }
        )
    return pd.DataFrame(rows)


def _category_pairwise_stats(
    distances_df: pd.DataFrame, category_of: dict[str, str | None], distance_column: str
) -> dict[str, dict]:
    """Per category: mean intra-category distance (cohesion) and the nearest other category by
    mean inter-category distance (separation)."""
    df = distances_df.copy()
    df["category_a"] = df["variant_id_a"].map(category_of)
    df["category_b"] = df["variant_id_b"].map(category_of)
    df = df[df["category_a"].notna() & df["category_b"].notna()]

    stats: dict[str, dict] = {}
    for category in sorted(set(df["category_a"]) | set(df["category_b"])):
        intra = df[(df["category_a"] == category) & (df["category_b"] == category)][distance_column]
        inter = df[
            ((df["category_a"] == category) & (df["category_b"] != category))
            | ((df["category_b"] == category) & (df["category_a"] != category))
        ].copy()
        inter["other_category"] = inter.apply(
            lambda r: r["category_b"] if r["category_a"] == category else r["category_a"], axis=1
        )

        nearest_other_id = None
        nearest_other_mean = float("nan")
        if len(inter):
            by_other = inter.groupby("other_category")[distance_column].mean()
            nearest_other_id = by_other.idxmin()
            nearest_other_mean = by_other.min()

        stats[category] = {
            "intra_mean": intra.mean() if len(intra) else float("nan"),
            "nearest_other_category_id": nearest_other_id,
            "nearest_other_mean": nearest_other_mean,
        }
    return stats


def _divergence_callout(
    structural_df: pd.DataFrame, profile_df: pd.DataFrame, category_of: dict[str, str | None], top_n: int = 10
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Pairs where the structural and profile distances disagree sharply: same category but
    structurally far apart ('loose_within'), or different category but structurally
    near-identical ('tight_across', the TP/TA-style case)."""
    merged = structural_df.merge(profile_df[["variant_id_a", "variant_id_b", "profile_distance_mean"]], on=["variant_id_a", "variant_id_b"])
    merged["category_a"] = merged["variant_id_a"].map(category_of)
    merged["category_b"] = merged["variant_id_b"].map(category_of)
    merged = merged[merged["category_a"].notna() & merged["category_b"].notna()]

    max_distance = merged["distance"].max()
    merged["structural_norm"] = merged["distance"] / max_distance if max_distance else 0.0

    same_category = merged[merged["category_a"] == merged["category_b"]]
    diff_category = merged[merged["category_a"] != merged["category_b"]]

    loose_within = same_category.nlargest(top_n, "structural_norm")
    tight_across = diff_category.nsmallest(top_n, "structural_norm")
    return loose_within, tight_across


def _fmt_stat(value: float | None, macro_count: int | None = None, precision: int = 2) -> str:
    """Renders a cohesion statistic, or a legible reason instead of a bare 'nan' when it's
    undefined — a singleton category has no intra-category pairs to average over."""
    if value is None or pd.isna(value):
        return "n/a (singleton category)" if macro_count == 1 else "n/a"
    return f"{value:.{precision}f}"


def build_assignment_report(
    taxonomy: Taxonomy,
    assignments_df: pd.DataFrame,
    merged_df: pd.DataFrame,
    structural_df: pd.DataFrame,
    profile_df: pd.DataFrame,
    config: PipelineConfig,
    pending_variant_ids: list[str] | None = None,
) -> str:
    """The consolidated Markdown explainability artifact for Step 9's human reviewer.

    pending_variant_ids: narratives with no assignment yet because their LLM call has failed
    every attempt so far (not because the LLM decided no category fits) — reported explicitly,
    distinct from the residual, since re-running Step 6 against the same run directory retries
    exactly these.
    """
    pending_variant_ids = pending_variant_ids or []
    category_of = dict(zip(assignments_df["variant_id"], assignments_df["category_id"]))
    freq_by_variant = dict(zip(merged_df["variant_id"], merged_df["frequency"]))
    total_variants = len(assignments_df)
    total_cases = sum(freq_by_variant.get(vid, 0) for vid in category_of)

    structural_stats = _category_pairwise_stats(structural_df, category_of, "distance")
    profile_stats = _category_pairwise_stats(profile_df, category_of, "profile_distance_mean")
    goal_model_text = config.goal_model_path.read_text(encoding="utf-8") if config.goal_model_path else None

    lines = [
        "# Step 6 — Narrative assignment report",
        "",
        f"Run: `{config.run_id}` | Log: `{config.log_stem}` | Taxonomy mode: `{config.taxonomy_mode}` "
        f"| Assignment model: `{config.llm.assignment_model}`",
        "",
        f"{total_variants} variants, {total_cases} cases total.",
        "",
    ]
    if pending_variant_ids:
        lines += [
            f"**{len(pending_variant_ids)} variants still pending** (API calls failed every "
            f"attempt this run, not yet a residual): {', '.join(pending_variant_ids)}. Re-run "
            f"Step 6 against run `{config.run_id}` to retry only these.",
            "",
        ]

    for category in taxonomy.categories:
        assigned = [vid for vid, cat in category_of.items() if cat == category.category_id]
        macro_count = len(assigned)
        macro_pct = macro_count / total_variants * 100 if total_variants else 0.0
        micro_count = sum(freq_by_variant.get(vid, 0) for vid in assigned)
        micro_pct = micro_count / total_cases * 100 if total_cases else 0.0

        s_stats = structural_stats.get(category.category_id, {})
        p_stats = profile_stats.get(category.category_id, {})

        anchor_labels = (
            _resolve_anchor_labels(goal_model_text, category.anchor_ids) if goal_model_text else "(no goal model)"
        )

        lines += [
            f"## {category.name} (`{category.category_id}`)",
            "",
            category.description,
            "",
            f"**Taxonomy-derivation rationale (Step 5):** {category.rationale}",
            "",
            f"**Goal-model linkage:** {anchor_labels}",
            "",
            f"**Coverage:** macro {macro_count}/{total_variants} variants ({macro_pct:.1f}%) · "
            f"micro {micro_count}/{total_cases} cases ({micro_pct:.1f}%)",
            "",
            f"**Cohesion — structural (control-flow proximity):** intra-category mean distance "
            f"{_fmt_stat(s_stats.get('intra_mean'), macro_count)}, nearest other category "
            f"`{s_stats.get('nearest_other_category_id')}` at mean distance "
            f"{_fmt_stat(s_stats.get('nearest_other_mean'))}",
            "",
            f"**Cohesion — profile (duration/outcome/rework):** intra-category mean distance "
            f"{_fmt_stat(p_stats.get('intra_mean'), macro_count, precision=3)}, nearest other category "
            f"`{p_stats.get('nearest_other_category_id')}` at mean distance "
            f"{_fmt_stat(p_stats.get('nearest_other_mean'), precision=3)}",
            "",
        ]

    loose_within, tight_across = _divergence_callout(structural_df, profile_df, category_of)
    lines += [
        "## Divergence between structural and profile distance",
        "",
        "Flagged for review, not resolved automatically — the two metrics measure different "
        "things (control-flow vs. business profile) and disagreement is informative on its own.",
        "",
        "**Same category, structurally far apart** (possibly a category covering two distinct "
        "control-flow patterns):",
        "",
    ]
    if len(loose_within):
        for _, row in loose_within.iterrows():
            lines.append(
                f"- `{row['variant_id_a']}` / `{row['variant_id_b']}` (category `{row['category_a']}`): "
                f"structural={row['distance']:.0f}, profile={row['profile_distance_mean']:.3f}"
            )
    else:
        lines.append("- none")

    lines += [
        "",
        "**Different category, structurally near-identical** (the TP/TA-style case — categories "
        "distinguished on business intent the activity sequence alone would not show):",
        "",
    ]
    if len(tight_across):
        for _, row in tight_across.iterrows():
            lines.append(
                f"- `{row['variant_id_a']}` (`{row['category_a']}`) / `{row['variant_id_b']}` "
                f"(`{row['category_b']}`): structural={row['distance']:.0f}, "
                f"profile={row['profile_distance_mean']:.3f}"
            )
    else:
        lines.append("- none")

    residual_ids = [vid for vid, cat in category_of.items() if pd.isna(cat)]
    residual_macro_pct = len(residual_ids) / total_variants * 100 if total_variants else 0.0
    residual_cases = sum(freq_by_variant.get(vid, 0) for vid in residual_ids)
    residual_micro_pct = residual_cases / total_cases * 100 if total_cases else 0.0
    rationale_by_variant = dict(zip(assignments_df["variant_id"], assignments_df["rationale"]))

    lines += [
        "",
        "## Residual",
        "",
        f"{len(residual_ids)}/{total_variants} variants ({residual_macro_pct:.1f}%), "
        f"{residual_cases}/{total_cases} cases ({residual_micro_pct:.1f}%) unassigned.",
        "",
    ]
    for vid in residual_ids:
        lines.append(f"- `{vid}`: {rationale_by_variant.get(vid, '')}")

    return "\n".join(lines)


def save_assignment_outputs(
    assignments_df: pd.DataFrame,
    metadata_list: list[RunMetadata],
    batch_prompts: list[tuple[str, str, str]],
    report_markdown: str,
    structural_df: pd.DataFrame,
    profile_df: pd.DataFrame,
    output_dir: Path,
) -> None:
    """batch_prompts: one (first_variant_id, last_variant_id, prompt_text) entry per batch this
    call actually sent (see assign_narratives_6) — written one file per batch under
    assignment_prompts/, named by the batch's variant_id range, for full traceability of every
    assignment prompt rather than a single example. Empty on a fully-resumed run that made zero
    new calls, which leaves any prompt files an earlier call already wrote untouched: each call
    against a run directory only covers its own pending subset, so nothing here is ever cleared."""
    output_dir.mkdir(parents=True, exist_ok=True)

    structural_stats = _per_variant_distance_stats(assignments_df, structural_df, "distance")
    profile_stats = _per_variant_distance_stats(assignments_df, profile_df, "profile_distance_mean")

    enriched = assignments_df.merge(
        structural_stats.rename(
            columns={
                "distance_to_category_medoid": "structural_distance_to_category_medoid",
                "nearest_other_category_id": "nearest_other_category_id",
                "nearest_other_category_distance": "nearest_other_category_structural_distance",
            }
        ),
        on="variant_id",
    ).merge(
        profile_stats.rename(
            columns={
                "distance_to_category_medoid": "profile_distance_to_category_medoid",
                "nearest_other_category_distance": "nearest_other_category_profile_distance",
            }
        )[["variant_id", "profile_distance_to_category_medoid", "nearest_other_category_profile_distance"]],
        on="variant_id",
    )
    enriched.to_csv(output_dir / "assignments.csv", index=False)

    structural_df.to_csv(output_dir / "structural_distances.csv", index=False)
    profile_df.to_csv(output_dir / "profile_distances.csv", index=False)

    (output_dir / "assignment_report.md").write_text(report_markdown, encoding="utf-8")
    if batch_prompts:
        prompts_dir = output_dir / "assignment_prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        for first_variant_id, last_variant_id, prompt in batch_prompts:
            (prompts_dir / f"{first_variant_id}_{last_variant_id}.txt").write_text(prompt, encoding="utf-8")

    metadata_payload = {
        "calls": [m.model_dump() for m in metadata_list],
        "total_input_tokens": sum(m.input_tokens or 0 for m in metadata_list),
        "total_output_tokens": sum(m.output_tokens or 0 for m in metadata_list),
        "total_latency_seconds": sum(m.latency_seconds for m in metadata_list),
    }
    (output_dir / "assignment_run_metadata.json").write_text(json.dumps(metadata_payload, indent=2), encoding="utf-8")

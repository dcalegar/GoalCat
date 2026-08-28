from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from . import grl
from .config import PipelineConfig, load_config
from .discovery import discover_all_categories, save_discovery_outputs
from .extraction.log_io import load_event_log
from .extraction.profiling import load_profiles, profile_variants, save_profiles
from .extraction.similarity import (
    compute_profile_distances,
    compute_structural_distances,
    empty_profile_distances,
    empty_structural_distances,
)
from .extraction.variants import extract_variants, load_variants, save_variants
from .indicators import (
    build_indicator_report,
    compute_indicator_satisfaction,
    save_indicator_outputs,
)
from .llm.assignment import (
    assign_narratives_6,
    build_assignment_report,
    check_assignment_grounding,
    load_prior_assignments,
    save_assignment_outputs,
)
from .llm.description import build_description_report, generate_descriptions_8, save_description_outputs
from .llm.taxonomy import (
    Taxonomy,
    check_taxonomy_grounding,
    induce_taxonomy_5a,
    induce_taxonomy_5b,
    save_taxonomy,
)
from .narrative.sampling import load_narrative_sample, sample_narratives, save_narrative_sample
from .narrative.textualization import load_narratives, render_narratives, save_narratives
from .review import process_review
from .run_logging import get_logger, log_peak_memory


class IncompleteAssignmentError(ValueError):
    """Raised when a step would proceed on an assignment that does not cover every variant.

    Subclasses ValueError because that is what every other refusal in this pipeline raises
    (goalcat.review.finalize_run's own completeness guard included), so existing callers keep
    catching it; declared as its own type so a resume driver can catch *this* specific condition —
    the one that a re-run of Step 6 actually repairs — without swallowing unrelated ValueErrors.
    """


def _get_or_build_variants(config: PipelineConfig, logger: logging.Logger) -> pd.DataFrame:
    """Loads variants.csv from config.variants_dir if it's already there (a reused execution
    directory), else computes it from the raw log and saves it. Shared by every step whose
    input, not primary output, is the variants table. Execution-scoped, not round-scoped."""
    path = config.variants_dir / "variants.csv"
    if path.exists():
        logger.info("Loading variants from existing run directory: %s", path)
        return load_variants(path)
    df = load_event_log(config)
    variants_df = extract_variants(df, config)
    save_variants(variants_df, path)
    return variants_df


def _get_or_build_profiles(config: PipelineConfig, logger: logging.Logger) -> pd.DataFrame:
    csv_path = config.profiling_dir / "profiles.csv"
    json_path = config.profiling_dir / "profiles.json"
    if csv_path.exists() and json_path.exists():
        logger.info("Loading profiles from existing run directory: %s", csv_path)
        return load_profiles(csv_path, json_path)
    variants_df = _get_or_build_variants(config, logger)
    df = load_event_log(config)
    profiles_df = profile_variants(df, variants_df, config)
    save_profiles(profiles_df, csv_path, json_path)
    return profiles_df


def _get_or_build_narratives(config: PipelineConfig, logger: logging.Logger) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Returns (profiles_df, narratives_df) — both, since Step 6 needs both and this is the
    shortest disk-first path to get them: if narratives.csv and profiles.* are all already in
    the run directory, this skips the raw log, variant extraction, and profiling entirely."""
    profiles_csv = config.profiling_dir / "profiles.csv"
    profiles_json = config.profiling_dir / "profiles.json"
    narratives_csv = config.textualization_dir / "narratives.csv"
    if profiles_csv.exists() and profiles_json.exists() and narratives_csv.exists():
        logger.info("Loading profiles/narratives from existing run directory: %s", config.run_output_dir)
        return load_profiles(profiles_csv, profiles_json), load_narratives(narratives_csv)
    profiles_df = _get_or_build_profiles(config, logger)
    narratives_df = render_narratives(profiles_df, config, logger)
    save_narratives(narratives_df, narratives_csv)
    return profiles_df, narratives_df


def _get_or_build_sample(config: PipelineConfig, logger: logging.Logger) -> pd.DataFrame:
    path = config.sampling_dir / "narrative_sample.csv"
    if path.exists():
        logger.info("Loading narrative sample from existing run directory: %s", path)
        return load_narrative_sample(path)
    profiles_df, narratives_df = _get_or_build_narratives(config, logger)
    sample_df = sample_narratives(profiles_df, narratives_df, config)
    save_narrative_sample(sample_df, path)
    return sample_df


def run_step1_variants(
    config_path: str | Path | None = None, run_id: str | None = None, force: bool = False
) -> pd.DataFrame:
    """Variant extraction (pipeline Step 1): load the log, group traces by activity sequence.

    force=False (default): if this run directory's variants.csv already exists, reuses it instead
    of recomputing — matching the resumability every OTHER step already gets when it needs
    variants.csv as an input dependency (via _get_or_build_variants()). Without this, a driver
    that retries a full run after a later step failed would silently redo every earlier step's
    work on each retry, even though its output is already correct and on disk (measured cost:
    ~4-5 minutes of redone Steps 1-4 work on BPIC2019's full log). Pass force=True to recompute
    on purpose (e.g. after a code change to extract_variants()).
    """
    config = load_config(config_path, run_id)
    logger = get_logger(config)

    logger.info("Step 1 (variant extraction) started for log: %s", config.log_path)

    output_path = config.variants_dir / "variants.csv"
    if not force and output_path.exists():
        logger.info(
            "Step 1: reusing existing variants.csv in this run directory (pass force=True to "
            "recompute): %s", output_path,
        )
        variants_df = load_variants(output_path)
        logger.info("Step 1 complete (reused).")
        return variants_df

    df = load_event_log(config)
    num_cases = df[config.case_id_key].nunique()
    logger.info("Loaded event log: %d events, %d cases", len(df), num_cases)

    variants_df = extract_variants(df, config)
    top = variants_df.iloc[0]
    logger.info(
        "Extracted %d variants. Top variant: %s (frequency=%d, %.1f%%)",
        len(variants_df),
        " > ".join(top["activity_sequence"]),
        top["frequency"],
        top["frequency_pct"] * 100,
    )

    save_variants(variants_df, output_path)
    logger.info("Saved variants to: %s", output_path)

    logger.info("Step 1 complete.")
    log_peak_memory(logger, "Step 1")
    return variants_df


def run_step2_profiling(
    config_path: str | Path | None = None,
    run_id: str | None = None,
    variants_df: pd.DataFrame | None = None,
    force: bool = False,
) -> pd.DataFrame:
    """Multi-view profiling (pipeline Step 2): duration, rework, outcome, resource per variant.

    force=False (default): reuses this run directory's profiles.csv/profiles.json if both already
    exist, instead of recomputing — see run_step1_variants()'s docstring for why. Pass force=True
    to recompute on purpose.
    """
    config = load_config(config_path, run_id)
    logger = get_logger(config)

    logger.info("Step 2 (multi-view profiling) started for log: %s", config.log_path)

    csv_path = config.profiling_dir / "profiles.csv"
    json_path = config.profiling_dir / "profiles.json"
    if not force and csv_path.exists() and json_path.exists():
        logger.info(
            "Step 2: reusing existing profiles.csv/profiles.json in this run directory (pass "
            "force=True to recompute): %s", csv_path,
        )
        profiles_df = load_profiles(csv_path, json_path)
        logger.info("Step 2 complete (reused).")
        return profiles_df

    if variants_df is None:
        variants_df = _get_or_build_variants(config, logger)
    df = load_event_log(config)
    logger.info("Profiling %d variants against %d events", len(variants_df), len(df))

    profiles_df = profile_variants(df, variants_df, config)
    top = profiles_df.iloc[0]
    logger.info(
        "Profiled %d variants. Top variant representative case: %s (outcome=%s, duration_median=%.0fs)",
        len(profiles_df),
        top["representative_case_id"],
        top["outcome"],
        top["duration_seconds_median"],
    )

    save_profiles(profiles_df, csv_path, json_path)
    logger.info("Saved profiles to: %s and %s", csv_path, json_path)

    logger.info("Step 2 complete.")
    log_peak_memory(logger, "Step 2")
    return profiles_df


def run_step3_textualization(
    config_path: str | Path | None = None,
    run_id: str | None = None,
    profiles_df: pd.DataFrame | None = None,
    force: bool = False,
) -> pd.DataFrame:
    """Textualization (pipeline Step 3): render each variant's profile as a narrative via LUPIN.

    force=False (default): reuses this run directory's narratives.csv if it already exists,
    instead of recomputing — see run_step1_variants()'s docstring for why. Pass force=True to
    recompute on purpose.
    """
    config = load_config(config_path, run_id)
    logger = get_logger(config)

    logger.info("Step 3 (textualization) started for log: %s", config.log_path)

    output_path = config.textualization_dir / "narratives.csv"
    if not force and output_path.exists():
        logger.info(
            "Step 3: reusing existing narratives.csv in this run directory (pass force=True to "
            "recompute): %s", output_path,
        )
        narratives_df = load_narratives(output_path)
        logger.info("Step 3 complete (reused).")
        return narratives_df

    if profiles_df is None:
        profiles_df = _get_or_build_profiles(config, logger)
    logger.info("Rendering narratives for %d variants", len(profiles_df))

    narratives_df = render_narratives(profiles_df, config, logger)
    top_narrative = narratives_df.iloc[0]["narrative"]
    logger.info(
        "Rendered %d narratives. Example (top variant): %s",
        len(narratives_df),
        top_narrative[:120],
    )

    save_narratives(narratives_df, output_path)
    logger.info("Saved narratives to: %s", output_path)

    logger.info("Step 3 complete.")
    log_peak_memory(logger, "Step 3")
    return narratives_df


def run_step4_sampling(
    config_path: str | Path | None = None,
    run_id: str | None = None,
    profiles_df: pd.DataFrame | None = None,
    narratives_df: pd.DataFrame | None = None,
    force: bool = False,
) -> pd.DataFrame:
    """Narrative sampling (pipeline Step 4): draw frequent/rare/extreme cases for calibration.

    force=False (default): reuses this run directory's narrative_sample.csv if it already exists,
    instead of recomputing — see run_step1_variants()'s docstring for why. Pass force=True to
    recompute on purpose.
    """
    config = load_config(config_path, run_id)
    logger = get_logger(config)

    logger.info("Step 4 (narrative sampling) started for log: %s", config.log_path)

    output_path = config.sampling_dir / "narrative_sample.csv"
    if not force and output_path.exists():
        logger.info(
            "Step 4: reusing existing narrative_sample.csv in this run directory (pass "
            "force=True to recompute): %s", output_path,
        )
        sample_df = load_narrative_sample(output_path)
        logger.info("Step 4 complete (reused).")
        return sample_df

    if profiles_df is None or narratives_df is None:
        profiles_df, narratives_df = _get_or_build_narratives(config, logger)

    sample_df = sample_narratives(profiles_df, narratives_df, config)
    logger.info(
        "Sampled %d unique variants (frequent=%d, rare=%d, extreme=%d per direction, before dedup)",
        len(sample_df),
        config.sample_frequent_n,
        config.sample_rare_n,
        config.sample_extreme_n,
    )

    save_narrative_sample(sample_df, output_path)
    logger.info("Saved narrative sample to: %s", output_path)

    logger.info("Step 4 complete.")
    log_peak_memory(logger, "Step 4")
    return sample_df


def run_step5a_taxonomy(
    config_path: str | Path | None = None,
    run_id: str | None = None,
    sample_df: pd.DataFrame | None = None,
    prior_taxonomy: Taxonomy | None = None,
    revision_instructions: str | None = None,
    round: int | None = None,
) -> Taxonomy:
    """Intent-guided taxonomy induction (pipeline Step 5a): subdivides the goal model's declared
    axis. prior_taxonomy/revision_instructions (Step 9's merge/split revision round): both set
    means this call revises an existing taxonomy instead of inducing fresh; both default to None
    for every other caller. round (also Step 9's revision round): which round's folder to write
    into — defaults to auto-detecting the current one (see load_config()).
    """
    config = load_config(config_path, run_id, round)
    logger = get_logger(config)

    logger.info("Step 5a (intent-guided taxonomy induction) started for log: %s", config.log_path)

    if sample_df is None:
        sample_df = _get_or_build_sample(config, logger)
    logger.info(
        "Inducing taxonomy from %d sampled narratives against goal model: %s",
        len(sample_df),
        config.goal_model_path,
    )

    taxonomy, metadata, prompt = induce_taxonomy_5a(
        sample_df, config, logger, prior_taxonomy=prior_taxonomy, revision_instructions=revision_instructions
    )
    logger.info(
        "Induced %d categories: %s",
        len(taxonomy.categories),
        ", ".join(c.category_id for c in taxonomy.categories),
    )

    goal_model_text = config.goal_model_path.read_text(encoding="utf-8")
    goal_model = grl.parse_jucm(goal_model_text)
    problems = check_taxonomy_grounding(taxonomy, sample_df, grl.declared_ids(goal_model), model=goal_model)
    for problem in problems:
        logger.warning("Taxonomy grounding check: %s", problem)
    if not problems:
        logger.info("Taxonomy grounding check: no problems found.")

    save_taxonomy(taxonomy, metadata, prompt, config.taxonomy_dir, config.llm.pricing_usd_per_million_tokens)
    logger.info("Saved taxonomy to: %s", config.taxonomy_dir / "taxonomy.json")

    logger.info("Step 5a complete.")
    log_peak_memory(logger, "Step 5a")
    return taxonomy


def run_step5b_taxonomy(
    config_path: str | Path | None = None,
    run_id: str | None = None,
    sample_df: pd.DataFrame | None = None,
    prior_taxonomy: Taxonomy | None = None,
    revision_instructions: str | None = None,
    round: int | None = None,
) -> Taxonomy:
    """Open taxonomy induction (pipeline Step 5b): proposes categories with no external axis.
    prior_taxonomy/revision_instructions/round: see run_step5a_taxonomy's docstring — same
    revision-round mechanism, minus the goal model.
    """
    config = load_config(config_path, run_id, round)
    logger = get_logger(config)

    logger.info("Step 5b (open taxonomy induction) started for log: %s", config.log_path)

    if sample_df is None:
        sample_df = _get_or_build_sample(config, logger)
    logger.info("Inducing taxonomy from %d sampled narratives (no goal model)", len(sample_df))

    taxonomy, metadata, prompt = induce_taxonomy_5b(
        sample_df, config, logger, prior_taxonomy=prior_taxonomy, revision_instructions=revision_instructions
    )
    logger.info(
        "Induced %d categories: %s",
        len(taxonomy.categories),
        ", ".join(c.category_id for c in taxonomy.categories),
    )

    problems = check_taxonomy_grounding(taxonomy, sample_df, None)
    for problem in problems:
        logger.warning("Taxonomy grounding check: %s", problem)
    if not problems:
        logger.info("Taxonomy grounding check: no problems found.")

    save_taxonomy(taxonomy, metadata, prompt, config.taxonomy_dir, config.llm.pricing_usd_per_million_tokens)
    logger.info("Saved taxonomy to: %s", config.taxonomy_dir / "taxonomy.json")

    logger.info("Step 5b complete.")
    log_peak_memory(logger, "Step 5b")
    return taxonomy


def run_step5_taxonomy(
    config_path: str | Path | None = None,
    run_id: str | None = None,
    sample_df: pd.DataFrame | None = None,
    prior_taxonomy: Taxonomy | None = None,
    revision_instructions: str | None = None,
    round: int | None = None,
) -> Taxonomy:
    """Dispatches to Step 5a or 5b per config.taxonomy_mode."""
    config = load_config(config_path, run_id, round)
    if config.taxonomy_mode == "intent_guided":
        return run_step5a_taxonomy(
            config_path, config.run_id, sample_df, prior_taxonomy, revision_instructions, config.round
        )
    if config.taxonomy_mode == "open":
        return run_step5b_taxonomy(
            config_path, config.run_id, sample_df, prior_taxonomy, revision_instructions, config.round
        )
    raise ValueError(f"Unknown taxonomy_mode={config.taxonomy_mode!r} (expected 'intent_guided' or 'open')")


def run_step6_assignment(
    config_path: str | Path | None = None,
    run_id: str | None = None,
    profiles_df: pd.DataFrame | None = None,
    narratives_df: pd.DataFrame | None = None,
    taxonomy: Taxonomy | None = None,
    round: int | None = None,
) -> pd.DataFrame:
    """Narrative assignment (pipeline Step 6): for every narrative, an LLM decides which
    taxonomy category (from Step 5a/5b) it realizes, if any.

    Unlike Steps 2-5, this does NOT compute a missing taxonomy from scratch: Step 5 is proven
    non-deterministic, so an implicit rebuild here could assign against a
    taxonomy nobody reviewed. A taxonomy must be passed in-memory, or run_id/round (arguments, or
    config.yaml's fields) must point at a round directory that already has a taxonomy.json.
    """
    config = load_config(config_path, run_id, round)
    logger = get_logger(config)

    logger.info("Step 6 (narrative assignment) started for log: %s", config.log_path)

    if profiles_df is None or narratives_df is None:
        profiles_df, narratives_df = _get_or_build_narratives(config, logger)

    if taxonomy is None:
        taxonomy_path = config.taxonomy_dir / "taxonomy.json"
        if not taxonomy_path.exists():
            raise ValueError(
                "run_step6_assignment() needs a taxonomy: pass taxonomy= directly, or point "
                "run_id/round (arguments, or config.yaml's fields) at a round directory that "
                f"already has a taxonomy.json in it (checked: {taxonomy_path})."
            )
        logger.info("Loading taxonomy from: %s", taxonomy_path)
        taxonomy = Taxonomy.model_validate_json(taxonomy_path.read_text(encoding="utf-8"))

    profile_columns = ["variant_id", "activity_sequence", "frequency", "frequency_pct", "duration_seconds_median", "outcome", "rework"]
    merged_df = profiles_df[profile_columns].merge(narratives_df, on="variant_id", how="inner")

    # The merge is inner, so a variant Step 3 produced no narrative for would not fail here — it
    # would silently never be offered to the LLM, never appear in assignments.csv, and surface
    # only at Step 9's completeness guard, after Steps 7/7b/8 had already run (and billed) on the
    # truncated partition. Checked before any LLM call rather than after.
    unnarrated_ids = set(profiles_df["variant_id"]) - set(merged_df["variant_id"])
    if unnarrated_ids:
        raise IncompleteAssignmentError(
            f"Step 6 cannot start: {len(unnarrated_ids)} profiled variant(s) have no narrative "
            f"from Step 3, so no LLM could ever assign them: {sorted(unnarrated_ids)}. Re-run "
            "Step 3 with force=True against this run_id to regenerate narratives.csv for every "
            "variant."
        )

    prior_assignments_df, prior_metadata_list = load_prior_assignments(config.assignment_dir)
    already_done_ids = set(prior_assignments_df["variant_id"])
    pending_df = merged_df[~merged_df["variant_id"].isin(already_done_ids)]
    if already_done_ids:
        logger.info(
            "Resuming run directory: %d/%d narratives already assigned, %d pending",
            len(already_done_ids), len(merged_df), len(pending_df),
        )

    batch_prompts: list[tuple[str, str, str]] = []
    new_metadata_list: list = []
    still_failed_ids: list[str] = []
    if len(pending_df) > 0:
        logger.info(
            "Assigning %d narratives against %d categories (model=%s, batch_size=%d, concurrency=%d)",
            len(pending_df),
            len(taxonomy.categories),
            config.llm.assignment_model,
            config.llm.assignment_batch_size,
            config.llm.concurrency,
        )
        new_assignments_df, new_metadata_list, batch_prompts, still_failed_ids = assign_narratives_6(
            pending_df, taxonomy, config, logger
        )
        assignments_df = pd.concat([prior_assignments_df, new_assignments_df], ignore_index=True)
    else:
        logger.info("Nothing pending — all narratives already assigned in this run directory.")
        assignments_df = prior_assignments_df

    metadata_list = prior_metadata_list + new_metadata_list

    assigned = assignments_df["category_id"].notna().sum()
    logger.info(
        "Assigned %d/%d narratives to a category, %d residual, %d still pending",
        assigned, len(assignments_df), len(assignments_df) - assigned, len(still_failed_ids),
    )
    if still_failed_ids:
        logger.warning(
            "%d narratives still pending after this attempt (API errors): %s — re-run against "
            "run_id=%s to retry just these.",
            len(still_failed_ids), still_failed_ids, config.run_id,
        )

    problems = check_assignment_grounding(assignments_df, taxonomy)
    for problem in problems:
        logger.warning("Assignment grounding check: %s", problem)
    if not problems:
        logger.info("Assignment grounding check: no problems found.")

    if config.skip_pairwise_distances:
        logger.info(
            "Skipping Step 6 pairwise structural/profile distances (skip_pairwise_distances=true) — "
            "assignment_report.md's cohesion/divergence sections and assignments.csv's nearest-neighbor "
            "columns will be empty for this round."
        )
        structural_df = empty_structural_distances()
        profile_df = empty_profile_distances()
    else:
        structural_df = compute_structural_distances(merged_df)
        profile_df = compute_profile_distances(merged_df)

    report_markdown = build_assignment_report(
        taxonomy, assignments_df, merged_df, structural_df, profile_df, config, still_failed_ids
    )
    save_assignment_outputs(
        assignments_df,
        metadata_list,
        batch_prompts,
        report_markdown,
        structural_df,
        profile_df,
        config.assignment_dir,
        config.llm.pricing_usd_per_million_tokens,
    )
    logger.info("Saved assignment outputs to: %s", config.assignment_dir)

    # Stop the run here rather than letting Steps 7, 7b and 8 compute (and, in Step 8's case, bill
    # LLM calls) on a partition that Step 9 is already guaranteed to refuse — goalcat.review's
    # finalize_run() rejects any round with a variant that has no Step 6 outcome. Raised *after*
    # save_assignment_outputs() on purpose: everything this attempt did assign is on disk, so
    # re-running Step 6 against the same run_id resumes from here and calls the LLM only for what
    # is still missing, rather than re-billing the whole step.
    if still_failed_ids:
        log_peak_memory(logger, "Step 6")
        raise IncompleteAssignmentError(
            f"Step 6 left {len(still_failed_ids)} narrative(s) with no outcome after "
            f"{config.llm.max_retries} attempts each — neither categorized nor residual: "
            f"{still_failed_ids}. The {len(assignments_df)} assignment(s) that did succeed are "
            f"saved in {config.assignment_dir}, so re-running Step 6 against run_id="
            f"{config.run_id} retries only these. Steps 7-9 are not run: Step 9 would refuse to "
            "accept this round anyway, and Step 8 would bill LLM calls for descriptions that a "
            "corrected assignment then invalidates."
        )

    logger.info("Step 6 complete.")
    log_peak_memory(logger, "Step 6")
    return assignments_df


def run_step7_discovery(
    config_path: str | Path | None = None,
    run_id: str | None = None,
    variants_df: pd.DataFrame | None = None,
    assignments_df: pd.DataFrame | None = None,
    taxonomy: Taxonomy | None = None,
    round: int | None = None,
) -> pd.DataFrame:
    """Per-category process discovery (pipeline Step 7): Inductive Miner + fitness/precision
    (token-based replay) on each categorized subset from Step 6.

    Like Step 6 with Step 5's taxonomy, this does NOT implicitly recompute a missing
    assignments_df/taxonomy from scratch: Step 6 is an LLM step, so an implicit rebuild here
    could silently re-run (and re-bill) it. Either pass both in-memory, or point run_id/round
    (arguments, or config.yaml's fields) at a round directory that already has assignments.csv
    and taxonomy.json.
    """
    config = load_config(config_path, run_id, round)
    logger = get_logger(config)

    logger.info("Step 7 (per-category discovery) started for log: %s", config.log_path)

    if variants_df is None:
        variants_df = _get_or_build_variants(config, logger)

    if assignments_df is None or taxonomy is None:
        assignments_path = config.assignment_dir / "assignments.csv"
        taxonomy_path = config.taxonomy_dir / "taxonomy.json"
        if not taxonomy_path.exists():
            # An accepted round has its taxonomy.json *moved* into final/ by review.py's
            # finalize_run() (models/ deleted at the same time) — discovery_report.md/
            # final/README.md both tell a reviewer to "re-run Step 7 against this round's
            # assignments.csv/taxonomy.json" to regenerate the deleted models, so that
            # instruction must keep working after acceptance, not just before it.
            final_taxonomy_path = config.final_dir / "taxonomy.json"
            if final_taxonomy_path.exists():
                taxonomy_path = final_taxonomy_path
        if not assignments_path.exists() or not taxonomy_path.exists():
            raise ValueError(
                "run_step7_discovery() needs assignments and a taxonomy: pass assignments_df= "
                "and taxonomy= directly, or point run_id/round (arguments, or config.yaml's "
                "fields) at a round directory that already has both assignments.csv and "
                f"taxonomy.json in it (checked: {assignments_path}, {taxonomy_path})."
            )
        logger.info("Loading assignments from: %s", assignments_path)
        assignments_df = pd.read_csv(assignments_path, dtype={"variant_id": str})
        logger.info("Loading taxonomy from: %s", taxonomy_path)
        taxonomy = Taxonomy.model_validate_json(taxonomy_path.read_text(encoding="utf-8"))

    # Same invariant Step 6 now enforces on its way out, re-checked on the way in because Step 7
    # is routinely invoked on its own — against a round directory written by an earlier, partial
    # Step 6, or with an assignments_df passed by a caller. Every metric this step reports (and
    # every description Step 8 writes from them) is computed per category, so an assignment that
    # covers only part of the log yields numbers that look complete and are not.
    unassigned_ids = set(variants_df["variant_id"]) - set(assignments_df["variant_id"])
    if unassigned_ids:
        raise IncompleteAssignmentError(
            f"Step 7 cannot run: {len(unassigned_ids)} variant(s) have no Step 6 outcome (neither "
            f"a category nor residual): {sorted(unassigned_ids)}. Re-run Step 6 against "
            f"run_id={config.run_id}, round {config.round} to retry them — it resumes, so only "
            "these are sent to the LLM. Per-category fitness/precision computed now would silently "
            "exclude them."
        )

    df = load_event_log(config)
    logger.info(
        "Discovering models for %d categories against %d events", len(taxonomy.categories), len(df)
    )

    metrics_df, models_by_category, dfgs_by_category = discover_all_categories(
        df, variants_df, assignments_df, taxonomy, config, logger
    )
    logger.info(
        "Discovered %d/%d category models (%d categories had no assigned variants)",
        len(models_by_category), len(taxonomy.categories), len(taxonomy.categories) - len(models_by_category),
    )

    save_discovery_outputs(
        metrics_df, models_by_category, dfgs_by_category, assignments_df, variants_df, taxonomy, config, config.discovery_dir
    )
    logger.info("Saved discovery outputs to: %s", config.discovery_dir)

    logger.info("Step 7 complete.")
    log_peak_memory(logger, "Step 7")
    return metrics_df


def run_step7b_indicators(
    config_path: str | Path | None = None,
    run_id: str | None = None,
    variants_df: pd.DataFrame | None = None,
    assignments_df: pd.DataFrame | None = None,
    taxonomy: Taxonomy | None = None,
    round: int | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Measured goal satisfaction per category (pipeline Step 7b): each goal-model indicator
    measured over each category's sublog, converted through its own `KPIEvalValueSet`, and
    propagated up the decomposition/contribution graph.

    Optional and deterministic — no LLM call, no alignment computation, and a silent no-op when the
    goal model declares no measurable indicator (every model except RTFM's today) or when
    `skip_indicators` is set. Reads the same assignments/taxonomy Step 7 does and, like Step 7,
    refuses to recompute them implicitly rather than risk silently re-running the LLM step that
    produced them.
    """
    config = load_config(config_path, run_id, round)
    logger = get_logger(config)

    logger.info("Step 7b (indicator satisfaction) started for log: %s", config.log_path)

    if config.skip_indicators:
        logger.info("skip_indicators is set — Step 7b skipped.")
        return pd.DataFrame(), pd.DataFrame()
    if config.goal_model_path is None:
        logger.info("No goal model configured — Step 7b has no indicators to measure, skipped.")
        return pd.DataFrame(), pd.DataFrame()

    if variants_df is None:
        variants_df = _get_or_build_variants(config, logger)

    if assignments_df is None or taxonomy is None:
        assignments_path = config.assignment_dir / "assignments.csv"
        taxonomy_path = config.taxonomy_dir / "taxonomy.json"
        if not taxonomy_path.exists() and (config.final_dir / "taxonomy.json").exists():
            taxonomy_path = config.final_dir / "taxonomy.json"
        if not assignments_path.exists() or not taxonomy_path.exists():
            raise ValueError(
                "run_step7b_indicators() needs assignments and a taxonomy: pass assignments_df= "
                "and taxonomy= directly, or point run_id/round (arguments, or config.yaml's "
                "fields) at a round directory that already has both assignments.csv and "
                f"taxonomy.json in it (checked: {assignments_path}, {taxonomy_path})."
            )
        logger.info("Loading assignments from: %s", assignments_path)
        assignments_df = pd.read_csv(assignments_path, dtype={"variant_id": str})
        logger.info("Loading taxonomy from: %s", taxonomy_path)
        taxonomy = Taxonomy.model_validate_json(taxonomy_path.read_text(encoding="utf-8"))

    model = grl.read_jucm(config.goal_model_path)
    df = load_event_log(config)

    indicator_df, goal_df = compute_indicator_satisfaction(
        df, variants_df, assignments_df, taxonomy, model, config, logger
    )
    if indicator_df.empty:
        logger.info("Step 7b complete (nothing measurable).")
        return indicator_df, goal_df

    report_markdown = build_indicator_report(indicator_df, goal_df, model)
    save_indicator_outputs(
        indicator_df, goal_df, report_markdown, config.goal_model_path, config.indicators_dir,
        f"{config.run_id} round{config.round}",
    )
    logger.info("Saved indicator outputs to: %s", config.indicators_dir)

    logger.info("Step 7b complete.")
    log_peak_memory(logger, "Step 7b")
    return indicator_df, goal_df


def run_step8_description(
    config_path: str | Path | None = None,
    run_id: str | None = None,
    variants_df: pd.DataFrame | None = None,
    assignments_df: pd.DataFrame | None = None,
    taxonomy: Taxonomy | None = None,
    metrics_df: pd.DataFrame | None = None,
    round: int | None = None,
) -> pd.DataFrame:
    """High-level description generation (pipeline Step 8): a deterministic discovered_pattern/
    model_looseness per category (pure functions of numbers Steps 2/7 already computed, no LLM),
    plus one batched LLM call judging goal_alignment against each category's real goal-model
    linkage (or Step 5's own description/rationale, in open mode).

    Like Step 7 with Step 6's taxonomy, this does NOT implicitly recompute a missing
    assignments_df/taxonomy/metrics_df from scratch: Step 6 is an LLM step and Step 7 discovers
    real process models, so an implicit rebuild here could silently re-run (and re-bill/
    re-discover) either. Either pass all three in-memory, or point run_id/round (arguments, or
    config.yaml's fields) at a round directory that already has assignments.csv, taxonomy.json,
    and discovery_metrics.csv.
    """
    config = load_config(config_path, run_id, round)
    logger = get_logger(config)

    logger.info("Step 8 (high-level description generation) started for log: %s", config.log_path)

    if variants_df is None:
        variants_df = _get_or_build_variants(config, logger)

    if assignments_df is None or taxonomy is None or metrics_df is None:
        assignments_path = config.assignment_dir / "assignments.csv"
        taxonomy_path = config.taxonomy_dir / "taxonomy.json"
        metrics_path = config.discovery_dir / "discovery_metrics.csv"
        if not assignments_path.exists() or not taxonomy_path.exists() or not metrics_path.exists():
            raise ValueError(
                "run_step8_description() needs assignments, a taxonomy, and discovery metrics: "
                "pass assignments_df=, taxonomy=, and metrics_df= directly, or point run_id/round "
                "(arguments, or config.yaml's fields) at a round directory that already has "
                f"all three (checked: {assignments_path}, {taxonomy_path}, {metrics_path})."
            )
        logger.info("Loading assignments from: %s", assignments_path)
        assignments_df = pd.read_csv(assignments_path, dtype={"variant_id": str})
        logger.info("Loading taxonomy from: %s", taxonomy_path)
        taxonomy = Taxonomy.model_validate_json(taxonomy_path.read_text(encoding="utf-8"))
        logger.info("Loading discovery metrics from: %s", metrics_path)
        metrics_df = pd.read_csv(metrics_path)

    df = load_event_log(config)
    logger.info("Generating descriptions for %d categories against %d events", len(taxonomy.categories), len(df))

    # Step 7b is optional, so its output is picked up if present and simply absent otherwise -- in
    # which case build_goal_alignment_prompt() renders exactly the prompt it rendered before Step 7b
    # existed. Not recomputed here: it is a separate step with its own outputs, and silently
    # re-running it would re-measure the whole log inside what is meant to be one LLM call.
    indicator_df = None
    indicator_path = config.indicators_dir / "indicator_satisfaction.csv"
    if indicator_path.exists():
        logger.info("Loading Step 7b indicator satisfaction from: %s", indicator_path)
        indicator_df = pd.read_csv(indicator_path)

    descriptions_df, metadata, prompt = generate_descriptions_8(
        df, variants_df, assignments_df, metrics_df, taxonomy, config, logger, indicator_df
    )
    logger.info("Generated %d/%d category descriptions", len(descriptions_df), len(taxonomy.categories))

    report_markdown = build_description_report(taxonomy, descriptions_df, metrics_df, config)
    save_description_outputs(
        descriptions_df, metadata, prompt, report_markdown, config.description_dir, config.llm.pricing_usd_per_million_tokens
    )
    logger.info("Saved description outputs to: %s", config.description_dir)

    logger.info("Step 8 complete.")
    log_peak_memory(logger, "Step 8")
    return descriptions_df


def run_step9_review(
    config_path: str | Path | None = None, run_id: str | None = None, round: int | None = None
) -> dict:
    """Business review (pipeline Step 9): file-based, not a UI — a human reads the single
    execution-level review_index.md/the current round's Step 6-8 reports, then records
    accept/rename/merge/split in that round's review_decisions.yaml. Re-invoking this against the
    same run_id processes whatever decision is there: accept finalizes (final/ + round_info.json
    status), a rename applies in place (no LLM call), a merge/split starts a new round (a fresh
    LLM-driven taxonomy revision nested under round{N+1}/, then Steps 6-8 re-run under it). See
    review.py for the full mechanism.

    Same not-implicitly-recomputed contract as Steps 6-8: needs an existing taxonomy.json and
    assignments.csv in the current round's directory (raises ValueError naming what's missing
    otherwise).
    """
    config = load_config(config_path, run_id, round)
    logger = get_logger(config)

    logger.info("Step 9 (business review) started for log: %s", config.log_path)
    result = process_review(config_path, config, logger)
    logger.info("Step 9 result: %s", result)

    return result

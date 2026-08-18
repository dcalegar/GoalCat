from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from .config import PipelineConfig, load_config, new_run_id
from .discovery import discover_all_categories, save_discovery_outputs
from .extraction.log_io import load_event_log
from .extraction.profiling import load_profiles, profile_variants, save_profiles
from .extraction.similarity import compute_profile_distances, compute_structural_distances
from .extraction.variants import extract_variants, load_variants, save_variants
from .llm.assignment import (
    assign_narratives_6,
    build_assignment_report,
    check_assignment_grounding,
    load_prior_assignments,
    save_assignment_outputs,
)
from .llm.taxonomy import (
    Taxonomy,
    _extract_declared_ids,
    check_taxonomy_grounding,
    induce_taxonomy_5a,
    induce_taxonomy_5b,
    save_taxonomy,
)
from .narrative.sampling import load_narrative_sample, sample_narratives, save_narrative_sample
from .narrative.textualization import load_narratives, render_narratives, save_narratives
from .run_logging import get_logger


def _get_or_build_variants(config: PipelineConfig, logger: logging.Logger) -> pd.DataFrame:
    """Loads variants.csv from config.run_output_dir if it's already there (a reused run
    directory), else computes it from the raw log and saves it. Shared by every step whose
    input, not primary output, is the variants table."""
    path = config.run_output_dir / "variants.csv"
    if path.exists():
        logger.info("Loading variants from existing run directory: %s", path)
        return load_variants(path)
    df = load_event_log(config)
    variants_df = extract_variants(df, config)
    save_variants(variants_df, path)
    return variants_df


def _get_or_build_profiles(config: PipelineConfig, logger: logging.Logger) -> pd.DataFrame:
    csv_path = config.run_output_dir / "profiles.csv"
    json_path = config.run_output_dir / "profiles.json"
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
    profiles_csv = config.run_output_dir / "profiles.csv"
    profiles_json = config.run_output_dir / "profiles.json"
    narratives_csv = config.run_output_dir / "narratives.csv"
    if profiles_csv.exists() and profiles_json.exists() and narratives_csv.exists():
        logger.info("Loading profiles/narratives from existing run directory: %s", config.run_output_dir)
        return load_profiles(profiles_csv, profiles_json), load_narratives(narratives_csv)
    profiles_df = _get_or_build_profiles(config, logger)
    narratives_df = render_narratives(profiles_df, config, logger)
    save_narratives(narratives_df, narratives_csv)
    return profiles_df, narratives_df


def _get_or_build_sample(config: PipelineConfig, logger: logging.Logger) -> pd.DataFrame:
    path = config.run_output_dir / "narrative_sample.csv"
    if path.exists():
        logger.info("Loading narrative sample from existing run directory: %s", path)
        return load_narrative_sample(path)
    profiles_df, narratives_df = _get_or_build_narratives(config, logger)
    sample_df = sample_narratives(profiles_df, narratives_df, config)
    save_narrative_sample(sample_df, path)
    return sample_df


def run_step1_variants(config_path: str | Path | None = None, run_id: str | None = None) -> pd.DataFrame:
    """Variant extraction (pipeline Step 1): load the log, group traces by activity sequence."""
    config = load_config(config_path, run_id)
    logger = get_logger(config)

    logger.info("Step 1 (variant extraction) started for log: %s", config.log_path)

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

    output_path = config.run_output_dir / "variants.csv"
    save_variants(variants_df, output_path)
    logger.info("Saved variants to: %s", output_path)

    logger.info("Step 1 complete.")
    return variants_df


def run_step2_profiling(
    config_path: str | Path | None = None,
    run_id: str | None = None,
    variants_df: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Multi-view profiling (pipeline Step 2): duration, rework, outcome, resource per variant."""
    config = load_config(config_path, run_id)
    logger = get_logger(config)

    logger.info("Step 2 (multi-view profiling) started for log: %s", config.log_path)

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

    csv_path = config.run_output_dir / "profiles.csv"
    json_path = config.run_output_dir / "profiles.json"
    save_profiles(profiles_df, csv_path, json_path)
    logger.info("Saved profiles to: %s and %s", csv_path, json_path)

    logger.info("Step 2 complete.")
    return profiles_df


def run_step3_textualization(
    config_path: str | Path | None = None,
    run_id: str | None = None,
    profiles_df: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Textualization (pipeline Step 3): render each variant's profile as a narrative via LUPIN."""
    config = load_config(config_path, run_id)
    logger = get_logger(config)

    logger.info("Step 3 (textualization) started for log: %s", config.log_path)

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

    output_path = config.run_output_dir / "narratives.csv"
    save_narratives(narratives_df, output_path)
    logger.info("Saved narratives to: %s", output_path)

    logger.info("Step 3 complete.")
    return narratives_df


def run_step4_sampling(
    config_path: str | Path | None = None,
    run_id: str | None = None,
    profiles_df: pd.DataFrame | None = None,
    narratives_df: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Narrative sampling (pipeline Step 4): draw frequent/rare/extreme cases for calibration."""
    config = load_config(config_path, run_id)
    logger = get_logger(config)

    logger.info("Step 4 (narrative sampling) started for log: %s", config.log_path)

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

    output_path = config.run_output_dir / "narrative_sample.csv"
    save_narrative_sample(sample_df, output_path)
    logger.info("Saved narrative sample to: %s", output_path)

    logger.info("Step 4 complete.")
    return sample_df


def run_step5a_taxonomy(
    config_path: str | Path | None = None,
    run_id: str | None = None,
    sample_df: pd.DataFrame | None = None,
) -> Taxonomy:
    """Intent-guided taxonomy induction (pipeline Step 5a): subdivides the goal model's declared axis."""
    config = load_config(config_path, run_id)
    logger = get_logger(config)

    logger.info("Step 5a (intent-guided taxonomy induction) started for log: %s", config.log_path)

    if sample_df is None:
        sample_df = _get_or_build_sample(config, logger)
    logger.info(
        "Inducing taxonomy from %d sampled narratives against goal model: %s",
        len(sample_df),
        config.goal_model_path,
    )

    taxonomy, metadata, prompt = induce_taxonomy_5a(sample_df, config, logger)
    logger.info(
        "Induced %d categories: %s",
        len(taxonomy.categories),
        ", ".join(c.category_id for c in taxonomy.categories),
    )

    goal_model_text = config.goal_model_path.read_text(encoding="utf-8")
    problems = check_taxonomy_grounding(taxonomy, sample_df, _extract_declared_ids(goal_model_text))
    for problem in problems:
        logger.warning("Taxonomy grounding check: %s", problem)
    if not problems:
        logger.info("Taxonomy grounding check: no problems found.")

    save_taxonomy(taxonomy, metadata, prompt, config.run_output_dir)
    logger.info("Saved taxonomy to: %s", config.run_output_dir / "taxonomy.json")

    logger.info("Step 5a complete.")
    return taxonomy


def run_step5b_taxonomy(
    config_path: str | Path | None = None,
    run_id: str | None = None,
    sample_df: pd.DataFrame | None = None,
) -> Taxonomy:
    """Open taxonomy induction (pipeline Step 5b): proposes categories with no external axis."""
    config = load_config(config_path, run_id)
    logger = get_logger(config)

    logger.info("Step 5b (open taxonomy induction) started for log: %s", config.log_path)

    if sample_df is None:
        sample_df = _get_or_build_sample(config, logger)
    logger.info("Inducing taxonomy from %d sampled narratives (no goal model)", len(sample_df))

    taxonomy, metadata, prompt = induce_taxonomy_5b(sample_df, config, logger)
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

    save_taxonomy(taxonomy, metadata, prompt, config.run_output_dir)
    logger.info("Saved taxonomy to: %s", config.run_output_dir / "taxonomy.json")

    logger.info("Step 5b complete.")
    return taxonomy


def run_step5_taxonomy(
    config_path: str | Path | None = None,
    run_id: str | None = None,
    sample_df: pd.DataFrame | None = None,
) -> Taxonomy:
    """Dispatches to Step 5a or 5b per config.taxonomy_mode."""
    config = load_config(config_path, run_id)
    if config.taxonomy_mode == "intent_guided":
        return run_step5a_taxonomy(config_path, config.run_id, sample_df)
    if config.taxonomy_mode == "open":
        return run_step5b_taxonomy(config_path, config.run_id, sample_df)
    raise ValueError(f"Unknown taxonomy_mode={config.taxonomy_mode!r} (expected 'intent_guided' or 'open')")


def run_step6_assignment(
    config_path: str | Path | None = None,
    run_id: str | None = None,
    profiles_df: pd.DataFrame | None = None,
    narratives_df: pd.DataFrame | None = None,
    taxonomy: Taxonomy | None = None,
) -> pd.DataFrame:
    """Narrative assignment (pipeline Step 6): for every narrative, an LLM decides which
    taxonomy category (from Step 5a/5b) it realizes, if any.

    Unlike Steps 2-5, this does NOT compute a missing taxonomy from scratch: Step 5 is proven
    non-deterministic (see PROGRESS.md), so an implicit rebuild here could assign against a
    taxonomy nobody reviewed. A taxonomy must be passed in-memory, or run_id (argument or
    config.yaml's run_id field) must point at a run directory that already has a taxonomy.json.
    """
    config = load_config(config_path, run_id)
    logger = get_logger(config)

    logger.info("Step 6 (narrative assignment) started for log: %s", config.log_path)

    if profiles_df is None or narratives_df is None:
        profiles_df, narratives_df = _get_or_build_narratives(config, logger)

    if taxonomy is None:
        taxonomy_path = config.run_output_dir / "taxonomy.json"
        if not taxonomy_path.exists():
            raise ValueError(
                "run_step6_assignment() needs a taxonomy: pass taxonomy= directly, or point "
                "run_id (argument, or config.yaml's run_id field) at a run directory that "
                f"already has a taxonomy.json in it (checked: {taxonomy_path})."
            )
        logger.info("Loading taxonomy from: %s", taxonomy_path)
        taxonomy = Taxonomy.model_validate_json(taxonomy_path.read_text(encoding="utf-8"))

    profile_columns = ["variant_id", "activity_sequence", "frequency", "frequency_pct", "duration_seconds_median", "outcome", "rework"]
    merged_df = profiles_df[profile_columns].merge(narratives_df, on="variant_id", how="inner")

    prior_assignments_df, prior_metadata_list = load_prior_assignments(config.run_output_dir)
    already_done_ids = set(prior_assignments_df["variant_id"])
    pending_df = merged_df[~merged_df["variant_id"].isin(already_done_ids)]
    if already_done_ids:
        logger.info(
            "Resuming run directory: %d/%d narratives already assigned, %d pending",
            len(already_done_ids), len(merged_df), len(pending_df),
        )

    example_prompt = None
    new_metadata_list: list = []
    still_failed_ids: list[str] = []
    if len(pending_df) > 0:
        logger.info(
            "Assigning %d narratives against %d categories (model=%s, concurrency=%d)",
            len(pending_df),
            len(taxonomy.categories),
            config.llm.assignment_model,
            config.llm.concurrency,
        )
        new_assignments_df, new_metadata_list, example_prompt, still_failed_ids = assign_narratives_6(
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

    structural_df = compute_structural_distances(merged_df)
    profile_df = compute_profile_distances(merged_df)

    report_markdown = build_assignment_report(
        taxonomy, assignments_df, merged_df, structural_df, profile_df, config, still_failed_ids
    )
    save_assignment_outputs(
        assignments_df, metadata_list, example_prompt, report_markdown, structural_df, profile_df, config.run_output_dir
    )
    logger.info("Saved assignment outputs to: %s", config.run_output_dir)

    logger.info("Step 6 complete.")
    return assignments_df


def run_step7_discovery(
    config_path: str | Path | None = None,
    run_id: str | None = None,
    variants_df: pd.DataFrame | None = None,
    assignments_df: pd.DataFrame | None = None,
    taxonomy: Taxonomy | None = None,
) -> pd.DataFrame:
    """Per-category process discovery (pipeline Step 7): Inductive Miner + fitness/precision
    (token-based replay) on each categorized subset from Step 6.

    Like Step 6 with Step 5's taxonomy, this does NOT implicitly recompute a missing
    assignments_df/taxonomy from scratch: Step 6 is an LLM step, so an implicit rebuild here
    could silently re-run (and re-bill) it. Either pass both in-memory, or point run_id (argument
    or config.yaml's run_id field) at a run directory that already has assignments.csv and
    taxonomy.json.
    """
    config = load_config(config_path, run_id)
    logger = get_logger(config)

    logger.info("Step 7 (per-category discovery) started for log: %s", config.log_path)

    if variants_df is None:
        variants_df = _get_or_build_variants(config, logger)

    if assignments_df is None or taxonomy is None:
        assignments_path = config.run_output_dir / "assignments.csv"
        taxonomy_path = config.run_output_dir / "taxonomy.json"
        if not assignments_path.exists() or not taxonomy_path.exists():
            raise ValueError(
                "run_step7_discovery() needs assignments and a taxonomy: pass assignments_df= "
                "and taxonomy= directly, or point run_id (argument, or config.yaml's run_id "
                "field) at a run directory that already has both assignments.csv and "
                f"taxonomy.json in it (checked: {assignments_path}, {taxonomy_path})."
            )
        logger.info("Loading assignments from: %s", assignments_path)
        assignments_df = pd.read_csv(assignments_path, dtype={"variant_id": str})
        logger.info("Loading taxonomy from: %s", taxonomy_path)
        taxonomy = Taxonomy.model_validate_json(taxonomy_path.read_text(encoding="utf-8"))

    df = load_event_log(config)
    logger.info(
        "Discovering models for %d categories against %d events", len(taxonomy.categories), len(df)
    )

    metrics_df, models_by_category = discover_all_categories(df, variants_df, assignments_df, taxonomy, config, logger)
    logger.info(
        "Discovered %d/%d category models (%d categories had no assigned variants)",
        len(models_by_category), len(taxonomy.categories), len(taxonomy.categories) - len(models_by_category),
    )

    save_discovery_outputs(metrics_df, models_by_category, assignments_df, variants_df, taxonomy, config, config.run_output_dir)
    logger.info("Saved discovery outputs to: %s", config.run_output_dir)

    logger.info("Step 7 complete.")
    return metrics_df


if __name__ == "__main__":
    # Steps 1-4 only: Step 5a/5b/6 require an LLM API key and make real (if cheap) network
    # calls, so they stay explicitly invoked rather than chained here. One run_id generated up
    # front so all four steps share the same run directory.
    run_id = new_run_id()
    variants_df = run_step1_variants(run_id=run_id)
    profiles_df = run_step2_profiling(run_id=run_id, variants_df=variants_df)
    narratives_df = run_step3_textualization(run_id=run_id, profiles_df=profiles_df)
    run_step4_sampling(run_id=run_id, profiles_df=profiles_df, narratives_df=narratives_df)

from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from pathlib import Path

import pandas as pd
import pm4py
from pm4py.objects.petri_net.obj import Marking, PetriNet

from .atomic_io import atomic_output_path, atomic_write_csv, atomic_write_text
from .config import PipelineConfig
from .llm.taxonomy import Taxonomy


def build_category_sublogs(
    df: pd.DataFrame, variants_df: pd.DataFrame, assignments_df: pd.DataFrame, config: PipelineConfig
) -> dict[str, pd.DataFrame]:
    """Filters the raw event log into one sub-DataFrame per category, via variant_id -> case_ids
    (variants_df) joined against variant_id -> category_id (assignments_df). Residual rows
    (category_id is NA) are excluded — pd.notna(), not `is None`, per the pandas-3 string-dtype
    convention already established in llm/assignment.py. A category with zero assigned variants
    has no entry in the returned dict; the caller is responsible for reporting that explicitly
    rather than treating a missing key as an error.
    """
    merged = variants_df[["variant_id", "case_ids"]].merge(
        assignments_df[["variant_id", "category_id"]], on="variant_id", how="inner"
    )
    merged = merged[merged["category_id"].notna()]

    case_ids_by_category: dict[str, set[str]] = {}
    for category_id, case_ids in zip(merged["category_id"], merged["case_ids"]):
        case_ids_by_category.setdefault(category_id, set()).update(case_ids)

    return {
        category_id: _sorted_sublog(df[df[config.case_id_key].isin(case_ids)], config)
        for category_id, case_ids in case_ids_by_category.items()
    }


def _sorted_sublog(sub_df: pd.DataFrame, config: PipelineConfig) -> pd.DataFrame:
    """Orders a sublog by (case_id, timestamp) before it reaches any pm4py discovery/conformance
    call. extraction/variants.py derives GoalCat's own variant_id via
    pm4py.split_by_process_variant(..., timestamp_key=...), which sorts by timestamp per case —
    but pm4py.fitness_token_based_replay/precision_token_based_replay (used by
    compute_conformance below) derive each case's replayed sequence from plain DataFrame row
    order (pandas_utils.get_traces() -> groupby(case_id_key)[activity_key].agg(list), no
    timestamp_key parameter at all). Without this sort, a sub_df whose rows aren't already
    strictly (case_id, timestamp)-ordered — e.g. BPIC 2019, whose coarse timestamps leave many
    same-instant events in file order — makes token-based replay see far more distinct sequences
    than GoalCat's own variant count (observed: pm4py's internal variant tally for one BPIC 2019
    category came out close to its raw case count, ~14x its true ~6k variant count), which is
    both a correctness risk (replaying a case's events out of chronological order against a
    model built from the properly-ordered sequence) and the direct cause of a replay slowdown
    severe enough to make Step 7 impractical at that scale. kind="stable" (mergesort) matches
    extraction/variants.py's own tie-breaking rationale — same-timestamp events keep their
    original relative order instead of an arbitrary one that could drift between runs."""
    return sub_df.sort_values([config.case_id_key, config.timestamp_key], kind="stable")


def build_residual_sublog(
    df: pd.DataFrame, variants_df: pd.DataFrame, assignments_df: pd.DataFrame, config: PipelineConfig
) -> pd.DataFrame:
    """The mirror image of build_category_sublogs: raw events for variants left unassigned
    (category_id is NA). Used by Step 9's accept/finalize path (review.py) to persist the
    residual as its own partitioned-log file, matching how every other report already reports
    it for context rather than treating it as silently absent."""
    merged = variants_df[["variant_id", "case_ids"]].merge(
        assignments_df[["variant_id", "category_id"]], on="variant_id", how="inner"
    )
    merged = merged[merged["category_id"].isna()]

    case_ids: set[str] = set()
    for ids in merged["case_ids"]:
        case_ids.update(ids)

    return _sorted_sublog(df[df[config.case_id_key].isin(case_ids)], config)


def discover_category_model(sub_df: pd.DataFrame, config: PipelineConfig) -> tuple[PetriNet, Marking, Marking]:
    """Inductive Miner over one category's sub-log. noise_threshold is fixed across every
    category via config.discovery_noise_threshold, per OVERVIEW.md's "fixed hyperparameters
    across categories" requirement — never tuned per category."""
    return pm4py.discover_petri_net_inductive(
        sub_df,
        noise_threshold=config.discovery_noise_threshold,
        activity_key=config.activity_key,
        timestamp_key=config.timestamp_key,
        case_id_key=config.case_id_key,
    )


def discover_category_dfg(sub_df: pd.DataFrame, config: PipelineConfig) -> tuple[dict, dict, dict]:
    """Directly-Follows Graph over one category's sub-log, used only for the rendered artifact
    (models/{category_id}.png). Conformance (fitness/precision) still comes from the Petri net
    discovered by discover_category_model — DFG-based conformance in pm4py lacks the token-based
    replay semantics those metrics rely on."""
    return pm4py.discover_dfg(
        sub_df,
        activity_key=config.activity_key,
        timestamp_key=config.timestamp_key,
        case_id_key=config.case_id_key,
    )


def compute_conformance(
    sub_df: pd.DataFrame,
    net: PetriNet,
    im: Marking,
    fm: Marking,
    config: PipelineConfig,
    logger: logging.Logger,
    category_id: str = "",
) -> dict:
    """Fitness and precision via token-based replay — the standard pairing with Inductive Miner,
    fast enough for both RTFM's largest category (111 variants) and smallest (1 variant, 30.8%
    of cases); see PROGRESS.md for why alignments were considered and not chosen.

    Precision (ET-Conformance) replays every distinct *prefix* in the category's sublog, not
    every distinct trace — a category with heavy internal behavioral diversity can have far more
    unique prefixes than variants (observed on BPIC 2019: one category's 6,082 variants produced
    88,241 unique prefixes), and each prefix replay's cost itself grows with how many invisible
    transitions the discovered net has (more of them on a noise_threshold=0.0 model of a diverse
    category), which a benchmark here confirmed doesn't parallelize under pm4py's own optional
    threading (~26s vs ~28s on a 500-variant slice — Python's GIL leaves pure-Python replay
    effectively single-threaded regardless). Not a bug, not fixable by more cores; genuinely
    expensive at that scale. config.discovery_precision_timeout_seconds (None = no timeout, the
    default) bounds the wait: on timeout, precision is reported as NaN rather than blocking the
    rest of Step 7 indefinitely — the orphaned replay thread keeps running to completion in the
    background (Python threads can't be killed cleanly), but this function stops waiting on it.

    config.skip_precision (default False) bypasses the replay call entirely and reports NaN
    unconditionally, reusing this same NaN path — an opt-in, human-decided tradeoff (see README's
    Resource usage section) for when Step 7's single-threaded replay cost isn't worth paying at
    all, not just bounding how long it's allowed to run.
    """
    fitness = pm4py.fitness_token_based_replay(
        sub_df, net, im, fm,
        activity_key=config.activity_key, timestamp_key=config.timestamp_key, case_id_key=config.case_id_key,
    )

    if config.skip_precision:
        precision = float("nan")
    else:
        timeout = config.discovery_precision_timeout_seconds
        if timeout is None:
            precision = pm4py.precision_token_based_replay(
                sub_df, net, im, fm,
                activity_key=config.activity_key, timestamp_key=config.timestamp_key, case_id_key=config.case_id_key,
            )
        else:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(
                    pm4py.precision_token_based_replay,
                    sub_df, net, im, fm,
                    activity_key=config.activity_key, timestamp_key=config.timestamp_key, case_id_key=config.case_id_key,
                )
                try:
                    precision = future.result(timeout=timeout)
                except FutureTimeoutError:
                    logger.warning(
                        "Precision computation for category %s exceeded discovery_precision_timeout_seconds=%s — "
                        "reporting precision=NaN. The replay keeps running in an orphaned background thread "
                        "(Python threads can't be cancelled) but this run no longer waits on it.",
                        category_id, timeout,
                    )
                    precision = float("nan")

    return {
        "perc_fit_traces": fitness["perc_fit_traces"],
        "average_trace_fitness": fitness["average_trace_fitness"],
        "log_fitness": fitness["log_fitness"],
        "precision": precision,
    }


def discover_all_categories(
    df: pd.DataFrame,
    variants_df: pd.DataFrame,
    assignments_df: pd.DataFrame,
    taxonomy: Taxonomy,
    config: PipelineConfig,
    logger: logging.Logger,
) -> tuple[pd.DataFrame, dict[str, tuple[PetriNet, Marking, Marking]], dict[str, tuple[dict, dict, dict]]]:
    """Discovers one model per taxonomy category (pipeline Step 7). Iterates taxonomy.categories
    in taxonomy order, not just categories that happen to appear in assignments_df, so a category
    with zero assigned variants is reported as 0/0 explicitly rather than silently absent —
    mirrors llm/assignment.py's build_assignment_report. The residual (category_id is NA) is not
    discovered at all: OVERVIEW.md's output is "one process model per category" and the residual
    isn't a category.

    Returns the Petri net (used for conformance and .pnml export) alongside a DFG per category
    (used only for the rendered .png artifact — DFGs are easier to read than Petri nets for this
    project's audience, per user preference).
    """
    sublogs = build_category_sublogs(df, variants_df, assignments_df, config)
    category_of = dict(zip(assignments_df["variant_id"], assignments_df["category_id"]))
    freq_by_variant = dict(zip(variants_df["variant_id"], variants_df["frequency"]))

    rows = []
    models_by_category: dict[str, tuple[PetriNet, Marking, Marking]] = {}
    dfgs_by_category: dict[str, tuple[dict, dict, dict]] = {}
    for category in taxonomy.categories:
        assigned_variant_ids = [vid for vid, cat in category_of.items() if cat == category.category_id]
        num_variants = len(assigned_variant_ids)
        num_cases = sum(freq_by_variant.get(vid, 0) for vid in assigned_variant_ids)

        if num_variants == 0:
            logger.warning("Category %s has no assigned variants — skipping discovery.", category.category_id)
            rows.append(
                {
                    "category_id": category.category_id,
                    "name": category.name,
                    "num_variants": 0,
                    "num_cases": 0,
                    "perc_fit_traces": float("nan"),
                    "average_trace_fitness": float("nan"),
                    "log_fitness": float("nan"),
                    "precision": float("nan"),
                }
            )
            continue

        sub_df = sublogs[category.category_id]
        net, im, fm = discover_category_model(sub_df, config)
        conformance = compute_conformance(sub_df, net, im, fm, config, logger, category.category_id)
        models_by_category[category.category_id] = (net, im, fm)
        dfgs_by_category[category.category_id] = discover_category_dfg(sub_df, config)
        rows.append(
            {"category_id": category.category_id, "name": category.name, "num_variants": num_variants, "num_cases": num_cases, **conformance}
        )
        logger.info(
            "Discovered model for %s: %d variants, %d cases, log_fitness=%.3f, precision=%.3f",
            category.category_id, num_variants, num_cases, conformance["log_fitness"], conformance["precision"],
        )

    metrics_df = pd.DataFrame(
        rows,
        columns=["category_id", "name", "num_variants", "num_cases", "perc_fit_traces", "average_trace_fitness", "log_fitness", "precision"],
    )
    return metrics_df, models_by_category, dfgs_by_category


def flag_low_precision_categories(metrics_df: pd.DataFrame, threshold: float) -> list[dict]:
    """Categories whose Step 7 precision falls below threshold — advisory only, consumed by Step
    9's write_review_template() to surface a heuristic signal in review_decisions.yaml, never
    applied automatically. Under a fitness-preserving discovery method (Inductive Miner,
    noise_threshold fixed via config.discovery_noise_threshold), a category whose sublog
    conflates distinct behavioral patterns doesn't show up as unfit — the model just stays
    permissive enough to replay everything in it — it shows up as low precision instead. Skips
    categories with 0 assigned variants (precision is NaN there by construction, see
    discover_all_categories)."""
    flagged = []
    for _, row in metrics_df.iterrows():
        if row["num_variants"] == 0 or pd.isna(row["precision"]):
            continue
        if row["precision"] < threshold:
            flagged.append(
                {
                    "category_id": row["category_id"],
                    "name": row["name"],
                    "precision": row["precision"],
                    "log_fitness": row["log_fitness"],
                }
            )
    return flagged


def build_discovery_report(
    metrics_df: pd.DataFrame,
    assignments_df: pd.DataFrame,
    variants_df: pd.DataFrame,
    taxonomy: Taxonomy,
    config: PipelineConfig,
    models_present: bool = True,
) -> str:
    """The Markdown explainability artifact for Step 7, in the same style as
    llm/assignment.py's build_assignment_report: per-category coverage and conformance, plus a
    residual line for context (no model attempted for it).

    models_present=False (set only when Step 9's finalize_run() re-renders this report after
    deleting the accepted round's models/ folder, per user direction — the rendered .pnml/.png
    aren't kept once a run is accepted, since the data to regenerate them stays in this round's
    own assignments.csv/taxonomy.json) swaps the "Model:" line for a note instead of a now-dead
    link.
    """
    metrics_by_category = metrics_df.set_index("category_id").to_dict(orient="index")
    freq_by_variant = dict(zip(variants_df["variant_id"], variants_df["frequency"]))
    category_of = dict(zip(assignments_df["variant_id"], assignments_df["category_id"]))

    total_variants = len(assignments_df)
    total_cases = sum(freq_by_variant.get(vid, 0) for vid in category_of)
    residual_ids = [vid for vid, cat in category_of.items() if pd.isna(cat)]
    residual_cases = sum(freq_by_variant.get(vid, 0) for vid in residual_ids)

    lines = [
        "# Step 7 — Per-category process discovery report",
        "",
        f"Run: `{config.run_id}` | Log: `{config.log_stem}` | "
        f"Inductive Miner noise_threshold: `{config.discovery_noise_threshold}`",
        "",
        f"{len(taxonomy.categories)} categories. Residual (no discovery attempted): "
        f"{len(residual_ids)}/{total_variants} variants, {residual_cases}/{total_cases} cases.",
        "",
    ]
    if config.skip_precision:
        lines += [
            "**Precision skipped** (`skip_precision=true`): every category's precision below is "
            "`NaN` by config, not because it timed out or genuinely came out undefined. Fitness "
            "is still computed.",
            "",
        ]

    for category in taxonomy.categories:
        stats = metrics_by_category.get(category.category_id, {})
        num_variants = stats.get("num_variants", 0)
        num_cases = stats.get("num_cases", 0)
        lines += [
            f"## {category.name} (`{category.category_id}`)",
            "",
            category.description,
            "",
            f"**Coverage:** {num_variants} variants, {num_cases} cases.",
            "",
        ]
        if num_variants == 0:
            lines += ["No variants assigned — discovery skipped.", ""]
            continue
        precision_display = "skipped (`skip_precision=true`)" if config.skip_precision else f"{stats['precision']:.3f}"
        lines += [
            f"**Conformance (token-based replay):** log fitness {stats['log_fitness']:.3f}, "
            f"average trace fitness {stats['average_trace_fitness']:.3f}, "
            f"{stats['perc_fit_traces']:.1f}% fit traces, precision {precision_display}",
            "",
        ]
        if models_present:
            lines += [
                f"Model: [`models/{category.category_id}.pnml`](models/{category.category_id}.pnml) (Petri net, Inductive Miner) · "
                f"[`models/{category.category_id}.png`](models/{category.category_id}.png) (Directly-Follows Graph)",
                "",
            ]
        else:
            lines += [
                "Model files were removed after this run was accepted (kept out of the final "
                "deliverable to save disk space) — re-run Step 7 against this round's "
                "`assignments.csv`/`taxonomy.json` to regenerate them if needed.",
                "",
            ]

    return "\n".join(lines)


def save_discovery_outputs(
    metrics_df: pd.DataFrame,
    models_by_category: dict[str, tuple[PetriNet, Marking, Marking]],
    dfgs_by_category: dict[str, tuple[dict, dict, dict]],
    assignments_df: pd.DataFrame,
    variants_df: pd.DataFrame,
    taxonomy: Taxonomy,
    config: PipelineConfig,
    output_dir: Path,
) -> None:
    models_dir = output_dir / "models"
    models_dir.mkdir(parents=True, exist_ok=True)

    atomic_write_csv(metrics_df, output_dir / "discovery_metrics.csv", index=False)

    for category_id, (net, im, fm) in models_by_category.items():
        with atomic_output_path(models_dir / f"{category_id}.pnml") as tmp:
            pm4py.write_pnml(net, im, fm, str(tmp))
    for category_id, (dfg, start_activities, end_activities) in dfgs_by_category.items():
        with atomic_output_path(models_dir / f"{category_id}.png") as tmp:
            pm4py.save_vis_dfg(dfg, start_activities, end_activities, str(tmp))

    report = build_discovery_report(metrics_df, assignments_df, variants_df, taxonomy, config)
    atomic_write_text(output_dir / "discovery_report.md", report)

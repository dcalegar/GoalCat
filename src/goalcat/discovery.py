from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd
import pm4py
from pm4py.objects.petri_net.obj import Marking, PetriNet

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
        category_id: df[df[config.case_id_key].isin(case_ids)]
        for category_id, case_ids in case_ids_by_category.items()
    }


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

    return df[df[config.case_id_key].isin(case_ids)]


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
    sub_df: pd.DataFrame, net: PetriNet, im: Marking, fm: Marking, config: PipelineConfig
) -> dict:
    """Fitness and precision via token-based replay — the standard pairing with Inductive Miner,
    fast enough for both RTFM's largest category (111 variants) and smallest (1 variant, 30.8%
    of cases); see PROGRESS.md for why alignments were considered and not chosen."""
    fitness = pm4py.fitness_token_based_replay(
        sub_df, net, im, fm,
        activity_key=config.activity_key, timestamp_key=config.timestamp_key, case_id_key=config.case_id_key,
    )
    precision = pm4py.precision_token_based_replay(
        sub_df, net, im, fm,
        activity_key=config.activity_key, timestamp_key=config.timestamp_key, case_id_key=config.case_id_key,
    )
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
        conformance = compute_conformance(sub_df, net, im, fm, config)
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
        lines += [
            f"**Conformance (token-based replay):** log fitness {stats['log_fitness']:.3f}, "
            f"average trace fitness {stats['average_trace_fitness']:.3f}, "
            f"{stats['perc_fit_traces']:.1f}% fit traces, precision {stats['precision']:.3f}",
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
    output_dir.mkdir(parents=True, exist_ok=True)
    models_dir = output_dir / "models"
    models_dir.mkdir(parents=True, exist_ok=True)

    metrics_df.to_csv(output_dir / "discovery_metrics.csv", index=False)

    for category_id, (net, im, fm) in models_by_category.items():
        pm4py.write_pnml(net, im, fm, str(models_dir / f"{category_id}.pnml"))
    for category_id, (dfg, start_activities, end_activities) in dfgs_by_category.items():
        pm4py.save_vis_dfg(dfg, start_activities, end_activities, str(models_dir / f"{category_id}.png"))

    report = build_discovery_report(metrics_df, assignments_df, variants_df, taxonomy, config)
    (output_dir / "discovery_report.md").write_text(report, encoding="utf-8")

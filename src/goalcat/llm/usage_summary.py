"""Rolls up the per-call token/char/latency/cost figures each LLM step already writes into its
own *_run_metadata.json (see llm_backend.RunMetadata, taxonomy.save_taxonomy,
assignment.save_assignment_outputs, description.save_description_outputs) into two coarser
views: one per round (Steps 5/6/8 combined) and one per execution (every round combined, written
once the run is actually done — see review.finalize_run). Neither AI Studio's GUI nor the linked
GCP Billing console can attribute spend to a specific run this way; this module is the
alternative discussed for the ICPM2027 write-up's usage/cost reporting.
"""

from __future__ import annotations

import dataclasses
import json
from pathlib import Path

from ..atomic_io import atomic_write_json
from ..config import ROUND_PREFIX, PipelineConfig

# Filename, relative to its step's own round-scoped directory, holding that step's RunMetadata.
_STEP_METADATA_FILENAMES = {
    "taxonomy": "taxonomy_run_metadata.json",
    "assignment": "assignment_run_metadata.json",
    "description": "description_run_metadata.json",
}


def _aggregate_calls(calls: list[dict]) -> dict:
    """Sums a list of raw RunMetadata dicts (each already carrying estimated_cost_usd, added by
    the step's own save_*() — see llm_backend.estimate_cost_usd) into one totals dict.
    total_estimated_cost_usd is None, not a silently-wrong 0.0, whenever any included call's cost
    is unknown (unpriced model)."""
    costs = [c.get("estimated_cost_usd") for c in calls]
    return {
        "call_count": len(calls),
        "total_input_tokens": sum(c.get("input_tokens") or 0 for c in calls),
        "total_output_tokens": sum(c.get("output_tokens") or 0 for c in calls),
        "total_prompt_chars": sum(c.get("prompt_chars") or 0 for c in calls),
        "total_response_chars": sum(c.get("response_chars") or 0 for c in calls),
        "total_latency_seconds": sum(c.get("latency_seconds") or 0.0 for c in calls),
        "total_estimated_cost_usd": sum(costs) if all(c is not None for c in costs) else None,
    }


def _sum_aggregates(aggregates: list[dict]) -> dict:
    """Same totals shape as _aggregate_calls, but summing already-aggregated dicts (steps into a
    round's totals, or rounds into an execution's totals) instead of raw calls."""
    costs = [a["total_estimated_cost_usd"] for a in aggregates]
    return {
        "call_count": sum(a["call_count"] for a in aggregates),
        "total_input_tokens": sum(a["total_input_tokens"] for a in aggregates),
        "total_output_tokens": sum(a["total_output_tokens"] for a in aggregates),
        "total_prompt_chars": sum(a["total_prompt_chars"] for a in aggregates),
        "total_response_chars": sum(a["total_response_chars"] for a in aggregates),
        "total_latency_seconds": sum(a["total_latency_seconds"] for a in aggregates),
        "total_estimated_cost_usd": sum(costs) if all(c is not None for c in costs) else None,
    }


def _step_calls(step: str, payload: dict) -> list[dict]:
    """Each step's *_run_metadata.json has a different shape (taxonomy/description: at most one
    call; assignment: a batch list) — normalized here to a flat list of call dicts."""
    if step == "taxonomy":
        return [payload]
    if step == "description":
        call = payload.get("call")
        return [call] if call is not None else []
    return payload["calls"]  # assignment


def compute_round_usage_summary(config: PipelineConfig) -> dict:
    """Reads whichever of Steps 5/6/8's *_run_metadata.json already exist under config.round_dir
    and combines them. Steps not yet run in this round (e.g. Step 9 called before Step 8) are
    simply absent from "steps" rather than raising — a round can legitimately be summarized
    mid-flight."""
    step_dirs = {
        "taxonomy": config.taxonomy_dir,
        "assignment": config.assignment_dir,
        "description": config.description_dir,
    }
    steps: dict[str, dict] = {}
    for step, step_dir in step_dirs.items():
        metadata_path = step_dir / _STEP_METADATA_FILENAMES[step]
        if not metadata_path.exists():
            continue
        payload = json.loads(metadata_path.read_text(encoding="utf-8"))
        steps[step] = _aggregate_calls(_step_calls(step, payload))

    return {
        "round": config.round,
        "steps": steps,
        "totals": _sum_aggregates(list(steps.values())),
    }


def save_round_usage_summary(config: PipelineConfig) -> dict:
    summary = compute_round_usage_summary(config)
    atomic_write_json(config.round_dir / "round_usage_summary.json", summary)
    return summary


def _existing_round_numbers(config: PipelineConfig) -> list[int]:
    if not config.run_output_dir.is_dir():
        return []
    numbers = []
    for entry in config.run_output_dir.iterdir():
        if entry.is_dir() and entry.name.startswith(ROUND_PREFIX):
            suffix = entry.name[len(ROUND_PREFIX) :]
            if suffix.isdigit():
                numbers.append(int(suffix))
    return sorted(numbers)


def compute_execution_usage_summary(config: PipelineConfig) -> dict:
    """Combines every round of this execution (config.run_id) into one total — the "whole run"
    figure for a revision chain that went through several rounds before acceptance. Prefers each
    round's own round_usage_summary.json (written by save_round_usage_summary(), called every
    time Step 9 runs against that round — see review.process_review()) and falls back to
    recomputing it on the fly for a round that never reached Step 9 with this feature present."""
    rounds: dict[int, dict] = {}
    for round_number in _existing_round_numbers(config):
        round_config = dataclasses.replace(config, round=round_number)
        summary_path = round_config.round_dir / "round_usage_summary.json"
        if summary_path.exists():
            rounds[round_number] = json.loads(summary_path.read_text(encoding="utf-8"))
        else:
            rounds[round_number] = compute_round_usage_summary(round_config)

    return {
        "run_id": config.run_id,
        "rounds": rounds,
        "totals": _sum_aggregates([r["totals"] for r in rounds.values()]),
    }


def save_execution_usage_summary(config: PipelineConfig) -> dict:
    summary = compute_execution_usage_summary(config)
    atomic_write_json(config.final_dir / "pipeline_usage_summary.json", summary)
    return summary

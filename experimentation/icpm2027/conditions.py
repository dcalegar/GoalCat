"""Executing one experimental condition end to end, and recording what it was.

A *condition* is one cell of the experimental design: a dataset, an arm
(intent-guided / open / Task C5's label-list control), an optional perturbation tag, and a
replicate index. `execute_condition()` is the only function in this package that causes LLM calls
to happen, and it always performs the same five things in the same order:

1. materialize the shared Steps 1-4 inputs (`inputs.py`) — never recompute them;
2. render and write the condition's config (`protocol.py`) — never hand-edited;
3. for the label-list arm only, write the supplied taxonomy directly, with no Step 5 call;
4. run Steps 5-6 (and 7-8 only where Task D6's decision says so) in a fresh subprocess;
5. write the run manifest (`manifest.py`).

Step 9 never runs. §3's paired comparison is defined on the partitions *before* any analyst
merge/split/rename, and `run_condition.py` rejects the step outright rather than relying on no
caller asking for it.
"""

from __future__ import annotations

import logging
import math
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from goalcat.atomic_io import atomic_write_json, atomic_write_text
from goalcat.config import REPO_ROOT, ROUND_PREFIX, TAXONOMY_DIRNAME, VARIANTS_DIRNAME
from goalcat.llm.taxonomy import Category, Taxonomy

from .inputs import SharedBase, materialize_condition_inputs, withhold_narrative_sample
from .manifest import build_manifest, now_iso, write_manifest
from .protocol import (
    ConditionSpec,
    PreRegistration,
    Protocol,
    resolve_assignment_batch_size,
    runs_step7b,
    write_condition_config,
)

LABEL_LISTS_DIR = Path(__file__).resolve().with_name("configs") / "label_lists"


@dataclass
class ConditionResult:
    condition: ConditionSpec
    run_dir: Path
    round_dir: Path
    manifest_path: Path | None
    skipped: bool = False
    reason: str | None = None


def round_dir_of(run_dir: Path, round_number: int = 1) -> Path:
    return run_dir / f"{ROUND_PREFIX}{round_number}"


def estimated_llm_calls(condition: ConditionSpec, base: SharedBase, batch_size: int) -> dict[str, int]:
    """Call-count accounting for one condition, before anything is billed.

    This is the only basis on which Task C10's `assignment_batch_size` may be chosen — the plan
    forbids tuning it against categorization outcomes, so the number that justifies it has to be
    available *before* the run, which is what this produces.
    """
    step5 = 0 if condition.arm == "label_list" else 1
    step6 = math.ceil(base.variant_count / batch_size) if batch_size > 0 else 0
    step8 = 1 if 8 in condition.steps else 0
    return {"step5": step5, "step6": step6, "step8": step8, "total": step5 + step6 + step8}


def load_label_list(dataset_id: str) -> list[dict[str, str]]:
    """Task C5's control condition: a domain-plausible label list of the same cardinality as the
    guided taxonomy, authored *without* reference to the goal model.

    Deliberately not shipped with content. Authoring it is a research act — the whole point of the
    control is that the labels are not goal-derived, which no code can certify — so this raises
    with instructions rather than inventing a list that would quietly become goal-derived by
    having been written next to the goal model.
    """
    path = LABEL_LISTS_DIR / f"{dataset_id}.yaml"
    if not path.exists():
        raise FileNotFoundError(
            f"Task C5's label-list control for {dataset_id!r} needs {path}, which does not exist. "
            "Author it as a list of {category_id, name, description} entries: same cardinality as "
            "the guided taxonomy, domain-plausible, and derived from domain knowledge rather than "
            "from the goal model (that independence is what the control tests, and it cannot be "
            "checked automatically — record how the list was authored in the file's header)."
        )
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    labels = raw.get("labels") or []
    if not labels:
        raise ValueError(f"{path} contains no `labels:` entries.")
    return labels


def write_label_list_taxonomy(condition: ConditionSpec, run_dir: Path, logger: logging.Logger) -> Path:
    """Writes the label-list control's taxonomy directly into round1/05_taxonomy, bypassing Step 5.

    The control supplies its categories rather than inducing them, so there is no Step 5 LLM call
    to make; `anchor_ids` stays empty (the list is not goal-derived, and a non-empty anchor would
    assert exactly the linkage the control is designed to lack) and `evidence_variant_ids` stays
    empty (no sample was consulted). Step 6 then runs identically to the open arm.
    """
    labels = load_label_list(condition.dataset.dataset_id)
    taxonomy = Taxonomy(
        categories=[
            Category(
                category_id=entry["category_id"],
                name=entry["name"],
                description=entry["description"],
                anchor_ids=[],
                rationale=entry.get(
                    "rationale",
                    "Supplied label-list control (Task C5): not induced from the narrative sample "
                    "and not derived from the goal model.",
                ),
                evidence_variant_ids=[],
            )
            for entry in labels
        ]
    )
    taxonomy_dir = round_dir_of(run_dir) / TAXONOMY_DIRNAME
    path = taxonomy_dir / "taxonomy.json"
    atomic_write_json(path, taxonomy.model_dump())
    atomic_write_text(
        taxonomy_dir / "taxonomy_source.md",
        "# Supplied taxonomy — Task C5 label-list control\n\n"
        f"Written directly from `configs/label_lists/{condition.dataset.dataset_id}.yaml`; no "
        "Step 5 LLM call was made for this condition. `anchor_ids` is empty by construction: the "
        "list is not goal-derived, which is the property the control isolates.\n",
    )
    logger.info("Label-list control: wrote supplied taxonomy (%d categories) to %s", len(labels), path)
    return path


def already_complete(condition: ConditionSpec) -> bool:
    """A condition counts as complete when its round holds both a taxonomy and assignments
    covering every variant in the condition's own population.

    Used to make a whole-experiment driver re-runnable: re-invoking after a partial failure should
    resume, not re-bill the conditions that already finished. A *partial* Step 6 is not complete
    and is resumed in place by Step 6's own `load_prior_assignments()` logic — but only if this
    check actually notices the gap. File *existence* alone is not enough: a batch that Step 6
    could not resolve after its own retries (a provider outage outlasting them) is dropped from
    `assignments.csv` entirely — neither categorized nor residual — and `IncompleteAssignmentError`
    is raised for that run, but a *later* invocation of the driver only sees the file that already
    exists and, without the row-count check below, silently treats a short assignments.csv as
    finished, permanently losing that variant from every downstream count. Observed concretely:
    Sepsis's `icpm2027_e1_open_rep1`, 2026-08-29 — one variant (`V0100`) missing from
    `assignments.csv` (845 rows for 846 variants) after a provider 503 outlasted Step 6's retries;
    the next driver invocation skipped the condition as already complete and never retried it.
    """
    round_dir = round_dir_of(condition.run_dir)
    taxonomy_path = round_dir / TAXONOMY_DIRNAME / "taxonomy.json"
    assignments_path = round_dir / "06_assignment" / "assignments.csv"
    if not taxonomy_path.exists() or not assignments_path.exists():
        return False

    variants_path = condition.run_dir / VARIANTS_DIRNAME / "variants.csv"
    if not variants_path.exists():
        # Steps 1-4 inputs not even materialized yet — can't verify coverage, so don't claim done.
        return False
    expected = len(pd.read_csv(variants_path, dtype=str, usecols=["variant_id"]))
    actual = len(pd.read_csv(assignments_path, dtype=str, usecols=["variant_id"]))
    return actual >= expected


def _launch(
    config_path: Path,
    run_id: str,
    steps: tuple[int, ...],
    logger: logging.Logger,
    *,
    indicators: bool = False,
) -> None:
    cmd = [
        sys.executable, "-m", "experimentation.icpm2027.run_condition",
        "--config", str(config_path),
        "--run-id", run_id,
        "--steps", ",".join(str(s) for s in steps),
    ]
    if indicators:
        cmd.append("--indicators")
    logger.info("Launching condition subprocess: %s", " ".join(cmd))
    completed = subprocess.run(cmd, cwd=str(REPO_ROOT), check=False)
    if completed.returncode != 0:
        raise RuntimeError(
            f"Condition run {run_id} failed with exit code {completed.returncode}. Its "
            f"pipeline.log is in data/output/.../{run_id}/; re-running this driver resumes from "
            "whatever that run directory already holds."
        )


def execute_condition(
    condition: ConditionSpec,
    base: SharedBase,
    protocol: Protocol,
    prereg: PreRegistration,
    logger: logging.Logger,
    *,
    pending_decisions: list[str],
    dry_run: bool = False,
    force: bool = False,
) -> ConditionResult:
    """Runs one condition and writes its manifest. Returns where everything landed."""
    run_dir = condition.run_dir
    round_dir = round_dir_of(run_dir)
    batch_size = resolve_assignment_batch_size(condition.dataset, protocol, prereg)
    estimate = estimated_llm_calls(condition, base, batch_size)

    logger.info(
        "Condition %s | dataset=%s arm=%s tag=%s replicate=%d | mode=%s goal_model=%s | steps=%s "
        "| %d variants, batch_size=%d → ~%d LLM calls",
        condition.condition_id, condition.dataset.dataset_id, condition.arm, condition.tag,
        condition.replicate, condition.taxonomy_mode, condition.effective_goal_model_filename,
        list(condition.steps), base.variant_count, batch_size, estimate["total"],
    )

    if dry_run:
        return ConditionResult(condition, run_dir, round_dir, None, skipped=True, reason="dry-run")

    if already_complete(condition) and not force:
        logger.info("Condition %s already complete — skipping (use --force to re-run).", condition.condition_id)
        return ConditionResult(condition, run_dir, round_dir, run_dir / "manifest.json", skipped=True, reason="already complete")

    if force and round_dir.exists():
        # `run_condition` skips Step 5a when 05_taxonomy/taxonomy.json is present (resume safety),
        # so a forced re-run has to start from a clean round dir or it would silently reuse the
        # stale taxonomy. Steps 1-4 live under run_dir, not round_dir, and are re-copied below.
        shutil.rmtree(round_dir)
        logger.info("Condition %s: --force — cleared %s for a clean re-run.", condition.condition_id, round_dir)

    started_at = now_iso()
    materialize_condition_inputs(base, run_dir, logger)
    sample_record: dict[str, Any] = {"withheld": False}
    if condition.withholds_narrative_sample:
        sample_record = withhold_narrative_sample(run_dir, logger)
    config_path = write_condition_config(condition, protocol, prereg)

    steps = condition.steps
    if condition.arm == "label_list":
        write_label_list_taxonomy(condition, run_dir, logger)
        steps = tuple(s for s in steps if s != 5)

    # `runs_step7b()` decides purely from arm/dataset (Task C13's policy) and knows nothing about
    # which steps *this* condition actually runs. A Task C12 stability condition requests Step 5a
    # alone, so it never produces `assignments.csv`; without this guard, Step 7b is launched anyway
    # and crashes on the missing Step 6 output it needs (`run_step7b_indicators()`'s own
    # precondition). Mirrors the `8 in condition.steps` gating pattern above (line 72).
    step7b = runs_step7b(condition.dataset, condition.arm, prereg) and 6 in steps
    _launch(config_path, condition.run_id, steps, logger, indicators=step7b)
    finished_at = now_iso()

    goal_model_filename = condition.effective_goal_model_filename
    goal_model_path = (REPO_ROOT / "data" / "goals" / goal_model_filename) if goal_model_filename else None

    manifest = build_manifest(
        experiment=condition.experiment,
        condition_id=condition.condition_id,
        dataset_id=condition.dataset.dataset_id,
        arm=condition.arm,
        replicate=condition.replicate,
        tag=condition.tag,
        axis=condition.effective_axis,
        axis_root=condition.effective_axis_root,
        protocol_version=protocol.version,
        preregistered=not pending_decisions,
        pending_decisions=pending_decisions,
        decisions=_decision_record(prereg, condition.dataset.dataset_id),
        run_dir=run_dir,
        round_dir=round_dir,
        log_path=condition.dataset.log_path,
        goal_model_path=goal_model_path,
        condition_config_path=config_path,
        shared_base=base.as_manifest_record(),
        variant_scope=base.scope,
        steps=steps,
        started_at=started_at,
        finished_at=finished_at,
        extra={
            "estimated_llm_calls": estimate,
            "assignment_batch_size": batch_size,
            "narrative_sample": sample_record,
            "step7b_indicators": step7b,
        },
    )
    manifest_path = write_manifest(manifest, run_dir)
    logger.info("Wrote manifest: %s", manifest_path)
    return ConditionResult(condition, run_dir, round_dir, manifest_path)


def _decision_record(prereg: PreRegistration, dataset_id: str) -> dict[str, Any]:
    """Every pre-registered decision governing this dataset, verbatim, into the manifest — so a
    run's evidence includes what was decided, when, and why, not only which values were used."""
    return {
        d.key: {
            "task": d.task,
            "status": d.status,
            "value": d.value,
            "decided_on": d.decided_on,
            "rationale": " ".join(d.rationale.split()),
        }
        for d in prereg.governing(dataset_id)
    }

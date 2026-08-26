"""The shared Steps 1-4 base every condition of a dataset draws its inputs from.

EXPERIMENTATION_PLAN.md §2.1: for dataset L_i, Steps 1-4 run **once** — variants, profiles,
narratives, narrative sample — and the *same* narratives and sample then feed both the
intent-guided and the open arm. §2.2's freeze table marks the narrative sample **identical** in
bold, and it is the one row that a naive "run the pipeline twice with different settings" design
would silently break, because Step 4's sample would be recomputed inside each arm's own run
directory.

This module closes that hole by construction: Steps 1-4 execute exactly once, into a shared base
directory, and each condition's run directory receives a byte-for-byte **copy** of the four
artifacts. Identity is then a property of the file system, not of Step 4's determinism, and
freeze.py re-verifies it by hash after the fact anyway.

The variant-scope policy (Task C7) is applied here, between Step 1 and Step 2, for the same
reason: scoping after profiling or after sampling would leave the sample drawn from a population
the conditions never see.
"""

from __future__ import annotations

import json
import logging
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from goalcat.atomic_io import atomic_write_json, atomic_write_text
from goalcat.config import (
    PROFILING_DIRNAME,
    SAMPLING_DIRNAME,
    TEXTUALIZATION_DIRNAME,
    VARIANTS_DIRNAME,
)
from goalcat.extraction.variants import load_variants, save_variants
from goalcat.pipeline import (
    run_step1_variants,
    run_step2_profiling,
    run_step3_textualization,
    run_step4_sampling,
)

from .manifest import sha256_file
from .protocol import (
    DatasetSpec,
    PreRegistration,
    Protocol,
    resolve_variant_scope,
    shared_base_dir,
    shared_base_run_id,
)

#: The four Steps 1-4 artifacts a condition inherits, as (directory, filename) pairs. Copied, not
#: recomputed, and hashed into every condition manifest.
SHARED_ARTIFACTS: tuple[tuple[str, str], ...] = (
    (VARIANTS_DIRNAME, "variants.csv"),
    (PROFILING_DIRNAME, "profiles.csv"),
    (PROFILING_DIRNAME, "profiles.json"),
    (TEXTUALIZATION_DIRNAME, "narratives.csv"),
    (SAMPLING_DIRNAME, "narrative_sample.csv"),
)

SCOPE_RECORD_FILENAME = "variant_scope.json"
UNSCOPED_VARIANTS_FILENAME = "variants_unscoped.csv"


@dataclass(frozen=True)
class SharedBase:
    """A prepared Steps 1-4 execution: where it is, what scope it was built under, and the hashes
    every condition inheriting from it records."""

    dataset_id: str
    run_id: str
    run_dir: Path
    scope: dict[str, Any]
    artifact_hashes: dict[str, str]
    variant_count: int
    case_count: int

    def as_manifest_record(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "run_dir": str(self.run_dir),
            "variant_count": self.variant_count,
            "case_count": self.case_count,
            "artifacts": self.artifact_hashes,
        }


def _base_config_dict(dataset: DatasetSpec, protocol: Protocol) -> dict[str, Any]:
    """Steps 1-4 read none of the LLM or taxonomy settings, but the base directory still carries a
    config snapshot (run_logging writes one), so it is generated from the same protocol as the
    conditions — a drift warning in the base's pipeline.log then means something real."""
    return {
        "log_filename": dataset.log_filename,
        "goal_model_filename": dataset.goal_model_filename,
        "output_dir": "data/output",
        "run_id": shared_base_run_id(dataset),
        "round": 1,
        "case_id_key": dataset.case_id_key,
        "activity_key": dataset.activity_key,
        "timestamp_key": dataset.timestamp_key,
        "resource_key": dataset.resource_key,
        **protocol.sampling,
        "taxonomy_mode": "intent_guided",
        **protocol.discovery,
        "llm": dict(protocol.llm),
    }


def _write_base_config(dataset: DatasetSpec, protocol: Protocol) -> Path:
    base_dir = shared_base_dir(dataset)
    path = base_dir / "base_config.yaml"
    header = (
        "# GENERATED — do not edit. The Steps 1-4 config for the shared base every ICPM 2027\n"
        f"# condition of dataset '{dataset.dataset_id}' inherits from (protocol "
        f"{protocol.version}). See experimentation/icpm2027/inputs.py.\n\n"
    )
    atomic_write_text(path, header + yaml.safe_dump(_base_config_dict(dataset, protocol), sort_keys=False))
    return path


def select_scoped_variants(variants_df: pd.DataFrame, scope: dict[str, Any]) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Applies a variant-scope policy to Step 1's output (Task C7).

    Policies:
      - ``all``: every extracted variant.
      - ``top_n_variants``: the N most frequent variants (Step 1's stable frequency sort already
        fixes tie order, so this is deterministic).
      - ``min_case_coverage``: the most frequent variants until their cumulative case share
        reaches the threshold.

    Returns the kept frame plus a record of what the policy actually did — kept/total variants and
    cases, and the resulting case coverage, so every downstream coverage figure can be read
    against the whole log rather than against a silently truncated population.
    """
    policy = scope.get("policy", "all")
    total_variants = len(variants_df)
    total_cases = int(variants_df["frequency"].sum())

    ordered = variants_df.sort_values("frequency", ascending=False, kind="stable")

    if policy == "all":
        kept = variants_df
    elif policy == "top_n_variants":
        kept = ordered.head(int(scope["top_n"]))
    elif policy == "min_case_coverage":
        threshold = float(scope["min_case_coverage"]) * total_cases
        cumulative = ordered["frequency"].cumsum()
        # searchsorted-style: keep through the first variant that reaches the threshold.
        n_keep = int((cumulative < threshold).sum()) + 1
        kept = ordered.head(min(n_keep, total_variants))
    else:
        raise ValueError(
            f"Unknown variant-scope policy {policy!r} (expected 'all', 'top_n_variants', or "
            "'min_case_coverage')"
        )

    # Restore Step 1's own row order/ids rather than the scoping sort's, so variants.csv keeps the
    # exact shape every downstream loader expects.
    kept = variants_df[variants_df["variant_id"].isin(set(kept["variant_id"]))].reset_index(drop=True)
    kept_cases = int(kept["frequency"].sum())

    record = {
        **{k: v for k, v in scope.items()},
        "applied_policy": policy,
        "variants_total": total_variants,
        "variants_kept": len(kept),
        "cases_total": total_cases,
        "cases_kept": kept_cases,
        "case_coverage_of_full_log": kept_cases / total_cases if total_cases else 0.0,
    }
    return kept, record


def _apply_scope_to_base(base_dir: Path, scope: dict[str, Any], logger: logging.Logger) -> dict[str, Any]:
    """Rewrites the base's variants.csv to the scoped subset, once, keeping the unscoped table
    beside it as `variants_unscoped.csv` and the decision as `variant_scope.json`.

    Rewriting Step 1's own output (rather than filtering later, per condition) is deliberate: every
    downstream step — profiling, textualization, sampling, and each condition's Step 6/7 — reads
    variants.csv, so scoping here makes the whole execution internally consistent with no
    scope-awareness anywhere else in the code. The unscoped copy and the record are what keep it
    auditable.
    """
    record_path = base_dir / VARIANTS_DIRNAME / SCOPE_RECORD_FILENAME
    if record_path.exists():
        existing = json.loads(record_path.read_text(encoding="utf-8"))
        logger.info(
            "Variant scope already applied to this base (%s kept of %s) — not re-applying.",
            existing.get("variants_kept"), existing.get("variants_total"),
        )
        return existing

    variants_path = base_dir / VARIANTS_DIRNAME / "variants.csv"
    variants_df = load_variants(variants_path)
    kept, record = select_scoped_variants(variants_df, scope)

    if record["variants_kept"] != record["variants_total"]:
        shutil.copy2(variants_path, base_dir / VARIANTS_DIRNAME / UNSCOPED_VARIANTS_FILENAME)
        save_variants(kept, variants_path)
        logger.info(
            "Variant scope '%s' applied: kept %d/%d variants covering %d/%d cases (%.1f%% of the "
            "full log). Unscoped table preserved as %s.",
            record["applied_policy"], record["variants_kept"], record["variants_total"],
            record["cases_kept"], record["cases_total"],
            record["case_coverage_of_full_log"] * 100, UNSCOPED_VARIANTS_FILENAME,
        )
    else:
        logger.info("Variant scope '%s': all %d variants kept.", record["applied_policy"], record["variants_total"])

    atomic_write_json(record_path, record)
    return record


def prepare_shared_base(
    dataset: DatasetSpec,
    protocol: Protocol,
    prereg: PreRegistration,
    logger: logging.Logger,
    force: bool = False,
) -> SharedBase:
    """Runs (or reuses) Steps 1-4 once for this dataset and returns the resulting SharedBase.

    Idempotent: a base directory that already holds all five artifacts is reused as-is, since
    Steps 1-4 are deterministic and re-running them would only burn wall-clock (textualization
    subprocesses the vendored LUPIN module once per variant). ``force=True`` deletes and rebuilds
    — needed after a protocol change that touches sampling, and nowhere else.
    """
    base_dir = shared_base_dir(dataset)
    if force and base_dir.exists():
        logger.warning("force=True — deleting existing shared base at %s", base_dir)
        shutil.rmtree(base_dir)

    config_path = _write_base_config(dataset, protocol)
    run_id = shared_base_run_id(dataset)
    scope = resolve_variant_scope(dataset, prereg)

    if _has_all_artifacts(base_dir):
        logger.info("Reusing existing shared Steps 1-4 base at %s", base_dir)
        scope_record_path = base_dir / VARIANTS_DIRNAME / SCOPE_RECORD_FILENAME
        scope_record = (
            json.loads(scope_record_path.read_text(encoding="utf-8"))
            if scope_record_path.exists()
            else {**scope, "applied_policy": scope.get("policy"), "note": "no scope record written"}
        )
    else:
        logger.info("Building shared Steps 1-4 base for %s at %s", dataset.dataset_id, base_dir)
        run_step1_variants(config_path, run_id)
        scope_record = _apply_scope_to_base(base_dir, scope, logger)
        # Steps 2-4 are called without in-memory frames on purpose: each re-reads the (now scoped)
        # variants.csv from disk, so the scope propagates without any step needing to know it.
        run_step2_profiling(config_path, run_id)
        run_step3_textualization(config_path, run_id)
        run_step4_sampling(config_path, run_id)

    variants_df = load_variants(base_dir / VARIANTS_DIRNAME / "variants.csv")
    return SharedBase(
        dataset_id=dataset.dataset_id,
        run_id=run_id,
        run_dir=base_dir,
        scope=scope_record,
        artifact_hashes=base_artifact_hashes(base_dir),
        variant_count=len(variants_df),
        case_count=int(variants_df["frequency"].sum()),
    )


def _has_all_artifacts(base_dir: Path) -> bool:
    return all((base_dir / subdir / name).exists() for subdir, name in SHARED_ARTIFACTS)


def base_artifact_hashes(base_dir: Path) -> dict[str, str]:
    """`<subdir>/<file>` -> sha256 for the five shared artifacts. The same dict is written into
    every condition manifest, which is what lets freeze.py assert that two arms really did consume
    identical Steps 1-4 output."""
    return {
        f"{subdir}/{name}": sha256_file(base_dir / subdir / name)
        for subdir, name in SHARED_ARTIFACTS
        if (base_dir / subdir / name).exists()
    }


def materialize_condition_inputs(base: SharedBase, condition_dir: Path, logger: logging.Logger) -> dict[str, str]:
    """Copies the shared Steps 1-4 artifacts into one condition's run directory.

    A copy, not a symlink: a replication package that is archived, zipped, or moved must stay
    self-contained, and a broken link would surface as a silent recomputation from the raw log
    (`_get_or_build_*` in goalcat/pipeline.py falls back to computing whatever is missing) rather
    than as an error. Returns the copied files' hashes, which must equal the base's.
    """
    condition_dir.mkdir(parents=True, exist_ok=True)
    for subdir, name in SHARED_ARTIFACTS:
        source = base.run_dir / subdir / name
        if not source.exists():
            raise FileNotFoundError(
                f"Shared base {base.run_dir} is missing {subdir}/{name} — Steps 1-4 did not "
                "complete. Re-run prepare_shared_base() before materializing conditions."
            )
        target = condition_dir / subdir / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    hashes = base_artifact_hashes(condition_dir)
    if hashes != base.artifact_hashes:
        differing = sorted(k for k in base.artifact_hashes if hashes.get(k) != base.artifact_hashes[k])
        raise RuntimeError(
            f"Copied Steps 1-4 artifacts do not match the shared base for {condition_dir} "
            f"(differing: {differing}). The freeze table's identical-inputs rows cannot be "
            "asserted for this condition."
        )
    logger.info("Materialized shared Steps 1-4 inputs into %s", condition_dir)
    return hashes


def withhold_narrative_sample(condition_dir: Path, logger: logging.Logger) -> dict[str, Any]:
    """Task C11a: empty this condition's narrative sample, keeping its columns.

    Called *after* `materialize_condition_inputs()` has already asserted that the copied Steps 1-4
    artifacts hash-match the shared base. That ordering is deliberate: the freeze table's
    identical-inputs rows are verified for this condition exactly as for every other, and only then
    is the one factor under ablation removed. The withheld row count is returned for the manifest,
    so a run whose sample was emptied can never be mistaken for a plain guided run.
    """
    sample_path = condition_dir / SAMPLING_DIRNAME / "narrative_sample.csv"
    sample_df = pd.read_csv(sample_path)
    withheld = len(sample_df)
    sample_df.iloc[0:0].to_csv(sample_path, index=False)
    logger.info(
        "Task C11a: withheld %d narrative(s) from Step 5a for %s (columns kept, rows emptied)",
        withheld, condition_dir.name,
    )
    return {
        "withheld": True,
        "narratives_withheld": withheld,
        "sample_path": str(sample_path.relative_to(REPO_ROOT)),
    }

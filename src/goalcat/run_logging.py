from __future__ import annotations

import json
import logging
import os
import platform

from .atomic_io import atomic_write_json
from .config import PipelineConfig, config_snapshot_dict


def get_logger(config: PipelineConfig) -> logging.Logger:
    """Logger shared by every pipeline step, so a multi-step unattended run leaves one trail.

    Writes to stdout and to `<output_dir>/<log_stem>/<run_id>/pipeline.log` (append mode), so
    later steps called with the same run_id keep accumulating into the same file — including
    every round of a Step 9 revision chain, since rounds nest inside one execution directory and
    never change run_output_dir. One process is assumed to correspond to one run_id — this cache
    is keyed by logger name only, not by run directory, so a single process switching run_ids
    mid-run would keep writing to the first run's log file.
    """
    logger = logging.getLogger("goalcat")
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    log_path = config.run_output_dir / "pipeline.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    _log_run_environment(logger)
    _snapshot_or_check_config(config, logger)

    return logger


def _log_run_environment(logger: logging.Logger) -> None:
    """Logs this process's execution environment once per run — host, OS, Python, CPU, RAM —
    so pipeline.log carries the traceability info RunMetadata (llm_backend.py) can't: which
    machine a run executed on, alongside which LLM backend/model each call used (logged
    per-call by LLMBackend itself)."""
    logger.info(
        "Run environment: host=%s, platform=%s, python=%s, cpu_count=%s, total_ram_gib=%s",
        platform.node(),
        platform.platform(),
        platform.python_version(),
        os.cpu_count(),
        _total_ram_gib(),
    )


def _total_ram_gib() -> str:
    try:
        total_bytes = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
    except (ValueError, OSError, AttributeError):
        return "unknown"
    return f"{total_bytes / (1024 ** 3):.1f}"


def _snapshot_or_check_config(config: PipelineConfig, logger: logging.Logger) -> None:
    """Writes run_config_snapshot.json the first time a run directory is touched; on reuse
    (run_id pointing at an existing directory), warns — does not block — if the live config
    disagrees with the one the directory was started under, since a step in this reused
    directory may then load artifacts computed under different settings.
    """
    snapshot_path = config.run_output_dir / "run_config_snapshot.json"
    current = config_snapshot_dict(config)

    if not snapshot_path.exists():
        atomic_write_json(snapshot_path, current)
        return

    saved = json.loads(snapshot_path.read_text(encoding="utf-8"))
    if saved != current:
        changed = sorted(key for key in current if current.get(key) != saved.get(key))
        logger.warning(
            "Config drift: run directory %s was started under different settings (changed keys: "
            "%s) — artifacts reused from this directory may not match the current config.",
            config.run_output_dir,
            changed,
        )

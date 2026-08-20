"""Per-run manifests (EXPERIMENTATION_PLAN.md §2.2, Task D4; §8's goal-model provenance).

Every frozen run "retains a manifest with hashes/versions for inputs, goal model, prompts, model
configuration, and outputs, extended per Task D4 to also record the resolved model version and any
seed." That is what this module writes: one `manifest.json` per condition run directory, plus a
human-readable `manifest.md` beside it.

What this stack can and cannot record about determinism, stated once here rather than implied:

- **Prompts** are hashed from the rendered text the run actually sent (Step 5's
  `taxonomy_prompt.txt`, Step 6's `assignment_prompts/*.txt`), not from the templates alone, so a
  template edit and a sample change are both visible.
- **Resolved model version** is taken from the provider's own echo in the run metadata when the
  backend records one. Where the provider returns nothing beyond the requested model string, the
  field is written as null with an explicit note — never back-filled with the configured string,
  which would assert a resolution that did not happen.
- **Seed** is null. Neither `PipelineConfig.llm` nor the Gemini path through litellm exposes a
  sampling seed; `temperature: 0` is the whole of what pins sampling here. Task C2's replicate
  runs are what actually measure the residual variance, and the manifest says so rather than
  implying reproducibility the stack cannot deliver.
"""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from goalcat.config import REPO_ROOT

MANIFEST_FILENAME = "manifest.json"
MANIFEST_MD_FILENAME = "manifest.md"

#: Prompt templates the LLM steps read. Hashed as a set so a wording change to any of them is
#: visible in every manifest written afterwards (freeze table: "Prompts: versioned").
_PROMPT_TEMPLATE_DIR = REPO_ROOT / "src" / "goalcat" / "templates"

_SEED_NOTE = (
    "null — no seed is exposed by PipelineConfig.llm or by the Gemini path through litellm; "
    "temperature=0 is the only sampling constraint applied. See Task C2's replicate runs for the "
    "empirical noise floor."
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def file_record(path: Path) -> dict[str, Any] | None:
    """Hash + size + repo-relative path for one input/output file, or None if it isn't there."""
    if not path.exists() or not path.is_file():
        return None
    return {
        "path": _relative(path),
        "sha256": sha256_file(path),
        "bytes": path.stat().st_size,
    }


def dir_record(directory: Path, pattern: str = "*") -> dict[str, str]:
    """Filename -> sha256 for every matching file in a directory, sorted. Used for the prompt
    templates and for Step 6's per-batch prompt files, where the *set* is the artifact."""
    if not directory.is_dir():
        return {}
    return {p.name: sha256_file(p) for p in sorted(directory.glob(pattern)) if p.is_file()}


def _relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path.resolve())


def git_commit() -> str | None:
    """The repository revision a run executed at, or None outside a git checkout. Recorded because
    the pipeline's own behaviour — not just its configuration — is part of the frozen condition."""
    try:
        out = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=10, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip() or None


def git_is_dirty() -> bool | None:
    try:
        out = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "status", "--porcelain"],
            capture_output=True, text=True, timeout=10, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return bool(out.stdout.strip())


def environment_record() -> dict[str, Any]:
    return {
        "host": platform.node(),
        "platform": platform.platform(),
        "python": platform.python_version(),
        "git_commit": git_commit(),
        "git_dirty": git_is_dirty(),
    }


def _resolved_llm_from_metadata(path: Path) -> dict[str, Any] | None:
    """Reads a Step 5/6/8 run-metadata file for what the provider actually reported.

    Handles both shapes goalcat writes: Step 5/8's single-object metadata and Step 6's
    {"calls": [...]} envelope. Returns the distinct (model, resolved_model, provider, backend,
    temperature) tuples seen — a set, not the first, so a mid-run model substitution would show
    up as two entries rather than being hidden behind whichever call happened to be first.
    """
    if not path.exists():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    calls = payload.get("calls") if isinstance(payload, dict) and "calls" in payload else [payload]
    seen: list[dict[str, Any]] = []
    for call in calls:
        if not isinstance(call, dict):
            continue
        record = {
            "model": call.get("model"),
            "resolved_model": call.get("resolved_model"),
            "provider": call.get("provider"),
            "backend": call.get("backend"),
            "temperature": call.get("temperature"),
        }
        if record not in seen:
            seen.append(record)
    if not seen:
        return None
    return {"distinct_call_configurations": seen, "call_count": len(calls)}


def build_manifest(
    *,
    experiment: str,
    condition_id: str,
    dataset_id: str,
    arm: str,
    replicate: int,
    tag: str | None,
    protocol_version: str,
    preregistered: bool,
    pending_decisions: list[str],
    decisions: dict[str, Any],
    run_dir: Path,
    round_dir: Path,
    log_path: Path,
    goal_model_path: Path | None,
    condition_config_path: Path,
    shared_base: dict[str, Any],
    variant_scope: dict[str, Any],
    steps: tuple[int, ...] | list[int],
    started_at: str,
    finished_at: str,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Assembles the manifest dict. Pure — writing is `write_manifest`'s job — so a driver can
    inspect or extend it before it lands."""
    taxonomy_dir = round_dir / "05_taxonomy"
    assignment_dir = round_dir / "06_assignment"

    manifest: dict[str, Any] = {
        "schema": "icpm2027/manifest/1",
        "protocol_version": protocol_version,
        "experiment": experiment,
        "condition_id": condition_id,
        "dataset": dataset_id,
        "arm": arm,
        "replicate": replicate,
        "tag": tag,
        "steps_executed": list(steps),
        "started_at": started_at,
        "finished_at": finished_at,
        # False whenever the run was launched with --allow-pending-decisions. A reader must be
        # able to tell a pre-registered run from one made under a recommended default that had
        # not yet been chosen (EXPERIMENTATION_PLAN.md §12, Tasks C7/C10).
        "preregistered": preregistered,
        "pending_decisions": pending_decisions,
        "decisions": decisions,
        "variant_scope": variant_scope,
        "inputs": {
            "event_log": file_record(log_path),
            "goal_model": file_record(goal_model_path) if goal_model_path else None,
            "goal_model_absent_by_design": goal_model_path is None,
            "condition_config": file_record(condition_config_path),
            "prompt_templates": dir_record(_PROMPT_TEMPLATE_DIR, "prompt_*.txt"),
            "shared_base": shared_base,
        },
        "prompts_sent": {
            "taxonomy_prompt": file_record(taxonomy_dir / "taxonomy_prompt.txt"),
            "assignment_prompts": dir_record(assignment_dir / "assignment_prompts", "*.txt"),
        },
        "llm": {
            "seed": None,
            "seed_note": _SEED_NOTE,
            "taxonomy": _resolved_llm_from_metadata(taxonomy_dir / "taxonomy_run_metadata.json"),
            "assignment": _resolved_llm_from_metadata(assignment_dir / "assignment_run_metadata.json"),
            "description": _resolved_llm_from_metadata(
                round_dir / "08_description" / "description_run_metadata.json"
            ),
        },
        "outputs": {
            "taxonomy": file_record(taxonomy_dir / "taxonomy.json"),
            "assignments": file_record(assignment_dir / "assignments.csv"),
            "discovery_metrics": file_record(round_dir / "07_discovery" / "discovery_metrics.csv"),
            "descriptions": file_record(round_dir / "08_description" / "descriptions.csv"),
        },
        "run_dir": _relative(run_dir),
        "round_dir": _relative(round_dir),
        "environment": environment_record(),
    }
    if extra:
        manifest.update(extra)
    return manifest


def write_manifest(manifest: dict[str, Any], run_dir: Path) -> Path:
    run_dir.mkdir(parents=True, exist_ok=True)
    path = run_dir / MANIFEST_FILENAME
    path.write_text(json.dumps(manifest, indent=2, sort_keys=False), encoding="utf-8")
    (run_dir / MANIFEST_MD_FILENAME).write_text(render_manifest_markdown(manifest), encoding="utf-8")
    return path


def read_manifest(run_dir: Path) -> dict[str, Any]:
    path = run_dir / MANIFEST_FILENAME
    if not path.exists():
        raise FileNotFoundError(f"No manifest at {path} — was this run executed by the icpm2027 drivers?")
    return json.loads(path.read_text(encoding="utf-8"))


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _short(value: Any, width: int = 16) -> str:
    if value is None:
        return "—"
    text = str(value)
    return text[:width] if len(text) > width else text


def render_manifest_markdown(manifest: dict[str, Any]) -> str:
    """A one-screen summary of the manifest, for a reader auditing a run directory by hand.
    Presented as tables per the project's readability convention; the JSON stays authoritative."""
    inputs = manifest["inputs"]
    log = inputs.get("event_log") or {}
    goal = inputs.get("goal_model") or {}
    config = inputs.get("condition_config") or {}
    outputs = manifest["outputs"]

    lines = [
        f"# Run manifest — `{manifest['condition_id']}`",
        "",
        f"Experiment `{manifest['experiment']}` · dataset `{manifest['dataset']}` · arm "
        f"`{manifest['arm']}` · replicate {manifest['replicate']}"
        + (f" · tag `{manifest['tag']}`" if manifest.get("tag") else ""),
        "",
        f"Protocol version `{manifest['protocol_version']}` · steps "
        f"{manifest['steps_executed']} · {manifest['started_at']} → {manifest['finished_at']}",
        "",
    ]

    if not manifest.get("preregistered", True):
        lines += [
            "> **Not pre-registered.** This run was launched with `--allow-pending-decisions` "
            "while the following decisions were still open: "
            + ", ".join(manifest.get("pending_decisions") or ["(none recorded)"])
            + ". It must not be reported as a frozen result without re-running under a closed "
            "pre-registration.",
            "",
        ]

    lines += [
        "## Inputs",
        "",
        "| Element | Path | SHA-256 (first 16) |",
        "|---|---|---|",
        f"| Event log | `{log.get('path', '—')}` | `{_short(log.get('sha256'))}` |",
    ]
    if manifest["inputs"].get("goal_model_absent_by_design"):
        lines.append("| Goal model | *(absent by design — open arm)* | — |")
    else:
        lines.append(f"| Goal model | `{goal.get('path', '—')}` | `{_short(goal.get('sha256'))}` |")
    lines += [
        f"| Condition config | `{config.get('path', '—')}` | `{_short(config.get('sha256'))}` |",
        "",
        "**Prompt templates:** "
        + ", ".join(f"`{name}`=`{_short(h, 12)}`" for name, h in inputs["prompt_templates"].items()),
        "",
        "**Shared Steps 1-4 base:** "
        + json.dumps(inputs["shared_base"].get("run_id"))
        + " — "
        + ", ".join(
            f"`{name}`=`{_short(h, 12)}`" for name, h in (inputs["shared_base"].get("artifacts") or {}).items()
        ),
        "",
        "## Variant scope",
        "",
        "```json",
        json.dumps(manifest["variant_scope"], indent=2),
        "```",
        "",
        "## LLM",
        "",
        f"Seed: {manifest['llm']['seed_note']}",
        "",
        "```json",
        json.dumps({k: v for k, v in manifest["llm"].items() if k not in ("seed", "seed_note")}, indent=2),
        "```",
        "",
        "## Outputs",
        "",
        "| Artifact | Path | SHA-256 (first 16) |",
        "|---|---|---|",
    ]
    for name, record in outputs.items():
        if record is None:
            lines.append(f"| {name} | *(not produced)* | — |")
        else:
            lines.append(f"| {name} | `{record['path']}` | `{_short(record['sha256'])}` |")

    env = manifest["environment"]
    lines += [
        "",
        "## Environment",
        "",
        f"`{env['host']}` · {env['platform']} · Python {env['python']} · git "
        f"`{_short(env.get('git_commit'), 12)}`"
        + (" **(working tree dirty)**" if env.get("git_dirty") else ""),
        "",
    ]
    return "\n".join(lines)

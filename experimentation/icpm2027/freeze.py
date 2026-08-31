"""Verification of the freeze table (`configs/protocol.yaml`) against what actually ran.

`protocol.py` makes the two arms of a pair identical *by construction*; this module checks that
claim against the artifacts on disk afterwards, from their manifests alone. The two are not
redundant: construction can only guarantee what the driver controls, while the manifests record
what the pipeline actually consumed — including the Steps 1-4 artifact hashes, which is the only
way to demonstrate the freeze table's bolded **identical** narrative-sample row rather than assert
it.

The output is the freeze table itself, row by row, with a verdict per row, written next to the
experiment's other cross-run artifacts. A failing row is a reason not to report the pair, and the
report says which manifests disagreed and how.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable

from goalcat.atomic_io import atomic_write_json, atomic_write_text

from .manifest import read_manifest


@dataclass(frozen=True)
class FreezeCheck:
    """One freeze-table row: what it is, what each condition reported, and whether they agree."""

    element: str
    requirement: str
    values: dict[str, Any]
    passed: bool
    note: str = ""


def _extract(manifest: dict, path: tuple[str, ...], default: Any = None) -> Any:
    node: Any = manifest
    for key in path:
        if not isinstance(node, dict) or key not in node:
            return default
        node = node[key]
    return node


def _identical(manifests: dict[str, dict], getter: Callable[[dict], Any]) -> tuple[dict[str, Any], bool]:
    values = {label: getter(m) for label, m in manifests.items()}
    distinct = {json.dumps(v, sort_keys=True, default=str) for v in values.values()}
    return values, len(distinct) <= 1


def _config_of(manifest: dict) -> dict:
    """The LLM/assignment settings a manifest records, flattened for comparison."""
    return {
        "assignment_batch_size": manifest.get("assignment_batch_size"),
        "protocol_version": manifest.get("protocol_version"),
    }


def _llm_configurations(manifest: dict) -> Any:
    """The distinct (model, provider, temperature) tuples the provider actually reported for this
    run's Step 5 and Step 6 calls — not the requested strings from the config, which would make
    this check circular."""
    out = []
    for role in ("taxonomy", "assignment"):
        record = _extract(manifest, ("llm", role)) or {}
        for call_config in record.get("distinct_call_configurations", []):
            entry = {
                "role": role,
                "model": call_config.get("model"),
                "resolved_model": call_config.get("resolved_model"),
                "provider": call_config.get("provider"),
                "temperature": call_config.get("temperature"),
            }
            if entry not in out:
                out.append(entry)
    # Step 5 and Step 6 use separately-configured models; comparison across conditions is on the
    # (role -> configuration) mapping, so a pair differing only in which role used which model
    # still fails, as it should.
    return sorted(out, key=lambda e: (e["role"], str(e["model"])))


def check_pair(manifests: dict[str, dict], *, perturbed: bool = False) -> list[FreezeCheck]:
    """Runs every freeze-table row across two or more conditions of one within-log pair.

    `manifests` maps a display label (e.g. "guided_rep1") to that condition's parsed manifest.

    `perturbed` inverts the goal-model row for an Experiment 2 comparison, where the goal model is
    the one thing that is *supposed* to differ: the requirement becomes that every guided condition
    read a *distinct* model, since two perturbations sharing a file would mean one of them did not
    write the edit it claims. Every other row still demands identity — that is the point of running
    this on E2 at all, and it is what would have caught each perturbed run using a newer
    `prompt_assignment_batch.txt` than the baseline it was measured against.
    """
    checks: list[FreezeCheck] = []

    def add(element: str, requirement: str, getter: Callable[[dict], Any], note: str = "") -> None:
        values, ok = _identical(manifests, getter)
        checks.append(FreezeCheck(element, requirement, values, ok, note))

    add("XES", "identical", lambda m: _extract(m, ("inputs", "event_log", "sha256")))
    add(
        "Variant extraction",
        "identical",
        lambda m: _extract(m, ("inputs", "shared_base", "artifacts", "01_variants/variants.csv")),
        note="Hash of the shared base's variants.csv, inherited by copy (inputs.py).",
    )
    add(
        "Multi-view profiles",
        "identical",
        lambda m: [
            _extract(m, ("inputs", "shared_base", "artifacts", "02_profiling/profiles.csv")),
            _extract(m, ("inputs", "shared_base", "artifacts", "02_profiling/profiles.json")),
        ],
    )
    add(
        "Narratives",
        "identical",
        lambda m: _extract(m, ("inputs", "shared_base", "artifacts", "03_textualization/narratives.csv")),
    )
    add(
        "Narrative sample",
        "IDENTICAL (bolded in §2.2)",
        lambda m: _extract(m, ("inputs", "shared_base", "artifacts", "04_sampling/narrative_sample.csv")),
        note="The row the design turns on: both arms consume one Step 4 output, copied, not recomputed.",
    )
    add("LLM / provider / model", "same", _llm_configurations, note="Read from the provider's own per-call echo.")
    add(
        "LLM parameters (temperature, seed)",
        "same",
        lambda m: {
            "temperature": [c["temperature"] for c in _llm_configurations(m)],
            "seed": _extract(m, ("llm", "seed")),
        },
        note="Seed is null throughout — no seed is exposed by this provider path (see manifest.py).",
    )
    add("Assignment mechanism", "same", lambda m: sorted(_extract(m, ("inputs", "prompt_templates"), {}).items()),
        note="Prompt-template set hashed as a whole; a wording change to any template fails this row.")
    add("Assignment batch size (Task C10)", "same", lambda m: m.get("assignment_batch_size"))
    axis_values = {label: m.get("axis") for label, m in manifests.items()}
    # Every arm that reads a goal model carries an axis, which is `guided_no_sample` as well as
    # `guided`. Keyed on the manifest's own goal-model record rather than on an arm-name list, so a
    # future arm cannot silently fall on the wrong side of this row.
    guided_axes = {
        label: value
        for label, value in axis_values.items()
        if not manifests[label].get("inputs", {}).get("goal_model_absent_by_design", True)
    }
    checks.append(
        FreezeCheck(
            element="Categorization axis",
            requirement="same across guided conditions (absent in open, by design)",
            values=axis_values,
            passed=len(set(guided_axes.values())) <= 1
            and all(axis_values[label] is None for label in axis_values if label not in guided_axes),
            note="Two guided conditions that induce against different Or frontiers partition "
            "different things and are not a paired comparison. The open arm carries no axis for "
            "the same reason it carries no goal model, and one open run serves every axis. Null "
            "throughout on a dataset declaring a single axis.",
        )
    )
    add("Variant scope (Task C7)", "same", lambda m: _extract(m, ("variant_scope", "variants_kept")))
    add("Protocol version", "same", lambda m: m.get("protocol_version"))

    # The goal-model row is the one that must *differ*, in a specific direction.
    goal_models = {
        label: {
            "arm": m.get("arm"),
            "sha256": _extract(m, ("inputs", "goal_model", "sha256")),
            "absent_by_design": _extract(m, ("inputs", "goal_model_absent_by_design")),
        }
        for label, m in manifests.items()
    }
    guided_hashes = {
        label: v["sha256"] for label, v in goal_models.items() if v["arm"] == "guided"
    }
    open_absent = all(
        v["absent_by_design"] for v in goal_models.values() if v["arm"] in ("open", "label_list")
    )
    if perturbed:
        guided_ok = bool(guided_hashes) and len(set(guided_hashes.values())) == len(guided_hashes) and all(guided_hashes.values())
        requirement = "present, and distinct per perturbation"
        note = (
            "Experiment 2's one intended difference. Every guided condition must read a distinct, "
            "present goal model: two conditions sharing a file means a perturbation did not write "
            "the edit it claims to test."
        )
    else:
        guided_ok = bool(guided_hashes) and len(set(guided_hashes.values())) == 1 and all(guided_hashes.values())
        requirement = "present and frozen (guided) / absent (open)"
        note = (
            "Guided arms must all read one identical goal-model file; open and label-list "
            "arms must have none configured at all — not merely be set to ignore one."
        )
    checks.append(
        FreezeCheck(
            element="Goal model",
            requirement=requirement,
            values=goal_models,
            passed=guided_ok and open_absent,
            note=note,
        )
    )

    # Pre-registration status is not a freeze-table row but governs whether the pair is reportable.
    prereg_values = {label: m.get("preregistered") for label, m in manifests.items()}
    checks.append(
        FreezeCheck(
            element="Pre-registration (§12)",
            requirement="all conditions pre-registered",
            values=prereg_values,
            passed=all(bool(v) for v in prereg_values.values()),
            note="False means the run was launched with --allow-pending-decisions.",
        )
    )
    return checks


def check_run_dirs(run_dirs: dict[str, Path], *, perturbed: bool = False) -> list[FreezeCheck]:
    return check_pair(
        {label: read_manifest(path) for label, path in run_dirs.items()}, perturbed=perturbed
    )


def render_freeze_report(title: str, checks: Iterable[FreezeCheck]) -> str:
    checks = list(checks)
    failed = [c for c in checks if not c.passed]
    lines = [
        f"# Freeze verification — {title}",
        "",
        "The frozen protocol's freeze table, verified against the conditions' manifests rather "
        "than against the driver's intent.",
        "",
        f"**{len(checks) - len(failed)}/{len(checks)} rows pass.**"
        + ("" if not failed else f" Failing: {', '.join(c.element for c in failed)}."),
        "",
        "| Element | Requirement | Verdict |",
        "|---|---|---|",
    ]
    for check in checks:
        lines.append(f"| {check.element} | {check.requirement} | {'PASS' if check.passed else '**FAIL**'} |")

    lines += ["", "## Per-row detail", ""]
    for check in checks:
        lines += [
            f"### {check.element} — {'PASS' if check.passed else '**FAIL**'}",
            "",
            f"Requirement: *{check.requirement}*",
            "",
        ]
        if check.note:
            lines += [check.note, ""]
        lines += ["```json", json.dumps(check.values, indent=2, default=str), "```", ""]
    return "\n".join(lines)


def write_freeze_report(title: str, checks: Iterable[FreezeCheck], out_dir: Path, stem: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    checks = list(checks)
    path = out_dir / f"{stem}.md"
    atomic_write_text(path, render_freeze_report(title, checks))
    atomic_write_json(
        out_dir / f"{stem}.json",
        [
            {"element": c.element, "requirement": c.requirement, "passed": c.passed, "values": c.values, "note": c.note}
            for c in checks
        ],
        default=str,
    )
    return path

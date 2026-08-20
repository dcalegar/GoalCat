"""The frozen protocol: what every ICPM 2027 run holds identical, and what it is allowed to vary.

This module is the single place that turns `configs/protocol.yaml` + `configs/<dataset>.yaml` +
`configs/preregistration.yaml` into a concrete, executable `PipelineConfig`-shaped YAML for one
experimental condition. Nothing else in this package writes a pipeline config, so the freeze table
(EXPERIMENTATION_PLAN.md §2.2) is enforced by construction rather than by discipline: an
intent-guided condition and its paired open condition are generated from one protocol dict and can
differ only in the two fields `condition_overrides()` is permitted to touch.

Two auditability rules are implemented here rather than left to the operator:

1. **Pre-registration gate.** A decision the plan requires to be fixed before execution (Tasks C7,
   C10, C5, C6, D6) blocks the run it governs while it is still `status: pending`, unless the
   driver passes ``allow_pending=True`` — which stamps the manifest ``preregistered: false`` so a
   run made under a not-yet-fixed decision can never be mistaken for one made under a fixed one.
2. **Generated configs are artifacts.** Each condition's rendered YAML is written into that
   condition's own run directory and hashed into its manifest, so "which settings produced this
   output" is answerable from the output alone.
"""

from __future__ import annotations

import dataclasses
from pathlib import Path
from typing import Any, Literal

import yaml

from goalcat.config import REPO_ROOT

CONFIGS_DIR = Path(__file__).resolve().with_name("configs")
PROTOCOL_PATH = CONFIGS_DIR / "protocol.yaml"
PREREGISTRATION_PATH = CONFIGS_DIR / "preregistration.yaml"

#: Where cross-run artifacts (manifests, freeze checks, analysis) go — a sibling of the per-log
#: run directories under data/output/, so a frozen experiment's bookkeeping never has to be
#: reassembled by guessing which run_ids belonged together.
EXPERIMENT_ROOT = REPO_ROOT / "data" / "output" / "icpm2027"

#: Goal-model perturbations (Experiment 2) are written here, never over the frozen base model.
PERTURBED_GOALS_DIRNAME = "perturbed"

DATASET_IDS = ("rtfm", "sepsis", "bpic2019")

Arm = Literal["guided", "open", "label_list"]

#: taxonomy_mode each arm runs under. "label_list" (Task C5's control) is an open induction over a
#: supplied label list, so it runs the same pipeline mode as "open" and differs in its prompt-side
#: input, not in the pipeline switch — see conditions.py.
_TAXONOMY_MODE_BY_ARM: dict[str, str] = {
    "guided": "intent_guided",
    "open": "open",
    "label_list": "open",
}


class PreRegistrationError(RuntimeError):
    """Raised when a frozen run is attempted while a decision governing it is still pending."""


@dataclasses.dataclass(frozen=True)
class Protocol:
    """configs/protocol.yaml, parsed. Immutable: a driver must never mutate the protocol to make
    a run fit."""

    version: str
    sampling: dict[str, int]
    discovery: dict[str, float]
    llm: dict[str, Any]
    steps: dict[str, list[int]]
    replicates: dict[str, int]

    @classmethod
    def load(cls, path: Path = PROTOCOL_PATH) -> "Protocol":
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        return cls(
            version=raw["protocol_version"],
            sampling=raw["sampling"],
            discovery=raw["discovery"],
            llm=raw["llm"],
            steps=raw["steps"],
            replicates=raw["replicates"],
        )


@dataclasses.dataclass(frozen=True)
class Decision:
    key: str
    task: str
    question: str
    governs: tuple[str, ...]
    status: str
    value: Any
    decided_on: str | None
    rationale: str

    @property
    def is_decided(self) -> bool:
        return self.status == "decided"


@dataclasses.dataclass(frozen=True)
class PreRegistration:
    """configs/preregistration.yaml, parsed — the §13 open decisions plus the ones already closed.

    `require(...)` is the gate: it is called by every driver before any LLM call is made for a
    frozen run, not after, so a pending decision costs nothing to discover.
    """

    decisions: dict[str, Decision]

    @classmethod
    def load(cls, path: Path = PREREGISTRATION_PATH) -> "PreRegistration":
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        decisions = {
            key: Decision(
                key=key,
                task=entry["task"],
                question=entry["question"],
                governs=tuple(entry.get("governs", ())),
                status=entry["status"],
                value=entry["value"],
                decided_on=entry.get("decided_on"),
                rationale=entry.get("rationale", ""),
            )
            for key, entry in raw["decisions"].items()
        }
        return cls(decisions=decisions)

    def get(self, key: str) -> Decision:
        if key not in self.decisions:
            raise KeyError(f"No pre-registered decision named {key!r} in {PREREGISTRATION_PATH}")
        return self.decisions[key]

    def governing(self, dataset_id: str) -> list[Decision]:
        return [d for d in self.decisions.values() if dataset_id in d.governs]

    def pending_for(self, dataset_id: str) -> list[Decision]:
        return [d for d in self.governing(dataset_id) if not d.is_decided]

    def require(self, dataset_id: str, allow_pending: bool = False) -> list[Decision]:
        """Gate a frozen run on this dataset. Returns the still-pending decisions (empty unless
        allow_pending); raises PreRegistrationError naming every one of them otherwise."""
        pending = self.pending_for(dataset_id)
        if pending and not allow_pending:
            lines = [
                f"Cannot launch a frozen ICPM 2027 run for {dataset_id!r}: "
                f"{len(pending)} decision(s) governing it are still pending in "
                f"{PREREGISTRATION_PATH}.",
                "",
                "EXPERIMENTATION_PLAN.md §12 requires these to be fixed *before* execution, so "
                "they cannot be chosen after seeing this run's categorization output.",
                "",
            ]
            for d in pending:
                lines.append(f"  - {d.key} (Task {d.task}): {' '.join(d.question.split())}")
                lines.append(f"      current recommended value: {d.value!r}")
            lines += [
                "",
                "Set each one's `value`, `status: decided`, `decided_on`, and `rationale`, or "
                "re-run with --allow-pending-decisions to proceed with the recommended defaults "
                "(the run's manifest is then stamped preregistered=false).",
            ]
            raise PreRegistrationError("\n".join(lines))
        return pending


@dataclasses.dataclass(frozen=True)
class DatasetSpec:
    """configs/<dataset>.yaml, parsed."""

    dataset_id: str
    log_filename: str
    goal_model_filename: str
    case_id_key: str
    activity_key: str
    timestamp_key: str
    resource_key: str
    role: str
    variant_scope: dict[str, Any]
    heldout_case_attribute: str | None

    @classmethod
    def load(cls, dataset_id: str) -> "DatasetSpec":
        path = CONFIGS_DIR / f"{dataset_id}.yaml"
        if not path.exists():
            raise FileNotFoundError(
                f"No dataset spec for {dataset_id!r} (looked for {path}). Known: {', '.join(DATASET_IDS)}."
            )
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        return cls(
            dataset_id=raw["dataset_id"],
            log_filename=raw["log_filename"],
            goal_model_filename=raw["goal_model_filename"],
            case_id_key=raw["case_id_key"],
            activity_key=raw["activity_key"],
            timestamp_key=raw["timestamp_key"],
            resource_key=raw["resource_key"],
            role=raw["role"],
            variant_scope=raw["variant_scope"],
            heldout_case_attribute=raw.get("heldout_case_attribute"),
        )

    @property
    def log_stem(self) -> str:
        name = self.log_filename
        for suffix in (".xes.gz", ".xes"):
            if name.endswith(suffix):
                return name[: -len(suffix)]
        return Path(name).stem

    @property
    def log_path(self) -> Path:
        return REPO_ROOT / "data" / "logs" / self.log_filename

    @property
    def goal_model_path(self) -> Path:
        return REPO_ROOT / "data" / "goals" / self.goal_model_filename


@dataclasses.dataclass(frozen=True)
class ConditionSpec:
    """One executable cell of the design: which dataset, which arm, which goal model (a
    perturbation writes its own), which replicate, which pipeline steps.

    `tag` names a non-baseline variation of the arm — an Experiment 2 perturbation
    ("pertA_tb", "pertB_tb_tc"), or Task C5's label-list control. It is part of the run_id, so a
    perturbed run can never overwrite the unperturbed one it is compared against.
    """

    dataset: DatasetSpec
    arm: Arm
    replicate: int = 1
    tag: str | None = None
    goal_model_filename: str | None = None
    steps: tuple[int, ...] = (5, 6)
    label_list: tuple[str, ...] = ()
    experiment: str = "e1"

    @property
    def taxonomy_mode(self) -> str:
        return _TAXONOMY_MODE_BY_ARM[self.arm]

    @property
    def effective_goal_model_filename(self) -> str | None:
        """The goal model this condition actually reads.

        The open arm gets None, not the dataset's model: config.yaml's own comment notes Step 5a
        reads goal_model_filename "even if taxonomy_mode is later switched to open", so leaving it
        populated in an open condition would leave a live path to the very artifact the arm is
        defined by not having. The freeze table's "Goal model: absent" row is enforced here.
        """
        if self.arm != "guided":
            return None
        return self.goal_model_filename or self.dataset.goal_model_filename

    @property
    def condition_id(self) -> str:
        parts = [self.experiment, self.arm]
        if self.tag:
            parts.append(self.tag)
        parts.append(f"rep{self.replicate}")
        return "_".join(parts)

    @property
    def run_id(self) -> str:
        """Doubles as the run directory name under data/output/<log_stem>/ — deliberately
        self-describing rather than a timestamp, so a frozen run is identifiable on disk without
        cross-referencing a manifest."""
        return f"icpm2027_{self.condition_id}"

    @property
    def run_dir(self) -> Path:
        return REPO_ROOT / "data" / "output" / self.dataset.log_stem / self.run_id


def shared_base_run_id(dataset: DatasetSpec) -> str:
    """The Steps 1-4 execution every condition of this dataset draws its inputs from (§2.1: Steps
    1-4 run *once* per dataset, then feed both arms)."""
    return "icpm2027_base"


def shared_base_dir(dataset: DatasetSpec) -> Path:
    return REPO_ROOT / "data" / "output" / dataset.log_stem / shared_base_run_id(dataset)


def resolve_variant_scope(dataset: DatasetSpec, prereg: PreRegistration) -> dict[str, Any]:
    """Resolves a dataset's variant-scope policy, following a `from_preregistration` indirection
    to the Task C7 decision. Returns the policy dict plus the provenance of where it came from."""
    scope = dict(dataset.variant_scope)
    if scope.get("policy") != "from_preregistration":
        return {**scope, "source": f"configs/{dataset.dataset_id}.yaml"}
    decision = prereg.get(scope["decision"])
    return {
        **decision.value,
        "source": f"preregistration.yaml:{decision.key}",
        "preregistered": decision.is_decided,
        "decided_on": decision.decided_on,
    }


def resolve_assignment_batch_size(dataset: DatasetSpec, protocol: Protocol, prereg: PreRegistration) -> int:
    """Task C10: one protocol value, plus any pre-registered per-dataset exception. An exception
    that is not pre-registered is still applied (the gate above is what refuses the run), but it
    is recorded in the manifest with its pending status, never silently."""
    decision = prereg.get("C10_assignment_batch_size")
    value = decision.value
    exceptions = value.get("exceptions") or {}
    if dataset.dataset_id in exceptions:
        return int(exceptions[dataset.dataset_id])
    return int(value.get("default", protocol.llm["assignment_batch_size"]))


def steps_for(arm: Arm, protocol: Protocol, prereg: PreRegistration) -> tuple[int, ...]:
    """Which pipeline steps a condition on this arm runs — Task D6. Step 9 is never included:
    §3 step 7 requires the paired comparison to happen before any analyst refinement."""
    decision = prereg.get("D6_open_arm_steps_7_9")
    policy = decision.value
    if policy == "run_both":
        return tuple(protocol.steps["with_descriptive"])
    if policy == "run_guided_only":
        return tuple(protocol.steps["with_descriptive"] if arm == "guided" else protocol.steps["default"])
    return tuple(protocol.steps["default"])


def render_condition_config(
    condition: ConditionSpec, protocol: Protocol, prereg: PreRegistration
) -> dict[str, Any]:
    """The full pipeline config for one condition, as a plain dict ready to be dumped as YAML.

    Everything except `taxonomy_mode` and `goal_model_filename` comes from the dataset spec and
    the protocol — the two arms of a pair are therefore identical by construction on every row the
    freeze table marks identical, and freeze.py re-verifies that against what actually landed on
    disk rather than trusting this function.
    """
    llm = dict(protocol.llm)
    llm["assignment_batch_size"] = resolve_assignment_batch_size(condition.dataset, protocol, prereg)

    return {
        "log_filename": condition.dataset.log_filename,
        "goal_model_filename": condition.effective_goal_model_filename,
        "output_dir": "data/output",
        "run_id": condition.run_id,
        "round": 1,
        "case_id_key": condition.dataset.case_id_key,
        "activity_key": condition.dataset.activity_key,
        "timestamp_key": condition.dataset.timestamp_key,
        "resource_key": condition.dataset.resource_key,
        **protocol.sampling,
        "taxonomy_mode": condition.taxonomy_mode,
        **protocol.discovery,
        "llm": llm,
    }


_CONFIG_HEADER = """\
# GENERATED — do not edit. Written by experimentation/icpm2027/protocol.py for one frozen
# experimental condition, and hashed into that condition's manifest. Edit configs/protocol.yaml,
# configs/<dataset>.yaml, or configs/preregistration.yaml and re-generate instead; editing this
# file makes the run's manifest a record of settings that were not the ones used.
#
# Condition: {condition_id} | dataset: {dataset_id} | protocol version: {protocol_version}
"""


def write_condition_config(
    condition: ConditionSpec, protocol: Protocol, prereg: PreRegistration, path: Path | None = None
) -> Path:
    """Renders and writes this condition's config into its own run directory, returning the path.

    Deliberately inside the run directory, not in configs/: the config that produced a run is part
    of that run's evidence, and a replication package a reader receives should not require them to
    reconstruct it from three source files plus a resolution order.
    """
    target = path or (condition.run_dir / "condition_config.yaml")
    target.parent.mkdir(parents=True, exist_ok=True)
    header = _CONFIG_HEADER.format(
        condition_id=condition.condition_id,
        dataset_id=condition.dataset.dataset_id,
        protocol_version=protocol.version,
    )
    body = yaml.safe_dump(render_condition_config(condition, protocol, prereg), sort_keys=False)
    target.write_text(header + "\n" + body, encoding="utf-8")
    return target

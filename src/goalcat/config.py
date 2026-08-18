from __future__ import annotations

import dataclasses
from datetime import datetime
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_CONFIG_PATH = Path(__file__).resolve().with_name("config.yaml")


@dataclasses.dataclass
class LLMConfig:
    taxonomy_model: str
    assignment_model: str
    description_model: str
    temperature: float
    timeout_seconds: int
    max_retries: int
    concurrency: int
    requests_per_minute: int | None


@dataclasses.dataclass
class PipelineConfig:
    log_filename: str
    goal_model_filename: str | None
    output_dir: Path
    case_id_key: str
    activity_key: str
    timestamp_key: str
    resource_key: str
    sample_frequent_n: int
    sample_rare_n: int
    sample_extreme_n: int
    taxonomy_mode: str
    discovery_noise_threshold: float
    llm: LLMConfig
    run_id: str

    @property
    def log_path(self) -> Path:
        return REPO_ROOT / "data" / "logs" / self.log_filename

    @property
    def goal_model_path(self) -> Path | None:
        if self.goal_model_filename is None:
            return None
        return REPO_ROOT / "data" / "goals" / self.goal_model_filename

    @property
    def log_stem(self) -> str:
        name = self.log_path.name
        for suffix in (".xes.gz", ".xes"):
            if name.endswith(suffix):
                return name[: -len(suffix)]
        return self.log_path.stem

    @property
    def log_output_dir(self) -> Path:
        """Directory holding every run of this log, one timestamped subdirectory per run."""
        return self.output_dir / self.log_stem

    @property
    def run_output_dir(self) -> Path:
        """This run's directory: fresh and empty for a new run_id, or an existing directory to
        resume/extend when run_id names one already on disk — each step reads whatever's already
        there instead of recomputing it (see the *_get_or_build_* helpers in pipeline.py)."""
        return self.log_output_dir / self.run_id


def load_config(config_path: str | Path | None = None, run_id: str | None = None) -> PipelineConfig:
    """Loads config.yaml.

    run_id picks which run directory this config points at, in priority order: the run_id
    argument (for a caller chaining several steps that must share one directory), then
    config.yaml's own run_id field (to point a standalone call at an existing run directory —
    e.g. set it to a prior Step 5 run's id before calling Step 6, and every step reads whatever
    it needs from that directory instead of recomputing it), then a fresh timestamp (a new,
    empty run directory — the default, and what running the full pipeline from scratch gets).
    """
    path = Path(config_path) if config_path is not None else _DEFAULT_CONFIG_PATH
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    return PipelineConfig(
        log_filename=raw["log_filename"],
        goal_model_filename=raw.get("goal_model_filename"),
        output_dir=_resolve(raw["output_dir"]),
        case_id_key=raw["case_id_key"],
        activity_key=raw["activity_key"],
        timestamp_key=raw["timestamp_key"],
        resource_key=raw["resource_key"],
        sample_frequent_n=raw["sample_frequent_n"],
        sample_rare_n=raw["sample_rare_n"],
        sample_extreme_n=raw["sample_extreme_n"],
        taxonomy_mode=raw["taxonomy_mode"],
        discovery_noise_threshold=raw["discovery_noise_threshold"],
        llm=LLMConfig(
            taxonomy_model=raw["llm"]["taxonomy_model"],
            assignment_model=raw["llm"]["assignment_model"],
            description_model=raw["llm"]["description_model"],
            temperature=raw["llm"]["temperature"],
            timeout_seconds=raw["llm"]["timeout_seconds"],
            max_retries=raw["llm"]["max_retries"],
            concurrency=raw["llm"]["concurrency"],
            requests_per_minute=raw["llm"].get("requests_per_minute"),
        ),
        run_id=run_id or raw.get("run_id") or datetime.now().strftime("%Y%m%d_%H%M%S"),
    )


def load_prompt_template(name: str) -> str:
    """Reads a prompt template from data/templates/<name>.

    Kept as plain str.format()-style text files, not Jinja2 — editing prompt wording is then a
    data change, not a code change, while Jinja2 itself stays walled off to the vendored LUPIN
    module per its isolation contract (see third_party/lupin/README.md).
    """
    return (REPO_ROOT / "data" / "templates" / name).read_text(encoding="utf-8")


def config_snapshot_dict(config: PipelineConfig) -> dict:
    """A JSON-serializable snapshot of config, excluding run_id (which matches by construction
    whenever this is being compared). Used to detect config drift when a run directory is
    reused across separate invocations — see run_logging.py's _snapshot_or_check_config()."""
    data = dataclasses.asdict(config)
    data.pop("run_id", None)
    data["output_dir"] = str(data["output_dir"])
    return data


def new_run_id() -> str:
    """A fresh run id, in the same format load_config() generates on its own.

    For a caller that chains several steps and needs them all to share one run directory —
    generate one run_id here, then pass it to every load_config()/run_stepN_*() call in the chain.
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _resolve(relative_path: str) -> Path:
    path = Path(relative_path)
    return path if path.is_absolute() else REPO_ROOT / path

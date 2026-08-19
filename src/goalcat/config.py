from __future__ import annotations

import dataclasses
from datetime import datetime
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_CONFIG_PATH = Path(__file__).resolve().with_name("config.yaml")

# Folder-naming scheme for a run directory (see PROGRESS.md's output-reorg entry). Steps 1-4 are
# execution-scoped (computed once, never per-round); Steps 5-9 are round-scoped, nested under
# ROUND_PREFIX + round number; FINAL_DIRNAME and REVIEW_INDEX_FILENAME are execution-scoped
# siblings of the round folders. Exported as module-level constants (not just baked into
# PipelineConfig's properties) since review.py needs them to address sibling rounds directly.
VARIANTS_DIRNAME = "01_variants"
PROFILING_DIRNAME = "02_profiling"
TEXTUALIZATION_DIRNAME = "03_textualization"
SAMPLING_DIRNAME = "04_sampling"
TAXONOMY_DIRNAME = "05_taxonomy"
ASSIGNMENT_DIRNAME = "06_assignment"
DISCOVERY_DIRNAME = "07_discovery"
DESCRIPTION_DIRNAME = "08_description"
REVIEW_DIRNAME = "09_review"
FINAL_DIRNAME = "final"
ROUND_PREFIX = "round"
REVIEW_INDEX_FILENAME = "review_index.md"


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
    round: int

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
        """Directory holding every execution of this log, one timestamped subdirectory per run_id."""
        return self.output_dir / self.log_stem

    @property
    def run_output_dir(self) -> Path:
        """This execution's directory: fresh and empty for a new run_id, or an existing directory
        to resume/extend when run_id names one already on disk. Steps 1-4's outputs live directly
        here (execution-scoped); Steps 5-9's outputs live under round_dir (round-scoped) — see
        PROGRESS.md's output-reorg entry for why revision rounds nest inside one execution instead
        of minting a new run_id each time."""
        return self.log_output_dir / self.run_id

    @property
    def round_dir(self) -> Path:
        """This round's directory within the execution — holds Steps 5-9's outputs."""
        return self.run_output_dir / f"{ROUND_PREFIX}{self.round}"

    # Execution-scoped (Steps 1-4, never vary by round).
    @property
    def variants_dir(self) -> Path:
        return self.run_output_dir / VARIANTS_DIRNAME

    @property
    def profiling_dir(self) -> Path:
        return self.run_output_dir / PROFILING_DIRNAME

    @property
    def textualization_dir(self) -> Path:
        return self.run_output_dir / TEXTUALIZATION_DIRNAME

    @property
    def sampling_dir(self) -> Path:
        return self.run_output_dir / SAMPLING_DIRNAME

    @property
    def final_dir(self) -> Path:
        return self.run_output_dir / FINAL_DIRNAME

    @property
    def review_index_path(self) -> Path:
        return self.run_output_dir / REVIEW_INDEX_FILENAME

    # Round-scoped (Steps 5-9).
    @property
    def taxonomy_dir(self) -> Path:
        return self.round_dir / TAXONOMY_DIRNAME

    @property
    def assignment_dir(self) -> Path:
        return self.round_dir / ASSIGNMENT_DIRNAME

    @property
    def discovery_dir(self) -> Path:
        return self.round_dir / DISCOVERY_DIRNAME

    @property
    def description_dir(self) -> Path:
        return self.round_dir / DESCRIPTION_DIRNAME

    @property
    def review_dir(self) -> Path:
        return self.round_dir / REVIEW_DIRNAME


def _detect_latest_round(run_output_dir: Path) -> int:
    """Scans an execution directory for existing roundN/ subfolders and returns the highest N,
    or 1 if none exist yet (a fresh execution). This is the "attach to latest, unless told
    otherwise" default that lets an ordinary Steps 5-9 call just operate on the current round
    without the caller tracking a number by hand — only start_revision_round() (review.py) ever
    explicitly requests round + 1."""
    if not run_output_dir.is_dir():
        return 1
    rounds = []
    for entry in run_output_dir.iterdir():
        if entry.is_dir() and entry.name.startswith(ROUND_PREFIX):
            suffix = entry.name[len(ROUND_PREFIX) :]
            if suffix.isdigit():
                rounds.append(int(suffix))
    return max(rounds) if rounds else 1


def load_config(
    config_path: str | Path | None = None, run_id: str | None = None, round: int | None = None
) -> PipelineConfig:
    """Loads config.yaml.

    run_id picks which execution directory this config points at, in priority order: the run_id
    argument (for a caller chaining several steps that must share one directory), then
    config.yaml's own run_id field, then a fresh timestamp (a new, empty execution — the default).

    round picks which round within that execution Steps 5-9 address — deliberately a *different*
    resolution order than run_id's, since the useful default here is "continue the current round,"
    not "start something new": the round argument, then config.yaml's own round field, then
    auto-detected as the highest existing roundN/ already on disk for this execution (or 1 for a
    fresh one). Steps 1-4 never read this field — they're execution-scoped, not round-scoped.
    """
    path = Path(config_path) if config_path is not None else _DEFAULT_CONFIG_PATH
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    resolved_run_id = run_id or raw.get("run_id") or datetime.now().strftime("%Y%m%d_%H%M%S")
    resolved_output_dir = _resolve(raw["output_dir"])
    resolved_log_stem = _log_stem_of(raw["log_filename"])
    resolved_run_output_dir = resolved_output_dir / resolved_log_stem / resolved_run_id
    resolved_round = round or raw.get("round") or _detect_latest_round(resolved_run_output_dir)

    return PipelineConfig(
        log_filename=raw["log_filename"],
        goal_model_filename=raw.get("goal_model_filename"),
        output_dir=resolved_output_dir,
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
        run_id=resolved_run_id,
        round=resolved_round,
    )


def _log_stem_of(log_filename: str) -> str:
    for suffix in (".xes.gz", ".xes"):
        if log_filename.endswith(suffix):
            return log_filename[: -len(suffix)]
    return Path(log_filename).stem


def load_prompt_template(name: str) -> str:
    """Reads a prompt template from data/templates/<name>.

    Kept as plain str.format()-style text files, not Jinja2 — editing prompt wording is then a
    data change, not a code change, while Jinja2 itself stays walled off to the vendored LUPIN
    module per its isolation contract (see third_party/lupin/README.md).
    """
    return (REPO_ROOT / "data" / "templates" / name).read_text(encoding="utf-8")


def config_snapshot_dict(config: PipelineConfig) -> dict:
    """A JSON-serializable snapshot of config, excluding run_id and round (both match by
    construction whenever this is being compared — round in particular must be excluded, or
    every new revision round would report false "config drift" purely because the round number
    advanced, even though nothing the user controls changed). Used to detect config drift when
    an execution directory is reused across separate invocations — see run_logging.py's
    _snapshot_or_check_config()."""
    data = dataclasses.asdict(config)
    data.pop("run_id", None)
    data.pop("round", None)
    data["output_dir"] = str(data["output_dir"])
    return data


def new_run_id() -> str:
    """A fresh run id, in the same format load_config() generates on its own.

    For a caller that chains several steps and needs them all to share one execution directory —
    generate one run_id here, then pass it to every load_config()/run_stepN_*() call in the chain.
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _resolve(relative_path: str) -> Path:
    path = Path(relative_path)
    return path if path.is_absolute() else REPO_ROOT / path

"""Pre-run log inspector advising the pipeline's opt-in performance flags.

Two tiers, both advisory only — neither this module nor any caller may mutate `PipelineConfig` on
the strength of its own output; both `skip_precision`/`skip_pairwise_distances` are documented
human-in-the-loop tradeoffs (`config.yaml`), and an inspector that applied its own advice would
break that stance.

- **Tier 0** (`inspect_log()`'s core fields): key validation, variant-pair count, disk estimate
  at ~20 bytes/pair, Step 6 call count, and — when a prior run against the same
  `assignment_model` already exists under `output_dir` — a USD estimate calibrated from that
  run's own recorded token counts. Every number here is exact arithmetic or calibrated against
  real measurements; nothing is a threshold.
- **Tier 1** (`REFERENCE_LOGS` / `format_prefix_comparison()`): unique-prefix count `P`, the
  quantity Step 7's precision replay cost actually tracks (not variant count), reported only
  *comparatively* against four already-measured logs. `P` is a valid but loose upper bound on any
  one category's cost (~2.4x loose against the one published per-category figure), so this
  deliberately never produces a threshold-based recommendation: an invented cutoff would produce
  over-conservative advice that is silently worse than no advice.
- **Tier 2** (`suggest_performance_flags()`): a *suggested* `skip_pairwise_distances` value,
  since predicted disk usage is exact/calibrated arithmetic and a disclosed heuristic threshold on
  top of a real number is defensible; and a descriptive-only `skip_precision` signal (no suggested
  boolean), since §2's per-category driver is only boundable, not predictable, before Step 6 runs.
  Suggestions are never applied on their own authority — the caller (the GUI) must record an
  explicit operator action before a suggested value takes effect. See that function's docstring
  for why the two flags are treated asymmetrically.

`inspect_log()` creates no run directory and writes nothing: it is safe to call from the GUI's
"New Run" form before `new_run_id()` is ever issued, or repeatedly while the form is still being
edited. Its expensive half (the XES parse, variant extraction, and prefix count) is memoized in
`_core_cache`, keyed on log-file identity (path + size + mtime, not a content hash — hashing the
full file would re-pay the I/O this cache exists to avoid) plus the four configured column keys;
repeated inspections of the same log during one form session, or a later "Run pipeline" launched
from the same session, reuse the cached parse instead of re-reading the XES file.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from .config import PipelineConfig
from .extraction.log_io import load_event_log
from .extraction.variants import extract_variants

#: (name, variants, unique prefixes, prefixes/variant, max trace length), measured directly from
#: each log's committed `variants.csv`. Never extend this into a cutoff; it exists only so an
#: operator can rank their log against known cases.
REFERENCE_LOGS: list[tuple[str, int, int, float, int]] = [
    ("rtfm_mini", 6, 12, 2.0, 7),
    ("rtfm", 231, 409, 1.8, 20),
    ("sepsis", 846, 6635, 7.8, 185),
    ("bpic2019", 11973, 213397, 17.8, 990),
]

#: Calibrated against three measured logs (RTFM 20.0, sepsis 19.6, BPIC 2019 19.1 bytes/pair) —
#: within 5% of every one. Re-derive from `extraction/similarity.py`'s pairwise schema if that
#: schema changes.
BYTES_PER_VARIANT_PAIR = 20.0

#: Precision replay's true driver (unique prefixes) is only exactly countable per-category, after
#: Step 6 runs. This is the loose factor observed between the log-wide bound and the one published
#: per-category figure (BPIC 2019: 88,241 actual vs. 213,397 log-wide).
PREFIX_BOUND_LOOSENESS_OBSERVED = 213_397 / 88_241


@dataclass
class KeyValidation:
    """Which of the four configured column keys are actually present in the loaded log,
    keyed by `PipelineConfig` field name -> the configured (missing) column name."""

    missing: dict[str, str] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not self.missing


@dataclass
class LogInspectionReport:
    log_filename: str
    num_events: int
    num_cases: int
    num_activities: int
    key_validation: KeyValidation
    # None whenever key_validation blocks variant extraction (missing case_id/activity/timestamp
    # key) — resource_key alone does not block this, since extract_variants() never reads it.
    num_variants: int | None = None
    max_trace_length: int | None = None
    num_unique_prefixes: int | None = None
    prefixes_per_variant: float | None = None
    variant_pairs: int | None = None
    predicted_pairwise_distance_mb: float | None = None
    step6_call_count: int | None = None
    step6_estimated_usd: float | None = None
    #: How many prior LLM calls (against the configured assignment_model, anywhere under
    #: output_dir) fed the USD estimate above. 0 means the estimate is None — no fabricated
    #: figure, matching this project's own estimate_cost_usd() convention (llm_backend.py).
    step6_usd_calibration_calls: int = 0


def _count_unique_prefixes(sequences) -> int:
    """Counts distinct prefixes across every activity sequence via a shared prefix trie —
    O(sum of trace lengths); measured at 0.32s on BPIC 2019's 11,973 variants, against 96s for
    that log's XES parse alone."""
    root: dict = {}
    count = 0
    for seq in sequences:
        node = root
        for activity in seq:
            child = node.get(activity)
            if child is None:
                child = {}
                node[activity] = child
                count += 1
            node = child
    return count


def _calibrate_step6_usd_per_call(
    output_dir: Path, model: str, pricing_usd_per_million_tokens: dict[str, dict[str, float]]
) -> tuple[float | None, int]:
    """Scans every `assignment_run_metadata.json` already on disk under `output_dir` for calls
    against `model`, and averages their recorded input/output tokens — a free calibration: no new
    measurement, only figures prior runs already recorded. Returns (usd_per_call,
    num_calls_used); (None, 0) if no prior call against this exact model string exists yet, or if
    it has no pricing entry."""
    rate = pricing_usd_per_million_tokens.get(model)
    if rate is None or not output_dir.is_dir():
        return None, 0

    input_tokens: list[int] = []
    output_tokens: list[int] = []
    for path in output_dir.rglob("assignment_run_metadata.json"):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for call in payload.get("calls", []):
            if call.get("model") != model:
                continue
            if call.get("input_tokens") is None or call.get("output_tokens") is None:
                continue
            input_tokens.append(call["input_tokens"])
            output_tokens.append(call["output_tokens"])

    if not input_tokens:
        return None, 0

    avg_input = sum(input_tokens) / len(input_tokens)
    avg_output = sum(output_tokens) / len(output_tokens)
    usd_per_call = (avg_input * rate["input"] + avg_output * rate["output"]) / 1_000_000
    return usd_per_call, len(input_tokens)


@dataclass
class _LogCore:
    """The expensive half of an inspection — everything that requires the XES parse. Cached by
    `inspect_log()` under `_core_cache`; the cheap half (disk/cost estimates, which depend on
    `assignment_batch_size`/pricing rather than the log itself) is recomputed on every call so a
    changed batch size or model never reads a stale estimate."""

    num_events: int
    num_cases: int
    num_activities: int
    key_validation: KeyValidation
    num_variants: int | None = None
    max_trace_length: int | None = None
    num_unique_prefixes: int | None = None
    prefixes_per_variant: float | None = None
    variant_pairs: int | None = None


_core_cache: dict[tuple, _LogCore] = {}


def clear_inspection_cache() -> None:
    """Drops every cached parse. Not needed in ordinary use — only for a caller that must force
    a re-read of a log file whose content changed without its size or mtime changing."""
    _core_cache.clear()


def _log_cache_key(config: PipelineConfig) -> tuple | None:
    """A fast proxy for log-file identity: path + size + mtime, not a content hash — hashing the
    full file would re-pay the I/O this cache exists to avoid before the parse even starts. The
    four configured column keys are part of the key because they change what `extract_variants()`
    reads, not just how the report is labeled. Returns None (uncacheable) if the log file does not
    exist yet, e.g. an inspection triggered before the log path is valid."""
    try:
        stat = config.log_path.stat()
    except OSError:
        return None
    return (
        str(config.log_path.resolve()),
        stat.st_size,
        stat.st_mtime_ns,
        config.case_id_key,
        config.activity_key,
        config.timestamp_key,
        config.resource_key,
    )


def _compute_core(config: PipelineConfig) -> _LogCore:
    df = load_event_log(config)

    required_keys = {
        "case_id_key": config.case_id_key,
        "activity_key": config.activity_key,
        "timestamp_key": config.timestamp_key,
        "resource_key": config.resource_key,
    }
    missing = {field_name: column for field_name, column in required_keys.items() if column not in df.columns}
    key_validation = KeyValidation(missing=missing)

    core = _LogCore(
        num_events=len(df),
        num_cases=df[config.case_id_key].nunique() if "case_id_key" not in missing else 0,
        num_activities=df[config.activity_key].nunique() if "activity_key" not in missing else 0,
        key_validation=key_validation,
    )

    # extract_variants() only needs these three; a missing resource_key alone (used downstream,
    # by profiling/textualization, not here) must not block the rest of this report.
    variant_blocking = {"case_id_key", "activity_key", "timestamp_key"}
    if variant_blocking & missing.keys():
        return core

    variants_df = extract_variants(df, config)
    n = len(variants_df)

    core.num_variants = n
    core.max_trace_length = int(variants_df["trace_length"].max()) if n else 0
    core.num_unique_prefixes = _count_unique_prefixes(variants_df["activity_sequence"])
    core.prefixes_per_variant = core.num_unique_prefixes / n if n else 0.0
    core.variant_pairs = n * (n - 1) // 2
    return core


def inspect_log(config: PipelineConfig, *, use_cache: bool = True) -> LogInspectionReport:
    """Tier 0 pre-run inspection: loads the log once (the one XES parse this necessarily pays,
    unless a cached parse for this exact log identity + key configuration is already available —
    see this module's docstring) and reports everything computable without a run directory.
    Writes nothing."""
    cache_key = _log_cache_key(config) if use_cache else None
    core = _core_cache.get(cache_key) if cache_key is not None else None
    if core is None:
        core = _compute_core(config)
        if cache_key is not None:
            _core_cache[cache_key] = core

    report = LogInspectionReport(
        log_filename=config.log_filename,
        num_events=core.num_events,
        num_cases=core.num_cases,
        num_activities=core.num_activities,
        key_validation=core.key_validation,
        num_variants=core.num_variants,
        max_trace_length=core.max_trace_length,
        num_unique_prefixes=core.num_unique_prefixes,
        prefixes_per_variant=core.prefixes_per_variant,
        variant_pairs=core.variant_pairs,
    )
    if report.variant_pairs is None:
        return report

    # Decimal MB (1e6 bytes): 71,670,378 pairs -> "~1.43 GB" only resolves against 1e9, not 2^30.
    report.predicted_pairwise_distance_mb = report.variant_pairs * BYTES_PER_VARIANT_PAIR / 1_000_000

    batch_size = config.llm.assignment_batch_size
    n = report.num_variants
    report.step6_call_count = -(-n // batch_size) if n else 0  # ceil division

    usd_per_call, calls_used = _calibrate_step6_usd_per_call(
        config.output_dir, config.llm.assignment_model, config.llm.pricing_usd_per_million_tokens
    )
    report.step6_usd_calibration_calls = calls_used
    if usd_per_call is not None:
        report.step6_estimated_usd = usd_per_call * report.step6_call_count

    return report


def format_report(report: LogInspectionReport) -> str:
    """Plain-text rendering for CLI use; the GUI renders the same fields with its own widgets
    (see `src/gui/pages/1_New_Run.py`)."""
    lines = [f"Log inspection: {report.log_filename}"]

    if report.key_validation.missing:
        lines.append("KEY VALIDATION — missing from the log:")
        for field_name, column in report.key_validation.missing.items():
            lines.append(f"  - {field_name} = {column!r} not found among the log's columns")
    else:
        lines.append("Key validation: all four configured keys present.")

    lines.append(f"Events: {report.num_events}, cases: {report.num_cases}, activities: {report.num_activities}")

    if report.num_variants is None:
        lines.append("Variant-level report skipped: case_id_key/activity_key/timestamp_key must all resolve first.")
        return "\n".join(lines)

    lines.append(f"Variants: {report.num_variants}, max trace length: {report.max_trace_length}")
    lines.append(
        f"Unique prefixes (P): {report.num_unique_prefixes} "
        f"({report.prefixes_per_variant:.1f} per variant) — precision replay's real cost driver, "
        f"not variant count (see README's Resource usage section)."
    )
    lines.append(
        f"Predicted structural+profile distance size (skip_pairwise_distances candidate): "
        f"{report.variant_pairs} pairs, ~{report.predicted_pairwise_distance_mb:.2f} MB "
        f"at {BYTES_PER_VARIANT_PAIR:.0f} B/pair"
    )
    lines.append(f"Step 6 LLM calls at current assignment_batch_size: {report.step6_call_count}")
    if report.step6_estimated_usd is not None:
        lines.append(
            f"Estimated Step 6 cost: ${report.step6_estimated_usd:.4f} "
            f"(calibrated from {report.step6_usd_calibration_calls} prior call(s) against this model)"
        )
    else:
        lines.append("Estimated Step 6 cost: unknown (no prior call against this assignment_model yet)")

    return "\n".join(lines)


def format_prefix_comparison(report: LogInspectionReport) -> str:
    """Tier 1: ranks this log's (variants, P, P/variant, max length) against the four reference
    logs, comparatively rather than against any invented cutoff — see this module's docstring for
    why a threshold here would be overconfident."""
    if report.num_variants is None:
        return "Prefix comparison unavailable: variant-level report was skipped (see key validation)."

    rows = list(REFERENCE_LOGS) + [
        (f"{report.log_filename} (this log)", report.num_variants, report.num_unique_prefixes,
         report.prefixes_per_variant, report.max_trace_length)
    ]
    rows.sort(key=lambda row: row[2])

    header = f"{'log':<28}{'variants':>10}{'prefixes (P)':>14}{'P/variant':>12}{'max length':>12}"
    lines = [header, "-" * len(header)]
    for name, variants, prefixes, per_variant, max_length in rows:
        marker = " <--" if "(this log)" in name else ""
        lines.append(f"{name:<28}{variants:>10}{prefixes:>14}{per_variant:>12.1f}{max_length:>12}{marker}")

    lines.append("")
    lines.append(
        f"Note: P is a valid upper bound on any one category's precision-replay cost, but "
        f"observed ~{PREFIX_BOUND_LOOSENESS_OBSERVED:.1f}x loose against the one published "
        f"per-category figure — treat this ranking as an order-of-magnitude signal ('RTFM "
        f"territory' vs. 'BPIC 2019 territory'), not a precise cost prediction."
    )
    return "\n".join(lines)


#: An unvalidated heuristic starting point, not an empirically calibrated cutoff — false authority
#: from an unvalidated threshold is a real risk here. Chosen as a round number between the two
#: points with a published actual: RTFM's measured ~0.53 MB and BPIC 2019's measured ~1.37 GB.
#: Recalibrate against real run wall-clock/disk measurements before treating this as more than a
#: starting point for an operator to accept or reject.
PAIRWISE_DISTANCE_MB_ADVISORY_THRESHOLD = 500.0


@dataclass
class PerformanceAdvice:
    """Tier 2: a suggested `skip_pairwise_distances` value, plus a descriptive (non-prescriptive)
    `skip_precision` signal. The two are treated asymmetrically on purpose:

    - `skip_pairwise_distances` cost is exact arithmetic (`predicted_pairwise_distance_mb`,
      calibrated within 5% against three published measurements — see the module docstring), so a
      disclosed heuristic threshold on top of a real number is at least grounded in a real number.
    - `skip_precision`'s true driver is a per-category quantity that provably does not exist until
      Step 6 runs; the log-wide prefix bound is ~2.4x loose against the one published per-category
      figure. Inventing a boolean cutoff here would produce false authority and over-conservative
      advice that is silently accepted, so this only ever returns a comparative signal for that
      flag.

    Nothing here is applied to a `PipelineConfig` by this module — see `inspect_log`'s docstring.
    An operator accepting a suggestion is an action the caller must record explicitly (the GUI's
    "Apply suggestion" button does, and tags the persisted inspection report accordingly), not a
    pipeline default."""

    skip_pairwise_distances: bool
    skip_pairwise_distances_reason: str
    precision_cost_signal: str
    nearest_reference_log: str


def suggest_performance_flags(report: LogInspectionReport) -> PerformanceAdvice | None:
    """Tier 2. Returns None when the variant-level report was skipped (missing keys) — there is
    nothing to advise on yet."""
    if report.num_variants is None or report.predicted_pairwise_distance_mb is None:
        return None

    skip_pd = report.predicted_pairwise_distance_mb > PAIRWISE_DISTANCE_MB_ADVISORY_THRESHOLD
    skip_pd_reason = (
        f"Predicted structural+profile distance size is ~{report.predicted_pairwise_distance_mb:.1f} MB, "
        f"{'above' if skip_pd else 'at or below'} the {PAIRWISE_DISTANCE_MB_ADVISORY_THRESHOLD:.0f} MB "
        "heuristic starting point (unvalidated — see this module's docstring). Compare against "
        "your available disk before accepting."
    )

    nearest = min(REFERENCE_LOGS, key=lambda row: abs(row[3] - report.prefixes_per_variant))
    precision_signal = (
        f"{report.prefixes_per_variant:.1f} prefixes/variant, max trace length "
        f"{report.max_trace_length} — closest to reference log '{nearest[0]}' "
        f"({nearest[3]:.1f} prefixes/variant, max length {nearest[4]}). Descriptive only: this is "
        "not a suggested skip_precision value, since the flag's true per-category cost driver "
        "isn't computable before Step 6 runs."
    )

    return PerformanceAdvice(
        skip_pairwise_distances=skip_pd,
        skip_pairwise_distances_reason=skip_pd_reason,
        precision_cost_signal=precision_signal,
        nearest_reference_log=nearest[0],
    )


def format_advice(advice: PerformanceAdvice) -> str:
    """Plain-text rendering of Tier 2, mirroring `format_report`/`format_prefix_comparison`."""
    return "\n".join(
        [
            f"skip_pairwise_distances suggestion: {advice.skip_pairwise_distances} — {advice.skip_pairwise_distances_reason}",
            f"skip_precision signal: {advice.precision_cost_signal}",
        ]
    )


def report_to_dict(report: LogInspectionReport, advice: PerformanceAdvice | None = None) -> dict:
    """JSON-serializable payload for persisting an inspection alongside a run's other
    auditability artifacts (`run_config_snapshot.json`'s sibling). The caller is responsible for
    adding whether a suggestion was actually accepted; this module only ever advises, so it does
    not know."""
    return {"report": asdict(report), "advice": asdict(advice) if advice is not None else None}

"""Pipeline wall-clock and LLM-call latency extraction from `pipeline.log` (Task C9).

Every run's `pipeline.log` already records step-level start/complete timestamps, per-call LLM
latencies (`latency=Xs` on every structured call), and peak RSS after each step — all without new
instrumentation. This module parses that log to report step-by-step runtime and LLM-call latency
distributions as a **feasibility/scalability result**, not evidence for RQ1's semantic-categorization
claim (§9, Task C9's own status note).

Status (2026-08-28): adopted. The extraction method here is being validated against existing,
*non-frozen* runs — the numbers it produces from those logs are provisional and must not be cited in
the paper. Once the frozen runs exist (§2.2), re-run this module against them for the reportable
figures.

**Concurrent-run contamination.** LLM-call latency in `pipeline.log` reflects wall-clock time
including provider-side queueing, so any two datasets/conditions run concurrently against the same
API contend for the same rate limit and inflate each other's `latency=Xs` figures relative to what a
sequential run would show. A run whose wall-clock window overlaps another run's must be excluded from
citable C9 figures, or the two runs must be re-executed sequentially. This module does not detect
overlap itself — cross-check `started_at` windows across datasets before trusting a latency figure.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import pandas as pd

CAVEAT = (
    "Step-by-step wall-clock and LLM-call latency figures characterize feasibility/scalability, "
    "not categorization quality; they are not evidence for RQ1's semantic-categorization claim "
    "(OVERVIEW.md, Task C9). Figures drawn from a non-frozen run are provisional and must not be "
    "cited in the paper — only figures from the frozen runs (§2.2) are reportable."
)

_TS = r"(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})"
_STEP_STARTED_RE = re.compile(_TS + r" \[INFO\] goalcat: Step (?P<step>\S+) \(.*?\) started")
_STEP_COMPLETE_RE = re.compile(_TS + r" \[INFO\] goalcat: Step (?P<step>\S+) complete\.")
# Step 9 (business review) never logs "Step 9 complete." — `pipeline.py` only logs "started" and
# "Step 9 result: {...}" (`pipeline.py:826-828`). Treat the result line as an alternate completion
# signal so Step 9 is not silently left open; other steps never emit this line, so it is a no-op
# for them.
_STEP_RESULT_RE = re.compile(_TS + r" \[INFO\] goalcat: Step (?P<step>\S+) result: ")
_PEAK_RSS_RE = re.compile(_TS + r" \[INFO\] goalcat: Peak RSS after Step (?P<step>[^:]+): (?P<rss>[\d.]+) MiB")
_LLM_CALL_RE = re.compile(
    _TS
    + r" \[INFO\] goalcat: LLM structured call ok \("
    r"backend=(?P<backend>[^,]+), model=(?P<model>[^,]+), "
    r"prompt_hash=(?P<hash>[^,]+), latency=(?P<latency>[\d.]+)s\)"
)


def _parse_ts(raw: str) -> datetime:
    return datetime.strptime(raw, "%Y-%m-%d %H:%M:%S,%f")


@dataclass(frozen=True)
class LLMCallRecord:
    timestamp: datetime
    backend: str
    model: str
    prompt_hash: str
    latency_seconds: float


@dataclass(frozen=True)
class StepTiming:
    step: str
    started_at: datetime
    completed_at: datetime | None  # None: run truncated or still in progress at parse time
    peak_rss_mib: float | None
    llm_calls: tuple[LLMCallRecord, ...] = field(default_factory=tuple)

    @property
    def is_complete(self) -> bool:
        return self.completed_at is not None

    @property
    def duration_seconds(self) -> float | None:
        if self.completed_at is None:
            return None
        return (self.completed_at - self.started_at).total_seconds()

    @property
    def llm_call_count(self) -> int:
        return len(self.llm_calls)

    @property
    def llm_latency_total_seconds(self) -> float:
        return sum(c.latency_seconds for c in self.llm_calls)

    @property
    def llm_latency_mean_seconds(self) -> float | None:
        if not self.llm_calls:
            return None
        return self.llm_latency_total_seconds / len(self.llm_calls)

    @property
    def llm_latency_max_seconds(self) -> float | None:
        if not self.llm_calls:
            return None
        return max(c.latency_seconds for c in self.llm_calls)

    def as_dict(self) -> dict:
        return {
            "step": self.step,
            "started_at": self.started_at.isoformat(),
            "complete": self.is_complete,
            "duration_s": self.duration_seconds,
            "llm_calls": self.llm_call_count,
            "llm_latency_total_s": round(self.llm_latency_total_seconds, 2) if self.llm_calls else None,
            "llm_latency_mean_s": round(self.llm_latency_mean_seconds, 2) if self.llm_calls else None,
            "llm_latency_max_s": round(self.llm_latency_max_seconds, 2) if self.llm_calls else None,
            "peak_rss_mib": self.peak_rss_mib,
        }


@dataclass(frozen=True)
class RunTiming:
    dataset: str
    run_id: str
    log_path: Path
    steps: tuple[StepTiming, ...]

    @property
    def is_complete(self) -> bool:
        """True only if every step seen in the log reached its `complete` marker. A run still in
        progress, or one that crashed mid-step, reports its last step as incomplete rather than
        silently omitting it — an incomplete run's totals must be read as partial, not as a smaller
        pipeline."""
        return bool(self.steps) and all(s.is_complete for s in self.steps)

    @property
    def total_duration_seconds(self) -> float | None:
        if not self.steps or not self.is_complete:
            return None
        return (self.steps[-1].completed_at - self.steps[0].started_at).total_seconds()

    @property
    def total_llm_calls(self) -> int:
        return sum(s.llm_call_count for s in self.steps)

    @property
    def total_llm_latency_seconds(self) -> float:
        return sum(s.llm_latency_total_seconds for s in self.steps)

    def step_frame(self) -> pd.DataFrame:
        """One row per step — the per-step table."""
        df = pd.DataFrame([s.as_dict() for s in self.steps])
        df.insert(0, "run_id", self.run_id)
        df.insert(0, "dataset", self.dataset)
        return df

    def summary_dict(self) -> dict:
        return {
            "dataset": self.dataset,
            "run_id": self.run_id,
            "complete": self.is_complete,
            "n_steps": len(self.steps),
            "total_duration_s": round(self.total_duration_seconds, 2) if self.total_duration_seconds else None,
            "total_llm_calls": self.total_llm_calls,
            "total_llm_latency_s": round(self.total_llm_latency_seconds, 2),
        }


def parse_pipeline_log(log_path: Path, dataset: str | None = None, run_id: str | None = None) -> RunTiming:
    """Parse one `pipeline.log`. `dataset`/`run_id` default to the two path components above the
    file (`data/output/<dataset>/<run_id>/pipeline.log`), matching this repo's run layout.

    Steps are recognized by their ``started``/``complete`` marker lines; ``LLM structured call ok``
    and ``Peak RSS after Step`` lines are attributed to whichever step is open when they occur. A
    step with no matching ``complete`` line (truncated log, crashed run, or a run still in progress)
    is kept with ``completed_at=None`` rather than dropped, so a partial log still yields partial
    figures instead of a silent gap.
    """
    if dataset is None:
        dataset = log_path.parent.parent.name
    if run_id is None:
        run_id = log_path.parent.name

    lines = log_path.read_text().splitlines()

    # Mutable per-step buffers, built in encounter order. `open_idx` is the step currently in
    # progress; `closed_idx` is the step that just closed, kept alive only until the *next* step
    # opens — `Peak RSS after Step N` is logged one line *after* `Step N complete.` (both the source
    # and the runs confirm this ordering), so it must still be attributable after the close.
    entries: list[dict] = []
    open_idx: int | None = None
    closed_idx: int | None = None

    def _open(step: str, started_at: datetime) -> None:
        nonlocal open_idx, closed_idx
        entries.append(
            {"step": step, "started_at": started_at, "completed_at": None, "peak_rss_mib": None, "llm_calls": []}
        )
        open_idx = len(entries) - 1
        closed_idx = None

    def _close(completed_at: datetime | None) -> None:
        nonlocal open_idx, closed_idx
        if open_idx is None:
            return
        entries[open_idx]["completed_at"] = completed_at
        closed_idx = open_idx
        open_idx = None

    for line in lines:
        m = _STEP_STARTED_RE.match(line)
        if m:
            # A new step starting implies the previous one never logged a completion marker
            # (truncated log or crash) — close it as incomplete before opening the new one.
            _close(None)
            _open(m.group("step"), _parse_ts(m.group("ts")))
            continue

        m = _STEP_COMPLETE_RE.match(line)
        if m and open_idx is not None and entries[open_idx]["step"] == m.group("step"):
            _close(_parse_ts(m.group("ts")))
            continue

        m = _STEP_RESULT_RE.match(line)
        if m and open_idx is not None and entries[open_idx]["step"] == m.group("step"):
            _close(_parse_ts(m.group("ts")))
            continue

        m = _LLM_CALL_RE.match(line)
        if m and open_idx is not None:
            entries[open_idx]["llm_calls"].append(
                LLMCallRecord(
                    timestamp=_parse_ts(m.group("ts")),
                    backend=m.group("backend"),
                    model=m.group("model"),
                    prompt_hash=m.group("hash"),
                    latency_seconds=float(m.group("latency")),
                )
            )
            continue

        m = _PEAK_RSS_RE.match(line)
        if m:
            step_name = m.group("step")
            rss = float(m.group("rss"))
            if open_idx is not None and entries[open_idx]["step"] == step_name:
                entries[open_idx]["peak_rss_mib"] = rss
            elif closed_idx is not None and entries[closed_idx]["step"] == step_name:
                entries[closed_idx]["peak_rss_mib"] = rss
            continue

    # Log ended mid-step (run still in progress, or truncated): keep it as incomplete.
    _close(None)

    steps = tuple(
        StepTiming(
            step=e["step"],
            started_at=e["started_at"],
            completed_at=e["completed_at"],
            peak_rss_mib=e["peak_rss_mib"],
            llm_calls=tuple(e["llm_calls"]),
        )
        for e in entries
    )
    return RunTiming(dataset=dataset, run_id=run_id, log_path=log_path, steps=steps)


def discover_run_logs(output_root: Path) -> list[Path]:
    """All `pipeline.log` files under `data/output/<dataset>/<run_id>/`, sorted for stable output."""
    return sorted(output_root.glob("*/*/pipeline.log"))


def step_table(runs: list[RunTiming]) -> pd.DataFrame:
    """Per-step rows across every run — the detailed table."""
    if not runs:
        return pd.DataFrame()
    return pd.concat([r.step_frame() for r in runs], ignore_index=True)


def run_summary_table(runs: list[RunTiming]) -> pd.DataFrame:
    """One row per run — total duration, total LLM calls, total LLM latency."""
    return pd.DataFrame([r.summary_dict() for r in runs])


def to_markdown(runs: list[RunTiming]) -> str:
    header = "**Pipeline timing (Task C9)** — feasibility/scalability characterization\n\n"
    parts = [header, "Per-run summary:\n\n", run_summary_table(runs).to_markdown(index=False), "\n\n"]
    parts += ["Per-step detail:\n\n", step_table(runs).to_markdown(index=False), "\n\n"]
    parts += [f"_{CAVEAT}_\n"]
    return "".join(parts)


def main(argv: list[str] | None = None) -> int:
    """`python -m experimentation.icpm2027.analysis.timing` — parse every frozen `pipeline.log`
    under `data/output/{rtfm,sepsis,bpic2019}/icpm2027_*/` (plus the shared bases, which hold
    Steps 1-4) and write `data/output/icpm2027_results/timing.md`.

    Concurrent-run contamination (see module docstring) is not detected here: cross-check
    `started_at` windows before quoting a latency figure.
    """
    import argparse

    from goalcat.config import REPO_ROOT

    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument("--datasets", default="rtfm,sepsis,bpic2019")
    args = parser.parse_args(argv)

    runs: list[RunTiming] = []
    for ds in [d.strip() for d in args.datasets.split(",") if d.strip()]:
        ds_dir = REPO_ROOT / "data" / "output" / ds
        if not ds_dir.is_dir():
            continue
        for run_dir in sorted(ds_dir.glob("icpm2027_*")):
            log = run_dir / "pipeline.log"
            if log.exists():
                runs.append(parse_pipeline_log(log, dataset=ds, run_id=run_dir.name))

    out = REPO_ROOT / "data" / "output" / "icpm2027_results" / "timing.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(to_markdown(runs), encoding="utf-8")
    print(f"Parsed {len(runs)} runs; wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

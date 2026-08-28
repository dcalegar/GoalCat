"""Post-hoc diagnostics over a finished (or crashed) run directory: where a run stopped, which
warnings fired, and what each one means.

Streamlit-free by design, like gui/artifacts.py and gui/run_control.py — everything here reads
files and returns plain dataclasses, so it is unit-testable and reusable outside the GUI.

Why this exists alongside `ui_helpers.render_progress_panel()`: that panel shows per-step state
live, but only for a run the GUI itself launched (it needs the worker's `Popen` handle in session
state) and only while the launching page stays open. Two consequences it cannot cover:

- A run launched from `experimentation/examples/*/example_run.py` or the ICPM 2027 harness writes
  no `gui_status.json` at all, so nothing outside its terminal ever recorded that it failed.
- Once the page is closed, a failure survives only in `pipeline.log`, which the GUI otherwise
  exposes as an unstructured 200-line tail during the run and nowhere afterwards.

`pipeline.log` is written by every run whatever launched it, so it is the primary source here;
`gui_status.json` is read as an *enrichment* when present, because it is the only artifact that
carries the failing exception's own message (see gui/worker.py's `_run_step`). Steps 5-9's
`round_info.json` supplies the accepted/pending_review verdict.

The warning catalog below is keyed to the `logger.warning(...)` call sites in `goalcat`, cited per
entry. A warning the catalog does not recognize is still reported, marked as unclassified, rather
than hidden — an unexplained warning is exactly what a reader most needs to see.
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass, field
from pathlib import Path

from gui import artifacts, run_control

#: A run whose last log line is older than this is treated as dead rather than in progress.
#: pipeline.log is written continuously (every LLM call is logged), so a live run is never this
#: quiet — except inside Step 7's precision replay on a large log, which is why this is generous
#: and why the resulting verdict always states the last-write time instead of asserting a crash.
STALE_AFTER_SECONDS = 900

_LOG_LINE_RE = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) \[(?P<level>[A-Z]+)\] goalcat: (?P<message>.*)$"
)
#: Step tokens as the log writes them: "1".."9", plus "7b" (the optional indicator step) and
#: "5a"/"5b" (Step 5's two mutually exclusive induction modes, only ever one per run).
_STEP_STARTED_RE = re.compile(r"^Step (?P<step>[0-9]+[ab]?) \(.*\) started")
#: `complete[.( ]` rather than `complete\.` because Step 3 logs "Step 3 complete (reused)." when it
#: reuses this run directory's narratives.csv instead of recomputing.
_STEP_COMPLETE_RE = re.compile(r"^Step (?P<step>[0-9]+[ab]?) complete[.( ]")
#: Step 9 is the one step that never logs "Step 9 complete." — goalcat.pipeline.run_step9_review
#: logs its verdict instead ("Step 9 result: {...}"), since a round can end accepted, revised, or
#: awaiting review. Treated as that step's terminator.
_STEP_9_DONE_RE = re.compile(r"^Step 9 result:")
#: Written by goalcat.review.start_revision_round when Step 9's merge/split opens a new round.
#: Deliberately narrow: "round N" appears inside plenty of unrelated messages (Step 9's own refusal
#: text among them), and attributing events to a round the run never entered would be worse than
#: attributing none.
_REVISION_ROUND_RE = re.compile(r"^Step 9 revision round started: round \d+ -> round (?P<round>\d+)")


@dataclass(frozen=True)
class WarningKind:
    """One recognized warning family: what the pipeline emitted, what it means, what to do."""

    kind_id: str
    title: str
    severity: str  # "blocking" | "quality" | "transient" | "benign" | "unclassified"
    source: str  # the goalcat call site that emits it, for anyone who wants the code
    meaning: str
    action: str


SEVERITY_ORDER = {"blocking": 0, "quality": 1, "transient": 2, "unclassified": 3, "benign": 4}

SEVERITY_HELP = {
    "blocking": "Leaves the run unfinalizable — Step 9 will refuse to accept it, or has already.",
    "quality": "The run completes, but a result is weaker or less trustworthy than it appears.",
    "transient": "An infrastructure hiccup the pipeline retried on its own; harmless if nothing "
    "downstream reports the work as still pending.",
    "benign": "Expected behavior on this input, logged for the record.",
    "unclassified": "Not in this catalog — read the message and the code that emitted it.",
}

UNCLASSIFIED = WarningKind(
    kind_id="unclassified",
    title="Unrecognized warning",
    severity="unclassified",
    source="—",
    meaning="This warning is not in gui/diagnostics.py's catalog, which is keyed to goalcat's "
    "logger.warning() call sites. Either it is new or the catalog is out of date.",
    action="Read the message below, then grep goalcat for the phrasing to find what emitted it. "
    "If it is a lasting warning family, add it to CATALOG so the next reader gets an explanation.",
)

#: Ordered — first pattern that matches a message classifies it, so put specific patterns above
#: general ones. Every entry cites the call site it was written against.
CATALOG: list[tuple[re.Pattern[str], WarningKind]] = [
    (
        re.compile(r"^\d+ narratives still pending after this attempt"),
        WarningKind(
            kind_id="assignment_pending",
            title="Narratives left unassigned after Step 6",
            severity="blocking",
            source="goalcat/pipeline.py — run_step6_assignment()",
            meaning="One or more assignment batches never produced a result, so these variants "
            "have no Step 6 outcome at all: they are neither categorized nor residual. Step 6 "
            "then raises IncompleteAssignmentError and the run stops there — Step 9 would refuse "
            "to finalize the round anyway (accepting it would silently drop those variants from "
            "every final/ artifact, category sublogs and residual.xes.gz alike), and stopping at "
            "Step 6 avoids paying for Steps 7, 7b and 8 on a partition that must be recomputed.",
            action="Re-run Step 6 against this same run_id. Step 6 resumes: it loads the "
            "assignments already on disk and calls the LLM only for what is missing. Then run "
            "Steps 7, 7b, 8 and 9 as usual.",
        ),
    ),
    (
        re.compile(r"^Assignment batch call failed for \d+ narratives"),
        WarningKind(
            kind_id="assignment_batch_failed",
            title="Assignment batch failed against the LLM API",
            severity="transient",
            source="goalcat/llm/assignment.py — _assign_batch()",
            meaning="A whole batch's LLM call raised after LiteLLM exhausted its own retries — "
            "typically a 429 (rate limit) or a 503 (the provider reporting high demand). The "
            "batch's narratives stay pending; the rest of the run continues.",
            action="Harmless on its own only if a later attempt picked the batch up. Check "
            "whether Step 6 also reported narratives still pending — if it did, the run is "
            "incomplete and must resume Step 6. Lowering llm.concurrency or setting "
            "llm.requests_per_minute reduces how often provider-side throttling triggers this.",
        ),
    ),
    (
        re.compile(r"^Assignment batch response missing \d+/\d+ narratives"),
        WarningKind(
            kind_id="assignment_batch_incomplete",
            title="LLM omitted narratives from an assignment batch",
            severity="transient",
            source="goalcat/llm/assignment.py — _assign_batch()",
            meaning="The call succeeded and validated, but the model simply did not return a "
            "verdict for every variant it was given. The omitted ones stay pending rather than "
            "being guessed at or silently dropped.",
            action="Same as a failed batch: confirm Step 6 does not report narratives still "
            "pending. A batch that repeatedly loses variants is a sign llm.assignment_batch_size "
            "is too large for the model's output budget.",
        ),
    ),
    (
        re.compile(r"^Assignment batch response returned unexpected variant_id"),
        WarningKind(
            kind_id="assignment_hallucinated_id",
            title="LLM invented a variant_id in an assignment batch",
            severity="quality",
            source="goalcat/llm/assignment.py — _assign_batch()",
            meaning="The response carried a variant_id that was not in the batch's prompt. It is "
            "discarded, so it cannot corrupt assignments.csv — but it is direct evidence of the "
            "model fabricating identifiers rather than transcribing them.",
            action="No recovery needed. Worth recording if you are reporting assignment "
            "reliability: it is a measurable hallucination event, not a pipeline error.",
        ),
    ),
    (
        re.compile(r"^LLM structured-output validation failed"),
        WarningKind(
            kind_id="structured_output_invalid",
            title="LLM response failed schema validation (retried)",
            severity="transient",
            source="goalcat/llm/llm_backend.py — generate_structured()",
            meaning="The response did not satisfy the Pydantic schema — a duplicated id, a "
            "missing field, a malformed value. The backend retries up to llm.max_retries; the "
            "attempt counter in the message says which attempt this was.",
            action="Ignore when a later attempt succeeded (the run continues past it normally). "
            "If the final attempt also failed, the call raises and the step that made it fails — "
            "look for a failed step in the timeline above.",
        ),
    ),
    (
        re.compile(r"^Taxonomy grounding check: .*share evidence_variant_ids"),
        WarningKind(
            kind_id="taxonomy_shared_evidence",
            title="Two categories cite the same variant as evidence",
            severity="quality",
            source="goalcat/llm/taxonomy.py — check_taxonomy_grounding()",
            meaning="Step 5 induced categories meant to be mutually exclusive, yet two of them "
            "justify themselves with the same sampled variant. The boundary between those "
            "categories is not as crisp as the taxonomy claims.",
            action="Warn-only by design: Step 9's human review is the correctness gate, not this "
            "check. Inspect the two categories in the Review page; merging them, or renaming one "
            "to sharpen its scope, is the intended remedy.",
        ),
    ),
    (
        re.compile(r"^Taxonomy grounding check: .*anchor_ids is empty"),
        WarningKind(
            kind_id="taxonomy_unanchored_category",
            title="Intent-guided category traceable to no goal-model element",
            severity="quality",
            source="goalcat/llm/taxonomy.py — check_taxonomy_grounding()",
            meaning="Under intent_guided induction every category must trace to a declared "
            "alternative of the goal model. This one anchors to nothing, so the pipeline's central "
            "claim — that the taxonomy *is* the goal model's decomposition — does not hold for it.",
            action="Treat the category as suspect in Step 9. Either it restates behavior the goal "
            "model genuinely does not declare (which belongs in the residual, or argues for "
            "revising the goal model) or Step 5 dropped an anchor it should have carried.",
        ),
    ),
    (
        re.compile(r"^Taxonomy grounding check: .*is an AND-decomposed child"),
        WarningKind(
            kind_id="taxonomy_and_anchor",
            title="Category anchored to a mandatory step, not an alternative",
            severity="quality",
            source="goalcat/llm/taxonomy.py — check_taxonomy_grounding()",
            meaning="The anchor is an AND-decomposed child in the goal model: every case performs "
            "it, so it cannot discriminate between variants. A category built on it will not "
            "partition the log along a meaningful axis.",
            action="Re-anchor or drop the category in Step 9. Recurring hits here usually mean "
            "the goal model states a procedure rather than a set of alternatives.",
        ),
    ),
    (
        re.compile(r"^Taxonomy grounding check: .*(not in goal model|not in sample|non-empty in open mode)"),
        WarningKind(
            kind_id="taxonomy_bad_reference",
            title="Taxonomy references something that does not exist",
            severity="quality",
            source="goalcat/llm/taxonomy.py — check_taxonomy_grounding()",
            meaning="A category cites an anchor id absent from the goal model, an evidence "
            "variant absent from the sample, or — in open mode, where no goal model exists — an "
            "anchor id at all. The reference was hallucinated.",
            action="Do not trust that category's stated provenance. Under temperature=0 a "
            "hallucinated id tends to reproduce on retry, so re-running Step 5 unchanged is "
            "unlikely to help; revise it through Step 9 instead.",
        ),
    ),
    (
        re.compile(r"^Taxonomy grounding check:"),
        WarningKind(
            kind_id="taxonomy_grounding_other",
            title="Taxonomy grounding check flagged a problem",
            severity="quality",
            source="goalcat/llm/taxonomy.py — check_taxonomy_grounding()",
            meaning="Step 5's induced taxonomy failed one of the grounding checks. All of them "
            "are warn-only: Step 9's human review is the actual correctness gate.",
            action="Read the message and judge the affected category during Step 9.",
        ),
    ),
    (
        re.compile(r"^Assignment grounding check:"),
        WarningKind(
            kind_id="assignment_bad_category",
            title="Assignment references a category that does not exist",
            severity="quality",
            source="goalcat/llm/assignment.py — check_assignment_grounding()",
            meaning="A variant was assigned a category_id that is neither null (residual) nor any "
            "id in the taxonomy — the model invented a category rather than choosing one.",
            action="Those rows cannot be read as belonging to any real category. Re-running "
            "Step 6 for the affected variants is the direct fix.",
        ),
    ),
    (
        re.compile(r"^Revision grounding check:"),
        WarningKind(
            kind_id="revision_not_applied",
            title="Step 9 revision was not carried out as requested",
            severity="quality",
            source="goalcat/review.py — check_revision_grounding()",
            meaning="The revised taxonomy does not reflect the merge/split that was asked for, or "
            "categories nobody mentioned vanished from it. Step 5's revision pass reinterpreted "
            "the instruction instead of applying it.",
            action="Compare the new round's taxonomy against the previous one before accepting. "
            "Re-issuing the decision with more explicit category ids usually resolves it.",
        ),
    ),
    (
        re.compile(r"^Goal alignment coverage check:"),
        WarningKind(
            kind_id="goal_alignment_coverage",
            title="Step 8 goal-alignment prose does not cover every category",
            severity="quality",
            source="goalcat/llm/description.py — check_goal_alignment_coverage()",
            meaning="The goal-alignment assessment omitted an active category, or invented one. "
            "The affected categories' descriptions are incomplete rather than wrong.",
            action="Re-run Step 8 for this round if the descriptions matter to what you are "
            "producing; nothing upstream of it is affected.",
        ),
    ),
    (
        re.compile(r"^Precision computation for category .* exceeded discovery_precision_timeout_seconds"),
        WarningKind(
            kind_id="precision_timeout",
            title="Precision computation timed out — reported as NaN",
            severity="quality",
            source="goalcat/discovery.py — discover_models_7()",
            meaning="The alignment-based precision replay for this category exceeded its timeout "
            "and was abandoned, so its precision is NaN. Fitness is unaffected. The replay itself "
            "keeps running in an orphaned thread (Python threads cannot be cancelled), which is "
            "why the process may stay busy after the step reports done.",
            action="Any per-category or averaged precision figure computed from this run is "
            "missing this category. Raise discovery_precision_timeout_seconds and re-run Step 7, "
            "or set skip_precision to declare precision out of scope for the whole run.",
        ),
    ),
    (
        re.compile(r"^Category .* has no assigned variants — skipping discovery\."),
        WarningKind(
            kind_id="empty_category_discovery",
            title="Category with no variants — no model discovered",
            severity="benign",
            source="goalcat/discovery.py — discover_models_7()",
            meaning="Step 5 declared a category that Step 6 then assigned nothing to. It gets a "
            "row of NaN metrics rather than a discovered model.",
            action="Nothing to repair mechanically. An empty category is a finding in itself: the "
            "goal model declares an alternative the log does not exercise.",
        ),
    ),
    (
        re.compile(r"^Category .* has no assigned variants -- skipping description\."),
        WarningKind(
            kind_id="empty_category_description",
            title="Category with no variants — no description generated",
            severity="benign",
            source="goalcat/llm/description.py — generate_descriptions_8()",
            meaning="Step 8's counterpart to the discovery warning above: no narrative exists to "
            "describe, so no prose is generated and no LLM call is spent.",
            action="None. Expect it once per empty category, alongside the Step 7 warning.",
        ),
    ),
    (
        re.compile(r"^Goal model .* declares no measurable indicator"),
        WarningKind(
            kind_id="no_measurable_indicator",
            title="Step 7b had nothing to measure",
            severity="benign",
            source="goalcat/indicators.py — measure_indicators_7b()",
            meaning="The goal model binds none of its KPI indicators to the log with goalcat:* "
            "metadata, so Step 7b is a no-op and writes empty tables. Only the RTFM goal model "
            "carries those bindings today.",
            action="None, unless indicator satisfaction was expected — in which case the goal "
            "model needs goalcat:from / goalcat:to bindings on its indicators, not a config change.",
        ),
    ),
    (
        re.compile(r"^Config drift: run directory"),
        WarningKind(
            kind_id="config_drift",
            title="Run directory reused under different settings",
            severity="quality",
            source="goalcat/run_logging.py — warn_on_config_drift()",
            meaning="Artifacts in this directory were produced under a config that differs from "
            "the one now running, in the keys the message lists. Steps that reuse earlier "
            "artifacts are mixing two configurations in one run directory.",
            action="Decisive for any run you intend to cite: start a fresh run_id instead of "
            "reusing this directory, unless you can account for every changed key.",
        ),
    ),
    (
        re.compile(r"^LUPIN textualization subprocess failed"),
        WarningKind(
            kind_id="lupin_failed",
            title="LUPIN textualization subprocess failed",
            severity="blocking",
            source="goalcat/narrative/textualization.py — textualize_3()",
            meaning="Step 3's vendored LUPIN subprocess exited non-zero, so no narratives were "
            "produced. Every LLM step downstream reads narratives, so the run cannot proceed.",
            action="Read the subprocess stderr in the message. A missing third_party/ checkout or "
            "an interpreter mismatch are the usual causes.",
        ),
    ),
]


def classify(message: str) -> WarningKind:
    """Maps a log message to its catalog entry, or to UNCLASSIFIED. Matches on the message's first
    line: several warnings append a multi-line provider payload or id list underneath."""
    first_line = message.split("\n", 1)[0]
    for pattern, kind in CATALOG:
        if pattern.search(first_line):
            return kind
    return UNCLASSIFIED


@dataclass
class LogEvent:
    timestamp: str
    level: str
    message: str
    step: str | None
    round: int | None
    line_number: int


@dataclass
class StepRun:
    """One execution of one step. A step appears more than once when Step 9 opens a revision round
    and Steps 5-8 run again — kept as separate entries rather than collapsed, so the timeline shows
    what actually happened rather than a per-step summary that hides a re-run."""

    step: str
    round: int | None
    started_at: str
    ended_at: str | None
    state: str  # "done" | "unterminated"


@dataclass
class RunDiagnosis:
    log_stem: str
    run_id: str
    run_dir: Path
    outcome: str  # "completed" | "awaiting_review" | "incomplete" | "failed" | "running" | "unknown"
    headline: str
    steps: list[StepRun] = field(default_factory=list)
    warnings: list[LogEvent] = field(default_factory=list)
    failed_step: str | None = None
    failure_message: str | None = None
    last_log_write: str | None = None
    has_log: bool = True

    @property
    def counts_by_severity(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for event in self.warnings:
            severity = classify(event.message).severity
            counts[severity] = counts.get(severity, 0) + 1
        return counts

    @property
    def blocking_count(self) -> int:
        return self.counts_by_severity.get("blocking", 0)


def parse_log(log_path: Path) -> tuple[list[LogEvent], list[StepRun]]:
    """Reads pipeline.log into events and step executions.

    A line that does not match the log's own `timestamp [LEVEL] goalcat: message` header belongs to
    the previous record: LiteLLM's provider payloads and Pydantic's validation errors are both
    multi-line, and splitting them would strip exactly the part that explains the failure.
    """
    if not log_path.exists():
        return [], []

    events: list[LogEvent] = []
    steps: list[StepRun] = []
    #: A stack per step, not one entry per step: Step 9 nests. When a reviewer merges or splits,
    #: goalcat.review.process_review opens the next round and runs Steps 5-8 *inside* the Step 9
    #: call that decided it, and only then logs its own "Step 9 result: revised" — so a run can
    #: have two Step 9 executions open at once, and the inner one finishes first. Closing them
    #: LIFO keeps the outer one from looking like it never returned.
    open_steps: dict[str, list[StepRun]] = {}
    current_round: int = 1
    current_step: str | None = None

    for line_number, line in enumerate(log_path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        match = _LOG_LINE_RE.match(line)
        if match is None:
            if events:
                events[-1].message += "\n" + line
            continue

        message = match.group("message")
        timestamp = match.group("timestamp")

        revision = _REVISION_ROUND_RE.match(message)
        if revision:
            current_round = int(revision.group("round"))

        started = _STEP_STARTED_RE.match(message)
        if started:
            current_step = started.group("step")
            step_run = StepRun(
                step=current_step, round=current_round, started_at=timestamp,
                ended_at=None, state="unterminated",
            )
            steps.append(step_run)
            open_steps.setdefault(current_step, []).append(step_run)

        completed = _STEP_COMPLETE_RE.match(message)
        finished_step = completed.group("step") if completed else ("9" if _STEP_9_DONE_RE.match(message) else None)
        if finished_step is not None:
            stack = open_steps.get(finished_step)
            if stack:
                open_step = stack.pop()
                open_step.ended_at = timestamp
                open_step.state = "done"

        events.append(
            LogEvent(
                timestamp=timestamp,
                level=match.group("level"),
                message=message,
                step=current_step,
                round=current_round,
                line_number=line_number,
            )
        )

    return events, steps


def _gui_status_failure(run_dir: Path) -> tuple[str, str] | None:
    """The failing step and its exception message, from gui_status.json — the only artifact that
    records *why* a run died, and only for runs the GUI launched (see gui/worker.py `_run_step`).
    Checks the run directory and every round directory, since Step 9 writes its status per round.
    """
    candidates = [run_dir / run_control.STATUS_FILENAME]
    candidates += sorted(run_dir.glob(f"*/{run_control.STATUS_FILENAME}"))
    for path in candidates:
        status = run_control.read_status(path)
        for step, entry in (status or {}).get("steps", {}).items():
            if entry.get("state") == "error":
                return step, entry.get("error") or "(no message recorded)"
    return None


def diagnose_run(log_stem: str, run_id: str, *, now: float | None = None) -> RunDiagnosis:
    """Full diagnosis of one run directory, from its own files alone."""
    run_dir = artifacts.run_output_dir(log_stem, run_id)
    log_path = run_dir / "pipeline.log"
    events, steps = parse_log(log_path)
    warnings = [e for e in events if e.level in ("WARNING", "ERROR")]

    diagnosis = RunDiagnosis(
        log_stem=log_stem, run_id=run_id, run_dir=run_dir,
        outcome="unknown", headline="", steps=steps, warnings=warnings,
        has_log=log_path.exists(),
    )

    if not log_path.exists():
        diagnosis.outcome = "unknown"
        diagnosis.headline = (
            "No pipeline.log in this run directory — nothing recorded what happened here."
        )
        return diagnosis

    last_write = log_path.stat().st_mtime
    diagnosis.last_log_write = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(last_write))
    idle_seconds = (now if now is not None else time.time()) - last_write

    rounds = artifacts.list_rounds(run_dir)
    latest_round = rounds[-1] if rounds else None
    unterminated = [s for s in steps if s.state == "unterminated"]

    gui_failure = _gui_status_failure(run_dir)
    if gui_failure is not None:
        diagnosis.failed_step, diagnosis.failure_message = gui_failure
        diagnosis.outcome = "failed"
        diagnosis.headline = (
            f"Failed in Step {diagnosis.failed_step} "
            f"({run_control.STEP_NAMES.get(step_key(diagnosis.failed_step), 'unknown step')})."
        )
        return diagnosis

    blocking = [e for e in warnings if classify(e.message).severity == "blocking"]

    if unterminated:
        last = unterminated[-1]
        step_name = run_control.STEP_NAMES.get(step_key(last.step), "unknown step")
        if idle_seconds < STALE_AFTER_SECONDS:
            diagnosis.outcome = "running"
            diagnosis.headline = (
                f"Step {last.step} ({step_name}) is in progress — started {last.started_at}, "
                f"last log write {diagnosis.last_log_write}."
            )
            if blocking:
                # Still moving, but already unacceptable: say so now rather than let it finish
                # into a round Step 9 must refuse.
                diagnosis.headline += (
                    f" A blocking condition has already been logged ({len(blocking)} warning(s) "
                    "below), so this round cannot be accepted as it stands."
                )
        else:
            diagnosis.outcome = "failed"
            diagnosis.failed_step = last.step
            diagnosis.headline = (
                f"Step {last.step} ({step_name}) started at {last.started_at} and never reported "
                f"an outcome; nothing has been written to pipeline.log since "
                f"{diagnosis.last_log_write}. The run died inside that step."
            )
            diagnosis.failure_message = (
                "pipeline.log records no reason: the exception was raised to whatever launched the "
                "run and printed there. A GUI-launched run would have recorded the message in "
                "gui_status.json; a run started from a script or the ICPM 2027 harness leaves it "
                "in that process's own terminal output."
            )
        return diagnosis

    if blocking and not (latest_round and latest_round.get("status") == "accepted"):
        # Every step that started also returned, so nothing looks broken in the timeline — but a
        # blocking warning means the round cannot be accepted, and saying "awaiting review" here
        # would send a reviewer to a Review page whose accept button is guaranteed to raise.
        diagnosis.outcome = "incomplete"
        diagnosis.headline = (
            f"Every step returned, but {len(blocking)} blocking warning(s) mean this round cannot "
            "be accepted as it stands — see the blocking entries below for the repair."
        )
    elif latest_round and latest_round.get("status") == "accepted":
        diagnosis.outcome = "completed"
        diagnosis.headline = f"Round {latest_round.get('round')} was accepted in Step 9."
    elif latest_round:
        diagnosis.outcome = "awaiting_review"
        diagnosis.headline = (
            f"Every step ran, and round {latest_round.get('round')} is "
            f"{latest_round.get('status')} — Step 9's human decision is still outstanding."
        )
    else:
        diagnosis.outcome = "unknown"
        diagnosis.headline = (
            "Every step that started also finished, but no round was ever opened for review."
        )
    return diagnosis


def step_key(step: str) -> int | str:
    """Maps a log's step token to a run_control.STEP_NAMES key: that dict keys Steps 1-9 as ints
    and 7b as a string, while the log writes them all as text and writes Step 5 as "5a"/"5b" (its
    two induction modes, which are one step and share one name)."""
    if step in ("5a", "5b"):
        return 5
    return int(step) if step.isdigit() else step


def diagnose_all() -> list[RunDiagnosis]:
    """Every run under data/output/, newest run_id first per log — the History page's overview."""
    return [
        diagnose_run(log_stem, run_id)
        for log_stem in artifacts.list_log_stems()
        for run_id in artifacts.list_run_ids(log_stem)
    ]

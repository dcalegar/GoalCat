"""Per-run diagnostics: where a run stopped, which warnings fired, and what each one means.

Complements the live panel on the New Run page (ui_helpers.render_progress_panel), which only
covers a run this GUI launched and only while that page stays open. Everything here is
reconstructed from the run directory's own files, so it works on any run — including one started
from experimentation/examples/*/example_run.py or the ICPM 2027 harness — at any time after it ran.
"""

from __future__ import annotations

import streamlit as st

from gui import artifacts, diagnostics, run_control

st.set_page_config(page_title="GoalCat — Diagnostics", page_icon="🐱", layout="wide")
st.title("Diagnostics")
st.caption(
    "Reconstructed from each run directory's own pipeline.log, gui_status.json and round_info.json "
    "— no run needs to have been launched from this GUI."
)

_OUTCOME_RENDER = {
    "completed": (st.success, "✅"),
    "awaiting_review": (st.info, "🟡"),
    "incomplete": (st.error, "🛑"),
    "running": (st.info, "🔵"),
    "failed": (st.error, "❌"),
    "unknown": (st.warning, "❔"),
}

_SEVERITY_BADGE = {
    "blocking": "🛑 blocking",
    "quality": "⚠️ quality",
    "transient": "🔁 transient",
    "benign": "ℹ️ benign",
    "unclassified": "❓ unclassified",
}

log_stems = artifacts.list_log_stems()
if not log_stems:
    st.info("No runs yet under data/output/.")
    st.stop()

log_stem_index = log_stems.index(st.session_state["nav_log_stem"]) if st.session_state.get("nav_log_stem") in log_stems else 0
log_stem = st.selectbox("Log", log_stems, index=log_stem_index)

run_ids = artifacts.list_run_ids(log_stem)
if not run_ids:
    st.info("This log has no runs yet.")
    st.stop()
run_id_index = run_ids.index(st.session_state["nav_run_id"]) if st.session_state.get("nav_run_id") in run_ids else 0
run_id = st.selectbox("Run (run_id)", run_ids, index=run_id_index)

diagnosis = diagnostics.diagnose_run(log_stem, run_id)

render, icon = _OUTCOME_RENDER[diagnosis.outcome]
render(f"{icon} **{diagnosis.outcome.replace('_', ' ').title()}** — {diagnosis.headline}")
if diagnosis.failure_message:
    st.code(diagnosis.failure_message, language=None)

if not diagnosis.has_log:
    st.stop()

st.subheader("Step timeline")
st.caption(
    "One row per step *execution*, in log order — a step appears twice when Step 9's merge or "
    "split opens a revision round and Steps 5-8 run again."
)
st.dataframe(
    [
        {
            "Round": step.round,
            "Step": step.step,
            "Name": run_control.STEP_NAMES.get(diagnostics.step_key(step.step), "—"),
            "State": "✅ done" if step.state == "done" else "❌ never finished",
            "Started": step.started_at,
            "Ended": step.ended_at or "—",
        }
        for step in diagnosis.steps
    ]
    or [{"Round": "—", "Step": "—", "Name": "No step ever started in this run.", "State": "—", "Started": "—", "Ended": "—"}],
    width="stretch",
    hide_index=True,
)

st.subheader("Warnings")
if not diagnosis.warnings:
    st.success("No warnings or errors in this run's pipeline.log.")
else:
    counts = diagnosis.counts_by_severity
    summary_cols = st.columns(len(counts))
    for col, (severity, count) in zip(summary_cols, sorted(counts.items(), key=lambda kv: diagnostics.SEVERITY_ORDER[kv[0]])):
        with col:
            st.metric(_SEVERITY_BADGE[severity], count, help=diagnostics.SEVERITY_HELP[severity])

    # Grouped by kind rather than listed chronologically: one flaky batch can emit the same
    # warning dozens of times, and a reader needs "which distinct things went wrong" before
    # "in what order".
    grouped: dict[str, list] = {}
    kinds: dict[str, diagnostics.WarningKind] = {}
    for event in diagnosis.warnings:
        kind = diagnostics.classify(event.message)
        kinds[kind.kind_id] = kind
        grouped.setdefault(kind.kind_id, []).append(event)

    for kind_id in sorted(grouped, key=lambda k: (diagnostics.SEVERITY_ORDER[kinds[k].severity], k)):
        kind = kinds[kind_id]
        events = grouped[kind_id]
        with st.expander(f"{_SEVERITY_BADGE[kind.severity]} · {kind.title} — {len(events)}×", expanded=(kind.severity == "blocking")):
            st.markdown(f"**What it means.** {kind.meaning}")
            st.markdown(f"**What to do.** {kind.action}")
            st.caption(f"Emitted by {kind.source}")
            st.divider()
            for event in events:
                step_label = f"Step {event.step}" if event.step else "before any step"
                st.markdown(f"`{event.timestamp}` · {step_label} · round {event.round} · pipeline.log line {event.line_number}")
                st.code(event.message, language=None)

st.subheader("pipeline.log")
log_path = diagnosis.run_dir / "pipeline.log"
tail_size = st.slider("Lines to show (from the end)", min_value=50, max_value=2000, value=200, step=50)
st.code("\n".join(run_control.tail_lines(log_path, tail_size)) or "(empty)", language=None)
st.download_button(
    "Download the full pipeline.log",
    data=log_path.read_bytes(),
    file_name=f"{log_stem}_{run_id}_pipeline.log",
    mime="text/plain",
)

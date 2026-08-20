"""Streamlit rendering helpers shared by gui/pages/*.py. Kept separate from run_control.py,
which must stay Streamlit-free (it's also imported indirectly by gui/worker.py's subprocess)."""

from __future__ import annotations

import os
from pathlib import Path

import streamlit as st

from gui import run_control

API_KEY_ENV_VARS = ("GEMINI_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY")

# Step -> (kind, color) for the home-page pipeline strip. Mirrors the project's own (unrendered)
# pipeline diagram's node classes: deterministic computation, an LLM call, or a human decision.
_STEP_KIND = {
    1: "det", 2: "det", 3: "det", 4: "det",
    5: "llm", 6: "llm",
    7: "det",
    8: "llm",
    9: "human",
}
_KIND_COLOR = {
    "det": "#5b7fa6",
    "llm": "#8a5fbf",
    "human": "#c17a3d",
}
_KIND_LABEL = {"det": "Deterministic", "llm": "LLM call", "human": "Human decision"}


def mask_key(value: str) -> str:
    if len(value) <= 8:
        return "•" * len(value)
    return f"{value[:4]}···{value[-4:]}"


def any_api_key_set() -> bool:
    return any(os.environ.get(k) for k in API_KEY_ENV_VARS)


def render_api_key_status(*, show_setup_link: bool = True) -> None:
    """Compact status row for whichever LLM API keys are set in the environment (shell-exported or
    entered on the Setup page — both land in os.environ, this only ever reads it live)."""
    set_vars = [k for k in API_KEY_ENV_VARS if os.environ.get(k)]
    if set_vars:
        st.success(f"LLM API key detected: {', '.join(set_vars)}. Steps 5, 6, 8, and Step 9 merges/splits are ready to run.")
    else:
        st.warning("No LLM API key detected (GEMINI_API_KEY / OPENAI_API_KEY / ANTHROPIC_API_KEY). Steps 5, 6, 8, and Step 9 merges/splits will fail until one is set.")
        if show_setup_link:
            st.page_link("pages/0_Setup.py", label="Open Setup", icon=":material/key:")


def render_pipeline_diagram() -> None:
    """A small inline HTML/CSS strip of the 9-step pipeline, color-coded by step kind. Home page
    only — no external image asset exists in the repo to embed instead (see project/OVERVIEW.md)."""
    chips = []
    for step, name in run_control.STEP_NAMES.items():
        color = _KIND_COLOR[_STEP_KIND[step]]
        chips.append(
            f'<div style="display:flex;flex-direction:column;align-items:center;min-width:86px;">'
            f'<div style="background:{color};color:white;border-radius:8px;padding:6px 10px;'
            f'font-weight:600;font-size:0.85rem;">{step}</div>'
            f'<div style="font-size:0.72rem;text-align:center;margin-top:4px;color:var(--text-color,inherit);">{name}</div>'
            f"</div>"
        )
        chips.append('<div style="align-self:flex-start;margin-top:10px;color:#999;">→</div>')
    chips.pop()  # drop the trailing arrow

    legend = "".join(
        f'<span style="display:inline-flex;align-items:center;gap:4px;margin-right:14px;font-size:0.78rem;">'
        f'<span style="width:10px;height:10px;border-radius:50%;background:{_KIND_COLOR[k]};display:inline-block;"></span>{label}</span>'
        for k, label in _KIND_LABEL.items()
    )

    st.markdown(
        f'<div style="display:flex;align-items:flex-start;gap:4px;overflow-x:auto;padding:8px 0 4px 0;">{"".join(chips)}</div>'
        f'<div style="margin-top:4px;">{legend}</div>',
        unsafe_allow_html=True,
    )


def render_progress_panel(
    *,
    status_path: Path,
    worker_log_path: Path,
    pipeline_log_path: Path,
    popen,
    steps: list[int],
    success_message: str,
    session_state_key: str,
    popen_state_key: str,
) -> None:
    """Live-updating (every 2s) status view over `steps` + a pipeline.log tail, for a worker
    subprocess launched via run_control.launch_worker(). Auto-refreshes via st.fragment without
    rerunning the rest of the page. Offers a "Stop run" button while the process is still running,
    and on exit offers a "Close" button that clears session_state[session_state_key]/
    [popen_state_key] and triggers a full rerun — done inside the fragment itself (not returned to
    the caller), since a widget click inside a fragment only reruns that fragment by default, so
    the caller's own script body would never see it.
    """
    stopped_flag_key = f"{session_state_key}_stopped"

    @st.fragment(run_every=2)
    def _panel() -> None:
        status = run_control.read_status(status_path)
        returncode = popen.poll()
        entries = (status or {}).get("steps", {})

        done_count = sum(1 for s in steps if entries.get(str(s), {}).get("state") == "done")

        if returncode is None:
            state = "running"
            label = f"Running — {done_count}/{len(steps)} steps complete"
        elif st.session_state.get(stopped_flag_key):
            state = "error"
            label = "Run stopped by user."
        elif returncode == 0:
            state = "complete"
            label = success_message
        else:
            state = "error"
            label = f"Process exited with an error (code {returncode})."

        with st.status(label, state=state, expanded=(state != "complete")):
            for s in steps:
                entry = entries.get(str(s))
                name = run_control.STEP_NAMES[s]
                if entry is None:
                    st.markdown(f"⬜ Step {s} — {name}")
                elif entry["state"] == "running":
                    st.markdown(f"🔵 Step {s} — {name} (in progress...)")
                elif entry["state"] == "done":
                    st.markdown(f"✅ Step {s} — {name}")
                else:
                    st.markdown(f"❌ Step {s} — {name}")
                    if entry.get("error"):
                        st.error(entry["error"])

            with st.expander("pipeline.log (tail)", expanded=False):
                lines = run_control.tail_lines(pipeline_log_path, 200)
                st.code("\n".join(lines) or "(nothing yet)", language=None)

            if returncode is not None and returncode != 0 and not st.session_state.get(stopped_flag_key):
                worker_log = run_control.tail_lines(worker_log_path, 50)
                if worker_log:
                    with st.expander("Process output (worker)", expanded=True):
                        st.code("\n".join(worker_log), language=None)

        if returncode is None:
            already_stopping = st.session_state.get(stopped_flag_key, False)
            if st.button(
                "🛑 Stop run",
                key=f"stop_{session_state_key}",
                disabled=already_stopping,
                help="Sends a termination signal to the running pipeline process.",
            ):
                popen.terminate()
                st.session_state[stopped_flag_key] = True
                st.rerun()
            elif already_stopping:
                st.caption("Stopping…")
        else:
            if st.button("Close", key=f"close_{session_state_key}"):
                st.session_state.pop(session_state_key, None)
                st.session_state.pop(popen_state_key, None)
                st.session_state.pop(stopped_flag_key, None)
                st.rerun()

    _panel()

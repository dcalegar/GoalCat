"""Streamlit rendering helpers shared by gui/pages/*.py. Kept separate from run_control.py,
which must stay Streamlit-free (it's also imported indirectly by gui/worker.py's subprocess)."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from gui import run_control


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
    """Live-updating (every 2s) checklist over `steps` + a pipeline.log tail, for a worker
    subprocess launched via run_control.launch_worker(). Auto-refreshes via st.fragment without
    rerunning the rest of the page. On exit, offers a "Cerrar" button that clears
    session_state[session_state_key]/[popen_state_key] and triggers a full rerun — done inside
    the fragment itself (not returned to the caller), since a widget click inside a fragment only
    reruns that fragment by default, so the caller's own script body would never see it.
    """

    @st.fragment(run_every=2)
    def _panel() -> None:
        status = run_control.read_status(status_path)
        returncode = popen.poll()
        entries = (status or {}).get("steps", {})

        done_count = sum(1 for s in steps if entries.get(str(s), {}).get("state") == "done")
        st.progress(done_count / len(steps), text=f"{done_count}/{len(steps)} steps completados")

        for s in steps:
            entry = entries.get(str(s))
            name = run_control.STEP_NAMES[s]
            if entry is None:
                st.markdown(f"⬜ Step {s} — {name}")
            elif entry["state"] == "running":
                st.markdown(f"🔵 Step {s} — {name} (en curso...)")
            elif entry["state"] == "done":
                st.markdown(f"✅ Step {s} — {name}")
            else:
                st.markdown(f"❌ Step {s} — {name}")
                if entry.get("error"):
                    st.error(entry["error"])

        with st.expander("pipeline.log (últimas líneas)", expanded=False):
            lines = run_control.tail_lines(pipeline_log_path, 200)
            st.code("\n".join(lines) or "(sin datos aún)", language=None)

        if returncode is not None:
            if returncode == 0:
                st.success(success_message)
            else:
                st.error(f"El proceso terminó con error (código {returncode}).")
                worker_log = run_control.tail_lines(worker_log_path, 50)
                if worker_log:
                    with st.expander("Salida del proceso (worker)", expanded=True):
                        st.code("\n".join(worker_log), language=None)

            if st.button("Cerrar", key=f"close_{session_state_key}"):
                st.session_state.pop(session_state_key, None)
                st.session_state.pop(popen_state_key, None)
                st.rerun()

    _panel()

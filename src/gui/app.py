"""GoalCat pipeline GUI — entry point.

Run with `streamlit run src/gui/app.py` (see project README's "Running the GUI" section). Pure
orchestration over the existing library (goalcat.pipeline / goalcat.config / goalcat.review) — no
pipeline logic lives here or in gui/pages/; see gui/worker.py, gui/run_control.py,
gui/config_form.py, gui/artifacts.py.
"""

from __future__ import annotations

import streamlit as st

from gui import ui_helpers

st.set_page_config(page_title="GoalCat", page_icon="🐱", layout="wide")

st.title("🐱 GoalCat")
st.markdown(
    "**GoalCat is a goal-driven process-variant categorization pipeline.** Process discovery on "
    "real event logs typically yields unreadable \"spaghetti\" models; the conventional fix "
    "clusters variants on their structure first and attaches a business-meaning label afterward. "
    "GoalCat inverts that order. A goal model (GRL/URN), authored from an organization's published "
    "process documentation, declares what the process is *for*; its decomposition into alternative "
    "tasks **is** the taxonomy. Each process variant is rendered as a natural-language narrative, "
    "and an LLM matches it against the goal model's declared alternatives rather than inventing "
    "categories from scratch. What matches nothing is not discarded — it is reported as a "
    "*residual*, evidence the goal model doesn't yet cover something the process actually does. "
    "Without a goal model, the same pipeline falls back to open taxonomy induction instead."
)

st.subheader("Pipeline at a glance")
ui_helpers.render_pipeline_diagram()

st.subheader("Get started")
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    with st.container(border=True):
        st.markdown("**1 · Setup**")
        st.caption("Check or enter your LLM API key.")
        st.page_link("pages/0_Setup.py", label="Open Setup", icon=":material/key:")
with c2:
    with st.container(border=True):
        st.markdown("**2 · New run**")
        st.caption("Pick a log + goal model, tune the config, launch Steps 1-8.")
        st.page_link("pages/1_New_Run.py", label="Open New Run", icon=":material/play_arrow:")
with c3:
    with st.container(border=True):
        st.markdown("**3 · Review**")
        st.caption("Accept, rename, merge, or split categories (Step 9).")
        st.page_link("pages/3_Review.py", label="Open Review", icon=":material/rate_review:")
with c4:
    with st.container(border=True):
        st.markdown("**4 · Results & history**")
        st.caption("Browse any run's variants, taxonomy, models, and reports.")
        st.page_link("pages/2_Results.py", label="Open Results", icon=":material/insights:")

with c5:
    with st.container(border=True):
        st.markdown("**5 · Diagnostics**")
        st.caption("See where a run stopped and what its warnings mean.")
        st.page_link("pages/5_Diagnostics.py", label="Open Diagnostics", icon=":material/troubleshoot:")

ui_helpers.render_api_key_status()

st.subheader("Study cases available in data/logs/ + data/goals/")
st.dataframe(
    [
        {
            "Log": "RTFM",
            "Domain": "Road traffic fine management (Italian local police)",
            "Scale": "150,370 cases / 561,470 events (or the 6-case rtfm_mini fixture)",
            "Goal model": "rtfm_goal_model.jucm",
        },
        {
            "Log": "BPIC 2019",
            "Domain": "Purchase-order handling, multinational coatings company",
            "Scale": "251,734 cases / 1,595,923 events",
            "Goal model": "bpic2019_goal_model.jucm",
        },
        {
            "Log": "Sepsis",
            "Domain": "Hospital pathway of sepsis patients",
            "Scale": "~1,000 cases / ~15,000 events",
            "Goal model": "sepsis_goal_model.jucm",
        },
    ],
    width="stretch",
    hide_index=True,
)
st.caption("See `data/README.md` for publisher references and per-case study status.")

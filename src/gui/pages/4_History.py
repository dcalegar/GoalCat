from __future__ import annotations

import streamlit as st

from gui import artifacts

st.set_page_config(page_title="GoalCat — History", page_icon="🐱", layout="wide")
st.title("Run history")

log_stems = artifacts.list_log_stems()
if not log_stems:
    st.info("No runs yet under data/output/.")
    st.stop()

rows = []
for log_stem in log_stems:
    for run_id in artifacts.list_run_ids(log_stem):
        run_dir = artifacts.run_output_dir(log_stem, run_id)
        rounds = artifacts.list_rounds(run_dir)
        latest = rounds[-1] if rounds else None
        snapshot = artifacts.config_snapshot(run_dir) or {}
        rows.append(
            {
                "log": log_stem,
                "run_id": run_id,
                "rounds": len(rounds),
                "latest_round_status": latest["status"] if latest else "(no rounds)",
                "accepted": "Yes" if latest and latest["status"] == "accepted" else "No",
                "taxonomy_mode": snapshot.get("taxonomy_mode", "?"),
                "sample_frequent_n": snapshot.get("sample_frequent_n", "?"),
                "sample_rare_n": snapshot.get("sample_rare_n", "?"),
                "sample_extreme_n": snapshot.get("sample_extreme_n", "?"),
            }
        )

st.dataframe(rows, width="stretch")

st.divider()
st.subheader("Open a run")
labels = [f"{r['log']} / {r['run_id']}" for r in rows]
choice = st.selectbox("Run", labels)
chosen = rows[labels.index(choice)]
st.session_state["nav_log_stem"] = chosen["log"]
st.session_state["nav_run_id"] = chosen["run_id"]

col1, col2 = st.columns(2)
with col1:
    if st.button("View in Results"):
        st.switch_page("pages/2_Results.py")
with col2:
    if st.button("View in Review", disabled=chosen["latest_round_status"] != "pending_review"):
        st.switch_page("pages/3_Review.py")

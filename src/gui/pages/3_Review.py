from __future__ import annotations

from pathlib import Path

import streamlit as st
import yaml

from goalcat.config import DISCOVERY_DIRNAME, REVIEW_DIRNAME, TAXONOMY_DIRNAME
from goalcat.discovery import flag_low_precision_categories
from goalcat.review import MergeDecision, RenameDecision, ReviewDecisions, SplitDecision
from gui import artifacts, run_control, ui_helpers

st.set_page_config(page_title="GoalCat — Review", page_icon="🐱", layout="wide")
st.title("Review (Step 9)")

ACTIVE_KEY = "gui_active_review"
POPEN_KEY = "_gui_review_popen"

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

run_dir = artifacts.run_output_dir(log_stem, run_id)

active = st.session_state.get(ACTIVE_KEY)
if active is not None and active["run_id"] == run_id:
    st.divider()
    st.subheader(f"Processing review: round {active['round']}")
    ui_helpers.render_progress_panel(
        status_path=Path(active["status_path"]),
        worker_log_path=Path(active["worker_log_path"]),
        pipeline_log_path=run_dir / "pipeline.log",
        popen=st.session_state[POPEN_KEY],
        steps=[9],
        success_message="Review processed — reselect the run above to see the result.",
        session_state_key=ACTIVE_KEY,
        popen_state_key=POPEN_KEY,
    )
    st.stop()

rounds = artifacts.list_rounds(run_dir)
pending = [r for r in rounds if r["status"] == "pending_review"]
if not pending:
    st.info("No round is awaiting review for this run.")
    st.stop()

round_num = pending[-1]["round"]
rd = artifacts.round_dir(run_dir, round_num)
st.caption(f"Reviewing round {round_num}.")

index_text = artifacts.read_text(run_dir / "review_index.md")
if index_text:
    with st.expander("review_index.md", expanded=False):
        st.markdown(index_text)

taxonomy = artifacts.read_taxonomy(rd / TAXONOMY_DIRNAME / "taxonomy.json")
if taxonomy is None:
    st.error("No taxonomy.json for this round yet.")
    st.stop()

category_ids = [c.category_id for c in taxonomy.categories]

# Step 7 metrics, advisory only — same source flag_low_precision_categories() feeds into the
# CLI's review_decisions.yaml template comment (goalcat.review._quality_flags_comment); the GUI
# bypasses that template entirely (it writes ReviewDecisions directly further below), so this is
# where the equivalent signal has to surface for a GUI reviewer instead.
metrics_df = artifacts.read_csv(rd / DISCOVERY_DIRNAME / "discovery_metrics.csv")
metrics_by_id: dict[str, dict] = {}
flagged_ids: set[str] = set()
precision_threshold = 0.3
if metrics_df is not None:
    metrics_by_id = metrics_df.set_index("category_id").to_dict(orient="index")
    gui_config_path = run_dir / "gui_run_config.yaml"
    if gui_config_path.exists():
        raw_config = yaml.safe_load(gui_config_path.read_text(encoding="utf-8")) or {}
        precision_threshold = float(raw_config.get("review_precision_flag_threshold", precision_threshold))
    flagged_ids = {f["category_id"] for f in flag_low_precision_categories(metrics_df, precision_threshold)}

st.subheader("Categories")
ACTION_CHOICES = ["Keep", "Rename", "Merge", "Split"]
actions: dict[str, str] = {}
new_names: dict[str, str] = {}
new_descriptions: dict[str, str] = {}
reasons: dict[str, str] = {}

for c in taxonomy.categories:
    flagged = c.category_id in flagged_ids
    label = f"{c.category_id} — {c.name}"
    if flagged:
        label += " ⚠️ low precision"
    with st.expander(label, expanded=False):
        st.caption(c.description)
        stats = metrics_by_id.get(c.category_id)
        if stats is not None and stats["num_variants"] > 0:
            metric_line = (
                f"Step 7: precision={stats['precision']:.3f}, log_fitness={stats['log_fitness']:.3f}, "
                f"{int(stats['num_variants'])} variants, {int(stats['num_cases'])} cases"
            )
            if flagged:
                st.warning(
                    f"{metric_line} — below the {precision_threshold} flag threshold. Low precision "
                    "under this pipeline's fitness-preserving discovery can mean the sublog still "
                    "spans multiple distinct behavioral patterns; consider a split. Heuristic only, "
                    "not a decision — check discovery_report.md before acting."
                )
            else:
                st.caption(metric_line)
        elif stats is not None:
            st.caption("Step 7: no variants assigned — discovery skipped.")
        action = st.pills(
            "Action",
            ACTION_CHOICES,
            default="Keep",
            key=f"action_{c.category_id}",
        )
        action = action or "Keep"
        actions[c.category_id] = action
        if action == "Rename":
            new_names[c.category_id] = st.text_input("New name", c.name, key=f"name_{c.category_id}")
            new_descriptions[c.category_id] = st.text_area(
                "New description", c.description, key=f"desc_{c.category_id}"
            )
            reasons[c.category_id] = st.text_input("Reason", key=f"reason_{c.category_id}")
        elif action == "Merge":
            others = [cid for cid in category_ids if cid != c.category_id]
            st.multiselect("Merge with", others, key=f"merge_{c.category_id}")
            reasons[c.category_id] = st.text_input("Reason", key=f"reason_{c.category_id}")
        elif action == "Split":
            reasons[c.category_id] = st.text_input("Reason for the split", key=f"reason_{c.category_id}")

st.divider()
notes = st.text_area("General notes (optional)")

col_a, col_b = st.columns(2)
with col_a:
    accept_clicked = st.button(
        "Accept taxonomy as-is",
        type="primary",
        disabled=any(a != "Keep" for a in actions.values()),
        help="Only available if no category has a pending action.",
    )
with col_b:
    submit_clicked = st.button(
        "Submit decision (revise)",
        disabled=all(a == "Keep" for a in actions.values()),
    )


def _build_decisions(decision_kind: str) -> ReviewDecisions:
    renames, merges, splits = [], [], []
    for cid, action in actions.items():
        reason = reasons.get(cid) or "(no reason given from the GUI)"
        if action == "Rename":
            renames.append(
                RenameDecision(
                    category_id=cid,
                    new_name=new_names.get(cid),
                    new_description=new_descriptions.get(cid),
                    reason=reason,
                )
            )
        elif action == "Merge":
            others = st.session_state.get(f"merge_{cid}", [])
            if others:
                merges.append(MergeDecision(category_ids=[cid, *others], reason=reason))
        elif action == "Split":
            splits.append(SplitDecision(category_id=cid, reason=reason))
    return ReviewDecisions(decision=decision_kind, notes=notes or None, renames=renames, merges=merges, splits=splits)


decisions_to_submit: ReviewDecisions | None = None
if accept_clicked:
    try:
        decisions_to_submit = _build_decisions("accept")
    except Exception as exc:  # pydantic ValidationError, shown verbatim — same convention as Step 9 itself
        st.error(str(exc))
elif submit_clicked:
    try:
        decisions_to_submit = _build_decisions("revise")
    except Exception as exc:
        st.error(str(exc))

if decisions_to_submit is not None:
    decisions_path = rd / REVIEW_DIRNAME / "review_decisions.yaml"
    decisions_path.parent.mkdir(parents=True, exist_ok=True)
    decisions_path.write_text(
        yaml.safe_dump(decisions_to_submit.model_dump(mode="json"), sort_keys=False), encoding="utf-8"
    )

    config_path = run_dir / "gui_run_config.yaml"
    if not config_path.exists():
        st.error(
            f"Could not find {config_path} — this run was not created from the GUI, so there is no "
            "config of its own to re-invoke Step 9 with. Run Step 9 from a script for this run "
            "(see goalcat.pipeline.run_step9_review)."
        )
    else:
        popen = run_control.launch_worker(config_path, run_id, "9", round_num, rd)
        st.session_state[ACTIVE_KEY] = {
            "run_id": run_id,
            "round": round_num,
            "status_path": str(rd / run_control.STATUS_FILENAME),
            "worker_log_path": str(rd / run_control.WORKER_LOG_FILENAME),
        }
        st.session_state[POPEN_KEY] = popen
        st.rerun()

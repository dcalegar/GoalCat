from __future__ import annotations

from pathlib import Path

import streamlit as st

from goalcat.config import new_run_id
from gui import config_form, run_control, ui_helpers

st.set_page_config(page_title="GoalCat — New Run", page_icon="🐱", layout="wide")
st.title("New run")

ACTIVE_KEY = "gui_active_run"
POPEN_KEY = "_gui_popen"

with st.expander("Add a new log or goal model", expanded=False):
    st.caption("Only files not already in `data/logs/` / `data/goals/` can be added here — pick a different name, or remove the existing one first, to replace one.")
    up_col1, up_col2 = st.columns(2)
    with up_col1:
        log_upload = st.file_uploader("Event log (.xes or .xes.gz)", key="log_upload")
        if log_upload is not None and st.button("Save log", key="save_log_upload"):
            try:
                config_form.save_uploaded_log(log_upload.name, log_upload.getvalue())
            except (ValueError, FileExistsError) as exc:
                st.error(str(exc))
            else:
                st.success(f"Saved `{log_upload.name}` to data/logs/.")
                st.rerun()
    with up_col2:
        goal_upload = st.file_uploader("Goal model (.jucm)", key="goal_upload")
        if goal_upload is not None and st.button("Save goal model", key="save_goal_upload"):
            try:
                config_form.save_uploaded_goal_model(goal_upload.name, goal_upload.getvalue())
            except (ValueError, FileExistsError) as exc:
                st.error(str(exc))
            else:
                st.success(f"Saved `{goal_upload.name}` to data/goals/.")
                st.rerun()

logs = config_form.list_log_filenames()
if not logs:
    st.error(f"No logs found in {config_form.LOGS_DIR}. Upload one above.")
    st.stop()

log_filename = st.selectbox("Log (data/logs/)", logs)
default_config_path = config_form.find_default_config_for_log(log_filename)
defaults = config_form.load_config_dict(default_config_path)
st.caption(f"Defaults loaded from `{default_config_path.relative_to(config_form.REPO_ROOT)}`.")

goal_models = ["(none — open mode)"] + config_form.list_goal_model_filenames()
default_goal = defaults.get("goal_model_filename")
goal_index = goal_models.index(default_goal) if default_goal in goal_models else 0
goal_model_choice = st.selectbox("Goal model (data/goals/)", goal_models, index=goal_index)
goal_model_filename = None if goal_model_choice.startswith("(none") else goal_model_choice

col1, col2 = st.columns(2)
with col1:
    case_id_key = st.text_input("case_id_key", defaults.get("case_id_key", "case:concept:name"))
    activity_key = st.text_input("activity_key", defaults.get("activity_key", "concept:name"))
    timestamp_key = st.text_input("timestamp_key", defaults.get("timestamp_key", "time:timestamp"))
    resource_key = st.text_input("resource_key", defaults.get("resource_key", "org:resource"))

    taxonomy_mode_options = ["intent_guided", "open"]
    default_mode = defaults.get("taxonomy_mode", "intent_guided")
    if goal_model_filename is None:
        default_mode = "open"
    taxonomy_mode = st.selectbox(
        "taxonomy_mode",
        taxonomy_mode_options,
        index=taxonomy_mode_options.index(default_mode) if default_mode in taxonomy_mode_options else 0,
        disabled=goal_model_filename is None,
        help="Only 'open' is available without a goal model." if goal_model_filename is None else None,
    )
    if goal_model_filename is None:
        taxonomy_mode = "open"
with col2:
    sample_frequent_n = st.number_input("sample_frequent_n", min_value=0, value=int(defaults.get("sample_frequent_n", 10)))
    sample_rare_n = st.number_input("sample_rare_n", min_value=0, value=int(defaults.get("sample_rare_n", 10)))
    sample_extreme_n = st.number_input("sample_extreme_n", min_value=0, value=int(defaults.get("sample_extreme_n", 5)))
    discovery_noise_threshold = st.slider(
        "discovery_noise_threshold", 0.0, 1.0, float(defaults.get("discovery_noise_threshold", 0.0))
    )

with st.expander("Performance", expanded=False):
    st.caption(
        "Opt-in flags that trade computation cost for lost information. Off by default: whether "
        "the tradeoff is worth it is a human-in-the-loop decision, made per run, not automated."
    )
    skip_precision = st.checkbox(
        "skip_precision",
        value=bool(defaults.get("skip_precision", False)),
        help=(
            "Skip Step 7's precision computation (token-based replay) — the single confirmed "
            "single-threaded/GIL-bound cost driver in the pipeline, scaling with each category's "
            "unique prefix count rather than its variant count. Fitness is still computed. "
            "precision is reported as NaN throughout, and Step 9's automated low-precision review "
            "flag has nothing to flag. Off by default."
        ),
    )
    skip_pairwise_distances = st.checkbox(
        "skip_pairwise_distances",
        value=bool(defaults.get("skip_pairwise_distances", False)),
        help=(
            "Skip Step 6's pairwise structural/profile distance computation "
            "(structural_distances.parquet/profile_distances.parquet) — the only O(n^2) "
            "computation in the pipeline (see README's Resource usage section). "
            "assignment_report.md's per-category cohesion/divergence sections and "
            "assignments.csv's nearest-neighbor columns are empty for this round. Off by default."
        ),
    )
    prune_pairwise_distances_on_finalize = st.checkbox(
        "prune_pairwise_distances_on_finalize",
        value=bool(defaults.get("prune_pairwise_distances_on_finalize", False)),
        help=(
            "On accept (Step 9), delete structural_distances.parquet/profile_distances.parquet from "
            "every round of this run, not just the accepted one. These are Step 6's O(n^2) "
            "pairwise variant-distance tables — the largest artifact class at scale (see "
            "README's Resource usage section). Off by default: a superseded round's copies are "
            "what a later rename re-render reads back, with no cheaper way to regenerate them "
            "than a full Step 6 recompute. Set once, before the run starts — this cannot be "
            "changed later without triggering a config-drift error at Step 9. Moot if "
            "skip_pairwise_distances is already on — there is nothing left to prune."
        ),
    )

llm_defaults = defaults.get("llm", {})
taxonomy_model = llm_defaults.get("taxonomy_model", "gemini/gemini-3.5-flash-lite")
assignment_model = llm_defaults.get("assignment_model", "gemini/gemini-3.5-flash-lite")
description_model = llm_defaults.get("description_model", "gemini/gemini-3.5-flash-lite")

with st.expander("Advanced LLM settings (Steps 5, 6, 8)", expanded=False):
    c1, c2, c3 = st.columns(3)
    with c1:
        taxonomy_model = st.text_input("taxonomy_model", taxonomy_model)
        assignment_model = st.text_input("assignment_model", assignment_model)
        description_model = st.text_input("description_model", description_model)
    with c2:
        temperature = st.number_input("temperature", min_value=0.0, max_value=2.0, value=float(llm_defaults.get("temperature", 0)))
        timeout_seconds = st.number_input("timeout_seconds", min_value=1, value=int(llm_defaults.get("timeout_seconds", 120)))
        max_retries = st.number_input("max_retries", min_value=0, value=int(llm_defaults.get("max_retries", 3)))
    with c3:
        concurrency = st.number_input("concurrency", min_value=1, value=int(llm_defaults.get("concurrency", 1)))
        requests_per_minute = st.number_input(
            "requests_per_minute (0 = no limit)", min_value=0, value=int(llm_defaults.get("requests_per_minute") or 0)
        )
        assignment_batch_size = st.number_input(
            "assignment_batch_size", min_value=1, value=int(llm_defaults.get("assignment_batch_size", 20))
        )

ui_helpers.render_api_key_status()

if st.button("Run pipeline (Steps 1-8)", type="primary", disabled=ACTIVE_KEY in st.session_state):
    run_id = new_run_id()
    llm = {
        "taxonomy_model": taxonomy_model,
        "assignment_model": assignment_model,
        "description_model": description_model,
        "temperature": temperature,
        "timeout_seconds": int(timeout_seconds),
        "max_retries": int(max_retries),
        "concurrency": int(concurrency),
        "requests_per_minute": int(requests_per_minute) or None,
        "assignment_batch_size": int(assignment_batch_size),
    }
    config_dict = config_form.build_config_dict(
        log_filename=log_filename,
        goal_model_filename=goal_model_filename,
        case_id_key=case_id_key,
        activity_key=activity_key,
        timestamp_key=timestamp_key,
        resource_key=resource_key,
        sample_frequent_n=int(sample_frequent_n),
        sample_rare_n=int(sample_rare_n),
        sample_extreme_n=int(sample_extreme_n),
        taxonomy_mode=taxonomy_mode,
        discovery_noise_threshold=float(discovery_noise_threshold),
        skip_precision=bool(skip_precision),
        prune_pairwise_distances_on_finalize=bool(prune_pairwise_distances_on_finalize),
        skip_pairwise_distances=bool(skip_pairwise_distances),
        llm=llm,
    )

    run_dir = config_form.run_output_dir_for(log_filename, run_id)
    gui_config_path = run_dir / "gui_run_config.yaml"
    config_form.write_run_config(config_dict, gui_config_path)

    popen = run_control.launch_worker(gui_config_path, run_id, "1-8", None, run_dir)

    st.session_state[ACTIVE_KEY] = {
        "run_id": run_id,
        "log_stem": config_form.log_stem_of(log_filename),
        "run_dir": str(run_dir),
        "status_path": str(run_dir / run_control.STATUS_FILENAME),
        "worker_log_path": str(run_dir / run_control.WORKER_LOG_FILENAME),
    }
    st.session_state[POPEN_KEY] = popen
    st.rerun()

if ACTIVE_KEY in st.session_state:
    info = st.session_state[ACTIVE_KEY]
    st.divider()
    st.subheader(f"Run in progress: {info['run_id']}")
    ui_helpers.render_progress_panel(
        status_path=Path(info["status_path"]),
        worker_log_path=Path(info["worker_log_path"]),
        pipeline_log_path=Path(info["run_dir"]) / "pipeline.log",
        popen=st.session_state[POPEN_KEY],
        steps=list(range(1, 9)),
        success_message=(
            f"Steps 1-8 complete. Open **Review** or **Results** from the sidebar for run "
            f"`{info['run_id']}`."
        ),
        session_state_key=ACTIVE_KEY,
        popen_state_key=POPEN_KEY,
    )

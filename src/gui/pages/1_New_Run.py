from __future__ import annotations

import os
from pathlib import Path

import streamlit as st

from goalcat.config import new_run_id
from gui import config_form, run_control, ui_helpers

st.set_page_config(page_title="GoalCat — Nueva corrida", page_icon="🐱", layout="wide")
st.title("Nueva corrida")

ACTIVE_KEY = "gui_active_run"
POPEN_KEY = "_gui_popen"

logs = config_form.list_log_filenames()
if not logs:
    st.error(f"No se encontraron logs en {config_form.LOGS_DIR}.")
    st.stop()

log_filename = st.selectbox("Log (data/logs/)", logs)
default_config_path = config_form.find_default_config_for_log(log_filename)
defaults = config_form.load_config_dict(default_config_path)
st.caption(f"Valores por defecto cargados de `{default_config_path.relative_to(config_form.REPO_ROOT)}`.")

goal_models = ["(ninguno — modo open)"] + config_form.list_goal_model_filenames()
default_goal = defaults.get("goal_model_filename")
goal_index = goal_models.index(default_goal) if default_goal in goal_models else 0
goal_model_choice = st.selectbox("Goal model (data/goals/)", goal_models, index=goal_index)
goal_model_filename = None if goal_model_choice.startswith("(ninguno") else goal_model_choice

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
        help="Sin goal model sólo está disponible 'open'." if goal_model_filename is None else None,
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

st.subheader("LLM (Steps 5, 6, 8)")
llm_defaults = defaults.get("llm", {})
c1, c2, c3 = st.columns(3)
with c1:
    taxonomy_model = st.text_input("taxonomy_model", llm_defaults.get("taxonomy_model", "gemini/gemini-3.5-flash-lite"))
    assignment_model = st.text_input("assignment_model", llm_defaults.get("assignment_model", "gemini/gemini-3.5-flash-lite"))
    description_model = st.text_input("description_model", llm_defaults.get("description_model", "gemini/gemini-3.5-flash-lite"))
with c2:
    temperature = st.number_input("temperature", min_value=0.0, max_value=2.0, value=float(llm_defaults.get("temperature", 0)))
    timeout_seconds = st.number_input("timeout_seconds", min_value=1, value=int(llm_defaults.get("timeout_seconds", 120)))
    max_retries = st.number_input("max_retries", min_value=0, value=int(llm_defaults.get("max_retries", 3)))
with c3:
    concurrency = st.number_input("concurrency", min_value=1, value=int(llm_defaults.get("concurrency", 1)))
    requests_per_minute = st.number_input(
        "requests_per_minute (0 = sin límite)", min_value=0, value=int(llm_defaults.get("requests_per_minute") or 0)
    )
    assignment_batch_size = st.number_input(
        "assignment_batch_size", min_value=1, value=int(llm_defaults.get("assignment_batch_size", 20))
    )

if not any(os.environ.get(k) for k in ("GEMINI_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY")):
    st.warning("No se detectó ninguna API key de LLM en el entorno (ver página principal).")

if st.button("Ejecutar pipeline (Steps 1-8)", type="primary", disabled=ACTIVE_KEY in st.session_state):
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
    st.subheader(f"Corrida en curso: {info['run_id']}")
    ui_helpers.render_progress_panel(
        status_path=Path(info["status_path"]),
        worker_log_path=Path(info["worker_log_path"]),
        pipeline_log_path=Path(info["run_dir"]) / "pipeline.log",
        popen=st.session_state[POPEN_KEY],
        steps=list(range(1, 9)),
        success_message=(
            "Steps 1-8 completados. Abrí **Revisión** o **Resultados** desde la barra lateral "
            f"para la corrida `{info['run_id']}`."
        ),
        session_state_key=ACTIVE_KEY,
        popen_state_key=POPEN_KEY,
    )

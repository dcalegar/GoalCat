from __future__ import annotations

import streamlit as st

from goalcat.config import (
    ASSIGNMENT_DIRNAME,
    DESCRIPTION_DIRNAME,
    DISCOVERY_DIRNAME,
    FINAL_DIRNAME,
    PROFILING_DIRNAME,
    SAMPLING_DIRNAME,
    TAXONOMY_DIRNAME,
    TEXTUALIZATION_DIRNAME,
    VARIANTS_DIRNAME,
)
from gui import artifacts

st.set_page_config(page_title="GoalCat — Resultados", page_icon="🐱", layout="wide")
st.title("Resultados")


def _show_df(df) -> None:
    if df is None:
        st.info("Sin datos.")
    elif df.empty:
        st.info("Tabla vacía.")
    else:
        st.dataframe(df, width="stretch")


log_stems = artifacts.list_log_stems()
if not log_stems:
    st.info("Todavía no hay corridas en data/output/.")
    st.stop()

log_stem_index = log_stems.index(st.session_state["nav_log_stem"]) if st.session_state.get("nav_log_stem") in log_stems else 0
log_stem = st.selectbox("Log", log_stems, index=log_stem_index)

run_ids = artifacts.list_run_ids(log_stem)
run_id_index = run_ids.index(st.session_state["nav_run_id"]) if st.session_state.get("nav_run_id") in run_ids else 0
run_id = st.selectbox("Corrida (run_id)", run_ids, index=run_id_index)

run_dir = artifacts.run_output_dir(log_stem, run_id)
rounds = artifacts.list_rounds(run_dir)
if not rounds:
    st.warning("Esta corrida todavía no tiene ninguna ronda (Steps 5-9) completa.")
    st.stop()

round_labels = [f"Ronda {r['round']} — {r['status']}" for r in rounds]
round_choice = st.selectbox("Ronda", round_labels, index=len(round_labels) - 1)
round_num = rounds[round_labels.index(round_choice)]["round"]
rd = artifacts.round_dir(run_dir, round_num)

tabs = st.tabs(
    ["Variantes", "Perfiles", "Narrativas", "Muestra", "Taxonomía", "Asignación", "Discovery", "Descripción", "Final"]
)

with tabs[0]:
    _show_df(artifacts.read_csv(run_dir / VARIANTS_DIRNAME / "variants.csv"))

with tabs[1]:
    _show_df(artifacts.read_csv(run_dir / PROFILING_DIRNAME / "profiles.csv"))

with tabs[2]:
    _show_df(artifacts.read_csv(run_dir / TEXTUALIZATION_DIRNAME / "narratives.csv"))

with tabs[3]:
    _show_df(artifacts.read_csv(run_dir / SAMPLING_DIRNAME / "narrative_sample.csv"))

with tabs[4]:
    taxonomy = artifacts.read_taxonomy(rd / TAXONOMY_DIRNAME / "taxonomy.json")
    if taxonomy is None:
        taxonomy = artifacts.read_taxonomy(run_dir / FINAL_DIRNAME / "taxonomy.json")
    if taxonomy is None:
        st.info("Sin taxonomía todavía.")
    else:
        st.dataframe(
            [{"category_id": c.category_id, "name": c.name, "description": c.description} for c in taxonomy.categories],
            width="stretch",
        )

with tabs[5]:
    report = artifacts.read_text(rd / ASSIGNMENT_DIRNAME / "assignment_report.md")
    df = artifacts.read_csv(rd / ASSIGNMENT_DIRNAME / "assignments.csv")
    if report:
        st.markdown(report)
    if df is not None:
        with st.expander("assignments.csv"):
            _show_df(df)
    if not report and df is None:
        st.info("Sin datos.")

with tabs[6]:
    report = artifacts.read_text(rd / DISCOVERY_DIRNAME / "discovery_report.md")
    metrics = artifacts.read_csv(rd / DISCOVERY_DIRNAME / "discovery_metrics.csv")
    if report:
        st.markdown(report)
    if metrics is not None:
        with st.expander("discovery_metrics.csv"):
            _show_df(metrics)
    models_dir = rd / DISCOVERY_DIRNAME / "models"
    if models_dir.is_dir():
        for img in sorted(models_dir.glob("*.png")):
            st.image(str(img), caption=img.stem)
            pnml = img.with_suffix(".pnml")
            if pnml.exists():
                st.download_button(
                    f"Descargar {pnml.name}", pnml.read_bytes(), file_name=pnml.name, key=f"pnml_{img.stem}"
                )
    if not report and metrics is None:
        st.info("Sin datos (¿ronda ya aceptada? los modelos se borran al aceptar — ver pestaña Final).")

with tabs[7]:
    report = artifacts.read_text(rd / DESCRIPTION_DIRNAME / "description_report.md")
    if report:
        st.markdown(report)
    else:
        st.info("Sin datos.")

with tabs[8]:
    final_dir = run_dir / FINAL_DIRNAME
    readme = artifacts.read_text(final_dir / "README.md")
    if readme:
        st.markdown(readme)
        for f in sorted(final_dir.glob("*.xes.gz")):
            st.download_button(f"Descargar {f.name}", f.read_bytes(), file_name=f.name, key=f"xes_{f.name}")
    else:
        st.info("Esta corrida todavía no fue aceptada (sin final/).")

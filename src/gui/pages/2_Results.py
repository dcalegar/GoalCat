from __future__ import annotations

import streamlit as st

from goalcat.config import (
    ASSIGNMENT_DIRNAME,
    DESCRIPTION_DIRNAME,
    DISCOVERY_DIRNAME,
    FINAL_DIRNAME,
    INDICATORS_DIRNAME,
    PROFILING_DIRNAME,
    SAMPLING_DIRNAME,
    SUBLOGS_DIRNAME,
    TAXONOMY_DIRNAME,
    TEXTUALIZATION_DIRNAME,
    VARIANTS_DIRNAME,
)
from gui import artifacts

st.set_page_config(page_title="GoalCat — Results", page_icon="🐱", layout="wide")
st.title("Results")


def _show_df(df) -> None:
    if df is None:
        st.info("No data.")
    elif df.empty:
        st.info("Empty table.")
    else:
        st.dataframe(df, width="stretch")


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
rounds = artifacts.list_rounds(run_dir)
if not rounds:
    st.warning("This run has no round (Steps 5-9) complete yet.")
    st.stop()

round_labels = [f"Round {r['round']} — {r['status']}" for r in rounds]
round_choice = st.selectbox("Round", round_labels, index=len(round_labels) - 1)
round_num = rounds[round_labels.index(round_choice)]["round"]
rd = artifacts.round_dir(run_dir, round_num)

variants_df = artifacts.read_csv(run_dir / VARIANTS_DIRNAME / "variants.csv")
taxonomy = artifacts.read_taxonomy(rd / TAXONOMY_DIRNAME / "taxonomy.json")
if taxonomy is None:
    taxonomy = artifacts.read_taxonomy(run_dir / FINAL_DIRNAME / "taxonomy.json")
assignments_df = artifacts.read_csv(rd / ASSIGNMENT_DIRNAME / "assignments.csv")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Variants", len(variants_df) if variants_df is not None else "—")
m2.metric("Categories", len(taxonomy.categories) if taxonomy is not None else "—")
if assignments_df is not None and "category_id" in assignments_df.columns:
    residual = int((assignments_df["category_id"].isna() | (assignments_df["category_id"] == "residual")).sum())
    m3.metric("Residual narratives", residual)
else:
    m3.metric("Residual narratives", "—")
m4.metric("Round", round_num)

tabs = st.tabs(
    ["Variants", "Profiles", "Narratives", "Sample", "Taxonomy", "Assignment", "Discovery", "Indicators",
     "Description", "Final"]
)

with tabs[0]:
    _show_df(variants_df)

with tabs[1]:
    _show_df(artifacts.read_csv(run_dir / PROFILING_DIRNAME / "profiles.csv"))

with tabs[2]:
    _show_df(artifacts.read_csv(run_dir / TEXTUALIZATION_DIRNAME / "narratives.csv"))

with tabs[3]:
    _show_df(artifacts.read_csv(run_dir / SAMPLING_DIRNAME / "narrative_sample.csv"))

with tabs[4]:
    if taxonomy is None:
        st.info("No taxonomy yet.")
    else:
        st.dataframe(
            [{"category_id": c.category_id, "name": c.name, "description": c.description} for c in taxonomy.categories],
            width="stretch",
        )

with tabs[5]:
    report = artifacts.read_text(rd / ASSIGNMENT_DIRNAME / "assignment_report.md")
    if report:
        st.markdown(report)
    if assignments_df is not None:
        with st.expander("assignments.csv"):
            _show_df(assignments_df)
    if not report and assignments_df is None:
        st.info("No data.")

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
                    f"Download {pnml.name}", pnml.read_bytes(), file_name=pnml.name, key=f"pnml_{img.stem}"
                )
    if not report and metrics is None:
        st.info("No data (round already accepted? models are deleted on acceptance — see the Final tab).")

with tabs[7]:
    report = artifacts.read_text(rd / INDICATORS_DIRNAME / "indicator_report.md")
    indicator_df = artifacts.read_csv(rd / INDICATORS_DIRNAME / "indicator_satisfaction.csv")
    goal_df = artifacts.read_csv(rd / INDICATORS_DIRNAME / "goal_satisfaction.csv")
    if report:
        st.markdown(report)
    if indicator_df is not None:
        with st.expander("indicator_satisfaction.csv"):
            _show_df(indicator_df)
    if goal_df is not None:
        with st.expander("goal_satisfaction.csv"):
            _show_df(goal_df)
    # The measured .jucm is the artifact this step exists to produce: one EvaluationStrategy per
    # category, so the analyst opens it in jUCMNav and compares the colored models side by side.
    for measured in sorted((rd / INDICATORS_DIRNAME).glob("*_measured.jucm")):
        st.download_button(
            f"Download {measured.name} (open in jUCMNav)",
            measured.read_bytes(),
            file_name=measured.name,
            key=f"jucm_{measured.stem}",
        )
    if not report and indicator_df is None:
        st.info(
            "Step 7b did not run for this round. It is optional (`skip_indicators`) and is a no-op "
            "on a goal model whose indicators carry no measurement binding — today, every model "
            "except RTFM's."
        )

with tabs[8]:
    report = artifacts.read_text(rd / DESCRIPTION_DIRNAME / "description_report.md")
    if report:
        st.markdown(report)
    else:
        st.info("No data.")

with tabs[9]:
    final_dir = run_dir / FINAL_DIRNAME
    readme = artifacts.read_text(final_dir / "README.md")
    if readme:
        st.markdown(readme)
        final_assignments = final_dir / "assignments.csv"
        if final_assignments.exists():
            st.download_button(
                "Download assignments.csv",
                final_assignments.read_bytes(),
                file_name="assignments.csv",
                key="final_assignments_csv",
            )
        for f in sorted((final_dir / SUBLOGS_DIRNAME).glob("*.xes.gz")):
            st.download_button(f"Download {f.name}", f.read_bytes(), file_name=f.name, key=f"xes_{f.name}")
    else:
        st.info("This run has not been accepted yet (no final/).")

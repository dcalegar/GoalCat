from __future__ import annotations

from pathlib import Path

import streamlit as st
import yaml

from goalcat.config import REVIEW_DIRNAME, TAXONOMY_DIRNAME
from goalcat.review import MergeDecision, RenameDecision, ReviewDecisions, SplitDecision
from gui import artifacts, run_control, ui_helpers

st.set_page_config(page_title="GoalCat — Revisión", page_icon="🐱", layout="wide")
st.title("Revisión (Step 9)")

ACTIVE_KEY = "gui_active_review"
POPEN_KEY = "_gui_review_popen"

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

active = st.session_state.get(ACTIVE_KEY)
if active is not None and active["run_id"] == run_id:
    st.divider()
    st.subheader(f"Procesando revisión: ronda {active['round']}")
    ui_helpers.render_progress_panel(
        status_path=Path(active["status_path"]),
        worker_log_path=Path(active["worker_log_path"]),
        pipeline_log_path=run_dir / "pipeline.log",
        popen=st.session_state[POPEN_KEY],
        steps=[9],
        success_message="Revisión procesada — volvé a seleccionar la corrida para ver el resultado.",
        session_state_key=ACTIVE_KEY,
        popen_state_key=POPEN_KEY,
    )
    st.stop()

rounds = artifacts.list_rounds(run_dir)
pending = [r for r in rounds if r["status"] == "pending_review"]
if not pending:
    st.info("No hay ninguna ronda esperando revisión para esta corrida.")
    st.stop()

round_num = pending[-1]["round"]
rd = artifacts.round_dir(run_dir, round_num)
st.caption(f"Revisando ronda {round_num}.")

index_text = artifacts.read_text(run_dir / "review_index.md")
if index_text:
    with st.expander("review_index.md", expanded=False):
        st.markdown(index_text)

taxonomy = artifacts.read_taxonomy(rd / TAXONOMY_DIRNAME / "taxonomy.json")
if taxonomy is None:
    st.error("Sin taxonomy.json en esta ronda todavía.")
    st.stop()

category_ids = [c.category_id for c in taxonomy.categories]

st.subheader("Categorías")
actions: dict[str, str] = {}
new_names: dict[str, str] = {}
new_descriptions: dict[str, str] = {}
reasons: dict[str, str] = {}

for c in taxonomy.categories:
    with st.expander(f"{c.category_id} — {c.name}", expanded=False):
        st.caption(c.description)
        action = st.radio(
            "Acción",
            ["Mantener", "Renombrar", "Fusionar", "Dividir"],
            key=f"action_{c.category_id}",
            horizontal=True,
        )
        actions[c.category_id] = action
        if action == "Renombrar":
            new_names[c.category_id] = st.text_input("Nuevo nombre", c.name, key=f"name_{c.category_id}")
            new_descriptions[c.category_id] = st.text_area(
                "Nueva descripción", c.description, key=f"desc_{c.category_id}"
            )
            reasons[c.category_id] = st.text_input("Motivo", key=f"reason_{c.category_id}")
        elif action == "Fusionar":
            others = [cid for cid in category_ids if cid != c.category_id]
            st.multiselect("Fusionar con", others, key=f"merge_{c.category_id}")
            reasons[c.category_id] = st.text_input("Motivo", key=f"reason_{c.category_id}")
        elif action == "Dividir":
            reasons[c.category_id] = st.text_input("Motivo de la división", key=f"reason_{c.category_id}")

st.divider()
notes = st.text_area("Notas generales (opcional)")

col_a, col_b = st.columns(2)
with col_a:
    accept_clicked = st.button(
        "Aceptar taxonomía tal cual",
        type="primary",
        disabled=any(a != "Mantener" for a in actions.values()),
        help="Sólo disponible si ninguna categoría tiene una acción pendiente.",
    )
with col_b:
    submit_clicked = st.button(
        "Enviar decisión (revisar)",
        disabled=all(a == "Mantener" for a in actions.values()),
    )


def _build_decisions(decision_kind: str) -> ReviewDecisions:
    renames, merges, splits = [], [], []
    for cid, action in actions.items():
        reason = reasons.get(cid) or "(sin motivo especificado desde la GUI)"
        if action == "Renombrar":
            renames.append(
                RenameDecision(
                    category_id=cid,
                    new_name=new_names.get(cid),
                    new_description=new_descriptions.get(cid),
                    reason=reason,
                )
            )
        elif action == "Fusionar":
            others = st.session_state.get(f"merge_{cid}", [])
            if others:
                merges.append(MergeDecision(category_ids=[cid, *others], reason=reason))
        elif action == "Dividir":
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
            f"No se encontró {config_path} — esta corrida no fue creada desde la GUI, así que no "
            "hay un config propio para re-invocar Step 9. Corré Step 9 desde un script para esta "
            "corrida (ver goalcat.pipeline.run_step9_review)."
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

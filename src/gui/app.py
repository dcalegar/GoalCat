"""GoalCat pipeline GUI — entry point.

Run with `streamlit run src/gui/app.py` (see project README's "Running the GUI" section). Pure
orchestration over the existing library (goalcat.pipeline / goalcat.config / goalcat.review) — no
pipeline logic lives here or in gui/pages/; see gui/worker.py, gui/run_control.py,
gui/config_form.py, gui/artifacts.py.
"""

from __future__ import annotations

import os

import streamlit as st

st.set_page_config(page_title="GoalCat", page_icon="🐱", layout="wide")

st.title("GoalCat pipeline")
st.markdown(
    """
Interfaz local para correr y revisar el pipeline GoalCat (Steps 1-9) sin editar YAML a mano.

Usá la barra lateral para:

- **Nueva corrida** — elegir un log + goal model, ajustar el config, y lanzar el pipeline con
  un medidor de avance en vivo.
- **Resultados** — explorar variantes, perfiles, narrativas, taxonomía, reportes y modelos de
  proceso de cualquier corrida ya ejecutada.
- **Revisión** — el Step 9 de negocio: aceptar, renombrar, fusionar o dividir categorías sin
  tocar `review_decisions.yaml` a mano.
- **Historial** — todas las corridas guardadas en `data/output/`.
"""
)

if not any(os.environ.get(k) for k in ("GEMINI_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY")):
    st.warning(
        "No se detectó GEMINI_API_KEY/OPENAI_API_KEY/ANTHROPIC_API_KEY en el entorno — los "
        "steps que llaman a un LLM (5, 6, 8, y Step 9 en caso de fusión/división) van a fallar "
        "hasta que exportes la key correspondiente en la shell antes de lanzar `streamlit run`."
    )

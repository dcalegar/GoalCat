from __future__ import annotations

import os

import streamlit as st

from gui.ui_helpers import API_KEY_ENV_VARS, mask_key

st.set_page_config(page_title="GoalCat — Setup", page_icon="🐱", layout="wide")
st.title("Setup")

st.markdown(
    "Steps 5 (taxonomy induction), 6 (narrative assignment), 8 (high-level description), and "
    "Step 9 merges/splits call an LLM through [litellm](https://github.com/BerriAI/litellm), which "
    "reads its API key straight from the environment. If your shell already exports one of the "
    "variables below, you're set — nothing to do here. Otherwise, paste a key below for this "
    "session."
)

st.info(
    "A key entered here is kept **only in this Streamlit server process's memory** — it is never "
    "written to a file, matching this project's convention (see `README.md`, \"LLM backend\"). It "
    "is lost when the server restarts; export it in your shell profile instead if you want it to "
    "persist across restarts."
)

st.divider()

for var in API_KEY_ENV_VARS:
    current = os.environ.get(var)
    col_status, col_form = st.columns([1, 2])
    with col_status:
        st.subheader(var)
        if current:
            st.success(f"Set — `{mask_key(current)}`")
        else:
            st.warning("Not set")
    with col_form:
        if current:
            if st.button(f"Clear {var} for this session", key=f"clear_{var}"):
                os.environ.pop(var, None)
                st.rerun()
        else:
            with st.form(key=f"set_{var}", clear_on_submit=True):
                value = st.text_input(f"Paste {var}", type="password", key=f"input_{var}")
                submitted = st.form_submit_button("Save for this session")
                if submitted:
                    if value.strip():
                        os.environ[var] = value.strip()
                        st.rerun()
                    else:
                        st.error("Enter a non-empty key first.")
    st.divider()

st.caption(
    "Prefer the default `gemini/gemini-3.5-flash-lite` backend (`GEMINI_API_KEY`) unless you have "
    "a specific reason to switch models — see `src/goalcat/config.yaml`. A local, no-API-key "
    "backend (Ollama) is also available — see README.md's \"LLM backend\" section, option B."
)

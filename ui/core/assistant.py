from __future__ import annotations

import streamlit as st

from pipeline import EntrepreneurshipAssistant


@st.cache_resource
def get_assistant() -> EntrepreneurshipAssistant:
    return EntrepreneurshipAssistant(base_dir=".")

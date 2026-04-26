from __future__ import annotations

import streamlit as st

from ui.core.i18n import init_language


def init_state() -> None:
    init_language()
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "pending_query" not in st.session_state:
        st.session_state.pending_query = None
    if "top_k" not in st.session_state:
        st.session_state.top_k = 5


def resolve_active_query(chat_query: str | None) -> str | None:
    if chat_query:
        return chat_query
    if st.session_state.pending_query:
        active_query = st.session_state.pending_query
        st.session_state.pending_query = None
        return active_query
    return None

from __future__ import annotations

import streamlit as st


def init_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "pending_query" not in st.session_state:
        st.session_state.pending_query = None


def resolve_active_query(chat_query: str | None) -> str | None:
    if chat_query:
        return chat_query
    if st.session_state.pending_query:
        active_query = st.session_state.pending_query
        st.session_state.pending_query = None
        return active_query
    return None

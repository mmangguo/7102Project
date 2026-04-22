from __future__ import annotations

import streamlit as st

from ui.components.chat_history import render_history
from ui.components.styles import inject_global_styles
from ui.core.assistant import get_assistant
from ui.core.session import init_state, resolve_active_query
from ui.flows.chat_turn import run_turn


def main() -> None:
    # Set page configuration
    st.set_page_config(
        page_title="Startup Assistant MVP", page_icon="💡", layout="wide"
    )

    # Main title
    st.title("Entrepreneurship Knowledge Base Chatbot")

    inject_global_styles()

    # Initialize session state and UI components
    init_state()
    render_history(st.session_state.messages)
    assistant = get_assistant()

    # Chat input with localized placeholder
    chat_query = st.chat_input(
        "Enter your startup question, e.g., How to validate a target market?"
    )
    active_query = resolve_active_query(chat_query)

    if active_query:
        run_turn(active_query, assistant)


if __name__ == "__main__":
    main()

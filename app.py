from __future__ import annotations

import streamlit as st

from ui.components.chat_history import render_history
from ui.components.styles import inject_global_styles
from ui.core.assistant import get_assistant
from ui.core.session import init_state, resolve_active_query
from ui.flows.chat_turn import run_turn


def main() -> None:
    st.set_page_config(page_title="创业助手 MVP", page_icon="💡", layout="wide")
    st.title("创业知识库聊天助手")
    inject_global_styles()

    init_state()
    render_history(st.session_state.messages)
    assistant = get_assistant()

    chat_query = st.chat_input("输入你的创业问题，例如：如何验证目标市场？")
    active_query = resolve_active_query(chat_query)

    if active_query:
        run_turn(active_query, assistant)


if __name__ == "__main__":
    main()

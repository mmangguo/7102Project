from __future__ import annotations

import streamlit as st

from . import icons


def render_next_question_buttons(
    next_questions: list[str], message_idx: int
) -> None:
    if not next_questions:
        return

    st.markdown(
        f'<div class="suggestions-label">{icons.CARET}<span>你可能接下来会问</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="suggestion-group">', unsafe_allow_html=True)
    for i, question in enumerate(next_questions, 1):
        if st.button(
            question,
            key=f"next_q_{message_idx}_{i}",
            use_container_width=True,
        ):
            st.session_state.pending_query = question
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

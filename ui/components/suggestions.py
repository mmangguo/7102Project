from __future__ import annotations

import streamlit as st


def render_next_question_buttons(next_questions: list[str], message_idx: int) -> None:
    if not next_questions:
        return

    st.markdown("**你可能接下来会问：**")
    for i, q in enumerate(next_questions, 1):
        if st.button(
            q,
            key=f"next_q_{message_idx}_{i}",
            use_container_width=True,
        ):
            st.session_state.pending_query = q

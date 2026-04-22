from __future__ import annotations

import streamlit as st

from .citations import render_answer_text, render_evidence_section
from .suggestions import render_next_question_buttons


def render_history(messages: list[dict]) -> None:
    for idx, msg in enumerate(messages):
        role = msg.get("role", "assistant")
        with st.chat_message(role):
            render_answer_text(msg.get("content", ""))
            evidence = msg.get("evidence")
            if role == "assistant" and evidence:
                render_evidence_section(evidence)

            if role == "assistant":
                render_next_question_buttons(msg.get("next_questions", []), idx)

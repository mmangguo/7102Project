from __future__ import annotations

import streamlit as st

from .citations import extract_cited_indices, render_answer_text, render_evidence_section
from .suggestions import render_next_question_buttons


_AVATARS = {"user": "👤", "assistant": "✨"}


def render_history(messages: list[dict]) -> None:
    for idx, msg in enumerate(messages):
        role = msg.get("role", "assistant")
        avatar = _AVATARS.get(role, None)
        with st.chat_message(role, avatar=avatar):
            content = msg.get("content", "")
            render_answer_text(content)

            evidence = msg.get("evidence")
            if role == "assistant" and evidence:
                cited = msg.get("cited_indices")
                if cited is not None:
                    cited_set = set(cited)
                else:
                    cited_set = extract_cited_indices(content)
                render_evidence_section(evidence, cited_indices=cited_set)

            if role == "assistant":
                render_next_question_buttons(msg.get("next_questions", []), idx)

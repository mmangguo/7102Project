from __future__ import annotations

import time

import streamlit as st

from pipeline import EntrepreneurshipAssistant
from ui.components.citations import (
    build_answer_cards_html,
    extract_cited_indices,
    render_evidence_section,
    stylize_inline_citations,
)
from ui.components.suggestions import render_next_question_buttons
from ui.core.i18n import t


def _typing_indicator_html() -> str:
    return (
        f'<div class="typing-indicator" role="status" aria-label="{t("turn.typing.aria")}">'
        '<span class="typing-indicator__dot"></span>'
        '<span class="typing-indicator__dot"></span>'
        '<span class="typing-indicator__dot"></span>'
        "</div>"
    )


def run_turn(
    query: str,
    assistant: EntrepreneurshipAssistant,
    lang: str = "zh",
) -> None:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user", avatar="👤"):
        st.markdown(query)

    with st.chat_message("assistant", avatar="✨"):
        started_at = time.perf_counter()
        thinking = st.status(t("turn.thinking"), expanded=False, state="running")

        top_k = int(st.session_state.get("top_k", 5))
        thinking.write(t("turn.retrieving", k=top_k))
        turn = assistant.prepare_turn(query, top_k=top_k, lang=lang)
        evidence_count = len(turn.get("evidence", []))
        thinking.write(t("turn.retrieve_done", n=evidence_count))

        thinking.update(label=t("turn.composing"), state="running")

        answer_placeholder = st.empty()
        typing_html = _typing_indicator_html()
        answer_placeholder.markdown(typing_html, unsafe_allow_html=True)

        chunks: list[str] = []
        for piece in assistant.stream_answer(turn):
            chunks.append(piece)
            partial = stylize_inline_citations("".join(chunks))
            answer_placeholder.markdown(
                partial + '<span class="stream-cursor" aria-hidden="true"></span>',
                unsafe_allow_html=True,
            )

        answer_text = "".join(chunks)
        answer_placeholder.markdown(
            build_answer_cards_html(answer_text),
            unsafe_allow_html=True,
        )

        cited = extract_cited_indices(answer_text)
        render_evidence_section(turn["evidence"], cited_indices=cited)

        thinking.update(label=t("turn.followups"), state="running")
        next_q_placeholder = st.empty()
        next_q_placeholder.markdown(typing_html, unsafe_allow_html=True)
        result = assistant.finalize_turn(turn, answer_text)
        next_q_placeholder.empty()

        elapsed = time.perf_counter() - started_at
        thinking.update(
            label=t("turn.complete", sec=elapsed),
            state="complete",
            expanded=False,
        )

        assistant_message_idx = len(st.session_state.messages)
        render_next_question_buttons(result["next_questions"], assistant_message_idx)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": result["answer"],
            "evidence": turn["evidence"],
            "cited_indices": list(cited),
            "next_questions": result["next_questions"],
        }
    )

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


_TYPING_INDICATOR_HTML = (
    '<div class="typing-indicator" role="status" aria-label="AI 正在生成回答">'
    '<span class="typing-indicator__dot"></span>'
    '<span class="typing-indicator__dot"></span>'
    '<span class="typing-indicator__dot"></span>'
    "</div>"
)


def run_turn(query: str, assistant: EntrepreneurshipAssistant) -> None:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user", avatar="👤"):
        st.markdown(query)

    with st.chat_message("assistant", avatar="✨"):
        started_at = time.perf_counter()
        thinking = st.status("正在理解你的问题…", expanded=False, state="running")

        top_k = int(st.session_state.get("top_k", 5))
        thinking.write(f"检索相关资料（top-k = {top_k}）")
        turn = assistant.prepare_turn(query, top_k=top_k)
        evidence_count = len(turn.get("evidence", []))
        thinking.write(f"检索完成：命中 {evidence_count} 条证据")

        thinking.update(label="组织结构化回答中…", state="running")

        answer_placeholder = st.empty()
        answer_placeholder.markdown(_TYPING_INDICATOR_HTML, unsafe_allow_html=True)

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

        thinking.update(label="生成高质量追问中…", state="running")
        next_q_placeholder = st.empty()
        next_q_placeholder.markdown(
            _TYPING_INDICATOR_HTML, unsafe_allow_html=True
        )
        result = assistant.finalize_turn(turn, answer_text)
        next_q_placeholder.empty()

        elapsed = time.perf_counter() - started_at
        thinking.update(
            label=f"完成 · 用时 {elapsed:.1f}s",
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

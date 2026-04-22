from __future__ import annotations

import streamlit as st

from pipeline import EntrepreneurshipAssistant
from ui.components.citations import render_evidence_section, stylize_inline_citations
from ui.components.suggestions import render_next_question_buttons


def run_turn(query: str, assistant: EntrepreneurshipAssistant) -> None:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        thinking_status = st.status("思考中...", expanded=False)
        thinking_status.write("正在理解你的问题")
        thinking_status.write("正在检索相关资料")
        with st.spinner("思考中..."):
            turn = assistant.prepare_turn(query)

        thinking_status.update(label="思考中...正在组织回答", state="running")
        answer_placeholder = st.empty()
        chunks: list[str] = []
        for piece in assistant.stream_answer(turn):
            chunks.append(piece)
            answer_placeholder.markdown(
                stylize_inline_citations("".join(chunks)),
                unsafe_allow_html=True,
            )

        answer_text = "".join(chunks)
        thinking_status.update(label="回答已生成", state="complete")
        assistant_message_idx = len(st.session_state.messages)
        render_evidence_section(turn["evidence"])

        next_q_loading = st.empty()
        next_q_loading.caption("正在生成你可能的下一问...")
        result = assistant.finalize_turn(turn, answer_text)
        next_q_loading.empty()
        render_next_question_buttons(result["next_questions"], assistant_message_idx)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": result["answer"],
            "evidence": turn["evidence"],
            "next_questions": result["next_questions"],
        }
    )

from __future__ import annotations

import streamlit as st

from pipeline import EntrepreneurshipAssistant
from ui.components.citations import render_evidence_section, stylize_inline_citations
from ui.components.suggestions import render_next_question_buttons


def run_turn(query: str, assistant: EntrepreneurshipAssistant) -> None:
    # Append and display user message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        # Status container for the RAG pipeline steps
        thinking_status = st.status("Thinking...", expanded=False)
        thinking_status.write("Analyzing your question...")
        thinking_status.write("Retrieving relevant resources...")

        with st.spinner("Processing..."):
            turn = assistant.prepare_turn(query)

        # Transition to generation phase
        thinking_status.update(label="Thinking... drafting response", state="running")
        answer_placeholder = st.empty()
        chunks: list[str] = []

        # Stream the response to the UI
        for piece in assistant.stream_answer(turn):
            chunks.append(piece)
            answer_placeholder.markdown(
                stylize_inline_citations("".join(chunks)),
                unsafe_allow_html=True,
            )

        answer_text = "".join(chunks)
        thinking_status.update(label="Response generated", state="complete")
        assistant_message_idx = len(st.session_state.messages)

        # Display the source/evidence section
        render_evidence_section(turn["evidence"])

        # Predict next questions
        next_q_loading = st.empty()
        next_q_loading.caption("Generating suggested follow-up questions...")
        result = assistant.finalize_turn(turn, answer_text)
        next_q_loading.empty()

        # Render the clickable suggestion buttons
        render_next_question_buttons(result["next_questions"], assistant_message_idx)

    # Persist the assistant's response in session state
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": result["answer"],
            "evidence": turn["evidence"],
            "next_questions": result["next_questions"],
        }
    )

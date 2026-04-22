from __future__ import annotations

import re

import streamlit as st


def stylize_inline_citations(text: str) -> str:
    """
    Finds patterns like (Based on evidence 1, 2) and converts them into
    styled HTML badges for the UI.
    """
    # Updated pattern to match English "Based on evidence"
    pattern = re.compile(
        r"[（\(]\s*Based on evidence\s*([0-9\s,]+)\s*[）\)]", re.IGNORECASE
    )

    def repl(match: re.Match[str]) -> str:
        # Standardize separators to commas
        refs = re.sub(r"\s+", "", match.group(1)).replace("，", ",").replace("、", ",")
        return (
            f'<span class="cite-badge" title="Source evidence {refs}">[{refs}]</span>'
        )

    return pattern.sub(repl, text)


def render_answer_text(text: str) -> None:
    st.markdown(stylize_inline_citations(text), unsafe_allow_html=True)


def render_evidence_section(evidence: list[dict]) -> None:
    if not evidence:
        return

    st.caption(
        "This response was generated based on relevant information retrieved via RAG."
    )

    with st.expander("View Sources", expanded=False):
        for i, ev in enumerate(evidence, 1):
            st.markdown(f"**Source {i}**")
            # Assumes 'title' and 'url' keys exist in the evidence dictionary
            st.markdown(f"[{ev['title']}]({ev['url']})")
            st.write(ev["snippet"])

from __future__ import annotations

import re

import streamlit as st


def stylize_inline_citations(text: str) -> str:
    pattern = re.compile(r"[（\(]\s*基于证据\s*([0-9\s,，、]+)\s*[）\)]")

    def repl(match: re.Match[str]) -> str:
        refs = re.sub(r"\s+", "", match.group(1)).replace("，", ",").replace("、", ",")
        return f'<span class="cite-badge" title="引用证据 {refs}">[{refs}]</span>'

    return pattern.sub(repl, text)


def render_answer_text(text: str) -> None:
    st.markdown(stylize_inline_citations(text), unsafe_allow_html=True)


def render_evidence_section(evidence: list[dict]) -> None:
    if not evidence:
        return
    st.caption("本回答基于 RAG 检索到的相关内容生成。")
    with st.expander("查看引用内容", expanded=False):
        for i, ev in enumerate(evidence, 1):
            st.markdown(f"**引用 {i}**")
            st.markdown(f"[{ev['title']}]({ev['url']})")
            st.write(ev["snippet"])

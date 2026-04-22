from __future__ import annotations

import html
import re

import streamlit as st

from . import icons

_CITE_PATTERN = re.compile(r"[（\(]\s*基于证据\s*([0-9\s,，、]+)\s*[）\)]")
_EVIDENCE_REF_PATTERN = re.compile(r"证据\s*(\d+)")


def stylize_inline_citations(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        refs = re.sub(r"\s+", "", match.group(1)).replace("，", ",").replace("、", ",")
        return (
            f'<span class="cite-badge" aria-label="引用证据 {refs}" '
            f'title="引用证据 {refs}">{refs}</span>'
        )

    return _CITE_PATTERN.sub(repl, text)


def extract_cited_indices(answer_text: str) -> set[int]:
    return {int(m) for m in _EVIDENCE_REF_PATTERN.findall(answer_text)}


def render_answer_text(text: str, streaming: bool = False) -> None:
    rendered = stylize_inline_citations(text)
    if streaming:
        rendered += '<span class="stream-cursor" aria-hidden="true"></span>'
    st.markdown(rendered, unsafe_allow_html=True)


def render_evidence_section(
    evidence: list[dict],
    cited_indices: set[int] | None = None,
) -> None:
    if not evidence:
        return

    if cited_indices:
        shown = [
            (i, ev) for i, ev in enumerate(evidence, 1) if i in cited_indices
        ]
    else:
        shown = list(enumerate(evidence, 1))

    if not shown:
        return

    count = len(shown)
    st.caption(f"本回答引用了 {count} 条检索证据")
    with st.expander("查看引用内容", expanded=False):
        for i, ev in shown:
            title = html.escape(str(ev.get("title", "")) or "(无标题)")
            url = html.escape(str(ev.get("url", "")) or "#")
            score = float(ev.get("score", 0.0))
            snippet = html.escape(str(ev.get("snippet", "")))
            score_label = f"{score:.3f}"
            st.markdown(
                f"""
<div class="evidence-card">
  <div class="evidence-card__header">
    <a class="evidence-card__title" href="{url}" target="_blank" rel="noopener noreferrer">
      <span class="evidence-card__index" aria-hidden="true">{i}</span>
      <span>{title}</span>
      {icons.EXTERNAL_LINK}
    </a>
    <span class="evidence-card__score" title="TF-IDF 相关性分数"
          aria-label="相关性分数 {score_label}">{score_label}</span>
  </div>
  <p class="evidence-card__snippet">{snippet}</p>
</div>
""",
                unsafe_allow_html=True,
            )

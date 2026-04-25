from __future__ import annotations

import html
import re

import streamlit as st

from ui.core.i18n import t

from . import icons

# Inline citation patterns recognise both Chinese and English styles, e.g.
#   （基于证据 1,2）  /  (基于证据1)
#   (based on evidence 1,2)  /  (Based on Evidence 1)
_CITE_PATTERN = re.compile(
    r"[（\(]\s*(?:基于证据|based\s+on\s+evidence|based\s+on\s+evidences?)\s*"
    r"(\d+(?:\s*[,，、]\s*\d+)*)[^）\)]*?[）\)]",
    re.IGNORECASE,
)
# Loose pattern used when extracting which evidence indices were cited.
_EVIDENCE_REF_PATTERN = re.compile(
    r"(?:证据|evidences?)\s*(\d+(?:\s*[,，、and\s]*\d+)*)",
    re.IGNORECASE,
)
# Section keywords accepted as numbered headings for the answer-card layout.
_SECTION_KW = (
    r"相关性评估|核心洞察|落地步骤|知识缺口|一句话总结"
    r"|relevance\s+assessment|core\s+insight|action(?:able)?\s+steps?"
    r"|knowledge\s+gaps?|one[-\s]?(?:line|sentence)\s+summary|summary"
)
_HEADING_SPLIT = re.compile(
    rf"(?im)^(?:#{{2,3}}\s+)?(?:\*\*)?(\d+[.、]\s*(?:{_SECTION_KW}).*?)(?:\*\*)?$"
)
_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")

# (icon, css-section-key) keyed by a substring that must appear in the heading.
# Order matters: more specific keys (e.g. "One-line") come before generic ones.
_SECTION_META: list[tuple[str, tuple[str, str]]] = [
    ("相关性", ("🎯", "assess")),
    ("Relevance", ("🎯", "assess")),
    ("核心洞察", ("💡", "insight")),
    ("Core Insight", ("💡", "insight")),
    ("落地", ("🚀", "action")),
    ("Action", ("🚀", "action")),
    ("知识缺口", ("🔍", "gap")),
    ("Knowledge Gap", ("🔍", "gap")),
    ("一句话", ("⭐", "summary")),
    ("One-line", ("⭐", "summary")),
    ("One line", ("⭐", "summary")),
    ("One-sentence", ("⭐", "summary")),
    ("Summary", ("⭐", "summary")),
]


def stylize_inline_citations(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        raw = re.sub(r"\s+", "", match.group(1))
        refs = raw.replace("\uff0c", ",").replace("\u3001", ",")
        aria = t("evidence.cite.aria", refs=refs)
        return (
            f'<span class="cite-badge" aria-label="{aria}" '
            f'title="{aria}">{refs}</span>'
        )

    return _CITE_PATTERN.sub(repl, text)


def extract_cited_indices(answer_text: str) -> set[int]:
    indices: set[int] = set()
    for group in _EVIDENCE_REF_PATTERN.findall(answer_text):
        for num in re.findall(r"\d+", group):
            indices.add(int(num))
    return indices


# ------------------------------------------------------------------
# Markdown -> HTML (subset used in answer cards)
# ------------------------------------------------------------------

def _md_to_html(text: str) -> str:
    """Convert bold, ordered/unordered lists, and paragraphs to HTML."""
    text = _BOLD_RE.sub(r"<strong>\1</strong>", text)

    lines = text.strip().split("\n")
    parts: list[str] = []
    cur_list: str | None = None
    para: list[str] = []

    def _flush_para():
        if para:
            parts.append("<p>" + "<br>".join(para) + "</p>")
            para.clear()

    def _flush_list():
        nonlocal cur_list
        if cur_list:
            parts.append(f"</{cur_list}>")
            cur_list = None

    for line in lines:
        s = line.strip()
        if not s:
            _flush_para()
            _flush_list()
            continue

        ol = re.match(r"^(\d+)[.\u3001]\s+(.+)", s)
        if ol:
            _flush_para()
            if cur_list != "ol":
                _flush_list()
                parts.append("<ol>")
                cur_list = "ol"
            parts.append(f"<li>{ol.group(2)}</li>")
            continue

        ul = re.match(r"^[-\u2022\u25cf]\s+(.+)", s)
        if ul:
            _flush_para()
            if cur_list != "ul":
                _flush_list()
                parts.append("<ul>")
                cur_list = "ul"
            parts.append(f"<li>{ul.group(1)}</li>")
            continue

        _flush_list()
        para.append(s)

    _flush_para()
    _flush_list()
    return "\n".join(parts)


# ------------------------------------------------------------------
# Card-layout rendering for structured answers
# ------------------------------------------------------------------

def build_answer_cards_html(text: str) -> str:
    """Split a structured LLM answer into card HTML sections."""
    styled = stylize_inline_citations(text)
    parts = _HEADING_SPLIT.split(styled)

    if len(parts) <= 1:
        return _md_to_html(styled)

    cards: list[str] = []

    pre = parts[0].strip()
    if pre:
        cards.append(f'<div class="answer-intro">{_md_to_html(pre)}</div>')

    for i in range(1, len(parts), 2):
        heading = parts[i].strip()
        content = parts[i + 1].strip() if i + 1 < len(parts) else ""

        icon = "\U0001f4cc"
        section_type = "insight"
        for kw, (ic, sec) in _SECTION_META:
            if kw.lower() in heading.lower():
                icon = ic
                section_type = sec
                break

        heading_html = _BOLD_RE.sub(r"<strong>\1</strong>", heading)
        body_html = _md_to_html(content) if content else ""

        cards.append(
            f'<div class="answer-card" data-section="{section_type}">'
            f'<div class="answer-card__header">'
            f'<span class="answer-card__icon">{icon}</span>'
            f'<span class="answer-card__heading">{heading_html}</span>'
            f"</div>"
            f'<div class="answer-card__body">{body_html}</div>'
            f"</div>"
        )

    return "\n".join(cards)


# ------------------------------------------------------------------
# Public rendering helpers
# ------------------------------------------------------------------

def render_answer_text(text: str, streaming: bool = False) -> None:
    if streaming:
        rendered = stylize_inline_citations(text)
        rendered += '<span class="stream-cursor" aria-hidden="true"></span>'
        st.markdown(rendered, unsafe_allow_html=True)
    else:
        st.markdown(build_answer_cards_html(text), unsafe_allow_html=True)


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
    st.caption(t("evidence.caption", n=count))
    with st.expander(t("evidence.expand"), expanded=False):
        for i, ev in shown:
            title = html.escape(str(ev.get("title", "")) or t("evidence.untitled"))
            url = html.escape(str(ev.get("url", "")) or "#")
            score = float(ev.get("score", 0.0))
            snippet = html.escape(str(ev.get("snippet", "")))

            if score > 0.001:
                pct = f"{score:.1%}"
                score_html = (
                    f'<span class="evidence-card__score" '
                    f'title="{t("evidence.score.title", pct=pct)}">'
                    f'{pct}</span>'
                )
            else:
                score_html = (
                    f'<span class="evidence-card__score" '
                    f'title="{t("evidence.rank.title", i=i)}">'
                    f'TOP {i}</span>'
                )

            st.markdown(
                f"""
<div class="evidence-card">
  <div class="evidence-card__header">
    <a class="evidence-card__title" href="{url}" target="_blank" rel="noopener noreferrer">
      <span class="evidence-card__index" aria-hidden="true">{i}</span>
      <span>{title}</span>
      {icons.EXTERNAL_LINK}
    </a>
    {score_html}
  </div>
  <p class="evidence-card__snippet">{snippet}</p>
</div>
""",
                unsafe_allow_html=True,
            )

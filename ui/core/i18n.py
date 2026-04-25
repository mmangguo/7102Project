"""Internationalization helpers for the Streamlit UI.

This module owns:
- the supported languages and the default language
- the in-session language state (st.session_state.language)
- the translation dictionary for every user-facing string
- the bilingual starter-prompt catalog used by the welcome screen

UI components should call ``t("some.key")`` (or ``t("...", **kwargs)``)
instead of hard-coding strings, so that the language toggle in the top
right corner can switch the entire interface without touching component
internals.
"""

from __future__ import annotations

import streamlit as st

DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES: tuple[str, ...] = ("en", "zh")

LANGUAGE_LABELS: dict[str, str] = {
    "zh": "中文",
    "en": "EN",
}

# ---------------------------------------------------------------------------
# Translation table
# ---------------------------------------------------------------------------

TRANSLATIONS: dict[str, dict[str, str]] = {
    # -- Page chrome -------------------------------------------------------
    "page.title": {
        "zh": "创业助手 MVP",
        "en": "Founder Assistant MVP",
    },
    # -- Hero header -------------------------------------------------------
    "header.title": {
        "zh": "创业助手",
        "en": "Founder Assistant",
    },
    "header.subtitle": {
        "zh": "检索知识库 · 结构化洞察 · 智能追问",
        "en": "Knowledge Retrieval · Structured Insight · Smart Follow-ups",
    },
    "header.chip.live.text": {
        "zh": "在线问答 · {chip}",
        "en": "Live · {chip}",
    },
    "header.chip.live.aria": {
        "zh": "大模型已连接 {chip}",
        "en": "LLM connected: {chip}",
    },
    "header.chip.live.title": {
        "zh": "已连接：{chip}",
        "en": "Connected: {chip}",
    },
    "header.chip.fallback.text": {
        "zh": "离线模式 · 未配置 API Key",
        "en": "Offline · No API key configured",
    },
    "header.chip.fallback.aria": {
        "zh": "未检测到可用 API Key，当前使用本地规则摘要回退",
        "en": "No API key detected; using local rule-based summary fallback",
    },
    "header.chip.fallback.title": {
        "zh": (
            "未检测到 API Key，当前使用本地规则摘要。"
            "请在项目根目录的 .env 里配置 BAILIAN_API_KEY 或 OPENAI_API_KEY 后刷新页面。"
        ),
        "en": (
            "No API key detected; using local rule-based summary. "
            "Configure BAILIAN_API_KEY or OPENAI_API_KEY in .env at the project root and refresh."
        ),
    },
    # -- Language switcher -------------------------------------------------
    "lang.aria": {
        "zh": "切换界面语言",
        "en": "Switch interface language",
    },
    # -- Sidebar -----------------------------------------------------------
    "sidebar.about": {
        "zh": "关于",
        "en": "About",
    },
    "sidebar.about.body": {
        "zh": "面向早期创业者的 RAG 问答 MVP：检索 · 主题分类 · 流式回答 · 下一问预测。",
        "en": (
            "An RAG Q&A MVP for early-stage founders: retrieval, topic classification, "
            "streaming answers and next-question prediction."
        ),
    },
    "sidebar.model_status": {
        "zh": "模型状态",
        "en": "Model status",
    },
    "sidebar.online.chip": {
        "zh": "在线 · {provider}",
        "en": "Online · {provider}",
    },
    "sidebar.online.caption": {
        "zh": "LLM 已连接，将流式生成结构化回答。",
        "en": "LLM connected; structured answers will stream live.",
    },
    "sidebar.offline.chip": {
        "zh": "离线 · 未配置 API Key",
        "en": "Offline · No API key configured",
    },
    "sidebar.offline.caption": {
        "zh": "未检测到可用 API Key，现在只能把检索到的证据片段拼成简短回答，不会调用大模型。",
        "en": (
            "No API key detected. Only short summaries assembled from the retrieved "
            "evidence will be returned; the LLM will not be called."
        ),
    },
    "sidebar.offline.expander": {
        "zh": "如何开启 LLM 在线问答？",
        "en": "How do I enable LLM online Q&A?",
    },
    "sidebar.offline.expander.body": {
        "zh": "在项目根目录创建 `.env`，任选一项配置后刷新页面：",
        "en": "Create `.env` at the project root and add one of the snippets below, then refresh the page:",
    },
    "sidebar.offline.expander.cn_comment": {
        "zh": "# 百炼（推荐，国内可用）",
        "en": "# DashScope / Bailian (recommended in mainland China)",
    },
    "sidebar.offline.expander.openai_comment": {
        "zh": "# 或 OpenAI",
        "en": "# or OpenAI",
    },
    "sidebar.retrieval": {
        "zh": "检索设置",
        "en": "Retrieval settings",
    },
    "sidebar.topk.label": {
        "zh": "证据条数 (top-k)",
        "en": "Evidence count (top-k)",
    },
    "sidebar.topk.help": {
        "zh": "每次检索返回的证据数量。越多越全面，但也可能引入噪声。",
        "en": "How many evidence chunks each retrieval returns. Higher means more coverage but more noise.",
    },
    "sidebar.session": {
        "zh": "会话",
        "en": "Session",
    },
    "sidebar.session.caption": {
        "zh": "已完成 {turn} 轮问答（{user} 条提问 / {assistant} 条回答）",
        "en": "Completed {turn} turns ({user} questions / {assistant} answers)",
    },
    "sidebar.clear": {
        "zh": "清空对话",
        "en": "Clear chat",
    },
    "sidebar.tips": {
        "zh": "使用提示",
        "en": "Tips",
    },
    "sidebar.tips.body": {
        "zh": (
            "问题越聚焦，检索越准<br>"
            "回答末尾的 <span class='cite-badge'>1</span> 为证据引用<br>"
            "展开“查看引用内容”可看原文片段<br>"
            "点击下一问按钮可自动追问"
        ),
        "en": (
            "The more specific your question, the better the retrieval<br>"
            "Numbers like <span class='cite-badge'>1</span> at the end of answers are evidence citations<br>"
            "Expand “View citations” to see the source snippets<br>"
            "Click a follow-up button to ask the next question automatically"
        ),
    },
    # -- Welcome screen ----------------------------------------------------
    "welcome.eyebrow": {
        "zh": "AI Entrepreneurship Advisor",
        "en": "AI Entrepreneurship Advisor",
    },
    "welcome.headline": {
        "zh": "你好，有什么创业问题想聊聊？",
        "en": "Hi — what entrepreneurship question is on your mind?",
    },
    "welcome.desc": {
        "zh": (
            "我是你的 AI 创业顾问，能帮你从知识库里找到相关的商业洞察，给出"
            "<strong>结构化建议</strong>和<strong>可执行的下一步</strong>。"
            "像跟朋友聊天一样，直接说就好。"
        ),
        "en": (
            "I'm your AI startup advisor. I'll surface relevant business insights from the "
            "knowledge base and give you <strong>structured advice</strong> and "
            "<strong>actionable next steps</strong>. Just chat with me like you would with a friend."
        ),
    },
    "welcome.section_label": {
        "zh": "试试这些问题",
        "en": "Try these questions",
    },
    "welcome.caption": {
        "zh": "直接在下方输入框里开始提问，支持中英文。",
        "en": "Type a question in the box below — both English and Chinese are supported.",
    },
    # -- Chat input --------------------------------------------------------
    "chat.input_placeholder": {
        "zh": "输入你的创业问题，例如：如何验证目标市场？",
        "en": "Type a question, e.g., how do I validate my target market?",
    },
    # -- Single-turn flow status updates -----------------------------------
    "turn.thinking": {
        "zh": "正在理解你的问题…",
        "en": "Understanding your question…",
    },
    "turn.retrieving": {
        "zh": "检索相关资料（top-k = {k}）",
        "en": "Retrieving evidence (top-k = {k})",
    },
    "turn.retrieve_done": {
        "zh": "检索完成：命中 {n} 条证据",
        "en": "Retrieval complete: {n} evidence chunks hit",
    },
    "turn.composing": {
        "zh": "组织结构化回答中…",
        "en": "Composing structured answer…",
    },
    "turn.followups": {
        "zh": "生成高质量追问中…",
        "en": "Generating high-quality follow-ups…",
    },
    "turn.complete": {
        "zh": "完成 · 用时 {sec:.1f}s",
        "en": "Done · {sec:.1f}s",
    },
    "turn.typing.aria": {
        "zh": "AI 正在生成回答",
        "en": "AI is generating an answer",
    },
    # -- Suggestions -------------------------------------------------------
    "suggestions.label": {
        "zh": "你可能接下来会问",
        "en": "You might ask next",
    },
    # -- Evidence section --------------------------------------------------
    "evidence.caption": {
        "zh": "本回答引用了 {n} 条检索证据",
        "en": "This answer cites {n} retrieved evidence chunks",
    },
    "evidence.expand": {
        "zh": "查看引用内容",
        "en": "View citations",
    },
    "evidence.untitled": {
        "zh": "(无标题)",
        "en": "(untitled)",
    },
    "evidence.score.title": {
        "zh": "相关度 {pct}",
        "en": "Relevance {pct}",
    },
    "evidence.rank.title": {
        "zh": "检索排名第 {i} 位",
        "en": "Retrieval rank #{i}",
    },
    "evidence.cite.aria": {
        "zh": "引用证据 {refs}",
        "en": "Cites evidence {refs}",
    },
}


# ---------------------------------------------------------------------------
# Bilingual starter prompts for the welcome grid
# ---------------------------------------------------------------------------

STARTER_PROMPT_KEYS: tuple[str, ...] = (
    "starter.market",
    "starter.marketing",
    "starter.pmf",
    "starter.finance",
)

_STARTER_PROMPTS: dict[str, dict[str, str]] = {
    "starter.market": {
        "zh": "开一家小型咖啡馆前，我该如何验证本地市场需求？",
        "en": "Before opening a small coffee shop, how do I validate local market demand?",
    },
    "starter.marketing": {
        "zh": "预算有限，我应该优先把钱投到哪几条营销渠道？",
        "en": "On a tight budget, which marketing channels should I prioritize?",
    },
    "starter.pmf": {
        "zh": "如何判断我的产品是否已经达到了 PMF？",
        "en": "How do I tell whether my product has reached PMF?",
    },
    "starter.finance": {
        "zh": "小微企业第一年最常见的财务与税务坑有哪些？",
        "en": "What are the most common finance & tax pitfalls for SMBs in year one?",
    },
}


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------

def init_language() -> None:
    """Ensure ``st.session_state.language`` is set to a supported value."""
    current = st.session_state.get("language")
    if current not in SUPPORTED_LANGUAGES:
        st.session_state.language = DEFAULT_LANGUAGE


def get_lang() -> str:
    """Return the active language, falling back to the default."""
    init_language()
    lang = st.session_state.get("language", DEFAULT_LANGUAGE)
    return lang if lang in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE


def set_lang(lang: str) -> bool:
    """Persist a new language choice. Returns True if it actually changed."""
    if lang not in SUPPORTED_LANGUAGES:
        return False
    if st.session_state.get("language") == lang:
        return False
    st.session_state.language = lang
    return True


def t(key: str, **kwargs: object) -> str:
    """Translate ``key`` into the active language with optional ``str.format`` kwargs."""
    entry = TRANSLATIONS.get(key)
    if not entry:
        return key
    lang = get_lang()
    text = entry.get(lang) or entry.get(DEFAULT_LANGUAGE) or key
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError, ValueError):
            return text
    return text


def starter_prompt(key: str) -> str:
    """Return the localized starter prompt text for the welcome grid."""
    entry = _STARTER_PROMPTS.get(key)
    if not entry:
        return key
    lang = get_lang()
    return entry.get(lang) or entry.get(DEFAULT_LANGUAGE) or key

from __future__ import annotations

import html

import streamlit as st

from pipeline import EntrepreneurshipAssistant

from . import icons


def render_header(assistant: EntrepreneurshipAssistant) -> None:
    provider = getattr(assistant.llm, "provider_name", None) or ""
    model = getattr(assistant.llm, "model_name", None) or ""
    available = bool(getattr(assistant.llm, "available", False))

    if available:
        provider_label = provider.capitalize() if provider else "LLM"
        model_label = html.escape(model) if model else ""
        chip_text = f"{provider_label} · {model_label}" if model_label else provider_label
        chip_html = (
            f'<span class="app-hero__chip app-hero__chip--live" role="status" '
            f'aria-label="大模型已连接 {chip_text}" title="已连接：{chip_text}">'
            f'<span class="dot" aria-hidden="true"></span>在线问答 · {chip_text}</span>'
        )
    else:
        chip_html = (
            '<span class="app-hero__chip app-hero__chip--fallback" role="status" '
            'aria-label="未检测到可用 API Key，当前使用本地规则摘要回退" '
            'title="未检测到 API Key，当前使用本地规则摘要。请在项目根目录的 .env 里配置 BAILIAN_API_KEY 或 OPENAI_API_KEY 后刷新页面。">'
            '<span class="dot" aria-hidden="true"></span>离线模式 · 未配置 API Key</span>'
        )

    st.markdown(
        f"""
<div class="app-hero">
  <div class="app-hero__logo" aria-hidden="true">{icons.SPARKLE}</div>
  <div class="app-hero__title-wrap">
    <h1 class="app-hero__title">创业助手</h1>
    <p class="app-hero__subtitle">检索知识库 · 结构化洞察 · 智能追问</p>
  </div>
  {chip_html}
</div>
""",
        unsafe_allow_html=True,
    )

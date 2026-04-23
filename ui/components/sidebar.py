from __future__ import annotations

import html

import streamlit as st

from pipeline import EntrepreneurshipAssistant


def render_sidebar(assistant: EntrepreneurshipAssistant) -> None:
    with st.sidebar:
        st.markdown(
            '<div class="sidebar-section">关于</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="sidebar-meta">面向早期创业者的 RAG 问答 MVP：'
            "检索 · 主题分类 · 流式回答 · 下一问预测。</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="sidebar-section" style="margin-top:20px;">模型状态</div>',
            unsafe_allow_html=True,
        )
        provider = getattr(assistant.llm, "provider_name", None)
        model = getattr(assistant.llm, "model_name", None)
        available = bool(getattr(assistant.llm, "available", False))

        if available:
            provider_label = (provider or "llm").capitalize()
            model_label = html.escape(model or "—")
            st.markdown(
                f'<span class="sidebar-chip sidebar-chip--live">在线 · {provider_label}</span>'
                '<span class="sidebar-chip" style="margin-left:6px;">'
                f'{model_label}</span>',
                unsafe_allow_html=True,
            )
            st.caption("LLM 已连接，将流式生成结构化回答。")
        else:
            st.markdown(
                '<span class="sidebar-chip sidebar-chip--fallback">'
                "离线 · 未配置 API Key</span>",
                unsafe_allow_html=True,
            )
            st.caption(
                "未检测到可用 API Key，现在只能把检索到的证据片段"
                "拼成简短回答，不会调用大模型。"
            )
            with st.expander("如何开启 LLM 在线问答？", expanded=False):
                st.markdown(
                    "在项目根目录创建 `.env`，任选一项配置后刷新页面：\n\n"
                    "```env\n"
                    "# 百炼（推荐，国内可用）\n"
                    "BAILIAN_API_KEY=sk-xxxxxxxxxxxx\n"
                    "LLM_MODEL=qwen-plus\n\n"
                    "# 或 OpenAI\n"
                    "# OPENAI_API_KEY=sk-xxxxxxxxxxxx\n"
                    "# LLM_MODEL=gpt-4o-mini\n"
                    "```"
                )

        st.markdown(
            '<div class="sidebar-section" style="margin-top:20px;">检索设置</div>',
            unsafe_allow_html=True,
        )
        st.slider(
            "证据条数 (top-k)",
            min_value=3,
            max_value=8,
            value=st.session_state.get("top_k", 5),
            step=1,
            key="top_k",
            help="每次检索返回的证据数量。越多越全面，但也可能引入噪声。",
        )

        st.markdown(
            '<div class="sidebar-section" style="margin-top:20px;">会话</div>',
            unsafe_allow_html=True,
        )
        turn_count = sum(
            1 for m in st.session_state.get("messages", []) if m.get("role") == "assistant"
        )
        st.caption(f"已进行 {turn_count} 轮对话")

        if st.button(
            "清空对话",
            use_container_width=True,
            key="btn_clear_chat",
            disabled=not st.session_state.get("messages"),
        ):
            st.session_state.messages = []
            st.session_state.pending_query = None
            st.rerun()

        st.markdown(
            '<div class="sidebar-section" style="margin-top:20px;">使用提示</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="sidebar-meta">'
            "问题越聚焦，检索越准<br>"
            "回答末尾的 <span class='cite-badge'>1</span> 为证据引用<br>"
            "展开“查看引用内容”可看原文片段<br>"
            "点击下一问按钮可自动追问"
            "</div>",
            unsafe_allow_html=True,
        )

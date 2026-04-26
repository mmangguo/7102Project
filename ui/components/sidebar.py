from __future__ import annotations

import html

import streamlit as st

from pipeline import EntrepreneurshipAssistant
from ui.core.i18n import t


def render_sidebar(assistant: EntrepreneurshipAssistant) -> None:
    with st.sidebar:
        st.markdown(
            f'<div class="sidebar-section">{t("sidebar.about")}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="sidebar-meta">{t("sidebar.about.body")}</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div class="sidebar-section" style="margin-top:20px;">{t("sidebar.model_status")}</div>',
            unsafe_allow_html=True,
        )
        provider = getattr(assistant.llm, "provider_name", None)
        model = getattr(assistant.llm, "model_name", None)
        available = bool(getattr(assistant.llm, "available", False))

        if available:
            provider_label = (provider or "llm").capitalize()
            model_label = html.escape(model or "—")
            st.markdown(
                f'<span class="sidebar-chip sidebar-chip--live">'
                f'{t("sidebar.online.chip", provider=provider_label)}</span>'
                '<span class="sidebar-chip" style="margin-left:6px;">'
                f'{model_label}</span>',
                unsafe_allow_html=True,
            )
            st.caption(t("sidebar.online.caption"))
        else:
            st.markdown(
                f'<span class="sidebar-chip sidebar-chip--fallback">'
                f'{t("sidebar.offline.chip")}</span>',
                unsafe_allow_html=True,
            )
            st.caption(t("sidebar.offline.caption"))
            with st.expander(t("sidebar.offline.expander"), expanded=False):
                st.markdown(
                    t("sidebar.offline.expander.body")
                    + "\n\n```env\n"
                    + t("sidebar.offline.expander.cn_comment") + "\n"
                    + "BAILIAN_API_KEY=sk-xxxxxxxxxxxx\n"
                    + "LLM_MODEL=qwen-plus\n\n"
                    + t("sidebar.offline.expander.openai_comment") + "\n"
                    + "# OPENAI_API_KEY=sk-xxxxxxxxxxxx\n"
                    + "# LLM_MODEL=gpt-4o-mini\n"
                    + "```"
                )

        st.markdown(
            f'<div class="sidebar-section" style="margin-top:20px;">{t("sidebar.retrieval")}</div>',
            unsafe_allow_html=True,
        )
        st.slider(
            t("sidebar.topk.label"),
            min_value=3,
            max_value=8,
            value=st.session_state.get("top_k", 5),
            step=1,
            key="top_k",
            help=t("sidebar.topk.help"),
        )

        st.markdown(
            f'<div class="sidebar-section" style="margin-top:20px;">{t("sidebar.session")}</div>',
            unsafe_allow_html=True,
        )
        msgs = st.session_state.get("messages", [])
        user_count = sum(1 for m in msgs if m.get("role") == "user")
        assistant_count = sum(1 for m in msgs if m.get("role") == "assistant")
        turn_count = min(user_count, assistant_count)
        st.caption(
            t(
                "sidebar.session.caption",
                turn=turn_count,
                user=user_count,
                assistant=assistant_count,
            )
        )

        if st.button(
            t("sidebar.clear"),
            use_container_width=True,
            key="btn_clear_chat",
            disabled=not st.session_state.get("messages"),
        ):
            st.session_state.messages = []
            st.session_state.pending_query = None
            st.rerun()

        st.markdown(
            f'<div class="sidebar-section" style="margin-top:20px;">{t("sidebar.tips")}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="sidebar-meta">{t("sidebar.tips.body")}</div>',
            unsafe_allow_html=True,
        )

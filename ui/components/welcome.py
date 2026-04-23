from __future__ import annotations

import streamlit as st

from . import icons

STARTER_PROMPTS: list[dict[str, str]] = [
    {
        "icon": icons.TARGET,
        "title": "开一家小型咖啡馆前，我该如何验证本地市场需求？",
    },
    {
        "icon": icons.MEGAPHONE,
        "title": "预算有限，我应该优先把钱投到哪几条营销渠道？",
    },
    {
        "icon": icons.CREDIT_CARD,
        "title": "如何判断我的产品是否已经达到了 PMF？",
    },
    {
        "icon": icons.CALCULATOR,
        "title": "小微企业第一年最常见的财务与税务坑有哪些？",
    },
]


def render_welcome() -> None:
    st.markdown(
        """
<div class="welcome">
  <div class="welcome__eyebrow">AI Entrepreneurship Advisor</div>
  <h2 class="welcome__headline">你好，有什么创业问题想聊聊？</h2>
  <p class="welcome__desc">
    我是你的 AI 创业顾问，能帮你从知识库里找到相关的商业洞察，给出
    <strong>结构化建议</strong>和<strong>可执行的下一步</strong>。像跟朋友聊天一样，直接说就好。
  </p>
  <div class="welcome__section-label">试试这些问题</div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="starter-grid">', unsafe_allow_html=True)
    cols = st.columns(2, gap="small")
    for idx, prompt in enumerate(STARTER_PROMPTS):
        with cols[idx % 2]:
            if st.button(
                prompt["title"],
                key=f"starter_{idx}",
                use_container_width=True,
            ):
                st.session_state.pending_query = prompt["title"]
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.caption("直接在下方输入框里开始提问，支持中英文。")

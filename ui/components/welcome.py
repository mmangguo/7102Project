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
  <div class="welcome__eyebrow">Early-stage founder copilot</div>
  <h2 class="welcome__headline">把碎片化的商业经验，变成你下一步的可落地动作。</h2>
  <p class="welcome__desc">
    基于 BusinessNewsDaily 清洗知识库的检索增强问答助手：先检索相关证据，再结构化给出
    <strong>核心洞察 · 落地建议 · 待补信息</strong>，并以“毒舌投资人”视角提出 3 个灵魂追问。
  </p>
  <div class="welcome__section-label">试试这些高频问题</div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="starter-grid">', unsafe_allow_html=True)
    cols = st.columns(2, gap="small")
    for idx, prompt in enumerate(STARTER_PROMPTS):
        with cols[idx % 2]:
            # Streamlit buttons don't support raw HTML labels, so we render a
            # plain text button and rely on CSS to give it a card look. The SVG
            # icon is decorative and lives in the description below.
            if st.button(
                prompt["title"],
                key=f"starter_{idx}",
                use_container_width=True,
            ):
                st.session_state.pending_query = prompt["title"]
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.caption("提示：你也可以直接在下方输入框里开始提问，支持中英文。")

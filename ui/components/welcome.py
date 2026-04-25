from __future__ import annotations

import streamlit as st

from ui.core.i18n import STARTER_PROMPT_KEYS, starter_prompt, t

from . import icons

_PROMPT_ICONS: dict[str, str] = {
    "starter.market": icons.TARGET,
    "starter.marketing": icons.MEGAPHONE,
    "starter.pmf": icons.CREDIT_CARD,
    "starter.finance": icons.CALCULATOR,
}


def render_welcome() -> None:
    st.markdown(
        f"""
<div class="welcome">
  <div class="welcome__eyebrow">{t("welcome.eyebrow")}</div>
  <h2 class="welcome__headline">{t("welcome.headline")}</h2>
  <p class="welcome__desc">{t("welcome.desc")}</p>
  <div class="welcome__section-label">{t("welcome.section_label")}</div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="starter-grid">', unsafe_allow_html=True)
    cols = st.columns(2, gap="small")
    for idx, key in enumerate(STARTER_PROMPT_KEYS):
        text_label = starter_prompt(key)
        with cols[idx % 2]:
            if st.button(
                text_label,
                key=f"starter_{key}",
                use_container_width=True,
            ):
                st.session_state.pending_query = text_label
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.caption(t("welcome.caption"))

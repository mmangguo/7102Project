"""Top-right language switcher used by app.py.

Renders a compact pill toggle (中文 / EN) anchored to the top-right of
the page, above the hero header. The active language is highlighted via
Streamlit's built-in ``type="primary"`` button styling, with a small CSS
polish in ``styles.py`` to compress the buttons into pills and right-align
them within the row.
"""

from __future__ import annotations

import streamlit as st

from ui.core.i18n import (
    LANGUAGE_LABELS,
    SUPPORTED_LANGUAGES,
    get_lang,
    set_lang,
    t,
)


def render_language_switcher() -> None:
    current = get_lang()

    # Zero-height marker; later CSS uses :has(.lang-switch) to scope styles
    # to the very next horizontal block (the row of pill buttons below).
    st.markdown(
        f'<div class="lang-switch" role="group" aria-label="{t("lang.aria")}"></div>',
        unsafe_allow_html=True,
    )

    spacer, *btn_cols = st.columns([6] + [1] * len(SUPPORTED_LANGUAGES))

    for col, lang_code in zip(btn_cols, SUPPORTED_LANGUAGES):
        with col:
            label = LANGUAGE_LABELS.get(lang_code, lang_code)
            if st.button(
                label,
                key=f"lang_btn_{lang_code}",
                type="primary" if current == lang_code else "secondary",
                use_container_width=True,
                help=label,
            ):
                if set_lang(lang_code):
                    st.rerun()

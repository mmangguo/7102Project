from __future__ import annotations

import streamlit as st


def inject_global_styles() -> None:
    st.markdown(
        """
<style>
.cite-badge {
    color: #8a8f98;
    font-size: 0.78em;
    vertical-align: super;
    margin-left: 2px;
    padding: 0 4px;
    border: 1px solid #d9dde3;
    border-radius: 8px;
    background: #f6f7f9;
}
</style>
""",
        unsafe_allow_html=True,
    )

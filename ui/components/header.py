from __future__ import annotations

import html

import streamlit as st

from pipeline import EntrepreneurshipAssistant
from ui.core.i18n import t

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
            f'aria-label="{t("header.chip.live.aria", chip=chip_text)}" '
            f'title="{t("header.chip.live.title", chip=chip_text)}">'
            f'<span class="dot" aria-hidden="true"></span>'
            f'{t("header.chip.live.text", chip=chip_text)}</span>'
        )
    else:
        chip_html = (
            f'<span class="app-hero__chip app-hero__chip--fallback" role="status" '
            f'aria-label="{t("header.chip.fallback.aria")}" '
            f'title="{t("header.chip.fallback.title")}">'
            f'<span class="dot" aria-hidden="true"></span>'
            f'{t("header.chip.fallback.text")}</span>'
        )

    st.markdown(
        f"""
<div class="app-hero">
  <div class="app-hero__logo" aria-hidden="true">{icons.SPARKLE}</div>
  <div class="app-hero__title-wrap">
    <h1 class="app-hero__title">{t("header.title")}</h1>
    <p class="app-hero__subtitle">{t("header.subtitle")}</p>
  </div>
  {chip_html}
</div>
""",
        unsafe_allow_html=True,
    )

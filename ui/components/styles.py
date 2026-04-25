from __future__ import annotations

import streamlit as st

_GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    /* ── Warm Intelligence palette ── */
    --color-primary: #6C5CE7;
    --color-primary-strong: #5B4ACF;
    --color-primary-light: #A78BFA;
    --color-primary-soft: rgba(108, 92, 231, 0.06);
    --color-primary-glow: rgba(108, 92, 231, 0.12);

    --color-accent: #38BDF8;
    --color-accent-warm: #FB923C;
    --color-accent-warm-soft: rgba(251, 146, 60, 0.08);

    --color-bg: #FAFBFF;
    --color-bg-card: #FFFFFF;
    --color-bg-sidebar: #F6F4FD;
    --color-bg-input: #FFFFFF;
    --color-bg-user: linear-gradient(135deg, #EEF2FF 0%, #F3EFFF 100%);

    --color-border: rgba(108, 92, 231, 0.07);
    --color-border-strong: rgba(108, 92, 231, 0.13);

    --color-text: #2D2B55;
    --color-text-muted: #6B7280;
    --color-text-subtle: #9CA3AF;

    --color-success: #10B981;
    --color-warning: #F59E0B;
    --color-danger: #EF4444;

    /* ── Gradients ── */
    --gradient-brand: linear-gradient(135deg, #6C5CE7 0%, #A78BFA 50%, #38BDF8 100%);
    --gradient-warm: linear-gradient(135deg, #6C5CE7 0%, #EC4899 100%);
    --gradient-text: linear-gradient(135deg, #6C5CE7, #A78BFA, #38BDF8);
    --gradient-card-assess: linear-gradient(135deg, rgba(251, 146, 60, 0.05) 0%, rgba(251, 146, 60, 0.01) 100%);
    --gradient-card-insight: linear-gradient(135deg, rgba(108, 92, 231, 0.05) 0%, rgba(108, 92, 231, 0.01) 100%);
    --gradient-card-action: linear-gradient(135deg, rgba(16, 185, 129, 0.05) 0%, rgba(16, 185, 129, 0.01) 100%);
    --gradient-card-gap: linear-gradient(135deg, rgba(156, 163, 175, 0.05) 0%, rgba(156, 163, 175, 0.01) 100%);
    --gradient-card-summary: linear-gradient(135deg, rgba(56, 189, 248, 0.05) 0%, rgba(56, 189, 248, 0.01) 100%);

    /* ── Spacing & Shape ── */
    --radius-sm: 12px;
    --radius-md: 16px;
    --radius-lg: 20px;
    --radius-xl: 24px;
    --radius-pill: 999px;

    --space-1: 4px;  --space-2: 8px;  --space-3: 12px;
    --space-4: 16px; --space-5: 20px; --space-6: 24px; --space-7: 32px;

    /* ── Shadows (warm-tinted) ── */
    --shadow-xs: 0 1px 3px rgba(108, 92, 231, 0.04);
    --shadow-sm: 0 2px 8px rgba(108, 92, 231, 0.05);
    --shadow-md: 0 4px 20px rgba(108, 92, 231, 0.07);
    --shadow-lg: 0 8px 40px rgba(108, 92, 231, 0.09);
    --shadow-glow: 0 0 0 3px var(--color-primary-glow);
    --shadow-gradient-glow:
        0 0 0 1px rgba(108, 92, 231, 0.12),
        0 0 16px rgba(108, 92, 231, 0.08),
        0 0 32px rgba(56, 189, 248, 0.05);

    /* ── Motion ── */
    --duration-fast: 150ms;
    --duration-base: 250ms;
    --duration-slow: 400ms;
    --ease: cubic-bezier(0.22, 1, 0.36, 1);
    --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);

    --typing-dot-size: 7px;
    --message-gap: 16px;
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

/* ── Typography ── */
.block-container,
[data-testid="stSidebar"] > div,
[data-testid="stChatInput"] textarea,
.app-hero, .welcome, .evidence-card,
.suggestions-label, .suggestion-group,
.starter-grid, .sidebar-meta, .sidebar-section,
.answer-card {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont,
                 'Segoe UI', Roboto, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* ================================================================
   PAGE BACKGROUND — Soft aurora glow
   ================================================================ */
[data-testid="stAppViewContainer"] {
    background: var(--color-bg);
}
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 60vh;
    background:
        radial-gradient(ellipse 80% 50% at 20% 0%, rgba(108, 92, 231, 0.06) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 5%, rgba(56, 189, 248, 0.05) 0%, transparent 55%),
        radial-gradient(ellipse 70% 50% at 50% 10%, rgba(167, 139, 250, 0.04) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}

.block-container {
    max-width: 840px;
    padding-top: 1.5rem;
    padding-bottom: 0.5rem;
    position: relative;
    z-index: 1;
}
h1, h2, h3 { letter-spacing: -0.02em; color: var(--color-text); }

footer, #MainMenu { visibility: hidden; }

/* Gradient text utility */
.gradient-text {
    background: var(--gradient-text);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ================================================================
   LANGUAGE SWITCHER — Top-right pill toggle
   The switcher renders a zero-height .lang-switch marker right before
   its row of columns. We use :has() to scope styling to the immediate
   next horizontal block, so unrelated columns elsewhere on the page
   are never affected.
   ================================================================ */
.lang-switch { display: block; height: 0; line-height: 0; margin: 0; }
[data-testid="stMarkdown"]:has(> div > .lang-switch),
[data-testid="stMarkdown"]:has(.lang-switch) {
    margin: 0 !important;
    padding: 0 !important;
}
[data-testid="element-container"]:has(.lang-switch) {
    margin: 0 !important;
    padding: 0 !important;
    min-height: 0 !important;
}
[data-testid="element-container"]:has(.lang-switch)
    + [data-testid="element-container"] [data-testid="stHorizontalBlock"] {
    gap: 6px !important;
    align-items: center !important;
    justify-content: flex-end !important;
    margin-bottom: 6px !important;
}
[data-testid="element-container"]:has(.lang-switch)
    + [data-testid="element-container"] .stButton > button {
    min-height: 30px !important;
    padding: 4px 12px !important;
    border-radius: var(--radius-pill) !important;
    font-weight: 600 !important;
    font-size: 0.78rem !important;
    line-height: 1 !important;
    letter-spacing: 0.02em !important;
    box-shadow: var(--shadow-xs) !important;
    transition: all var(--duration-base) var(--ease) !important;
}
[data-testid="element-container"]:has(.lang-switch)
    + [data-testid="element-container"] .stButton > button[kind="secondary"] {
    background: rgba(255, 255, 255, 0.85) !important;
    color: var(--color-text-muted) !important;
    border: 1px solid var(--color-border-strong) !important;
}
[data-testid="element-container"]:has(.lang-switch)
    + [data-testid="element-container"] .stButton > button[kind="secondary"]:hover {
    color: var(--color-primary-strong) !important;
    border-color: var(--color-primary) !important;
    background: var(--color-primary-soft) !important;
}
[data-testid="element-container"]:has(.lang-switch)
    + [data-testid="element-container"] .stButton > button[kind="primary"] {
    background: var(--gradient-brand) !important;
    color: #fff !important;
    border: 1px solid transparent !important;
    box-shadow: 0 2px 8px rgba(108, 92, 231, 0.22) !important;
}

/* ================================================================
   HERO HEADER — Clean + gradient logo
   ================================================================ */
.app-hero {
    display: flex;
    align-items: center;
    gap: var(--space-4);
    padding: var(--space-4) var(--space-5);
    margin: 0 calc(-1 * var(--space-5)) var(--space-5);
    background: rgba(255, 255, 255, 0.65);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(108, 92, 231, 0.06);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-sm);
}
.app-hero__logo {
    width: 40px; height: 40px;
    border-radius: var(--radius-md);
    background: var(--gradient-brand);
    color: #fff;
    display: grid; place-items: center;
    box-shadow:
        0 2px 8px rgba(108, 92, 231, 0.2),
        0 0 0 3px rgba(108, 92, 231, 0.06);
    flex-shrink: 0;
    animation: logo-breathe 4s ease-in-out infinite;
}
@keyframes logo-breathe {
    0%, 100% { box-shadow: 0 2px 8px rgba(108, 92, 231, 0.2), 0 0 0 3px rgba(108, 92, 231, 0.06); }
    50%      { box-shadow: 0 4px 16px rgba(108, 92, 231, 0.25), 0 0 0 5px rgba(108, 92, 231, 0.08); }
}
.app-hero__logo svg { width: 20px; height: 20px; }
.app-hero__title-wrap { display: flex; flex-direction: column; gap: 2px; flex: 1; min-width: 0; }
.app-hero__title {
    font-size: 1.05rem; font-weight: 700; color: var(--color-text);
    line-height: 1.2; margin: 0; letter-spacing: -0.02em;
}
.app-hero__subtitle { font-size: 0.76rem; color: var(--color-text-muted); margin: 0; }

/* Status chip */
.app-hero__chip {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 5px 12px; border-radius: var(--radius-pill);
    font-size: 0.7rem; font-weight: 600; white-space: nowrap;
    background: rgba(255, 255, 255, 0.8);
    border: 1px solid var(--color-border);
    color: var(--color-text-muted);
}
.app-hero__chip .dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: var(--color-text-subtle);
}
.app-hero__chip--live {
    background: rgba(16, 185, 129, 0.06);
    border-color: rgba(16, 185, 129, 0.18);
    color: #059669;
}
.app-hero__chip--live .dot {
    background: var(--color-success);
    box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.12);
    animation: pulse-dot 2.5s ease-in-out infinite;
}
@keyframes pulse-dot {
    0%, 100% { box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.12); }
    50%      { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0.18); }
}
.app-hero__chip--fallback {
    background: rgba(245, 158, 11, 0.06);
    border-color: rgba(245, 158, 11, 0.18);
    color: #B45309;
}
.app-hero__chip--fallback .dot { background: var(--color-warning); }

/* ================================================================
   WELCOME / EMPTY STATE — Atmospheric
   ================================================================ */
.welcome { padding: var(--space-6) 0 var(--space-3); }
.welcome__eyebrow {
    font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.18em;
    color: var(--color-primary); font-weight: 700; margin-bottom: var(--space-3);
}
.welcome__headline {
    font-size: 1.75rem; font-weight: 700;
    line-height: 1.2; margin: 0 0 var(--space-4); letter-spacing: -0.025em;
    background: var(--gradient-text);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.welcome__desc {
    font-size: 0.92rem; color: var(--color-text-muted); line-height: 1.7;
    margin: 0 0 var(--space-6); max-width: 56ch;
}
.welcome__desc strong { color: var(--color-text); font-weight: 600; }
.welcome__section-label {
    font-size: 0.68rem; font-weight: 700; color: var(--color-text-subtle);
    text-transform: uppercase; letter-spacing: 0.16em;
    margin: var(--space-6) 0 var(--space-3);
}

/* Starter cards — floating bubble style */
.starter-grid .stButton > button {
    width: 100% !important; min-height: 72px;
    padding: 16px 20px !important;
    text-align: left !important; justify-content: flex-start !important; align-items: center;
    white-space: normal !important; line-height: 1.55;
    border-radius: 20px !important;
    background: #FFFFFF !important;
    border: 1.5px solid rgba(108, 92, 231, 0.12) !important;
    color: var(--color-text) !important; font-weight: 500 !important; font-size: 0.88rem !important;
    box-shadow:
        0 6px 20px rgba(108, 92, 231, 0.10),
        0 2px 6px rgba(0, 0, 0, 0.04) !important;
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.22, 1, 0.36, 1) !important;
    position: relative;
}
.starter-grid .stButton > button:hover {
    border-color: rgba(108, 92, 231, 0.25) !important;
    background: #FFFFFF !important;
    box-shadow:
        0 10px 32px rgba(108, 92, 231, 0.14),
        0 4px 12px rgba(0, 0, 0, 0.05),
        0 0 0 3px rgba(108, 92, 231, 0.06) !important;
    transform: translateY(-4px) !important;
}
.starter-grid .stButton > button:active {
    transform: translateY(-1px) !important;
    box-shadow:
        0 3px 10px rgba(108, 92, 231, 0.08),
        0 1px 3px rgba(0, 0, 0, 0.04) !important;
}
.starter-grid .stButton > button:focus-visible {
    outline: none !important;
    border-color: var(--color-primary) !important;
    box-shadow:
        0 0 0 3px rgba(108, 92, 231, 0.14),
        0 6px 20px rgba(108, 92, 231, 0.10) !important;
}

/* ================================================================
   CHAT MESSAGES — Natural conversation feel
   ================================================================ */
[data-testid="stChatMessage"] {
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    background: rgba(255, 255, 255, 0.75);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    padding: 16px 20px;
    margin-bottom: var(--message-gap);
    box-shadow: var(--shadow-xs);
    transition: box-shadow var(--duration-base) var(--ease);
}

/* User message — warm gradient tint */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: var(--color-bg-user);
    border-color: rgba(108, 92, 231, 0.08);
    box-shadow: var(--shadow-xs);
}

/* Assistant message — clean white with subtle left accent */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: rgba(255, 255, 255, 0.85);
    border-color: rgba(108, 92, 231, 0.06);
    border-left: 2px solid rgba(108, 92, 231, 0.15);
}

/* Avatar styling */
[data-testid="stChatMessage"] [data-testid*="chatAvatarIcon"] > div {
    border-radius: var(--radius-sm) !important;
}

/* Bottom bar container — floating bubble island */
[data-testid="stBottom"] {
    background: transparent !important;
    border-top: none !important;
    padding-bottom: 0 !important;
}
[data-testid="stBottom"] > div {
    background: transparent !important;
}
[data-testid="stBottomBlockContainer"] {
    background: transparent !important;
    padding-top: 0;
    padding-bottom: env(safe-area-inset-bottom, 6px);
    max-width: 840px;
    margin: 0 auto;
}

/* Floating bubble wrapper */
[data-testid="stChatInput"] {
    border-radius: 28px !important;
    border: 1.5px solid rgba(108, 92, 231, 0.16) !important;
    background: rgba(255, 255, 255, 0.92) !important;
    backdrop-filter: blur(24px) saturate(1.4);
    -webkit-backdrop-filter: blur(24px) saturate(1.4);
    box-shadow:
        0 -2px 16px rgba(108, 92, 231, 0.05),
        0 4px 24px rgba(108, 92, 231, 0.10),
        0 1px 4px rgba(0, 0, 0, 0.06),
        inset 0 1px 0 rgba(255, 255, 255, 0.8);
    transition: all var(--duration-base) var(--ease);
    margin-bottom: 4px;
}
[data-testid="stChatInput"] textarea {
    font-size: 0.95rem !important;
    min-height: 48px !important;
    color: var(--color-text);
    background: transparent !important;
}
[data-testid="stChatInput"] button {
    color: #fff !important;
    background: var(--gradient-brand) !important;
    border-radius: 50% !important;
    width: 36px !important; height: 36px !important;
    min-width: 36px !important;
    padding: 0 !important;
    display: inline-flex; align-items: center; justify-content: center;
    box-shadow: 0 2px 10px rgba(108, 92, 231, 0.25);
    transition: all var(--duration-base) var(--ease);
}
[data-testid="stChatInput"] button:hover {
    color: #fff !important;
    box-shadow: 0 4px 16px rgba(108, 92, 231, 0.35);
    transform: scale(1.08);
}
[data-testid="stChatInput"]:focus-within {
    border-color: rgba(108, 92, 231, 0.30) !important;
    background: #FFFFFF !important;
    box-shadow:
        0 -2px 16px rgba(108, 92, 231, 0.05),
        0 4px 24px rgba(108, 92, 231, 0.12),
        0 0 0 3px rgba(108, 92, 231, 0.10),
        0 0 48px rgba(56, 189, 248, 0.06),
        inset 0 1px 0 rgba(255, 255, 255, 0.9);
}

/* ================================================================
   TYPING INDICATOR (soft pulse)
   ================================================================ */
.typing-indicator {
    display: inline-flex; align-items: center; gap: 5px; padding: 8px 0;
}
.typing-indicator__dot {
    width: var(--typing-dot-size); height: var(--typing-dot-size);
    border-radius: 50%;
    background: var(--color-primary-light);
    opacity: 0.35;
    animation: t-pulse 1.4s ease-in-out infinite;
}
.typing-indicator__dot:nth-child(2) { animation-delay: 0.16s; }
.typing-indicator__dot:nth-child(3) { animation-delay: 0.32s; }
@keyframes t-pulse {
    0%, 100% { opacity: 0.35; transform: scale(0.85); }
    50%      { opacity: 1;   transform: scale(1);     }
}

/* Streaming cursor */
.stream-cursor {
    display: inline-block; width: 2px; height: 1.05em;
    vertical-align: -0.15em; margin-left: 2px;
    background: var(--gradient-brand); border-radius: 1px;
    animation: blink 1s steps(2) infinite;
}
@keyframes blink { 50% { opacity: 0; } }

/* ================================================================
   ANSWER CARDS — Soft gradient headers, no harsh borders
   ================================================================ */
.answer-intro {
    margin-bottom: 14px;
    font-size: 0.88rem;
    color: var(--color-text-muted);
    line-height: 1.7;
}
.answer-intro p { margin: 0 0 8px; }

.answer-card {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: 0;
    margin-bottom: 10px;
    box-shadow: var(--shadow-xs);
    overflow: hidden;
    transition: box-shadow var(--duration-base) var(--ease),
                transform var(--duration-fast) var(--ease);
}
.answer-card:hover {
    box-shadow: var(--shadow-sm);
    transform: translateY(-1px);
}
.answer-card:last-child { margin-bottom: 4px; }

.answer-card__header {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 16px;
    background: var(--gradient-card-insight);
    border-bottom: 1px solid var(--color-border);
}
.answer-card__icon {
    font-size: 0.95rem;
    line-height: 1;
    flex-shrink: 0;
}
.answer-card__heading {
    font-size: 0.88rem;
    font-weight: 700;
    color: var(--color-text);
    letter-spacing: -0.01em;
}
.answer-card__body {
    padding: 12px 16px;
    font-size: 0.85rem;
    color: var(--color-text-muted);
    line-height: 1.75;
}
.answer-card__body p { margin: 0 0 8px; }
.answer-card__body p:last-child { margin-bottom: 0; }
.answer-card__body ol, .answer-card__body ul {
    margin: 4px 0 8px;
    padding-left: 22px;
}
.answer-card__body li { margin-bottom: 6px; }
.answer-card__body li:last-child { margin-bottom: 0; }
.answer-card__body strong {
    color: var(--color-text);
    font-weight: 600;
}

/* Per-section gradient tints (set via inline style in Python) */
.answer-card[data-section="assess"]  .answer-card__header { background: var(--gradient-card-assess); }
.answer-card[data-section="insight"] .answer-card__header { background: var(--gradient-card-insight); }
.answer-card[data-section="action"]  .answer-card__header { background: var(--gradient-card-action); }
.answer-card[data-section="gap"]     .answer-card__header { background: var(--gradient-card-gap); }
.answer-card[data-section="summary"] .answer-card__header { background: var(--gradient-card-summary); }

/* ================================================================
   CITATIONS
   ================================================================ */
.cite-badge {
    display: inline-flex; align-items: center; justify-content: center;
    min-width: 20px; height: 18px; padding: 0 6px;
    margin: 0 2px; border-radius: var(--radius-pill);
    font-size: 0.64rem; font-weight: 700; letter-spacing: 0.02em;
    color: #fff; background: var(--gradient-brand);
    line-height: 1; vertical-align: baseline;
    box-shadow: 0 1px 4px rgba(108, 92, 231, 0.2);
}

/* Evidence cards */
.evidence-card {
    display: flex; flex-direction: column; gap: 8px;
    padding: 14px 16px;
    margin-bottom: 10px;
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-xs);
    cursor: default;
    transition: all var(--duration-base) var(--ease);
}
.evidence-card:hover {
    box-shadow: var(--shadow-sm);
    transform: translateY(-1px);
}
.evidence-card__header {
    display: flex; align-items: center; gap: 10px; justify-content: space-between;
}
.evidence-card__title {
    font-weight: 600; font-size: 0.88rem; color: var(--color-text);
    text-decoration: none; display: inline-flex; align-items: center;
    gap: 8px; line-height: 1.4; word-break: break-word;
    transition: color var(--duration-fast) var(--ease);
}
.evidence-card__title:hover { color: var(--color-primary); }
.evidence-card__title svg { width: 13px; height: 13px; opacity: 0.35; flex-shrink: 0; }
.evidence-card__index {
    display: inline-flex; align-items: center; justify-content: center;
    width: 20px; height: 20px; border-radius: var(--radius-sm);
    background: var(--gradient-brand); color: #fff;
    font-size: 0.64rem; font-weight: 700; flex-shrink: 0;
    box-shadow: 0 1px 3px rgba(108, 92, 231, 0.18);
}
.evidence-card__score {
    display: inline-flex; align-items: center; gap: 4px;
    padding: 3px 10px; font-size: 0.66rem; font-weight: 600;
    color: #059669;
    background: rgba(16, 185, 129, 0.06);
    border-radius: var(--radius-pill);
    border: 1px solid rgba(16, 185, 129, 0.12);
    white-space: nowrap; flex-shrink: 0; font-variant-numeric: tabular-nums;
}
.evidence-card__snippet {
    font-size: 0.83rem; color: var(--color-text-muted);
    line-height: 1.65; margin: 0;
}

/* ================================================================
   SUGGESTIONS — Conversation-style follow-ups
   ================================================================ */
.suggestions-label {
    display: flex; align-items: center; gap: 8px;
    font-size: 0.68rem; font-weight: 700; color: var(--color-primary);
    text-transform: uppercase; letter-spacing: 0.16em;
    margin: var(--space-5) 0 var(--space-3);
    opacity: 0.7;
}
.suggestions-label svg { width: 13px; height: 13px; color: var(--color-primary-light); }

.suggestion-group .stButton > button {
    width: 100%;
    text-align: left !important;
    justify-content: flex-start !important;
    white-space: normal; line-height: 1.55;
    padding: 11px 16px 11px 14px;
    border-radius: var(--radius-md);
    background: rgba(255, 255, 255, 0.7) !important;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--color-border) !important;
    border-left: 3px solid rgba(108, 92, 231, 0.15) !important;
    color: var(--color-text) !important;
    font-weight: 500; font-size: 0.86rem;
    box-shadow: var(--shadow-xs);
    cursor: pointer;
    transition: all var(--duration-base) var(--ease);
}
.suggestion-group .stButton > button:hover {
    border-color: rgba(108, 92, 231, 0.12) !important;
    border-left-color: var(--color-primary) !important;
    background: var(--color-primary-soft) !important;
    color: var(--color-primary-strong) !important;
    box-shadow: var(--shadow-sm);
    transform: translateY(-1px);
}
.suggestion-group .stButton > button:focus-visible {
    outline: none;
    box-shadow: var(--shadow-glow);
    border-color: var(--color-primary) !important;
}

/* ================================================================
   SIDEBAR
   ================================================================ */
section[data-testid="stSidebar"] {
    background: var(--color-bg-sidebar);
    border-right: 1px solid var(--color-border);
}
section[data-testid="stSidebar"] .sidebar-section {
    font-size: 0.66rem; text-transform: uppercase; letter-spacing: 0.16em;
    font-weight: 700; color: var(--color-text-subtle); margin: 14px 0 6px;
}
section[data-testid="stSidebar"] .sidebar-meta {
    font-size: 0.84rem; color: var(--color-text-muted); line-height: 1.55;
}
section[data-testid="stSidebar"] .sidebar-chip {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 4px 12px; border-radius: var(--radius-pill);
    font-size: 0.7rem; font-weight: 600;
    background: var(--color-bg-card); border: 1px solid var(--color-border);
    color: var(--color-text-muted); box-shadow: var(--shadow-xs);
}
section[data-testid="stSidebar"] .sidebar-chip--live {
    color: #059669; border-color: rgba(16,185,129,0.18); background: rgba(16,185,129,0.06);
}
section[data-testid="stSidebar"] .sidebar-chip--fallback {
    color: #B45309; border-color: rgba(245,158,11,0.18); background: rgba(245,158,11,0.06);
}
section[data-testid="stSidebar"] .stButton > button {
    width: 100%; border-radius: var(--radius-md);
    border: 1px solid var(--color-border);
    background: var(--color-bg-card); color: var(--color-text);
    font-weight: 500; cursor: pointer; box-shadow: var(--shadow-xs);
    transition: all var(--duration-base) var(--ease);
}
section[data-testid="stSidebar"] .stButton > button:hover {
    border-color: var(--color-danger); color: var(--color-danger);
}

/* Slider accent */
[data-testid="stSlider"] [role="slider"] {
    background: var(--color-primary) !important;
}

/* ================================================================
   MISC
   ================================================================ */
.stCaption, [data-testid="stCaption"] {
    color: var(--color-text-subtle) !important; font-size: 0.78rem !important;
}
[data-testid="stExpander"] summary {
    border-radius: var(--radius-md); cursor: pointer;
    transition: color var(--duration-fast) var(--ease);
}
[data-testid="stExpander"] summary:hover { color: var(--color-primary); }

/* Status widget */
[data-testid="stStatusWidget"] {
    border-radius: var(--radius-md);
    border: 1px solid var(--color-border);
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(8px);
}

/* ================================================================
   GLOBAL MOBILE FOUNDATIONS
   ================================================================ */
html, body, [data-testid="stAppViewContainer"] {
    overflow-x: hidden;
}
*, *::before, *::after {
    -webkit-tap-highlight-color: transparent;
}
button, [role="button"], a {
    touch-action: manipulation;
}

/* ================================================================
   RESPONSIVE — TABLET  (max 768px)
   ================================================================ */
@media (max-width: 768px) {
    :root {
        --radius-sm: 10px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --radius-xl: 20px;
        --message-gap: 12px;
        --typing-dot-size: 6px;
    }

    [data-testid="stAppViewContainer"]::before { height: 40vh; }

    .block-container {
        max-width: 100%;
        padding-top: 1rem;
        padding-bottom: calc(1.5rem + env(safe-area-inset-bottom, 0px));
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    .app-hero {
        flex-wrap: wrap;
        gap: var(--space-3);
        padding: var(--space-3) var(--space-4);
        margin: 0 -1rem var(--space-4);
        border-radius: var(--radius-md);
    }
    .app-hero__logo { width: 34px; height: 34px; border-radius: var(--radius-sm); }
    .app-hero__logo svg { width: 17px; height: 17px; }
    .app-hero__title { font-size: 0.95rem; }
    .app-hero__subtitle { font-size: 0.7rem; }
    .app-hero__chip {
        order: 3; width: 100%; justify-content: center;
        padding: 4px 10px; font-size: 0.66rem; margin-top: 2px;
    }

    .welcome { padding: var(--space-4) 0 var(--space-2); }
    .welcome__eyebrow { font-size: 0.62rem; }
    .welcome__headline { font-size: 1.3rem; }
    .welcome__desc { font-size: 0.84rem; max-width: 100%; }
    .welcome__section-label { margin: var(--space-4) 0 var(--space-2); }

    .starter-grid .stButton > button {
        min-height: 56px; padding: 14px 16px;
        font-size: 0.84rem; border-radius: var(--radius-md);
    }
    .starter-grid .stButton > button:hover { transform: translateY(-2px); }

    [data-testid="stChatMessage"] {
        padding: 12px 14px; border-radius: var(--radius-md);
    }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        border-left-width: 2px;
    }

    [data-testid="stChatInput"] {
        border-radius: 22px !important;
        margin-bottom: 4px;
    }
    [data-testid="stChatInput"] textarea {
        font-size: 16px !important; min-height: 44px !important;
    }
    [data-testid="stChatInput"] button {
        width: 34px !important; height: 34px !important; min-width: 34px !important;
    }
    [data-testid="stBottom"] {
        padding-bottom: env(safe-area-inset-bottom, 0px);
    }

    .answer-card__header { padding: 9px 14px; }
    .answer-card__heading { font-size: 0.84rem; }
    .answer-card__body { padding: 10px 14px; font-size: 0.82rem; }
    .answer-card__body ol, .answer-card__body ul { padding-left: 18px; }
    .answer-card:hover { transform: none; }

    .evidence-card { padding: 12px 14px; border-radius: var(--radius-sm); }
    .evidence-card:hover { transform: none; }
    .evidence-card__header { flex-wrap: wrap; gap: 8px; }
    .evidence-card__title { font-size: 0.82rem; gap: 6px; }
    .evidence-card__snippet { font-size: 0.8rem; }

    .suggestions-label { margin: var(--space-4) 0 var(--space-2); }
    .suggestion-group .stButton > button {
        padding: 10px 14px 10px 12px; font-size: 0.82rem; min-height: 44px;
    }
    .suggestion-group .stButton > button:hover { transform: none; }

    .cite-badge { min-width: 18px; height: 17px; font-size: 0.6rem; }
}

/* ================================================================
   RESPONSIVE — PHONE  (max 480px)
   ================================================================ */
@media (max-width: 480px) {
    .block-container {
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
    }

    .app-hero {
        margin-left: -0.75rem; margin-right: -0.75rem;
        padding: var(--space-2) var(--space-3);
        border-radius: var(--radius-sm);
    }
    .app-hero__logo { width: 30px; height: 30px; }
    .app-hero__logo svg { width: 15px; height: 15px; }
    .app-hero__title { font-size: 0.88rem; }
    .app-hero__subtitle { font-size: 0.66rem; }

    .welcome__headline { font-size: 1.15rem; line-height: 1.25; }
    .welcome__desc { font-size: 0.8rem; }

    [data-testid="stChatMessage"] { padding: 10px 12px; }

    .answer-card__header { padding: 8px 12px; gap: 6px; }
    .answer-card__icon { font-size: 0.85rem; }
    .answer-card__heading { font-size: 0.8rem; }
    .answer-card__body { padding: 9px 12px; font-size: 0.78rem; line-height: 1.65; }
    .answer-card__body ol, .answer-card__body ul { padding-left: 16px; }
    .answer-card__body li { margin-bottom: 4px; }

    .evidence-card { padding: 10px 12px; }
    .evidence-card__header { flex-direction: column; align-items: flex-start; gap: 6px; }
    .evidence-card__title { font-size: 0.78rem; }
    .evidence-card__snippet { font-size: 0.76rem; }
    .evidence-card__score { font-size: 0.62rem; }

    .starter-grid .stButton > button {
        min-height: 52px; padding: 10px 12px; font-size: 0.8rem;
    }
    .suggestion-group .stButton > button {
        padding: 10px 12px 10px 10px; font-size: 0.8rem;
    }
}
</style>
"""


def inject_global_styles() -> None:
    st.markdown(_GLOBAL_CSS, unsafe_allow_html=True)

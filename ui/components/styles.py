from __future__ import annotations

import streamlit as st

_GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    /* ── Premium Light palette (Micro SaaS Indigo + Emerald) ── */
    --color-primary: #6366F1;
    --color-primary-strong: #4F46E5;
    --color-primary-soft: rgba(99, 102, 241, 0.08);
    --color-primary-glow: rgba(99, 102, 241, 0.15);

    --color-cta: #10B981;
    --color-cta-strong: #059669;
    --color-cta-soft: rgba(16, 185, 129, 0.08);

    --color-bg: #F5F3FF;
    --color-bg-card: #FFFFFF;
    --color-bg-sidebar: #F0EDFC;
    --color-bg-input: #FFFFFF;
    --color-bg-user: rgba(99, 102, 241, 0.06);

    --color-border: rgba(99, 102, 241, 0.10);
    --color-border-strong: rgba(99, 102, 241, 0.18);
    --color-border-glass: rgba(255, 255, 255, 0.55);

    --color-text: #1E1B4B;
    --color-text-muted: #4C5270;
    --color-text-subtle: #8084A1;

    --color-success: #10B981;
    --color-warning: #F59E0B;
    --color-danger: #EF4444;

    /* ── Spacing & Shape ── */
    --radius-sm: 12px;
    --radius-md: 16px;
    --radius-lg: 20px;
    --radius-xl: 24px;
    --radius-pill: 999px;

    --space-1: 4px;  --space-2: 8px;  --space-3: 12px;
    --space-4: 16px; --space-5: 20px; --space-6: 24px; --space-7: 32px;

    /* ── Shadows (layered depth) ── */
    --shadow-xs: 0 1px 2px rgba(99, 102, 241, 0.04);
    --shadow-sm: 0 2px 8px rgba(99, 102, 241, 0.06);
    --shadow-md: 0 4px 16px rgba(99, 102, 241, 0.08);
    --shadow-lg: 0 8px 32px rgba(99, 102, 241, 0.10);
    --shadow-glow: 0 0 0 4px var(--color-primary-glow);

    /* ── Glass effects ── */
    --glass-bg: rgba(255, 255, 255, 0.72);
    --glass-blur: 16px;
    --glass-border: 1px solid rgba(255, 255, 255, 0.45);

    /* ── Motion ── */
    --duration-fast: 150ms;
    --duration-base: 250ms;
    --duration-slow: 400ms;
    --ease: cubic-bezier(0.22, 1, 0.36, 1);

    --typing-dot-size: 7px;
    --message-gap: 20px;
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

/* ── Typography: scoped to content areas only ── */
.block-container,
[data-testid="stSidebar"] > div,
[data-testid="stChatInput"] textarea,
.app-hero, .welcome, .evidence-card,
.suggestions-label, .suggestion-group,
.starter-grid, .sidebar-meta, .sidebar-section {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont,
                 'Segoe UI', Roboto, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* ── Page chrome ── */
.block-container {
    max-width: 840px;
    padding-top: 1.5rem;
    padding-bottom: 6rem;
}
h1, h2, h3 { letter-spacing: -0.02em; color: var(--color-text); }

footer, #MainMenu { visibility: hidden; }

/* ================================================================
   HERO HEADER
   ================================================================ */
.app-hero {
    display: flex;
    align-items: center;
    gap: var(--space-4);
    padding: var(--space-4) var(--space-5);
    margin: 0 calc(-1 * var(--space-5)) var(--space-6);
    background: var(--glass-bg);
    backdrop-filter: blur(var(--glass-blur));
    -webkit-backdrop-filter: blur(var(--glass-blur));
    border: var(--glass-border);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-sm);
}
.app-hero__logo {
    width: 42px; height: 42px;
    border-radius: var(--radius-md);
    background: linear-gradient(135deg, #6366F1 0%, #818CF8 50%, #10B981 100%);
    color: #fff;
    display: grid; place-items: center;
    box-shadow: var(--shadow-md);
    flex-shrink: 0;
}
.app-hero__logo svg { width: 22px; height: 22px; }
.app-hero__title-wrap { display: flex; flex-direction: column; gap: 2px; flex: 1; min-width: 0; }
.app-hero__title {
    font-size: 1.15rem; font-weight: 700; color: var(--color-text);
    line-height: 1.2; margin: 0; letter-spacing: -0.02em;
}
.app-hero__subtitle { font-size: 0.8rem; color: var(--color-text-muted); margin: 0; }

/* Status chip */
.app-hero__chip {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 5px 12px; border-radius: var(--radius-pill);
    font-size: 0.72rem; font-weight: 600; white-space: nowrap;
    background: var(--glass-bg);
    backdrop-filter: blur(8px);
    border: 1px solid var(--color-border);
    color: var(--color-text-muted);
}
.app-hero__chip .dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: var(--color-text-subtle);
}
.app-hero__chip--live {
    background: rgba(16, 185, 129, 0.06);
    border-color: rgba(16, 185, 129, 0.22);
    color: #059669;
}
.app-hero__chip--live .dot {
    background: var(--color-success);
    box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15);
    animation: pulse-dot 2s ease-in-out infinite;
}
@keyframes pulse-dot {
    0%, 100% { box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15); }
    50%      { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0.22); }
}
.app-hero__chip--fallback {
    background: rgba(245, 158, 11, 0.06);
    border-color: rgba(245, 158, 11, 0.22);
    color: #B45309;
}
.app-hero__chip--fallback .dot { background: var(--color-warning); }

/* ================================================================
   WELCOME / EMPTY STATE
   ================================================================ */
.welcome { padding: var(--space-5) 0 var(--space-3); }
.welcome__eyebrow {
    font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.16em;
    color: var(--color-primary); font-weight: 700; margin-bottom: var(--space-3);
}
.welcome__headline {
    font-size: 1.75rem; font-weight: 700; color: var(--color-text);
    line-height: 1.18; margin: 0 0 var(--space-3); letter-spacing: -0.025em;
}
.welcome__desc {
    font-size: 0.95rem; color: var(--color-text-muted); line-height: 1.6;
    margin: 0 0 var(--space-6); max-width: 60ch;
}
.welcome__desc strong { color: var(--color-text); font-weight: 600; }
.welcome__section-label {
    font-size: 0.7rem; font-weight: 700; color: var(--color-text-subtle);
    text-transform: uppercase; letter-spacing: 0.16em;
    margin: var(--space-6) 0 var(--space-3);
}

/* Starter cards — glass morphism */
.starter-grid .stButton > button {
    width: 100%; min-height: 88px;
    padding: 16px 18px;
    text-align: left; justify-content: flex-start; align-items: flex-start;
    white-space: normal; line-height: 1.5;
    border-radius: var(--radius-lg);
    background: var(--glass-bg);
    backdrop-filter: blur(var(--glass-blur));
    -webkit-backdrop-filter: blur(var(--glass-blur));
    border: 1px solid var(--color-border);
    color: var(--color-text); font-weight: 500; font-size: 0.9rem;
    box-shadow: var(--shadow-sm);
    cursor: pointer;
    transition: transform var(--duration-fast) var(--ease),
                border-color var(--duration-base) var(--ease),
                box-shadow var(--duration-base) var(--ease);
}
.starter-grid .stButton > button:hover {
    border-color: var(--color-primary);
    box-shadow: var(--shadow-md), var(--shadow-glow);
    transform: translateY(-2px);
}
.starter-grid .stButton > button:active {
    transform: translateY(0);
    box-shadow: var(--shadow-sm);
}
.starter-grid .stButton > button:focus-visible {
    outline: none;
    box-shadow: var(--shadow-glow);
    border-color: var(--color-primary);
}

/* ================================================================
   CHAT MESSAGES  (glass bubbles)
   ================================================================ */
[data-testid="stChatMessage"] {
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    background: var(--glass-bg);
    backdrop-filter: blur(var(--glass-blur));
    -webkit-backdrop-filter: blur(var(--glass-blur));
    padding: 16px 20px;
    margin-bottom: var(--message-gap);
    box-shadow: var(--shadow-xs);
    transition: box-shadow var(--duration-base) var(--ease);
}
[data-testid="stChatMessage"]:hover {
    box-shadow: var(--shadow-sm);
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: var(--color-bg-user);
    border-color: rgba(99, 102, 241, 0.12);
}

/* Chat input — elevated glass */
[data-testid="stChatInput"] {
    border-radius: var(--radius-xl) !important;
    box-shadow: var(--shadow-md);
    border: 1px solid var(--color-border-strong) !important;
    background: var(--color-bg-input);
}
[data-testid="stChatInput"] textarea {
    font-size: 0.95rem !important;
    min-height: 48px !important;
    color: var(--color-text);
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--color-primary) !important;
    box-shadow: var(--shadow-glow), var(--shadow-md);
}

/* ================================================================
   TYPING INDICATOR (3-dot pulse)
   ================================================================ */
.typing-indicator {
    display: inline-flex; align-items: center; gap: 5px; padding: 8px 0;
}
.typing-indicator__dot {
    width: var(--typing-dot-size); height: var(--typing-dot-size);
    border-radius: 50%;
    background: var(--color-primary);
    opacity: 0.3;
    animation: t-pulse 1.4s ease-in-out infinite;
}
.typing-indicator__dot:nth-child(2) { animation-delay: 0.16s; }
.typing-indicator__dot:nth-child(3) { animation-delay: 0.32s; }
@keyframes t-pulse {
    0%, 100% { opacity: 0.3; transform: scale(0.8); }
    50%      { opacity: 1;   transform: scale(1);   }
}

/* Streaming cursor */
.stream-cursor {
    display: inline-block; width: 2px; height: 1.05em;
    vertical-align: -0.15em; margin-left: 2px;
    background: var(--color-primary); border-radius: 1px;
    animation: blink 1s steps(2) infinite;
}
@keyframes blink { 50% { opacity: 0; } }

/* ================================================================
   ANSWER CARDS (structured response sections)
   ================================================================ */
.answer-intro {
    margin-bottom: 14px;
    font-size: 0.88rem;
    color: var(--color-text-muted);
    line-height: 1.7;
}
.answer-intro p { margin: 0 0 8px; }

.answer-card {
    background: #FFFFFF;
    border: 1px solid var(--color-border);
    border-left: 3px solid var(--color-primary);
    border-radius: var(--radius-sm);
    padding: 14px 18px;
    margin-bottom: 10px;
    box-shadow: var(--shadow-xs);
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
    margin-bottom: 10px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--color-border);
}
.answer-card__icon {
    font-size: 1rem;
    line-height: 1;
    flex-shrink: 0;
}
.answer-card__heading {
    font-size: 0.92rem;
    font-weight: 700;
    color: var(--color-text);
    letter-spacing: -0.01em;
}
.answer-card__body {
    font-size: 0.86rem;
    color: var(--color-text-muted);
    line-height: 1.7;
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

/* ================================================================
   CITATIONS
   ================================================================ */
.cite-badge {
    display: inline-flex; align-items: center; justify-content: center;
    min-width: 20px; height: 18px; padding: 0 6px;
    margin: 0 2px; border-radius: var(--radius-pill);
    font-size: 0.66rem; font-weight: 700; letter-spacing: 0.02em;
    color: #fff; background: var(--color-primary);
    line-height: 1; vertical-align: baseline;
    box-shadow: 0 1px 3px rgba(99, 102, 241, 0.25);
}

/* Evidence context cards — glass + left accent */
.evidence-card {
    display: flex; flex-direction: column; gap: 8px;
    padding: 14px 16px 14px 18px;
    margin-bottom: 12px;
    background: var(--glass-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--color-border);
    border-left: 3px solid var(--color-primary);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-xs);
    cursor: default;
    transition: border-color var(--duration-base) var(--ease),
                box-shadow var(--duration-base) var(--ease),
                transform var(--duration-fast) var(--ease);
}
.evidence-card:hover {
    border-left-color: var(--color-cta);
    box-shadow: var(--shadow-sm);
    transform: translateY(-1px);
}
.evidence-card__header {
    display: flex; align-items: center; gap: 10px; justify-content: space-between;
}
.evidence-card__title {
    font-weight: 600; font-size: 0.9rem; color: var(--color-text);
    text-decoration: none; display: inline-flex; align-items: center;
    gap: 8px; line-height: 1.4; word-break: break-word;
    transition: color var(--duration-fast) var(--ease);
}
.evidence-card__title:hover { color: var(--color-primary); }
.evidence-card__title svg { width: 13px; height: 13px; opacity: 0.4; flex-shrink: 0; }
.evidence-card__index {
    display: inline-flex; align-items: center; justify-content: center;
    width: 20px; height: 20px; border-radius: 50%;
    background: var(--color-primary); color: #fff;
    font-size: 0.66rem; font-weight: 700; flex-shrink: 0;
    box-shadow: 0 1px 3px rgba(99, 102, 241, 0.2);
}
.evidence-card__score {
    display: inline-flex; align-items: center; gap: 4px;
    padding: 3px 10px; font-size: 0.68rem; font-weight: 600;
    color: var(--color-cta-strong);
    background: var(--color-cta-soft);
    border-radius: var(--radius-pill);
    border: 1px solid rgba(16, 185, 129, 0.18);
    white-space: nowrap; flex-shrink: 0; font-variant-numeric: tabular-nums;
}
.evidence-card__snippet {
    font-size: 0.84rem; color: var(--color-text-muted);
    line-height: 1.6; margin: 0;
}

/* ================================================================
   SUGGESTIONS
   ================================================================ */
.suggestions-label {
    display: flex; align-items: center; gap: 8px;
    font-size: 0.7rem; font-weight: 700; color: var(--color-text-subtle);
    text-transform: uppercase; letter-spacing: 0.16em;
    margin: var(--space-6) 0 var(--space-3);
}
.suggestions-label svg { width: 13px; height: 13px; color: var(--color-primary); }

.suggestion-group .stButton > button {
    width: 100%; text-align: left; justify-content: flex-start;
    white-space: normal; line-height: 1.5;
    padding: 11px 16px;
    border-radius: var(--radius-md);
    background: var(--glass-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--color-border);
    color: var(--color-text); font-weight: 500; font-size: 0.88rem;
    box-shadow: var(--shadow-xs);
    cursor: pointer;
    transition: border-color var(--duration-base) var(--ease),
                background var(--duration-base) var(--ease),
                color var(--duration-base) var(--ease),
                box-shadow var(--duration-base) var(--ease),
                transform var(--duration-fast) var(--ease);
}
.suggestion-group .stButton > button:hover {
    border-color: var(--color-primary);
    background: var(--color-primary-soft);
    color: var(--color-primary-strong);
    box-shadow: var(--shadow-sm);
    transform: translateY(-1px);
}
.suggestion-group .stButton > button:focus-visible {
    outline: none;
    box-shadow: var(--shadow-glow);
    border-color: var(--color-primary);
}

/* ================================================================
   SIDEBAR
   ================================================================ */
section[data-testid="stSidebar"] {
    background: var(--color-bg-sidebar);
    border-right: 1px solid var(--color-border);
}
section[data-testid="stSidebar"] .sidebar-section {
    font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.16em;
    font-weight: 700; color: var(--color-text-subtle); margin: 14px 0 6px;
}
section[data-testid="stSidebar"] .sidebar-meta {
    font-size: 0.84rem; color: var(--color-text-muted); line-height: 1.55;
}
section[data-testid="stSidebar"] .sidebar-chip {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 4px 12px; border-radius: var(--radius-pill);
    font-size: 0.72rem; font-weight: 600;
    background: var(--color-bg-card); border: 1px solid var(--color-border);
    color: var(--color-text-muted); box-shadow: var(--shadow-xs);
}
section[data-testid="stSidebar"] .sidebar-chip--live {
    color: #059669; border-color: rgba(16,185,129,0.22); background: rgba(16,185,129,0.06);
}
section[data-testid="stSidebar"] .sidebar-chip--fallback {
    color: #B45309; border-color: rgba(245,158,11,0.22); background: rgba(245,158,11,0.06);
}
section[data-testid="stSidebar"] .stButton > button {
    width: 100%; border-radius: var(--radius-md);
    border: 1px solid var(--color-border);
    background: var(--color-bg-card); color: var(--color-text);
    font-weight: 500; cursor: pointer; box-shadow: var(--shadow-xs);
    transition: border-color var(--duration-base) var(--ease),
                color var(--duration-base) var(--ease);
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
   RESPONSIVE — TABLET  (≤ 768px)
   ================================================================ */
@media (max-width: 768px) {
    :root {
        --radius-sm: 10px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --radius-xl: 20px;
        --message-gap: 14px;
        --typing-dot-size: 6px;
    }

    .block-container {
        max-width: 100%;
        padding-top: 1rem;
        padding-bottom: calc(5rem + env(safe-area-inset-bottom, 0px));
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    /* ── Hero ── */
    .app-hero {
        flex-wrap: wrap;
        gap: var(--space-3);
        padding: var(--space-3) var(--space-4);
        margin: 0 calc(-1 * 1rem) var(--space-4);
        border-radius: var(--radius-md);
    }
    .app-hero__logo { width: 36px; height: 36px; border-radius: var(--radius-sm); }
    .app-hero__logo svg { width: 18px; height: 18px; }
    .app-hero__title { font-size: 1rem; }
    .app-hero__subtitle { font-size: 0.72rem; }
    .app-hero__chip {
        order: 3;
        width: 100%;
        justify-content: center;
        padding: 4px 10px;
        font-size: 0.68rem;
        margin-top: 2px;
    }

    /* ── Welcome ── */
    .welcome { padding: var(--space-3) 0 var(--space-2); }
    .welcome__eyebrow { font-size: 0.65rem; }
    .welcome__headline { font-size: 1.3rem; }
    .welcome__desc { font-size: 0.86rem; max-width: 100%; }
    .welcome__section-label { margin: var(--space-4) 0 var(--space-2); }

    .starter-grid .stButton > button {
        min-height: 64px;
        padding: 12px 14px;
        font-size: 0.84rem;
        border-radius: var(--radius-md);
    }

    /* ── Chat messages ── */
    [data-testid="stChatMessage"] {
        padding: 12px 14px;
        border-radius: var(--radius-md);
    }

    /* ── Chat input ── */
    [data-testid="stChatInput"] {
        border-radius: var(--radius-lg) !important;
    }
    [data-testid="stChatInput"] textarea {
        font-size: 16px !important;
        min-height: 44px !important;
    }
    [data-testid="stBottom"] {
        padding-bottom: env(safe-area-inset-bottom, 0px);
    }

    /* ── Answer cards ── */
    .answer-card {
        padding: 12px 14px;
        margin-bottom: 8px;
        border-radius: 10px;
    }
    .answer-card__header { gap: 6px; margin-bottom: 8px; padding-bottom: 6px; }
    .answer-card__heading { font-size: 0.86rem; }
    .answer-card__body { font-size: 0.82rem; }
    .answer-card__body ol, .answer-card__body ul { padding-left: 18px; }
    .answer-card:hover { transform: none; }

    /* ── Evidence cards ── */
    .evidence-card {
        padding: 12px 14px 12px 14px;
        border-radius: var(--radius-sm);
    }
    .evidence-card:hover { transform: none; }
    .evidence-card__header { flex-wrap: wrap; gap: 8px; }
    .evidence-card__title { font-size: 0.84rem; gap: 6px; }
    .evidence-card__snippet { font-size: 0.8rem; }

    /* ── Suggestions ── */
    .suggestions-label { margin: var(--space-4) 0 var(--space-2); }
    .suggestion-group .stButton > button {
        padding: 10px 14px;
        font-size: 0.84rem;
        min-height: 44px;
    }
    .suggestion-group .stButton > button:hover { transform: none; }

    /* ── Citation badges ── */
    .cite-badge { min-width: 18px; height: 17px; font-size: 0.62rem; }
}

/* ================================================================
   RESPONSIVE — PHONE  (≤ 480px)
   ================================================================ */
@media (max-width: 480px) {
    .block-container {
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
    }

    .app-hero {
        margin-left: -0.75rem;
        margin-right: -0.75rem;
        padding: var(--space-2) var(--space-3);
        border-radius: var(--radius-sm);
    }
    .app-hero__logo { width: 32px; height: 32px; }
    .app-hero__logo svg { width: 16px; height: 16px; }
    .app-hero__title { font-size: 0.92rem; }
    .app-hero__subtitle { font-size: 0.68rem; }

    .welcome__headline { font-size: 1.15rem; line-height: 1.25; }
    .welcome__desc { font-size: 0.82rem; }

    [data-testid="stChatMessage"] { padding: 10px 12px; }

    .answer-card { padding: 10px 12px; }
    .answer-card__header { gap: 6px; margin-bottom: 6px; padding-bottom: 5px; }
    .answer-card__icon { font-size: 0.9rem; }
    .answer-card__heading { font-size: 0.82rem; }
    .answer-card__body { font-size: 0.78rem; line-height: 1.65; }
    .answer-card__body ol, .answer-card__body ul { padding-left: 16px; }
    .answer-card__body li { margin-bottom: 4px; }

    .evidence-card { padding: 10px 12px 10px 12px; }
    .evidence-card__header {
        flex-direction: column;
        align-items: flex-start;
        gap: 6px;
    }
    .evidence-card__title { font-size: 0.8rem; }
    .evidence-card__snippet { font-size: 0.78rem; }
    .evidence-card__score { font-size: 0.64rem; }

    .starter-grid .stButton > button {
        min-height: 56px;
        padding: 10px 12px;
        font-size: 0.82rem;
    }

    .suggestion-group .stButton > button {
        padding: 10px 12px;
        font-size: 0.82rem;
    }
}
</style>
"""


def inject_global_styles() -> None:
    st.markdown(_GLOBAL_CSS, unsafe_allow_html=True)

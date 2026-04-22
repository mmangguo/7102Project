from __future__ import annotations

import streamlit as st

_GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

:root {
    /* AI-Native palette (ui-ux-pro-max recommendation for conversational AI) */
    --color-primary: #7C3AED;
    --color-primary-strong: #6D28D9;
    --color-primary-soft: #F3EEFF;
    --color-cta: #06B6D4;
    --color-cta-strong: #0891B2;
    --color-cta-soft: #ECFEFF;

    --color-bg: #FFFFFF;
    --color-bg-muted: #FAF7FF;
    --color-bg-elevated: #FFFFFF;
    --color-border: #EAE6F0;
    --color-border-strong: #D6D0E0;

    --color-text: #1E1B4B;
    --color-text-muted: #4C5270;
    --color-text-subtle: #8084A1;

    /* AI-Native message bubbles */
    --user-bubble-bg: #E0E7FF;
    --user-bubble-border: #C7D2FE;
    --ai-bubble-bg: #FAFAFB;
    --ai-bubble-border: #EAE6F0;

    --color-success: #10B981;
    --color-warning: #F59E0B;
    --color-danger: #EF4444;

    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;

    --shadow-sm: 0 1px 2px rgba(30, 27, 75, 0.06);
    --shadow-md: 0 4px 14px rgba(30, 27, 75, 0.08);
    --shadow-lg: 0 12px 28px rgba(30, 27, 75, 0.10);

    --space-1: 4px;
    --space-2: 8px;
    --space-3: 12px;
    --space-4: 16px;
    --space-5: 20px;
    --space-6: 24px;

    --message-gap: 16px;
    --typing-dot-size: 8px;
    --input-height: 48px;

    --duration-fast: 120ms;
    --duration-base: 200ms;
    --ease-standard: cubic-bezier(.2,.8,.2,1);
}

@media (prefers-color-scheme: dark) {
    :root {
        --color-primary: #A78BFA;
        --color-primary-strong: #C4B5FD;
        --color-primary-soft: rgba(167, 139, 250, 0.14);
        --color-cta: #22D3EE;
        --color-cta-strong: #67E8F9;
        --color-cta-soft: rgba(34, 211, 238, 0.12);

        --color-bg: #0F0F17;
        --color-bg-muted: #15121F;
        --color-bg-elevated: #1B1830;
        --color-border: #2A2640;
        --color-border-strong: #3A3554;

        --color-text: #EEEBF5;
        --color-text-muted: #B0ADC7;
        --color-text-subtle: #7A7691;

        --user-bubble-bg: rgba(167, 139, 250, 0.14);
        --user-bubble-border: rgba(167, 139, 250, 0.28);
        --ai-bubble-bg: #1B1830;
        --ai-bubble-border: #2A2640;

        --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.4);
        --shadow-md: 0 4px 14px rgba(0, 0, 0, 0.5);
        --shadow-lg: 0 12px 28px rgba(0, 0, 0, 0.6);
    }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

/* Font override — only applied to known text-content containers, NOT to body.
 * This preserves Streamlit's Material Symbols icon glyphs (sidebar toggle,
 * expander chevrons, status icons) which rely on font-family inheritance. */
.block-container,
[data-testid="stSidebar"] > div,
[data-testid="stChatInput"] textarea,
.app-hero,
.welcome,
.evidence-card,
.suggestions-label,
.suggestion-group,
.starter-grid,
.sidebar-meta,
.sidebar-section {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont,
                 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

.block-container {
    max-width: 820px;
    padding-top: 2rem;
    padding-bottom: 6rem;
}

h1, h2, h3 {
    letter-spacing: -0.012em;
    color: var(--color-text);
}

/* ============== Hero / Header (minimal chrome) ============== */

.app-hero {
    display: flex;
    align-items: center;
    gap: var(--space-4);
    padding: var(--space-2) 0 var(--space-4);
    margin-bottom: var(--space-4);
    border-bottom: 1px solid var(--color-border);
}

.app-hero__logo {
    width: 40px;
    height: 40px;
    border-radius: 12px;
    background: linear-gradient(135deg, #7C3AED, #06B6D4);
    color: #fff;
    display: grid;
    place-items: center;
    box-shadow: var(--shadow-md);
    flex-shrink: 0;
}
.app-hero__logo svg {
    width: 22px;
    height: 22px;
}

.app-hero__title-wrap {
    display: flex;
    flex-direction: column;
    gap: 2px;
    min-width: 0;
    flex: 1;
}

.app-hero__title {
    font-size: 1.15rem;
    font-weight: 600;
    color: var(--color-text);
    line-height: 1.2;
    margin: 0;
}

.app-hero__subtitle {
    font-size: 0.82rem;
    color: var(--color-text-muted);
    margin: 0;
}

.app-hero__chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    border: 1px solid var(--color-border);
    background: var(--color-bg-muted);
    color: var(--color-text-muted);
    white-space: nowrap;
}
.app-hero__chip .dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--color-text-subtle);
}
.app-hero__chip--live {
    background: rgba(16, 185, 129, 0.10);
    border-color: rgba(16, 185, 129, 0.28);
    color: var(--color-success);
}
.app-hero__chip--live .dot {
    background: var(--color-success);
    box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.18);
    animation: pulse-dot 1.8s ease-in-out infinite;
}
@keyframes pulse-dot {
    0%, 100% { box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.18); }
    50%      { box-shadow: 0 0 0 5px rgba(16, 185, 129, 0.26); }
}
.app-hero__chip--fallback {
    background: rgba(245, 158, 11, 0.10);
    border-color: rgba(245, 158, 11, 0.28);
    color: var(--color-warning);
}
.app-hero__chip--fallback .dot {
    background: var(--color-warning);
}

/* ============== Welcome / Empty State ============== */

.welcome {
    padding: var(--space-4) 0 var(--space-2);
}
.welcome__eyebrow {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: var(--color-primary);
    font-weight: 700;
    margin-bottom: var(--space-3);
}
.welcome__headline {
    font-size: 1.7rem;
    font-weight: 700;
    color: var(--color-text);
    line-height: 1.2;
    margin: 0 0 var(--space-3);
    letter-spacing: -0.02em;
}
.welcome__desc {
    font-size: 0.95rem;
    color: var(--color-text-muted);
    line-height: 1.6;
    margin: 0 0 var(--space-5);
    max-width: 60ch;
}
.welcome__desc strong {
    color: var(--color-text);
    font-weight: 600;
}
.welcome__section-label {
    font-size: 0.74rem;
    font-weight: 700;
    color: var(--color-text-subtle);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin: var(--space-5) 0 var(--space-2);
}

/* Starter prompt cards */
.starter-grid .stButton > button {
    width: 100%;
    min-height: 92px;
    padding: 14px 16px;
    text-align: left;
    justify-content: flex-start;
    align-items: flex-start;
    white-space: normal;
    line-height: 1.45;
    border-radius: var(--radius-md);
    border: 1px solid var(--color-border);
    background: var(--color-bg-elevated);
    color: var(--color-text);
    font-weight: 500;
    font-size: 0.9rem;
    box-shadow: var(--shadow-sm);
    cursor: pointer;
    transition: border-color var(--duration-base) var(--ease-standard),
                background var(--duration-base) var(--ease-standard),
                box-shadow var(--duration-base) var(--ease-standard);
}
.starter-grid .stButton > button:hover {
    border-color: var(--color-primary);
    background: var(--color-primary-soft);
    box-shadow: var(--shadow-md);
}
.starter-grid .stButton > button:focus-visible {
    outline: 3px solid rgba(124, 58, 237, 0.24);
    outline-offset: 2px;
    border-color: var(--color-primary);
}

/* ============== Chat messages (AI-Native bubbles) ============== */

[data-testid="stChatMessage"] {
    border: 1px solid var(--ai-bubble-border);
    border-radius: var(--radius-md);
    background: var(--ai-bubble-bg);
    padding: 14px 18px;
    margin-bottom: var(--message-gap);
    box-shadow: none;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: var(--user-bubble-bg);
    border-color: var(--user-bubble-border);
}

/* Chat input — AI-Native sticky bottom input */
[data-testid="stChatInput"] {
    border-radius: var(--radius-lg) !important;
    box-shadow: var(--shadow-md);
    border: 1px solid var(--color-border-strong) !important;
    background: var(--color-bg-elevated);
}
[data-testid="stChatInput"] textarea {
    font-size: 0.95rem !important;
    min-height: var(--input-height) !important;
    color: var(--color-text);
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--color-primary) !important;
    box-shadow: 0 0 0 4px rgba(124, 58, 237, 0.12), var(--shadow-md);
}

/* ============== Typing indicator (3-dot pulse, AI-Native signature) ============== */

.typing-indicator {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 0;
}
.typing-indicator__dot {
    width: var(--typing-dot-size);
    height: var(--typing-dot-size);
    border-radius: 50%;
    background: var(--color-primary);
    opacity: 0.35;
    animation: typing-pulse 1.2s ease-in-out infinite;
}
.typing-indicator__dot:nth-child(2) { animation-delay: 0.15s; }
.typing-indicator__dot:nth-child(3) { animation-delay: 0.30s; }
@keyframes typing-pulse {
    0%, 100% { opacity: 0.35; transform: scale(0.85); }
    50%      { opacity: 1;    transform: scale(1);    }
}

/* Streaming cursor */
.stream-cursor {
    display: inline-block;
    width: 2px;
    height: 1em;
    vertical-align: -0.15em;
    margin-left: 2px;
    background: var(--color-primary);
    animation: cursor-blink 1s steps(2) infinite;
}
@keyframes cursor-blink {
    50% { opacity: 0; }
}

/* ============== Citations ============== */

.cite-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 20px;
    height: 18px;
    padding: 0 6px;
    margin: 0 2px;
    border-radius: 999px;
    font-size: 0.68rem;
    font-weight: 700;
    color: #fff;
    background: var(--color-primary);
    vertical-align: baseline;
    line-height: 1;
    letter-spacing: 0.02em;
}

/* Evidence as "context cards" (border-left accent, AI-Native spec) */
.evidence-card {
    display: flex;
    flex-direction: column;
    gap: 6px;
    padding: 12px 14px 12px 16px;
    margin-bottom: 10px;
    border: 1px solid var(--color-border);
    border-left: 3px solid var(--color-primary);
    border-radius: var(--radius-sm);
    background: var(--color-bg-muted);
    transition: border-color var(--duration-base) var(--ease-standard),
                box-shadow var(--duration-base) var(--ease-standard),
                transform var(--duration-fast) var(--ease-standard);
    cursor: default;
}
.evidence-card:hover {
    border-color: var(--color-border-strong);
    border-left-color: var(--color-cta);
    box-shadow: var(--shadow-sm);
}
.evidence-card__header {
    display: flex;
    align-items: center;
    gap: 10px;
    justify-content: space-between;
}
.evidence-card__title {
    font-weight: 600;
    font-size: 0.92rem;
    color: var(--color-text);
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    line-height: 1.4;
    word-break: break-word;
}
.evidence-card__title:hover {
    color: var(--color-primary);
    text-decoration: underline;
}
.evidence-card__title svg {
    width: 14px;
    height: 14px;
    opacity: 0.5;
    flex-shrink: 0;
}
.evidence-card__index {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: var(--color-primary);
    color: #fff;
    font-size: 0.68rem;
    font-weight: 700;
    flex-shrink: 0;
}
.evidence-card__score {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 2px 8px;
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--color-cta-strong);
    background: var(--color-cta-soft);
    border-radius: 999px;
    border: 1px solid rgba(6, 182, 212, 0.22);
    white-space: nowrap;
    flex-shrink: 0;
    font-variant-numeric: tabular-nums;
}
.evidence-card__snippet {
    font-size: 0.85rem;
    color: var(--color-text-muted);
    line-height: 1.55;
    margin: 0;
}

/* ============== Suggestions ============== */

.suggestions-label {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--color-text-subtle);
    text-transform: uppercase;
    letter-spacing: 0.14em;
    margin: var(--space-5) 0 var(--space-2);
}
.suggestions-label svg {
    width: 14px;
    height: 14px;
    color: var(--color-primary);
}

.suggestion-group .stButton > button {
    width: 100%;
    text-align: left;
    justify-content: flex-start;
    white-space: normal;
    line-height: 1.5;
    padding: 10px 14px;
    border-radius: var(--radius-sm);
    background: var(--color-bg-elevated);
    border: 1px solid var(--color-border);
    color: var(--color-text);
    font-weight: 500;
    font-size: 0.9rem;
    box-shadow: none;
    cursor: pointer;
    transition: border-color var(--duration-base) var(--ease-standard),
                background var(--duration-base) var(--ease-standard),
                color var(--duration-base) var(--ease-standard);
}
.suggestion-group .stButton > button:hover {
    border-color: var(--color-primary);
    background: var(--color-primary-soft);
    color: var(--color-primary-strong);
}
.suggestion-group .stButton > button:focus-visible {
    outline: 3px solid rgba(124, 58, 237, 0.24);
    outline-offset: 2px;
    border-color: var(--color-primary);
}

/* ============== Sidebar ============== */

section[data-testid="stSidebar"] {
    background: var(--color-bg-muted);
    border-right: 1px solid var(--color-border);
}
section[data-testid="stSidebar"] .sidebar-section {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    font-weight: 700;
    color: var(--color-text-subtle);
    margin: 12px 0 6px;
}
section[data-testid="stSidebar"] .sidebar-meta {
    font-size: 0.84rem;
    color: var(--color-text-muted);
    line-height: 1.55;
}
section[data-testid="stSidebar"] .sidebar-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    background: var(--color-bg-elevated);
    border: 1px solid var(--color-border);
    color: var(--color-text-muted);
}
section[data-testid="stSidebar"] .sidebar-chip--live {
    color: var(--color-success);
    border-color: rgba(16, 185, 129, 0.30);
    background: rgba(16, 185, 129, 0.08);
}
section[data-testid="stSidebar"] .sidebar-chip--fallback {
    color: var(--color-warning);
    border-color: rgba(245, 158, 11, 0.30);
    background: rgba(245, 158, 11, 0.08);
}

section[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    border-radius: var(--radius-sm);
    border: 1px solid var(--color-border);
    background: var(--color-bg-elevated);
    color: var(--color-text);
    font-weight: 500;
    cursor: pointer;
    transition: border-color var(--duration-base) var(--ease-standard),
                color var(--duration-base) var(--ease-standard),
                background var(--duration-base) var(--ease-standard);
}
section[data-testid="stSidebar"] .stButton > button:hover {
    border-color: var(--color-danger);
    color: var(--color-danger);
    background: rgba(239, 68, 68, 0.06);
}

/* Slider tint */
[data-testid="stSlider"] [role="slider"] {
    background: var(--color-primary) !important;
}

/* ============== Misc ============== */

.stCaption, [data-testid="stCaption"] {
    color: var(--color-text-subtle) !important;
    font-size: 0.8rem !important;
}

[data-testid="stExpander"] summary {
    border-radius: var(--radius-sm);
    cursor: pointer;
}
[data-testid="stExpander"] summary:hover {
    color: var(--color-primary);
}

footer {visibility: hidden;}
#MainMenu {visibility: hidden;}
</style>
"""


def inject_global_styles() -> None:
    st.markdown(_GLOBAL_CSS, unsafe_allow_html=True)

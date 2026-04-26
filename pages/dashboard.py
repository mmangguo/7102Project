import streamlit as st
from PIL import Image
from pathlib import Path
from ui.components.styles import inject_global_styles

st.set_page_config(page_title="Dashboard", page_icon="⚙️", layout="wide")
inject_global_styles()

# Custom CSS for a beautiful dashboard
st.markdown("""
<style>
.section-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: #2563EB;
    margin-top: 1rem;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #E5E7EB;
}
.img-card {
    background-color: #ffffff;
    border-radius: 0.5rem;
    padding: 1rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    margin-bottom: 1rem;
    transition: transform 0.2s ease-in-out;
    border: 1px solid #F3F4F6;
}
.img-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}
.img-caption {
    text-align: center;
    font-weight: 500;
    color: #4B5563;
    margin-top: 0.5rem;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# --- State Initialization ---
if "api_provider" not in st.session_state:
    st.session_state["api_provider"] = "Qwen"
if "top_k" not in st.session_state:
    st.session_state["top_k"] = 5
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "theme_mode" not in st.session_state:
    st.session_state["theme_mode"] = "Light"

def _sync_theme():
    st.session_state["theme_mode"] = st.session_state["theme_selector"]

# --- Theme Handling ---
if st.session_state.get("theme_mode") == "Dark" or st.session_state.get("theme") == "Dark":
    st.markdown("""
    <style>
    /* Dark Mode Overrides */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .section-title {
        color: #60A5FA !important;
        border-bottom-color: #374151 !important;
    }
    .img-card {
        background-color: #1E2127 !important;
        border-color: #374151 !important;
    }
    .img-caption {
        color: #D1D5DB !important;
    }
    div[data-testid="stContainer"] {
        border-color: #374151 !important;
        background-color: #1E2127 !important;
    }
    div[data-testid="stContainer"] h3, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #E5E7EB !important;
    }
    </style>
    """, unsafe_allow_html=True)

def clear_chat():
    st.session_state["messages"] = []
    st.session_state["pending_query"] = None
    st.toast("Chat history cleared!", icon="🧹")

# --- Settings Section ---
st.markdown('<div class="section-title">⚙️ System Settings</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.subheader("🤖 Model Configuration")
        st.markdown("<p style='color: #6B7280; font-size: 0.9rem;'>Select the underlying large language model.</p>", unsafe_allow_html=True)
        st.selectbox(
            "API Provider",
            options=["Qwen", "Kimi", "Gemini", "GPT-4o", "Claude"],
            key="api_provider",
            label_visibility="collapsed"
        )

with col2:
    with st.container(border=True):
        st.subheader("📚 RAG Configuration")
        st.markdown("<p style='color: #6B7280; font-size: 0.9rem;'>Adjust the number of knowledge chunks (Top K).</p>", unsafe_allow_html=True)
        st.slider(
            "Chunk Count",
            min_value=1,
            max_value=10,
            key="top_k",
            label_visibility="collapsed"
        )

with col3:
    with st.container(border=True):
        st.subheader("💬 Session Management")
        st.markdown("<p style='color: #6B7280; font-size: 0.9rem;'>Clear all current chat history and context.</p>", unsafe_allow_html=True)
        st.write("") # spacer to align the button
        st.button("🗑️ Clean Chat", use_container_width=True, type="primary", on_click=clear_chat)

col4, col5 = st.columns(2)

with col4:
    with st.container(border=True):
        st.subheader("📊 Token Usage")
        st.markdown("<p style='color: #6B7280; font-size: 0.9rem;'>Monitor your API token consumption.</p>", unsafe_allow_html=True)
        
        tokens = st.session_state.get("token_usage", {"prompt": 0, "completion": 0, "total": 0})
        if isinstance(tokens, int):
            tokens = {"prompt": 0, "completion": 0, "total": tokens}
            
        m1, m2, m3 = st.columns(3)
        m1.metric("Prompt", tokens.get("prompt", 0))
        m2.metric("Completion", tokens.get("completion", 0))
        m3.metric("Total", tokens.get("total", 0))

with col5:
    with st.container(border=True):
        st.subheader("🌗 Appearance")
        st.markdown("<p style='color: #6B7280; font-size: 0.9rem;'>Toggle between Light and Dark mode.</p>", unsafe_allow_html=True)
        
        st.radio(
            "Theme Selection",
            options=["Light", "Dark"],
            key="theme_selector",
            index=0 if st.session_state.get("theme_mode", "Light") == "Light" else 1,
            on_change=_sync_theme,
            horizontal=True,
            label_visibility="collapsed"
        )


# --- Visualizations Section ---
st.markdown('<div class="section-title">📊 RAG Data Visualizations</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📈 Business News Daily", "🏢 HK Company Registry"])

def render_images(folder_path, limit_to_three=False):
    p = Path(folder_path)
    if not p.exists() or not p.is_dir():
        st.warning(f"Directory not found: {folder_path}")
        return
    
    images = sorted([f for f in p.glob("*.*") if f.suffix.lower() in [".png", ".jpg", ".jpeg"]])
    
    if limit_to_three:
        # Prioritize key visualization images if they exist
        preferred = ["word_cloud.png", "article_title.png", "char_per_chunk.png"]
        selected = [img for img in images if img.name in preferred]
        if len(selected) < 3:
            # fill with other images up to 3
            selected.extend([img for img in images if img not in selected])
        images = selected[:3]
    
    if not images:
        st.info("No images found in this directory.")
        return
        
    # Mapping filenames to readable English descriptions
    IMAGE_CAPTIONS = {
        "word_cloud.png": "Word Cloud Analysis: Most frequent terms",
        "article_title.png": "Article Title Length Distribution",
        "char_per_chunk.png": "Character Count per Chunk Distribution",
        "content_type.png": "Content Type Distribution Analysis",
        "01_url_count_before_after.png": "URL Count Before & After Cleaning",
        "02_precheck_accessibility.png": "Accessibility Pre-check Status",
        "03_http_status_distribution.png": "HTTP Status Code Distribution",
        "04_request_latency_boxplot.png": "Request Latency Analysis Boxplot",
        "05_parsing_success.png": "HTML Parsing Success Rate",
        "06_quality_tier_distribution.png": "Content Quality Tier Distribution",
        "07_clean_text_length_distribution.png": "Cleaned Text Length Distribution",
        "08_chunk_count_per_document.png": "Chunks Count per Document",
        "09_chunk_length_distribution.png": "Chunk Length Distribution",
        "10_incremental_crawl_summary.png": "Incremental Crawl Summary"
    }
        
    cols = st.columns(2)
    for i, img_path in enumerate(images):
        try:
            img = Image.open(img_path)
            # Use predefined caption or fallback to a formatted filename
            caption = IMAGE_CAPTIONS.get(img_path.name, img_path.stem.replace("_", " ").title())
            with cols[i % 2]:
                with st.container(border=True):
                    st.image(img, caption=caption, use_container_width=True)
        except Exception as e:
            st.error(f"Failed to load image {img_path.name}: {e}")

with tab1:
    render_images("data/img/Business_News_Daily", limit_to_three=True)

with tab2:
    render_images("data/img/HK_Company_Registry")

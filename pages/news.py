import newspaper
import random
import streamlit as st
from ui.components.styles import inject_global_styles

st.set_page_config(page_title="Startup News", page_icon="📰", layout="wide")
inject_global_styles()

st.markdown("""
<style>
.page-title {
    font-size: 2rem;
    font-weight: 700;
    background: var(--gradient-brand);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}
.news-card {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: 16px;
    margin-bottom: 20px;
    box-shadow: var(--shadow-sm);
    transition: all 0.25s ease;
    height: 100%;
}
.news-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-md);
    border-color: var(--color-primary-light);
}
.news-title {
    text-decoration: none;
    color: var(--color-text);
    font-weight: 700;
    font-size: 1.1rem;
    display: block;
    margin-bottom: 12px;
    line-height: 1.4;
    transition: color 0.2s ease;
}
.news-title:hover {
    color: var(--color-primary);
}
.news-summary {
    font-size: 0.9rem;
    color: var(--color-text-muted);
    display: -webkit-box;
    -webkit-line-clamp: 4;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
    line-height: 1.6;
}
.news-img {
    width: 100%;
    border-radius: var(--radius-md);
    margin-bottom: 16px;
    object-fit: cover;
    height: 200px;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600, show_spinner="Fetching latest news from tech sites, please wait...")
def fetch_startup_news():
    urls = [
        'https://techcrunch.com/category/startups/',
        'https://review.firstround.com/',
        'https://www.entrepreneur.com/',
        'https://www.ycombinator.com/blog/'
    ]
    news_items = []
    
    for url in urls:
        try:
            # Setting memoize_articles=False ensures we always get the latest list of articles
            paper = newspaper.build(url, memoize_articles=False, language='en')
            articles = paper.articles
            if not articles:
                continue
                
            # Randomly select up to 4 articles per source to parse, to save time
            samples = random.sample(articles, min(4, len(articles)))
            for article in samples:
                try:
                    article.download()
                    article.parse()
                    # We only want articles that successfully parse a title and have an image
                    if article.title and article.top_image:
                        news_items.append({
                            "title": article.title,
                            "link": article.url,
                            "image": article.top_image,
                            "summary": article.meta_description or (article.text[:150] + "...")
                        })
                except Exception:
                    continue
        except Exception:
            continue
            
    # Shuffle to mix sources
    random.shuffle(news_items)
    return news_items

col1, col2 = st.columns([0.8, 0.2])
with col1:
    st.markdown('<div class="page-title">📰 Startup News</div>', unsafe_allow_html=True)
    st.markdown("<p style='color: var(--color-text-muted); font-size: 1.05rem; margin-bottom: 2rem;'>The latest frontier startup dynamics and practical articles (real-time fetch).</p>", unsafe_allow_html=True)
with col2:
    st.write("")
    st.write("")
    if st.button("🔄 Refresh News", use_container_width=True):
        fetch_startup_news.clear()

try:
    news_data = fetch_startup_news()
    
    if not news_data:
        st.info("No news available to display at the moment, possibly due to network issues. Please try again later.")
    else:
        cols = st.columns(3)
        for i, item in enumerate(news_data):
            with cols[i % 3]:
                image_html = f'<img src="{item.get("image", "")}" class="news-img">' if item.get("image") else ""
                st.markdown(
                    f"""
                    <div class="news-card">
                        {image_html}
                        <a href="{item.get('link', '#')}" target="_blank" class="news-title">
                            {item.get('title', 'No Title')}
                        </a>
                        <div class="news-summary">
                            {item.get('summary', 'No Summary')}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
except Exception as e:
    st.error(f"Failed to load news: {e}")

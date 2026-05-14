import streamlit as st
import pickle
import joblib
import pandas as pd
import requests

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root & Background ── */
:root {
    --gold: #E8B86D;
    --gold-dim: #c9973a;
    --red: #E84545;
    --bg: #0A0A0F;
    --surface: #13131A;
    --surface2: #1C1C27;
    --border: rgba(232,184,109,0.15);
    --text: #E8E8F0;
    --muted: #6B6B80;
}

html, body, [class*="css"], .stApp {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif;
}

/* ── Hide Streamlit Boilerplate ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 3rem 3rem 3rem !important; max-width: 1400px !important; }

/* ── Hero Header ── */
.hero {
    text-align: center;
    padding: 3.5rem 0 2rem;
    position: relative;
}
.hero::before {
    content: '';
    position: absolute;
    top: 0; left: 50%; transform: translateX(-50%);
    width: 600px; height: 300px;
    background: radial-gradient(ellipse at center, rgba(232,184,109,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero-eyebrow {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 0.6rem;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(4rem, 10vw, 7rem);
    letter-spacing: 0.08em;
    color: var(--text);
    line-height: 1;
    margin: 0;
}
.hero-title span {
    color: var(--gold);
}
.hero-sub {
    font-size: 0.95rem;
    color: var(--muted);
    margin-top: 0.8rem;
    font-weight: 300;
    letter-spacing: 0.02em;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold-dim), transparent);
    margin: 1.5rem auto 2.5rem;
    max-width: 500px;
    opacity: 0.4;
}

/* ── Search Area ── */
.search-label {
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.5rem;
    text-align: center;
}

/* Selectbox override */
div[data-baseweb="select"] > div {
    background-color: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    transition: border-color 0.2s ease;
}
div[data-baseweb="select"] > div:focus-within {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 2px rgba(232,184,109,0.15) !important;
}
div[data-baseweb="select"] svg { fill: var(--gold) !important; }
[data-baseweb="popover"] { background-color: var(--surface2) !important; border: 1px solid var(--border) !important; }
[role="option"] { color: var(--text) !important; }
[role="option"]:hover { background-color: rgba(232,184,109,0.1) !important; }

/* ── Button ── */
div.stButton > button {
    background: linear-gradient(135deg, var(--gold-dim), var(--gold)) !important;
    color: #0A0A0F !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 0.65rem 2.5rem !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(232,184,109,0.25) !important;
    display: block;
    margin: 0 auto;
}
div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(232,184,109,0.4) !important;
    filter: brightness(1.05) !important;
}
div.stButton > button:active { transform: translateY(0) !important; }

/* ── Results Section ── */
.results-header {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.4rem;
    letter-spacing: 0.15em;
    color: var(--muted);
    text-align: center;
    margin: 2.5rem 0 1.5rem;
}
.results-header span { color: var(--gold); }

/* ── Movie Cards ── */
.movie-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    position: relative;
}
.movie-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 16px 40px rgba(0,0,0,0.5), 0 0 20px rgba(232,184,109,0.1);
    border-color: rgba(232,184,109,0.4);
}
.movie-card img {
    width: 100%;
    border-radius: 0;
    display: block;
}
.movie-card-title {
    padding: 0.75rem 0.85rem 0.85rem;
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--text);
    line-height: 1.3;
    letter-spacing: 0.01em;
}
.rank-badge {
    position: absolute;
    top: 8px; left: 8px;
    background: rgba(10,10,15,0.85);
    border: 1px solid var(--border);
    color: var(--gold);
    font-family: 'Bebas Neue', sans-serif;
    font-size: 0.9rem;
    letter-spacing: 0.1em;
    padding: 2px 8px;
    border-radius: 4px;
    backdrop-filter: blur(4px);
}

/* ── Columns spacing ── */
div[data-testid="column"] { padding: 0 0.4rem !important; }

/* ── Image styling ── */
div[data-testid="stImage"] img {
    border-radius: 0 !important;
    width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

# ─── API & Data ────────────────────────────────────────────────────────────────
API_KEY = "94f735744e1c04428ed9b69e3d71df44"

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Load data
import joblib

# Load data
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

# Load compressed similarity matrix
similarity = joblib.load('similarity.pkl')

# ─── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">✦ Powered by Content-Based Filtering ✦</div>
    <h1 class="hero-title">CINE<span>MATCH</span></h1>
    <p class="hero-sub">Tell us a movie you love — we'll find your next obsession.</p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# ─── Search ───────────────────────────────────────────────────────────────────
col_l, col_center, col_r = st.columns([1, 2, 1])
with col_center:
    st.markdown('<div class="search-label">Select a movie</div>', unsafe_allow_html=True)
    selected_movie_name = st.selectbox(
        label="",
        options=movies['title'].values,
        label_visibility="collapsed"
    )
    st.markdown("<br>", unsafe_allow_html=True)
    recommend_btn = st.button("🎬 Find Matches")

# ─── Results ──────────────────────────────────────────────────────────────────
if recommend_btn:
    with st.spinner("Finding your perfect matches..."):
        names, posters = recommend(selected_movie_name)

    st.markdown(f"""
    <div class="results-header">
        Because you liked <span>{selected_movie_name}</span>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(5)
    ranks = ["01", "02", "03", "04", "05"]

    for idx, col in enumerate(cols):
        with col:
            st.markdown(f"""
            <div class="movie-card">
                <div class="rank-badge">{ranks[idx]}</div>
                <img src="{posters[idx]}" alt="{names[idx]}"/>
                <div class="movie-card-title">{names[idx]}</div>
            </div>
            """, unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; margin-top: 4rem; padding-top: 1.5rem;
     border-top: 1px solid rgba(232,184,109,0.08);
     font-size: 0.72rem; letter-spacing: 0.15em; text-transform: uppercase;
     color: #3a3a4a;">
    CineMatch &nbsp;·&nbsp; Powered by TMDB &nbsp;·&nbsp; Content-Based Recommendations
</div>
""", unsafe_allow_html=True)
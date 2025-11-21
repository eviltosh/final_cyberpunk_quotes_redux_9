import streamlit as st
from pathlib import Path
import base64

# -------------------------------------------------------
# MUST BE FIRST STREAMLIT COMMAND
# -------------------------------------------------------
st.set_page_config(
    page_title="CYBERPUNK QUOTES",
    page_icon="images/cyberpunk.ico",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------------
# REMOVE GITHUB ICON, THREE-DOTS MENU, STREAMLIT BADGES
# AND FORCE DARK MODE ONLY (SAFE FOR APK)
# -------------------------------------------------------
st.markdown("""
<style>

/* Remove Streamlit top-right toolbar (three dots) */
[data-testid="stToolbar"] {
    display: none !important;
}

/* Remove GitHub icon + Streamlit decoration bar */
[data-testid="stDecoration"] {
    display: none !important;
}

/* Remove app header/footer to eliminate Streamlit branding */
header, footer {
    visibility: hidden !important;
    height: 0px !important;
}

/* Force dark mode globally */
:root {
    color-scheme: dark !important;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# RESTORE SIDEBAR IN ANDROID WEBVIEW (RESPONSIVE AND SAFE)
# (Avoid min-width tricks that break mobile layout)
# -------------------------------------------------------
st.markdown("""
<style>
/* Desktop / large tablet: show sidebar as fixed column and push content */
@media (min-width: 900px) {
    [data-testid="stSidebar"] {
        position: fixed !important;
        left: 0;
        top: 0;
        width: 260px !important;
        height: 100vh !important;
        z-index: 1000 !important;
        transform: none !important; /* ensure it's visible */
    }
    [data-testid="stAppViewContainer"] {
        margin-left: 260px !important;
        width: calc(100% - 260px) !important;
        min-width: 0 !important;
    }
    .block-container {
        max-width: calc(100% - 260px) !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }
}

/* Small screens / phones: make sidebar overlay (visible) but do not push content off-screen */
@media (max-width: 899px) {
    [data-testid="stSidebar"] {
        position: fixed !important;
        left: 0;
        top: 0;
        width: 260px !important;
        height: 100vh !important;
        z-index: 1000 !important;
        transform: none !important;
        background: rgba(13,13,13,0.98) !important;
        box-shadow: 0 8px 30px rgba(0,0,0,0.6) !important;
    }
    /* Keep main content full width and allow scrolling under the overlay sidebar */
    [data-testid="stAppViewContainer"] {
        margin-left: 0 !important;
        width: 100% !important;
        min-width: 0 !important;
    }
    .block-container {
        max-width: 100% !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
}

/* General protections so the UI doesn't collapse */
.stApp > div[style] { position: relative; z-index: 1; }
.block-container { box-sizing: border-box; }

/* Ensure charts and video cover correctly and aren't clipped */
video, .plotly, .stPlotlyChart {
    max-width: 100% !important;
    height: auto !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# FORCE DARK MODE (WITHOUT TOUCHING TITLE STYLE)
# -------------------------------------------------------
dark_mode_css = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #0a0a0a !important;
    color: #e0e0e0 !important;
}
section[data-testid="stSidebar"] {
    background-color: #0d0d0d !important;
    color: #e0e0e0 !important;
}

/* Avoid overriding h1 so your title keeps its custom style */
h2, h3, h4, h5, h6, p, span, label {
    color: #e0e0e0 !important;
}

input, textarea, select {
    background-color: #111 !important;
    color: #e0e0e0 !important;
    border: 1px solid #333 !important;
}

.plotly {
    background-color: rgba(0,0,0,0) !important;
}

/* Ensure Streamlit metric colors remain visible */
[data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
    color: #00eaff !important;
    text-shadow: 0 0 6px rgba(0,234,255,0.8);
}
</style>
"""
st.markdown(dark_mode_css, unsafe_allow_html=True)

# -------------------------------------------------------
# SPLASH SCREEN (UNCHANGED)
# -------------------------------------------------------
def splash_screen(image_path: str):
    try:
        img_file = Path(image_path)
        if img_file.exists():
            data = img_file.read_bytes()
            b64 = base64.b64encode(data).decode()
            splash_html = f"""
            <style>
            @keyframes fadeout {{
                0% {{ opacity: 1; }}
                80% {{ opacity: 1; }}
                100% {{ opacity: 0; visibility: hidden; }}
            }}
            #splash-screen {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                background: black;
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 999999999;
                animation: fadeout 2.8s ease-out forwards;
            }}
            </style>
            <div id="splash-screen">
                <img src="data:image/jpeg;base64,{b64}" style="max-width:70vw; max-height:70vh;">
            </div>
            """
            st.markdown(splash_html, unsafe_allow_html=True)
    except:
        pass

# -------------------------------------------------------
# ZERO-WHITE-FLASH FIX (UNCHANGED)
# -------------------------------------------------------
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"], [data-testid="stBody"],
[data-testid="stMain"], .block-container {
    background: black !important;
}
#splash-screen {
    opacity: 1 !important;
    transition: opacity 0.8s ease-out;
}
</style>

<script>
window.addEventListener("load", function() {
    const splash = document.getElementById("splash-screen");
    if (!splash) return;
    const checkReady = setInterval(() => {
        const appRoot = document.querySelector('[data-testid="stApp"]');
        if (appRoot && appRoot.innerHTML.trim().length > 0) {
            clearInterval(checkReady);
            splash.style.opacity = "0";
            setTimeout(() => { splash.style.display = "none"; }, 900);
        }
    }, 50);
});
</script>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# CALL SPLASH AFTER PAGE CONFIG
# -------------------------------------------------------
splash_screen("images/cyberpunk.jpg")

# -------------------------------------------------------
# MAIN APP
# -------------------------------------------------------
def run_app():
    import streamlit.components.v1 as components
    import yfinance as yf
    import requests
    from io import BytesIO
    from PIL import Image
    import datetime
    import time
    import pandas as pd
    import plotly.graph_objects as go

    from app_render import (
        render_company_header,
        render_matplotlib_cyberpunk_chart,
        render_plotly_fallback
    )

    def safe_markdown(html: str):
        st.markdown(html, unsafe_allow_html=True)

    safe_markdown("""
    <style>
    html, body, [data-testid="stBody"], [data-testid="stApp"],
    [data-testid="stAppViewContainer"], [data-testid="stMain"],
    section.main, .block-container { background: transparent !important; }
    .block-container { padding-top: 0rem !important; }
    .stApp > div[style] { position: relative; z-index: 1; }
    </style>
    """)

    safe_markdown("""
    <style>
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"] {
        color: #00eaff !important;
        text-shadow: 0 0 6px rgba(0,234,255,0.8);
    }
    .st-emotion-cache-1wivap2.e14qm3311 {
        text-shadow: none !important;
    }
    .st-emotion-cache-1wivap2.e14qm3311[style*='color: green'] {
        color: green !important;
    }
    .st-emotion-cache-1wivap2.e14qm3311[style*='color: red'] {
        color: red !important;
    }
    </style>
    """)

    css_path = Path("cyberpunk_style_embedded.css")
    if css_path.exists():
        try:
            with css_path.open("r", encoding="utf-8") as fh:
                safe_markdown(f"<style>{fh.read()}</style>")
        except:
            pass
    else:
        safe_markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Major+Mono+Display&display=swap');
        .cyberpunk-title {
            font-family: 'Major Mono Display', monospace;
            font-size:58px;
            color:#00eaff;
            text-align:center;
            letter-spacing:2px;
            text-shadow:0 0 8px rgba(0,234,255,0.9),0 0 18px rgba(0,128,170,0.25);
            position:relative;
            top:-25px;
            margin-bottom:6px;
        }
        .news-card { background: rgba(0,0,0,0.35); padding:8px; border-radius:8px; margin-bottom:8px; }
        .card { background: linear-gradient(180deg, rgba(0,0,0,0.45), rgba(0,0,0,0.25)); border-radius:10px; padding:12px; border:1px solid rgba(0,234,255,0.08); }
        </style>
        """)

    def try_embed_local_video(path: Path) -> bool:
        try:
            if path.exists():
                data = path.read_bytes()
                b64 = base64.b64encode(data).decode()
                safe_markdown(f"""
                <video autoplay muted loop playsinline style="position:fixed;top:0;left:0;width:100vw;height:100vh;object-fit:cover;z-index:-1;">
                    <source src="data:video/mp4;base64,{b64}" type="video/mp4">
                </video>
                """)
                return True
        except:
            pass
        return False

    video_embedded = try_embed_local_video(Path("videos/cyberpunk_light.mp4"))
    if not video_embedded:
        components.html("""
        <video autoplay loop muted playsinline style="position:fixed;top:0;left:0;width:100vw;height:100vh;object-fit:cover;z-index:-1;">
            <source src="https://github.com/eviltosh/final_cyberpunk_quotes_redux_V4/releases/download/v1.0/cyberpunk_light.mp4" type="video/mp4">
        </video>
        """, height=0, width=0)

    # ---------------- Sidebar Controls ----------------
    st.sidebar.header("⚙️ Controls")
    tickers_input = st.sidebar.text_input("Enter stock tickers (comma-separated):", "AAPL, TSLA, NVDA")
    period = st.sidebar.selectbox("Select time range:", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "max"])
    refresh_rate = st.sidebar.slider("Auto-refresh interval (seconds):", 10, 300, 60)

    st.sidebar.subheader("🔑 API Keys")
    finnhub_api = st.sidebar.text_input("Finnhub API key", value="", type="password")

    st.sidebar.subheader("🌅 Chart Background")
    bg_choice = st.sidebar.selectbox("Select Background Image:", ["Beach 1", "Beach 2", "Classic", "Upload Your Own"])
    uploaded_bg = st.sidebar.file_uploader("Upload a background image", type=["jpg", "jpeg", "png"]) if bg_choice == "Upload Your Own" else None

    bg_image = None
    try:
        if uploaded_bg:
            bg_image = Image.open(uploaded_bg)
        elif bg_choice == "Beach 1":
            bg_image = Image.open("images/1.jpg")
        elif bg_choice == "Beach 2":
            bg_image = Image.open("images/2.jpg")
    except:
        bg_image = None

    # ---------------- Title ----------------
    safe_markdown("""
    <br>
    <div style='text-align:center;'>
        <h1 class='cyberpunk-title'>CYBERPUNK QUOTES</h1>
        <br><br>
    </div>
    """)

    # ---------------- Ticker Refresh Logic ----------------
    tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
    if "last_refresh" not in st.session_state:
        st.session_state["last_refresh"] = time.time()
    elif time.time() - st.session_state["last_refresh"] > refresh_rate:
        st.session_state["last_refresh"] = time.time()
        st.rerun()

    @st.cache_data(ttl=3600)
    def get_stock_data(ticker: str, period: str):
        try:
            return yf.Ticker(ticker).history(period=period)
        except:
            return pd.DataFrame()

    @st.cache_data(ttl=3600)
    def get_info_cached(ticker: str):
        try:
            return yf.Ticker(ticker).get_info()
        except:
            return {}

    @st.cache_data(ttl=1800)
    def get_company_news(symbol: str, api_key: str):
        if not api_key:
            return []
        url = "https://finnhub.io/api/v1/company-news"
        today = datetime.date.today()
        past = today - datetime.timedelta(days=30)
        params = {"symbol": symbol, "from": past.isoformat(), "to": today.isoformat(), "token": api_key}
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return [item for item in data if item.get("headline") and item.get("url")]
        except:
            pass
        return []

    # ---------------- Main Ticker Loop ----------------
    for ticker in tickers:
        try:
            info = get_info_cached(ticker)
            hist = get_stock_data(ticker, period)

            if hist is None or hist.empty:
                st.warning(f"No data available for {ticker}")
                continue

            render_company_header(info, ticker)

            rendered = render_matplotlib_cyberpunk_chart(hist, ticker, bg_image)
            if not rendered:
                render_plotly_fallback(hist, ticker)

            # ----- Metrics -----
            row1 = st.columns(2)
            row2 = st.columns(2)

            c_price, c_cap = row1
            c_range, c_change = row2

            price = info.get("currentPrice") or info.get("regularMarketPrice")
            cap = info.get("marketCap")
            high = info.get("fiftyTwoWeekHigh")
            low = info.get("fiftyTwoWeekLow")

            c_price.metric("Current Price", f"${price:,.2f}" if price else "N/A")
            c_cap.metric("Market Cap", f"${cap:,.0f}" if cap else "N/A")
            c_range.metric("52w High / Low", f"${high} / ${low}")

            hist_5d = get_stock_data(ticker, "5d")
            if hist_5d is not None and len(hist_5d) >= 2:
                change = hist_5d["Close"].iloc[-1] - hist_5d["Close"].iloc[-2]
                pct = (change / hist_5d["Close"].iloc[-2]) * 100
                c_change.metric("Daily Change", f"${change:.2f}", f"{pct:.2f}%")

            summary = info.get("longBusinessSummary", "No company description available.")
            if summary.strip():
                with st.expander("📘 Company Info (click to expand)"):
                    st.write(summary)
            else:
                st.info("No company description available.")

            st.markdown("---")

            # ----- News -----
            st.subheader(f"📰 {ticker} Recent News")
            news = get_company_news(ticker, finnhub_api) if finnhub_api else []

            if news:
                for article in news[:5]:
                    dt = datetime.datetime.fromtimestamp(article.get("datetime", 0))
                    t_str = dt.strftime("%b %d, %Y")
                    safe_markdown(
                        f"<div class='news-card'><a href='{article.get('url')}' target='_blank'><b>{article.get('headline')}</b></a><br><small>{article.get('source', 'Unknown')} | {t_str}</small></div>"
                    )
            else:
                if finnhub_api:
                    st.info("No recent news available.")

            safe_markdown("<hr style='border: 1px solid #00f5ff; opacity: 0.3;'>")

        except Exception as e:
            st.error(f"Could not load info for {ticker}: {e}")

    safe_markdown("<hr>")
    safe_markdown("Built with ❤️ — Wizard Q")

# run
if __name__ == "__main__":
    run_app()

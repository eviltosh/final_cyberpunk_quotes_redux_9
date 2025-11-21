import streamlit as st
from pathlib import Path
import base64

# -------------------------------------------------------
# MUST BE FIRST STREAMLIT COMMAND
# -------------------------------------------------------
st.set_page_config(
    page_title="Cyberpunk Stock Tracker",
    page_icon="images/cyberpunk.ico",
    layout="wide"
)
# ✅ PATCH: FORCE DESKTOP MODE IN ANDROID WEBVIEW
st.markdown("""
<head>
<meta name="viewport" content="width=1280, initial-scale=0.85">
</head>
""", unsafe_allow_html=True)

# --- Hide Streamlit's GitHub Icon, Menu, and Footer ---

# ⭐ PATCH 1 — TOOLBAR / GITHUB / 3-DOT REMOVAL
st.markdown("""
<style>

/* REMOVE STREAMLIT MAIN MENU (3 DOTS) */
#MainMenu {visibility: hidden !important; display: none !important;}

/* REMOVE GITHUB ICONS */
a[href*="github"], img[src*="github"] {
    display: none !important;
    visibility: hidden !important;
}

/* REMOVE "FORK THIS APP" TOOLBAR */
[data-testid="stToolbar"] {
    display: none !important;
    visibility: hidden !important;
}

/* REMOVE STREAMLIT HEADER BAR */
header[data-testid="stHeader"] {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
}

/* REMOVE FOOTER BRANDING */
footer, .stFooter {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
}

/* PREVENT LAYOUT SHIFT AFTER REMOVING HEADER */
[data-testid="stAppViewContainer"] {
    margin-top: 0 !important;
    padding-top: 0 !important;
}

</style>
""", unsafe_allow_html=True)

# ⭐ PATCH 2 — FULL DARK MODE (APK-SAFE, NO WHITE FLASH)
st.markdown("""
<style>

/* GLOBAL DARK MODE */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"], [data-testid="stBody"],
[data-testid="stMain"], .block-container {
    background-color: #000 !important;
    color: #e0e0e0 !important;
}

/* SIDEBAR DARK MODE */
section[data-testid="stSidebar"] {
    background-color: #0a0a0a !important;
    color: #e0e0e0 !important;
}

/* INPUT FIELDS */
input, textarea, select {
    background-color: #111 !important;
    color: #e0e0e0 !important;
    border: 1px solid #333 !important;
}

/* WIDGET LABELS */
label, p, span, h2, h3, h4, h5, h6 {
    color: #e0e0e0 !important;
}

/* METRIC TEXT COLORS */
[data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
    color: #00eaff !important;
    text-shadow: 0 0 6px rgba(0,234,255,0.8);
}

/* PLOTLY BACKGROUND */
.plotly, .stPlotlyChart {
    background-color: rgba(0,0,0,0) !important;
}

/* REMOVE ANY LIGHT ELEMENT FLASHES */
* {
    background: transparent !important;
}

</style>
""", unsafe_allow_html=True)

# ⭐ PATCH 3 — SIDEBAR FIX (APK-SAFE + VIDEO-SAFE + DARK-MODE SAFE)
st.markdown("""
<style>

/* --- SIDEBAR MUST ALWAYS SIT ABOVE VIDEO AND CONTENT --- */
[data-testid="stSidebar"] {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 260px !important;
    height: 100vh !important;
    z-index: 999999 !important;
    background: rgba(0,0,0,0.90) !important;
    border-right: 1px solid rgba(0, 234, 255, 0.18);
    overflow-y: auto !important;
}

/* --- SHIFT MAIN APP RIGHT SO NOTHING SITS UNDER THE SIDEBAR --- */
[data-testid="stAppViewContainer"] {
    margin-left: 260px !important;
    padding-left: 1rem !important;
    min-width: calc(100% - 260px) !important;
}

/* --- BLOCK-CONTAINER MUST NOT SLIDE UNDER VIDEO OR SIDEBAR --- */
.block-container {
    padding-top: 1rem !important;
    max-width: calc(100% - 260px) !important;
}

/* --- PREVENT TITLE OR VIDEO FROM OVERLAYING SIDEBAR --- */
video {
    position: relative !important;
    z-index: 1 !important;
}

.stApp {
    overflow: hidden !important;
}

</style>
""", unsafe_allow_html=True)

# ⭐ THE FIX — PATCH 4 (VIDEO RESTORATION + DARK MODE SAFE)
st.markdown("""
<style>

/* --- ENSURE VIDEO BACKGROUND FILLS THE SCREEN --- */
video {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    object-fit: cover !important;
    z-index: -1 !important; /* behind everything */
    pointer-events: none !important; /* sidebar stays clickable */
}

/* --- ENSURE NO WHITE BACKGROUND BEHIND VIDEO --- */
html, body, [data-testid="stAppViewContainer"] {
    background: transparent !important;
}

/* --- BLOCK-CONTAINER MUST BE TRANSPARENT --- */
.block-container {
    background: transparent !important;
}

/* --- ENSURE VIDEO IS NOT SCALED DOWN BY FLEX OR OVERLAYS --- */
[data-testid="stApp"] {
    background: transparent !important;
    overflow: hidden !important;
}

</style>
""", unsafe_allow_html=True)

# ⭐ Patch 5 — LAYOUT NORMALIZATION (the anti–one-column fix)
st.markdown("""
<style>

/* --- RESTORE STREAMLIT DESKTOP LAYOUT EVEN IN MOBILE WEBVIEW --- */
[data-testid="stAppViewContainer"] {
    display: flex !important;
    flex-direction: row !important;
}

/* --- PREVENT COLUMN COLLAPSE --- */
[data-testid="stMain"] {
    flex: 1 1 auto !important;
    width: 100% !important;
}

/* --- FORCE CONTENT TO USE FULL WIDTH --- */
.block-container {
    width: 100% !important;
    max-width: 100% !important;
}

/* --- PREVENT SIDEBAR + VIDEO COLLAPSE BEHAVIOR --- */
.stApp {
    display: block !important;
    overflow-x: hidden !important;
}

/* --- PREVENT BODY OVERFLOW WHICH BREAKS LAYOUT --- */
html, body {
    overflow-x: hidden !important;
}

</style>
""", unsafe_allow_html=True)



# -------------------------------------------------------
# CSS-ONLY SPLASH (SAFE)
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
# ZERO-FLASH FIX — KEEP SPLASH UNTIL STREAMLIT IS READY
# -------------------------------------------------------
st.markdown("""
<style>
/* Force the entire DOM to stay black so Streamlit cannot flash white */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"], [data-testid="stBody"],
[data-testid="stMain"], .block-container {
    background: black !important;
}

/* Hold the splash until JS removes it */
#splash-screen {
    opacity: 1 !important;
    transition: opacity 0.8s ease-out;
}
</style>

<script>
// delay removal until Streamlit fully hydrates
window.addEventListener("load", function() {
    const splash = document.getElementById("splash-screen");
    if (!splash) return;

    // Poll until Streamlit app is rendered
    const checkReady = setInterval(() => {
        // Streamlit attaches stApp after hydration
        const appRoot = document.querySelector('[data-testid="stApp"]');

        if (appRoot && appRoot.innerHTML.trim().length > 0) {
            clearInterval(checkReady);

            // Fade out
            splash.style.opacity = "0";
            setTimeout(() => {
                splash.style.display = "none";
            }, 900);
        }
    }, 50);
});
</script>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# CALL SPLASH **AFTER** page_config
# -------------------------------------------------------
splash_screen("images/cyberpunk.jpg")

# -------------------------------------------------------
# APP ENTRYPOINT
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


    # ------------------------------------------------------------------
    # Import rendering helpers from app_render.py (no circular imports)
    # ------------------------------------------------------------------
    from app_render import (
        render_company_header,
        render_matplotlib_cyberpunk_chart,
        render_plotly_fallback
    )

    # ------------------------------------------------------------------
    # Helper: safe st.markdown wrapper to avoid accidental reassignment
    # ------------------------------------------------------------------
    def safe_markdown(html: str):
        st.markdown(html, unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # TRANSPARENCY + BASIC CSS (applied after page config)
    # ------------------------------------------------------------------
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

    /* Cyan labels + values (keep this) */
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"] {
        color: #00eaff !important;
        text-shadow: 0 0 6px rgba(0, 234, 255, 0.8);
    }

    /* DAILY CHANGE DELTA FIX */
    /* This targets the *actual* delta element you sent */
    .st-emotion-cache-1wivap2.e14qm3311 {
        text-shadow: none !important;
    }

    /* Positive → green */
    .st-emotion-cache-1wivap2.e14qm3311[style*='color: green'],
    .st-emotion-cache-1wivap2.e14qm3311 span[style*='color: green'] {
        color: green !important;
    }

    /* Negative → red */
    .st-emotion-cache-1wivap2.e14qm3311[style*='color: red'],
    .st-emotion-cache-1wivap2.e14qm3311 span[style*='color: red'] {
        color: red !important;
    }

    </style>
    """)

    # ------------------------------------------------------------------
    # Load external cyberpunk CSS if available, otherwise use a minimal fallback
    # ------------------------------------------------------------------
    css_path = Path("cyberpunk_style_embedded.css")
    if css_path.exists():
        try:
            with css_path.open("r", encoding="utf-8") as fh:
                safe_markdown(f"<style>{fh.read()}</style>")
        except Exception:
            # fail silently; fallback provided below
            pass
    else:
        safe_markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Major+Mono+Display&display=swap');
        .cyberpunk-title { font-family: 'Major Mono Display', monospace; font-size:58px; color:#00eaff; text-align:center; letter-spacing:2px; text-shadow:0 0 8px rgba(0,234,255,0.9),0 0 18px rgba(0,128,170,0.25); position:relative; top:-25px; margin-bottom:6px; }
        .news-card { background: rgba(0,0,0,0.35); padding:8px; border-radius:8px; margin-bottom:8px; }
        .card { background: linear-gradient(180deg, rgba(0,0,0,0.45), rgba(0,0,0,0.25)); border-radius:10px; padding:12px; border:1px solid rgba(0,234,255,0.08); }
        </style>
        """)

    # ------------------------------------------------------------------
    # VIDEO BACKGROUND: try local file first, then fallback to GitHub URL
    # ------------------------------------------------------------------
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
        except Exception:
            pass
        return False

    video_embedded = try_embed_local_video(Path("videos/cyberpunk_light.mp4"))
    if not video_embedded:
        # GitHub release fallback; use components.html to avoid large markup inside st.markdown
        components.html("""
        <video autoplay loop muted playsinline style="position:fixed;top:0;left:0;width:100vw;height:100vh;object-fit:cover;z-index:-1;">
            <source src="https://github.com/eviltosh/final_cyberpunk_quotes_redux_V4/releases/download/v1.0/cyberpunk_light.mp4" type="video/mp4">
        </video>
        """, height=0, width=0)

    # ------------------------------------------------------------------
    # Sidebar controls
    # ------------------------------------------------------------------
    st.sidebar.header("⚙️ Controls")
    tickers_input = st.sidebar.text_input("Enter stock tickers (comma-separated):", "AAPL, TSLA, NVDA")
    period = st.sidebar.selectbox("Select time range:", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "max"])
    refresh_rate = st.sidebar.slider("Auto-refresh interval (seconds):", 10, 300, 60)

    st.sidebar.subheader("🔑 API Keys")
    finnhub_api = st.sidebar.text_input("Finnhub API key", value="", type="password")

    st.sidebar.subheader("🌅 Chart Background")
    bg_choice = st.sidebar.selectbox("Select Background Image:", ["Beach 1", "Beach 2", "Classic", "Upload Your Own"])
    uploaded_bg = None
    if bg_choice == "Upload Your Own":
        uploaded_bg = st.sidebar.file_uploader("Upload a background image", type=["jpg", "jpeg", "png"])

    bg_image = None
    if uploaded_bg is not None:
        try:
            from PIL import Image as PILImage
            bg_image = PILImage.open(uploaded_bg)
        except Exception:
            bg_image = None
    else:
        try:
            if bg_choice == "Beach 1":
                bg_image = Image.open("images/1.jpg")
            elif bg_choice == "Beach 2":
                bg_image = Image.open("images/2.jpg")
            else:
                bg_image = None
        except Exception:
            bg_image = None

    # ------------------------------------------------------------------
    # Title (with one extra line above and two below as requested)
    # ------------------------------------------------------------------
    safe_markdown("""
    <br>
    <div style='text-align:center;'>
        <h1 class='cyberpunk-title'>CYBERPUNK QUOTES</h1>
        <br><br>
    </div>
    """)

    # ------------------------------------------------------------------
    # Tickers list and auto-refresh
    # ------------------------------------------------------------------
    tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

    if "last_refresh" not in st.session_state:
        st.session_state["last_refresh"] = time.time()
    else:
        if time.time() - st.session_state["last_refresh"] > refresh_rate:
            st.session_state["last_refresh"] = time.time()
            st.rerun()

    # ------------------------------------------------------------------
    # Cached helpers
    # ------------------------------------------------------------------
    @st.cache_data(ttl=3600)
    def get_stock_data(ticker: str, period: str):
        try:
            return yf.Ticker(ticker).history(period=period)
        except Exception:
            return pd.DataFrame()

    @st.cache_data(ttl=3600)
    def get_info_cached(ticker: str):
        try:
            return yf.Ticker(ticker).get_info()
        except Exception:
            return {}

    @st.cache_data(ttl=1800)
    def get_company_news(symbol: str, api_key: str):
        if not api_key:
            return []
        FINNHUB_NEWS_URL = "https://finnhub.io/api/v1/company-news"
        today = datetime.date.today()
        past = today - datetime.timedelta(days=30)
        params = {"symbol": symbol, "from": past.isoformat(), "to": today.isoformat(), "token": api_key}
        try:
            response = requests.get(FINNHUB_NEWS_URL, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return [item for item in data if item.get("headline") and item.get("url")]
        except Exception:
            pass
        return []

    # ------------------------------------------------------------------
    # Main loop: iterate tickers and render sections
    # ------------------------------------------------------------------
    for ticker in tickers:
        try:
            info = get_info_cached(ticker)
            hist = get_stock_data(ticker, period)

            if hist is None or hist.empty:
                st.warning(f"No data available for {ticker}")
                continue

            # Render company header
            render_company_header(info, ticker)

            # Try matplotlib cyberpunk chart first
            rendered = render_matplotlib_cyberpunk_chart(hist, ticker, bg_image)
            if not rendered:
                render_plotly_fallback(hist, ticker)

            # Metrics row
            # ----------------------------------------------------------
            # METRICS (2 on top row, 2 on bottom row — only change)
            # ----------------------------------------------------------

            # Top row: Price, Market Cap
            row1 = st.columns(2)

            # Bottom row: 52w Range, Daily Change
            row2 = st.columns(2)

            c_price, c_cap = row1[0], row1[1]
            c_range, c_change = row2[0], row2[1]

            price = info.get("currentPrice") or info.get("regularMarketPrice")
            cap = info.get("marketCap")
            high = info.get("fiftyTwoWeekHigh")
            low = info.get("fiftyTwoWeekLow")

            with c_price:
                st.metric("Current Price", f"${price:,.2f}" if price else "N/A")

            with c_cap:
                st.metric("Market Cap", f"${cap:,.0f}" if cap else "N/A")

            with c_range:
                st.metric("52w High / Low", f"${high} / ${low}")

            with c_change:
                hist_5d = get_stock_data(ticker, "5d")
                if hist_5d is not None and len(hist_5d) >= 2:
                    change = (
                            hist_5d["Close"].iloc[-1]
                            - hist_5d["Close"].iloc[-2]
                    )
                    pct = (change / hist_5d["Close"].iloc[-2]) * 100
                    st.metric(
                        "Daily Change",
                        f"${change:.2f}",
                        f"{pct:.2f}%"
                    )

            # Company info
            summary = info.get("longBusinessSummary", "No company description available.")
            if summary and summary.strip():
                with st.expander("📘 Company Info (click to expand)"):
                    st.write(summary)
            else:
                st.info("No company description available.")

            st.markdown("---")

            # News
            st.subheader(f"📰 {ticker} Recent News")
            if not finnhub_api:
                st.info("Enter your Finnhub API key in the sidebar to enable company news.")
                news = []
            else:
                news = get_company_news(ticker, finnhub_api)
            if news:
                for article in news[:5]:
                    dt = datetime.datetime.fromtimestamp(article.get("datetime", 0))
                    t_str = dt.strftime("%b %d, %Y")
                    safe_markdown(
                        f"<div class='news-card'><a href='{article.get('url')}' target='_blank'><b>{article.get('headline')}</b></a><br><small>{article.get('source', 'Unknown')} | {t_str}</small></div>")
            else:
                if finnhub_api:
                    st.info("No recent news available.")

            safe_markdown("<hr style='border: 1px solid #00f5ff; opacity: 0.3;'>")

        except Exception as e:
            st.error(f"Could not load info for {ticker}: {e}")

    # Footer
    safe_markdown("<hr>")
    safe_markdown("Built with ❤️ — Wizard Q")

# run
if __name__ == "__main__":
    run_app()

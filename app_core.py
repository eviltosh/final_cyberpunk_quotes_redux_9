# Path of the original uploaded file (for your tooling / transforms)
ORIGINAL_FILE_PATH = "/mnt/data/app_core.py"

import streamlit as st
from pathlib import Path
import base64

# -------------------------------------------------------
# MUST BE FIRST STREAMLIT COMMAND
# -------------------------------------------------------
st.set_page_config(
    page_title="Cyberpunk Stock Tracker",
    page_icon="images/cyberpunk.ico",
    layout="wide",
)

# -------------------------------------------------------
# Minimal global dark theme (keeps header present)
# -------------------------------------------------------
st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #000 !important;
        color: #EEE !important;
    }
    /* keep header area black but visible (do NOT hide header entirely) */
    header, [data-testid="stToolbar"] { background: #000 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------
# SPLASH (kept but lowered z-index so Android won't permanently block)
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
                z-index: 10000; /* lowered from enormous values */
                animation: fadeout 2.5s ease-out forwards;
            }}
            #splash-screen img {{ max-width:70vw; max-height:70vh; }}
            </style>
            <div id="splash-screen">
                <img src="data:image/jpeg;base64,{b64}">
            </div>
            <script>
            (function() {{
                // Poll until Streamlit fully hydrates and root has content
                const maxTries = 200; // 200 * 50ms = 10s
                let tries = 0;
                const checkReady = setInterval(() => {{
                    tries += 1;
                    const appRoot = document.querySelector('[data-testid="stApp"]');
                    if (appRoot && appRoot.innerHTML && appRoot.innerHTML.trim().length > 80) {{
                        clearInterval(checkReady);
                        const splash = document.getElementById('splash-screen');
                        if (!splash) return;
                        splash.style.opacity = '0';
                        setTimeout(() => {{
                            splash.style.display = 'none';
                        }}, 700);
                    }} else if (tries >= maxTries) {{
                        // give up after a bit — remove splash so it doesn't block
                        clearInterval(checkReady);
                        const splash = document.getElementById('splash-screen');
                        if (splash) {{
                            splash.style.opacity = '0';
                            setTimeout(() => splash.style.display = 'none', 700);
                        }}
                    }}
                }}, 50);
            }})();
            </script>
            """
            st.markdown(splash_html, unsafe_allow_html=True)
    except Exception:
        pass


# call splash immediately (still before main UI)
splash_screen("images/cyberpunk.jpg")

# -------------------------------------------------------
# Centralized APP CSS: keep transparency and ensure video visible behind content
# -------------------------------------------------------
st.markdown(
    """
    <style>
    /* Keep main area transparent so the video shows through */
    html, body, [data-testid="stBody"], [data-testid="stApp"], [data-testid="stAppViewContainer"] {
        background: transparent !important;
    }

    /* Ensure the main block sits above the video */
    .stApp > div[style] { position: relative; z-index: 2; }

    /* Make sure video elements are visible and do not capture pointer events */
    .bgvideo { position: fixed !important; top:0; left:0; width:100vw; height:100vh; object-fit:cover; z-index: -1 !important; pointer-events: none !important; opacity: 1 !important; visibility: visible !important; }

    /* Sidebar chevron: force it visible and above everything */
    [data-testid="collapsedControl"],
    button[title="Toggle sidebar"],
    button[aria-label="Toggle sidebar"] {
        position: fixed !important;
        top: 36px !important;
        right: 12px !important;
        z-index: 300000 !important;
        display: flex !important;
        opacity: 1 !important;
        visibility: visible !important;
        pointer-events: auto !important;
        background: transparent !important;
    }

    /* Metrics cyan styling preserved */
    [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
        color: #00eaff !important;
        text-shadow: 0 0 6px rgba(0,234,255,0.8);
    }

    /* Prevent horizontal scroll */
    html, body { overflow-x: hidden !important; }

    /* Small safety: don't hide header content (we'll hide specific buttons only) */
    header, [data-testid="stToolbar"] { display: block !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------
# APK mode: hide ONLY GitHub / Fork buttons (by title or data-testid)
# but DO NOT hide header or the chevron.
# -------------------------------------------------------
st.markdown(
    """
    <style>
    /* Target titles used by Streamlit toolbar buttons (best-effort selectors) */
    [title="GitHub repository"], /* classic button */
    [title="Fork"], /* fork button */
    [aria-label="GitHub repository"], 
    [data-testid="stToolbarGitHubIcon"] {
        display: none !important;
        pointer-events: none !important;
    }
    /* If a header link element exists that matches 'View streamlit' or similar, do not hide the entire header */
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------
# SINGLE, RELIABLE VIDEO BACKGROUND EMBED
# Put this once. Use a relative path to your videos folder.
# If you prefer to provide an absolute URL or transform local path with your tool,
# modify VIDEO_SRC accordingly.
# -------------------------------------------------------
VIDEO_SRC = "videos/cyberpunk_light.mp4"  # keep relative; your deploy should serve this path

st.markdown(
    f"""
    <div id="video-bg-container" aria-hidden="true">
        <video class="bgvideo" autoplay muted loop playsinline preload="auto" poster="" tabindex="-1">
            <source src="{VIDEO_SRC}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    </div>
    <style>
    /* Ensure container occupies space so browsers won't drop the media */
    #video-bg-container {{ position: fixed; inset:0; width:100%; height:100%; overflow:hidden; z-index: -1; }}
    #video-bg-container video {{ width:100%; height:100%; object-fit:cover; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------
# Main app content (kept largely as in your original file,
# but cleaned for clarity and to avoid conflicts).
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

    # local helpers (you referenced app_render.py — keep imports)
    try:
        from app_render import (
            render_company_header,
            render_matplotlib_cyberpunk_chart,
            render_plotly_fallback,
        )
    except Exception:
        # If app_render isn't available, create minimal fallbacks so app doesn't crash
        def render_company_header(info, ticker):
            name = info.get("longName") or info.get("shortName") or ticker
            st.markdown(f"<h2 style='color:#00eaff;text-shadow:0 0 6px rgba(0,234,255,0.6);'>{name}</h2>", unsafe_allow_html=True)

        def render_matplotlib_cyberpunk_chart(hist, ticker, bg_image):
            # fallback: plot simple st.line_chart
            try:
                st.line_chart(hist["Close"])
            except Exception:
                pass
            return True

        def render_plotly_fallback(hist, ticker):
            st.line_chart(hist["Close"])

    def safe_markdown(html: str):
        st.markdown(html, unsafe_allow_html=True)

    # --- keep basic transparency rules for the inner app
    safe_markdown(
        """
        <style>
        .block-container { padding-top: 0.5rem !important; box-sizing: border-box; }
        html, body { overflow-x: hidden !important; }
        </style>
        """
    )

    # Sidebar (controls)
    st.sidebar.header("⚙️ Controls (APK Mode)")
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
    try:
        if uploaded_bg is not None:
            bg_image = Image.open(uploaded_bg)
        else:
            if bg_choice == "Beach 1":
                bg_image = Image.open("images/1.jpg")
            elif bg_choice == "Beach 2":
                bg_image = Image.open("images/2.jpg")
            else:
                bg_image = None
    except Exception:
        bg_image = None

    # Title
    safe_markdown(
        """
        <div style='text-align:center;'>
            <h1 style="font-family: 'Major Mono Display', monospace; font-size:58px; color:#00eaff; text-shadow:0 0 8px rgba(0,234,255,0.9); margin-bottom:6px;">CYBERPUNK QUOTES</h1>
            <br><br>
        </div>
        """
    )

    # Tickers processing, refresh, caching helpers
    tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

    if "last_refresh" not in st.session_state:
        st.session_state["last_refresh"] = time.time()
    else:
        if time.time() - st.session_state["last_refresh"] > refresh_rate:
            st.session_state["last_refresh"] = time.time()
            st.experimental_rerun()

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

    # Main loop
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

            # Metrics layout
            row1 = st.columns(2)
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
                st.metric("52w High / Low", f"${high} / ${low}" if high and low else "N/A")

            with c_change:
                hist_5d = get_stock_data(ticker, "5d")
                if hist_5d is not None and len(hist_5d) >= 2:
                    change = hist_5d["Close"].iloc[-1] - hist_5d["Close"].iloc[-2]
                    pct = (change / hist_5d["Close"].iloc[-2]) * 100
                    st.metric("Daily Change", f"${change:.2f}", f"{pct:.2f}%")

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
                        f"<div style='background:rgba(0,0,0,0.35); padding:8px; border-radius:8px; margin-bottom:8px;'><a href='{article.get('url')}' target='_blank' rel='noopener noreferrer'><b style='color:#fff'>{article.get('headline')}</b></a><br><small style='color:#ccc'>{article.get('source', 'Unknown')} | {t_str}</small></div>"
                    )
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

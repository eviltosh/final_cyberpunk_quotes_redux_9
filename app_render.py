# app_render.py
# Rendering helpers extracted from original app_core_2.py
import streamlit as st
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt
try:
    import mplcyberpunk
except Exception:
    mplcyberpunk = None
import plotly.graph_objects as go
import requests

def render_company_header(info: dict, ticker: str):
    # safe logo retrieval
    logo_url = info.get("logo_url")
    if not logo_url:
        domain = info.get("website", "").replace("https://", "").replace("http://", "").split("/")[0]
        if domain:
            logo_url = f"https://logo.clearbit.com/{domain}"

    cols = st.columns([1, 4])
    col_logo, col_meta = cols[0], cols[1]
    with col_logo:
        if logo_url:
            try:
                r = requests.get(logo_url, timeout=5)
                if r.status_code == 200:
                    st.image(Image.open(BytesIO(r.content)), width=100)
            except Exception:
                pass
    with col_meta:
        st.markdown(f"### {info.get('shortName', ticker)}")
        st.caption(f"{info.get('sector', 'N/A')} | {info.get('industry', 'N/A')}")

def render_matplotlib_cyberpunk_chart(hist, ticker, bg_image):
    try:
        if mplcyberpunk is not None:
            plt.style.use("cyberpunk")
    except Exception:
        pass
    try:
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_alpha(0)
        ax.set_facecolor('none')
        if bg_image is not None:
            try:
                ax.imshow(bg_image,
                          extent=[hist.index.min(), hist.index.max(), hist['Close'].min(), hist['Close'].max()],
                          aspect='auto', alpha=1.0, zorder=0)
            except Exception:
                pass
        ax.plot(hist.index, hist['Close'], label=ticker, linewidth=2, zorder=2)
        from matplotlib.dates import DateFormatter
        import sys
        if sys.platform.startswith('win'):
            ax.xaxis.set_major_formatter(DateFormatter('%m/%d/%y'))
        else:
            ax.xaxis.set_major_formatter(DateFormatter('%-m/%-d/%y'))
        ax.grid(True, color='white', alpha=0.25)
        ax.set_title(f"{ticker} Stock Price", fontsize=14)
        ax.set_xlabel("Date")
        ax.set_ylabel("Price ($)")
        try:
            if mplcyberpunk is not None:
                mplcyberpunk.add_glow_effects()
        except Exception:
            pass
        st.pyplot(fig)
        return True
    except Exception:
        return False

def render_plotly_fallback(hist, ticker):
    fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist['Close'], mode='lines', name=ticker)])
    fig.update_layout(template='plotly_dark', margin=dict(l=0, r=0, t=30, b=0), height=320,
                      paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    fig.update_xaxes(showgrid=True, gridcolor='rgba(255,255,255,0.3)', zeroline=False, showline=True,
                     linecolor='rgba(255,255,255,0.6)', ticks='outside', tickformat='%m/%d/%y')
    fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.3)', zeroline=False, showline=True,
                     linecolor='rgba(255,255,255,0.6)')
    st.markdown("""
    <style>
    .plotly-graph-div, .js-plotly-plot svg, .js-plotly-plot .svg-container { background: transparent !important; }
    </style>
    """, unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

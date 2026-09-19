# main.py
import os
import base64
import streamlit as st

from app.pages import (
    login_page,
    dashboard_page,
    predictions_page,
    signals_page
)

# ------------------------
# Page config
# ------------------------
st.set_page_config(
    page_title="AI Automated Trading System",
    layout="wide"
)

# ------------------------
# Session defaults
# ------------------------
for key, default in {
    'logged_in': False,
    'username': '',
    'current_page': 'Dashboard',
    'show_splash': True
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ------------------------
# Project paths
# ------------------------
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
LOGO_PATH = os.path.join(ASSETS_DIR, "Logo.jpg")

# ------------------------
# Helper: Base64 logo
# ------------------------
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_base64 = get_base64_image(LOGO_PATH)

# =========================================================
# SPLASH SCREEN (LOGO CENTERED)
# =========================================================
if st.session_state['show_splash']:

    st.markdown(
        """
        <style>
        body {
            background-color: #121212;
        }

        .splash-container {
            height: 70vh;
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            text-align: center;
        }

        .splash-logo {
            width: 450px;
            margin-bottom: 20px;
            transition: transform 0.3s ease;
        }

        .splash-logo:hover {
            transform: scale(1.05);
        }

        div[data-testid="stButton"] {
            display: flex;
            justify-content: center;
        }

        div[data-testid="stButton"] > button {
            background: none;
            border: none;
            color: #aaa;
            font-size: 18px;
            letter-spacing: 1.5px;
            cursor: pointer;
            text-align: center;
        }

        div[data-testid="stButton"] > button:hover {
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="splash-container">
            <img src="data:image/jpg;base64,{logo_base64}" class="splash-logo"/>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if st.button("WELCOME TO AI AUTOMATED TRADING SYSTEM", key="welcome_btn", use_container_width=True):
            st.session_state['show_splash'] = False
            st.rerun()

    st.stop()


# =========================================================
# MAIN APP STYLE (DARK MODE)
# =========================================================
st.markdown(
    """
    <style>
    body, .stApp {
        background-color: #121212;
        color: #e0e0e0;
    }

    div.stButton button {
        border-radius: 12px;
        font-weight: bold;
        padding: 0.8em 0;
        width: 100%;
        transition: all 0.2s ease;
    }

    div.stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.4);
    }

    footer {
        color: #aaa !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------
# Header (Logo centered + Title below)
# ------------------------
st.markdown(
    f"""
    <div style="
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        gap: 15px;
        background: linear-gradient(90deg, #1f4037, #4caf50);
        padding: 20px 30px;
        border-radius: 16px;
        margin-bottom: 20px;
        color: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    ">
        <img src="data:image/jpg;base64,{logo_base64}" style="height:100px; border-radius:12px;">
        <h1 style="margin:0; font-size:34px; font-weight:bold;">AI Automated Trading System</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------------
# Top bar (Greeting + Logout)
# ------------------------
col_left, col_center, col_right = st.columns([2, 6, 2])

with col_left:
    if st.session_state['logged_in']:
        st.markdown(f"### Hello, {st.session_state['username']} 👋")

with col_right:
    if st.session_state['logged_in']:
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = ""
            st.rerun()

# ------------------------
# Login / Registration
# ------------------------
if not st.session_state['logged_in']:
    login_page.render()

else:
    # ------------------------
    # Navigation Tabs
    # ------------------------
    tab_labels = ["Dashboard", "Predictions", "Signals"]
    cols = st.columns(len(tab_labels), gap="small")

    for i, label in enumerate(tab_labels):
        is_active = st.session_state['current_page'] == label
        bg_color = "#4caf50" if is_active else "#333"
        text_color = "#fff" if is_active else "#e0e0e0"

        with cols[i]:
            if st.button(label, key=f"tab_{label}", use_container_width=True):
                st.session_state['current_page'] = label
                st.rerun()

        st.markdown(
            f"""
            <style>
            div.stButton button[key="tab_{label}"] {{
                background-color: {bg_color} !important;
                color: {text_color} !important;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ------------------------
    # Render Pages
    # ------------------------
    if st.session_state['current_page'] == "Dashboard":
        dashboard_page.render()

    elif st.session_state['current_page'] == "Predictions":
        predictions_page.render()

    elif st.session_state['current_page'] == "Signals":
        signals_page.render()

# ------------------------
# Footer
# ------------------------
st.markdown(
    """
    <hr>
    <div style="text-align:center; color:#aaa; font-size:13px; padding:10px 0">
        AI Automated Trading System © 2025<br>
        Graduation Project
    </div>
    """,
    unsafe_allow_html=True
)

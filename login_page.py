# app/pages/login_page.py

import streamlit as st
from controllers.auth_controller import login_user, register_user
import os

def render():
    """
     # Path to logo
        PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
        LOGO_PATH = os.path.join(ASSETS_DIR, "Logo.jpg")

        # Show logo if exists
        if os.path.exists(LOGO_PATH):
            col1, col2, col3 = st.columns([1, 2, 1])  # middle column twice as wide
            with col2:
                st.image(LOGO_PATH, width=200)
        else:
            st.warning("Logo not found in assets folder.")
    """

    st.subheader('🔐 Login / Register')

    col1, col2 = st.columns(2)
    with col1:
        st.write('Login')
        username = st.text_input('Username', key='login_username')
        password = st.text_input('Password', type='password', key='login_password')
        if st.button('Login'):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
            else:
                st.error('Invalid credentials')
    with col2:
        st.write('Register')
        new_u = st.text_input('New Username', key='reg_username')
        new_p = st.text_input('New Password', type='password', key='reg_password')
        if st.button('Register'):
            if register_user(new_u, new_p):
                st.success('Registered successfully — now login')
            else:
                st.error('Registration failed (Username may exist)')

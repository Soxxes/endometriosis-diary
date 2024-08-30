import streamlit as st
from sections.login import login_register
from helpers.auth import check_authentication


if 'login_mode' not in st.session_state:
    st.session_state.login_mode = True
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = ""


login_register()
check_authentication()

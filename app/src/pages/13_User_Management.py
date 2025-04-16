import streamlit as st

API_BASE_URL = "http://web-api:4000"
if not st.session_state.get('authenticated', False) or st.session_state.role != "admin":
    st.warning("Please log in as Alvin to access this page")
    st.stop()

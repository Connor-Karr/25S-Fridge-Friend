import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

# Auth check
if not st.session_state.get('authenticated', False) or st.session_state.role != "athlete":
    st.warning("Please log in as Riley to access this page")
    st.stop()

# Navigation
SideBarLinks(st.session_state.role)

# Page Header
st.title("Athlete Dashboard")
st.subheader("Welcome, Riley!")

# API config
API_BASE_URL = "http://localhost:4000"
CLIENT_ID = st.session_state.get("client_id", 11)

def get_api_data(endpoint, params=None):
    try:
        response = requests.get(f"{API_BASE_URL}/{endpoint}", params=params)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching {endpoint}: Status {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Connection error for {endpoint}: {e}")
        return []

# Tabs
tab1, tab2 = st.tabs(["Macro Tracking", "Meal Plan"])

# === Macro Tracking ===
with tab1:
    st.subheader("📊 Daily Macro Tracking")
    nutrition_logs = get_api_data(f"logs/nutrition/{CLIENT_ID}")

    if nutrition_logs:
        st.dataframe(pd.DataFrame(nutrition_logs[:1]), use_container_width=True)
    else:
        st.info("No nutrition data available.")

    st.subheader("📅 Weekly Macro Trends")
    if nutrition_logs:
        st.dataframe(pd.DataFrame(nutrition_logs[:7]), use_container_width=True)
    else:
        st.info("No weekly macro data found.")

# === Meal Plan ===
with tab2:
    st.subheader("🍽️ Current Meal Plan")
    meals = get_api_data("meal-plans", {"client_id": CLIENT_ID})

    if meals:
        st.dataframe(pd.DataFrame(meals), use_container_width=True)
    else:
        st.info("No meal plan data available.")

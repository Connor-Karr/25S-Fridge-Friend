import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

# Auth check
if not st.session_state.get('authenticated', False) or st.session_state.role != "athlete":
    st.warning("Please log in as Riley to access this page")
    st.stop()

SideBarLinks(st.session_state.role)

st.title("🍽️ Athlete Meal Plans")
st.write("Optimize your nutrition with targeted meal plans for different training phases")

API_BASE_URL = "http://web-api:4000"
CLIENT_ID = st.session_state.get("client_id", 11)  # Default to Riley if missing

# Fetch Data from API
def get_data(endpoint, params=None):
    try:
        res = requests.get(f"{API_BASE_URL}/{endpoint}", params=params)
        if res.status_code == 200:
            return res.json()
        else:
            st.error(f"Failed to fetch {endpoint}: Status {res.status_code}")
            return []
    except Exception as e:
        st.error(f"Error connecting to {endpoint}: {e}")
        return []

meal_plans_data = get_data("meal-plans/", {"client_id": CLIENT_ID})  
leftovers_data = get_data("leftovers", {"client_id": CLIENT_ID})

# Fallback if empty
if not meal_plans_data:
    meal_plans_data = [{
        "meal_name": "Sample Meal",
        "phase": "Maintenance",
        "calories": 400,
        "protein": 25,
        "carbs": 50,
        "fat": 12,
        "servings": 1
    }]

if not leftovers_data:
    leftovers_data = [{
        "name": "Sample Leftover",
        "quantity": 1,
        "expiration_date": "2025-04-20"
    }]

# Tabs
tab1, tab2 = st.tabs(["Current Plans", "Leftovers"])

# Tab 1: Current Plans
with tab1:
    st.subheader("Current Meal Plans")
    st.dataframe(pd.DataFrame(meal_plans_data))

# Tab 2: Leftovers 
with tab2:
    st.subheader("Available Leftovers")
    st.dataframe(pd.DataFrame(leftovers_data))

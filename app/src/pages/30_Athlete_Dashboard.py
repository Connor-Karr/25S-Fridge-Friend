import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

# Authentication check
if not st.session_state.get('authenticated', False) or st.session_state.role != "athlete":
    st.warning("Please log in as Riley to access this page")
    st.stop()

# Set up navigation
SideBarLinks(st.session_state.role)

# Page title
st.title("Athlete Dashboard")
st.subheader("Welcome, Riley!")

# API base URL
API_BASE_URL = "http://web-api:4000"
CLIENT_ID = 11  # Riley's client_id

# --- Reusable API call function ---
def get_api_data(endpoint, params=None):
    try:
        response = requests.get(f"{API_BASE_URL}/{endpoint}", params=params)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching data from {endpoint}: Status code {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error fetching data from {endpoint}: {str(e)}")
        return []

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["Macro Tracking", "Events & Insights", "Recommendations"])

# === Tab 1: Macro Tracking ===
with tab1:
    st.subheader("📊 Daily Macro Tracking")
    nutrition_data = get_api_data(f"logs/nutrition/{CLIENT_ID}")

    if nutrition_data:
        today = nutrition_data[0]
        targets = {
            "Protein (g)": 135,
            "Carbs (g)": 220,
            "Fat (g)": 55,
            "Calories (kcal)": 1900
        }
        consumed = {
            "Protein (g)": today.get("protein", 0),
            "Carbs (g)": today.get("carbs", 0),
            "Fat (g)": today.get("fat", 0),
            "Calories (kcal)": today.get("calories", 0)
        }
        macro_df = pd.DataFrame({"Target": targets, "Consumed": consumed})
        st.dataframe(macro_df, use_container_width=True)
    else:
        st.info("No nutrition data available for today.")

    st.subheader("📅 Weekly Macro Trends")
    weekly_data = nutrition_data[:7] if nutrition_data else []
    if weekly_data:
        week_df = pd.DataFrame(weekly_data)[["tracking_id", "protein", "carbs", "fat"]]
        week_df.columns = ["Day", "Protein (g)", "Carbs (g)", "Fat (g)"]
        st.dataframe(week_df, use_container_width=True)
    else:
        st.info("No weekly macro data available.")

    st.subheader("🏋️ Today's Training")
    workouts = get_api_data("client_workouts", {"client_id": CLIENT_ID})
    if workouts:
        st.dataframe(pd.DataFrame(workouts).head(1), use_container_width=True)
    else:
        st.info("No workout data found.")

    st.subheader("🍽️ Today's Meal Plan")
    meals = get_api_data("meal_plans", {"client_id": CLIENT_ID})
    if meals:
        st.dataframe(pd.DataFrame(meals), use_container_width=True)
    else:
        st.info("No meal plan data found.")

# === Tab 2: Events & Insights ===
with tab2:
    st.subheader("🏆 Upcoming Events")
    st.dataframe(pd.DataFrame({
        "Date": ["2025-05-03", "2025-06-21"],
        "Event": ["Spring Half Marathon", "Mountain Trail 10K"],
        "Distance": ["21.1 km", "10 km"]
    }), use_container_width=True)

    st.subheader("🔍 Nutrition Impact")
    impact_data = get_api_data(f"logs/nutrition/{CLIENT_ID}")
    if impact_data:
        impact_df = pd.DataFrame(impact_data[:14])[["tracking_id", "carbs", "calories"]]
        impact_df.columns = ["Day", "Carb Intake (g)", "Calories"]
        st.dataframe(impact_df, use_container_width=True)
    else:
        st.info("No nutrition impact data available.")

# === Tab 3: Recommendations ===
with tab3:
    st.subheader("🔎 Personalized Recommendations")
    st.dataframe(pd.DataFrame({
        "Recommendation": [
            "Increase pre-workout carbs to 60–80g",
            "Add tart cherry juice post-workout",
            "Hydrate more on cardio days",
            "Stretch for 10 minutes post-lift"
        ]
    }), use_container_width=True)

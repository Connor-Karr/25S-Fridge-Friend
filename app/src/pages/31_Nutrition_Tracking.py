import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
from modules.nav import SideBarLinks
import os

# Base URL defaults to local Flask if environment variable not set
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:4000")

# Auth Check 
if not st.session_state.get('authenticated', False) or st.session_state.role != "athlete":
    st.warning("Please log in as an athlete to access this page")
    st.stop()

SideBarLinks(st.session_state.role)

st.title("Nutrition Tracking")
st.write("Track and analyze your nutrition based on logged intake")

# Identify User 
client_id = st.session_state.get("user_id")
if not client_id:
    st.warning("User ID not found in session.")
    st.stop()

# Fetch Logs 
try:
    response = requests.get(f"{API_BASE_URL}/logs/nutrition/{client_id}")
    response.raise_for_status()
    logs = response.json()
    df = pd.DataFrame(logs)
except Exception as e:
    st.error(f"Failed to fetch nutrition logs: {e}")
    st.stop()

# If empty, initialize columns 
if df.empty:
    st.info("No nutrition tracking data available.")
    df = pd.DataFrame(columns=["date", "protein", "carbs", "fat", "calories", "fiber", "sodium"])

# Normalize columns 
numeric_cols = ["protein", "carbs", "fat", "calories", "fiber", "sodium"]
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

df['date'] = pd.to_datetime(df.get('date', pd.Timestamp.now()))
df = df.sort_values(by='date', ascending=False)

# Log a New Entry 
st.markdown("## Log New Nutrition Entry")
with st.form("log_form"):
    col1, col2, col3 = st.columns(3)
    date_input = col1.date_input("Date", datetime.today())
    protein = col2.number_input("Protein (g)", min_value=0)
    carbs = col3.number_input("Carbs (g)", min_value=0)
    fat = col1.number_input("Fat (g)", min_value=0)
    calories = col2.number_input("Calories", min_value=0)
    fiber = col3.number_input("Fiber (g)", min_value=0)
    sodium = col1.number_input("Sodium (mg)", min_value=0)

    submitted = st.form_submit_button("Add Log")
    if submitted:
        payload = {
            "client_id": client_id,
            "date": str(date_input),
            "protein": protein,
            "carbs": carbs,
            "fat": fat,
            "calories": calories,
            "fiber": fiber,
            "sodium": sodium
        }
        try:
            post_resp = requests.post(f"{API_BASE_URL}/logs/nutrition", json=payload)
            post_resp.raise_for_status()
            st.success("Log added successfully. Refresh to see update.")
        except Exception as e:
            st.error(f"Failed to add log: {e}")

# Most Recent Entry
st.markdown("## Most Recent Entry")
if not df.empty:
    latest = df.iloc[0]
    nutrients = {k: latest[k] for k in numeric_cols}
    nutrient_df = pd.DataFrame.from_dict(nutrients, orient='index', columns=["Consumed"])
    st.dataframe(nutrient_df)

# Log History
st.markdown("## Recent Nutrition Logs")
display_cols = ["date"] + [col for col in numeric_cols if col in df.columns]
st.dataframe(df[display_cols], use_container_width=True)

#  Weekly Summary 
st.markdown("## Weekly Summary (Last 7 Days)")
last_7_days = df[df['date'] >= (datetime.now() - timedelta(days=7))]
if not last_7_days.empty:
    summary = {
        "Avg. Protein": [last_7_days["protein"].mean()],
        "Avg. Carbs": [last_7_days["carbs"].mean()],
        "Avg. Fat": [last_7_days["fat"].mean()],
        "Avg. Calories": [last_7_days["calories"].mean()]
    }
    st.dataframe(pd.DataFrame(summary).round(1))
else:
    st.info("No logs found in the last 7 days.")

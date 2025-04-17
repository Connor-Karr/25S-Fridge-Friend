import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
from modules.nav import SideBarLinks
import os

# Base URL defaults to local Flask if environment variable not set
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:4000")

# --- Authentication check ---
if not st.session_state.get('authenticated', False) or st.session_state.role != "athlete":
    st.warning("Please log in as an athlete to access this page")
    st.stop()

# --- Sidebar ---
SideBarLinks(st.session_state.role)

# --- Page Header ---
st.title("📊 Nutrition Tracking")
st.write("Track and analyze your nutrition based on logged intake")

# --- Identify User ---
client_id = st.session_state.get("user_id")
if not client_id:
    st.warning("User ID not found in session.")
    st.stop()

# --- Fetch Logs ---
try:
    response = requests.get(f"{API_BASE_URL}/logs/nutrition/{client_id}")
    response.raise_for_status()
    logs = response.json()
    df = pd.DataFrame(logs)
except Exception as e:
    st.error(f"Failed to fetch nutrition logs: {e}")
    st.stop()

# --- Process & Clean ---
if df.empty:
    st.info("No nutrition tracking data available.")
    st.stop()

# Convert common fields to numeric (in case they come as strings)
numeric_cols = ["protein", "carbs", "fat", "calories", "fiber", "sodium"]
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Convert and sort by date
df['date'] = pd.to_datetime(df.get('date', pd.Timestamp.now()))
df = df.sort_values(by='date', ascending=False)

# --- Section: Latest Entry ---
st.markdown("## 🔍 Most Recent Entry")
latest = df.iloc[0]
nutrients = {k: latest[k] for k in df.columns if k in numeric_cols}
nutrient_df = pd.DataFrame.from_dict(nutrients, orient='index', columns=["Consumed"])
st.dataframe(nutrient_df)

# --- Section: Log History ---
st.markdown("## 📜 Recent Nutrition Logs")
display_cols = ["date"] + [col for col in numeric_cols if col in df.columns]
st.dataframe(df[display_cols], use_container_width=True)

# --- Section: Weekly Summary ---
st.markdown("## 📈 Weekly Summary (Last 7 Days)")
last_7_days = df[df['date'] >= (datetime.now() - timedelta(days=7))]

if not last_7_days.empty:
    summary = {
        "Avg. Protein": [pd.to_numeric(last_7_days["protein"], errors='coerce').mean()],
        "Avg. Carbs": [last_7_days["carbs"].mean()],
        "Avg. Fat": [last_7_days["fat"].mean()],
        "Avg. Calories": [last_7_days["calories"].mean()]
    }
    st.dataframe(pd.DataFrame(summary).round(1))
else:
    st.info("No logs found in the last 7 days.")
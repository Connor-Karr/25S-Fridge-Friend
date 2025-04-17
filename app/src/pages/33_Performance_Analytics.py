import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime
from modules.nav import SideBarLinks
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:4000")

# Auth check 
if not st.session_state.get('authenticated', False) or st.session_state.role != "athlete":
    st.warning("Please log in as an athlete to access this page")
    st.stop()

SideBarLinks(st.session_state.role)

st.title("📈 Performance Analytics")
st.write("Track your nutrition and macro breakdown over time")

client_id = st.session_state.get("user_id")
if not client_id:
    st.warning("User ID not found.")
    st.stop()

# Fetch logs 
try:
    res = requests.get(f"{API_BASE_URL}/logs/nutrition/{client_id}")
    res.raise_for_status()
    df = pd.DataFrame(res.json())
except Exception as e:
    st.error(f"Error loading nutrition data: {e}")
    st.stop()

if df.empty:
    st.info("No nutrition data available.")
    df = pd.DataFrame(columns=["date", "protein", "carbs", "fat", "calories"])

# Clean data
df["date"] = pd.to_datetime(df.get("date", pd.Timestamp.now()))
for col in ["protein", "carbs", "fat", "calories"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
df.fillna(0, inplace=True)
df = df.sort_values(by="date", ascending=False)

# Add Entry Form (POST only) 
st.markdown("## ✍️ Add Nutrient Log")

with st.form("log_form"):
    entry_date = st.date_input("Date", datetime.today())
    protein = st.number_input("Protein (g)", min_value=0)
    carbs = st.number_input("Carbs (g)", min_value=0)
    fat = st.number_input("Fat (g)", min_value=0)
    calories = st.number_input("Calories", min_value=0)

    submitted = st.form_submit_button("Submit Entry")
    if submitted:
        payload = {
            "client_id": client_id,
            "date": str(entry_date),
            "protein": protein,
            "carbs": carbs,
            "fat": fat,
            "calories": calories
        }

        try:
            r = requests.post(f"{API_BASE_URL}/logs/nutrition", json=payload)
            r.raise_for_status()
            st.success("Log submitted successfully!")
        except Exception as e:
            st.error(f"Error saving data: {e}")

# Tabs for Visualization
tab1, tab2 = st.tabs(["Nutrition Summary", "Performance"])

# Tab 1: Nutrition Summary 
with tab1:
    st.header("Nutrition Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Calories", f"{df['calories'].mean():.0f}")
    col2.metric("Avg Protein", f"{df['protein'].mean():.0f}g")
    col3.metric("Avg Carbs", f"{df['carbs'].mean():.0f}g")

    st.subheader("Calories Over Time")
    st.plotly_chart(px.line(df, x="date", y="calories", markers=True))

    st.subheader("Protein Over Time")
    st.plotly_chart(px.line(df, x="date", y="protein", markers=True))

    st.subheader("Carbs Over Time")
    st.plotly_chart(px.line(df, x="date", y="carbs", markers=True))

    if "fat" in df.columns:
        st.subheader("Fat Over Time")
        st.plotly_chart(px.line(df, x="date", y="fat", markers=True))

# Tab 2: Performance Breakdown 
with tab2:
    st.header("Macro-Driven Performance Insights")

    daily_summary = df.groupby("date").agg({
        "calories": "sum",
        "protein": "sum",
        "carbs": "sum",
        "fat": "sum"
    }).reset_index()

    daily_summary["protein_cal"] = daily_summary["protein"] * 4
    daily_summary["carbs_cal"] = daily_summary["carbs"] * 4
    daily_summary["fat_cal"] = daily_summary["fat"] * 9
    daily_summary["total_macro_cal"] = (
        daily_summary["protein_cal"] +
        daily_summary["carbs_cal"] +
        daily_summary["fat_cal"]
    )

    daily_summary["% Protein"] = (daily_summary["protein_cal"] / daily_summary["total_macro_cal"] * 100).round(1)
    daily_summary["% Carbs"] = (daily_summary["carbs_cal"] / daily_summary["total_macro_cal"] * 100).round(1)
    daily_summary["% Fat"] = (daily_summary["fat_cal"] / daily_summary["total_macro_cal"] * 100).round(1)

    st.subheader("Macro Performance Table (Grouped by Date)")
    display_cols = [
        "date", "calories", "protein", "carbs", "fat",
        "protein_cal", "carbs_cal", "fat_cal",
        "% Protein", "% Carbs", "% Fat"
    ]
    st.dataframe(daily_summary[display_cols].sort_values(by="date", ascending=False), use_container_width=True)

    st.subheader("Macro Breakdown (Most Recent Entry)")
    latest_day = daily_summary.sort_values(by="date", ascending=False).iloc[0]
    if latest_day["total_macro_cal"] > 0:
        st.plotly_chart(
            px.pie(
                names=["Protein", "Carbs", "Fat"],
                values=[
                    latest_day["protein_cal"],
                    latest_day["carbs_cal"],
                    latest_day["fat_cal"]
                ],
                title=f"Macro % Breakdown for {latest_day['date']}"
            )
        )
    else:
        st.info("No valid macro data available for pie chart.")

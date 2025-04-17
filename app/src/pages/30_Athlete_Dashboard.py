import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from modules.nav import SideBarLinks

# Authentication check
if not st.session_state.get('authenticated', False) or st.session_state.role != "athlete":
    st.warning("Please log in as Riley to access this page")
    st.stop()

# Set up navigation
SideBarLinks(st.session_state.role)


# --- Main content area ---
st.title("Athlete Dashboard")
st.subheader("Welcome, Riley!")

tab1, tab2, tab3 = st.tabs(["Macro Tracking", "Events & Insights", "Recommendations"])

with tab1:
    st.subheader("📊 Daily Macro Tracking")
    macros = {
        "Protein (g)": [135, 89],
        "Carbs (g)": [220, 135],
        "Fat (g)": [55, 38],
        "Calories (kcal)": [1900, 1241]
    }
    macro_df = pd.DataFrame(macros, index=["Target", "Consumed"]).T
    st.dataframe(macro_df)

    st.subheader("Weekly Macro Trends")
    days = 7
    dates = [(datetime.now() - timedelta(days=x)).strftime('%a') for x in range(days)]
    dates.reverse()
    np.random.seed(42)
    protein_data = np.clip(np.random.normal(130, 15, days), 90, 160).astype(int)
    carbs_data = np.clip(np.random.normal(210, 25, days), 150, 280).astype(int)
    fat_data = np.clip(np.random.normal(50, 8, days), 35, 70).astype(int)
    macro_data = pd.DataFrame({
        'Day': dates,
        'Protein (g)': protein_data,
        'Carbs (g)': carbs_data,
        'Fat (g)': fat_data
    })
    st.dataframe(macro_data)

    st.subheader("Water & Workout")
    st.write("Water Intake: 1.8L / 3L")
    st.write("Workout Calories: 450 kcal")

    st.subheader("🏋️ Today's Training")
    st.write("Type: Speed Intervals")
    st.write("Duration: 45 minutes")
    st.write("Details: 5 min warmup, 10 x (1 min sprint, 2 min recovery), 5 min cooldown")
    st.write("Focus: Anaerobic Capacity")
    st.write("Nutrition: Pre: Carb-focused snack, Post: Protein shake")

    st.subheader("🍽️ Today's Meal Plan")
    meals = [
        ["Breakfast", "7:00 AM", "Oatmeal with Banana & Protein", "Completed"],
        ["Snack", "10:30 AM", "Protein Bar & Apple", "Completed"],
        ["Lunch", "1:00 PM", "Chicken Bowl with Quinoa & Veggies", "Current"],
        ["Pre-Workout", "4:30 PM", "Rice Cakes with Honey", "Planned"],
        ["Dinner", "7:30 PM", "Salmon, Sweet Potato & Broccoli", "Planned"]
    ]
    st.dataframe(pd.DataFrame(meals, columns=["Meal", "Time", "Description", "Status"]))

with tab2:
    st.subheader("🏆 Upcoming Events")
    races = [
        ["May 3, 2025", "Spring Half Marathon", "21.1 km", "Sub 1:45", "Build"],
        ["June 21, 2025", "Mountain Trail 10K", "10 km", "Top 15 finish", "Peak"],
        ["July 12, 2025", "Independence Day 5K", "5 km", "Sub 20:00", "Race"],
        ["October 9, 2025", "Fall Marathon", "42.2 km", "Sub 3:45", "Base"]
    ]
    today = datetime.now().date()
    days_until = [(datetime.strptime(r[0], "%B %d, %Y").date() - today).days for r in races]
    race_df = pd.DataFrame(races, columns=["Date", "Event", "Distance", "Goal", "Training Phase"])
    race_df["Days Until"] = days_until
    st.dataframe(race_df.sort_values("Days Until"))

    st.subheader("🔍 Nutrition Impact")
    days = 14
    dates = [(datetime.now() - timedelta(days=x)).strftime('%m/%d') for x in range(days)]
    dates.reverse()
    np.random.seed(45)
    carb_intake = np.clip(np.random.normal(210, 40, days), 120, 300).astype(int)
    energy_level = np.clip((carb_intake/300)*10 + np.random.normal(0, 1, days), 1, 10).astype(int)
    impact_df = pd.DataFrame({
        "Date": dates,
        "Carb Intake (g)": carb_intake,
        "Energy Level (1-10)": energy_level
    })
    st.dataframe(impact_df)

    st.write("Insight: Higher carb intake correlates with higher energy levels. Aim for 220g+ carbs on hard days.")

    st.subheader("🔍 Recovery Analysis")
    np.random.seed(46)
    protein_intake = np.clip(np.random.normal(130, 20, days), 90, 170).astype(int)
    recovery_score = np.clip((protein_intake/170)*100 + np.random.normal(0, 10, days), 50, 100).astype(int)
    recovery_df = pd.DataFrame({
        "Date": dates,
        "Protein Intake (g)": protein_intake,
        "Recovery Score (%)": recovery_score
    })
    st.dataframe(recovery_df)
    st.write("Insight: More protein is associated with better recovery. Target 140g+ protein on heavy days.")

with tab3:
    st.subheader("🔎 Personalized Recommendations")
    recs = [
        ["Increase Pre-Workout Carbs", "Nutrition", "Increase carbs to 60-80g in your pre-workout meal for better energy during intervals."],
        ["Improve Recovery with Tart Cherry Juice", "Recovery", "Add 8oz tart cherry juice post-workout to reduce inflammation and improve recovery."],
        ["Adjust Protein Timing", "Nutrition", "Distribute protein evenly (30-40g per meal) instead of consuming most at dinner."]
    ]
    st.dataframe(pd.DataFrame(recs, columns=["Title", "Category", "Description"]))

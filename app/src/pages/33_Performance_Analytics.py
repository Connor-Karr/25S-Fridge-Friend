import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import plotly.express as px
from modules.nav import SideBarLinks
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:4000")

# Auth check 
if not st.session_state.get('authenticated', False) or st.session_state.role != "athlete":
    st.warning("Please log in as an athlete to access this page")
    st.stop()

# Sidebar
SideBarLinks(st.session_state.role)

# Page header
st.title("📈 Performance Analytics")
st.write("Track your workouts and nutrition")

client_id = st.session_state.get("user_id")
if not client_id:
    st.warning("User ID not found.")
    st.stop()

# Load nutrition + workout logs 
try:
    nutri_res = requests.get(f"{API_BASE_URL}/logs/nutrition/{client_id}")
    nutri_res.raise_for_status()
    nutri_df = pd.DataFrame(nutri_res.json())

    workout_res = requests.get(f"{API_BASE_URL}/logs/workouts/{client_id}")
    workout_res.raise_for_status()
    workout_df = pd.DataFrame(workout_res.json())
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Clean/standardize nutrition
if not nutri_df.empty:
    nutri_df['date'] = pd.to_datetime(nutri_df.get('date', pd.Timestamp.now()))
    for col in ['protein', 'carbs', 'fat', 'calories']:
        if col in nutri_df.columns:
            nutri_df[col] = pd.to_numeric(nutri_df[col], errors="coerce")

# Clean/standardize workouts
if not workout_df.empty:
    workout_df['date'] = pd.to_datetime(workout_df.get('date', pd.Timestamp.now()))
    for col in ['distance', 'energy', 'recovery', 'sleep']:
        if col in workout_df.columns:
            workout_df[col] = pd.to_numeric(workout_df[col], errors="coerce")

# Merge data 
df = pd.merge(nutri_df, workout_df, on='date', how='outer').sort_values(by='date', ascending=True)
df.fillna(0, inplace=True)

# Tabs 
tab1, tab2, tab3 = st.tabs(["Workouts", "Nutrition", "Performance"])

# Workouts 
with tab1:
    st.header("Workout Summary")

    if "workout" in df.columns and "distance" in df.columns:
        col1, col2 = st.columns(2)
        with col1:
            total_workouts = len(df[df["workout"].str.lower() != "rest"])
            st.metric("Total Workouts", total_workouts)

        with col2:
            total_distance = df["distance"].sum()
            st.metric("Total Distance", f"{total_distance:.1f} km")

        st.subheader("Workout Types")
        workout_counts = df["workout"].value_counts()
        fig = px.pie(
            values=workout_counts.values,
            names=workout_counts.index,
            title="Workout Distribution"
        )
        st.plotly_chart(fig)

        st.subheader("Running Distance Over Time")
        fig = px.bar(df, x='date', y='distance', color='workout', title="Daily Distance")
        st.plotly_chart(fig)
    else:
        st.info("No workout data available.")

# Nutrition 
with tab2:
    st.header("Nutrition Overview")

    if not nutri_df.empty:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Avg Calories", int(nutri_df["calories"].mean()))
        with col2:
            st.metric("Avg Protein", f"{int(nutri_df['protein'].mean())}g")
        with col3:
            st.metric("Avg Carbs", f"{int(nutri_df['carbs'].mean())}g")

        st.subheader("Daily Calories")
        st.plotly_chart(px.line(df, x='date', y='calories', markers=True, title="Calories"))

        st.subheader("Daily Protein")
        st.plotly_chart(px.line(df, x='date', y='protein', markers=True, title="Protein (g)"))

        st.subheader("Daily Carbs")
        st.plotly_chart(px.line(df, x='date', y='carbs', markers=True, title="Carbs (g)"))
    else:
        st.info("No nutrition data available.")

# Performance 
with tab3:
    st.header("Performance Metrics")

    if 'energy' in df.columns:
        st.subheader("Energy Levels")
        st.plotly_chart(px.line(df, x='date', y='energy', markers=True, title="Daily Energy"))

    if 'recovery' in df.columns:
        st.subheader("Recovery Quality")
        st.plotly_chart(px.line(df, x='date', y='recovery', markers=True, title="Daily Recovery"))

    if 'sleep' in df.columns:
        st.subheader("Sleep Duration")
        st.plotly_chart(px.line(df, x='date', y='sleep', markers=True, title="Sleep (hrs)"))

    if "workout" in df.columns and "energy" in df.columns:
        avg_by_type = df.groupby("workout")["energy"].mean().reset_index()
        st.subheader("Energy by Workout Type")
        st.plotly_chart(px.bar(avg_by_type, x='workout', y='energy', color='workout', title="Energy per Workout Type"))
    else:
        st.info("Insufficient performance data.")
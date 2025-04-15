import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from modules.nav import SideBarLinks

# API base URL
API_BASE_URL = "http://web-api:4000"

# Authentication check
if not st.session_state.get('authenticated', False) or st.session_state.role != "athlete":
    st.warning("Please log in as Riley to access this page")
    st.stop()

# Set up navigation
SideBarLinks(st.session_state.role)

# Page header
st.title(f"Athlete Dashboard")
st.subheader(f"Welcome, {st.session_state.first_name}!")


# Create dashboard layout
col1, col2 = st.columns([2, 1])

# Macro tracking
with col1:
    st.subheader("📊 Daily Macro Tracking")
    
    # Mock data for daily macros
    macros = {
        "targets": {"Protein": 135, "Carbs": 220, "Fat": 55, "Calories": 1900},
        "consumed": {"Protein": 89, "Carbs": 135, "Fat": 38, "Calories": 1241}
    }
    
    # Calculate percentages
    percentages = {
        key: round((macros["consumed"][key] / macros["targets"][key]) * 100, 1) 
        for key in macros["targets"].keys()
    }
    
    # Display progress bars
    for macro, target in macros["targets"].items():
        consumed = macros["consumed"][macro]
        percentage = percentages[macro]
        
        if macro == "Calories":
            macro_label = f"{macro}: {consumed} / {target} kcal ({percentage}%)"
        else:
            macro_label = f"{macro}: {consumed}g / {target}g ({percentage}%)"
        
        if percentage < 50:
            color = "red"
        elif percentage < 80:
            color = "orange"
        elif percentage <= 100:
            color = "green"
        else:
            color = "red"
        
        st.progress(min(percentage/100, 1.0), text=macro_label)
    
    macro_col1, macro_col2 = st.columns(2)
    
    with macro_col1:
        remaining_calories = macros["targets"]["Calories"] - macros["consumed"]["Calories"]
        st.metric("Remaining Calories", f"{remaining_calories} kcal")
        
        protein_calories = macros["consumed"]["Protein"] * 4
        total_calories = macros["consumed"]["Calories"]
        protein_ratio = (protein_calories / total_calories) * 100 if total_calories > 0 else 0
        st.metric("Protein Ratio", f"{protein_ratio:.1f}%", delta="1.2%")
    
    with macro_col2:
        st.metric("Water Intake", "1.8L / 3L", delta="-0.2L", delta_color="inverse")
        st.metric("Workout Calories", "450 kcal", delta="50 kcal")
    
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
    
    fig = px.line(
        macro_data, 
        x='Day', 
        y=['Protein (g)', 'Carbs (g)', 'Fat (g)'],
        markers=True,
        title='Daily Macronutrient Intake'
    )
    
    fig.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis_title="Grams"
    )
    
    st.plotly_chart(fig, use_container_width=True)


# Upcoming workouts and meals
with col2:
    st.subheader("🏋️ Today's Training")
    
    workout = {
        "type": "Speed Intervals",
        "duration": "45 minutes",
        "details": "5 min warmup, 10 x (1 min sprint, 2 min recovery), 5 min cooldown",
        "focus": "Anaerobic Capacity",
        "nutrition": "Pre: Carb-focused snack, Post: Protein shake"
    }
    
    with st.container():
        st.write(f"**Type:** {workout['type']}")
        st.write(f"**Duration:** {workout['duration']}")
        st.write(f"**Details:** {workout['details']}")
        st.write(f"**Focus:** {workout['focus']}")
        st.write(f"**Nutrition Strategy:** {workout['nutrition']}")
        
        if st.button("Log Workout", use_container_width=True):
            with st.spinner("Logging workout..."):
                time.sleep(1)
                st.success("Workout logged successfully!")
    
    st.markdown("---")
    st.subheader("🍽️ Today's Meal Plan")
    
    meals = [
        {"name": "Breakfast", "time": "7:00 AM", "meal": "Oatmeal with Banana & Protein", "status": "Completed"},
        {"name": "Snack", "time": "10:30 AM", "meal": "Protein Bar & Apple", "status": "Completed"},
        {"name": "Lunch", "time": "1:00 PM", "meal": "Chicken Bowl with Quinoa & Veggies", "status": "Current"},
        {"name": "Pre-Workout", "time": "4:30 PM", "meal": "Rice Cakes with Honey", "status": "Planned"},
        {"name": "Dinner", "time": "7:30 PM", "meal": "Salmon, Sweet Potato & Broccoli", "status": "Planned"}
    ]
    
    for meal in meals:
        status_color = "green" if meal["status"] == "Completed" else "orange" if meal["status"] == "Current" else "gray"
        status_icon = "✅" if meal["status"] == "Completed" else "⏳" if meal["status"] == "Current" else "⏱️"
        
        with st.container():
            st.markdown(f"**{meal['name']} ({meal['time']})** {status_icon}")
            st.write(f"{meal['meal']}")
            
            if meal["status"] != "Completed":
                if st.button("Log as Eaten", key=f"log_{meal['name']}", use_container_width=True):
                    with st.spinner("Logging meal..."):
                        time.sleep(1)
                        st.success(f"{meal['name']} logged as eaten!")
                        st.rerun()
            
            st.markdown("---")


# Race/Performance Calendar
st.markdown("---")
st.subheader("🏆 Upcoming Events")

# Mock race data
races = [
    {"date": "May 3, 2025", "name": "Spring Half Marathon", "distance": "21.1 km", "goal": "Sub 1:45", "training_phase": "Build"},
    {"date": "June 21, 2025", "name": "Mountain Trail 10K", "distance": "10 km", "goal": "Top 15 finish", "training_phase": "Peak"},
    {"date": "July 12, 2025", "name": "Independence Day 5K", "distance": "5 km", "goal": "Sub 20:00", "training_phase": "Race"},
    {"date": "October 9, 2025", "name": "Fall Marathon", "distance": "42.2 km", "goal": "Sub 3:45", "training_phase": "Base"}
]

# Calculate days until event
today = datetime.now().date()
for race in races:
    race_date = datetime.strptime(race["date"], "%B %d, %Y").date()
    race["days_until"] = (race_date - today).days

# Sort by days until race
races.sort(key=lambda x: x["days_until"])

# Create race calendar
race_cols = st.columns(len(races))

for i, race in enumerate(races):
    with race_cols[i]:
        # Set color based on proximity
        if race["days_until"] < 14:
            color = "#FFCDD2"  # Light red
        elif race["days_until"] < 30:
            color = "#FFF9C4"  # Light yellow
        else:
            color = "#C8E6C9"  # Light green
        
        # Display race card
        with st.container(border=True):
            st.markdown(f"#### {race['name']}")
            st.write(f"**Date:** {race['date']}")
            st.write(f"**Distance:** {race['distance']}")
            st.write(f"**Goal:** {race['goal']}")
            st.write(f"**Training Phase:** {race['training_phase']}")
            st.write(f"**Days Until:** {race['days_until']}")

# Nutrition and Performance Insights
st.markdown("---")
st.subheader("🔍 Performance Insights")

# Create tabs for different insights
insight_tab1, insight_tab2 = st.tabs(["Nutrition Impact", "Recovery Analysis"])

# Nutrition Impact Tab
with insight_tab1:
    # Mock data for energy level vs. carb intake
    days = 14
    dates = [(datetime.now() - timedelta(days=x)).strftime('%m/%d') for x in range(days)]
    dates.reverse()  # oldest to newest

    np.random.seed(45)
    carb_intake = np.clip(np.random.normal(210, 40, days), 120, 300).astype(int)
    energy_level = np.clip((carb_intake/300)*10 + np.random.normal(0, 1, days), 1, 10).astype(int)

    energy_data = pd.DataFrame({
        'Date': dates,
        'Carb Intake (g)': carb_intake,
        'Energy Level (1-10)': energy_level
    })

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=energy_data['Date'],
        y=energy_data['Carb Intake (g)'],
        name='Carb Intake (g)',
        marker_color='rgba(55, 83, 109, 0.7)'
    ))

    fig.add_trace(go.Scatter(
        x=energy_data['Date'],
        y=energy_data['Energy Level (1-10)'],
        name='Energy Level (1-10)',
        mode='lines+markers',
        marker=dict(color='red'),
        yaxis='y2'
    ))

    fig.update_layout(
        title='Carb Intake vs. Energy Level',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Carb Intake (g)', titlefont=dict(color='rgba(55, 83, 109, 1)'), tickfont=dict(color='rgba(55, 83, 109, 1)')),
        yaxis2=dict(title='Energy Level (1-10)', titlefont=dict(color='red'), tickfont=dict(color='red'), anchor='x', overlaying='y', side='right', range=[0, 11]),
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig, use_container_width=True)

    st.write("""
    **Insight:** Your energy levels show a strong correlation with carbohydrate intake. Days with 240g+ of carbs resulted in 
    energy levels of 8 or higher, while days below 180g of carbs averaged energy levels of 5-6. Consider maintaining carb 
    intake above 220g on hard training days.
    """)

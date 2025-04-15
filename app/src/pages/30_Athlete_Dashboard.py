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

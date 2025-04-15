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
if not st.session_state.get('authenticated', False) or st.session_state.role != "nutritionist":
    st.warning("Please log in as Nancy to access this page")
    st.stop()

# Set up navigation
SideBarLinks(st.session_state.role)

# Page header
st.title(f"Nutritionist Dashboard")
st.subheader(f"Welcome, {st.session_state.first_name}!")


# Mock client data
clients = [
    {"id": 1, "name": "John D.", "age": 27, "goal": "Weight Loss", "diet": "Low Carb", "allergies": "Peanuts"},
    {"id": 2, "name": "Sarah M.", "age": 34, "goal": "Muscle Gain", "diet": "High Protein", "allergies": "Dairy"},
    {"id": 3, "name": "Michael R.", "age": 42, "goal": "Maintenance", "diet": "Balanced", "allergies": "None"},
    {"id": 4, "name": "Emma L.", "age": 19, "goal": "Performance", "diet": "Keto", "allergies": "Gluten"},
    {"id": 5, "name": "David W.", "age": 55, "goal": "Health", "diet": "Mediterranean", "allergies": "Shellfish"}
]

# Create dashboard layout
col1, col2 = st.columns([2, 1])

# Client overview section
with col1:
    st.subheader("👥 Active Clients")

    for client in clients:
        with st.container():
            col_a, col_b, col_c, col_d, col_e = st.columns([3, 2, 2, 2, 1])

            with col_a:
                st.write(f"**{client['name']}**")
            with col_b:
                st.write(f"Age: {client['age']}")
            with col_c:
                st.write(f"Goal: {client['goal']}")
            with col_d:
                st.write(f"Diet: {client['diet']}")
            with col_e:
                if st.button("View", key=f"view_{client['id']}"):
                    st.session_state.selected_client_id = client['id']
                    st.session_state.selected_client_name = client['name']
                    st.switch_page("pages/21_Client_Management.py")

            st.write("---")

    if st.button("+ Add New Client"):
        st.switch_page("pages/21_Client_Management.py")


# Today's agenda section
with col2:
    st.subheader("📅 Today's Agenda")

    # Mock appointments
    appointments = [
        {"time": "9:00 AM", "client": "John D.", "type": "Check-in"},
        {"time": "11:30 AM", "client": "Emma L.", "type": "Meal Plan Review"},
        {"time": "2:00 PM", "client": "Sarah M.", "type": "Initial Consultation"},
        {"time": "4:30 PM", "client": "Michael R.", "type": "Progress Review"}
    ]

    for appt in appointments:
        st.info(f"**{appt['time']}** - {appt['client']} ({appt['type']})")

# Client analytics section
st.markdown("---")
st.subheader("📊 Client Analytics")

# Create tabs for different analytics
tab1, tab2 = st.tabs(["Nutrition Distribution", "Goal Progress"])

# Nutrition Distribution Tab
with tab1:
    macros = {
        "Weight Loss": {"Protein": 35, "Carbs": 25, "Fat": 40},
        "Muscle Gain": {"Protein": 40, "Carbs": 40, "Fat": 20},
        "Maintenance": {"Protein": 30, "Carbs": 40, "Fat": 30},
        "Performance": {"Protein": 25, "Carbs": 55, "Fat": 20},
        "Health": {"Protein": 25, "Carbs": 45, "Fat": 30}
    }

    selected_goal = st.selectbox("Select dietary goal:", list(macros.keys()))
    selected_macros = macros[selected_goal]

    macro_df = pd.DataFrame({
        'Macronutrient': list(selected_macros.keys()),
        'Percentage': list(selected_macros.values())
    })

    fig = px.pie(
        macro_df,
        values='Percentage',
        names='Macronutrient',
        title=f"Average Macronutrient Distribution for {selected_goal} Clients",
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Recommended Foods")

    recommended_foods = {
        "Weight Loss": ["Lean Chicken", "Leafy Greens", "Greek Yogurt", "Berries", "Eggs"],
        "Muscle Gain": ["Chicken Breast", "Lean Beef", "Salmon", "Quinoa", "Sweet Potatoes"],
        "Maintenance": ["Avocados", "Mixed Nuts", "Brown Rice", "Whole Grains", "Fish"],
        "Performance": ["Oats", "Bananas", "Rice", "Potatoes", "Lean Meats"],
        "Health": ["Olive Oil", "Nuts", "Leafy Greens", "Fish", "Whole Grains"]
    }

    foods = recommended_foods.get(selected_goal, [])
    food_cols = st.columns(len(foods))

    for i, food in enumerate(foods):
        with food_cols[i]:
            st.write(f"**{food}**")


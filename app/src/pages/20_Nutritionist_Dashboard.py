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


# Goal Progress Tab
with tab2:
    # Mock data for goal progress over time
    dates = [(datetime.now() - timedelta(days=x*7)).strftime('%Y-%m-%d') for x in range(8)]
    dates.reverse()

    weight_loss_progress = [0, 12, 23, 35, 48, 57, 68, 75]
    muscle_gain_progress = [0, 15, 28, 42, 55, 62, 70, 78]
    maintenance_progress = [0, 10, 25, 40, 50, 60, 72, 85]
    performance_progress = [0, 18, 30, 45, 58, 65, 75, 82]
    health_progress = [0, 8, 20, 32, 45, 58, 68, 80]

    progress_df = pd.DataFrame({
        'Date': dates,
        'Weight Loss': weight_loss_progress,
        'Muscle Gain': muscle_gain_progress,
        'Maintenance': maintenance_progress,
        'Performance': performance_progress,
        'Health': health_progress
    })

    fig = px.line(
        progress_df,
        x='Date',
        y=['Weight Loss', 'Muscle Gain', 'Maintenance', 'Performance', 'Health'],
        title='Client Goal Progress Over Time (% Completion)',
        markers=True
    )

    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        yaxis_title="Progress (%)"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Client count by goal
    st.subheader("Client Distribution by Goal")

    goal_counts = {
        'Weight Loss': 12,
        'Muscle Gain': 8,
        'Maintenance': 5,
        'Performance': 7,
        'Health': 9
    }

    goal_df = pd.DataFrame({
        'Goal': list(goal_counts.keys()),
        'Clients': list(goal_counts.values())
    })

    fig = px.bar(
        goal_df,
        x='Goal',
        y='Clients',
        title='Number of Clients by Goal',
        color='Goal',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)

# Dietary Alerts section
st.markdown("---")
st.subheader("⚠️ Dietary Alerts")

alerts = [
    {"client": "John D.", "alert": "High sodium intake detected in last 3 days", "priority": "Medium"},
    {"client": "Emma L.", "alert": "Consistent low protein intake (below 15% target)", "priority": "High"},
    {"client": "Michael R.", "alert": "Possible food allergy reaction - review food diary", "priority": "High"},
    {"client": "David W.", "alert": "Missing dinner logs for past 2 days", "priority": "Low"}
]

for alert in alerts:
    if alert["priority"] == "High":
        st.error(f"**{alert['client']}:** {alert['alert']} (Priority: {alert['priority']})")
    elif alert["priority"] == "Medium":
        st.warning(f"**{alert['client']}:** {alert['alert']} (Priority: {alert['priority']})")
    else:
        st.info(f"**{alert['client']}:** {alert['alert']} (Priority: {alert['priority']})")

# Quick actions section
st.markdown("---")
st.subheader("⚡ Quick Actions")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Create Meal Plan", use_container_width=True):
        st.switch_page("pages/22_Meal_Planning.py")

with col2:
    if st.button("Generate Nutrition Report", use_container_width=True):
        with st.spinner("Generating report..."):
            time.sleep(2)
            st.success("Report generated successfully!")
            st.download_button(
                label="Download Report",
                data="This is a sample nutrition report for clients.",
                file_name="nutrition_report.txt",
                mime="text/plain"
            )

with col3:
    if st.button("Schedule Check-in", use_container_width=True):
        st.info("Redirecting to scheduling page...")
        time.sleep(1)
        st.success("Check-in scheduled successfully!")

with col4:
    if st.button("View Analytics", use_container_width=True):
        st.switch_page("pages/23_Nutrition_Analytics.py")

# Recent activities
st.markdown("---")
st.subheader("🔄 Recent Activities")

activities = [
    {"time": "10:23 AM", "activity": "Created new meal plan for Emma L."},
    {"time": "Yesterday", "activity": "Updated dietary restrictions for John D."},
    {"time": "Yesterday", "activity": "Added new client: David W."},
    {"time": "2 days ago", "activity": "Generated nutrition report for Sarah M."},
    {"time": "2 days ago", "activity": "Updated macronutrient goals for Michael R."}
]

for activity in activities:
    st.write(f"**{activity['time']}:** {activity['activity']}")





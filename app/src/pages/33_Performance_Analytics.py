import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px

# Page header
st.title("📈 Performance Analytics")
st.write("Track your workouts and nutrition")

# Create simple sample data
def create_sample_data():
    # Create 30 days of data
    dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30, 0, -1)]
    
    # Create simple workout data
    workouts = ["Easy Run", "Tempo Run", "Long Run", "Rest"]
    workout_types = [np.random.choice(workouts) for _ in dates]
    
    # Distance depends on workout type
    distances = []
    for workout in workout_types:
        if workout == "Long Run":
            distances.append(round(np.random.uniform(8, 12), 1))
        elif workout == "Tempo Run":
            distances.append(round(np.random.uniform(5, 7), 1))
        elif workout == "Easy Run":
            distances.append(round(np.random.uniform(3, 5), 1))
        else:  # Rest
            distances.append(0)
    
    # Simple nutrition and performance data
    data = pd.DataFrame({
        'Date': dates,
        'Workout': workout_types,
        'Distance': distances,
        'Calories': [round(np.random.uniform(1800, 2500)) for _ in dates],
        'Protein': [round(np.random.uniform(80, 150)) for _ in dates],
        'Carbs': [round(np.random.uniform(150, 300)) for _ in dates],
        'Energy': [round(np.random.uniform(3, 9), 1) for _ in dates],
        'Recovery': [round(np.random.uniform(4, 9), 1) for _ in dates],
        'Sleep': [round(np.random.uniform(5, 9), 1) for _ in dates]
    })
    
    return data

# Get data
data = create_sample_data()

# Create tabs
tab1, tab2, tab3 = st.tabs(["Workouts", "Nutrition", "Performance"])

# Tab 1: Workouts
with tab1:
    st.header("Workout Summary")
    
    # Show total workouts and distance
    col1, col2 = st.columns(2)
    
    with col1:
        total_workouts = len(data[data['Workout'] != 'Rest'])
        st.metric("Total Workouts", total_workouts)
    
    with col2:
        total_distance = data['Distance'].sum()
        st.metric("Total Distance", f"{total_distance:.1f} miles")
    
    # Show workout types
    st.subheader("Workout Types")
    workout_counts = data['Workout'].value_counts()
    
    fig = px.pie(
        values=workout_counts.values,
        names=workout_counts.index,
        title="Workout Distribution"
    )
    
    st.plotly_chart(fig)
    
    # Show distance chart
    st.subheader("Running Distance")
    fig = px.bar(
        data,
        x='Date',
        y='Distance',
        color='Workout',
        title="Daily Distance"
    )
    
    st.plotly_chart(fig)

# Tab 2: Nutrition
with tab2:
    st.header("Nutrition Overview")

    # Show average nutrition
    avg_calories = int(data['Calories'].mean())
    avg_protein = int(data['Protein'].mean())
    
    st.metric("Average Daily Calories", avg_calories)
    st.metric("Average Daily Protein", f"{avg_protein}g")

    # Show nutrition chart
    st.subheader("Nutrition Tracking")
    nutrient = st.radio(
        "Select nutrient:",
        ["Calories", "Protein", "Carbs"]
    )

    fig = px.line(
        data,
        x='Date',
        y=nutrient,
        markers=True,
        title=f"Daily {nutrient}"
    )
    st.plotly_chart(fig)

# Tab 3: Performance
with tab3:
    st.header("Performance Metrics")
    
    # Show performance chart
    st.subheader("Performance Over Time")
    metric = st.radio(
        "Select metric:",
        ["Energy", "Recovery", "Sleep"]
    )
    
    fig = px.line(
        data,
        x='Date',
        y=metric,
        markers=True,
        title=f"Daily {metric} Levels"
    )
    st.plotly_chart(fig)
    
    # Show performance by workout
    st.subheader("Performance by Workout Type")
    avg_by_workout = data.groupby('Workout')[metric].mean().reset_index()
    
    fig = px.bar(
        avg_by_workout,
        x='Workout',
        y=metric,
        color='Workout',
        title=f"{metric} Levels by Workout Type"
    )
    st.plotly_chart(fig)
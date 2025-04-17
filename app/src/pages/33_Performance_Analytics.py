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
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_calories = int(data['Calories'].mean())
        st.metric("Average Daily Calories", avg_calories)
    
    with col2:
        avg_protein = int(data['Protein'].mean())
        st.metric("Average Daily Protein", f"{avg_protein}g")
        
    with col3:
        avg_carbs = int(data['Carbs'].mean())
        st.metric("Average Daily Carbs", f"{avg_carbs}g")

    # Show nutrition charts - one for each metric instead of using radio buttons
    st.subheader("Daily Calories")
    calories_fig = px.line(
        data,
        x='Date',
        y='Calories',
        markers=True,
        title="Daily Calories"
    )
    st.plotly_chart(calories_fig)
    
    st.subheader("Daily Protein")
    protein_fig = px.line(
        data,
        x='Date',
        y='Protein',
        markers=True,
        title="Daily Protein (g)"
    )
    st.plotly_chart(protein_fig)
    
    st.subheader("Daily Carbs")
    carbs_fig = px.line(
        data,
        x='Date',
        y='Carbs',
        markers=True,
        title="Daily Carbs (g)"
    )
    st.plotly_chart(carbs_fig)

# Tab 3: Performance
with tab3:
    st.header("Performance Metrics")
    
    # Show all performance metrics instead of using radio buttons
    st.subheader("Energy Levels")
    energy_fig = px.line(
        data,
        x='Date',
        y='Energy',
        markers=True,
        title="Daily Energy Levels"
    )
    st.plotly_chart(energy_fig)
    
    st.subheader("Recovery Quality")
    recovery_fig = px.line(
        data,
        x='Date',
        y='Recovery',
        markers=True,
        title="Daily Recovery Quality"
    )
    st.plotly_chart(recovery_fig)
    
    st.subheader("Sleep Quality")
    sleep_fig = px.line(
        data,
        x='Date',
        y='Sleep',
        markers=True,
        title="Daily Sleep Quality"
    )
    st.plotly_chart(sleep_fig)
    
    # Show one performance by workout type chart for Energy
    st.subheader("Energy by Workout Type")
    avg_by_workout = data.groupby('Workout')['Energy'].mean().reset_index()
    
    workout_fig = px.bar(
        avg_by_workout,
        x='Workout',
        y='Energy',
        color='Workout',
        title="Energy Levels by Workout Type"
    )
    st.plotly_chart(workout_fig)
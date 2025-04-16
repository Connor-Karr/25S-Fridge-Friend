mport streamlit as st
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
st.title("📈 Performance Analytics")
st.write("Analyze the relationship between your nutrition and athletic performance")

# Mock workout data (in a real app, this would come from an API)
@st.cache_data(ttl=600)
def generate_mock_workout_data(days=60):
    np.random.seed(42)
    
    # Generate dates
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days-1)
    dates = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days)]
    
    # Generate workout types with some patterns
    workout_types = []
    for i in range(days):
        day_of_week = (start_date + timedelta(days=i)).weekday()
        
        if day_of_week == 0:  # Monday
            workout_types.append("Easy Run")
        elif day_of_week == 1:  # Tuesday
            workout_types.append(np.random.choice(["Tempo Run", "Interval Training"]))
        elif day_of_week == 2:  # Wednesday
            workout_types.append("Recovery Run")
        elif day_of_week == 3:  # Thursday
            workout_types.append(np.random.choice(["Hill Training", "Tempo Run"]))
        elif day_of_week == 4:  # Friday
            workout_types.append("Easy Run")
        elif day_of_week == 5:  # Saturday
            workout_types.append("Long Run")
        else:  # Sunday
            workout_types.append(np.random.choice(["Rest", "Cross Training"]))

 # Generate distance based on workout type
    distances = []
    for workout in workout_types:
        if workout == "Long Run":
            distances.append(round(np.random.uniform(10, 15), 1))
        elif workout == "Tempo Run":
            distances.append(round(np.random.uniform(5, 8), 1))
        elif workout == "Interval Training" or workout == "Hill Training":
            distances.append(round(np.random.uniform(4, 6), 1))
        elif workout == "Easy Run":
            distances.append(round(np.random.uniform(3, 5), 1))
        elif workout == "Recovery Run":
            distances.append(round(np.random.uniform(2, 4), 1))
        else:
            distances.append(0)  # Rest or Cross Training
    
    # Generate duration based on distance and some randomness
    durations = []
    for i, distance in enumerate(distances):
        if distance > 0:
            # Base pace in minutes per mile/km
            if workout_types[i] == "Easy Run" or workout_types[i] == "Recovery Run":
                base_pace = 9.5  # 9:30 min/mile
            elif workout_types[i] == "Long Run":
                base_pace = 9.0  # 9:00 min/mile
            elif workout_types[i] == "Tempo Run":
                base_pace = 7.5  # 7:30 min/mile
            else:  # Intervals or Hills
                base_pace = 8.0  # 8:00 min/mile average including recovery
            
            # Add some random variation
            pace = base_pace + np.random.normal(0, 0.5)
            duration = round(distance * pace)
            durations.append(duration)
        else:
            # For cross training, assign a duration
            if workout_types[i] == "Cross Training":
                durations.append(round(np.random.uniform(30, 60)))
            else:
                durations.append(0)  # Rest day
    
    # Generate perceived exertion (RPE)
    rpe = []
    for workout in workout_types:
        if workout == "Rest":
            rpe.append(0)
        elif workout == "Recovery Run":
            rpe.append(round(np.random.uniform(2, 4)))
        elif workout == "Easy Run":
            rpe.append(round(np.random.uniform(3, 5)))
        elif workout == "Cross Training":
            rpe.append(round(np.random.uniform(4, 6)))
        elif workout == "Long Run":
            rpe.append(round(np.random.uniform(5, 7)))
        elif workout == "Tempo Run":
            rpe.append(round(np.random.uniform(6, 8)))
        else:  # Intervals or Hills
            rpe.append(round(np.random.uniform(7, 9)))
    
    # Generate calories burned
    calories = []
    for i, duration in enumerate(durations):
        if duration > 0:
            # Base calorie burn per minute
            if workout_types[i] == "Easy Run" or workout_types[i] == "Recovery Run":
                cal_per_min = 10
            elif workout_types[i] == "Long Run" or workout_types[i] == "Tempo Run":
                cal_per_min = 12
            else:  # Intervals or Hills or Cross Training
                cal_per_min = 11
            
            # Add some random variation
            calories.append(round(duration * cal_per_min * np.random.uniform(0.9, 1.1)))
        else:
            calories.append(0)
    
    # Create DataFrame
    workout_data = pd.DataFrame({
        'Date': dates,
        'Workout': workout_types,
        'Distance (miles)': distances,
        'Duration (min)': durations,
        'RPE (0-10)': rpe,
        'Calories': calories
    })
    
    return workout_data


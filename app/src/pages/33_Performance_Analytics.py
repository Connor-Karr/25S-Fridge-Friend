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

# Mock nutrition data
@st.cache_data(ttl=600)
def generate_mock_nutrition_data(days=60):
    np.random.seed(43)
    
    # Generate dates
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days-1)
    dates = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days)]
    
    # Generate baseline nutrition values with weekly patterns
    calories = []
    protein = []
    carbs = []
    fat = []
    water = []
    
    for i in range(days):
        day_of_week = (start_date + timedelta(days=i)).weekday()
        
        # Pattern: Higher carbs on workout days, higher protein on strength days, higher calories on weekends
        if day_of_week in [0, 2, 3, 5]:  # Run days (Mon, Wed, Thu, Sat)
            base_carbs = 250
            base_protein = 120
            base_fat = 65
            base_calories = 2400
            base_water = 3.0
        elif day_of_week == 1:  # Strength day (Tue)
            base_carbs = 200
            base_protein = 150
            base_fat = 70
            base_calories = 2300
            base_water = 3.2
        elif day_of_week == 6:  # Rest day (Sun)
            base_carbs = 180
            base_protein = 100
            base_fat = 75
            base_calories = 2000
            base_water = 2.8
        else:
            base_carbs = 200
            base_protein = 110
            base_fat = 70
            base_calories = 2100
            base_water = 3.0
        
        # Add some random variation
        calories.append(round(base_calories + np.random.normal(0, 100)))
        protein.append(round(base_protein + np.random.normal(0, 10)))
        carbs.append(round(base_carbs + np.random.normal(0, 20)))
        fat.append(round(base_fat + np.random.normal(0, 8)))
        water.append(round(base_water + np.random.normal(0, 0.5), 1))
    
    # Create DataFrame
    nutrition_data = pd.DataFrame({
        'Date': dates,
        'Calories': calories,
        'Protein (g)': protein,
        'Carbs (g)': carbs,
        'Fat (g)': fat,
        'Water (L)': water
    })
    
    return nutrition_data

# Mock performance metrics
@st.cache_data(ttl=600)
def generate_mock_performance_metrics(workout_data, nutrition_data):
    dates = workout_data['Date'].tolist()
    
    # Generate energy levels with some correlation to nutrition
    energy = []
    recovery = []
    sleep_quality = []
    
    for i, date in enumerate(dates):
        # Find nutrition for the previous day (if available)
        prev_day_nutrition = nutrition_data[nutrition_data['Date'] == date]
        
        if not prev_day_nutrition.empty:
            # Base energy on carbs and calories
            carbs = prev_day_nutrition['Carbs (g)'].values[0]
            calories = prev_day_nutrition['Calories'].values[0]
            water = prev_day_nutrition['Water (L)'].values[0]
            
            # Factors that influence energy
            carb_factor = (carbs / 250) * 5  # Scale to 0-5 range
            calorie_factor = (calories / 2400) * 3  # Scale to 0-3 range
            water_factor = (water / 3) * 2  # Scale to 0-2 range
            
            # Calculate base energy (0-10 scale)
            base_energy = carb_factor + calorie_factor + water_factor
            energy_value = np.clip(base_energy + np.random.normal(0, 0.5), 1, 10)
            energy.append(round(energy_value, 1))
            
            # Calculate recovery based on protein, sleep and previous workout
            protein = prev_day_nutrition['Protein (g)'].values[0]
            
            # Get previous day's workout if available
            if i > 0:
                prev_workout_rpe = workout_data.iloc[i-1]['RPE (0-10)']
            else:
                prev_workout_rpe = 0
            
            # Factors that influence recovery
            protein_factor = (protein / 140) * 5  # Scale to 0-5 range
            workout_factor = (1 - (prev_workout_rpe / 10)) * 3  # Lower RPE = better recovery
            sleep_factor = np.random.uniform(0, 2)  # Random sleep quality
            
            # Calculate base recovery (0-10 scale)
            base_recovery = protein_factor + workout_factor + sleep_factor
            recovery_value = np.clip(base_recovery + np.random.normal(0, 0.5), 1, 10)
            recovery.append(round(recovery_value, 1))
            
            # Generate sleep quality (somewhat independent)
            sleep_value = np.clip(np.random.normal(7, 1), 3, 10)
            sleep_quality.append(round(sleep_value, 1))
        else:
            # Default values if no nutrition data
            energy.append(round(np.random.uniform(5, 7), 1))
            recovery.append(round(np.random.uniform(5, 7), 1))
            sleep_quality.append(round(np.random.uniform(6, 8), 1))
    
    # Create DataFrame
    performance_data = pd.DataFrame({
        'Date': dates,
        'Energy (1-10)': energy,
        'Recovery (1-10)': recovery,
        'Sleep (1-10)': sleep_quality
    })
    
    return performance_data

# Get data
workout_data = generate_mock_workout_data()
nutrition_data = generate_mock_nutrition_data()
performance_data = generate_mock_performance_metrics(workout_data, nutrition_data)

# Combine all data
combined_data = pd.merge(workout_data, nutrition_data, on='Date', how='left')
combined_data = pd.merge(combined_data, performance_data, on='Date', how='left')

# Create tabs for different analysis views
tab1, tab2, tab3, tab4 = st.tabs(["Performance Overview", "Nutrition Impact", "Recovery Analysis", "Optimization"])

# Performance Overview Tab
with tab1:
    st.subheader("Training & Performance Overview")
    
    # Date range selection
    date_range = st.slider(
        "Select date range:",
        min_value=datetime.strptime(combined_data['Date'].min(), '%Y-%m-%d').date(),
        max_value=datetime.strptime(combined_data['Date'].max(), '%Y-%m-%d').date(),
        value=(
            datetime.strptime(combined_data['Date'].min(), '%Y-%m-%d').date(),
            datetime.strptime(combined_data['Date'].max(), '%Y-%m-%d').date()
        )
    )
    
    # Filter data based on date range
    start_date = date_range[0].strftime('%Y-%m-%d')
    end_date = date_range[1].strftime('%Y-%m-%d')
    
    filtered_data = combined_data[
        (combined_data['Date'] >= start_date) & 
        (combined_data['Date'] <= end_date)
    ]
    
    # Weekly volume chart
    st.subheader("Weekly Training Volume")
    
    # Calculate weekly volume
    filtered_data['Week'] = pd.to_datetime(filtered_data['Date']).dt.strftime('%Y-%U')
    weekly_volume = filtered_data.groupby('Week').agg({
        'Distance (miles)': 'sum',
        'Duration (min)': 'sum',
        'Calories': 'sum'
    }).reset_index()
    
    # Create figure
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add distance bars
    fig.add_trace(
        go.Bar(
            x=weekly_volume['Week'],
            y=weekly_volume['Distance (miles)'],
            name="Weekly Distance",
            marker_color='royalblue'
        ),
        secondary_y=False
    )
    
    # Add duration line
    fig.add_trace(
        go.Scatter(
            x=weekly_volume['Week'], 
            y=weekly_volume['Duration (min)'],
            name="Weekly Duration",
            line=dict(color='firebrick')
        ),
        secondary_y=True
    )
    
    # Set titles
    fig.update_layout(
        title_text="Weekly Training Volume",
        height=400
    )
    
    # Set axis titles
    fig.update_xaxes(title_text="Week")
    fig.update_yaxes(title_text="Distance (miles)", secondary_y=False)
    fig.update_yaxes(title_text="Duration (minutes)", secondary_y=True)
    
    st.plotly_chart(fig, use_container_width=True)
    

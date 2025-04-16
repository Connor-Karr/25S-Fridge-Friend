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
    
# Workout distribution
    st.subheader("Workout Distribution")
    
    # Calculate workout counts
    workout_counts = filtered_data['Workout'].value_counts().reset_index()
    workout_counts.columns = ['Workout Type', 'Count']
    
    # Create pie chart
    fig = px.pie(
        workout_counts,
        values='Count',
        names='Workout Type',
        title='Workout Type Distribution',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    fig.update_layout(height=400)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Performance metrics over time
    st.subheader("Performance Metrics")
    
    # Select metrics to display
    metrics = st.multiselect(
        "Select metrics to display:",
        ["Energy (1-10)", "Recovery (1-10)", "Sleep (1-10)", "RPE (0-10)"],
        default=["Energy (1-10)", "Recovery (1-10)"]
    )
    
    if metrics:
        # Create line chart
        fig = go.Figure()
        
        for metric in metrics:
            fig.add_trace(
                go.Scatter(
                    x=filtered_data['Date'], 
                    y=filtered_data[metric],
                    mode='lines+markers',
                    name=metric
                )
            )
        
        # Update layout
        fig.update_layout(
            title="Performance Metrics Over Time",
            xaxis_title="Date",
            yaxis_title="Score",
            height=400,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Training load and fatigue
    st.subheader("Training Load & Recovery")
    
    # Calculate training load using RPE * Duration
    filtered_data['Training Load'] = filtered_data['RPE (0-10)'] * filtered_data['Duration (min)'] / 60
    
    # Calculate 7-day rolling average for acute load
    filtered_data['Acute Load'] = filtered_data['Training Load'].rolling(7).mean()
    
    # Calculate 28-day rolling average for chronic load
    filtered_data['Chronic Load'] = filtered_data['Training Load'].rolling(28).mean()
    
    # Calculate acute:chronic workload ratio (ACWR)
    filtered_data['ACWR'] = filtered_data['Acute Load'] / filtered_data['Chronic Load']
    
    # Create figure
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add load lines
    fig.add_trace(
        go.Scatter(
            x=filtered_data['Date'],
            y=filtered_data['Acute Load'],
            name="7-day Load",
            line=dict(color='royalblue')
        ),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(
            x=filtered_data['Date'],
            y=filtered_data['Chronic Load'],
            name="28-day Load",
            line=dict(color='green')
        ),
        secondary_y=False
    )
    
    # Add ACWR line
    fig.add_trace(
        go.Scatter(
            x=filtered_data['Date'],
            y=filtered_data['ACWR'],
            name="Acute:Chronic Ratio",
            line=dict(color='firebrick')
        ),
        secondary_y=True
    )
    
    # Add safety zones for ACWR
    fig.add_hrect(
        y0=0.8, y1=1.3,
        line_width=0,
        fillcolor="green", opacity=0.1,
        secondary_y=True
    )
    
    fig.add_hrect(
        y0=1.3, y1=1.5,
        line_width=0,
        fillcolor="yellow", opacity=0.1,
        secondary_y=True
    )
    
    fig.add_hrect(
        y0=1.5, y1=2.0,
        line_width=0,
        fillcolor="red", opacity=0.1,
        secondary_y=True
    )
    
    # Set titles
    fig.update_layout(
        title_text="Training Load & Recovery",
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Set axis titles
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Training Load (RPE * Hours)", secondary_y=False)
    fig.update_yaxes(title_text="Acute:Chronic Workload Ratio", secondary_y=True)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show interpretation
    with st.expander("Understanding Training Load"):
        st.write("""
        **Acute Load (7-day average)**: Represents your short-term training stress.
        
        **Chronic Load (28-day average)**: Represents your longer-term training adaptation.
        
        **Acute:Chronic Workload Ratio (ACWR)**:
        - **0.8-1.3**: Optimal training zone (green)
        - **1.3-1.5**: Caution zone - increased injury risk (yellow)
        - **>1.5**: Danger zone - high injury risk (red)
        
        Maintaining an ACWR in the "sweet spot" (0.8-1.3) helps balance training adaptations with recovery, reducing injury risk while optimizing performance.
        """)

# Nutrition Impact Tab
with tab2:
    st.subheader("Nutrition's Impact on Performance")
    
    # Performance metric selection
    performance_metric = st.selectbox(
        "Select performance metric:",
        ["Energy (1-10)", "Recovery (1-10)", "RPE (0-10)", "Sleep (1-10)"]
    )
    
    # Nutrition metric selection
    nutrition_metric = st.selectbox(
        "Select nutrition metric:",
        ["Calories", "Carbs (g)", "Protein (g)", "Fat (g)", "Water (L)"]
    )
    
    # Scatter plot of relationship
    fig = px.scatter(
        combined_data,
        x=nutrition_metric,
        y=performance_metric,
        title=f"{nutrition_metric} vs. {performance_metric}",
        trendline="ols",
        hover_data=["Date", "Workout"]
    )
    
    # Update layout
    fig.update_layout(height=500)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Calculate correlation
    correlation = combined_data[[nutrition_metric, performance_metric]].corr().iloc[0, 1]
    
    # Interpret correlation
    if abs(correlation) < 0.2:
        relationship = "very weak"
    elif abs(correlation) < 0.4:
        relationship = "weak"
    elif abs(correlation) < 0.6:
        relationship = "moderate"
    elif abs(correlation) < 0.8:
        relationship = "strong"
    else:
        relationship = "very strong"
    
    direction = "positive" if correlation > 0 else "negative"
    
    st.info(f"**Analysis:** There is a {relationship} {direction} relationship (correlation = {correlation:.2f}) between {nutrition_metric} and {performance_metric}.")
    
    # Advanced analysis with time lag
    st.subheader("Time-Lagged Nutrition Impact")
    
    st.write("""
    This analysis shows how nutrition from previous days affects your performance metrics, 
    accounting for the delayed effect of nutrition on performance.
    """)
    
    # Calculate lagged correlations
    lag_days = 3  # Check up to 3 days of lag
    
    lag_correlations = []
    for lag in range(0, lag_days+1):
        # Create lagged nutrition data
        lagged_data = combined_data.copy()
        
        if lag > 0:
            # Shift nutrition metrics back by 'lag' days
            lagged_nutrition = nutrition_data.copy()
            lagged_nutrition['Date'] = pd.to_datetime(lagged_nutrition['Date'])
            lagged_nutrition['Date'] = lagged_nutrition['Date'] + timedelta(days=lag)
            lagged_nutrition['Date'] = lagged_nutrition['Date'].dt.strftime('%Y-%m-%d')
            
            # Merge with performance data
            lagged_combined = pd.merge(
                performance_data,
                lagged_nutrition,
                on='Date',
                how='left'
            )
            
            # Calculate correlation
            if performance_metric in lagged_combined.columns and nutrition_metric in lagged_combined.columns:
                lag_corr = lagged_combined[[nutrition_metric, performance_metric]].corr().iloc[0, 1]
                lag_correlations.append({
                    "Lag (days)": lag,
                    "Correlation": lag_corr
                })
            else:
                lag_correlations.append({
                    "Lag (days)": lag,
                    "Correlation": np.nan
                })
        else:
            # No lag (same day)
            if performance_metric in combined_data.columns and nutrition_metric in combined_data.columns:
                lag_corr = combined_data[[nutrition_metric, performance_metric]].corr().iloc[0, 1]
                lag_correlations.append({
                    "Lag (days)": lag,
                    "Correlation": lag_corr
                })
            else:
                lag_correlations.append({
                    "Lag (days)": lag,
                    "Correlation": np.nan
                })
    
    # Create lag correlation DataFrame
    lag_df = pd.DataFrame(lag_correlations)
    
    # Create bar chart
    fig = px.bar(
        lag_df,
        x="Lag (days)",
        y="Correlation",
        title=f"Impact of {nutrition_metric} on {performance_metric} (by days of lag)",
        color="Correlation",
        color_continuous_scale=px.colors.diverging.RdBu,
        range_color=[-1, 1],
        labels={"Lag (days)": "Days Before Performance", "Correlation": "Correlation Strength"}
    )
    
    fig.update_layout(height=350)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Find the strongest lag correlation
    max_lag_corr = lag_df.loc[lag_df["Correlation"].abs().idxmax()]
    max_lag = max_lag_corr["Lag (days)"]
    max_corr = max_lag_corr["Correlation"]
    
    st.info(f"**Insight:** The strongest relationship between {nutrition_metric} and {performance_metric} occurs with a lag of {max_lag:.0f} days (correlation = {max_corr:.2f}).")
    
    # Performance metrics by workout type
    st.subheader("Nutrition & Performance by Workout Type")
    
    # Group data by workout type
    workout_groups = combined_data.groupby("Workout").agg({
        nutrition_metric: "mean",
        performance_metric: "mean",
        "RPE (0-10)": "mean",
        "Distance (miles)": "mean"
    }).reset_index()
    
    # Create bar chart
    fig = px.bar(
        workout_groups,
        x="Workout",
        y=[nutrition_metric, performance_metric],
        title=f"Average {nutrition_metric} and {performance_metric} by Workout Type",
        barmode="group"
    )
    
    fig.update_layout(height=400)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Find the optimal nutrition level
    st.subheader("Optimal Nutrition Levels")
    
    # Group data by nutrition levels
    if nutrition_metric == "Calories":
        bin_size = 200
        min_val = (combined_data[nutrition_metric].min() // bin_size) * bin_size
        max_val = ((combined_data[nutrition_metric].max() // bin_size) + 1) * bin_size
    elif nutrition_metric in ["Carbs (g)", "Protein (g)"]:
        bin_size = 20
        min_val = (combined_data[nutrition_metric].min() // bin_size) * bin_size
        max_val = ((combined_data[nutrition_metric].max() // bin_size) + 1) * bin_size
    elif nutrition_metric == "Fat (g)":
        bin_size = 10
        min_val = (combined_data[nutrition_metric].min() // bin_size) * bin_size
        max_val = ((combined_data[nutrition_metric].max() // bin_size) + 1) * bin_size
    else:  # Water
        bin_size = 0.5
        min_val = (combined_data[nutrition_metric].min() // bin_size) * bin_size
        max_val = ((combined_data[nutrition_metric].max() // bin_size) + 1) * bin_size

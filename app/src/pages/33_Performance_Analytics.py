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

# Create bins
    bins = np.arange(min_val, max_val + bin_size, bin_size)
    bin_labels = [f"{b} - {b+bin_size}" for b in bins[:-1]]
    
    # Bin the nutrition data
    combined_data['Nutrition Bin'] = pd.cut(
        combined_data[nutrition_metric],
        bins=bins,
        labels=bin_labels,
        include_lowest=True
    )
    
    # Group by nutrition bin
    bin_groups = combined_data.groupby("Nutrition Bin").agg({
        performance_metric: ["mean", "count"]
    }).reset_index()
    
    bin_groups.columns = ["Nutrition Bin", "Performance Mean", "Count"]
    
    # Only include bins with sufficient data
    bin_groups = bin_groups[bin_groups["Count"] >= 3]
    
    if not bin_groups.empty:
        # Create bar chart
        fig = px.bar(
            bin_groups,
            x="Nutrition Bin",
            y="Performance Mean",
            title=f"Average {performance_metric} by {nutrition_metric} Range",
            color="Performance Mean",
            color_continuous_scale=px.colors.sequential.Viridis
        )
        
        # Add count as text
        fig.update_traces(text=bin_groups["Count"], textposition='outside')
        
        # Find optimal nutrition level
        optimal_bin = bin_groups.loc[bin_groups["Performance Mean"].idxmax()]
        
        # Add annotation for optimal level
        fig.add_annotation(
            x=optimal_bin["Nutrition Bin"],
            y=optimal_bin["Performance Mean"],
            text="Optimal Range",
            showarrow=True,
            arrowhead=1
        )
        
        fig.update_layout(height=400)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show interpretation
        st.info(f"**Optimal Range:** Your {performance_metric} appears to be highest when your {nutrition_metric} is in the range of {optimal_bin['Nutrition Bin']}.")
    else:
        st.warning("Not enough data to determine optimal nutrition levels. Try adjusting the date range or metrics.")

# Recovery Analysis Tab
with tab3:
    st.subheader("Recovery Analysis")
    
    # Workout impact on recovery
    st.write("### Workout Impact on Recovery")
    
    # Calculate next-day recovery by workout type
    workout_recovery = []
    
    for i in range(len(combined_data)-1):
        current_workout = combined_data.iloc[i]
        next_day_recovery = combined_data.iloc[i+1]["Recovery (1-10)"]
        
        workout_recovery.append({
            "Workout Type": current_workout["Workout"],
            "RPE (0-10)": current_workout["RPE (0-10)"],
            "Duration (min)": current_workout["Duration (min)"],
            "Next Day Recovery": next_day_recovery
        })
    
    workout_recovery_df = pd.DataFrame(workout_recovery)
    
    # Group by workout type
    workout_recovery_groups = workout_recovery_df.groupby("Workout Type").agg({
        "Next Day Recovery": "mean",
        "RPE (0-10)": "mean",
        "Duration (min)": "mean"
    }).reset_index()
    
    # Only include workout types with data
    workout_recovery_groups = workout_recovery_groups[workout_recovery_groups["Workout Type"] != "Rest"]
    
    if not workout_recovery_groups.empty:
        # Create horizontal bar chart
        fig = px.bar(
            workout_recovery_groups,
            y="Workout Type",
            x="Next Day Recovery",
            orientation='h',
            title="Average Next-Day Recovery by Workout Type",
            color="RPE (0-10)",
            color_continuous_scale=px.colors.sequential.Plasma,
            hover_data=["Duration (min)"]
        )
        
        fig.update_layout(height=400)
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Nutrition impact on recovery
    st.write("### Nutrition Impact on Recovery")
    
    # Select two nutrition metrics
    col1, col2 = st.columns(2)
    
    with col1:
        x_metric = st.selectbox(
            "Select first nutrition metric:",
            ["Protein (g)", "Carbs (g)", "Fat (g)", "Calories", "Water (L)"],
            index=0
        )
    
    with col2:
        y_metric = st.selectbox(
            "Select second nutrition metric:",
            ["Protein (g)", "Carbs (g)", "Fat (g)", "Calories", "Water (L)"],
            index=1
        )
    
    # Create scatter plot with recovery as color
    fig = px.scatter(
        combined_data,
        x=x_metric,
        y=y_metric,
        color="Recovery (1-10)",
        title=f"Recovery by {x_metric} and {y_metric}",
        color_continuous_scale=px.colors.sequential.Viridis,
        hover_data=["Date", "Workout", "RPE (0-10)"]
    )
    
    # Add quadrant lines at the median of each metric
    x_median = combined_data[x_metric].median()
    y_median = combined_data[y_metric].median()
    
    fig.add_vline(
        x=x_median,
        line_dash="dash",
        line_color="gray"
    )
    
    fig.add_hline(
        y=y_median,
        line_dash="dash",
        line_color="gray"
    )
    
    # Add quadrant annotations
    fig.add_annotation(
        x=combined_data[x_metric].max() * 0.75,
        y=combined_data[y_metric].max() * 0.75,
        text=f"High {x_metric}, High {y_metric}",
        showarrow=False,
        font=dict(size=10)
    )
    
    fig.add_annotation(
        x=combined_data[x_metric].min() * 1.25,
        y=combined_data[y_metric].max() * 0.75,
        text=f"Low {x_metric}, High {y_metric}",
        showarrow=False,
        font=dict(size=10)
    )
    
    fig.add_annotation(
        x=combined_data[x_metric].max() * 0.75,
        y=combined_data[y_metric].min() * 1.25,
        text=f"High {x_metric}, Low {y_metric}",
        showarrow=False,
        font=dict(size=10)
    )
    
    fig.add_annotation(
        x=combined_data[x_metric].min() * 1.25,
        y=combined_data[y_metric].min() * 1.25,
        text=f"Low {x_metric}, Low {y_metric}",
        showarrow=False,
        font=dict(size=10)
    )
    
    fig.update_layout(height=500)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Recovery timeline visualization
    st.write("### Recovery Timeline After Hard Workouts")
    
    # Define hard workouts as RPE >= 7
    hard_workouts = combined_data[combined_data['RPE (0-10)'] >= 7]
    
    if not hard_workouts.empty:
        # Find recovery patterns after hard workouts
        recovery_patterns = []
        
        for index, workout in hard_workouts.iterrows():
            workout_date = workout['Date']
            workout_date_dt = datetime.strptime(workout_date, '%Y-%m-%d')
            
            # Get next 3 days of recovery data
            recovery_days = []
            
            for i in range(1, 4):
                next_date = (workout_date_dt + timedelta(days=i)).strftime('%Y-%m-%d')
                next_day_data = combined_data[combined_data['Date'] == next_date]
                
                if not next_day_data.empty:
                    recovery_days.append({
                        "Day": i,
                        "Recovery": next_day_data['Recovery (1-10)'].values[0],
                        "Workout Type": workout['Workout'],
                        "Workout Date": workout_date,
                        "RPE": workout['RPE (0-10)']
                    })
            
            recovery_patterns.extend(recovery_days)
        
        recovery_df = pd.DataFrame(recovery_patterns)
        
        if not recovery_df.empty:
            # Group by day after workout
            recovery_by_day = recovery_df.groupby("Day").agg({
                "Recovery": "mean"
            }).reset_index()
            
            # Create line chart
            fig = px.line(
                recovery_by_day,
                x="Day",
                y="Recovery",
                title="Average Recovery Pattern After Hard Workouts",
                markers=True,
                line_shape="spline"
            )
            
            # Update x-axis to show days
            fig.update_xaxes(
                tickvals=[1, 2, 3],
                ticktext=["Day 1", "Day 2", "Day 3"]
            )
            
            fig.update_layout(
                height=350,
                xaxis_title="Days After Hard Workout",
                yaxis_title="Recovery Score (1-10)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show recovery by workout type
            recovery_by_type = recovery_df.groupby(["Workout Type", "Day"]).agg({
                "Recovery": "mean"
            }).reset_index()
            
            # Create line chart by workout type
            fig = px.line(
                recovery_by_type,
                x="Day",
                y="Recovery",
                color="Workout Type",
                title="Recovery Patterns by Workout Type",
                markers=True
            )
            
            # Update x-axis to show days
            fig.update_xaxes(
                tickvals=[1, 2, 3],
                ticktext=["Day 1", "Day 2", "Day 3"]
            )
            
            fig.update_layout(
                height=350,
                xaxis_title="Days After Workout",
                yaxis_title="Recovery Score (1-10)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Not enough recovery data available after hard workouts.")
    else:
        st.info("No hard workouts (RPE >= 7) found in the selected date range.")

# Optimization Tab
with tab4:
    st.subheader("Nutrition Optimization Recommendations")
    
    st.write("""
    Based on your performance and nutrition data, here are personalized recommendations 
    to optimize your nutrition for better performance.
    """)

# Create nutrition target recommendations
    target_calories = round(combined_data['Calories'].mean())
    target_protein = round(combined_data['Protein (g)'].mean())
    target_carbs = round(combined_data['Carbs (g)'].mean())
    target_fat = round(combined_data['Fat (g)'].mean())
    target_water = round(combined_data['Water (L)'].mean(), 1)
    
    # Adjust targets based on performance correlations
    # Calories adjustment
    cal_energy_corr = combined_data[['Calories', 'Energy (1-10)']].corr().iloc[0, 1]
    cal_recovery_corr = combined_data[['Calories', 'Recovery (1-10)']].corr().iloc[0, 1]
    if cal_energy_corr > 0.3 or cal_recovery_corr > 0.3:
        target_calories = round(target_calories * 1.05)  # Increase by 5%
    elif cal_energy_corr < -0.3 or cal_recovery_corr < -0.3:
        target_calories = round(target_calories * 0.95)  # Decrease by 5%
    
    # Protein adjustment
    protein_recovery_corr = combined_data[['Protein (g)', 'Recovery (1-10)']].corr().iloc[0, 1]
    if protein_recovery_corr > 0.3:
        target_protein = round(target_protein * 1.1)  # Increase by 10%
    elif protein_recovery_corr < -0.3:
        target_protein = round(target_protein * 0.95)  # Decrease by 5%
    
    # Carbs adjustment
    carbs_energy_corr = combined_data[['Carbs (g)', 'Energy (1-10)']].corr().iloc[0, 1]
    if carbs_energy_corr > 0.3:
        target_carbs = round(target_carbs * 1.1)  # Increase by 10%
    elif carbs_energy_corr < -0.3:
        target_carbs = round(target_carbs * 0.95)  # Decrease by 5%
    
    # Display current averages and targets
    st.write("### Nutrition Targets")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Daily Calories", 
            f"{target_calories} kcal", 
            delta=f"{target_calories - round(combined_data['Calories'].mean())} kcal"
        )
        st.metric(
            "Protein", 
            f"{target_protein} g", 
            delta=f"{target_protein - round(combined_data['Protein (g)'].mean())} g"
        )
    
    with col2:
        st.metric(
            "Carbohydrates", 
            f"{target_carbs} g", 
            delta=f"{target_carbs - round(combined_data['Carbs (g)'].mean())} g"
        )
        st.metric(
            "Fat", 
            f"{target_fat} g", 
            delta=f"{target_fat - round(combined_data['Fat (g)'].mean())} g"
        )
    
    with col3:
        st.metric(
            "Water", 
            f"{target_water} L", 
            delta=f"{target_water - round(combined_data['Water (L)'].mean(), 1)} L"
        )
    
    # Workout-specific nutrition recommendations
    st.write("### Workout-Specific Recommendations")
    
    # Create recommendations for different workout types
    workout_recommendations = {
        "Long Run": {
            "carbs": "8-10g/kg body weight (day before)",
            "protein": "1.6-1.8g/kg body weight",
            "timing": "Carb-heavy dinner night before, breakfast 3h before",
            "hydration": "500-750ml per hour during run"
        },
        "Tempo Run": {
            "carbs": "6-8g/kg body weight",
            "protein": "1.6-1.8g/kg body weight",
            "timing": "Carbs 2-3h before, recovery nutrition within 30min after",
            "hydration": "400-600ml per hour during run"
        },
        "Interval Training": {
            "carbs": "6-8g/kg body weight",
            "protein": "1.8-2.0g/kg body weight",
            "timing": "Small snack 1-2h before, protein+carbs within 30min after",
            "hydration": "500-750ml per hour during training"
        },
        "Easy Run": {
            "carbs": "5-7g/kg body weight",
            "protein": "1.6-1.8g/kg body weight",
            "timing": "Normal meal timing, no special considerations needed",
            "hydration": "400-600ml per hour during run"
        }
    }
    
    # Create tabs for each workout type
    workout_tabs = st.tabs(list(workout_recommendations.keys()))
    
    for i, (workout_type, recommendations) in enumerate(workout_recommendations.items()):
        with workout_tabs[i]:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Nutritional Targets:**")
                st.write(f"Carbohydrates: {recommendations['carbs']}")
                st.write(f"Protein: {recommendations['protein']}")
                st.write(f"Timing: {recommendations['timing']}")
                st.write(f"Hydration: {recommendations['hydration']}")
            
            with col2:
                st.write("**Sample Pre-Workout Meal:**")
                
                if workout_type == "Long Run":
                    st.write("- Oatmeal with banana, honey, and almond butter")
                    st.write("- Toast with jam")
                    st.write("- Coffee or tea")
                elif workout_type == "Tempo Run":
                    st.write("- Greek yogurt with berries and granola")
                    st.write("- Banana")
                    st.write("- Small coffee (if tolerated)")
                elif workout_type == "Interval Training":
                    st.write("- Rice cake with nut butter and honey")
                    st.write("- Small apple")
                    st.write("- Water")
                else:  # Easy Run
                    st.write("- Normal balanced meal 1-2 hours before")
                    st.write("- No special considerations needed")
                
                st.write("**Sample Post-Workout Meal:**")
                
                if workout_type == "Long Run":
                    st.write("- Protein smoothie with banana and berries")
                    st.write("- Peanut butter sandwich")
                    st.write("- Chocolate milk")
                elif workout_type == "Tempo Run":
                    st.write("- Protein shake")
                    st.write("- Banana or energy bar")
                    st.write("- Complete meal within 2 hours")
                elif workout_type == "Interval Training":
                    st.write("- Recovery shake with 3:1 carb:protein ratio")
                    st.write("- Piece of fruit")
                    st.write("- Complete meal within 2 hours")
                else:  # Easy Run
                    st.write("- Normal balanced meal")
                    st.write("- Focus on hydration")
    
    # Periodized nutrition planner
    st.write("### Periodized Nutrition Plan")
    
    st.write("""
    This tool helps you match your nutrition strategy with your training periodization 
    for optimal performance and recovery.
    """)
    
    # Create form for training phase input
    with st.form("periodized_nutrition_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            training_phase = st.selectbox(
                "Current training phase:",
                ["Base Building", "Build Phase", "Peak Phase", "Taper", "Race Week", "Recovery"]
            )
            
            weight = st.number_input("Weight (lbs):", min_value=80, max_value=300, value=150)
        
        with col2:
            training_hours = st.slider("Weekly training hours:", min_value=3, max_value=20, value=8)
            
            goal = st.selectbox(
                "Primary goal:",
                ["General Fitness", "Performance", "Weight Management", "Recovery"]
            )
        
        submit_button = st.form_submit_button("Generate Nutrition Plan")
        
        if submit_button:
            # Convert weight to kg
            weight_kg = weight * 0.453592
            
            # Calculate base nutrition needs
            if training_phase == "Base Building":
                carbs_g_per_kg = 5
                protein_g_per_kg = 1.6
                fat_g_per_kg = 1.0
                adjust_text = "Focus on establishing good nutritional habits and fueling for general training."
            elif training_phase == "Build Phase":
                carbs_g_per_kg = 6 + (training_hours / 10)  # Increase with training volume
                protein_g_per_kg = 1.8
                fat_g_per_kg = 1.0
                adjust_text = "Increase carbohydrates to support higher training load."
            elif training_phase == "Peak Phase":
                carbs_g_per_kg = 7 + (training_hours / 8)
                protein_g_per_kg = 2.0
                fat_g_per_kg = 0.8
                adjust_text = "Prioritize carbohydrates for workout fueling and recovery."
            elif training_phase == "Taper":
                carbs_g_per_kg = 6
                protein_g_per_kg = 1.8
                fat_g_per_kg = 0.8
                adjust_text = "Maintain high carbs while reducing calories slightly as training volume decreases."
            elif training_phase == "Race Week":
                carbs_g_per_kg = 8 + (training_hours / 5)
                protein_g_per_kg = 1.6
                fat_g_per_kg = 0.6
                adjust_text = "Implement carb-loading protocol 2-3 days before race."
            else:  # Recovery
                carbs_g_per_kg = 4
                protein_g_per_kg = 2.0
                fat_g_per_kg = 1.2
                adjust_text = "Focus on protein for recovery and anti-inflammatory foods."
            
            # Apply goal-specific adjustments
            if goal == "Weight Management":
                carbs_g_per_kg *= 0.9  # Reduce carbs slightly
                fat_g_per_kg *= 0.9  # Reduce fat slightly
            elif goal == "Performance":
                carbs_g_per_kg *= 1.1  # Increase carbs
            elif goal == "Recovery":
                protein_g_per_kg *= 1.1  # Increase protein
            
            # Calculate total macros
            carbs = round(weight_kg * carbs_g_per_kg)
            protein = round(weight_kg * protein_g_per_kg)
            fat = round(weight_kg * fat_g_per_kg)
            
            # Calculate calories
            calories = (carbs * 4) + (protein * 4) + (fat * 9)
            
            # Display nutrition plan
            st.success("Personalized Nutrition Plan Generated!")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Daily Calories", f"{calories} kcal")
            
            with col2:
                st.metric("Protein", f"{protein}g ({round(protein/weight_kg, 1)}g/kg)")
            
            with col3:
                st.metric("Carbs", f"{carbs}g ({round(carbs/weight_kg, 1)}g/kg)")
            
            st.write(f"**Fat:** {fat}g ({round(fat/weight_kg, 1)}g/kg)")
            
            st.write(f"**Adjustment Strategy:** {adjust_text}")
            
            # Macro ratio
            protein_pct = round((protein * 4) / calories * 100)
            carbs_pct = round((carbs * 4) / calories * 100)
            fat_pct = round((fat * 9) / calories * 100)
            
            # Create macro ratio pie chart
            macro_data = pd.DataFrame({
                'Macronutrient': ['Carbs', 'Protein', 'Fat'],
                'Percentage': [carbs_pct, protein_pct, fat_pct]
            })
            
            fig = px.pie(
                macro_data,
                values='Percentage',
                names='Macronutrient',
                title='Recommended Macro Ratio',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            
            fig.update_layout(height=300)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Workout-specific recommendations
            st.subheader("Workout-Day Adjustments")
            
            st.write("**Hard Workout Days:**")
            st.write(f"- Increase carbs to {round(carbs * 1.2)}g (+20%)")
            st.write("- Consume ~60% of daily carbs in the meals before and after workout")
            st.write("- Consider intra-workout nutrition for sessions >90 minutes")
            
            st.write("**Easy/Recovery Days:**")
            st.write(f"- Decrease carbs to {round(carbs * 0.8)}g (-20%)")
            st.write(f"- Maintain protein at {protein}g to support recovery")
            st.write("- Focus on nutrient-dense foods and adequate hydration")

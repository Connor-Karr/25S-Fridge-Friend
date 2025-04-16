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
st.title("📊 Nutrition Tracking")
st.write("Track and analyze your nutrition to optimize performance")

# Function to get macro tracking data
@st.cache_data(ttl=300)
def get_nutrition_logs(client_id=1):
    try:
        response = requests.get(f"{API_BASE_URL}/logs/nutrition/{client_id}")
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            st.error(f"Error fetching nutrition logs: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []

# Function to log nutrition entry
def log_nutrition_entry(data):
    try:
        response = requests.post(f"{API_BASE_URL}/logs/nutrition", json=data)
        
        if response.status_code == 201:
            return True
        else:
            st.error(f"Error logging nutrition: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

# Create tabs for different views
tab1, tab2, tab3 = st.tabs(["Daily Tracker", "Log Meal", "Nutrition Analysis"])

# Daily Tracker Tab
with tab1:
    st.subheader("Today's Nutrition")
    
    # Get today's date
    today = datetime.now().date()
    
    # Get nutrition logs
    nutrition_logs = get_nutrition_logs()
    
    # If no logs found, use mock data
    if not nutrition_logs:
        # Mock nutrition data
        nutrition_logs = [
            {"tracking_id": 1, "client_id": 1, "protein": 89, "fat": 38, "fiber": 18, "sodium": 1200, "vitamins": 80, "calories": 1241, "carbs": 135},
            {"tracking_id": 2, "client_id": 1, "protein": 120, "fat": 45, "fiber": 22, "sodium": 1500, "vitamins": 90, "calories": 1650, "carbs": 180},
            {"tracking_id": 3, "client_id": 1, "protein": 105, "fat": 42, "fiber": 25, "sodium": 1350, "vitamins": 85, "calories": 1450, "carbs": 160}
        ]
    
    # Use the most recent log for today
    today_log = nutrition_logs[0] if nutrition_logs else None

# Define targets based on athlete profile
    targets = {
        "Protein": 135,
        "Carbs": 225, 
        "Fat": 55,
        "Fiber": 30,
        "Sodium": 2000,
        "Calories": 1900
    }
    
    if today_log:
        consumed = {
            "Protein": today_log.get("protein", 0),
            "Carbs": today_log.get("carbs", 0),
            "Fat": today_log.get("fat", 0),
            "Fiber": today_log.get("fiber", 0),
            "Sodium": today_log.get("sodium", 0),
            "Calories": today_log.get("calories", 0)
        }
        
        # Calculate percentages
        percentages = {
            key: round((consumed[key] / targets[key]) * 100, 1) 
            for key in targets.keys()
        }
        
        # Create two columns: one for macros, one for micros
        col1, col2 = st.columns(2)
        
        # Macros column
        with col1:
            st.subheader("Macronutrients")
            
            # Display progress bars for macros
            for macro in ["Protein", "Carbs", "Fat", "Calories"]:
                target = targets[macro]
                value = consumed[macro]
                percentage = percentages[macro]
                
                # Create label
                if macro == "Calories":
                    macro_label = f"{macro}: {value} / {target} kcal ({percentage}%)"
                else:
                    macro_label = f"{macro}: {value}g / {target}g ({percentage}%)"
                
                # Set color based on percentage
                if percentage < 50:
                    color = "red"
                elif percentage < 80:
                    color = "orange"
                elif percentage <= 100:
                    color = "green"
                else:
                    color = "red"  # Over target
                
                # Display progress bar
                st.progress(min(percentage/100, 1.0), text=macro_label)
            
            # Macro ratios
            st.subheader("Macro Ratios")
            
            # Calculate total calories from macros
            protein_calories = consumed["Protein"] * 4
            carb_calories = consumed["Carbs"] * 4
            fat_calories = consumed["Fat"] * 9
            total_macro_calories = protein_calories + carb_calories + fat_calories
            
            # Calculate percentages
            if total_macro_calories > 0:
                protein_percent = (protein_calories / total_macro_calories) * 100
                carb_percent = (carb_calories / total_macro_calories) * 100
                fat_percent = (fat_calories / total_macro_calories) * 100
            else:
                protein_percent = carb_percent = fat_percent = 0
            
            # Create pie chart
            macro_ratios = pd.DataFrame({
                'Macronutrient': ['Protein', 'Carbs', 'Fat'],
                'Percentage': [protein_percent, carb_percent, fat_percent]
            })
            
            fig = px.pie(
                macro_ratios,
                values='Percentage',
                names='Macronutrient',
                title='Current Macro Ratio',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            
            fig.update_layout(
                height=300,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Micros column
        with col2:
            st.subheader("Micronutrients")
            
            # Display progress bars for micros
            for micro in ["Fiber", "Sodium"]:
                target = targets[micro]
                value = consumed[micro]
                percentage = percentages[micro]
                
                # Create label
                if micro == "Sodium":
                    micro_label = f"{micro}: {value}mg / {target}mg ({percentage}%)"
                else:
                    micro_label = f"{micro}: {value}g / {target}g ({percentage}%)"
                
                # Set color based on percentage
                if percentage < 50:
                    color = "red"
                elif percentage < 80:
                    color = "orange"
                elif percentage <= 100:
                    color = "green"
                else:
                    color = "red"  # Over target
                
                # Display progress bar
                st.progress(min(percentage/100, 1.0), text=micro_label)
            
            # Additional metrics
            st.subheader("Performance Metrics")
            
            # Calculate metrics
            remaining_calories = targets["Calories"] - consumed["Calories"]
            carb_to_protein_ratio = round(consumed["Carbs"] / consumed["Protein"], 2) if consumed["Protein"] > 0 else 0
            
            # Display metrics
            st.metric("Remaining Calories", f"{remaining_calories} kcal")
            st.metric("Carb to Protein Ratio", f"{carb_to_protein_ratio}", delta="0.2")
            
            # Water intake (mock data)
            water_consumed = 1.8
            water_target = 3.0
            water_percent = (water_consumed / water_target) * 100
            
            st.write(f"**Water Intake:** {water_consumed}L / {water_target}L ({water_percent:.1f}%)")
            st.progress(water_consumed / water_target)
            
            # Quick add water button
            if st.button("+ Add 0.5L Water"):
                st.success("Added 0.5L of water!")
                # In a real app, this would update the water tracker
    else:
        st.info("No nutrition data logged for today. Use the 'Log Meal' tab to start tracking.")

# Log Meal Tab
with tab2:
    st.subheader("Log a Meal")
    
    # Create form for logging a meal
    with st.form("log_meal_form"):
        # Meal selection
        meal_options = ["Breakfast", "Lunch", "Dinner", "Snack", "Pre-Workout", "Post-Workout"]
        meal_type = st.selectbox("Meal Type:", meal_options)
        
        # Create columns for macro inputs
        col1, col2 = st.columns(2)
        
        with col1:
            protein = st.number_input("Protein (g):", min_value=0.0, step=1.0)
            carbs = st.number_input("Carbs (g):", min_value=0.0, step=1.0)
            fat = st.number_input("Fat (g):", min_value=0.0, step=1.0)
        
        with col2:
            fiber = st.number_input("Fiber (g):", min_value=0.0, step=1.0)
            sodium = st.number_input("Sodium (mg):", min_value=0.0, step=10.0)
            calories = st.number_input("Calories:", min_value=0, step=10)
        
        # Option to add specific food items (simplified)
        with st.expander("Add Specific Foods"):
            st.caption("Quickly add common foods")
            
            # Common foods with pre-filled nutrition data
            foods = {
                "Chicken Breast (100g)": {"protein": 31, "carbs": 0, "fat": 3.6, "fiber": 0, "sodium": 74, "calories": 165},
                "Brown Rice (100g)": {"protein": 2.6, "carbs": 23, "fat": 0.9, "fiber": 1.8, "sodium": 5, "calories": 112},
                "Broccoli (100g)": {"protein": 2.8, "carbs": 6.6, "fat": 0.4, "fiber": 2.6, "sodium": 33, "calories": 34},
                "Egg (whole)": {"protein": 6.3, "carbs": 0.6, "fat": 5.3, "fiber": 0, "sodium": 70, "calories": 72},
                "Banana (medium)": {"protein": 1.3, "carbs": 27, "fat": 0.4, "fiber": 3.1, "sodium": 1, "calories": 105},
                "Protein Shake": {"protein": 25, "carbs": 5, "fat": 2, "fiber": 1, "sodium": 120, "calories": 140}
            }
            
            # Create buttons for quick-add foods
            food_cols = st.columns(3)
            
            for i, (food, nutrients) in enumerate(foods.items()):
                with food_cols[i % 3]:
                    if st.button(f"+ {food}", key=f"add_{food}"):
                        # This would add the food's nutrients to the form in a real app
                        st.session_state.added_protein = nutrients["protein"]
                        st.session_state.added_carbs = nutrients["carbs"]
                        st.session_state.added_fat = nutrients["fat"]
                        st.session_state.added_fiber = nutrients["fiber"]
                        st.session_state.added_sodium = nutrients["sodium"]
                        st.session_state.added_calories = nutrients["calories"]
                        
                        st.success(f"Added {food} to your meal!")
        
        # Notes field
        notes = st.text_area("Notes:", placeholder="How did you feel after this meal? Any digestive issues?")
        
        # Submit button
        submit_button = st.form_submit_button("Log Meal")
        
        if submit_button:
            # Calculate calories if not provided
            if calories == 0:
                calories = (protein * 4) + (carbs * 4) + (fat * 9)
            
            # Create nutrition log data
            nutrition_data = {
                "client_id": 1,  # This would be dynamic in a real app
                "protein": protein,
                "fat": fat,
                "fiber": fiber,
                "sodium": sodium,
                "vitamins": 0,  # Not tracking in the form
                "calories": calories,
                "carbs": carbs
            }
            
            # Log nutrition
            success = log_nutrition_entry(nutrition_data)
            
            if success:
                st.success(f"Successfully logged {meal_type} with {calories} calories!")
                st.cache_data.clear()
                time.sleep(1)
                
                # Switch to Daily Tracker tab
                tab1.set_active(True)
                st.rerun()
            else:
                # If API call fails, show a mock success for demo purposes
                st.success(f"Successfully logged {meal_type} with {calories} calories! (Mock)")
                time.sleep(1)
                
                # Switch to Daily Tracker tab
                tab1.set_active(True)
                st.rerun()
    
    # Quick meal templates
    st.markdown("---")
    st.subheader("Meal Templates")
    
    # Mock meal templates based on athlete needs
    templates = [
        {"name": "Pre-run Breakfast", "protein": 20, "carbs": 50, "fat": 10, "calories": 370},
        {"name": "Post-workout Recovery", "protein": 30, "carbs": 45, "fat": 8, "calories": 372},
        {"name": "Light Pre-race Dinner", "protein": 25, "carbs": 60, "fat": 12, "calories": 448},
        {"name": "Protein-focused Lunch", "protein": 35, "carbs": 35, "fat": 15, "calories": 415}
    ]
    
    # Display templates as expandable cards
    for template in templates:
        with st.expander(f"{template['name']} - {template['calories']} cal"):
            st.write(f"**Protein:** {template['protein']}g | **Carbs:** {template['carbs']}g | **Fat:** {template['fat']}g")
            
            if st.button("Use Template", key=f"use_{template['name']}"):
                st.session_state.template_protein = template['protein']
                st.session_state.template_carbs = template['carbs']
                st.session_state.template_fat = template['fat']
                st.session_state.template_calories = template['calories']
                
                st.success(f"Template values applied!")
                st.rerun()

# Nutrition Analysis Tab
with tab3:
    st.subheader("Nutrition Analysis")
    
    # Date range selection
    col1, col2 = st.columns(2)
    
    with col1:
        analysis_period = st.selectbox(
            "Analysis Period:",
            ["Last 7 Days", "Last 14 Days", "Last 30 Days", "Custom Range"]
        )
    
    with col2:
        if analysis_period == "Custom Range":
            date_range = st.date_input(
                "Select date range:",
                value=(datetime.now().date() - timedelta(days=7), datetime.now().date()),
                max_value=datetime.now().date()
            )
        else:
            if analysis_period == "Last 7 Days":
                days = 7
            elif analysis_period == "Last 14 Days":
                days = 14
            else:  # Last 30 Days
                days = 30
            
            date_range = (datetime.now().date() - timedelta(days=days), datetime.now().date())
    
    # Generate mock data for the analysis period
    analysis_dates = []
    current_date = date_range[0]
    while current_date <= date_range[1]:
        analysis_dates.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)
    
    # Generate mock nutrition data
    np.random.seed(42)  # for reproducibility
    
    nutrition_data = []
    for date in analysis_dates:
        # Base values with some random variation
        protein = np.random.normal(120, 15)
        carbs = np.random.normal(200, 30)
        fat = np.random.normal(50, 8)
        calories = (protein * 4) + (carbs * 4) + (fat * 9) + np.random.normal(0, 50)
        
        nutrition_data.append({
            'date': date,
            'protein': max(0, round(protein)),
            'carbs': max(0, round(carbs)),
            'fat': max(0, round(fat)),
            'calories': max(0, round(calories))
        })
    
    # Convert to DataFrame
    df = pd.DataFrame(nutrition_data)
    
    # Display average metrics for the period
    avg_protein = df['protein'].mean()
    avg_carbs = df['carbs'].mean()
    avg_fat = df['fat'].mean()
    avg_calories = df['calories'].mean()
    
    # Create metric cards
    metric_cols = st.columns(4)
    
    with metric_cols[0]:
        st.metric("Avg. Protein", f"{avg_protein:.1f}g", delta=f"{avg_protein - targets['Protein']:.1f}g")
    
    with metric_cols[1]:
        st.metric("Avg. Carbs", f"{avg_carbs:.1f}g", delta=f"{avg_carbs - targets['Carbs']:.1f}g")
    
    with metric_cols[2]:
        st.metric("Avg. Fat", f"{avg_fat:.1f}g", delta=f"{avg_fat - targets['Fat']:.1f}g")
    
    with metric_cols[3]:
        st.metric("Avg. Calories", f"{avg_calories:.0f}", delta=f"{avg_calories - targets['Calories']:.0f}")
    
    # Trends over time
    st.subheader("Nutrient Trends")
    
    # Select nutrient to visualize
    nutrient_options = ["Calories", "Protein", "Carbs", "Fat", "All Macros"]
    selected_nutrient = st.selectbox("Select nutrient to visualize:", nutrient_options)
    
    # Create appropriate chart based on selection
    if selected_nutrient == "All Macros":
        # Create a line chart for all macros
        fig = go.Figure()
        
        # Add traces for each macro
        fig.add_trace(go.Scatter(x=df['date'], y=df['protein'], mode='lines+markers', name='Protein (g)'))
        fig.add_trace(go.Scatter(x=df['date'], y=df['carbs'], mode='lines+markers', name='Carbs (g)'))
        fig.add_trace(go.Scatter(x=df['date'], y=df['fat'], mode='lines+markers', name='Fat (g)'))
        
        # Update layout
        fig.update_layout(
            title=f'Macronutrient Trends ({analysis_period})',
            xaxis_title='Date',
            yaxis_title='Grams',
            height=400,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        # For single nutrient, show trend with target line
        nutrient_column = selected_nutrient.lower()
        
        # Create figure
        fig = go.Figure()
        
        # Add nutrient trace
        fig.add_trace(go.Scatter(
            x=df['date'], 
            y=df[nutrient_column],
            mode='lines+markers',
            name=selected_nutrient
        ))
        
        # Add target line
        if selected_nutrient in targets:
            target_value = targets[selected_nutrient]
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=[target_value] * len(df),
                mode='lines',
                name=f'Target ({target_value})',
                line=dict(color='red', dash='dash')
            ))
        
        # Update layout
        unit = "kcal" if selected_nutrient == "Calories" else "g"
        fig.update_layout(
            title=f'{selected_nutrient} Trend ({analysis_period})',
            xaxis_title='Date',
            yaxis_title=f'{selected_nutrient} ({unit})',
            height=400,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Nutrition insights
    st.subheader("Nutrition Insights")
    
    # Generate some insights based on the data
    insights = []

# Protein insights
    if avg_protein < targets["Protein"] * 0.9:
        insights.append("❌ Protein intake is consistently below your target. Consider adding more lean protein sources to support muscle recovery.")
    elif avg_protein > targets["Protein"] * 1.1:
        insights.append("⚠️ Protein intake is consistently above your target. While adequate protein is important for runners, excessive amounts may be unnecessary.")
    else:
        insights.append("✅ Protein intake is well-balanced and consistent, supporting muscle repair and recovery.")
    
    # Carb insights
    if avg_carbs < targets["Carbs"] * 0.9:
        insights.append("❌ Carbohydrate intake is lower than optimal for your training volume. Consider increasing carbs to fuel your workouts more effectively.")
    elif avg_carbs > targets["Carbs"] * 1.1:
        insights.append("⚠️ Carbohydrate intake is higher than your target. Ensure timing aligns with your training schedule for optimal performance.")
    else:
        insights.append("✅ Carbohydrate intake is well-aligned with your training needs, providing adequate energy for workouts.")
    
    # Fat insights
    if avg_fat < targets["Fat"] * 0.8:
        insights.append("❌ Fat intake is too low, which may impact hormone production and vitamin absorption. Consider adding healthy fats like avocados, nuts, and olive oil.")
    elif avg_fat > targets["Fat"] * 1.2:
        insights.append("⚠️ Fat intake is higher than optimal. While healthy fats are important, they are calorie-dense and may impact performance if excessive.")
    else:
        insights.append("✅ Fat intake is in the optimal range, supporting hormone production and overall health.")
    
    # Calorie insights
    if avg_calories < targets["Calories"] * 0.9:
        insights.append("❌ Calorie intake is below your estimated needs. This may impact energy levels, recovery, and long-term performance.")
    elif avg_calories > targets["Calories"] * 1.1:
        insights.append("⚠️ Calorie intake is higher than your estimated needs. This may impact body composition over time.")
    else:
        insights.append("✅ Calorie intake is well-balanced, supporting your training needs and recovery.")
    
    # Display insights
    for insight in insights:
        st.write(insight)

# Recommendations based on insights
    st.subheader("Recommendations")
    
    recommendations = []
    
    # Generate recommendations based on the nutrition data
    if avg_protein < targets["Protein"] * 0.9:
        recommendations.append("Add a post-workout protein shake (25-30g protein) to boost your daily intake.")
    
    if avg_carbs < targets["Carbs"] * 0.9:
        recommendations.append("Include more whole grains, fruits, and starchy vegetables to increase your carbohydrate intake.")
    
    if avg_fat < targets["Fat"] * 0.8:
        recommendations.append("Add 1-2 servings of healthy fats daily (avocado, nuts, olive oil) to reach optimal fat intake.")
    
    if avg_calories < targets["Calories"] * 0.9:
        recommendations.append("Increase portion sizes slightly at each meal to ensure adequate energy intake for training.")
    
    # Display recommendations
    for i, recommendation in enumerate(recommendations):
        st.write(f"{i+1}. {recommendation}")
    
    # If no recommendations (all metrics on target)
    if not recommendations:
        st.success("Your nutrition is well-balanced! Continue with your current approach as it's supporting your training needs effectively.")

# Tracking resources
st.markdown("---")
st.subheader("📚 Nutrition Resources for Runners")

# Create a container for the resources
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Race Day Nutrition Guide**")
        st.write("Learn how to fuel before, during, and after races")
        if st.button("View Guide"):
            with st.spinner("Loading guide..."):
                time.sleep(1)
                st.success("Guide loaded!")
                st.markdown("""
                ## Race Day Nutrition Guide
                
                ### Pre-Race (3-4 hours before)
                - 400-600 calories
                - 80-120g carbs
                - Low fat and fiber
                - Examples: Oatmeal with banana, toast with honey
                
                ### During Race
                - 30-60g carbs per hour for races >60 min
                - Stay hydrated with 16-20 oz fluid per hour
                - Use easily digestible sources (gels, sports drinks)
                
                ### Post-Race
                - 20-30g protein within 30 minutes
                - 60-100g carbs within 2 hours
                - Rehydrate with 20-24 oz fluid per pound lost
                """)
        
        st.write("**Runner's Recipe Book**")
        st.write("Quick, nutritious recipes optimized for training")
        if st.button("Download Recipes"):
            with st.spinner("Preparing download..."):
                time.sleep(1)
                st.success("Download ready!")
                st.download_button(
                    label="Download Recipe Book",
                    data="Sample runner's recipe book content. Would contain actual recipes in a real app.",
                    file_name="runners_recipes.txt",
                    mime="text/plain"
                )
    
    with col2:
        st.write("**Training Phase Nutrition Calculator**")
        st.write("Adjust your nutrition based on your training phase")
        if st.button("Open Calculator"):
            st.info("This would open a training phase calculator in a real app.")
        
        st.write("**Hydration Calculator**")
        st.write("Calculate your personal hydration needs")
        if st.button("Calculate Hydration Needs"):
            with st.form("hydration_calculator"):
                weight = st.number_input("Weight (lbs):", min_value=80, max_value=300, value=150)
                activity_duration = st.number_input("Workout Duration (minutes):", min_value=15, max_value=240, value=60)
                intensity = st.select_slider("Workout Intensity:", options=["Low", "Moderate", "High", "Very High"])
                temperature = st.number_input("Temperature (°F):", min_value=40, max_value=110, value=75)
                
                submit_button = st.form_submit_button("Calculate")
                
                if submit_button:
                    # Mock calculation
                    base_fluid = weight * 0.5  # 0.5oz per pound of body weight
                    
                    # Adjustments for intensity
                    intensity_factor = 1.0
                    if intensity == "Moderate":
                        intensity_factor = 1.2
                    elif intensity == "High":
                        intensity_factor = 1.5
                    elif intensity == "Very High":
                        intensity_factor = 1.8
                    
                    # Adjustments for temperature
                    temp_factor = 1.0
                    if temperature > 80:
                        temp_factor = 1.3
                    elif temperature > 90:
                        temp_factor = 1.5
                    elif temperature > 100:
                        temp_factor = 1.8
                    
                    # Calculate fluid needs
                    fluid_needs = base_fluid * intensity_factor * temp_factor * (activity_duration / 60)
                    
                    st.success(f"Recommended Fluid Intake: {fluid_needs:.1f} oz during your {activity_duration} minute workout")
                    st.write(f"This equals approximately {fluid_needs/8:.1f} cups of water")

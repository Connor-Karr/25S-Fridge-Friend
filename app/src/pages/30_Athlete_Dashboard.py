import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

# API base URL
API_BASE_URL = "http://web-api:4000"

# Authentication check
if not st.session_state.get('authenticated', False) or st.session_state.role != "athlete":
    st.warning("Please log in as an athlete to access this page")
    st.stop()

# Set up navigation
SideBarLinks(st.session_state.role)

# Page header
st.title(f"Athlete Dashboard")
st.subheader(f"Welcome, {st.session_state.first_name}!")

# API helper function
def get_api_data(endpoint):
    """Get data from API with error handling"""
    try:
        response = requests.get(f"{API_BASE_URL}/{endpoint}")
        if response.status_code == 200:
            return response.json()
        else:
            # Don't show error messages for 404s
            if response.status_code != 404:
                st.error(f"Error fetching data from {endpoint}: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return []

# Get user data
client_id = st.session_state.get('user_id', 1)

# Tabs for different dashboard sections
tab1, tab2, tab3 = st.tabs(["Nutrition", "Meal Plans", "Workouts"])

# Nutrition Tab
with tab1:
    st.header("Nutrition Tracking")
    
    # Get nutrition logs
    nutrition_logs = get_api_data(f"logs/nutrition/{client_id}")
    
    if nutrition_logs:
        # Convert to DataFrame
        nutrition_df = pd.DataFrame(nutrition_logs)
        
        # Display recent nutrition logs
        st.subheader("Recent Nutrition Logs")
        
        # Select columns to display
        display_cols = []
        for col in ['tracking_id', 'protein', 'fat', 'carbs', 'calories', 'fiber', 'sodium', 'vitamins']:
            if col in nutrition_df.columns:
                display_cols.append(col)
        
        if display_cols:
            st.dataframe(nutrition_df[display_cols].head(10), use_container_width=True)
        else:
            st.dataframe(nutrition_df.head(10), use_container_width=True)
        
        # Display average nutrition values
        st.subheader("Nutrition Summary")
        
        # Only calculate averages for numeric columns
        numeric_cols = nutrition_df.select_dtypes(include=['float', 'int']).columns
        if len(numeric_cols) > 0:
            avg_nutrition = nutrition_df[numeric_cols].mean().to_dict()
            
            # Convert to dataframe for display
            summary_data = {
                "Metric": list(avg_nutrition.keys()),
                "Average Value": [round(float(val), 1) if isinstance(val, (int, float)) else val for val in avg_nutrition.values()]
            }
            summary_df = pd.DataFrame(summary_data)
            
            st.dataframe(summary_df, use_container_width=True, hide_index=True)
    else:
        st.info("No nutrition logs found.")

# Meal Plans Tab
with tab2:
    st.header("Meal Plans")
    
    # Get meal plans
    meal_plans = get_api_data(f"meal-plans?client_id={client_id}")
    
    if meal_plans:
        # Convert to DataFrame
        meal_df = pd.DataFrame(meal_plans)
        
        # Display meal plans
        st.subheader("Your Meal Plans")
        
        # Select columns to display if they exist
        display_cols = []
        for col in ['meal_id', 'recipe_name', 'quantity']:
            if col in meal_df.columns:
                display_cols.append(col)
        
        if display_cols:
            st.dataframe(
                meal_df[display_cols], 
                column_config={
                    "meal_id": "ID",
                    "recipe_name": "Recipe",
                    "quantity": "Servings"
                },
                use_container_width=True
            )
        else:
            st.dataframe(meal_df, use_container_width=True)
    else:
        st.info("No meal plans found.")

# Workouts Tab
with tab3:
    st.header("Workouts")
    
    # Get workout data from the new endpoint
    workouts = get_api_data(f"users/client/{client_id}/workouts")
    
    if workouts:
        # Convert to DataFrame
        workout_df = pd.DataFrame(workouts)
        
        # Display workouts
        st.subheader("Your Workouts")
        
        # Select columns to display if they exist
        display_cols = []
        for col in ['workout_id', 'name', 'quantity', 'weight', 'calories_burnt']:
            if col in workout_df.columns:
                display_cols.append(col)
        
        if display_cols:
            st.dataframe(
                workout_df[display_cols], 
                column_config={
                    "workout_id": "ID",
                    "name": "Workout Type",
                    "quantity": "Duration (min)",
                    "weight": "Weight (lbs)",
                    "calories_burnt": "Calories Burned"
                },
                use_container_width=True
            )
        else:
            st.dataframe(workout_df, use_container_width=True)
            
        # Calculate total calories burned
        if 'calories_burnt' in workout_df.columns:
            total_calories = workout_df['calories_burnt'].sum()
            st.metric("Total Calories Burned", f"{int(total_calories)} kcal")
    else:
        st.info("No workout data found.")

# Refresh button
if st.button("Refresh Data"):
    st.rerun()
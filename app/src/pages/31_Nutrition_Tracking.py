import streamlit as st
import pandas as pd
import requests
from datetime import datetime
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
st.title("📊 Nutrition Tracking")
st.write("Track and analyze your nutrition to optimize performance")

# API helper functions
def get_api_data(endpoint):
    """Get data from API with error handling"""
    try:
        response = requests.get(f"{API_BASE_URL}/{endpoint}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching data from {endpoint}: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return []

def post_api_data(endpoint, data):
    """Post data to API with error handling"""
    try:
        response = requests.post(f"{API_BASE_URL}/{endpoint}", json=data)
        if response.status_code in [200, 201]:
            return True
        else:
            st.error(f"Error posting data to {endpoint}: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"Error posting data: {str(e)}")
        return False

# Get user data
client_id = st.session_state.get('user_id', 1)

# Create tabs for different views
tab1, tab2 = st.tabs(["View Nutrition", "Log Nutrition"])

# View Nutrition Tab
with tab1:
    st.subheader("Nutrition Logs")
    
    # Get nutrition logs
    nutrition_logs = get_api_data(f"logs/nutrition/{client_id}")
    
    if nutrition_logs:
        # Convert to DataFrame
        nutrition_df = pd.DataFrame(nutrition_logs)
        
        # Display nutrition logs table
        st.dataframe(nutrition_df, use_container_width=True)
        
        # Show the most recent log details
        st.subheader("Latest Nutrition Log")
        latest_log = nutrition_df.iloc[0] if not nutrition_df.empty else None
        
        if latest_log is not None:
            # Create a nicer display of the latest log
            metrics_cols = st.columns(4)
            
            # Only display metrics if they exist in the data
            if 'protein' in latest_log:
                with metrics_cols[0]:
                    st.metric("Protein", f"{latest_log['protein']}g")
            
            if 'carbs' in latest_log:
                with metrics_cols[1]:
                    st.metric("Carbs", f"{latest_log['carbs']}g")
            
            if 'fat' in latest_log:
                with metrics_cols[2]:
                    st.metric("Fat", f"{latest_log['fat']}g")
            
            if 'calories' in latest_log:
                with metrics_cols[3]:
                    st.metric("Calories", f"{latest_log['calories']} kcal")
            
            # Second row of metrics if they exist
            if any(x in latest_log for x in ['fiber', 'sodium', 'vitamins']):
                metrics_cols2 = st.columns(3)
                
                if 'fiber' in latest_log:
                    with metrics_cols2[0]:
                        st.metric("Fiber", f"{latest_log['fiber']}g")
                
                if 'sodium' in latest_log:
                    with metrics_cols2[1]:
                        st.metric("Sodium", f"{latest_log['sodium']}mg")
                
                if 'vitamins' in latest_log:
                    with metrics_cols2[2]:
                        st.metric("Vitamins", f"{latest_log['vitamins']} units")
        
        # Display nutrition summary
        st.subheader("Nutrition Summary")
        
        # Only include numeric columns in the summary
        numeric_cols = nutrition_df.select_dtypes(include=['float', 'int']).columns
        if not numeric_cols.empty:
            # Calculate average values
            avg_nutrition = nutrition_df[numeric_cols].mean()
            
            # Drop client_id and tracking_id from the summary if they exist
            if 'client_id' in avg_nutrition:
                avg_nutrition = avg_nutrition.drop('client_id')
            if 'tracking_id' in avg_nutrition:
                avg_nutrition = avg_nutrition.drop('tracking_id')
            
            # Display averages in a table
            summary_data = {
                "Metric": avg_nutrition.index,
                "Average Value": [f"{round(float(val), 1)}" for val in avg_nutrition.values]
            }
            summary_df = pd.DataFrame(summary_data)
            
            st.dataframe(summary_df, hide_index=True, use_container_width=True)
    else:
        st.info("No nutrition logs found. Start tracking your nutrition using the 'Log Nutrition' tab.")

# Log Nutrition Tab
with tab2:
    st.subheader("Log New Nutrition Data")
    
    # Create form for logging nutrition
    with st.form("log_nutrition_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            protein = st.number_input("Protein (g):", min_value=0.0, step=1.0)
            carbs = st.number_input("Carbs (g):", min_value=0.0, step=1.0)
            fat = st.number_input("Fat (g):", min_value=0.0, step=1.0)
            fiber = st.number_input("Fiber (g):", min_value=0.0, step=1.0)
        
        with col2:
            sodium = st.number_input("Sodium (mg):", min_value=0.0, step=10.0)
            vitamins = st.number_input("Vitamins (units):", min_value=0.0, step=1.0)
            calories = st.number_input("Calories:", min_value=0, step=10)
        
        # Form submission
        submit_button = st.form_submit_button("Log Nutrition")
        
        if submit_button:
            # If calories weren't manually entered, use the calculated value
            if calories == 0:
                calories = (protein * 4) + (carbs * 4) + (fat * 9)
            
            # Prepare nutrition data
            nutrition_data = {
                "client_id": client_id,
                "protein": protein,
                "fat": fat,
                "fiber": fiber,
                "sodium": sodium,
                "vitamins": vitamins,
                "calories": calories,
                "carbs": carbs
            }
            
            # Send data to API
            success = post_api_data("logs/nutrition", nutrition_data)
            
            if success:
                st.success("Nutrition log added successfully!")
                st.rerun()

# Refresh button
if st.button("Refresh Data"):
    st.rerun()
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

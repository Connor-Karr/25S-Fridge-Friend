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

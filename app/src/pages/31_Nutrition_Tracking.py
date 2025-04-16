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

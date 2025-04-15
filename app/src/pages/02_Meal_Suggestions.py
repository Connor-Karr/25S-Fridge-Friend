import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime, timedelta
import json
from modules.nav import SideBarLinks

# API base URL
API_BASE_URL = "http://web-api:4000"

# Authentication check
if not st.session_state.get('authenticated', False) or st.session_state.role != "busy_student":
    st.warning("Please log in as Ben to access this page")
    st.stop()

# Set up navigation
SideBarLinks(st.session_state.role)

# Page header
st.title("🍲 Meal Suggestions")
st.write("Find recipes based on what's in your fridge and your budget")

# Function to get fridge inventory
@st.cache_data(ttl=300)
def get_fridge_inventory():
    try:
        response = requests.get(f"{API_BASE_URL}/fridge?client_id=1")
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            st.error(f"Error fetching inventory: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []

# Function to get meal plans
@st.cache_data(ttl=300)
def get_meal_plans():
    try:
        response = requests.get(f"{API_BASE_URL}/meal-plans?client_id=1")
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            st.error(f"Error fetching meal plans: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []
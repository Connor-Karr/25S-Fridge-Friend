import streamlit as st
import pandas as pd
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
st.title("🍱 Leftovers Tracker")
st.write("Track and manage your leftover meals to reduce food waste")

# Function to get leftovers
@st.cache_data(ttl=300)
def get_leftovers():
    try:
        response = requests.get(f"{API_BASE_URL}/leftovers")
        
        if response.status_code == 200:
            data = response.json()
            leftovers = []
            
            for item in data:
                # Calculate days left (assuming leftovers last 5 days)
                # In a real app, this would come from the API
                created_date = datetime.now().date() - timedelta(days=1)  # Mock date
                expire_date = created_date + timedelta(days=5)
                days_left = (expire_date - datetime.now().date()).days
                
                leftovers.append({
                    'id': item.get('leftover_id'),
                    'name': item.get('recipe_name', 'Unknown'),
                    'quantity': item.get('quantity', 1),
                    'is_expired': item.get('is_expired', False),
                    'created_date': created_date.strftime('%Y-%m-%d'),
                    'days_left': days_left
                })
            
            return leftovers
        else:
            st.error(f"Error fetching leftovers: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []

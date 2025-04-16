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

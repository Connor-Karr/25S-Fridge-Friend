import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from modules.nav import SideBarLinks

API_BASE_URL = "http://web-api:4000"

if not st.session_state.get('authenticated', False) or st.session_state.role != "nutritionist":
    st.warning("Please log in as Nancy to access this page")
    st.stop()

SideBarLinks(st.session_state.role)

# Page header
st.title("📈 Nutrition Analytics")
st.write("Analyze nutritional data across clients and identify trends")

# Mock client data
clients = [
    {"id": 1, "name": "John D.", "age": 27, "goal": "Weight Loss", "diet": "Low Carb"},
    {"id": 2, "name": "Sarah M.", "age": 34, "goal": "Muscle Gain", "diet": "High Protein"},
    {"id": 3, "name": "Michael R.", "age": 42, "goal": "Maintenance", "diet": "Balanced"},
    {"id": 4, "name": "Emma L.", "age": 19, "goal": "Performance", "diet": "Keto"},
    {"id": 5, "name": "David W.", "age": 55, "goal": "Health", "diet": "Mediterranean"}
]
# Time period selection
time_period = st.selectbox(
    "Analysis Period:",
    ["Last 30 Days", "Last 3 Months", "Last 6 Months", "Year to Date", "Custom Range"]
)

if time_period == "Custom Range":
    date_range = st.date_input(
        "Select date range:",
        value=(datetime.now().date() - timedelta(days=30), datetime.now().date()),
        max_value=datetime.now().date()
    )
else:
    if time_period == "Last 30 Days":
        days = 30
    elif time_period == "Last 3 Months":
        days = 90
    elif time_period == "Last 6 Months":
        days = 180
    else:  # Year to Date
        start_of_year = datetime(datetime.now().year, 1, 1).date()
        days = (datetime.now().date() - start_of_year).days

    date_range = (datetime.now().date() - timedelta(days=days), datetime.now().date())
# Create different tabs
tab1, tab2, tab3, tab4 = st.tabs(["Diet Compliance", "Nutrient Analysis", "Client Comparisons", "Allergy Insights"])

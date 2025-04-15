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

if not st.session_state.get('authenticated', False) or st.session_state.role != "admin":
    st.warning("Please log in as Alvin to access this page")
    st.stop()

SideBarLinks(st.session_state.role)

st.title("📝 System Logs")
st.write("Monitor system activity, track errors, and analyze food scan performance")

tab1, tab2, tab3 = st.tabs(["Error Logs", "Food Scan Logs", "Analytics"])

@st.cache_data(ttl=300)
def get_error_logs():
    try:
        response = requests.get(f"{API_BASE_URL}/logs/errors")
        if response.status_code == 200:
            data = response.json()
            return [{
                'error_id': log.get('error_id'),
                'timestamp': log.get('timestamp', 'Unknown'),
                'message': log.get('message', 'No message'),
                'status': log.get('scan_status', 'Unknown'),
                'ingredient': log.get('ingredient_name', 'Unknown')
            } for log in data]
        else:
            st.error(f"Error fetching logs: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []

@st.cache_data(ttl=300)
def get_scan_logs():
    try:
        response = requests.get(f"{API_BASE_URL}/logs/scans")
        if response.status_code == 200:
            data = response.json()
            return [{
                'log_id': log.get('log_id'),
                'timestamp': log.get('timestamp', 'Unknown'),
                'status': log.get('status', 'Unknown'),
                'ingredient': log.get('ingredient_name', 'Unknown')
            } for log in data]
        else:
            st.error(f"Error fetching scan logs: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []



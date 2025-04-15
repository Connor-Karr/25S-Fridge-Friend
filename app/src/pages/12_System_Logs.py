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

# Error Logs Tab
with tab1:
    st.subheader("System Error Logs")
    error_logs = get_error_logs()
    if not error_logs:
        error_logs = [
            {'error_id': 1, 'timestamp': '2023-04-14 09:23:45', 'message': 'Unrecognized barcode during scan', 'status': 'FAILED', 'ingredient': 'Unknown Cereal'},
            {'error_id': 2, 'timestamp': '2023-04-13 15:42:21', 'message': 'Network error during scan', 'status': 'FAILED', 'ingredient': 'Organic Apple'},
            {'error_id': 3, 'timestamp': '2023-04-13 08:17:32', 'message': 'Database connection timeout', 'status': 'FAILED', 'ingredient': 'Almond Milk'}
        ]
    
    col1, col2 = st.columns(2)
    date_range = st.date_input("Date range:", (datetime.now().date() - timedelta(days=7), datetime.now().date()), max_value=datetime.now().date())
    error_types = ["All"] + list(set([log['status'] for log in error_logs])) if error_logs else []
    error_filter = st.selectbox("Filter by status:", error_types) if error_logs else "All"
    
    filtered_logs = error_logs
    if date_range and len(date_range) == 2:
        start_date, end_date = date_range
        filtered_logs = [log for log in filtered_logs if 'timestamp' in log and start_date <= datetime.strptime(log['timestamp'].split()[0], '%Y-%m-%d').date() <= end_date]
    if error_filter != "All":
        filtered_logs = [log for log in filtered_logs if log.get('status') == error_filter]
    
    if filtered_logs:
        log_df = pd.DataFrame(filtered_logs)
        st.dataframe(log_df, column_config={"error_id": st.column_config.NumberColumn("ID"), "timestamp": "Timestamp", "message": "Error Message", "status": "Status", "ingredient": "Ingredient"}, height=400)
        st.subheader("Error Details")
        error_ids = {f"{log['timestamp']} - {log['message'][:30]}...": i for i, log in enumerate(filtered_logs)}
        selected_error = st.selectbox("Select error for details:", list(error_ids.keys()))
        selected_log = filtered_logs[error_ids[selected_error]]
        with st.expander("Error Details", expanded=True):
            st.write(f"**Error ID:** {selected_log['error_id']}")
            st.write(f"**Timestamp:** {selected_log['timestamp']}")
            st.write(f"**Status:** {selected_log['status']}")
            st.write(f"**Ingredient:** {selected_log['ingredient']}")
            st.code(selected_log['message'])
            if st.button("Create Support Ticket"):
                with st.spinner("Creating ticket..."):
                    time.sleep(2)
                    st.success("Support ticket created successfully!")
    else:
        st.info("No error logs found matching the selected filters.")
    
    if st.button("Refresh Error Logs"):
        st.cache_data.clear()
        st.rerun()



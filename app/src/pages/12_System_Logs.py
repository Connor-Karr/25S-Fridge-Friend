import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
from modules.nav import SideBarLinks

# Authentication check
if not st.session_state.get('authenticated', False) or st.session_state.role != "admin":
    st.warning("Please log in as an admin to access this page")
    st.stop()

# Set up navigation
SideBarLinks(st.session_state.role)

# Page header
st.title("📝 System Logs")
st.write("Monitor system activity, track errors, and analyze food scan performance")

# API base URL
API_BASE_URL = "http://web-api:4000"

# Function to get data from API with error handling
def get_api_data(endpoint):
    try:
        response = requests.get(f"{API_BASE_URL}/{endpoint}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching data from {endpoint}: Status code {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error fetching data from {endpoint}: {str(e)}")
        return []

# Create tabs for different log types
tab1, tab2 = st.tabs(["Error Logs", "Food Scan Logs"])

# Tab 1: Error Logs
with tab1:
    st.subheader("System Error Logs")
    
    # Get error logs from API
    error_logs = get_api_data("logs/errors")
    
    if error_logs:
        # Date range filter
        date_range = st.date_input(
            "Filter by date range:", 
            (datetime.now().date() - timedelta(days=7), datetime.now().date()),
            max_value=datetime.now().date()
        )
        
        # Apply date filter if selected
        filtered_logs = error_logs
        if date_range and len(date_range) == 2:
            start_date, end_date = date_range
            filtered_logs = [
                log for log in filtered_logs 
                if 'timestamp' in log 
                and start_date <= datetime.strptime(log['timestamp'].split(', ')[1][:11], '%d %b %Y').date() <= end_date
            ]
        
        # Display filtered error logs in a table
        if filtered_logs:
            st.dataframe(
                pd.DataFrame(filtered_logs),
                use_container_width=True
            )
            
            # Show error details for selected log
            if len(filtered_logs) > 0:
                log_ids = [log.get('error_id') for log in filtered_logs]
                selected_id = st.selectbox("Select error ID for details:", log_ids)
                
                selected_log = next((log for log in filtered_logs if log.get('error_id') == selected_id), None)
                
                if selected_log:
                    with st.expander("Error Details", expanded=True):
                        for key, value in selected_log.items():
                            st.write(f"**{key}:** {value}")
        else:
            st.info("No error logs found matching the selected filters.")
    else:
        st.info("No error logs found or unable to fetch error log data.")
    
    # Refresh button
    if st.button("Refresh Error Logs"):
        st.rerun()

# Tab 2: Food Scan Logs
with tab2:
    st.subheader("Food Scan Logs")
    
    # Get scan logs from API
    scan_logs = get_api_data("logs/scans")
    
    if scan_logs:
        # Date range filter
        scan_date_range = st.date_input(
            "Filter by date range:", 
            (datetime.now().date() - timedelta(days=7), datetime.now().date()),
            max_value=datetime.now().date(),
            key="scan_date_range"
        )
        
        # Status filter - get unique statuses
        status_options = ["All"] + list(set([log.get('status', '') for log in scan_logs if log.get('status')]))
        status_filter = st.selectbox("Filter by status:", status_options)
        
        # Apply filters
        filtered_scan_logs = scan_logs
        
        # Apply date filter
        if scan_date_range and len(scan_date_range) == 2:
            start_date, end_date = scan_date_range
            filtered_logs = [
                log for log in filtered_logs 
                if 'timestamp' in log 
                and start_date <= datetime.strptime(log['timestamp'].split(', ')[1][:11], '%d %b %Y').date() <= end_date
            ]
        
        # Apply status filter
        if status_filter != "All":
            filtered_scan_logs = [log for log in filtered_scan_logs if log.get('status') == status_filter]
        
        # Display filtered scan logs in a table
        if filtered_scan_logs:
            st.dataframe(
                pd.DataFrame(filtered_scan_logs),
                use_container_width=True
            )
            
            # Basic scan statistics
            total_scans = len(filtered_scan_logs)
            successful_scans = len([log for log in filtered_scan_logs if log.get('status') == 'SUCCESS'])
            failed_scans = len([log for log in filtered_scan_logs if log.get('status') == 'FAILED'])
            
            # Display statistics in columns
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Scans", total_scans)
            with col2:
                st.metric("Successful Scans", successful_scans)
            with col3:
                st.metric("Failed Scans", failed_scans)
        else:
            st.info("No scan logs found matching the selected filters.")
    else:
        st.info("No scan logs found or unable to fetch scan log data.")
    
    # Refresh button
    if st.button("Refresh Scan Logs"):
        st.rerun()

# Refresh All Data button at the bottom
if st.button("Refresh All Data"):
    st.rerun()
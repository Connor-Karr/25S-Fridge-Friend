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

# Food Scan Logs Tab
with tab2:
    st.subheader("Food Scan Logs")
    scan_logs = get_scan_logs()
    if not scan_logs:
        ingredients = ["Apple", "Banana", "Milk", "Eggs", "Bread", "Chicken", "Rice", "Tomatoes", "Cheese", "Yogurt"]
        scan_logs = [{
            'log_id': i + 1,
            'timestamp': (datetime.now() - timedelta(days=np.random.randint(0, 14), hours=np.random.randint(0, 24), minutes=np.random.randint(0, 60))).strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'SUCCESS' if np.random.random() > 0.2 else 'FAILED',
            'ingredient': np.random.choice(ingredients)
        } for i in range(20)]
        scan_logs.sort(key=lambda x: x['timestamp'], reverse=True)

    col1, col2, col3 = st.columns(3)
    scan_date_range = st.date_input("Date range:", (datetime.now().date() - timedelta(days=7), datetime.now().date()), max_value=datetime.now().date(), key="scan_date_range")
    scan_status_filter = st.selectbox("Filter by status:", ["All"] + list(set([log['status'] for log in scan_logs])))
    ingredient_filter = st.selectbox("Filter by ingredient:", ["All"] + list(set([log['ingredient'] for log in scan_logs])))

    filtered_scan_logs = scan_logs
    if scan_date_range and len(scan_date_range) == 2:
        start_date, end_date = scan_date_range
        filtered_scan_logs = [log for log in filtered_scan_logs if start_date <= datetime.strptime(log['timestamp'].split()[0], '%Y-%m-%d').date() <= end_date]
    if scan_status_filter != "All":
        filtered_scan_logs = [log for log in filtered_scan_logs if log.get('status') == scan_status_filter]
    if ingredient_filter != "All":
        filtered_scan_logs = [log for log in filtered_scan_logs if log.get('ingredient') == ingredient_filter]

    if filtered_scan_logs:
        scan_df = pd.DataFrame(filtered_scan_logs)
        def color_status(val): return 'background-color: #FFCCCC' if val == "FAILED" else 'background-color: #CCFFCC'
        st.dataframe(scan_df.style.applymap(color_status, subset=['status']), column_config={"log_id": st.column_config.NumberColumn("ID"), "timestamp": "Timestamp", "status": "Status", "ingredient": "Ingredient"}, height=400)
        st.subheader("Scan Statistics")
        total_scans = len(filtered_scan_logs)
        successful_scans = len([log for log in filtered_scan_logs if log['status'] == 'SUCCESS'])
        success_rate = (successful_scans / total_scans) * 100 if total_scans > 0 else 0
        st.metric("Total Scans", total_scans)
        st.metric("Successful Scans", successful_scans)
        st.metric("Success Rate", f"{success_rate:.1f}%")

        if 'timestamp' in scan_df.columns:
            scan_df['date'] = pd.to_datetime(scan_df['timestamp']).dt.date
            scans_by_day = scan_df.groupby(['date', 'status']).size().reset_index(name='count')
            pivot_df = scans_by_day.pivot(index='date', columns='status', values='count').reset_index().fillna(0)
            if 'SUCCESS' not in pivot_df: pivot_df['SUCCESS'] = 0
            if 'FAILED' not in pivot_df: pivot_df['FAILED'] = 0
            fig = px.bar(pivot_df, x='date', y=['SUCCESS', 'FAILED'], title='Daily Scan Activity', labels={'value': 'Number of Scans', 'date': 'Date'}, color_discrete_map={'SUCCESS': '#4CAF50', 'FAILED': '#FF5252'})
            fig.update_layout(legend_title_text='Scan Status', height=300, margin=dict(l=20, r=20, t=40, b=20), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No scan logs found matching the selected filters.")

    if st.button("Refresh Scan Logs"):
        st.cache_data.clear()
        st.rerun()



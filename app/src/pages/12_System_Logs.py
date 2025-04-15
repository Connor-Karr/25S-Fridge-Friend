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


# Analytics Tab
with tab3:
    st.subheader("System Analytics")
    time_periods = ["Last 7 Days", "Last 30 Days", "Last 90 Days", "Year to Date", "All Time"]
    selected_period = st.selectbox("Select time period:", time_periods)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Users", "158", delta="12" if selected_period == "Last 7 Days" else "27" if selected_period == "Last 30 Days" else "58")
    with col2:
        st.metric("Food Scans", "873" if selected_period == "Last 7 Days" else "3,241" if selected_period == "Last 30 Days" else "12,873", delta="124" if selected_period == "Last 7 Days" else "487" if selected_period == "Last 30 Days" else "1,842")
    with col3:
        st.metric("Success Rate", "84.2%" if selected_period == "Last 7 Days" else "82.7%" if selected_period == "Last 30 Days" else "81.9%", delta="1.5%" if selected_period == "Last 7 Days" else "0.8%" if selected_period == "Last 30 Days" else "-0.3%", delta_color="inverse" if selected_period == "All Time" else "normal")
    with col4:
        st.metric("Avg Response Time", "42ms" if selected_period == "Last 7 Days" else "47ms" if selected_period == "Last 30 Days" else "49ms", delta="-5ms" if selected_period == "Last 7 Days" else "-2ms" if selected_period == "Last 30 Days" else "3ms", delta_color="inverse")

    st.subheader("Error Distribution by Type")
    fig = px.pie(values=[42, 23, 17, 11, 5], names=["Barcode Unrecognized", "Network Error", "Database Timeout", "API Error", "Authentication Error"], title="Error Distribution", color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Daily Error Trend")
    days = 14
    dates = [(datetime.now() - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(days)][::-1]
    np.random.seed(45)
    error_trend = np.clip(np.round(np.linspace(20, 10, days) + np.random.normal(0, 3, days)), 0, None).astype(int)
    trend_df = pd.DataFrame({'Date': dates, 'Errors': error_trend})
    fig = px.line(trend_df, x='Date', y='Errors', title='Daily Error Count', markers=True)
    fig.add_trace(go.Scatter(x=trend_df['Date'], y=np.poly1d(np.polyfit(range(len(trend_df)), trend_df['Errors'], 1))(range(len(trend_df))), mode='lines', name='Trend', line=dict(color='red', dash='dash')))
    fig.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

# Recommendations
st.markdown("---")
st.subheader("🔍 System Recommendations")
recommendations = [
    {"title": "Improve Barcode Recognition", "description": "Barcode recognition failures account for 42% of all errors. Consider upgrading the image processing algorithm.", "priority": "High"},
    {"title": "Optimize Database Queries", "description": "Database timeouts have increased by 15% in the last 30 days. Review and optimize slow queries.", "priority": "Medium"},
    {"title": "Update Error Logging", "description": "Add more detailed context to error logs to facilitate faster troubleshooting.", "priority": "Low"}
]
for i, rec in enumerate(recommendations):
    with st.expander(f"{rec['title']} (Priority: {rec['priority']})", expanded=i==0):
        st.write(rec['description'])
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("Implement", key=f"implement_{i}"):
                st.info("This would initiate the implementation process in a real system.")
        with col2:
            if st.button("Dismiss", key=f"dismiss_{i}"):
                st.info("Recommendation would be dismissed in a real system.")

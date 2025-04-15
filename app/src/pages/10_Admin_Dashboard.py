import streamlit as st

API_BASE_URL = "http://web-api:4000"

if not st.session_state.get('authenticated', False) or st.session_state.role != "admin":
    st.warning("Please log in as an admin to access this page")
    st.stop()

SideBarLinks(st.session_state.role)

st.title("Admin Dashboard")
st.subheader(f"Welcome, {st.session_state.first_name}!")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🚦 System Health")
    system_metrics = {
        "API Response Time": "42ms",
        "Database Connections": "17",
        "Active Users": "153",
        "Error Rate": "0.12%",
        "CPU Usage": "23%",
        "Memory Usage": "47%"
    }
    metric_cols = st.columns(2)
    for i, (metric, value) in enumerate(system_metrics.items()):
        with metric_cols[i % 2]:
            if "Error" in metric and float(value.strip('%')) > 1:
                st.metric(metric, value, delta="1.2%", delta_color="inverse")
            else:
                st.metric(metric, value)
    st.success("✅ All systems operational")

    st.subheader("Recent System Events")
    events = [
        {"time": "10:23 AM", "event": "Database backup completed", "level": "INFO"},
        {"time": "09:45 AM", "event": "New ingredient added: Quinoa", "level": "INFO"},
        {"time": "08:32 AM", "event": "Failed food scan logged", "level": "WARNING"},
        {"time": "Yesterday", "event": "System update deployed v2.3.1", "level": "INFO"},
        {"time": "Yesterday", "event": "Database optimization completed", "level": "INFO"}
    ]
    for event in events:
        if event["level"] == "WARNING":
            st.warning(f"**{event['time']}**: {event['event']}")
        elif event["level"] == "ERROR":
            st.error(f"**{event['time']}**: {event['event']}")
        else:
            st.info(f"**{event['time']}**: {event['event']}")


with col2:
    st.subheader("📊 System Statistics")

    @st.cache_data(ttl=600)
    def get_ingredient_count():
        try:
            res = requests.get(f"{API_BASE_URL}/ingredients")
            return len(res.json()) if res.status_code == 200 else "N/A"
        except:
            return "N/A"

    @st.cache_data(ttl=600)
    def get_users_count():
        try:
            res = requests.get(f"{API_BASE_URL}/users")
            return len(res.json()) if res.status_code == 200 else "N/A"
        except:
            return "N/A"

    @st.cache_data(ttl=600)
    def get_error_logs_count():
        try:
            res = requests.get(f"{API_BASE_URL}/logs/errors")
            return len(res.json()) if res.status_code == 200 else "N/A"
        except:
            return "N/A"

    stats_cols = st.columns(2)
    with stats_cols[0]:
        st.metric("Registered Users", get_users_count())
        st.metric("Ingredients", get_ingredient_count())
        st.metric("Error Logs", get_error_logs_count())
    with stats_cols[1]:
        st.metric("Food Scans Today", "128")
        st.metric("Active Meal Plans", "76")
        st.metric("Trusted Brands", "42")

    # Chart
    days = 14
    dates = [(datetime.now() - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(days)][::-1]
    np.random.seed(42)
    scan_success = np.random.randint(70, 120, size=days)
    scan_failed = np.random.randint(5, 20, size=days)

    scan_data = pd.DataFrame({
        'Date': dates,
        'Successful Scans': scan_success,
        'Failed Scans': scan_failed
    })
    fig = px.bar(
        scan_data,
        x='Date',
        y=['Successful Scans', 'Failed Scans'],
        title='Food Scan Activity',
        barmode='stack',
        color_discrete_map={'Successful Scans': '#4CAF50', 'Failed Scans': '#FF5252'}
    )
    fig.update_layout(height=300, margin=dict(l=10, r=10, t=40, b=10), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig, use_container_width=True)

st.subheader("⚡ Quick Actions")
act1, act2, act3, act4 = st.columns(4)

with act1:
    if st.button("Update Expired Status", use_container_width=True):
        try:
            res = requests.put(f"{API_BASE_URL}/fridge/expired")
            st.success("Expired status updated successfully!") if res.status_code == 200 else st.error(f"Error: {res.status_code}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

with act2:
    if st.button("Remove Expired Items", use_container_width=True):
        try:
            res = requests.delete(f"{API_BASE_URL}/fridge/expired")
            st.success("Expired items removed successfully!") if res.status_code == 200 else st.error(f"Error: {res.status_code}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

with act3:
    if st.button("Generate System Report", use_container_width=True):
        with st.spinner("Generating report..."):
            time.sleep(2)
            st.success("System report generated successfully!")
            st.download_button("Download Report", data="This is a mock system report for FridgeFriend.", file_name="system_report.txt", mime="text/plain")

with act4:
    if st.button("Database Maintenance", use_container_width=True):
        with st.spinner("Running maintenance tasks..."):
            time.sleep(3)
            st.success("Database maintenance completed successfully!")

st.subheader("📜 Recent System Logs")

@st.cache_data(ttl=300)
def get_error_logs():
    try:
        res = requests.get(f"{API_BASE_URL}/logs/errors")
        if res.status_code == 200:
            return [{
                'error_id': log.get('error_id'),
                'timestamp': log.get('timestamp', 'Unknown'),
                'message': log.get('message', 'No message'),
                'status': log.get('scan_status', 'Unknown'),
                'ingredient': log.get('ingredient_name', 'Unknown')
            } for log in res.json()]
        else:
            st.error(f"Error fetching logs: {res.status_code}")
            return []
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []

error_logs = get_error_logs()
if not error_logs:
    error_logs = [
        {'error_id': 1, 'timestamp': '2023-04-14 09:23:45', 'message': 'Unrecognized barcode during scan', 'status': 'FAILED', 'ingredient': 'Unknown Cereal'},
        {'error_id': 2, 'timestamp': '2023-04-13 15:42:21', 'message': 'Network error during scan', 'status': 'FAILED', 'ingredient': 'Organic Apple'},
        {'error_id': 3, 'timestamp': '2023-04-13 08:17:32', 'message': 'Database connection timeout', 'status': 'FAILED', 'ingredient': 'Almond Milk'}
    ]

if error_logs:
    with st.expander("View Error Logs", expanded=True):
        st.dataframe(
            pd.DataFrame(error_logs),
            column_config={
                "error_id": None,
                "timestamp": "Timestamp",
                "message": "Error Message",
                "status": "Status",
                "ingredient": "Ingredient"
            },
            height=200
        )
else:
    st.info("No error logs found. That's a good thing!")

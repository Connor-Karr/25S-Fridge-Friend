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

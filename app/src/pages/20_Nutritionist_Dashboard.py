import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from modules.nav import SideBarLinks

# Authentication check
if not st.session_state.get('authenticated', False) or st.session_state.role != "nutritionist":
    st.warning("Please log in as Nancy to access this page")
    st.stop()

# Set up navigation
SideBarLinks(st.session_state.role)

# Define API endpoints
API_BASE_URL = "http://web-api:4000"
CLIENTS_ENDPOINT = f"{API_BASE_URL}/users"
MEAL_PLANS_ENDPOINT = f"{API_BASE_URL}/meal_plans"

# Page header
st.title("Nutritionist Dashboard")
st.subheader(f"Welcome, {st.session_state.first_name}!")

# Get clients from API
def get_clients():
    try:
        response = requests.get(CLIENTS_ENDPOINT)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching clients: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return []

# Get meal plans from API
def get_client_meal_plans(client_id):
    try:
        response = requests.get(f"{MEAL_PLANS_ENDPOINT}?client_id={client_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching meal plans: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return []

# Get clients
clients = get_clients()

# Display clients in a table
if clients:
    # Create DataFrame for display
    client_data = []
    for client in clients:
        # Convert client data to match database structure
        client_data.append({
            "ID": client.get("user_id"),
            "Name": f"{client.get('f_name', '')} {client.get('l_name', '')}",
            "Email": client.get("email", ""),
            "Status": "Active"
        })
    
    clients_df = pd.DataFrame(client_data)
    
    # Create a simple layout
    col1, col2 = st.columns([2, 1])
    
    # Display client table
    with col1:
        st.header("Your Clients")
        st.table(clients_df)
    
    # Today's appointments
    with col2:
        st.header("Today's Appointments")
        # This would come from a real API in a production app
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Placeholder data - in production, this would come from an API
        appointments = [
            {"time": "9:00 AM", "client": clients[0]["f_name"], "type": "Check-in"},
            {"time": "11:30 AM", "client": clients[1]["f_name"] if len(clients) > 1 else "New Client", "type": "Meal Plan Review"},
        ]
        
        for appt in appointments:
            st.info(f"**{appt['time']}** - {appt['client']} ({appt['type']})")
else:
    st.info("No clients found. Please check your API connection.")

# Client alerts section
st.header("Client Alerts")

# In a real app, this would come from an API endpoint like "/alerts"
# For now, we'll create simple alerts for demonstration purposes
alerts = []
for i, client in enumerate(clients[:3]):  # Limit to first 3 clients for demo
    if i == 0:
        alerts.append({"client": f"{client.get('f_name', '')} {client.get('l_name', '')}", 
                      "alert": "Needs updated meal plan", 
                      "priority": "Medium"})
    elif i == 1:
        alerts.append({"client": f"{client.get('f_name', '')} {client.get('l_name', '')}", 
                      "alert": "Low protein intake detected", 
                      "priority": "High"})
    else:
        alerts.append({"client": f"{client.get('f_name', '')} {client.get('l_name', '')}", 
                      "alert": "Missing food logs for past 2 days", 
                      "priority": "Low"})

# Display alerts with color coding
for alert in alerts:
    if alert["priority"] == "High":
        st.error(f"**{alert['client']}:** {alert['alert']} (Priority: {alert['priority']})")
    elif alert["priority"] == "Medium":
        st.warning(f"**{alert['client']}:** {alert['alert']} (Priority: {alert['priority']})")
    else:
        st.info(f"**{alert['client']}:** {alert['alert']} (Priority: {alert['priority']})")

# Quick Actions section
st.header("Quick Actions")

# Simple layout for buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Create Meal Plan", use_container_width=True):
        st.switch_page("pages/22_Meal_Planning.py")

with col2:
    if st.button("View Analytics", use_container_width=True):
        st.switch_page("pages/23_Nutrition_Analytics.py")

# Recent Activities section
st.header("Recent Activities")

# In a real app, this would come from an API endpoint like "/activities" or "/logs"
activities_data = []
for i, client in enumerate(clients[:5]):  # Use up to 5 clients for demo
    client_name = f"{client.get('f_name', '')} {client.get('l_name', '')}"
    
    if i == 0:
        activities_data.append({"time": "Today", "activity": f"Created new meal plan for {client_name}"})
    elif i == 1:
        activities_data.append({"time": "Yesterday", "activity": f"Updated dietary restrictions for {client_name}"})
    elif i == 2:
        activities_data.append({"time": "Yesterday", "activity": f"Added new client: {client_name}"})
    elif i == 3:
        activities_data.append({"time": "2 days ago", "activity": f"Generated nutrition report for {client_name}"})
    elif i == 4:
        activities_data.append({"time": "2 days ago", "activity": f"Updated macronutrient goals for {client_name}"})

# Create activities DataFrame and display
activities_df = pd.DataFrame(activities_data)
if not activities_df.empty:
    st.table(activities_df)
else:
    st.info("No recent activities found.")
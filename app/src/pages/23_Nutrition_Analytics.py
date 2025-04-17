import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

# Authentication check
if not st.session_state.get('authenticated', False) or st.session_state.role != "nutritionist":
    st.warning("Please log in as a nutritionist to access this page")
    st.stop()

# Set up navigation
SideBarLinks(st.session_state.role)

# API base URL
API_BASE_URL = "http://web-api:4000"

# Page header
st.title("Nutrition Analytics")
st.write("Analyze nutritional data across clients")

# Function to get clients for this nutritionist
def get_clients(advisor_id=2):  # Default to Nancy (advisor_id=2)
    try:
        response = requests.get(f"{API_BASE_URL}/users/nutritionist/{advisor_id}/clients")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error fetching clients: {str(e)}")
        return []

# Function to get nutrition logs for a specific client
def get_nutrition_logs(client_id):
    try:
        response = requests.get(f"{API_BASE_URL}/logs/nutrition/{client_id}")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error fetching nutrition logs: {str(e)}")
        return []

# Function to get nutrition summary for all clients
def get_nutrition_summary(advisor_id=2):
    try:
        response = requests.get(f"{API_BASE_URL}/users/nutritionist/{advisor_id}/nutrition-summary")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error fetching nutrition summary: {str(e)}")
        return []

# Get data
clients = get_clients()
nutrition_summary = get_nutrition_summary()

# Simple time period selector for analysis context
st.subheader("Analysis Period")
time_period = st.selectbox(
    "Select time period:",
    ["Last 30 Days", "Last 3 Months", "Last 6 Months", "Year to Date"]
)

# Main content in two sections
st.markdown("---")

# Section 1: Nutrition Summary by Diet Type
st.subheader("Nutrition Summary by Diet Type")

if nutrition_summary:
    # Convert to DataFrame for display
    summary_df = pd.DataFrame(nutrition_summary)

    # Display as table
    if 'diet_type' in summary_df.columns:
        # Clean up column names for display
        display_cols = []
        display_names = {}
        
        if 'diet_type' in summary_df.columns:
            display_cols.append('diet_type')
            display_names['diet_type'] = 'Diet Type'
        if 'avg_protein' in summary_df.columns:
            display_cols.append('avg_protein')
            display_names['avg_protein'] = 'Avg. Protein (g)'
        if 'avg_carbs' in summary_df.columns:
            display_cols.append('avg_carbs')
            display_names['avg_carbs'] = 'Avg. Carbs (g)'
        if 'avg_fat' in summary_df.columns:
            display_cols.append('avg_fat')
            display_names['avg_fat'] = 'Avg. Fat (g)'
            
        if display_cols:
            display_df = summary_df[display_cols].copy()
            display_df.rename(columns=display_names, inplace=True)
            st.table(display_df)
        else:
            st.table(summary_df)
    else:
        st.table(summary_df)
else:
    st.info("No nutrition summary data available.")

# Section 2: Client Nutrition Details
st.markdown("---")
st.subheader("Client Nutrition Details")

if clients:
    # Create client selection dropdown
    client_options = []
    client_id_map = {}
    
    for client in clients:
        if 'f_name' in client and 'l_name' in client and 'client_id' in client:
            name = f"{client['f_name']} {client['l_name']}"
            client_options.append(name)
            client_id_map[name] = client['client_id']
    
    if client_options:
        selected_client = st.selectbox("Select client to view details:", client_options)
        client_id = client_id_map.get(selected_client)
        
        if client_id:
            # Get nutrition logs for selected client
            nutrition_logs = get_nutrition_logs(client_id)
            
            if nutrition_logs:
                # Convert to DataFrame for display
                logs_df = pd.DataFrame(nutrition_logs)
                
                # Clean up column names for better display
                display_cols = []
                display_names = {}
                
                for col in logs_df.columns:
                    if col in ['tracking_id', 'client_id']:
                        continue  # Skip these columns
                    display_cols.append(col)
                    if col == 'protein':
                        display_names[col] = 'Protein (g)'
                    elif col == 'fat':
                        display_names[col] = 'Fat (g)'
                    elif col == 'carbs':
                        display_names[col] = 'Carbs (g)'
                    elif col == 'fiber':
                        display_names[col] = 'Fiber (g)'
                    elif col == 'sodium':
                        display_names[col] = 'Sodium (mg)'
                    elif col == 'calories':
                        display_names[col] = 'Calories'
                    else:
                        # Convert snake_case to Title Case
                        display_names[col] = ' '.join(word.capitalize() for word in col.split('_'))
                
                if display_cols:
                    display_df = logs_df[display_cols].copy()
                    display_df.rename(columns=display_names, inplace=True)
                    st.table(display_df)
                else:
                    st.table(logs_df)
            else:
                st.info(f"No nutrition logs available for {selected_client}.")
    else:
        st.info("No clients available with proper data structure.")
else:
    st.info("No clients found.")
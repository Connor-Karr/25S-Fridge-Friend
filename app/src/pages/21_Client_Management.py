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
st.title("Client Management")

# We know advisor_id=2 is Nancy from Home.py
advisor_id = 2

# Function to get all clients for a nutritionist
def get_clients(advisor_id):
    try:
        response = requests.get(f"{API_BASE_URL}/users/nutritionist/{advisor_id}/clients")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error fetching clients: {str(e)}")
        return []

# Function to get nutrition tracking data
def get_nutrition_data(client_id):
    try:
        response = requests.get(f"{API_BASE_URL}/logs/nutrition/{client_id}")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error fetching nutrition data: {str(e)}")
        return []

# Function to update user constraints
def update_constraints(pc_id, data):
    try:
        response = requests.put(f"{API_BASE_URL}/users/constraints/{pc_id}", json=data)
        return response.status_code == 200
    except Exception as e:
        st.error(f"Error updating constraints: {str(e)}")
        return False

# Function to create user constraints silently
def create_constraints(client_id):
    try:
        default_constraints = {
            "budget": 100,
            "dietary_restrictions": "none",
            "personal_diet": "balanced",
            "age_group": "adult",
            "client_id": client_id
        }
        
        response = requests.post(f"{API_BASE_URL}/users/constraints", json=default_constraints)
        if response.status_code == 201:
            result = response.json()
            return result.get("pc_id")
        return None
    except Exception as e:
        return None

# Get all clients
clients = get_clients(advisor_id)

# Display all clients in a table
if clients:
    # Create a DataFrame for better display
    clients_df = pd.DataFrame(clients)
    
    # Prepare client names if first name and last name are available
    if 'f_name' in clients_df.columns and 'l_name' in clients_df.columns:
        clients_df['client_name'] = clients_df['f_name'] + ' ' + clients_df['l_name']
    
    # Display the table with all clients
    st.markdown("### All Clients")
    
    # Select columns to display and rename them for better readability
    display_cols = []
    if 'client_name' in clients_df.columns:
        display_cols.append('client_name')
    if 'age_group' in clients_df.columns:
        display_cols.append('age_group')
    if 'personal_diet' in clients_df.columns:
        display_cols.append('personal_diet')
    if 'dietary_restrictions' in clients_df.columns:
        display_cols.append('dietary_restrictions')
    if 'budget' in clients_df.columns:
        display_cols.append('budget')
    
    if display_cols:
        display_df = clients_df[display_cols].copy()
        
        # Rename columns for better readability
        column_map = {
            'client_name': 'Client Name',
            'age_group': 'Age Group',
            'personal_diet': 'Diet Type',
            'dietary_restrictions': 'Dietary Restrictions',
            'budget': 'Budget ($)'
        }
        display_df.rename(columns=column_map, inplace=True)
        
        st.table(display_df)
    else:
        # If we didn't find expected columns, just show what we have
        st.table(clients_df)
else:
    st.info("No clients found for this nutritionist.")

# Create a section to select a client and make changes
st.markdown("---")
st.markdown("### Update Client Information")

# Create a dropdown to select a client
client_options = []
if clients:
    for client in clients:
        client_id = client.get('client_id', '')
        
        # Format the client name
        if 'f_name' in client and 'l_name' in client:
            name = f"{client['f_name']} {client['l_name']}"
        else:
            name = f"Client {client_id}"
            
        client_options.append({"id": client_id, "name": name, "pc_id": client.get('pc_id')})

if client_options:
    # Convert client options to format for selectbox
    client_names = [c["name"] for c in client_options]
    client_ids = [c["id"] for c in client_options]
    pc_ids = [c["pc_id"] for c in client_options]
    
    # Create a mapping of names to IDs
    selected_index = st.selectbox("Select a client to update:", range(len(client_names)), format_func=lambda i: client_names[i])
    
    selected_client_id = client_ids[selected_index]
    selected_pc_id = pc_ids[selected_index]
    
    # Once a client is selected, show update options
    if selected_client_id:
        st.markdown(f"**Updating information for: {client_names[selected_index]}**")
        
        # Silently create constraints if needed
        if not selected_pc_id:
            selected_pc_id = create_constraints(selected_client_id)
        
        # Create sections for different types of updates, all visible by default
        st.markdown("### Update Dietary Preferences")
        with st.form("update_diet_form"):
            new_diet = st.selectbox(
                "Diet Type:",
                ["balanced", "low-carb", "high-protein", "keto", "mediterranean", "vegan", "vegetarian"]
            )
            
            new_restrictions = st.text_input(
                "Dietary Restrictions (comma-separated):"
            )
            
            update_diet_button = st.form_submit_button("Update Diet")
            
            if update_diet_button and selected_pc_id:
                # Prepare data for update
                diet_data = {
                    "personal_diet": new_diet,
                    "dietary_restrictions": new_restrictions
                }
                
                # Update constraints
                success = update_constraints(selected_pc_id, diet_data)
                
                if success:
                    st.success("Dietary preferences updated successfully!")
                else:
                    st.error("Failed to update dietary preferences.")
        
        st.markdown("### Log Nutrition Data")
        with st.form("log_nutrition_form"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                protein = st.number_input("Protein (g):", min_value=0.0, value=0.0)
                fat = st.number_input("Fat (g):", min_value=0.0, value=0.0)
            
            with col2:
                fiber = st.number_input("Fiber (g):", min_value=0.0, value=0.0)
                sodium = st.number_input("Sodium (mg):", min_value=0.0, value=0.0)
            
            with col3:
                calories = st.number_input("Calories:", min_value=0, value=0)
                carbs = st.number_input("Carbs (g):", min_value=0.0, value=0.0)
            
            log_nutrition_button = st.form_submit_button("Log Nutrition")
            
            if log_nutrition_button:
                # Prepare nutrition data
                nutrition_entry = {
                    "client_id": selected_client_id,
                    "protein": protein,
                    "fat": fat,
                    "fiber": fiber,
                    "sodium": sodium,
                    "vitamins": 0,  # Default value
                    "calories": calories,
                    "carbs": carbs
                }
                
                # Call API to create nutrition log
                try:
                    response = requests.post(f"{API_BASE_URL}/logs/nutrition", json=nutrition_entry)
                    if response.status_code == 201:
                        st.success("Nutrition entry logged successfully!")
                    else:
                        st.error(f"Failed to log nutrition entry: {response.status_code}")
                except Exception as e:
                    st.error(f"Error logging nutrition entry: {str(e)}")
        
        st.markdown("### Nutrition History")
        # Get nutrition data for the selected client
        nutrition_data = get_nutrition_data(selected_client_id)
        
        if nutrition_data:
            # Convert to DataFrame for better display
            nutrition_df = pd.DataFrame(nutrition_data)
            
            # Rename columns for better display if needed
            column_map = {
                'tracking_id': 'ID',
                'client_id': 'Client ID',
                'protein': 'Protein (g)',
                'fat': 'Fat (g)',
                'fiber': 'Fiber (g)',
                'sodium': 'Sodium (mg)',
                'vitamins': 'Vitamins',
                'calories': 'Calories',
                'carbs': 'Carbs (g)'
            }
            
            # Only rename columns that exist in the DataFrame
            rename_cols = {k: v for k, v in column_map.items() if k in nutrition_df.columns}
            if rename_cols:
                nutrition_df.rename(columns=rename_cols, inplace=True)
            
            st.table(nutrition_df)
        else:
            st.info("No nutrition data available for this client.")
        
        st.markdown("### Update Budget")
        with st.form("update_budget_form"):
            new_budget = st.number_input("Weekly Budget ($):", min_value=50.0, max_value=500.0, value=100.0, step=10.0)
            
            update_budget_button = st.form_submit_button("Update Budget")
            
            if update_budget_button and selected_pc_id:
                # Prepare data for update
                budget_data = {
                    "budget": new_budget
                }
                
                # Update constraints
                success = update_constraints(selected_pc_id, budget_data)
                
                if success:
                    st.success("Budget updated successfully!")
                else:
                    st.error("Failed to update budget.")
else:
    st.info("No clients available to update.")
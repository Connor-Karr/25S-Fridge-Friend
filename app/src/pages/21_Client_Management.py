import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
from modules.nav import SideBarLinks

# Authentication check
if not st.session_state.get('authenticated', False) or st.session_state.role != "nutritionist":
    st.warning("Please log in as Nancy to access this page")
    st.stop()

SideBarLinks(st.session_state.role)

# Define API endpoints
API_BASE_URL = "http://web-api:4000"
USERS_ENDPOINT = f"{API_BASE_URL}/users"
MEAL_PLANS_ENDPOINT = f"{API_BASE_URL}/meal_plans"
MACROS_ENDPOINT = f"{API_BASE_URL}/macros"
CONSTRAINTS_ENDPOINT = f"{API_BASE_URL}/users/constraints"

# Get selected client ID from session state
selected_client_id = st.session_state.get('selected_client_id', None)

# Function to get user data
def get_user(user_id):
    try:
        response = requests.get(f"{USERS_ENDPOINT}/{user_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching user: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"API connection error: {str(e)}")
        return None

# Function to get user constraints
def get_user_constraints(pc_id):
    try:
        response = requests.get(f"{CONSTRAINTS_ENDPOINT}/{pc_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching constraints: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"API connection error: {str(e)}")
        return None

# Function to get all users
def get_all_users():
    try:
        response = requests.get(USERS_ENDPOINT)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching users: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"API connection error: {str(e)}")
        return []

# Function to get meal plans for client
def get_client_meal_plans(client_id):
    try:
        response = requests.get(f"{MEAL_PLANS_ENDPOINT}?client_id={client_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching meal plans: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"API connection error: {str(e)}")
        return []

# Main page content
if selected_client_id:
    # Get client data from API
    client = get_user(selected_client_id)
    
    if client:
        st.title(f"Client Profile: {client.get('f_name', '')} {client.get('l_name', '')}")
        
        # Create tabs for different sections
        tab1, tab2, tab3 = st.tabs(["Basic Info", "Nutrition Plan", "Progress"])
        
        # Basic Info Tab
        with tab1:
            st.header("Client Information")
            
            # Get constraints for this client
            constraints = None
            if 'pc_id' in client:
                constraints = get_user_constraints(client['pc_id'])
            
            # Create a simple table with client details
            client_info = {
                "Field": ["Email", "Username", "Dietary Restrictions", "Diet Type", "Age Group", "Budget"],
                "Value": [
                    client.get('email', 'N/A'),
                    client.get('username', 'N/A'),
                    constraints.get('dietary_restrictions', 'N/A') if constraints else 'N/A',
                    constraints.get('personal_diet', 'N/A') if constraints else 'N/A',
                    constraints.get('age_group', 'N/A') if constraints else 'N/A',
                    f"${constraints.get('budget', 'N/A')}" if constraints else 'N/A'
                ]
            }
            
            client_df = pd.DataFrame(client_info)
            st.table(client_df)
            
            # Calculate basic nutrition targets based on constraints
            if constraints:
                # Simple calculation based on diet type
                diet_type = constraints.get('personal_diet', 'balanced').lower()
                age_group = constraints.get('age_group', 'adult').lower()
                
                # Set base values
                calorie_target = 2000
                protein_target = 100
                carb_target = 250
                fat_target = 65
                
                # Adjust based on diet type
                if 'low-carb' in diet_type:
                    carb_target = 100
                    fat_target = 85
                elif 'high-protein' in diet_type:
                    protein_target = 150
                    carb_target = 200
                elif 'keto' in diet_type:
                    carb_target = 50
                    fat_target = 120
                
                # Adjust based on age group
                if age_group == 'teen':
                    calorie_target += 200
                elif age_group == 'child':
                    calorie_target -= 400
                    protein_target = int(protein_target * 0.7)
                elif age_group == 'older-adult':
                    calorie_target -= 200
                
                # Display nutrition targets
                st.header("Nutrition Targets")
                targets_data = {
                    "Target": ["Calories", "Protein", "Carbohydrates", "Fat"],
                    "Daily Amount": [
                        f"{calorie_target} kcal",
                        f"{protein_target} g",
                        f"{carb_target} g",
                        f"{fat_target} g"
                    ]
                }
                
                targets_df = pd.DataFrame(targets_data)
                st.table(targets_df)
        
        # Nutrition Plan Tab
        with tab2:
            st.header("Daily Meal Plan")
            
            # Get meal plans for this client
            meal_plans = get_client_meal_plans(selected_client_id)
            
            if meal_plans:
                # Create a table for the meal plan
                meal_data = []
                for meal in meal_plans:
                    meal_data.append({
                        "Meal": f"Meal {meal.get('meal_id', '')}",
                        "Recipe": meal.get('recipe_name', 'Unknown Recipe'),
                        "Quantity": meal.get('quantity', 1),
                        "Instructions": meal.get('instructions', '')[:50] + "..." if meal.get('instructions', '') else "N/A"
                    })
                
                meal_df = pd.DataFrame(meal_data)
                st.table(meal_df)
                
                # Show meal plan details
                for meal in meal_plans:
                    with st.expander(f"Details for {meal.get('recipe_name', 'Meal')}"):
                        st.write(f"Recipe ID: {meal.get('recipe_id', 'N/A')}")
                        st.write(f"Quantity: {meal.get('quantity', 'N/A')}")
                        if meal.get('instructions'):
                            st.write("**Instructions:**")
                            st.write(meal.get('instructions'))
            else:
                st.info("No meal plans found. Create a new plan for this client.")
                if st.button("Create Meal Plan"):
                    st.switch_page("pages/22_Meal_Planning.py")
        
        # Progress Tab
        with tab3:
            st.header("Client Progress")
            
            # In a real app, we would fetch nutrition tracking data from an API
            # For now, create example data for the past 6 weeks
            progress_data = []
            
            # Start date (6 weeks ago)
            start_date = datetime.now() - timedelta(weeks=6)
            
            # Generate weekly data based on constraints if available
            for i in range(6):
                week_date = (start_date + timedelta(weeks=i)).strftime('%Y-%m-%d')
                
                # Set metrics based on diet type if constraints exist
                if constraints:
                    diet_type = constraints.get('personal_diet', 'balanced').lower()
                    if 'low-carb' in diet_type:
                        carbs = f"{100 + i * 5}g"
                        compliance = f"{75 + i * 3}%"
                    elif 'high-protein' in diet_type:
                        carbs = f"{200 + i * 5}g"
                        compliance = f"{80 + i * 3}%"
                    elif 'keto' in diet_type:
                        carbs = f"{50 + i * 2}g"
                        compliance = f"{70 + i * 4}%"
                    else:  # balanced
                        carbs = f"{250 + i * 5}g"
                        compliance = f"{85 + i * 2}%"
                else:
                    carbs = f"{200 + i * 5}g"
                    compliance = f"{80 + i * 3}%"
                
                progress_data.append({
                    "Week": week_date,
                    "Protein": f"{100 + i * 5}g",
                    "Carbs": carbs,
                    "Plan Adherence": compliance,
                    "Notes": [
                        "Started program",
                        "Adjusted meal timing",
                        "Increased water consumption",
                        "Added meal prep",
                        "Improved portion control",
                        "Meeting all targets"
                    ][i]
                })
            
            # Create DataFrame and display
            progress_df = pd.DataFrame(progress_data)
            st.table(progress_df)
            
            # Current stats
            st.subheader("Current Status")
            st.info(f"Plan adherence trend: Improving (from {progress_data[0]['Plan Adherence']} to {progress_data[-1]['Plan Adherence']})")
        
        # Go back to client list button
        if st.button("← Back to Client List"):
            st.session_state.selected_client_id = None
            st.rerun()
else:
    # Display the client list
    st.title("Client Management")
    
    # Get all users
    users = get_all_users()
    
    # Simple client search
    search_term = st.text_input("Search by name or email:", placeholder="Enter search term...")
    
    # Filter users based on search term
    if search_term and users:
        filtered_users = [
            user for user in users
            if search_term.lower() in user.get('f_name', '').lower() or
               search_term.lower() in user.get('l_name', '').lower() or
               search_term.lower() in user.get('email', '').lower()
        ]
    else:
        filtered_users = users
    
    # Show filtered client list
    if filtered_users:
        st.subheader(f"Showing {len(filtered_users)} clients")
        
        # Convert clients to DataFrame for table display
        clients_for_display = []
        for user in filtered_users:
            clients_for_display.append({
                "ID": user.get("user_id", ""),
                "Name": f"{user.get('f_name', '')} {user.get('l_name', '')}",
                "Email": user.get("email", ""),
                "Username": user.get("username", "")
            })
        
        clients_df = pd.DataFrame(clients_for_display)
        st.table(clients_df)
        
        # Client selection input
        if filtered_users:
            selected_id = st.selectbox(
                "Select Client to View:",
                options=[user.get("user_id") for user in filtered_users],
                format_func=lambda x: next((
                    f"{user.get('f_name', '')} {user.get('l_name', '')}" 
                    for user in filtered_users 
                    if user.get("user_id") == x
                ), "")
            )
            
            if st.button("View Client"):
                st.session_state.selected_client_id = selected_id
                st.rerun()
    else:
        st.info("No clients found. Please check your API connection or add new clients.")
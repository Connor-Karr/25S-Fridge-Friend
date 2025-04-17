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
st.title("Meal Planning")

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

# Function to get all recipes
def get_recipes():
    try:
        # Using a direct recipe route instead of ingredients
        response = requests.get(f"{API_BASE_URL}/recipes")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error fetching recipes: {str(e)}")
        return []

# Function to get meal plans
def get_meal_plans():
    try:
        response = requests.get(f"{API_BASE_URL}/meal-plans")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error fetching meal plans: {str(e)}")
        return []

# Function to create a meal plan
def create_meal_plan(data):
    try:
        response = requests.post(f"{API_BASE_URL}/meal-plans", json=data)
        return response.status_code == 201
    except Exception as e:
        st.error(f"Error creating meal plan: {str(e)}")
        return False

# Function to update a meal plan
def update_meal_plan(meal_id, data):
    try:
        response = requests.put(f"{API_BASE_URL}/meal-plans/{meal_id}", json=data)
        return response.status_code == 200
    except Exception as e:
        st.error(f"Error updating meal plan: {str(e)}")
        return False

# Function to delete a meal plan
def delete_meal_plan(meal_id):
    try:
        response = requests.delete(f"{API_BASE_URL}/meal-plans/{meal_id}")
        return response.status_code == 200
    except Exception as e:
        st.error(f"Error deleting meal plan: {str(e)}")
        return False

# Get data
clients = get_clients()
recipes = get_recipes()
meal_plans = get_meal_plans()

# Section 1: View Meal Plans
st.subheader("Current Meal Plans")

# Display all meal plans
if meal_plans:
    # Convert to DataFrame
    plans_df = pd.DataFrame(meal_plans)
    
    # Clean up column names for display
    if 'recipe_name' in plans_df.columns:
        display_cols = ['meal_id', 'recipe_name', 'quantity']
        display_names = {'meal_id': 'Meal ID', 'recipe_name': 'Recipe', 'quantity': 'Servings'}
        
        display_df = plans_df[display_cols].copy()
        display_df.rename(columns=display_names, inplace=True)
    else:
        display_df = plans_df
    
    # Display as a table
    st.table(display_df)
else:
    st.info("No meal plans found.")

# Section 2: Create New Meal Plan
st.markdown("---")
st.subheader("Create New Meal Plan")

with st.form("create_meal_plan"):
    # Client selection with dropdown if available
    if clients:
        client_options = []
        pc_id_map = {}
        
        for client in clients:
            if 'client_id' in client and 'f_name' in client and 'l_name' in client and 'pc_id' in client:
                name = f"{client['f_name']} {client['l_name']}"
                client_options.append(name)
                pc_id_map[name] = client['pc_id']
        
        selected_client = st.selectbox("Select Client:", client_options) if client_options else None
        pc_id = pc_id_map.get(selected_client) if selected_client else st.number_input("Personal Constraints ID:", min_value=1, value=1)
    else:
        # Fallback to direct ID input
        pc_id = st.number_input("Personal Constraints ID:", min_value=1, value=1)
    
    # Recipe selection with dropdown if available
    if recipes:
        recipe_options = []
        recipe_id_map = {}
        
        for recipe in recipes:
            if 'recipe_id' in recipe and 'name' in recipe:
                recipe_options.append(recipe['name'])
                recipe_id_map[recipe['name']] = recipe['recipe_id']
        
        selected_recipe = st.selectbox("Select Recipe:", recipe_options) if recipe_options else None
        recipe_id = recipe_id_map.get(selected_recipe) if selected_recipe else st.number_input("Recipe ID:", min_value=1, value=1)
    else:
        # Fallback to direct ID input
        recipe_id = st.number_input("Recipe ID:", min_value=1, value=1)
    
    # Number of servings
    quantity = st.number_input("Number of Servings:", min_value=1, value=1)
    
    # Submit button
    create_submitted = st.form_submit_button("Create Meal Plan")
    
    if create_submitted:
        # Create meal plan data
        meal_plan_data = {
            "pc_id": int(pc_id),
            "recipe_id": int(recipe_id),
            "quantity": int(quantity)
        }
        
        # Submit to API
        if create_meal_plan(meal_plan_data):
            st.success("Meal plan created successfully!")
            st.rerun()

# Section 3: Update/Delete Meal Plan
st.markdown("---")
st.subheader("Update or Delete Meal Plan")

if meal_plans:
    # Option to select from existing meal plans or enter ID directly
    meal_id_options = [plan.get('meal_id') for plan in meal_plans if 'meal_id' in plan]
    
    if meal_id_options:
        meal_id = st.selectbox("Select Meal Plan:", meal_id_options, 
                              format_func=lambda x: f"Meal Plan {x}")
    else:
        meal_id = st.number_input("Meal Plan ID:", min_value=1, value=1)
    
    col1, col2 = st.columns(2)
    
    # Update section
    with col1:
        with st.form("update_meal_plan"):
            st.markdown("**Update Meal Plan**")
            new_quantity = st.number_input("New Number of Servings:", min_value=1, value=1)
            update_submitted = st.form_submit_button("Update")
            
            if update_submitted:
                update_data = {"quantity": new_quantity}
                if update_meal_plan(meal_id, update_data):
                    st.success("Meal plan updated successfully!")
                    st.rerun()
    
    # Delete section
    with col2:
        st.markdown("**Delete Meal Plan**")
        if st.button("Delete Selected Meal Plan"):
            if delete_meal_plan(meal_id):
                st.success("Meal plan deleted successfully!")
                st.rerun()
else:
    st.info("No meal plans available to update or delete.")
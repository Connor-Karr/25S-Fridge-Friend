import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

# API base URL
API_BASE_URL = "http://web-api:4000"

# Authentication check
if not st.session_state.get('authenticated', False) or st.session_state.role != "athlete":
    st.warning("Please log in as an athlete to access this page")
    st.stop()

# Set up navigation
SideBarLinks(st.session_state.role)

# Page header
st.title("🍽️ Athlete Meal Plans")
st.write("Optimize your nutrition with targeted meal plans for different training phases")

# API helper functions
def get_api_data(endpoint):
    """Get data from API with error handling"""
    try:
        response = requests.get(f"{API_BASE_URL}/{endpoint}")
        if response.status_code == 200:
            return response.json()
        else:
            # Don't show error for 404s
            if response.status_code != 404:
                st.error(f"Error fetching data from {endpoint}: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []

def post_api_data(endpoint, data):
    """Post data to API with error handling"""
    try:
        response = requests.post(f"{API_BASE_URL}/{endpoint}", json=data)
        if response.status_code in [200, 201]:
            return response.json(), True
        else:
            st.error(f"Error posting to {endpoint}: {response.status_code}")
            return None, False
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None, False

def delete_api_data(endpoint):
    """Delete data via API with error handling"""
    try:
        response = requests.delete(f"{API_BASE_URL}/{endpoint}")
        if response.status_code == 200:
            return True
        else:
            st.error(f"Error deleting from {endpoint}: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

# Get user data
client_id = st.session_state.get('user_id', 1)

# Create tabs for different sections
tab1, tab2 = st.tabs(["Current Meal Plans", "Add New Plan"])

# Current Meal Plans Tab
with tab1:
    st.subheader("Current Meal Plans")
    
    # Get meal plans
    meal_plans = get_api_data(f"meal-plans?client_id={client_id}")
    
    if meal_plans:
        # Convert to DataFrame for display
        meal_df = pd.DataFrame(meal_plans)
        
        # Display meal plans table
        st.dataframe(
            meal_df,
            column_config={
                "meal_id": "ID",
                "recipe_id": "Recipe ID",
                "recipe_name": "Recipe",
                "quantity": "Servings"
            },
            use_container_width=True
        )
        
        # Allow user to select a meal plan to manage
        if 'meal_id' in meal_df.columns and not meal_df.empty:
            meal_ids = meal_df['meal_id'].tolist()
            
            if meal_ids:
                selected_meal_id = st.selectbox("Select meal plan to manage:", meal_ids)
                
                # Get related recipe name if available
                selected_meal = meal_df[meal_df['meal_id'] == selected_meal_id]
                recipe_name = selected_meal['recipe_name'].iloc[0] if 'recipe_name' in selected_meal.columns and not selected_meal.empty else f"Meal Plan {selected_meal_id}"
                
                # Show details and actions for selected meal plan
                st.subheader(f"Manage: {recipe_name}")
                
                # Allow user to delete the selected meal plan
                if st.button("Remove Meal Plan"):
                    if delete_api_data(f"meal-plans/{selected_meal_id}"):
                        st.success(f"Removed {recipe_name} from your meal plans!")
                        st.rerun()
    else:
        st.info("No meal plans found. You can add a new plan in the 'Add New Plan' tab.")

# Add New Plan Tab
with tab2:
    st.subheader("Add New Meal Plan")
    
    # Fetch available recipes
    recipes = get_api_data("meal-plans/recipes")
    
    if recipes:
        # Get user's personal constraints
        pc_info = None
        
        # Get user information to find pc_id
        client_info = get_api_data(f"users/auth/student/{client_id}")
        
        if client_info and 'data' in client_info and client_info['data']:
            # Extract client's pc_id from the client data if available
            pc_id = 1  # Default to 1
            
            for client_data in client_info['data']:
                if 'client_id' == client_id:
                    pc_id = client_data.get('pc_id', 1)
                    break
        else:
            pc_id = 1  # Default pc_id if we can't find the user's constraints
        
        # Create form for adding a meal plan
        with st.form("add_meal_plan"):
            # Recipe selection
            recipe_options = {}
            for recipe in recipes:
                recipe_id = recipe.get('recipe_id')
                recipe_name = recipe.get('name', f"Recipe {recipe_id}")
                if recipe_id and recipe_name:
                    recipe_options[recipe_name] = recipe_id
            
            selected_recipe = st.selectbox("Select recipe:", list(recipe_options.keys()))
            
            # Quantity input
            quantity = st.number_input("Servings:", min_value=1, value=1, step=1)
            
            # Submit button
            submit = st.form_submit_button("Add Meal Plan")
            
            if submit:
                # Create meal plan data
                meal_plan_data = {
                    "pc_id": pc_id,
                    "recipe_id": recipe_options[selected_recipe],
                    "quantity": quantity
                }
                
                # Post to API
                result, success = post_api_data("meal-plans", meal_plan_data)
                
                if success:
                    st.success(f"Added {selected_recipe} to your meal plans!")
                    st.rerun()
    else:
        st.info("No recipes found. Please contact a nutritionist to add recipes to the system.")

# Nutrition information section
st.markdown("---")
st.subheader("📊 Nutrition Information")

# Simplified nutrition tips in a table
nutrition_data = {
    "Training Phase": ["Base Building", "Build Phase", "Peaking", "Race Week", "Recovery"],
    "Carbs (g/kg)": ["5-6", "6-8", "8-10", "8-12", "5-6"],
    "Protein (g/kg)": ["1.6-1.8", "1.8-2.0", "1.8-2.0", "1.5-1.6", "1.8-2.0"],
    "Fat (g/kg)": ["1.0", "1.0", "0.8", "0.5-0.8", "1.0"],
    "Focus": ["Building habits", "Workout fueling", "Glycogen storage", "Carb loading", "Tissue repair"]
}

# Display nutrition table
nutrition_df = pd.DataFrame(nutrition_data)
st.dataframe(nutrition_df, use_container_width=True, hide_index=True)

# Display client's nutrition logs if available
st.subheader("Your Recent Nutrition")
nutrition_logs = get_api_data(f"logs/nutrition/{client_id}")

if nutrition_logs:
    # Convert to DataFrame and display
    logs_df = pd.DataFrame(nutrition_logs)
    
    # Limit to most recent entries and select relevant columns
    display_cols = [col for col in ['protein', 'carbs', 'fat', 'calories', 'fiber'] if col in logs_df.columns]
    
    if display_cols and not logs_df.empty:
        st.dataframe(
            logs_df[display_cols].head(5),
            column_config={
                "protein": "Protein (g)",
                "carbs": "Carbs (g)",
                "fat": "Fat (g)",
                "calories": "Calories",
                "fiber": "Fiber (g)"
            },
            use_container_width=True
        )
else:
    st.info("No nutrition logs found. Track your nutrition to see your data here.")

# Button to refresh data
if st.button("Refresh Data"):
    st.rerun()
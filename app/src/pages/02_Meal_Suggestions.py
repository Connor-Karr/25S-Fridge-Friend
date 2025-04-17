import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from modules.nav import SideBarLinks

# API base URL
API_BASE_URL = "http://web-api:4000"

# Authentication check
if not st.session_state.get('authenticated', False) or st.session_state.role != "busy_student":
    st.warning("Please log in as a student to access this page")
    st.stop()

# Set up navigation
SideBarLinks(st.session_state.role)

# Page header
st.title("🍲 Meal Suggestions")

# Function to get fridge inventory
def get_fridge_inventory(client_id=1):
    try:
        response = requests.get(f"{API_BASE_URL}/fridge?client_id={client_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []

# Function to get meal plans
def get_meal_plans(client_id=1):
    try:
        response = requests.get(f"{API_BASE_URL}/meal-plans?client_id={client_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []

# Function to get health advisor suggestions
def get_advisor_suggestions(client_id=1):
    try:
        response = requests.get(f"{API_BASE_URL}/users/{client_id}/advisor-suggestions")
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except Exception as e:
        return []

# Get data
inventory = get_fridge_inventory()
meal_plans = get_meal_plans()
advisor_suggestions = get_advisor_suggestions()

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["Your Meals", "Advisor Suggestions", "Fridge Inventory", "Expiring Items"])

# Your Meals Tab
with tab1:
    st.markdown("### 🍽️ Your Meal Plans")
    st.markdown("---")
    
    if meal_plans:
        meals_df = pd.DataFrame(meal_plans)
        if 'recipe_name' in meals_df.columns and 'quantity' in meals_df.columns:
            # Rename columns for better display
            renamed_df = meals_df[['recipe_name', 'quantity']].copy()
            renamed_df.columns = ['Recipe Name', 'Servings']
            st.table(renamed_df)
        else:
            st.info("No meal plans available.")
    else:
        st.info("No meal plans available.")

# Advisor Suggestions Tab
with tab2:
    st.markdown("### 👩‍⚕️ Health Advisor Recommendations")
    st.markdown("---")
    
    if advisor_suggestions:
        suggestions_df = pd.DataFrame(advisor_suggestions)
        if 'recipe_name' in suggestions_df.columns:
            display_cols = ['recipe_name']
            if 'advisor_name' in suggestions_df.columns:
                display_cols.append('advisor_name')
            
            # Rename columns for better display
            renamed_df = suggestions_df[display_cols].copy()
            column_mapping = {
                'recipe_name': 'Recipe Name', 
                'advisor_name': 'Recommended By'
            }
            renamed_df.columns = [column_mapping.get(col, col) for col in display_cols]
            
            st.table(renamed_df)
        else:
            st.info("No advisor recommendations available.")
    else:
        st.info("No advisor recommendations available.")

# Fridge Inventory Tab
with tab3:
    st.markdown("### 🧊 Current Fridge Inventory")
    st.markdown("---")
    
    if inventory:
        inventory_df = pd.DataFrame(inventory)
        
        if 'name' in inventory_df.columns and 'quantity' in inventory_df.columns:
            display_cols = ['name', 'quantity']
            if 'expiration_date' in inventory_df.columns:
                display_cols.append('expiration_date')
            
            # Rename columns for better display
            renamed_df = inventory_df[display_cols].copy()
            column_mapping = {
                'name': 'Ingredient', 
                'quantity': 'Amount',
                'expiration_date': 'Expires On'
            }
            renamed_df.columns = [column_mapping.get(col, col) for col in display_cols]
            
            st.table(renamed_df)
        else:
            st.info("No inventory available.")
    else:
        st.info("No inventory available.")

# Expiring Items Tab
with tab4:
    st.markdown("### ⚠️ Items Expiring Soon")
    st.markdown("---")
    
    if inventory and any('expiration_date' in item for item in inventory):
        today = datetime.now().date()
        expiring_soon = []
        
        for item in inventory:
            if item.get("expiration_date"):
                try:
                    exp_date = datetime.strptime(item["expiration_date"], '%Y-%m-%d').date()
                    days_left = (exp_date - today).days
                    
                    if 0 <= days_left <= 3 and not item.get("is_expired", False):
                        item['days_left'] = days_left
                        expiring_soon.append(item)
                except:
                    pass
        
        if expiring_soon:
            expiring_df = pd.DataFrame(expiring_soon)
            
            # Rename columns for better display
            renamed_df = expiring_df[['name', 'expiration_date', 'days_left']].copy()
            renamed_df.columns = ['Ingredient', 'Expiration Date', 'Days Left']
            
            st.table(renamed_df)
        else:
            st.success("No items expiring soon!")
    else:
        st.info("No expiration data available.")
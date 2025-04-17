import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from modules.nav import SideBarLinks

# Add sidebar navigation
SideBarLinks(st.session_state.role)

# Authentication check
if not st.session_state.get('authenticated', False) or st.session_state.role != "busy_student":
    st.warning("Please log in as Ben to access this page")
    st.stop()

# Get user's client ID (assuming it's stored in session state or using default 1)
CLIENT_ID = st.session_state.get('user_id', 1)

# Try localhost instead of container name since they're port-mapped
API_BASE_URL = "http://localhost:4000"

# Page title
st.title(f"Welcome, {st.session_state.first_name}!")
st.write("Manage your fridge, plan meals, and stay on budget!")

# Expiring Soon section
st.subheader("Expiring Soon")

# Get data directly from the fridge endpoint with client_id
try:
    # The fridge route takes client_id as a query parameter
    response = requests.get(f"{API_BASE_URL}/fridge/?client_id={CLIENT_ID}")
    
    if response.status_code == 200:
        fridge_items = response.json()
        
        # Process items to find those expiring soon
        expiring_items = []
        today = datetime.now().date()
        
        for item in fridge_items:
            # Check if item has expiration date and is not expired
            if item.get('expiration_date') and not item.get('is_expired'):
                try:
                    exp_date = datetime.strptime(item['expiration_date'], '%Y-%m-%d').date()
                    days_left = (exp_date - today).days
                    
                    # Only add if it's expiring within 5 days
                    if 0 <= days_left <= 5:
                        expiring_items.append({
                            "Item": item['name'],
                            "Days Left": days_left,
                            "Quantity": item['quantity']
                        })
                except:
                    pass
        
        # Show expiring items
        if expiring_items:
            # Sort by days left (most urgent first)
            expiring_items.sort(key=lambda x: x['Days Left'])
            st.table(pd.DataFrame(expiring_items))
        else:
            st.success("No items expiring soon! Your fridge is in good shape.")
    else:
        st.error(f"Error fetching data: {response.status_code}")
except Exception as e:
    st.error(f"Error fetching data: {str(e)}")

# Update expired status button
if st.button("Update Expired Status"):
    try:
        # The route to update expired status is a PUT to /fridge/expired
        response = requests.put(f"{API_BASE_URL}/fridge/expired")
        
        if response.status_code == 200:
            st.success("Updated expired item status!")
            st.rerun()
        else:
            st.error(f"Error updating status: {response.status_code}")
    except Exception as e:
        st.error(f"Error updating status: {str(e)}")

# Meal Suggestions section
st.subheader("Quick Meal Ideas")

try:
    # The meal_plans route takes client_id as a query parameter
    response = requests.get(f"{API_BASE_URL}/meal_plans/?client_id={CLIENT_ID}")
    
    if response.status_code == 200:
        meal_plans = response.json()
        
        # Display meal suggestions
        if meal_plans:
            # Show top 3 meal suggestions
            meal_suggestions = []
            for meal in meal_plans[:3]:
                meal_suggestions.append({
                    "Meal": meal.get('recipe_name', 'Unknown Recipe'),
                    "Servings": meal.get('quantity', 1),
                    "ID": meal.get('meal_id')
                })
            
            st.table(pd.DataFrame(meal_suggestions))
        else:
            st.info("No meal suggestions available. Add ingredients to your fridge!")
    else:
        st.error(f"Error fetching meal suggestions: {response.status_code}")
except Exception as e:
    st.error(f"Error fetching meal suggestions: {str(e)}")

# Button to see all meal suggestions
if st.button("See All Meal Suggestions"):
    st.switch_page("pages/02_Meal_Suggestions.py")

# Budget Overview section
st.subheader("Budget Overview")

# Budget data with calculation
total_budget = 100.00
used_budget = 62.35
remaining_budget = total_budget - used_budget

budget_data = [
    {"Category": "Total Budget", "Amount": f"${total_budget:.2f}"},
    {"Category": "Used", "Amount": f"${used_budget:.2f}"},
    {"Category": "Remaining", "Amount": f"${remaining_budget:.2f}"}
]

st.table(pd.DataFrame(budget_data))
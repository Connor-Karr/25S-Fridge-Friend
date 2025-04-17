import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
from modules.nav import SideBarLinks

# Add sidebar navigation
SideBarLinks(st.session_state.role)

# Authentication check
if not st.session_state.get('authenticated', False) or st.session_state.role != "busy_student":
    st.warning("Please log in as Ben to access this page")
    st.stop()

# Page title
st.title(f"Welcome, {st.session_state.first_name}!")
st.write("Manage your fridge, plan meals, and stay on budget!")

# Expiring Soon section
st.subheader("Expiring Soon")

# Try to get data from API, but have mock data ready as fallback
try:
    response = requests.get("http://web-api:4000/fridge")
    
    if response.status_code == 200:
        fridge_items = response.json()
        
        # Process items
        expiring_items = []
        today = datetime.now().date()
        
        for item in fridge_items:
            if item.get('expiration_date') and not item.get('is_expired'):
                try:
                    exp_date = datetime.strptime(item['expiration_date'], '%Y-%m-%d').date()
                    days_left = (exp_date - today).days
                    
                    if 0 <= days_left <= 5:
                        expiring_items.append({
                            "Item": item['name'],
                            "Days Left": days_left,
                            "Quantity": item['quantity']
                        })
                except:
                    pass
    else:
        # Use mock data if API call fails
        st.error(f"Error fetching fridge data: {response.status_code}")
        # Mock data for expiring items
        expiring_items = [
            {"Item": "Milk", "Days Left": 2, "Quantity": 1},
            {"Item": "Chicken Breast", "Days Left": 1, "Quantity": 2.5},
            {"Item": "Spinach", "Days Left": 3, "Quantity": 1}
        ]
except Exception as e:
    st.error(f"Error fetching fridge data: {str(e)}")
    # Mock data for expiring items
    expiring_items = [
        {"Item": "Milk", "Days Left": 2, "Quantity": 1},
        {"Item": "Chicken Breast", "Days Left": 1, "Quantity": 2.5},
        {"Item": "Spinach", "Days Left": 3, "Quantity": 1}
    ]

# Display expiring items (either from API or mock data)
if expiring_items:
    # Sort by days left (most urgent first)
    expiring_items.sort(key=lambda x: x['Days Left'])
    st.table(pd.DataFrame(expiring_items))
else:
    st.success("No items expiring soon! Your fridge is in good shape.")

# Update expired status button
if st.button("Update Expired Status"):
    try:
        response = requests.put("http://web-api:4000/fridge/expired")
        
        if response.status_code == 200:
            st.success("Updated expired item status!")
            st.rerun()
        else:
            st.error(f"Error updating status: {response.status_code}")
    except Exception as e:
        st.error(f"Error updating status: {str(e)}")

# Meal Suggestions section
st.subheader("Quick Meal Ideas")

# Try to get data from API, but have mock data ready as fallback
try:
    response = requests.get("http://web-api:4000/meal-plans")
    
    if response.status_code == 200:
        meal_plans = response.json()
        
        # Process meal plans
        meal_suggestions = []
        for meal in meal_plans[:3]:  # Only get top 3
            meal_suggestions.append({
                "Meal": meal.get('recipe_name', 'Unknown Recipe'),
                "Servings": meal.get('quantity', 1),
                "ID": meal.get('meal_id')
            })
    else:
        # Use mock data if API call fails
        st.error(f"Error fetching meal suggestions: {response.status_code}")
        # Mock data for meal suggestions
        meal_suggestions = [
            {"Meal": "Chicken and Rice Bowl", "Servings": 1, "ID": 1},
            {"Meal": "Spinach Salad", "Servings": 2, "ID": 2},
            {"Meal": "Pasta with Tomato Sauce", "Servings": 1, "ID": 3}
        ]
except Exception as e:
    st.error(f"Error fetching meal suggestions: {str(e)}")
    # Mock data for meal suggestions
    meal_suggestions = [
        {"Meal": "Chicken and Rice Bowl", "Servings": 1, "ID": 1},
        {"Meal": "Spinach Salad", "Servings": 2, "ID": 2},
        {"Meal": "Pasta with Tomato Sauce", "Servings": 1, "ID": 3}
    ]

# Display meal suggestions (either from API or mock data)
if meal_suggestions:
    st.table(pd.DataFrame(meal_suggestions))
else:
    st.info("No meal suggestions available. Add ingredients to your fridge!")

# Button to see all meal suggestions
if st.button("See All Meal Suggestions"):
    st.switch_page("pages/02_Meal_Suggestions.py")

# Budget Overview section
st.subheader("Budget Overview")

# Mock data for budget - could be replaced with API call if endpoint exists
total_budget = 100.00
used_budget = 62.35
remaining_budget = total_budget - used_budget

budget_data = [
    {"Category": "Total Budget", "Amount": f"${total_budget:.2f}"},
    {"Category": "Used", "Amount": f"${used_budget:.2f}"},
    {"Category": "Remaining", "Amount": f"${remaining_budget:.2f}"}
]

st.table(pd.DataFrame(budget_data))
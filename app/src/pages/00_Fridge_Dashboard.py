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

# Page title
st.title(f"Welcome, {st.session_state.first_name}!")
st.write("Manage your fridge, plan meals, and stay on budget!")

# Expiring Soon section
st.subheader("Expiring Soon")

try:
    response = requests.get("http://web-api:4000/fridge?client_id=1")
    if response.status_code == 200:
        data = response.json()
        today = datetime.now().date()
        expiring_items = []
        
        for item in data:
            if item.get('expiration_date'):
                try:
                    exp_date = datetime.strptime(item['expiration_date'], '%Y-%m-%d').date()
                    days_left = (exp_date - today).days
                    
                    if 0 <= days_left <= 5 and not item.get('is_expired', False):
                        expiring_items.append({
                            "Item": item['name'],
                            "Days Left": days_left,
                            "Quantity": item.get('quantity', 1)
                        })
                except:
                    pass
        
        if expiring_items:
            st.table(pd.DataFrame(expiring_items))
        else:
            st.success("No items expiring soon! Your fridge is in good shape.")
    else:
        st.error("Error fetching data")
except:
    st.error("Error fetching data")

if st.button("Update Expired Status"):
    try:
        response = requests.put("http://web-api:4000/fridge/expired")
        if response.status_code == 200:
            st.success("Updated expired item status!")
            st.rerun()
        else:
            st.error("Error updating status")
    except:
        st.error("Error updating status")

# Quick Meal Ideas section
st.subheader("Quick Meal Ideas")

try:
    response = requests.get("http://web-api:4000/meal-plans?client_id=1")
    if response.status_code == 200:
        meals = response.json()
        
        if meals:
            meal_data = []
            for meal in meals[:3]:  # Show top 3 suggestions
                meal_data.append({
                    "Meal": meal.get('recipe_name', 'Unknown Recipe'),
                    "Servings": meal.get('quantity', 1),
                    "ID": meal.get('meal_id')
                })
            
            st.table(pd.DataFrame(meal_data))
        else:
            st.info("No meal suggestions available. Add ingredients to your fridge!")
    else:
        st.error("Error fetching meal suggestions")
except:
    st.error("Error fetching meal suggestions")

if st.button("See All Meal Suggestions"):
    st.switch_page("pages/02_Meal_Suggestions.py")

# Budget Overview section
st.subheader("Budget Overview")

# Budget data
budget_data = [
    {"Category": "Total Budget", "Amount": "$100.00"},
    {"Category": "Used", "Amount": "$62.35"},
    {"Category": "Remaining", "Amount": "$37.65"}
]

st.table(pd.DataFrame(budget_data))

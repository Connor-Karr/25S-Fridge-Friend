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
st.title("Leftovers Tracker")
st.write("Track and manage your leftover meals to reduce food waste")

# Create tabs
tab1, tab2 = st.tabs(["Current Leftovers", "Add New Leftover"])

# Current Leftovers Tab
with tab1:
    st.subheader("Current Leftovers")
    
    # Get leftovers data
    try:
        response = requests.get("http://web-api:4000/leftovers")
        if response.status_code == 200:
            data = response.json()
            
            # Process leftover data
            if data:
                leftovers = []
                for item in data:
                    # Calculate days left (assuming leftovers last 5 days)
                    created_date = datetime.now().date() - timedelta(days=1)  # Mock date
                    expire_date = created_date + timedelta(days=5)
                    days_left = (expire_date - datetime.now().date()).days
                    
                    status = "Good"
                    if days_left <= 0 or item.get('is_expired', False):
                        status = "Expired"
                    elif days_left <= 1:
                        status = "Eat Soon"
                    
                    leftovers.append({
                        "ID": item.get('leftover_id'),
                        "Meal": item.get('recipe_name', 'Unknown'),
                        "Servings": item.get('quantity', 1),
                        "Days Left": days_left,
                        "Status": status
                    })
                
                # Group leftovers by status
                expired = [l for l in leftovers if l['Status'] == "Expired"]
                eat_soon = [l for l in leftovers if l['Status'] == "Eat Soon"]
                good = [l for l in leftovers if l['Status'] == "Good"]
                
                # Display summary
                summary_data = [
                    {"Category": "Good", "Count": len(good)},
                    {"Category": "Eat Soon", "Count": len(eat_soon)},
                    {"Category": "Expired", "Count": len(expired)}
                ]
                st.subheader("Leftover Summary")
                st.table(pd.DataFrame(summary_data))
                
                # Display leftovers by group
                if expired:
                    st.subheader("Expired Leftovers")
                    st.table(pd.DataFrame(expired))
                    
                    if st.button("Remove All Expired Leftovers"):
                        try:
                            response = requests.delete("http://web-api:4000/leftovers/expired")
                            if response.status_code == 200:
                                st.success("All expired leftovers removed!")
                                st.rerun()
                            else:
                                st.error("Error removing expired leftovers")
                        except:
                            st.error("Error removing expired leftovers")
                
                if eat_soon:
                    st.subheader("Eat Soon")
                    st.table(pd.DataFrame(eat_soon))
                
                if good:
                    st.subheader("Good Leftovers")
                    st.table(pd.DataFrame(good))
                
                # Update or remove leftover form
                st.subheader("Update or Remove Leftover")
                with st.form("update_leftover_form"):
                    leftover_id = st.number_input("Leftover ID:", min_value=1, step=1)
                    new_quantity = st.number_input("New Quantity (0 to remove):", min_value=0.0, step=0.5)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        update = st.form_submit_button("Update Quantity")
                    with col2:
                        remove = st.form_submit_button("Remove Leftover")
                    
                    if update and new_quantity > 0:
                        try:
                            data = {'quantity': new_quantity}
                            response = requests.put(f"http://web-api:4000/leftovers/{leftover_id}", json=data)
                            
                            if response.status_code == 200:
                                st.success("Leftover updated successfully!")
                                st.rerun()
                            else:
                                st.error("Error updating leftover")
                        except:
                            st.error("Error updating leftover")
                    
                    if update and new_quantity == 0 or remove:
                        try:
                            response = requests.delete(f"http://web-api:4000/leftovers/{leftover_id}")
                            
                            if response.status_code == 200:
                                st.success("Leftover removed successfully!")
                                st.rerun()
                            else:
                                st.error("Error removing leftover")
                        except:
                            st.error("Error removing leftover")
            else:
                st.info("No leftovers tracked. Add some to keep track of your prepared meals!")
        else:
            st.error("Error fetching leftovers")
    except:
        st.error("Error fetching leftovers")

# Add New Leftover Tab
with tab2:
    st.subheader("Add New Leftover Meal")
    
    # Get recipes for dropdown
    try:
        response = requests.get("http://web-api:4000/meal-plans")
        if response.status_code == 200:
            recipes_data = response.json()
            
            if recipes_data:
                # Display available recipes
                recipes = []
                for recipe in recipes_data:
                    recipes.append({
                        "ID": recipe.get('recipe_id'),
                        "Name": recipe.get('recipe_name', 'Unknown Recipe')
                    })
                
                st.subheader("Available Recipes")
                st.table(pd.DataFrame(recipes))
                
                # Add leftover form
                with st.form("add_leftover_form"):
                    recipe_id = st.number_input("Recipe ID:", min_value=1, step=1)
                    quantity = st.number_input("Number of servings:", min_value=0.5, value=1.0, step=0.5)
                    
                    if st.form_submit_button("Add Leftover"):
                        try:
                            data = {
                                'recipe_id': recipe_id,
                                'quantity': quantity
                            }
                            
                            response = requests.post("http://web-api:4000/leftovers", json=data)
                            
                            if response.status_code == 201:
                                st.success("Added leftover successfully!")
                                st.rerun()
                            else:
                                st.error("Error adding leftover")
                        except:
                            st.error("Error adding leftover")
            else:
                st.warning("No recipes available. Add some meal plans first!")
                
                if st.button("Go to Meal Suggestions"):
                    st.switch_page("pages/02_Meal_Suggestions.py")
        else:
            st.error("Error fetching recipes")
    except:
        st.error("Error fetching recipes")
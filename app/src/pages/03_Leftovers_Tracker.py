import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime, timedelta
import json
from modules.nav import SideBarLinks

# API base URL
API_BASE_URL = "http://web-api:4000"

# Authentication check
if not st.session_state.get('authenticated', False) or st.session_state.role != "busy_student":
    st.warning("Please log in as Ben to access this page")
    st.stop()

# Set up navigation
SideBarLinks(st.session_state.role)

# Page header
st.title("🍱 Leftovers Tracker")
st.write("Track and manage your leftover meals to reduce food waste")

# Function to get leftovers
@st.cache_data(ttl=300)
def get_leftovers():
    try:
        response = requests.get(f"{API_BASE_URL}/leftovers")
        
        if response.status_code == 200:
            data = response.json()
            leftovers = []
            
            for item in data:
                # Calculate days left (assuming leftovers last 5 days)
                # In a real app, this would come from the API
                created_date = datetime.now().date() - timedelta(days=1)  # Mock date
                expire_date = created_date + timedelta(days=5)
                days_left = (expire_date - datetime.now().date()).days
                
                leftovers.append({
                    'id': item.get('leftover_id'),
                    'name': item.get('recipe_name', 'Unknown'),
                    'quantity': item.get('quantity', 1),
                    'is_expired': item.get('is_expired', False),
                    'created_date': created_date.strftime('%Y-%m-%d'),
                    'days_left': days_left
                })
            
            return leftovers
        else:
            st.error(f"Error fetching leftovers: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []

# Function to update leftover quantity
def update_leftover(leftover_id, new_quantity):
    try:
        data = {'quantity': new_quantity}
        response = requests.put(f"{API_BASE_URL}/leftovers/{leftover_id}", json=data)
        
        if response.status_code == 200:
            st.success("Leftover updated successfully!")
            st.cache_data.clear()
            return True
        else:
            st.error(f"Error updating leftover: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

# Function to remove a leftover
def remove_leftover(leftover_id):
    try:
        response = requests.delete(f"{API_BASE_URL}/leftovers/{leftover_id}")
        
        if response.status_code == 200:
            st.success("Leftover removed successfully!")
            st.cache_data.clear()
            return True
        else:
            st.error(f"Error removing leftover: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

# Get all leftovers
leftovers = get_leftovers()

# Create two tabs
tab1, tab2 = st.tabs(["Current Leftovers", "Add New Leftover"])

# Current Leftovers Tab
with tab1:
    if not leftovers:
        st.info("No leftovers tracked. Add some to keep track of your prepared meals!")
    else:
        # Group leftovers by status
        good_leftovers = [l for l in leftovers if l['days_left'] > 1 and not l['is_expired']]
        expiring_soon = [l for l in leftovers if 0 <= l['days_left'] <= 1 and not l['is_expired']]
        expired = [l for l in leftovers if l['days_left'] < 0 or l['is_expired']]
        
        # Display counts
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Good", len(good_leftovers))
        with col2:
            st.metric("Eat Soon", len(expiring_soon))
        with col3:
            st.metric("Expired", len(expired))
        
        # Display leftovers by group
        if expired:
            st.error("⚠️ Expired Leftovers")
            for item in expired:
                with st.expander(f"{item['name']} - EXPIRED"):
                    st.write(f"**Quantity:** {item['quantity']} servings")
                    st.write(f"**Created:** {item['created_date']}")
                    
                    if st.button("Remove", key=f"remove_{item['id']}"):
                        if remove_leftover(item['id']):
                            time.sleep(1)
                            st.rerun()
        
        if expiring_soon:
            st.warning("⚠️ Eat Soon!")
            for item in expiring_soon:
                with st.expander(f"{item['name']} - EAT TODAY!"):
                    st.write(f"**Quantity:** {item['quantity']} servings")
                    st.write(f"**Created:** {item['created_date']}")
                    st.write(f"**Days Left:** {item['days_left']}")
                    
                    new_qty = st.number_input(
                        "Servings remaining:", 
                        min_value=0.0, 
                        max_value=float(item['quantity']),
                        value=float(item['quantity']),
                        step=0.5,
                        key=f"qty_{item['id']}"
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Update", key=f"update_{item['id']}"):
                            if update_leftover(item['id'], new_qty):
                                time.sleep(1)
                                st.rerun()
                    
                    with col2:
                        if st.button("Finished", key=f"finish_{item['id']}"):
                            if remove_leftover(item['id']):
                                time.sleep(1)
                                st.rerun()
        
        if good_leftovers:
            st.subheader("🥗 Good Leftovers")
            for item in good_leftovers:
                with st.expander(f"{item['name']} - {item['days_left']} days left"):
                    st.write(f"**Quantity:** {item['quantity']} servings")
                    st.write(f"**Created:** {item['created_date']}")
                    st.write(f"**Days Left:** {item['days_left']}")
                    
                    new_qty = st.number_input(
                        "Servings remaining:", 
                        min_value=0.0, 
                        max_value=float(item['quantity']),
                        value=float(item['quantity']),
                        step=0.5,
                        key=f"qty_{item['id']}"
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Update", key=f"update_{item['id']}"):
                            if update_leftover(item['id'], new_qty):
                                time.sleep(1)
                                st.rerun()
                    
                    with col2:
                        if st.button("Finished", key=f"finish_{item['id']}"):
                            if remove_leftover(item['id']):
                                time.sleep(1)
                                st.rerun()

# Remove all expired button
        if expired:
            if st.button("Remove All Expired Leftovers"):
                try:
                    response = requests.delete(f"{API_BASE_URL}/leftovers/expired")
                    
                    if response.status_code == 200:
                        st.success("All expired leftovers removed!")
                        st.cache_data.clear()
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"Error removing expired leftovers: {response.status_code}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Add New Leftover Tab
with tab2:
    st.subheader("Add New Leftover Meal")
    
    # Function to get recipes
    @st.cache_data(ttl=600)
    def get_recipes():
        try:
            # Using meal plans API to get recipes
            response = requests.get(f"{API_BASE_URL}/meal-plans")
            
            if response.status_code == 200:
                data = response.json()
                recipes = []
                
                for item in data:
                    recipes.append({
                        'id': item.get('recipe_id'),
                        'name': item.get('recipe_name', 'Unknown Recipe')
                    })
                
                return recipes
            else:
                st.error(f"Error fetching recipes: {response.status_code}")
                return []
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return []
    
    recipes = get_recipes()
    
    if recipes:
        with st.form("add_leftover_form"):
            # Recipe selection
            recipe_names = [r['name'] for r in recipes]
            recipe_ids = {r['name']: r['id'] for r in recipes}
            
            selected_recipe = st.selectbox("Select recipe:", recipe_names)
            recipe_id = recipe_ids[selected_recipe]
            
            # Quantity
            quantity = st.number_input(
                "Number of servings:",
                min_value=0.5,
                value=1.0,
                step=0.5
            )
            
            # Submit
            submit = st.form_submit_button("Add Leftover")
            
            if submit:
                try:
                    data = {
                        'recipe_id': recipe_id,
                        'quantity': quantity
                    }
                    
                    response = requests.post(f"{API_BASE_URL}/leftovers", json=data)
                    
                    if response.status_code == 201:
                        st.success(f"Added {quantity} servings of {selected_recipe} to leftovers!")
                        st.cache_data.clear()
                    else:
                        st.error(f"Error adding leftover: {response.status_code}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    else:
        st.warning("No recipes available. Add some meal plans first!")
        
        if st.button("Go to Meal Suggestions"):
            st.switch_page("pages/02_Meal_Suggestions.py")

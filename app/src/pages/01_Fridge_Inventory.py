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
st.title("🧊 Fridge Inventory")
st.write("Manage your fridge ingredients and keep track of what's in stock")

# Tabs for different views
tab1, tab2, tab3 = st.tabs(["Current Inventory", "Add Items", "Remove Expired"])

# Current Inventory Tab
with tab1:
    st.subheader("Current Fridge Contents")
    
    # Function to get fridge inventory
    @st.cache_data(ttl=300)
    def get_fridge_inventory():
        try:
            response = requests.get(f"{API_BASE_URL}/fridge?client_id=1")
            
            if response.status_code == 200:
                data = response.json()
                inventory = []
                
                for item in data:
                    expiration_date = "N/A"
                    days_left = None
                    status = "Good"
                    
                    if item.get('expiration_date'):
                        expiration_date = item['expiration_date']
                        exp_date = datetime.strptime(expiration_date, '%Y-%m-%d').date()
                        today = datetime.now().date()
                        days_left = (exp_date - today).days
                        
                        if days_left < 0 or item.get('is_expired', False):
                            status = "Expired"
                        elif days_left <= 2:
                            status = "Expiring Soon"
                    
                    inventory.append({
                        'name': item['name'],
                        'quantity': item.get('quantity', 1),
                        'expiration_date': expiration_date,
                        'days_left': days_left,
                        'status': status,
                        'ingredient_id': item.get('ingredient_id')
                    })
                
                return inventory
            else:
                st.error(f"Error fetching inventory: {response.status_code}")
                return []
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return []
    
    inventory = get_fridge_inventory()

# Display inventory
    if inventory:
        # Convert to DataFrame for easier display
        df = pd.DataFrame(inventory)
        
        # Create filtered views
        filter_option = st.radio(
            "Filter items:",
            ["All", "Expiring Soon", "Expired", "Good"],
            horizontal=True
        )
        
        if filter_option != "All":
            filtered_df = df[df['status'] == filter_option]
        else:
            filtered_df = df
        
        # Apply color to status
        def color_status(val):
            if val == "Expired":
                return 'background-color: #FFCCCC'
            elif val == "Expiring Soon":
                return 'background-color: #FFFFCC'
            else:
                return 'background-color: #CCFFCC'
        
        # Display styled dataframe
        st.dataframe(
            filtered_df.style.applymap(
                color_status, 
                subset=['status']
            ).format({
                'quantity': '{:.1f}'
            }),
            column_config={
                "ingredient_id": None,  # Hide ID column
                "name": "Ingredient",
                "quantity": "Quantity",
                "expiration_date": "Expiration Date",
                "days_left": "Days Left",
                "status": "Status"
            },
            height=400
        )
        
        # Summary stats
        st.write(f"**Total items:** {len(df)}")
        st.write(f"**Expiring soon:** {len(df[df['status'] == 'Expiring Soon'])}")
        st.write(f"**Expired:** {len(df[df['status'] == 'Expired'])}")
    else:
        st.info("Your fridge is empty! Add some ingredients to get started.")
    
    if st.button("Refresh Inventory"):
        st.cache_data.clear()
        st.rerun()

# Add Items Tab
with tab2:
    st.subheader("Add New Items to Fridge")
    
    # Get available ingredients
    @st.cache_data(ttl=600)
    def get_available_ingredients():
        try:
            response = requests.get(f"{API_BASE_URL}/ingredients")
            
            if response.status_code == 200:
                data = response.json()
                ingredients = []
                
                for item in data:
                    ingredients.append({
                        'id': item.get('ingredient_id'),
                        'name': item.get('name', 'Unknown')
                    })
                
                return ingredients
            else:
                st.error(f"Error fetching ingredients: {response.status_code}")
                return []
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return []
    
    ingredients = get_available_ingredients()
    
    if ingredients:
        # Create a form for adding items
        with st.form("add_item_form"):
            # Create a mapping of names to IDs
            ingredient_names = [ing['name'] for ing in ingredients]
            ingredient_ids = {ing['name']: ing['id'] for ing in ingredients}
            
            # Selection of ingredient
            selected_ingredient = st.selectbox(
                "Select ingredient:",
                ingredient_names
            )
            
            # Quantity input
            quantity = st.number_input(
                "Quantity:",
                min_value=0.1,
                value=1.0,
                step=0.1
            )
            
            # Submit button
            submit_button = st.form_submit_button("Add to Fridge")
            
            # Process form submission
            if submit_button:
                ingredient_id = ingredient_ids[selected_ingredient]
                
                try:
                    # Prepare data for API call
                    data = {
                        'fridge_id': 1,  # Hardcoded for demo
                        'quantity': quantity
                    }
                    
                    # Make API call
                    response = requests.post(
                        f"{API_BASE_URL}/fridge/{ingredient_id}",
                        json=data
                    )
                    
                    if response.status_code == 201:
                        st.success(f"Added {quantity} {selected_ingredient} to your fridge!")
                        st.cache_data.clear()  # Clear cache to refresh inventory
                    else:
                        st.error(f"Error adding item: {response.status_code}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    else:
        st.warning("No ingredients available. Please contact support.")
    
    # Option to add a custom ingredient
    st.markdown("---")
    st.subheader("Add Custom Ingredient")
    
    with st.form("custom_ingredient_form"):
        new_name = st.text_input("Ingredient name:")
        expiration_date = st.date_input("Expiration date:", 
                                       value=datetime.now().date() + timedelta(days=7))
        new_quantity = st.number_input("Quantity:", min_value=0.1, value=1.0, step=0.1)
        
        custom_submit = st.form_submit_button("Add Custom Ingredient")
        
        if custom_submit and new_name:
            try:
                # First add the ingredient
                ingredient_data = {
                    'name': new_name,
                    'expiration_date': expiration_date.strftime('%Y-%m-%d')
                }
                
                response = requests.post(
                    f"{API_BASE_URL}/ingredients",
                    json=ingredient_data
                )
                
                if response.status_code == 201:
                    ingredient_id = response.json().get('ingredient_id')
                    
                    # Then add to fridge
                    fridge_data = {
                        'fridge_id': 1,
                        'quantity': new_quantity
                    }
                    
                    fridge_response = requests.post(
                        f"{API_BASE_URL}/fridge/{ingredient_id}",
                        json=fridge_data
                    )
                    
                    if fridge_response.status_code == 201:
                        st.success(f"Added custom ingredient {new_name}!")
                        st.cache_data.clear()
                    else:
                        st.error(f"Error adding to fridge: {fridge_response.status_code}")
                else:
                    st.error(f"Error creating ingredient: {response.status_code}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Remove Expired Tab
with tab3:
    st.subheader("Remove Expired Items")
    
    # Get expired items
    expired_items = [item for item in get_fridge_inventory() if item['status'] == 'Expired']
    
    if expired_items:
        st.warning(f"You have {len(expired_items)} expired items in your fridge.")
        
        for item in expired_items:
            st.write(f"• {item['name']} (Expired on {item['expiration_date']})")
        
        if st.button("Remove All Expired Items"):
            try:
                response = requests.delete(f"{API_BASE_URL}/fridge/expired")
                
                if response.status_code == 200:
                    st.success("All expired items removed!")
                    st.cache_data.clear()
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"Error removing expired items: {response.status_code}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.success("No expired items in your fridge!")

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

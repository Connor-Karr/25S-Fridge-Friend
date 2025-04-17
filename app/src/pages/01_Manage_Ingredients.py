import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime, timedelta
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
st.title("🧊 Fridge Inventory")
st.write("Manage your fridge ingredients and keep track of what's in stock")


# API helper functions
def get_user_fridge_id():
   """Get the user's fridge ID"""
   # If we've already stored the fridge ID in session state, use it
   if 'fridge_id' in st.session_state:
       return st.session_state.fridge_id
  
   # Otherwise, fetch it from the API
   user_id = st.session_state.get('user_id', 1)  # Default to user 1 if not set
  
   try:
       response = requests.get(f"{API_BASE_URL}/users/fridge/{user_id}")
       if response.status_code == 200:
           result = response.json()
           fridge_id = result.get('fridge_id')
           # Store in session state for future use
           st.session_state.fridge_id = fridge_id
           return fridge_id
       else:
           st.error(f"Error fetching user's fridge: {response.status_code}")
           # Fall back to default fridge ID
           return 1
   except Exception as e:
       st.error(f"Error: {str(e)}")
       # Fall back to default fridge ID
       return 1


def get_fridge_inventory():
   """Get the fridge inventory for the current user"""
   client_id = st.session_state.get('user_id', 1)  # Default to user 1 if not set
  
   try:
       response = requests.get(f"{API_BASE_URL}/fridge?client_id={client_id}")
       if response.status_code == 200:
           return response.json()
       else:
           st.error(f"Error fetching inventory: {response.status_code}")
           return []
   except Exception as e:
       st.error(f"Error: {str(e)}")
       return []


def get_ingredients():
   """Get all ingredients"""
   try:
       response = requests.get(f"{API_BASE_URL}/ingredients")
       if response.status_code == 200:
           return response.json()
       else:
           st.error(f"Error fetching ingredients: {response.status_code}")
           return []
   except Exception as e:
       st.error(f"Error: {str(e)}")
       return []


def add_ingredient_to_fridge(ingredient_id, quantity):
   """Add an ingredient to the fridge"""
   # Get the user's fridge ID
   fridge_id = get_user_fridge_id()
  
   try:
       data = {
           'fridge_id': fridge_id,
           'quantity': quantity
       }
       response = requests.post(f"{API_BASE_URL}/fridge/{ingredient_id}", json=data)
       return response.status_code == 201
   except Exception as e:
       st.error(f"Error adding ingredient: {str(e)}")
       return False


def add_new_ingredient(name, expiration_date, macros=None):
   """Create a new ingredient"""
   try:
       data = {
           'name': name,
           'expiration_date': expiration_date
       }
       if macros:
           data['macros'] = macros
          
       response = requests.post(f"{API_BASE_URL}/ingredients", json=data)
       if response.status_code == 201:
           # Get the ingredient_id from the response
           result = response.json()
           ingredient_id = result.get('ingredient_id')
           return ingredient_id, True
       else:
           st.error(f"Error creating ingredient: {response.status_code}")
           if response.text:
               st.error(f"Response: {response.text}")
           return None, False
   except Exception as e:
       st.error(f"Error creating ingredient: {str(e)}")
       return None, False


def update_expired_status():
   """Update expired status of ingredients"""
   try:
       response = requests.put(f"{API_BASE_URL}/fridge/expired")
       return response.status_code == 200
   except Exception as e:
       st.error(f"Error updating expired status: {str(e)}")
       return False


def remove_expired_ingredients():
   """Remove expired ingredients from fridge"""
   try:
       response = requests.delete(f"{API_BASE_URL}/fridge/expired")
       return response.status_code == 200
   except Exception as e:
       st.error(f"Error removing expired ingredients: {str(e)}")
       return False


# Function to process inventory data
def process_inventory(inventory):
   """Process inventory data for display"""
   if not inventory:
       return []
  
   processed = []
   today = datetime.now().date()
  
   for item in inventory:
       status = "Good"
       days_left = None
      
       if item.get('expiration_date'):
           try:
               exp_date = datetime.strptime(item['expiration_date'], '%Y-%m-%d').date()
               days_left = (exp_date - today).days
              
               if days_left < 0 or item.get('is_expired', False):
                   status = "Expired"
               elif days_left <= 2:
                   status = "Expiring Soon"
           except ValueError:
               # Handle date parsing errors
               pass
      
       processed.append({
           'name': item.get('name', 'Unknown'),
           'quantity': item.get('quantity', 1),
           'expiration_date': item.get('expiration_date', 'N/A'),
           'days_left': days_left,
           'status': status,
           'ingredient_id': item.get('ingredient_id'),
           'is_expired': item.get('is_expired', False)
       })
  
   return processed


# Ensure we have the user's fridge ID
fridge_id = get_user_fridge_id()


# Tabs for different views
tab1, tab2, tab3 = st.tabs(["Current Inventory", "Add Items", "Remove Expired"])


# Current Inventory Tab
with tab1:
   st.subheader("Current Fridge Contents")
  
   # Get and process inventory
   raw_inventory = get_fridge_inventory()
   inventory = process_inventory(raw_inventory)
  
   if inventory:
       # Convert to DataFrame
       df = pd.DataFrame(inventory)
      
       # Filter options
       filter_option = st.radio(
           "Filter items:",
           ["All", "Expiring Soon", "Expired", "Good"],
           horizontal=True
       )
      
       filtered_df = df[df['status'] == filter_option] if filter_option != "All" else df
      
       # Display table
       st.dataframe(
           filtered_df,
           column_config={
               "ingredient_id": None,  # Hide ID column
               "is_expired": None,     # Hide expired flag
               "name": "Ingredient",
               "quantity": "Quantity",
               "expiration_date": "Expiration Date",
               "days_left": "Days Left",
               "status": "Status"
           },
           use_container_width=True
       )
      
       # Summary stats
       col1, col2, col3 = st.columns(3)
       with col1:
           st.metric("Total Items", len(df))
       with col2:
           st.metric("Expiring Soon", len(df[df['status'] == 'Expiring Soon']))
       with col3:
           st.metric("Expired", len(df[df['status'] == 'Expired']))
   else:
       st.info("Your fridge is empty! Add some ingredients to get started.")
  
   if st.button("Refresh Inventory"):
       st.rerun()


# Add Items Tab
with tab2:
   st.subheader("Add New Items to Fridge")
  
   # Get available ingredients
   ingredients_data = get_ingredients()
  
   if ingredients_data:
       # Extract ingredient info
       ingredients = []
       for item in ingredients_data:
           ingredient_id = item.get('ingredient_id')
           if ingredient_id:
               ingredients.append({
                   'id': ingredient_id,
                   'name': item.get('name', f"Ingredient {ingredient_id}")
               })
      
       # Create mapping of names to IDs
       ingredient_names = [ing['name'] for ing in ingredients]
       ingredient_ids = {ing['name']: ing['id'] for ing in ingredients}
      
       # Add existing item form
       with st.form("add_item_form"):
           st.subheader("Add Existing Ingredient")
          
           selected_ingredient = st.selectbox(
               "Select ingredient:",
               ingredient_names
           )
          
           quantity = st.number_input(
               "Quantity:",
               min_value=0.1,
               value=1.0,
               step=0.1
           )
          
           submit_button = st.form_submit_button("Add to Fridge")
          
           if submit_button:
               ingredient_id = ingredient_ids[selected_ingredient]
              
               success = add_ingredient_to_fridge(ingredient_id, quantity)
              
               if success:
                   st.success(f"Added {quantity} {selected_ingredient} to your fridge!")
                   time.sleep(1)
                   st.rerun()
   else:
       st.warning("Unable to fetch ingredients list.")
  


# Remove Expired Tab
with tab3:
   st.subheader("Remove Expired Items")
  
   # Get and process inventory
   raw_inventory = get_fridge_inventory()
   inventory = process_inventory(raw_inventory)
  
   # Find expired items
   expired_items = [item for item in inventory if item['status'] == 'Expired' or item['is_expired']]
  
   if expired_items:
       # Display expired items
       st.warning(f"You have {len(expired_items)} expired items in your fridge.")
      
       # Show as a table
       expired_df = pd.DataFrame(expired_items)
       st.dataframe(
           expired_df[['name', 'quantity', 'expiration_date']],
           column_config={
               "name": "Ingredient",
               "quantity": "Quantity",
               "expiration_date": "Expired On"
           },
           use_container_width=True
       )
      
       # Action buttons
       col1, col2 = st.columns(2)
      
       with col1:
           if st.button("Update Expired Status"):
               success = update_expired_status()
               if success:
                   st.success("Updated expired ingredient status!")
                   time.sleep(1)
                   st.rerun()
      
       with col2:
           if st.button("Remove All Expired Items"):
               success = remove_expired_ingredients()
               if success:
                   st.success("All expired items removed!")
                   time.sleep(1)
                   st.rerun()
   else:
       st.success("No expired items in your fridge!")

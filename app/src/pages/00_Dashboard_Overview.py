import streamlit as st
import pandas as pd
import requests
import time
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
st.title(f"Welcome, {st.session_state.first_name}! 👋")
st.write("Manage your fridge, plan meals, and track ingredients")


# API helper functions
def get_api_data(endpoint):
   try:
       response = requests.get(f"{API_BASE_URL}/{endpoint}")
       return response.json() if response.status_code == 200 else []
   except Exception as e:
       st.error(f"Error: {str(e)}")
       return []


def api_request(method, endpoint, data=None):
   try:
       if method == "PUT":
           response = requests.put(f"{API_BASE_URL}/{endpoint}")
       elif method == "DELETE":
           response = requests.delete(f"{API_BASE_URL}/{endpoint}")
       elif method == "POST":
           response = requests.post(f"{API_BASE_URL}/{endpoint}", json=data)
       else:
           return None, False
          
       success = response.status_code in [200, 201]
       return response.json() if success else None, success
   except Exception as e:
       st.error(f"Error: {str(e)}")
       return None, False


# Parse dates safely
def parse_date(date_str):
   if not date_str:
       return None
  
   formats = ['%Y-%m-%d', '%a, %d %b %Y %H:%M:%S GMT']
   for fmt in formats:
       try:
           return datetime.strptime(date_str, fmt).date()
       except ValueError:
           continue
   return None


# Create columns for dashboard widgets
col1, col2 = st.columns(2)


# Fridge Inventory Widget
with col1:
   st.subheader("🧊 Fridge Inventory")
  
   fridge_inventory = get_api_data("fridge?client_id=1")
  
   if fridge_inventory:
       # Create DataFrame and calculate days until expiration
       df = pd.DataFrame(fridge_inventory)
       today = datetime.now().date()
      
       # Add expiration info
       if 'is_expired' in df.columns:
           df['Expired'] = df['is_expired'].apply(lambda x: "Yes" if x else "No")
          
       # Calculate days until expiration
       df['days_left'] = None
       for i, item in df.iterrows():
           if 'expiration_date' in item and item['expiration_date']:
               exp_date = parse_date(item['expiration_date'])
               if exp_date:
                   df.at[i, 'days_left'] = (exp_date - today).days
      
       # Display inventory table
       display_cols = [col for col in ['name', 'quantity', 'days_left', 'Expired'] if col in df.columns]
       if display_cols:
           rename_map = {'name': 'Ingredient', 'quantity': 'Quantity', 'days_left': 'Days Left'}
           st.dataframe(
               df[display_cols].rename(columns=rename_map),
               use_container_width=True
           )
          
           # Show expiring items
           if 'days_left' in df.columns:
               expiring_items = df[(df['days_left'] >= 0) & (df['days_left'] <= 5) & (~df['is_expired'])]
              
               if not expiring_items.empty:
                   st.subheader("⚠️ Items Expiring Soon")
                   for _, item in expiring_items.iterrows():
                       if item['days_left'] <= 0:
                           st.error(f"⚠️ {item['name']} - Expires today! ({item['quantity']} remaining)")
                       elif item['days_left'] == 1:
                           st.warning(f"⚠️ {item['name']} - Expires tomorrow ({item['quantity']} remaining)")
                       else:
                           st.info(f"ℹ️ {item['name']} - Expires in {int(item['days_left'])} days ({item['quantity']} remaining)")
               else:
                   st.success("No items expiring soon! Your fridge is in good shape.")
       else:
           st.dataframe(df, use_container_width=True)
   else:
       st.info("No items in your fridge inventory.")


# Meal Suggestions Widget
with col2:
   st.subheader("🍲 Meal Suggestions")
  
   meal_plans = get_api_data("meal-plans?client_id=1")
  
   if meal_plans:
       # Display meal plans table
       meal_df = pd.DataFrame(meal_plans)
       display_cols = [col for col in ['recipe_name', 'quantity'] if col in meal_df.columns]
      
       if display_cols:
           rename_map = {'recipe_name': 'Recipe', 'quantity': 'Servings'}
           st.dataframe(
               meal_df[display_cols].rename(columns=rename_map),
               use_container_width=True
           )
          
              
       else:
           st.dataframe(meal_df, use_container_width=True)
   else:
       st.info("No meal suggestions available.")


# Leftovers Section
st.markdown("---")
st.subheader("🥡 Leftovers")


leftovers_data = get_api_data("leftovers")


if leftovers_data:
   # Display leftovers table
   leftovers_df = pd.DataFrame(leftovers_data)
   display_cols = [col for col in ['recipe_name', 'quantity', 'is_expired'] if col in leftovers_df.columns]
  
   if display_cols:
       rename_map = {'recipe_name': 'Recipe', 'quantity': 'Servings', 'is_expired': 'Expired'}
       leftover_display = leftovers_df[display_cols].rename(columns=rename_map)
      
       if 'Expired' in leftover_display.columns:
           leftover_display['Expired'] = leftover_display['Expired'].apply(lambda x: "Yes" if x else "No")
      
       st.dataframe(leftover_display, use_container_width=True)
      
       # Leftovers action buttons
       col1, col2 = st.columns(2)
       with col1:
           if st.button("Update Expired Status", key="update_expired_leftovers"):
               result, success = api_request("PUT", "leftovers/expired")
               if success:
                   st.success("Updated expired leftovers status!")
                   time.sleep(1)
                   st.rerun()
      
       with col2:
           if st.button("Remove Expired Leftovers", key="remove_expired_leftovers"):
               result, success = api_request("DELETE", "leftovers/expired")
               if success:
                   st.success("Removed expired leftovers!")
                   time.sleep(1)
                   st.rerun()
   else:
       st.dataframe(leftovers_df, use_container_width=True)
else:
   st.info("No leftovers available.")


# Refresh button
if st.button("Refresh Data", key="refresh"):
   st.rerun()

import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

# Authentication check
if not st.session_state.get('authenticated', False) or st.session_state.role != "admin":
    st.warning("Please log in as an admin to access this page")
    st.stop()

# Set up navigation
SideBarLinks(st.session_state.role)

# Page title
st.title("Admin Dashboard")
st.subheader(f"Welcome, {st.session_state.first_name}!")

# API base URL
API_BASE_URL = "http://web-api:4000"

# Function to get data from API with error handling
def get_api_data(endpoint):
    try:
        response = requests.get(f"{API_BASE_URL}/{endpoint}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching data from {endpoint}: Status code {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error fetching data from {endpoint}: {str(e)}")
        return []

# Quick Actions Section
actions_cols = st.columns(2)

with actions_cols[0]:
    if st.button("Update Expired Status", use_container_width=True):
        try:
            res = requests.put(f"{API_BASE_URL}/fridge/expired")
            if res.status_code == 200:
                st.success("Expired status updated successfully!")
            else:
                st.error(f"Error: {res.status_code}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

with actions_cols[1]:
    if st.button("Remove Expired Items", use_container_width=True):
        try:
            res = requests.delete(f"{API_BASE_URL}/fridge/expired")
            if res.status_code == 200:
                st.success("Expired items removed successfully!")
            else:
                st.error(f"Error: {res.status_code}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Users Table
st.subheader("👤 User Management")
users_data = get_api_data("users")

if users_data:
    st.dataframe(
        pd.DataFrame(users_data),
        column_config={
            "user_id": "ID",
            "f_name": "First Name",
            "l_name": "Last Name",
            "username": "Username",
            "email": "Email"
        },
        use_container_width=True
    )
else:
    st.info("No users found or unable to fetch user data.")

# Ingredients Table
st.subheader("🥕 Ingredients Management")
ingredients_data = get_api_data("ingredients")

if ingredients_data:
    st.dataframe(
        pd.DataFrame(ingredients_data),
        use_container_width=True
    )
else:
    st.info("No ingredients found or unable to fetch ingredient data.")

# Fridge Inventory Table
st.subheader("🧊 Fridge Inventory")
# Using client_id=1 as an example - you might want to make this configurable
fridge_data = get_api_data("fridge?client_id=1")

if fridge_data:
    st.dataframe(
        pd.DataFrame(fridge_data),
        use_container_width=True
    )
else:
    st.info("No fridge inventory found or unable to fetch data.")

# Macronutrients Table
st.subheader("🍎 Macronutrients")
macros_data = get_api_data("macronutrients")

if macros_data:
    st.dataframe(
        pd.DataFrame(macros_data),
        use_container_width=True
    )
else:
    st.info("No macronutrient data found or unable to fetch data.")

# Error Logs Table
st.subheader("📜 Error Logs")
error_logs = get_api_data("logs/errors")

if error_logs:
    st.dataframe(
        pd.DataFrame(error_logs),
        use_container_width=True
    )
else:
    st.info("No error logs found or unable to fetch error log data.")

# Food Scan History
st.subheader("📱 Food Scan History")
scan_logs = get_api_data("logs/scans")

if scan_logs:
    st.dataframe(
        pd.DataFrame(scan_logs),
        use_container_width=True
    )
else:
    st.info("No scan logs found or unable to fetch scan log data.")

# Leftovers Table
st.subheader("🥡 Leftovers")
leftovers_data = get_api_data("leftovers")

if leftovers_data:
    st.dataframe(
        pd.DataFrame(leftovers_data),
        use_container_width=True
    )
else:
    st.info("No leftovers found or unable to fetch data.")

# Refresh Button
if st.button("Refresh Dashboard Data"):
    st.rerun()
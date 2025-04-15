import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime, timedelta
import json
from modules.nav import SideBarLinks

# API base URL
API_BASE_URL = "http://web-api:4000"

# Authentication check
if not st.session_state.get('authenticated', False) or st.session_state.role != "admin":
    st.warning("Please log in as Alvin to access this page")
    st.stop()

# Set up navigation
SideBarLinks(st.session_state.role)

# Page header
st.title("🥕 Ingredient Management")
st.write("Add, update, and manage ingredients and their nutritional data")

# Create tabs for different functions
tab1, tab2, tab3 = st.tabs(["Ingredient Database", "Add New Ingredient", "Update Macros"])


# Function to get all ingredients
@st.cache_data(ttl=300)
def get_ingredients():
    try:
        response = requests.get(f"{API_BASE_URL}/ingredients")
        
        if response.status_code == 200:
            data = response.json()
            ingredients = []
            
            for item in data:
                ingredients.append({
                    'id': item.get('ingredient_id'),
                    'name': item.get('name', 'Unknown'),
                    'expiration_date': item.get('expiration_date', 'N/A')
                })
            
            return ingredients
        else:
            st.error(f"Error fetching ingredients: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []

# Function to get ingredient details including macros
@st.cache_data(ttl=300)
def get_ingredient_details(ingredient_id):
    try:
        response = requests.get(f"{API_BASE_URL}/ingredients/{ingredient_id}")
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching ingredient details: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None
# Function to update ingredient
def update_ingredient(ingredient_id, data):
    try:
        response = requests.put(f"{API_BASE_URL}/ingredients/{ingredient_id}", json=data)
        
        if response.status_code == 200:
            st.success("Ingredient updated successfully!")
            st.cache_data.clear()
            return True
        else:
            st.error(f"Error updating ingredient: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

# Function to delete ingredient
def delete_ingredient(ingredient_id):
    try:
        response = requests.delete(f"{API_BASE_URL}/ingredients/{ingredient_id}")
        
        if response.status_code == 200:
            st.success("Ingredient deleted successfully!")
            st.cache_data.clear()
            return True
        else:
            st.error(f"Error deleting ingredient: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

# Function to update macronutrients
def update_macros(macro_id, data):
    try:
        response = requests.put(f"{API_BASE_URL}/macros/{macro_id}", json=data)
        
        if response.status_code == 200:
            st.success("Macronutrients updated successfully!")
            st.cache_data.clear()
            return True
        else:
            st.error(f"Error updating macronutrients: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

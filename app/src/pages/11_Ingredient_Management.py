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

# Ingredient Database Tab
with tab1:
    st.subheader("Ingredient Database")
    ingredients = get_ingredients()
    
    if ingredients:
        search_term = st.text_input("Search ingredients:", key="search_ingredients")
        filtered_ingredients = [i for i in ingredients if search_term.lower() in i['name'].lower()] if search_term else ingredients
        df = pd.DataFrame(filtered_ingredients)
        st.dataframe(df, column_config={"id": st.column_config.NumberColumn("ID"), "name": "Ingredient Name", "expiration_date": "Default Expiration"}, height=300)
        st.subheader("Ingredient Details")
        
        ingredient_names = [i['name'] for i in ingredients]
        ingredient_ids = {i['name']: i['id'] for i in ingredients}
        selected_ingredient = st.selectbox("Select ingredient to view/edit:", ingredient_names)
        ingredient_id = ingredient_ids[selected_ingredient]
        ingredient_details = get_ingredient_details(ingredient_id)
        
        if ingredient_details:
            with st.expander(f"Details for {selected_ingredient}", expanded=True):
                ingredient = ingredient_details.get('ingredient', {})
                macros = ingredient_details.get('macronutrients', {})
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Basic Information")
                    st.write(f"**ID:** {ingredient.get('ingredient_id')}")
                    st.write(f"**Name:** {ingredient.get('name')}")
                    st.write(f"**Expiration Date:** {ingredient.get('expiration_date', 'N/A')}")
                    with st.form(f"edit_ingredient_{ingredient_id}"):
                        new_name = st.text_input("Update Name:", value=ingredient.get('name', ''))
                        new_expiration = st.date_input("Update Default Expiration:", value=datetime.now().date() + timedelta(days=7))
                        col1, col2 = st.columns(2)
                        with col1: submit = st.form_submit_button("Update Ingredient")
                        with col2: delete = st.form_submit_button("Delete Ingredient", type="secondary")
                        if submit:
                            data = {'name': new_name, 'expiration_date': new_expiration.strftime('%Y-%m-%d')}
                            if update_ingredient(ingredient_id, data): time.sleep(1); st.rerun()
                        if delete:
                            if delete_ingredient(ingredient_id): time.sleep(1); st.rerun()
                
                with col2:
                    st.subheader("Macronutrient Information")
                    if macros:
                        st.write(f"**Macro ID:** {macros.get('macro_id')}")
                        st.write(f"**Protein:** {macros.get('protein', 0)} g")
                        st.write(f"**Fat:** {macros.get('fat', 0)} g")
                        st.write(f"**Carbs:** {macros.get('carbs', 0)} g")
                        st.write(f"**Fiber:** {macros.get('fiber', 0)} g")
                        st.write(f"**Sodium:** {macros.get('sodium', 0)} mg")
                        st.write(f"**Calories:** {macros.get('calories', 0)}")
                        with st.form(f"edit_macros_quick_{macros.get('macro_id')}"):
                            st.caption("Quick Macronutrient Update")
                            calories = st.number_input("Calories:", min_value=0, value=int(macros.get('calories', 0)))
                            protein = st.number_input("Protein (g):", min_value=0.0, value=float(macros.get('protein', 0)), step=0.1)
                            if st.form_submit_button("Update"):
                                data = {'calories': calories, 'protein': protein}
                                if update_macros(macros.get('macro_id'), data): time.sleep(1); st.rerun()
                    else:
                        st.info("No macronutrient data available for this ingredient.")
                        if st.button("Add Macronutrient Data"):
                            st.session_state.selected_ingredient_id = ingredient_id
                            st.session_state.selected_ingredient_name = selected_ingredient
                            st.switch_page("pages/13_User_Management.py")
    else:
        st.info("No ingredients found in the database.")
        if st.button("Add New Ingredient"):
            tab2.set_active(True)

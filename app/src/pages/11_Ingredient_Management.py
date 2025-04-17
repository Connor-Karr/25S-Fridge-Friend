import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
from modules.nav import SideBarLinks

# Authentication check
if not st.session_state.get('authenticated', False) or st.session_state.role != "admin":
    st.warning("Please log in as an admin to access this page")
    st.stop()

# Set up navigation
SideBarLinks(st.session_state.role)

# Page header
st.title("🥕 Ingredient Management")
st.write("Add, update, and manage ingredients and their nutritional data")

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

# Create tabs for different functions
tab1, tab2, tab3 = st.tabs(["Ingredient Database", "Add New Ingredient", "Macronutrients"])

# Tab 1: Ingredient Database
with tab1:
    st.subheader("Ingredient Database")
    
    # Get all ingredients
    ingredients_data = get_api_data("ingredients")
    
    if ingredients_data:
        # Display ingredients table
        st.dataframe(
            pd.DataFrame(ingredients_data),
            use_container_width=True
        )
        
        # Select an ingredient to view details or update
        ingredient_ids = [item.get('ingredient_id') for item in ingredients_data]
        ingredient_names = [item.get('name', f"Ingredient {item.get('ingredient_id')}") for item in ingredients_data]
        ingredient_dict = dict(zip(ingredient_names, ingredient_ids))
        
        selected_ingredient = st.selectbox("Select ingredient to view/edit:", ingredient_names)
        selected_id = ingredient_dict[selected_ingredient]
        
        # Get detailed ingredient info
        ingredient_detail = get_api_data(f"ingredients/{selected_id}")
        
        if ingredient_detail:
            st.subheader(f"Details for: {selected_ingredient}")
            
            # Basic ingredient information
            basic_info = ingredient_detail.get('ingredient', {})
            st.write("**Basic Information:**")
            st.dataframe(pd.DataFrame([basic_info]), use_container_width=True)
            
            # Macronutrient information
            macros = ingredient_detail.get('macronutrients', {})
            if macros:
                st.write("**Macronutrient Information:**")
                st.dataframe(pd.DataFrame([macros]), use_container_width=True)
            else:
                st.info("No macronutrient data available for this ingredient.")
            
            # Update form
            with st.form(f"update_ingredient_{selected_id}"):
                st.subheader("Update Ingredient")
                new_name = st.text_input("Name:", value=basic_info.get('name', ''))
                expiration_date = st.date_input("Expiration Date:", value=datetime.now().date() + timedelta(days=7))
                
                col1, col2 = st.columns(2)
                with col1:
                    update_button = st.form_submit_button("Update Ingredient")
                with col2:
                    delete_button = st.form_submit_button("Delete Ingredient")
                
                if update_button:
                    data = {
                        'name': new_name,
                        'expiration_date': expiration_date.strftime('%Y-%m-%d')
                    }
                    try:
                        response = requests.put(f"{API_BASE_URL}/ingredients/{selected_id}", json=data)
                        if response.status_code == 200:
                            st.success("Ingredient updated successfully!")
                            st.rerun()
                        else:
                            st.error(f"Error updating ingredient: {response.status_code}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                
                if delete_button:
                    try:
                        response = requests.delete(f"{API_BASE_URL}/ingredients/{selected_id}")
                        if response.status_code == 200:
                            st.success("Ingredient deleted successfully!")
                            st.rerun()
                        else:
                            st.error(f"Error deleting ingredient: {response.status_code}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    else:
        st.info("No ingredients found or unable to fetch ingredient data.")
        st.button("Add New Ingredient", on_click=lambda: tab2)

# Tab 2: Add New Ingredient
with tab2:
    st.subheader("Add New Ingredient")
    
    with st.form("add_ingredient_form"):
        name = st.text_input("Ingredient Name:")
        expiration_days = st.number_input("Default Shelf Life (days):", min_value=1, value=7)
        expiration_date = (datetime.now() + timedelta(days=expiration_days)).strftime('%Y-%m-%d')
        
        st.subheader("Macronutrient Information")
        col1, col2 = st.columns(2)
        
        with col1:
            protein = st.number_input("Protein (g):", min_value=0.0, step=0.1)
            fat = st.number_input("Fat (g):", min_value=0.0, step=0.1)
            fiber = st.number_input("Fiber (g):", min_value=0.0, step=0.1)
        
        with col2:
            carbs = st.number_input("Carbs (g):", min_value=0.0, step=0.1)
            sodium = st.number_input("Sodium (mg):", min_value=0.0, step=0.1)
            calories = st.number_input("Calories:", min_value=0)
        
        submit_button = st.form_submit_button("Add Ingredient")
        
        if submit_button and name:
            ingredient_data = {
                'name': name,
                'expiration_date': expiration_date,
                'macros': {
                    'protein': protein,
                    'fat': fat,
                    'carbs': carbs,
                    'fiber': fiber,
                    'sodium': sodium,
                    'calories': calories
                }
            }
            
            try:
                response = requests.post(f"{API_BASE_URL}/ingredients", json=ingredient_data)
                if response.status_code == 201:
                    st.success(f"Added {name} to the database!")
                    st.rerun()
                else:
                    st.error(f"Error adding ingredient: {response.status_code}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Tab 3: Macronutrients
with tab3:
    st.subheader("Macronutrients Database")
    
    # Get all macronutrients
    macros_data = get_api_data("macronutrients")
    
    if macros_data:
        # Display macronutrients table
        st.dataframe(pd.DataFrame(macros_data), use_container_width=True)
        
        # Select macronutrient to update
        macro_ids = [item.get('macro_id') for item in macros_data]
        selected_macro_id = st.selectbox("Select macronutrient to update:", macro_ids)
        
        selected_macro = next((item for item in macros_data if item.get('macro_id') == selected_macro_id), None)
        
        if selected_macro:
            with st.form(f"update_macro_{selected_macro_id}"):
                st.subheader("Update Macronutrient Values")
                
                col1, col2 = st.columns(2)
                with col1:
                    protein = st.number_input("Protein (g):", min_value=0.0, value=float(selected_macro.get('protein', 0)), step=0.1)
                    fat = st.number_input("Fat (g):", min_value=0.0, value=float(selected_macro.get('fat', 0)), step=0.1)
                    fiber = st.number_input("Fiber (g):", min_value=0.0, value=float(selected_macro.get('fiber', 0)), step=0.1)
                
                with col2:
                    carbs = st.number_input("Carbs (g):", min_value=0.0, value=float(selected_macro.get('carbs', 0)), step=0.1)
                    sodium = st.number_input("Sodium (mg):", min_value=0.0, value=float(selected_macro.get('sodium', 0)), step=0.1)
                    calories = st.number_input("Calories:", min_value=0, value=int(selected_macro.get('calories', 0)))
                
                update_button = st.form_submit_button("Update Macronutrients")
                
                if update_button:
                    macro_data = {
                        'protein': protein,
                        'fat': fat,
                        'carbs': carbs,
                        'fiber': fiber,
                        'sodium': sodium,
                        'calories': calories
                    }
                    
                    try:
                        response = requests.put(f"{API_BASE_URL}/macronutrients/{selected_macro_id}", json=macro_data)
                        if response.status_code == 200:
                            st.success("Macronutrients updated successfully!")
                            st.rerun()
                        else:
                            st.error(f"Error updating macronutrients: {response.status_code}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    else:
        st.info("No macronutrient data found or unable to fetch data.")

# Refresh button
if st.button("Refresh Data"):
    st.rerun()
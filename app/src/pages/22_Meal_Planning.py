import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime, timedelta
import plotly.express as px
import json
from modules.nav import SideBarLinks

API_BASE_URL = "http://web-api:4000"

if not st.session_state.get('authenticated', False) or st.session_state.role != "nutritionist":
    st.warning("Please log in as Nancy to access this page")
    st.stop()

SideBarLinks(st.session_state.role)

# Page header
st.title("🍽️ Meal Planning")
st.write("Create and manage personalized meal plans for your clients")

# Get meal plans
@st.cache_data(ttl=300)
def get_meal_plans():
    try:
        response = requests.get(f"{API_BASE_URL}/meal-plans")
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            st.error(f"Error fetching meal plans: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []

# Get a specific meal plan
@st.cache_data(ttl=300)
def get_meal_plan(meal_id):
    try:
        response = requests.get(f"{API_BASE_URL}/meal-plans/{meal_id}")
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            st.error(f"Error fetching meal plan: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Create a meal plan
def create_meal_plan(data):
    try:
        response = requests.post(f"{API_BASE_URL}/meal-plans", json=data)
        if response.status_code == 201:
            return response.json(), True
        else:
            st.error(f"Error creating meal plan: {response.status_code}")
            return None, False
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None, False

# Update a meal plan
def update_meal_plan(meal_id, data):
    try:
        response = requests.put(f"{API_BASE_URL}/meal-plans/{meal_id}", json=data)
        if response.status_code == 200:
            return True
        else:
            st.error(f"Error updating meal plan: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

# Delete a meal plan
def delete_meal_plan(meal_id):
    try:
        response = requests.delete(f"{API_BASE_URL}/meal-plans/{meal_id}")
        if response.status_code == 200:
            return True
        else:
            st.error(f"Error deleting meal plan: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False
# Mock client data
clients = [
    {"id": 1, "name": "John D.", "age": 27, "goal": "Weight Loss", "diet": "Low Carb", "allergies": "Peanuts"},
    {"id": 2, "name": "Sarah M.", "age": 34, "goal": "Muscle Gain", "diet": "High Protein", "allergies": "Dairy"},
    {"id": 3, "name": "Michael R.", "age": 42, "goal": "Maintenance", "diet": "Balanced", "allergies": "None"},
    {"id": 4, "name": "Emma L.", "age": 19, "goal": "Performance", "diet": "Keto", "allergies": "Gluten"},
    {"id": 5, "name": "David W.", "age": 55, "goal": "Health", "diet": "Mediterranean", "allergies": "Shellfish"}
]

# Mock recipe data
recipes = [
    {"id": 1, "name": "Grilled Chicken Salad", "calories": 350, "protein": 32, "carbs": 12, "fat": 18, "tags": ["low-carb", "high-protein", "gluten-free"]},
    {"id": 2, "name": "Salmon with Quinoa", "calories": 420, "protein": 28, "carbs": 35, "fat": 15, "tags": ["balanced", "omega-3", "gluten-free"]},
    {"id": 3, "name": "Vegetable Stir Fry", "calories": 280, "protein": 15, "carbs": 42, "fat": 8, "tags": ["vegan", "low-fat", "gluten-free"]},
    {"id": 4, "name": "Greek Yogurt Parfait", "calories": 230, "protein": 18, "carbs": 25, "fat": 7, "tags": ["breakfast", "high-protein", "vegetarian"]},
    {"id": 5, "name": "Spinach and Feta Omelette", "calories": 320, "protein": 22, "carbs": 8, "fat": 22, "tags": ["low-carb", "keto", "vegetarian"]},
    {"id": 6, "name": "Beef and Vegetable Stew", "calories": 380, "protein": 25, "carbs": 30, "fat": 16, "tags": ["high-protein", "balanced", "meal-prep"]},
    {"id": 7, "name": "Mediterranean Salad", "calories": 310, "protein": 14, "carbs": 20, "fat": 19, "tags": ["mediterranean", "low-carb", "vegetarian"]},
    {"id": 8, "name": "Protein Smoothie", "calories": 290, "protein": 30, "carbs": 28, "fat": 5, "tags": ["breakfast", "high-protein", "quick"]}
]
# Create different tabs
tab1, tab2, tab3 = st.tabs(["Current Meal Plans", "Create New Plan", "Recipe Database"])
# Current Meal Plans Tab
with tab1:
    st.subheader("Current Meal Plans")
    
    meal_plans = get_meal_plans()
    if not meal_plans:
        meal_plans = [
            {"meal_id": 1, "pc_id": 1, "recipe_id": 1, "quantity": 1, "recipe_name": "Grilled Chicken Salad"},
            {"meal_id": 2, "pc_id": 1, "recipe_id": 4, "quantity": 1, "recipe_name": "Greek Yogurt Parfait"},
            {"meal_id": 3, "pc_id": 2, "recipe_id": 2, "quantity": 1, "recipe_name": "Salmon with Quinoa"},
            {"meal_id": 4, "pc_id": 2, "recipe_id": 6, "quantity": 1, "recipe_name": "Beef and Vegetable Stew"},
            {"meal_id": 5, "pc_id": 3, "recipe_id": 3, "quantity": 1, "recipe_name": "Vegetable Stir Fry"},
            {"meal_id": 6, "pc_id": 4, "recipe_id": 5, "quantity": 1, "recipe_name": "Spinach and Feta Omelette"},
            {"meal_id": 7, "pc_id": 5, "recipe_id": 7, "quantity": 1, "recipe_name": "Mediterranean Salad"}
        ]
    
    # Filter options for clients
    client_names = ["All Clients"] + [client["name"] for client in clients]
    selected_client = st.selectbox("Filter by client:", client_names)
    
    if selected_client != "All Clients":
        client_id = next((client["id"] for client in clients if client["name"] == selected_client), None)
        filtered_plans = [plan for plan in meal_plans if plan.get("pc_id") == client_id]
    else:
        filtered_plans = meal_plans
    
    # Display meal plans with actions
    if filtered_plans:
        for plan in filtered_plans:
            with st.expander(f"{plan['recipe_name']} (Servings: {plan['quantity']})"):
                # Identify client name
                client_name = next((c["name"] for c in clients if c["id"] == plan.get("pc_id")), "Unknown")
                st.write(f"**Client:** {client_name}")
                
                # Find corresponding recipe
                recipe = next((r for r in recipes if r["id"] == plan.get("recipe_id")), None)
                if recipe:
                    st.write(f"**Calories:** {recipe['calories']} per serving")
                    st.write(f"**Protein:** {recipe['protein']}g | **Carbs:** {recipe['carbs']}g | **Fat:** {recipe['fat']}g")
                    st.write(f"**Tags:** {', '.join(recipe['tags'])}")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("Edit", key=f"edit_{plan['meal_id']}"):
                        st.session_state.edit_meal_id = plan['meal_id']
                        st.session_state.edit_meal_data = plan
                        st.rerun()
                with col2:
                    if st.button("Delete", key=f"delete_{plan['meal_id']}"):
                        if delete_meal_plan(plan['meal_id']):
                            st.success("Meal plan deleted successfully!")
                            st.cache_data.clear()
                            time.sleep(1)
                            st.rerun()
                with col3:
                    if st.button("Print", key=f"print_{plan['meal_id']}"):
                        with st.spinner("Generating printable version..."):
                            time.sleep(2)
                            st.success("Meal plan ready for printing!")
                            printable_content = f"""
                            # Meal Plan: {plan['recipe_name']}
                            
                            **Client:** {client_name}
                            **Servings:** {plan['quantity']}
                            
                            ## Nutritional Information (per serving)
                            - Calories: {recipe['calories'] if recipe else 'N/A'}
                            - Protein: {recipe['protein'] if recipe else 'N/A'}g
                            - Carbs: {recipe['carbs'] if recipe else 'N/A'}g
                            - Fat: {recipe['fat'] if recipe else 'N/A'}g
                            
                            ## Preparation Instructions
                            1. Step 1: Prepare ingredients
                            2. Step 2: Cook according to recipe
                            3. Step 3: Serve and enjoy!
                            """
                            st.download_button(
                                label="Download Plan",
                                data=printable_content,
                                file_name=f"meal_plan_{plan['meal_id']}.txt",
                                mime="text/plain"
                            )
        
        # Edit meal plan form
        if 'edit_meal_id' in st.session_state and 'edit_meal_data' in st.session_state:
            meal_id = st.session_state.edit_meal_id
            meal_data = st.session_state.edit_meal_data
            st.subheader(f"Edit Meal Plan: {meal_data['recipe_name']}")
            
            with st.form("edit_meal_form"):
                new_quantity = st.number_input("Number of servings:", min_value=1, value=meal_data['quantity'])
                submit_button = st.form_submit_button("Update Meal Plan")
                if submit_button:
                    update_data = {'quantity': new_quantity}
                    if update_meal_plan(meal_id, update_data):
                        st.success("Meal plan updated successfully!")
                        st.cache_data.clear()
                        del st.session_state.edit_meal_id
                        del st.session_state.edit_meal_data
                        time.sleep(1)
                        st.rerun()
            if st.button("Cancel Edit"):
                del st.session_state.edit_meal_id
                del st.session_state.edit_meal_data
                st.rerun()
    else:
        st.info("No meal plans found. Create a new meal plan in the 'Create New Plan' tab.")
# Create New Plan Tab
with tab2:
    st.subheader("Create New Meal Plan")
    
    with st.form("create_meal_form"):
        # Client selection
        client_options = [f"{client['name']} ({client['diet']})" for client in clients]
        selected_client_option = st.selectbox("Select client:", client_options)
        selected_client_index = client_options.index(selected_client_option)
        selected_client_id = clients[selected_client_index]['id']
        
        # Recipe selection
        recipe_options = [f"{recipe['name']} ({recipe['calories']} cal)" for recipe in recipes]
        selected_recipe_option = st.selectbox("Select recipe:", recipe_options)
        selected_recipe_index = recipe_options.index(selected_recipe_option)
        selected_recipe_id = recipes[selected_recipe_index]['id']
        
        servings = st.number_input("Number of servings:", min_value=1, value=1)
        
        # Check for dietary restrictions and compatibility
        selected_client = clients[selected_client_index]
        selected_recipe = recipes[selected_recipe_index]
        
        allergy_warning = False
        diet_mismatch = False
        
        if selected_client['allergies'] != "None":
            allergy_list = selected_client['allergies'].lower().split(',')
            for allergy in allergy_list:
                if any(allergy.strip() in tag.lower() for tag in selected_recipe['tags']):
                    allergy_warning = True
                    break
        
        diet_mapping = {
            "Low Carb": ["low-carb", "keto"],
            "High Protein": ["high-protein"],
            "Balanced": ["balanced"],
            "Keto": ["keto", "low-carb"],
            "Mediterranean": ["mediterranean"]
        }
        
        if selected_client['diet'] in diet_mapping:
            compatible_tags = diet_mapping[selected_client['diet']]
            if not any(tag in selected_recipe['tags'] for tag in compatible_tags):
                diet_mismatch = True
        
        if allergy_warning:
            st.warning(f"⚠️ Warning: This recipe may contain allergens that {selected_client['name']} is allergic to.")
        if diet_mismatch:
            st.warning(f"⚠️ Warning: This recipe may not be compatible with {selected_client['name']}'s {selected_client['diet']} diet.")
        
        with st.expander("Recipe Preview"):
            st.write(f"**{selected_recipe['name']}**")
            st.write(f"**Calories:** {selected_recipe['calories']} per serving")
            st.write(f"**Protein:** {selected_recipe['protein']}g | **Carbs:** {selected_recipe['carbs']}g | **Fat:** {selected_recipe['fat']}g")
            st.write(f"**Tags:** {', '.join(selected_recipe['tags'])}")
        
        submit_button = st.form_submit_button("Create Meal Plan")
        if submit_button:
            meal_plan_data = {
                'pc_id': selected_client_id,
                'recipe_id': selected_recipe_id,
                'quantity': servings
            }
            result, success = create_meal_plan(meal_plan_data)
            if success:
                st.success(f"Meal plan created successfully for {selected_client['name']}!")
                st.cache_data.clear()
                time.sleep(1)
                tab1.set_active(True)
                st.rerun()
# Recipe Database Tab
with tab3:
    st.subheader("Recipe Database")
    
    search_term = st.text_input("Search recipes:", key="recipe_search")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        diet_options = ["All"] + list(set(tag for recipe in recipes for tag in recipe['tags']))
        selected_diet = st.selectbox("Filter by diet:", diet_options)
    with col2:
        meal_type_options = ["All", "Breakfast", "Lunch", "Dinner", "Snack"]
        selected_meal_type = st.selectbox("Filter by meal type:", meal_type_options)
    with col3:
        sort_options = ["Name", "Calories (Low to High)", "Calories (High to Low)", "Protein (High to Low)"]
        sort_by = st.selectbox("Sort by:", sort_options)
    
    filtered_recipes = recipes.copy()
    if search_term:
        filtered_recipes = [r for r in filtered_recipes if search_term.lower() in r['name'].lower()]
    if selected_diet != "All":
        filtered_recipes = [r for r in filtered_recipes if selected_diet in r['tags']]
    if selected_meal_type != "All":
        filtered_recipes = [r for r in filtered_recipes if selected_meal_type.lower() in r['name'].lower() or selected_meal_type.lower() in " ".join(r['tags']).lower()]
    if sort_by == "Calories (Low to High)":
        filtered_recipes.sort(key=lambda x: x['calories'])
    elif sort_by == "Calories (High to Low)":
        filtered_recipes.sort(key=lambda x: x['calories'], reverse=True)
    elif sort_by == "Protein (High to Low)":
        filtered_recipes.sort(key=lambda x: x['protein'], reverse=True)
    else:
        filtered_recipes.sort(key=lambda x: x['name'])
    
    if filtered_recipes:
        for i in range(0, len(filtered_recipes), 2):
            col1, col2 = st.columns(2)
            with col1:
                if i < len(filtered_recipes):
                    recipe = filtered_recipes[i]
                    st.subheader(recipe['name'])
                    st.write(f"**Calories:** {recipe['calories']} | **Protein:** {recipe['protein']}g")
                    st.write(f"**Carbs:** {recipe['carbs']}g | **Fat:** {recipe['fat']}g")
                    st.write(f"**Tags:** {', '.join(recipe['tags'])}")
                    if st.button("Add to Meal Plan", key=f"add_{recipe['id']}"):
                        st.session_state.selected_recipe_id = recipe['id']
                        tab2.set_active(True)
                        st.rerun()
            with col2:
                if i + 1 < len(filtered_recipes):
                    recipe = filtered_recipes[i + 1]
                    st.subheader(recipe['name'])
                    st.write(f"**Calories:** {recipe['calories']} | **Protein:** {recipe['protein']}g")
                    st.write(f"**Carbs:** {recipe['carbs']}g | **Fat:** {recipe['fat']}g")
                    st.write(f"**Tags:** {', '.join(recipe['tags'])}")
                    if st.button("Add to Meal Plan", key=f"add_{recipe['id']}"):
                        st.session_state.selected_recipe_id = recipe['id']
                        tab2.set_active(True)
                        st.rerun()
    else:
        st.info("No recipes found matching your filters.")

import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from modules.nav import SideBarLinks

API_BASE_URL = "http://web-api:4000"

if not st.session_state.get('authenticated', False) or st.session_state.role != "nutritionist":
    st.warning("Please log in as Nancy to access this page")
    st.stop()

SideBarLinks(st.session_state.role)

@st.cache_data(ttl=300)
def get_users():
    try:
        response = requests.get(f"{API_BASE_URL}/users")
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            st.error(f"Error fetching users: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []

# Get user details
@st.cache_data(ttl=300)
def get_user_details(user_id):
    try:
        response = requests.get(f"{API_BASE_URL}/users/{user_id}")
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            st.error(f"Error fetching user details: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Update user constraints
def update_user_constraints(pc_id, data):
    try:
        response = requests.put(f"{API_BASE_URL}/users/constraints/{pc_id}", json=data)
        if response.status_code == 200:
            return True
        else:
            st.error(f"Error updating constraints: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

# Create user constraints
def create_user_constraints(data):
    try:
        response = requests.post(f"{API_BASE_URL}/users/constraints", json=data)
        if response.status_code == 201:
            return response.json(), True
        else:
            st.error(f"Error creating constraints: {response.status_code}")
            return None, False
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None, False
# Mock client data
clients = [
    {
        "id": 1, 
        "name": "John D.", 
        "age": 27, 
        "goal": "Weight Loss", 
        "diet": "Low Carb", 
        "allergies": "Peanuts",
        "email": "john.d@example.com",
        "phone": "555-123-4567",
        "height": "5'10\"",
        "weight": "185 lbs",
        "activity_level": "Moderate",
        "constraints": {
            "pc_id": 1,
            "budget": 100.00,
            "dietary_restrictions": "peanuts",
            "personal_diet": "low-carb",
            "age_group": "adult"
        }
    },
    {
        "id": 2, 
        "name": "Sarah M.", 
        "age": 34, 
        "goal": "Muscle Gain", 
        "diet": "High Protein", 
        "allergies": "Dairy",
        "email": "sarah.m@example.com",
        "phone": "555-234-5678",
        "height": "5'6\"",
        "weight": "145 lbs",
        "activity_level": "Very Active",
        "constraints": {
            "pc_id": 2,
            "budget": 150.00,
            "dietary_restrictions": "dairy",
            "personal_diet": "high-protein",
            "age_group": "adult"
        }
    },
    {
        "id": 3, 
        "name": "Michael R.", 
        "age": 42, 
        "goal": "Maintenance", 
        "diet": "Balanced", 
        "allergies": "None",
        "email": "michael.r@example.com",
        "phone": "555-345-6789",
        "height": "6'0\"",
        "weight": "190 lbs",
        "activity_level": "Active",
        "constraints": {
            "pc_id": 3,
            "budget": 120.00,
            "dietary_restrictions": "none",
            "personal_diet": "balanced",
            "age_group": "adult"
        }
    },
    {
        "id": 4, 
        "name": "Emma L.", 
        "age": 19, 
        "goal": "Performance", 
        "diet": "Keto", 
        "allergies": "Gluten",
        "email": "emma.l@example.com",
        "phone": "555-456-7890",
        "height": "5'4\"",
        "weight": "128 lbs",
        "activity_level": "Very Active",
        "constraints": {
            "pc_id": 4,
            "budget": 90.00,
            "dietary_restrictions": "gluten",
            "personal_diet": "keto",
            "age_group": "teen"
        }
    },
    {
        "id": 5, 
        "name": "David W.", 
        "age": 55, 
        "goal": "Health", 
        "diet": "Mediterranean", 
        "allergies": "Shellfish",
        "email": "david.w@example.com",
        "phone": "555-567-8901",
        "height": "5'11\"",
        "weight": "205 lbs",
        "activity_level": "Light",
        "constraints": {
            "pc_id": 5,
            "budget": 200.00,
            "dietary_restrictions": "shellfish",
            "personal_diet": "mediterranean",
            "age_group": "older-adult"
        }
    }
]
selected_client_id = st.session_state.get('selected_client_id', None)
selected_client_name = st.session_state.get('selected_client_name', None)

# Main page content
if selected_client_id:
    client = next((c for c in clients if c["id"] == selected_client_id), None)
    
    if client:
        st.title(f"Client Profile: {client['name']}")
        
        # Creates tabs for different sections
        tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Nutrition Plan", "Allergy Management", "Progress"])
        
        # Overview Tab
        with tab1:
            col1, col2 = st.columns([1, 2])
            
            # Basic info column
            with col1:
                st.subheader("Basic Information")
                st.write(f"**Age:** {client['age']}")
                st.write(f"**Email:** {client['email']}")
                st.write(f"**Phone:** {client['phone']}")
                st.write(f"**Height:** {client['height']}")
                st.write(f"**Weight:** {client['weight']}")
                st.write(f"**Activity Level:** {client['activity_level']}")
                st.write(f"**Goal:** {client['goal']}")
                st.write(f"**Diet Type:** {client['diet']}")
                st.write(f"**Allergies:** {client['allergies']}")
                
                if st.button("Edit Profile"):
                    st.session_state.edit_profile = True
            
            # Nutrition overview column
            with col2:
                st.subheader("Nutrition Overview")
            # Edit profile form
            if st.session_state.get('edit_profile', False):
                st.markdown("---")
                st.subheader("Edit Client Profile")
                
                with st.form("edit_profile_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        new_age = st.number_input("Age:", min_value=16, max_value=100, value=client['age'])
                        new_height = st.text_input("Height:", value=client['height'])
                        new_weight = st.text_input("Weight:", value=client['weight'])
                    
                    with col2:
                        new_email = st.text_input("Email:", value=client['email'])
                        new_phone = st.text_input("Phone:", value=client['phone'])
                        new_activity = st.selectbox(
                            "Activity Level:",
                            ["Sedentary", "Light", "Moderate", "Active", "Very Active"],
                            index=["Sedentary", "Light", "Moderate", "Active", "Very Active"].index(client['activity_level']) if client['activity_level'] in ["Sedentary", "Light", "Moderate", "Active", "Very Active"] else 0
                        )
                    
                    # Dietary preferences
                    st.subheader("Dietary Information")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        new_goal = st.selectbox(
                            "Goal:",
                            ["Weight Loss", "Muscle Gain", "Maintenance", "Performance", "Health"],
                            index=["Weight Loss", "Muscle Gain", "Maintenance", "Performance", "Health"].index(client['goal']) if client['goal'] in ["Weight Loss", "Muscle Gain", "Maintenance", "Performance", "Health"] else 0
                        )
                        
                        new_diet = st.selectbox(
                            "Diet Type:",
                            ["Low Carb", "High Protein", "Balanced", "Keto", "Mediterranean", "Vegan", "Vegetarian"],
                            index=["Low Carb", "High Protein", "Balanced", "Keto", "Mediterranean", "Vegan", "Vegetarian"].index(client['diet']) if client['diet'] in ["Low Carb", "High Protein", "Balanced", "Keto", "Mediterranean", "Vegan", "Vegetarian"] else 0
                        )
                    
                    with col2:
                        new_allergies = st.text_input("Allergies (comma-separated):", value=client['allergies'])
                        new_budget = st.number_input("Weekly Budget ($):", min_value=50.0, max_value=500.0, value=float(client['constraints']['budget']), step=10.0)
                        new_age_group = st.selectbox(
                            "Age Group:",
                            ["child", "teen", "adult", "older-adult"],
                            index=["child", "teen", "adult", "older-adult"].index(client['constraints']['age_group']) if client['constraints']['age_group'] in ["child", "teen", "adult", "older-adult"] else 0
                        )
                    
                    # Submit and cancel buttons
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        submit_button = st.form_submit_button("Save Changes")
                    
                    with col2:
                        cancel_button = st.form_submit_button("Cancel")
                    
                    if submit_button:
                        constraints_data = {
                            'dietary_restrictions': new_allergies.lower(),
                            'personal_diet': new_diet.lower().replace(' ', '-'),
                            'age_group': new_age_group,
                            'budget': new_budget
                        }
                        
                        st.success("Client profile updated successfully!")
                        if 'edit_profile' in st.session_state:
                            del st.session_state.edit_profile
                        time.sleep(1)
                        st.rerun()
                    
                    if cancel_button:
                        if 'edit_profile' in st.session_state:
                            del st.session_state.edit_profile
                        st.rerun()
        # Nutrition Plan Tab
        with tab2:
            st.subheader("Client Nutrition Plan")
            
            st.write("### Macronutrient Targets")
            
            # Calculate macros based on client profile
            weight_lbs = float(client['weight'].split()[0])
            weight_kg = weight_lbs * 0.453592
            
            activity_multipliers = {
                "Sedentary": 1.2,
                "Light": 1.375,
                "Moderate": 1.55,
                "Active": 1.725,
                "Very Active": 1.9
            }
            
            if client['age'] < 30:
                bmr = 25 * weight_kg if client['height'].split("'")[0] > "5" else 24 * weight_kg
            else:
                bmr = 23 * weight_kg if client['height'].split("'")[0] > "5" else 22 * weight_kg
            
            activity_factor = activity_multipliers.get(client['activity_level'], 1.55)
            tdee = bmr * activity_factor
            
            if client['goal'] == "Weight Loss":
                calorie_target = tdee * 0.85
                protein_target = weight_kg * 2.2
                fat_target = weight_kg * 1.0
            elif client['goal'] == "Muscle Gain":
                calorie_target = tdee * 1.1
                protein_target = weight_kg * 2.5
                fat_target = weight_kg * 1.0
            elif client['goal'] == "Performance":
                calorie_target = tdee * 1.05
                protein_target = weight_kg * 2.0
                fat_target = weight_kg * 1.1
            else:
                calorie_target = tdee
                protein_target = weight_kg * 1.8
                fat_target = weight_kg * 1.1
            
            protein_calories = protein_target * 4
            fat_calories = fat_target * 9
            carb_calories = calorie_target - protein_calories - fat_calories
            carb_target = carb_calories / 4
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Daily Calories", f"{calorie_target:.0f} kcal")
            with col2:
                st.metric("Protein", f"{protein_target:.0f}g")
            with col3:
                st.metric("Carbs", f"{carb_target:.0f}g")
            
            st.write("### Daily Meal Plan")
            
            # Mock meal plan
            meals = [
                {"name": "Breakfast", "description": "Greek yogurt with berries and granola", "calories": 350, "protein": 20, "carbs": 40, "fat": 10},
                {"name": "Snack", "description": "Apple with almond butter", "calories": 200, "protein": 5, "carbs": 25, "fat": 10},
                {"name": "Lunch", "description": "Grilled chicken salad with olive oil dressing", "calories": 450, "protein": 35, "carbs": 20, "fat": 25},
                {"name": "Snack", "description": "Protein shake with banana", "calories": 250, "protein": 25, "carbs": 30, "fat": 3},
                {"name": "Dinner", "description": "Salmon with quinoa and roasted vegetables", "calories": 550, "protein": 40, "carbs": 45, "fat": 22}
            ]
            
            for meal in meals:
                with st.expander(f"{meal['name']} - {meal['calories']} calories"):
                    st.write(f"**{meal['description']}**")
                    st.write(f"**Protein:** {meal['protein']}g | **Carbs:** {meal['carbs']}g | **Fat:** {meal['fat']}g")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Edit", key=f"edit_{meal['name']}"):
                            st.session_state.edit_meal = meal['name']
                    with col2:
                        if st.button("View Recipe", key=f"recipe_{meal['name']}"):
                            st.info(f"This would show the detailed recipe for {meal['description']}")
            
            if st.button("+ Add Meal"):
                st.session_state.add_meal = True
            
            # Meal edit form
            if st.session_state.get('edit_meal'):
                meal_name = st.session_state.edit_meal
                meal = next((m for m in meals if m['name'] == meal_name), None)
                
                if meal:
                    st.markdown("---")
                    st.subheader(f"Edit {meal_name}")
                    
                    with st.form("edit_meal_form"):
                        new_description = st.text_input("Description:", value=meal['description'])
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            new_calories = st.number_input("Calories:", min_value=0, value=meal['calories'])
                        with col2:
                            new_protein = st.number_input("Protein (g):", min_value=0.0, value=float(meal['protein']))
                        with col3:
                            new_carbs = st.number_input("Carbs (g):", min_value=0.0, value=float(meal['carbs']))
                            new_fat = st.number_input("Fat (g):", min_value=0.0, value=float(meal['fat']))
                        col1, col2 = st.columns(2)
                        with col1:
                            submit = st.form_submit_button("Save Changes")
                        with col2:
                            cancel = st.form_submit_button("Cancel")
                        
                        if submit:
                            st.success(f"{meal_name} updated successfully!")
                            if 'edit_meal' in st.session_state:
                                del st.session_state.edit_meal
                            time.sleep(1)
                            st.rerun()
                        if cancel:
                            if 'edit_meal' in st.session_state:
                                del st.session_state.edit_meal
                            st.rerun()
            
            # Add meal form
            if st.session_state.get('add_meal', False):
                st.markdown("---")
                st.subheader("Add New Meal")
                
                with st.form("add_meal_form"):
                    new_meal_name = st.text_input("Meal Name:")
                    new_description = st.text_input("Description:")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        new_calories = st.number_input("Calories:", min_value=0, value=0)
                    with col2:
                        new_protein = st.number_input("Protein (g):", min_value=0.0, value=0.0)
                    with col3:
                        new_carbs = st.number_input("Carbs (g):", min_value=0.0, value=0.0)
                        new_fat = st.number_input("Fat (g):", min_value=0.0, value=0.0)
                    col1, col2 = st.columns(2)
                    with col1:
                        submit = st.form_submit_button("Add Meal")
                    with col2:
                        cancel = st.form_submit_button("Cancel")
                    
                    if submit and new_meal_name and new_description:
                        st.success(f"{new_meal_name} added successfully!")
                        if 'add_meal' in st.session_state:
                            del st.session_state.add_meal
                        time.sleep(1)
                        st.rerun()
                    if cancel:
                        if 'add_meal' in st.session_state:
                            del st.session_state.add_meal
                        st.rerun()
            
            # Export Meal Plan
            st.markdown("---")
            if st.button("Export Meal Plan"):
                with st.spinner("Generating meal plan..."):
                    time.sleep(2)
                    meal_plan_text = f"# Meal Plan for {client['name']}\n\n"
                    meal_plan_text += f"**Daily Targets:**\n"
                    meal_plan_text += f"- Calories: {calorie_target:.0f} kcal\n"
                    meal_plan_text += f"- Protein: {protein_target:.0f}g\n"
                    meal_plan_text += f"- Carbs: {carb_target:.0f}g\n"
                    meal_plan_text += f"- Fat: {fat_target:.0f}g\n\n"
                    meal_plan_text += f"**Meals:**\n\n"
                    for meal in meals:
                        meal_plan_text += f"### {meal['name']} ({meal['calories']} calories)\n"
                        meal_plan_text += f"{meal['description']}\n"
                        meal_plan_text += f"Protein: {meal['protein']}g | Carbs: {meal['carbs']}g | Fat: {meal['fat']}g\n\n"
                    
                    st.download_button(
                        label="Download Meal Plan",
                        data=meal_plan_text,
                        file_name=f"meal_plan_{client['name'].replace(' ', '_')}.txt",
                        mime="text/plain"
                    )

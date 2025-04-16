import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from modules.nav import SideBarLinks

# API base URL
API_BASE_URL = "http://web-api:4000"

# Authentication check
if not st.session_state.get('authenticated', False) or st.session_state.role != "athlete":
    st.warning("Please log in as Riley to access this page")
    st.stop()

# Set up navigation
SideBarLinks(st.session_state.role)

# Page header
st.title("🍽️ Athlete Meal Plans")
st.write("Optimize your nutrition with targeted meal plans for different training phases")

# Function to get meal plans
@st.cache_data(ttl=300)
def get_meal_plans(client_id=1):
    try:
        response = requests.get(f"{API_BASE_URL}/meal-plans?client_id={client_id}")
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            st.error(f"Error fetching meal plans: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []

# Function to create meal plan
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

# Function to delete meal plan
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

# Create tabs for different meal plan categories
tab1, tab2, tab3, tab4 = st.tabs(["Current Plans", "Race Day", "Recovery", "Training Phases"])

# Current Plans Tab
with tab1:
    st.subheader("Current Meal Plans")
    
    # Get existing meal plans
    meal_plans = get_meal_plans()
    
    # Mock meal plans if none are returned
    if not meal_plans:
        meal_plans = [
            {"meal_id": 1, "recipe_id": 1, "recipe_name": "Pre-Run Oatmeal Bowl", "quantity": 1},
            {"meal_id": 2, "recipe_id": 2, "recipe_name": "Recovery Protein Smoothie", "quantity": 1},
            {"meal_id": 3, "recipe_id": 3, "recipe_name": "Salmon & Quinoa Dinner", "quantity": 1},
            {"meal_id": 4, "recipe_id": 4, "recipe_name": "Carb-Loading Pasta", "quantity": 2}
        ]
    
    # Mock recipe data with training phase tags
    recipes = {
        1: {
            "name": "Pre-Run Oatmeal Bowl",
            "description": "Quick energy oatmeal with banana and honey",
            "calories": 380,
            "protein": 12,
            "carbs": 68,
            "fat": 8,
            "phase": "Pre-Workout"
        },
        2: {
            "name": "Recovery Protein Smoothie",
            "description": "Protein-packed smoothie with berries and banana",
            "calories": 320,
            "protein": 30,
            "carbs": 42,
            "fat": 5,
            "phase": "Recovery"
        },
        3: {
            "name": "Salmon & Quinoa Dinner",
            "description": "Omega-3 rich salmon with quinoa and vegetables",
            "calories": 450,
            "protein": 35,
            "carbs": 40,
            "fat": 18,
            "phase": "Maintenance"
        },
        4: {
            "name": "Carb-Loading Pasta",
            "description": "High-carb pasta dish for pre-race fueling",
            "calories": 580,
            "protein": 20,
            "carbs": 95,
            "fat": 12,
            "phase": "Race Day"
        }
    }
    
    # Display meal plans grouped by training phase
    if meal_plans:
        # Group by phase
        phases = set(recipes[meal["recipe_id"]]["phase"] for meal in meal_plans if meal["recipe_id"] in recipes)
        
        for phase in phases:
            st.write(f"### {phase} Meals")
            
            phase_meals = [meal for meal in meal_plans 
                          if meal["recipe_id"] in recipes and recipes[meal["recipe_id"]]["phase"] == phase]
            
            for meal in phase_meals:
                recipe = recipes.get(meal["recipe_id"])
                
                if recipe:
                    with st.expander(f"{recipe['name']} - {recipe['calories']} calories"):
                        st.write(f"**Description:** {recipe['description']}")
                        st.write(f"**Nutrition:** Protein: {recipe['protein']}g | Carbs: {recipe['carbs']}g | Fat: {recipe['fat']}g")
                        st.write(f"**Servings:** {meal['quantity']}")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            if st.button("View Recipe", key=f"view_{meal['meal_id']}"):
                                st.session_state.view_recipe = meal['recipe_id']
                                st.success(f"Viewing recipe for {recipe['name']}")
                        
                        with col2:
                            if st.button("Remove Plan", key=f"remove_{meal['meal_id']}"):
                                if delete_meal_plan(meal['meal_id']):
                                    st.success("Meal plan removed successfully!")
                                    st.cache_data.clear()
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    # Mock successful removal
                                    st.success("Meal plan removed successfully! (Mock)")
                                    time.sleep(1)
                                    st.rerun()

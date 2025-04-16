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

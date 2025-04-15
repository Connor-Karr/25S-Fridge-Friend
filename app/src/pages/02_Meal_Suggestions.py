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
if not st.session_state.get('authenticated', False) or st.session_state.role != "busy_student":
    st.warning("Please log in as Ben to access this page")
    st.stop()

# Set up navigation
SideBarLinks(st.session_state.role)

# Page header
st.title("🍲 Meal Suggestions")
st.write("Find recipes based on what's in your fridge and your budget")

# Function to get fridge inventory
@st.cache_data(ttl=300)
def get_fridge_inventory():
    try:
        response = requests.get(f"{API_BASE_URL}/fridge?client_id=1")
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            st.error(f"Error fetching inventory: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []

# Function to get meal plans
@st.cache_data(ttl=300)
def get_meal_plans():
    try:
        response = requests.get(f"{API_BASE_URL}/meal-plans?client_id=1")
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            st.error(f"Error fetching meal plans: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []

# Get current inventory and meal plans
inventory = get_fridge_inventory()
meal_plans = get_meal_plans()

# If no inventory or meal plans, use mock data
if not inventory:
    # Mock data for inventory
    inventory = [
        {"ingredient_id": 1, "name": "Chicken Breast", "quantity": 2, "expiration_date": "2025-04-20", "is_expired": False},
        {"ingredient_id": 2, "name": "Rice", "quantity": 1.5, "expiration_date": "2025-06-15", "is_expired": False},
        {"ingredient_id": 3, "name": "Broccoli", "quantity": 1, "expiration_date": "2025-04-18", "is_expired": False},
        {"ingredient_id": 4, "name": "Eggs", "quantity": 8, "expiration_date": "2025-04-25", "is_expired": False},
        {"ingredient_id": 5, "name": "Milk", "quantity": 1, "expiration_date": "2025-04-19", "is_expired": False},
        {"ingredient_id": 6, "name": "Bread", "quantity": 0.5, "expiration_date": "2025-04-17", "is_expired": False},
        {"ingredient_id": 7, "name": "Pasta", "quantity": 1, "expiration_date": "2025-05-30", "is_expired": False},
        {"ingredient_id": 8, "name": "Tomatoes", "quantity": 3, "expiration_date": "2025-04-16", "is_expired": False}
    ]

if not meal_plans:
    # Mock data for meal plans
    meal_plans = [
        {"meal_id": 1, "recipe_id": 1, "recipe_name": "Chicken and Rice Bowl", "quantity": 2},
        {"meal_id": 2, "recipe_id": 2, "recipe_name": "Veggie Pasta", "quantity": 1},
        {"meal_id": 3, "recipe_id": 3, "recipe_name": "Breakfast Scramble", "quantity": 1},
        {"meal_id": 4, "recipe_id": 4, "recipe_name": "Chicken Stir Fry", "quantity": 2},
        {"meal_id": 5, "recipe_id": 5, "recipe_name": "Simple Sandwich", "quantity": 1}
    ]

# Create tabs for different suggestion types
tab1, tab2, tab3 = st.tabs(["Quick Meals", "Budget-Friendly", "Using Expiring Items"])

# Recipe data structure with ingredient IDs, time to prepare, and cost
recipes = [
    {
        "id": 1, 
        "name": "Chicken and Rice Bowl", 
        "ingredients": [1, 2], 
        "prep_time": 20, 
        "cost": 3.50,
        "description": "Simple bowl with grilled chicken over rice",
        "instructions": "1. Cook rice according to package instructions\n2. Season chicken with salt and pepper\n3. Grill chicken for 6-8 minutes per side\n4. Slice chicken and serve over rice",
        "calories": 450,
        "protein": 35,
        "carbs": 45,
        "fat": 12
    },
    {
        "id": 2, 
        "name": "Veggie Pasta", 
        "ingredients": [7, 8, 3], 
        "prep_time": 15, 
        "cost": 2.75,
        "description": "Simple pasta with tomatoes and vegetables",
        "instructions": "1. Boil pasta until al dente\n2. Sauté tomatoes and broccoli\n3. Mix with pasta and season with salt and pepper",
        "calories": 380,
        "protein": 12,
        "carbs": 65,
        "fat": 8
    },
    {
        "id": 3, 
        "name": "Breakfast Scramble", 
        "ingredients": [4, 5], 
        "prep_time": 10, 
        "cost": 1.50,
        "description": "Quick and easy egg scramble",
        "instructions": "1. Beat eggs with a splash of milk\n2. Cook in a pan over medium heat\n3. Season with salt and pepper",
        "calories": 250,
        "protein": 18,
        "carbs": 8,
        "fat": 15
    },
    {
        "id": 4, 
        "name": "Chicken Stir Fry", 
        "ingredients": [1, 3], 
        "prep_time": 25, 
        "cost": 4.00,
        "description": "Stir-fried chicken with broccoli",
        "instructions": "1. Cut chicken into small pieces\n2. Stir-fry chicken until cooked through\n3. Add broccoli and cook until tender\n4. Season with soy sauce and serve",
        "calories": 320,
        "protein": 28,
        "carbs": 15,
        "fat": 14
    },
    {
        "id": 5, 
        "name": "Simple Sandwich", 
        "ingredients": [6], 
        "prep_time": 5, 
        "cost": 1.25,
        "description": "Quick and easy sandwich",
        "instructions": "1. Toast bread if desired\n2. Add your favorite toppings\n3. Enjoy!",
        "calories": 200,
        "protein": 8,
        "carbs": 25,
        "fat": 6
    }
]

# Quick Meals Tab
with tab1:
    st.subheader("Quick Meal Ideas (Under 15 Minutes)")
    
    # Filter recipes by prep time
    quick_recipes = [recipe for recipe in recipes if recipe["prep_time"] <= 15]
    
    # Check which recipes can be made with available ingredients
    available_quick_recipes = []
    for recipe in quick_recipes:
        # Get list of ingredient IDs in the fridge
        fridge_ingredient_ids = [item["ingredient_id"] for item in inventory]
        
        # Check if all required ingredients are available
        if all(ing_id in fridge_ingredient_ids for ing_id in recipe["ingredients"]):
            available_quick_recipes.append(recipe)
    
    # Display available quick recipes
    if available_quick_recipes:
        for recipe in available_quick_recipes:
            with st.expander(f"{recipe['name']} - {recipe['prep_time']} mins"):
                st.write(f"**Description:** {recipe['description']}")
                st.write(f"**Preparation Time:** {recipe['prep_time']} minutes")
                st.write(f"**Cost Estimate:** ${recipe['cost']:.2f}")
                st.write(f"**Calories:** {recipe['calories']} | **Protein:** {recipe['protein']}g | **Carbs:** {recipe['carbs']}g | **Fat:** {recipe['fat']}g")
                
                # Show ingredients
                st.write("**Ingredients:**")
                for ing_id in recipe["ingredients"]:
                    for item in inventory:
                        if item["ingredient_id"] == ing_id:
                            st.write(f"- {item['name']} ({item['quantity']} available)")
                
                st.write("**Instructions:**")
                st.write(recipe["instructions"])
                
                # Cook now or save as meal plan buttons
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("Cook Now", key=f"cook_{recipe['id']}"):
                        st.success(f"Preparing {recipe['name']}!")
                        time.sleep(1)
                        
                        # Show step-by-step
                        for i, step in enumerate(recipe["instructions"].split('\n')):
                            st.write(f"Step {i+1}: {step}")
                            time.sleep(0.5)
                
                with col2:
                    if st.button("Add to Meal Plan", key=f"save_{recipe['id']}"):
                        # Mock creating a meal plan
                        with st.spinner("Adding to meal plan..."):
                            time.sleep(1)
                            st.success(f"Added {recipe['name']} to your meal plan!")
    else:
        st.info("No quick recipes available with your current ingredients.")
        
        # Show what's missing for quick recipes
        st.subheader("What you're missing for quick meals:")
        
        for recipe in quick_recipes:
            missing_ingredients = []
            fridge_ingredient_ids = [item["ingredient_id"] for item in inventory]
            
            for ing_id in recipe["ingredients"]:
                if ing_id not in fridge_ingredient_ids:
                    # Find the ingredient name
                    for rec in recipes:
                        if rec["id"] == ing_id:
                            missing_ingredients.append(rec["name"])
                            break
            
            if missing_ingredients:
                st.write(f"**{recipe['name']}** - Missing: {', '.join(missing_ingredients)}")
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
# Budget-Friendly Tab
with tab2:
    st.subheader("Budget-Friendly Meals (Under $3)")
    
    # Filter recipes by cost
    budget_recipes = [recipe for recipe in recipes if recipe["cost"] <= 3.00]
    
    # Check which recipes can be made with available ingredients
    available_budget_recipes = []
    for recipe in budget_recipes:
        # Get list of ingredient IDs in the fridge
        fridge_ingredient_ids = [item["ingredient_id"] for item in inventory]
        
        # Check if all required ingredients are available
        if all(ing_id in fridge_ingredient_ids for ing_id in recipe["ingredients"]):
            available_budget_recipes.append(recipe)
    
    # Display available budget recipes
    if available_budget_recipes:
        # Sort by cost
        available_budget_recipes.sort(key=lambda x: x["cost"])
        
        for recipe in available_budget_recipes:
            with st.expander(f"{recipe['name']} - ${recipe['cost']:.2f}"):
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
                    if st.button("Cook Now", key=f"cook_budget_{recipe['id']}"):
                        st.success(f"Preparing {recipe['name']}!")
                        # Mock cooking steps
                        
                with col2:
                    if st.button("Add to Meal Plan", key=f"save_budget_{recipe['id']}"):
                        # Mock creating a meal plan
                        with st.spinner("Adding to meal plan..."):
                            time.sleep(1)
                            st.success(f"Added {recipe['name']} to your meal plan!")
    else:
        st.info("No budget-friendly recipes available with your current ingredients.")
        
        # Show what's missing for budget recipes
        st.subheader("What you're missing for budget-friendly meals:")
        
        for recipe in budget_recipes:
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
    
    # Weekly budget tracking
    st.markdown("---")
    st.subheader("Weekly Grocery Budget")
    
    # Mock budget data
    budget_total = 100
    spent_so_far = 62.35
    remaining = budget_total - spent_so_far
    
    # Display budget information
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Budget", f"${budget_total:.2f}")
    
    with col2:
        st.metric("Spent", f"${spent_so_far:.2f}")
    
    with col3:
        st.metric("Remaining", f"${remaining:.2f}")
    
    # Budget visualization
    st.progress(spent_so_far / budget_total)
    
    # Budget tips
    with st.expander("Budget-Saving Tips"):
        st.write("""
        1. **Meal Planning:** Plan your meals to avoid impulse purchases
        2. **Bulk Buying:** Purchase staples like rice, pasta, and beans in bulk
        3. **Seasonal Produce:** Buy fruits and vegetables that are in season
        4. **Reduce Food Waste:** Use leftovers creatively in new meals
        5. **Store Brands:** Choose store brands over name brands when possible
        """)
# Using Expiring Items Tab
with tab3:
    st.subheader("Recipes Using Soon-to-Expire Items")
    
    # Filter inventory for items expiring soon (within 3 days)
    today = datetime.now().date()
    expiring_soon = []
    
    for item in inventory:
        if item.get("expiration_date"):
            exp_date = datetime.strptime(item["expiration_date"], '%Y-%m-%d').date()
            days_left = (exp_date - today).days
            
            if 0 <= days_left <= 3 and not item.get("is_expired", False):
                expiring_soon.append(item)
    
    # Display expiring items
    if expiring_soon:
        st.warning(f"You have {len(expiring_soon)} items expiring within the next 3 days.")
        
        # Display expiring items
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Expiring Soon:**")
            for item in expiring_soon:
                exp_date = datetime.strptime(item["expiration_date"], '%Y-%m-%d').date()
                days_left = (exp_date - today).days
                
                if days_left == 0:
                    st.write(f"- {item['name']} (Expires today!)")
                else:
                    st.write(f"- {item['name']} (Expires in {days_left} days)")
        
        # Find recipes that use expiring items
        with col2:
            expiring_ids = [item["ingredient_id"] for item in expiring_soon]
            recipes_using_expiring = []
            
            for recipe in recipes:
                if any(ing_id in expiring_ids for ing_id in recipe["ingredients"]):
                    recipes_using_expiring.append(recipe)
            
            if recipes_using_expiring:
                st.write("**Recommended Recipes:**")
                for recipe in recipes_using_expiring:
                    st.write(f"- {recipe['name']} ({recipe['prep_time']} mins)")
            else:
                st.write("No specific recipes found for expiring items.")
        
        # Display detailed recipes using expiring items
        st.subheader("Recipe Details")
        
        if recipes_using_expiring:
            for recipe in recipes_using_expiring:
                # Highlight which ingredients are expiring
                expiring_ingredients = []
                for ing_id in recipe["ingredients"]:
                    if ing_id in expiring_ids:
                        for item in expiring_soon:
                            if item["ingredient_id"] == ing_id:
                                expiring_ingredients.append(item["name"])
                
                with st.expander(f"{recipe['name']} (Uses {', '.join(expiring_ingredients)})"):
                    st.write(f"**Description:** {recipe['description']}")
                    st.write(f"**Preparation Time:** {recipe['prep_time']} minutes")
                    st.write(f"**Cost Estimate:** ${recipe['cost']:.2f}")
                    st.write(f"**Calories:** {recipe['calories']} | **Protein:** {recipe['protein']}g | **Carbs:** {recipe['carbs']}g | **Fat:** {recipe['fat']}g")
                    
                    # Show ingredients
                    st.write("**Ingredients:**")
                    for ing_id in recipe["ingredients"]:
                        for item in inventory:
                            if item["ingredient_id"] == ing_id:
                                if ing_id in expiring_ids:
                                    st.markdown(f"- **{item['name']}** ({item['quantity']} available) - **EXPIRING SOON!**")
                                else:
                                    st.write(f"- {item['name']} ({item['quantity']} available)")
                    
                    st.write("**Instructions:**")
                    st.write(recipe["instructions"])
                    
                    # Cook now button
                    if st.button("Cook Now", key=f"cook_expiring_{recipe['id']}"):
                        st.success(f"Preparing {recipe['name']}!")
                        # Mock cooking steps
        else:
            st.info("No recipes found that use your expiring ingredients.")
            
            # Suggest creative uses
            st.subheader("Creative Ways to Use Expiring Items")
            
            creative_uses = {
                "Vegetables": "Make a quick stir-fry or soup",
                "Fruits": "Blend into smoothies or freeze for later",
                "Bread": "Make croutons or bread pudding",
                "Milk": "Use in pancakes, baking, or make pudding",
                "Eggs": "Hard boil for quick snacks",
                "Meat": "Cook and freeze in portions for future meals"
            }
            
            for item in expiring_soon:
                item_type = None
                item_name = item["name"].lower()
                
                if "chicken" in item_name or "beef" in item_name or "pork" in item_name:
                    item_type = "Meat"
                elif "bread" in item_name:
                    item_type = "Bread"
                elif "milk" in item_name:
                    item_type = "Milk"
                elif "egg" in item_name:
                    item_type = "Eggs"
                elif any(veggie in item_name for veggie in ["broccoli", "carrot", "spinach", "tomato"]):
                    item_type = "Vegetables"
                elif any(fruit in item_name for fruit in ["apple", "banana", "berry", "orange"]):
                    item_type = "Fruits"
                
                if item_type and item_type in creative_uses:
                    st.write(f"**{item['name']}**: {creative_uses[item_type]}")
    else:
        st.success("No items expiring soon. Your fridge is in good shape!")

# Show more complex recipe ideas
st.markdown("---")
st.subheader("Weekend Cooking Projects")

# Mock complex recipes
complex_recipes = [
    {
        "name": "Homemade Pizza",
        "description": "Make your own pizza from scratch with dough and toppings",
        "time": "2 hours",
        "difficulty": "Medium",
        "cost": "$5.00"
    },
    {
        "name": "Slow-Cooked Chili",
        "description": "Rich and flavorful chili perfect for meal prep",
        "time": "3 hours",
        "difficulty": "Easy",
        "cost": "$8.00"
    },
    {
        "name": "Pasta Carbonara from Scratch",
        "description": "Classic Italian pasta dish with egg, cheese, and bacon",
        "time": "45 minutes",
        "difficulty": "Medium",
        "cost": "$6.50"
    }
]

# Display complex recipes
for recipe in complex_recipes:
    st.write(f"**{recipe['name']}** - {recipe['description']}")
    st.write(f"Time: {recipe['time']} | Difficulty: {recipe['difficulty']} | Cost: {recipe['cost']}")
    
    if st.button("View Recipe", key=f"view_{recipe['name']}"):
        st.info(f"This would display the full recipe for {recipe['name']}.")

# Tips section
st.markdown("---")
st.subheader("Student Cooking Tips")

tips = [
    "**Batch Cook**: Prepare large portions on weekends to eat throughout the week.",
    "**One-Pot Meals**: Save on dishes and time with simple one-pot recipes.",
    "**Learn 5 Basic Recipes**: Master a few versatile recipes you can modify with different ingredients.",
    "**Use a Slow Cooker**: Prep in the morning for a ready meal when you return from classes.",
    "**Frozen Vegetables**: Keep frozen vegetables on hand for quick nutrition when fresh produce runs out."
]

# Show random tip
tip_index = datetime.now().day % len(tips)  # Changes daily
st.info(f"Tip of the Day: {tips[tip_index]}")

# Show all tips
with st.expander("View All Tips"):
    for tip in tips:
        st.write(tip)
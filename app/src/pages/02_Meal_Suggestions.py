import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from modules.nav import SideBarLinks

# Add sidebar navigation
SideBarLinks(st.session_state.role)

# Authentication check
if not st.session_state.get('authenticated', False) or st.session_state.role != "busy_student":
    st.warning("Please log in as Ben to access this page")
    st.stop()

# Page header
st.title("Meal Suggestions")

# Get fridge inventory
try:
    response = requests.get("http://web-api:4000/fridge?client_id=1")
    if response.status_code == 200:
        inventory = response.json()
    else:
        inventory = []
except:
    inventory = []

# Use mock data if no inventory
if not inventory:
    inventory = [
        {"ingredient_id": 1, "name": "Chicken Breast", "quantity": 2, "expiration_date": "2025-04-20"},
        {"ingredient_id": 2, "name": "Rice", "quantity": 1.5, "expiration_date": "2025-06-15"},
        {"ingredient_id": 3, "name": "Broccoli", "quantity": 1, "expiration_date": "2025-04-18"},
        {"ingredient_id": 4, "name": "Eggs", "quantity": 8, "expiration_date": "2025-04-25"},
        {"ingredient_id": 5, "name": "Milk", "quantity": 1, "expiration_date": "2025-04-19"},
        {"ingredient_id": 6, "name": "Bread", "quantity": 0.5, "expiration_date": "2025-04-17"},
        {"ingredient_id": 7, "name": "Pasta", "quantity": 1, "expiration_date": "2025-05-30"},
        {"ingredient_id": 8, "name": "Tomatoes", "quantity": 3, "expiration_date": "2025-04-16"}
    ]

# Recipe data
recipes = [
    {
        "id": 1, 
        "name": "Chicken and Rice Bowl", 
        "ingredients": [1, 2], 
        "prep_time": 20, 
        "cost": 3.50,
        "instructions": "Cook rice. Grill chicken. Serve together."
    },
    {
        "id": 2, 
        "name": "Veggie Pasta", 
        "ingredients": [7, 8, 3], 
        "prep_time": 15, 
        "cost": 2.75,
        "instructions": "Boil pasta. Sauté vegetables. Mix together."
    },
    {
        "id": 3, 
        "name": "Breakfast Scramble", 
        "ingredients": [4, 5], 
        "prep_time": 10, 
        "cost": 1.50,
        "instructions": "Beat eggs with milk. Cook in pan. Season and serve."
    },
    {
        "id": 4, 
        "name": "Chicken Stir Fry", 
        "ingredients": [1, 3], 
        "prep_time": 25, 
        "cost": 4.00,
        "instructions": "Cut chicken. Stir-fry with broccoli. Season and serve."
    },
    {
        "id": 5, 
        "name": "Simple Sandwich", 
        "ingredients": [6], 
        "prep_time": 5, 
        "cost": 1.25,
        "instructions": "Toast bread. Add toppings. Enjoy!"
    }
]

# Create tabs
tab1, tab2, tab3 = st.tabs(["Quick Meals", "Budget-Friendly", "Using Expiring Items"])

# Tab 1: Quick Meals
with tab1:
    st.subheader("Quick Meals (Under 15 Minutes)")
    
    # Filter recipes by prep time
    quick_recipes = [recipe for recipe in recipes if recipe["prep_time"] <= 15]
    
    # Create dataframe
    if quick_recipes:
        quick_data = []
        for recipe in quick_recipes:
            quick_data.append({
                "Name": recipe["name"],
                "Prep Time": f"{recipe['prep_time']} mins",
                "Cost": f"${recipe['cost']:.2f}",
                "Instructions": recipe["instructions"]
            })
        
        # Display table
        st.table(pd.DataFrame(quick_data))
    else:
        st.info("No quick recipes available")

# Tab 2: Budget-Friendly
with tab2:
    st.subheader("Budget-Friendly Meals (Under $3)")
    
    # Filter recipes by cost
    budget_recipes = [recipe for recipe in recipes if recipe["cost"] <= 3.00]
    
    # Create dataframe
    if budget_recipes:
        budget_data = []
        for recipe in budget_recipes:
            budget_data.append({
                "Name": recipe["name"],
                "Cost": f"${recipe['cost']:.2f}",
                "Prep Time": f"{recipe['prep_time']} mins",
                "Instructions": recipe["instructions"]
            })
        
        # Display table
        st.table(pd.DataFrame(budget_data))
    else:
        st.info("No budget-friendly recipes available")
    
    # Budget overview
    st.subheader("Budget Overview")
    budget_total = 100
    budget_used = 62.35
    budget_remaining = budget_total - budget_used
    
    budget_data = [
        {"Category": "Total Budget", "Amount": f"${budget_total:.2f}"},
        {"Category": "Used", "Amount": f"${budget_used:.2f}"},
        {"Category": "Remaining", "Amount": f"${budget_remaining:.2f}"}
    ]
    
    st.table(pd.DataFrame(budget_data))

# Tab 3: Using Expiring Items
with tab3:
    st.subheader("Recipes Using Soon-to-Expire Items")
    
    # Find expiring items
    today = datetime.now().date()
    expiring_items = []
    
    for item in inventory:
        if item.get("expiration_date"):
            try:
                exp_date = datetime.strptime(item["expiration_date"], '%Y-%m-%d').date()
                days_left = (exp_date - today).days
                
                if 0 <= days_left <= 3:
                    expiring_items.append({
                        "ingredient_id": item["ingredient_id"],
                        "name": item["name"],
                        "days_left": days_left
                    })
            except:
                pass
    
    # Display expiring items table
    if expiring_items:
        expiring_data = []
        for item in expiring_items:
            expiring_data.append({
                "Ingredient": item["name"],
                "Days Until Expiration": item["days_left"]
            })
        
        st.subheader("Expiring Ingredients")
        st.table(pd.DataFrame(expiring_data))
        
        # Find recipes using expiring items
        expiring_ids = [item["ingredient_id"] for item in expiring_items]
        recipes_using_expiring = []
        
        for recipe in recipes:
            if any(ing_id in expiring_ids for ing_id in recipe["ingredients"]):
                # Find which expiring ingredients are used
                used_ingredients = []
                for ing_id in recipe["ingredients"]:
                    if ing_id in expiring_ids:
                        for item in expiring_items:
                            if item["ingredient_id"] == ing_id:
                                used_ingredients.append(item["name"])
                
                recipes_using_expiring.append({
                    "Name": recipe["name"],
                    "Prep Time": f"{recipe['prep_time']} mins",
                    "Cost": f"${recipe['cost']:.2f}",
                    "Uses Expiring": ", ".join(used_ingredients),
                    "Instructions": recipe["instructions"]
                })
        
        # Display recipes using expiring items
        if recipes_using_expiring:
            st.subheader("Recipes Using Expiring Ingredients")
            st.table(pd.DataFrame(recipes_using_expiring))
        else:
            st.info("No recipes found using your expiring ingredients")
    else:
        st.success("No items expiring soon. Your fridge is in good shape!")
import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

# Authentication check
if not st.session_state.get('authenticated', False) or st.session_state.role != "nutritionist":
    st.warning("Please log in as Nancy to access this page")
    st.stop()

SideBarLinks(st.session_state.role)

# Define API endpoints
API_BASE_URL = "http://web-api:4000"
USERS_ENDPOINT = f"{API_BASE_URL}/users"
MEAL_PLANS_ENDPOINT = f"{API_BASE_URL}/meal_plans"
INGREDIENTS_ENDPOINT = f"{API_BASE_URL}/ingredients"
MACROS_ENDPOINT = f"{API_BASE_URL}/macros"
CONSTRAINTS_ENDPOINT = f"{API_BASE_URL}/users/constraints"

# Page header
st.title("Meal Planning")
st.write("Create and manage personalized meal plans for your clients")

# Function to get all users
def get_all_users():
    try:
        response = requests.get(USERS_ENDPOINT)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching users: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"API connection error: {str(e)}")
        return []

# Function to get user constraints
def get_user_constraints(pc_id):
    try:
        response = requests.get(f"{CONSTRAINTS_ENDPOINT}/{pc_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching constraints: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"API connection error: {str(e)}")
        return None

# Function to get all meal plans
def get_meal_plans(client_id=None):
    try:
        endpoint = MEAL_PLANS_ENDPOINT
        if client_id:
            endpoint += f"?client_id={client_id}"
        response = requests.get(endpoint)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching meal plans: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"API connection error: {str(e)}")
        return []

# Function to get ingredients
def get_ingredients():
    try:
        response = requests.get(INGREDIENTS_ENDPOINT)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching ingredients: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"API connection error: {str(e)}")
        return []

# Function to get ingredient details with macronutrients
def get_ingredient_details(ingredient_id):
    try:
        response = requests.get(f"{INGREDIENTS_ENDPOINT}/{ingredient_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching ingredient: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"API connection error: {str(e)}")
        return None

# Function to create a new meal plan
def create_meal_plan(data):
    try:
        response = requests.post(MEAL_PLANS_ENDPOINT, json=data)
        if response.status_code == 201:
            return response.json(), True
        else:
            st.error(f"Error creating meal plan: {response.status_code}")
            return None, False
    except Exception as e:
        st.error(f"API connection error: {str(e)}")
        return None, False

# Get users from API
users = get_all_users()

# Create tabs for different functions
tab1, tab2, tab3 = st.tabs(["Current Meal Plans", "Create New Plan", "Ingredients"])

# Current Meal Plans Tab
with tab1:
    st.header("Current Meal Plans")
    
    # Filter dropdown
    client_filter = st.selectbox(
        "Filter by client:",
        ["All Clients"] + [f"{user.get('f_name', '')} {user.get('l_name', '')}" for user in users]
    )
    
    # Get all meal plans
    meal_plans = get_meal_plans()
    
    # Apply client filter
    if client_filter != "All Clients":
        # Find client ID based on name
        client_id = None
        for user in users:
            full_name = f"{user.get('f_name', '')} {user.get('l_name', '')}"
            if full_name == client_filter:
                client_id = user.get('user_id')
                break
        
        if client_id:
            # Try to get client's constraints to find pc_id
            filtered_plans = [plan for plan in meal_plans if plan.get("pc_id") == client_id]
        else:
            filtered_plans = []
    else:
        filtered_plans = meal_plans
    
    # Display plans in a table
    if filtered_plans:
        # Create a DataFrame for display
        plans_df = pd.DataFrame({
            "ID": [plan.get("meal_id") for plan in filtered_plans],
            "Personal Constraints ID": [plan.get("pc_id") for plan in filtered_plans],
            "Recipe ID": [plan.get("recipe_id") for plan in filtered_plans],
            "Recipe": [plan.get("recipe_name", "Unknown Recipe") for plan in filtered_plans],
            "Servings": [plan.get("quantity", 1) for plan in filtered_plans]
        })
        
        st.table(plans_df)
    else:
        st.info(f"No meal plans found for {client_filter if client_filter != 'All Clients' else 'any client'}.")
    
    # View details option
    if filtered_plans:
        st.subheader("View Plan Details")
        plan_id = st.selectbox(
            "Select a plan to view details:",
            options=[plan.get("meal_id") for plan in filtered_plans],
            format_func=lambda x: next((f"{plan.get('recipe_name', 'Unknown Recipe')}" for plan in filtered_plans if plan.get("meal_id") == x), "")
        )
        
        if st.button("View Details"):
            # Find selected plan
            selected_plan = next((plan for plan in filtered_plans if plan.get("meal_id") == plan_id), None)
            if selected_plan:
                st.success(f"Details for meal plan {plan_id}")
                
                # Display recipe details in a table
                details = {
                    "Detail": ["Meal ID", "Personal Constraints ID", "Recipe ID", "Recipe Name", "Servings", "Instructions"],
                    "Value": [
                        selected_plan.get("meal_id", "N/A"),
                        selected_plan.get("pc_id", "N/A"),
                        selected_plan.get("recipe_id", "N/A"),
                        selected_plan.get("recipe_name", "N/A"),
                        selected_plan.get("quantity", 1),
                        selected_plan.get("instructions", "No instructions available.")
                    ]
                }
                
                details_df = pd.DataFrame(details)
                st.table(details_df)

# Create New Plan Tab
with tab2:
    st.header("Create New Meal Plan")
    
    # Client selection
    client_names = [f"{user.get('f_name', '')} {user.get('l_name', '')}" for user in users]
    if client_names:
        client_name = st.selectbox(
            "Select client:",
            client_names
        )
        
        # Find selected user and their personal constraints ID
        selected_user = None
        for user in users:
            full_name = f"{user.get('f_name', '')} {user.get('l_name', '')}"
            if full_name == client_name:
                selected_user = user
                break
        
        if selected_user:
            # Get user's personal constraints
            pc_id = selected_user.get("pc_id")
            constraints = None
            if pc_id:
                constraints = get_user_constraints(pc_id)
            
            # Get all ingredients for recipes
            ingredients = get_ingredients()
            
            if ingredients:
                # Recipe creation
                st.subheader("Create Recipe")
                
                recipe_name = st.text_input("Recipe name:")
                
                # Select ingredients for recipe
                ingredient_options = [ingredient.get("name", f"Ingredient {ingredient.get('ingredient_id')}") for ingredient in ingredients]
                selected_ingredient_names = st.multiselect("Select ingredients:", ingredient_options)
                
                # Find ingredient IDs for selected names
                selected_ingredients = []
                for ing_name in selected_ingredient_names:
                    ing = next((i for i in ingredients if i.get("name") == ing_name), None)
                    if ing:
                        selected_ingredients.append(ing)
                
                # Instructions
                instructions = st.text_area("Recipe instructions:")
                
                # Servings
                servings = st.number_input("Number of servings:", min_value=1, max_value=10, value=1, step=1)
                
                # Analyze selected ingredients if any
                if selected_ingredients:
                    st.subheader("Recipe Nutritional Analysis")
                    
                    # Try to get macronutrient information for each ingredient
                    nutrition_data = []
                    for ingredient in selected_ingredients:
                        # Get ingredient details with macros
                        details = get_ingredient_details(ingredient.get("ingredient_id"))
                        
                        if details and "macronutrients" in details:
                            macros = details.get("macronutrients", {})
                            nutrition_data.append({
                                "Ingredient": ingredient.get("name", f"Ingredient {ingredient.get('ingredient_id')}"),
                                "Protein (g)": macros.get("protein", 0),
                                "Carbs (g)": macros.get("carbs", 0),
                                "Fat (g)": macros.get("fat", 0),
                                "Calories": macros.get("calories", 0)
                            })
                        else:
                            # If no macros available, add with zeros
                            nutrition_data.append({
                                "Ingredient": ingredient.get("name", f"Ingredient {ingredient.get('ingredient_id')}"),
                                "Protein (g)": 0,
                                "Carbs (g)": 0,
                                "Fat (g)": 0,
                                "Calories": 0
                            })
                    
                    # Display ingredients nutritional info
                    nutrition_df = pd.DataFrame(nutrition_data)
                    st.table(nutrition_df)
                    
                    # Total nutrition for recipe
                    total_protein = sum(item.get("Protein (g)", 0) for item in nutrition_data)
                    total_carbs = sum(item.get("Carbs (g)", 0) for item in nutrition_data)
                    total_fat = sum(item.get("Fat (g)", 0) for item in nutrition_data)
                    total_calories = sum(item.get("Calories", 0) for item in nutrition_data)
                    
                    st.subheader("Total Recipe Nutrition (per serving)")
                    recipe_nutrition = {
                        "Nutrient": ["Protein", "Carbs", "Fat", "Calories"],
                        "Amount": [
                            f"{total_protein/servings:.1f} g",
                            f"{total_carbs/servings:.1f} g",
                            f"{total_fat/servings:.1f} g",
                            f"{total_calories/servings:.1f} kcal"
                        ]
                    }
                    
                    st.table(pd.DataFrame(recipe_nutrition))
                
                # Display dietary restrictions if available
                if constraints:
                    st.subheader("Client Dietary Information")
                    st.info(f"Diet type: {constraints.get('personal_diet', 'Not specified')}")
                    st.info(f"Restrictions: {constraints.get('dietary_restrictions', 'None')}")
                    
                    # Check if any ingredients conflict with restrictions
                    if constraints.get('dietary_restrictions'):
                        restrictions = constraints.get('dietary_restrictions').lower().split(',')
                        for ingredient in selected_ingredients:
                            ing_name = ingredient.get("name", "").lower()
                            for restriction in restrictions:
                                if restriction.strip() in ing_name:
                                    st.warning(f"⚠️ Warning: {ingredient.get('name')} may conflict with {client_name}'s dietary restrictions.")
                
                # Create meal plan button
                if st.button("Create Meal Plan") and recipe_name and selected_ingredients:
                    # In a real app, this would first create a recipe and then a meal plan
                    # Here we'll simulate it with the data we have
                    
                    # Prepare data for creating meal plan
                    meal_plan_data = {
                        "pc_id": pc_id,
                        "recipe_id": selected_ingredients[0].get("ingredient_id"),  # Using first ingredient as mock recipe ID
                        "quantity": servings
                    }
                    
                    # Make API call to create meal plan
                    result, success = create_meal_plan(meal_plan_data)
                    
                    if success:
                        st.success(f"Meal plan created successfully for {client_name}!")
                        meal_id = result.get("meal_id")
                        st.info(f"Meal plan ID: {meal_id}")
                    else:
                        st.error("Failed to create meal plan. Please check API connection.")
            else:
                st.warning("No ingredients found. Please check your API connection.")
        else:
            st.error("Selected client not found.")
    else:
        st.warning("No clients found. Please check your API connection.")

# Ingredients Tab
with tab3:
    st.header("Ingredient Database")
    
    # Get all ingredients
    ingredients = get_ingredients()
    
    # Simple search for ingredients
    search = st.text_input("Search ingredients:", placeholder="Enter ingredient name...")
    
    # Filter based on search
    if search and ingredients:
        filtered_ingredients = [i for i in ingredients if search.lower() in i.get("name", "").lower()]
    else:
        filtered_ingredients = ingredients
    
    # Display ingredients
    if filtered_ingredients:
        # Create DataFrame for display
        ingredients_df = pd.DataFrame({
            "ID": [i.get("ingredient_id") for i in filtered_ingredients],
            "Name": [i.get("name") for i in filtered_ingredients],
            "Expiration Date": [i.get("expiration_date") for i in filtered_ingredients]
        })
        
        st.table(ingredients_df)
        
        # View ingredient details
        st.subheader("View Ingredient Details")
        ingredient_id = st.selectbox(
            "Select ingredient to view details:",
            options=[i.get("ingredient_id") for i in filtered_ingredients],
            format_func=lambda x: next((i.get("name", f"Ingredient {x}") for i in filtered_ingredients if i.get("ingredient_id") == x), "")
        )
        
        if st.button("View Details"):
            selected_ingredient = get_ingredient_details(ingredient_id)
            
            if selected_ingredient:
                st.success(f"Details for {selected_ingredient.get('ingredient', {}).get('name', 'Ingredient')}")
                
                # Display ingredient information
                ingredient_data = selected_ingredient.get('ingredient', {})
                macros_data = selected_ingredient.get('macronutrients', {})
                
                # Basic info
                st.subheader("Basic Information")
                basic_info = {
                    "Property": ["ID", "Name", "Expiration Date"],
                    "Value": [
                        ingredient_data.get("ingredient_id", "N/A"),
                        ingredient_data.get("name", "N/A"),
                        ingredient_data.get("expiration_date", "N/A")
                    ]
                }
                
                st.table(pd.DataFrame(basic_info))
                
                # Macronutrient info if available
                if macros_data:
                    st.subheader("Macronutrients")
                    macros_info = {
                        "Nutrient": ["Protein", "Carbs", "Fat", "Fiber", "Sodium", "Calories"],
                        "Value": [
                            f"{macros_data.get('protein', 0)} g",
                            f"{macros_data.get('carbs', 0)} g",
                            f"{macros_data.get('fat', 0)} g",
                            f"{macros_data.get('fiber', 0)} g",
                            f"{macros_data.get('sodium', 0)} mg",
                            f"{macros_data.get('calories', 0)} kcal"
                        ]
                    }
                    
                    st.table(pd.DataFrame(macros_info))
                else:
                    st.info("No macronutrient data available for this ingredient.")
    else:
        st.info("No ingredients found. Please check your API connection or adjust your search.")
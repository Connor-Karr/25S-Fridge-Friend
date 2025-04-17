import streamlit as st
import pandas as pd
from modules.nav import SideBarLinks

if not st.session_state.get('authenticated', False) or st.session_state.role != "nutritionist":
    st.warning("Please log in as Nancy to access this page")
    st.stop()

SideBarLinks(st.session_state.role)

# Page header
st.title("Meal Planning")
st.write("Create and manage personalized meal plans for your clients")

# Mock client data
clients = [
    {"id": 1, "name": "John D.", "goal": "Weight Loss", "diet": "Low Carb", "allergies": "Peanuts"},
    {"id": 2, "name": "Sarah M.", "goal": "Muscle Gain", "diet": "High Protein", "allergies": "Dairy"},
    {"id": 3, "name": "Michael R.", "goal": "Maintenance", "diet": "Balanced", "allergies": "None"},
    {"id": 4, "name": "Emma L.", "goal": "Performance", "diet": "Keto", "allergies": "Gluten"},
    {"id": 5, "name": "David W.", "goal": "Health", "diet": "Mediterranean", "allergies": "Shellfish"}
]

# Mock recipe data
recipes = [
    {"id": 1, "name": "Grilled Chicken Salad", "calories": 350, "protein": 32, "carbs": 12, "fat": 18, "tags": "low-carb, high-protein, gluten-free"},
    {"id": 2, "name": "Salmon with Quinoa", "calories": 420, "protein": 28, "carbs": 35, "fat": 15, "tags": "balanced, omega-3, gluten-free"},
    {"id": 3, "name": "Vegetable Stir Fry", "calories": 280, "protein": 15, "carbs": 42, "fat": 8, "tags": "vegan, low-fat, gluten-free"},
    {"id": 4, "name": "Greek Yogurt Parfait", "calories": 230, "protein": 18, "carbs": 25, "fat": 7, "tags": "breakfast, high-protein, vegetarian"},
    {"id": 5, "name": "Spinach and Feta Omelette", "calories": 320, "protein": 22, "carbs": 8, "fat": 22, "tags": "low-carb, keto, vegetarian"},
    {"id": 6, "name": "Beef and Vegetable Stew", "calories": 380, "protein": 25, "carbs": 30, "fat": 16, "tags": "high-protein, balanced, meal-prep"},
    {"id": 7, "name": "Mediterranean Salad", "calories": 310, "protein": 14, "carbs": 20, "fat": 19, "tags": "mediterranean, low-carb, vegetarian"},
    {"id": 8, "name": "Protein Smoothie", "calories": 290, "protein": 30, "carbs": 28, "fat": 5, "tags": "breakfast, high-protein, quick"}
]

# Convert to DataFrames for easy display
clients_df = pd.DataFrame(clients)
recipes_df = pd.DataFrame(recipes)

# Create tabs for different functions
tab1, tab2, tab3 = st.tabs(["Current Meal Plans", "Create New Plan", "Recipe Database"])

# Current Meal Plans Tab
with tab1:
    st.header("Current Meal Plans")
    
    # Mock meal plans
    meal_plans = [
        {"meal_id": 1, "client_id": 1, "client_name": "John D.", "recipe_id": 1, "recipe_name": "Grilled Chicken Salad", "quantity": 1},
        {"meal_id": 2, "client_id": 1, "client_name": "John D.", "recipe_id": 4, "recipe_name": "Greek Yogurt Parfait", "quantity": 1},
        {"meal_id": 3, "client_id": 2, "client_name": "Sarah M.", "recipe_id": 2, "recipe_name": "Salmon with Quinoa", "quantity": 1},
        {"meal_id": 4, "client_id": 2, "client_name": "Sarah M.", "recipe_id": 6, "recipe_name": "Beef and Vegetable Stew", "quantity": 1},
        {"meal_id": 5, "client_id": 3, "client_name": "Michael R.", "recipe_id": 3, "recipe_name": "Vegetable Stir Fry", "quantity": 1},
        {"meal_id": 6, "client_id": 4, "client_name": "Emma L.", "recipe_id": 5, "recipe_name": "Spinach and Feta Omelette", "quantity": 1},
        {"meal_id": 7, "client_id": 5, "client_name": "David W.", "recipe_id": 7, "recipe_name": "Mediterranean Salad", "quantity": 1}
    ]
    
    # Create DataFrame for display
    meal_plans_df = pd.DataFrame(meal_plans)
    
    # Filter options
    selected_client = st.selectbox(
        "Filter by client:",
        ["All Clients"] + [client["name"] for client in clients]
    )
    
    if selected_client != "All Clients":
        filtered_plans = meal_plans_df[meal_plans_df["client_name"] == selected_client]
    else:
        filtered_plans = meal_plans_df
    
    # Display meal plans table
    if not filtered_plans.empty:
        st.subheader(f"Showing {len(filtered_plans)} meal plans")
        
        # Simplify the dataframe for display
        display_df = filtered_plans[["client_name", "recipe_name", "quantity"]]
        display_df.columns = ["Client", "Recipe", "Servings"]
        
        # Show as a table
        st.table(display_df)
        
        # Simple edit option
        st.subheader("Edit Meal Plan")
        meal_id = st.number_input("Enter Meal ID to edit:", min_value=1, max_value=max(meal_plans_df["meal_id"]), step=1)
        new_quantity = st.number_input("New quantity:", min_value=1, max_value=10, value=1)
        
        if st.button("Update Meal Plan"):
            st.success(f"Meal plan {meal_id} updated to {new_quantity} servings!")
    else:
        st.info("No meal plans found. Create a new meal plan in the 'Create New Plan' tab.")

# Create New Plan Tab
with tab2:
    st.header("Create New Meal Plan")
    
    # Client selection
    selected_client_name = st.selectbox("Select client:", [client["name"] for client in clients])
    selected_client = next(client for client in clients if client["name"] == selected_client_name)
    
    # Recipe selection
    selected_recipe_name = st.selectbox("Select recipe:", [recipe["name"] for recipe in recipes])
    selected_recipe = next(recipe for recipe in recipes if recipe["name"] == selected_recipe_name)
    
    # Show recipe details
    st.subheader("Recipe Details")
    recipe_details = {
        "Detail": ["Calories", "Protein", "Carbs", "Fat", "Tags"],
        "Value": [
            f"{selected_recipe['calories']} kcal",
            f"{selected_recipe['protein']}g",
            f"{selected_recipe['carbs']}g",
            f"{selected_recipe['fat']}g",
            selected_recipe['tags']
        ]
    }
    
    recipe_df = pd.DataFrame(recipe_details)
    st.table(recipe_df)
    
    # Simple allergy check
    if selected_client["allergies"] != "None":
        allergies = [a.strip().lower() for a in selected_client["allergies"].split(",")]
        tags = [t.strip().lower() for t in selected_recipe["tags"].split(",")]
        
        for allergy in allergies:
            if any(allergy in tag for tag in tags):
                st.warning(f"⚠️ Warning: This recipe may contain {allergy}, which {selected_client_name} is allergic to.")
    
    # Servings and submit
    servings = st.number_input("Number of servings:", min_value=1, max_value=10, value=1)
    
    if st.button("Create Meal Plan", type="primary"):
        st.success(f"Meal plan created for {selected_client_name}!")
        
        # Display summary of created plan
        st.subheader("Created Meal Plan")
        summary_data = {
            "Detail": ["Client", "Recipe", "Servings", "Total Calories", "Total Protein", "Total Carbs", "Total Fat"],
            "Value": [
                selected_client_name,
                selected_recipe_name,
                servings,
                f"{selected_recipe['calories'] * servings} kcal",
                f"{selected_recipe['protein'] * servings}g",
                f"{selected_recipe['carbs'] * servings}g",
                f"{selected_recipe['fat'] * servings}g"
            ]
        }
        
        summary_df = pd.DataFrame(summary_data)
        st.table(summary_df)

# Recipe Database Tab
with tab3:
    st.header("Recipe Database")
    
    # Simple search and filter
    search_term = st.text_input("Search recipes:", placeholder="Enter recipe name...")
    
    diet_options = ["All", "low-carb", "high-protein", "balanced", "keto", "mediterranean", "vegan", "vegetarian"]
    diet_filter = st.selectbox("Filter by diet:", diet_options)
    
    # Filter recipes
    filtered_recipes = recipes_df.copy()
    if search_term:
        filtered_recipes = filtered_recipes[filtered_recipes["name"].str.contains(search_term, case=False)]
    
    if diet_filter != "All":
        filtered_recipes = filtered_recipes[filtered_recipes["tags"].str.contains(diet_filter, case=False)]
    
    # Show filtered recipes
    if not filtered_recipes.empty:
        st.subheader(f"Showing {len(filtered_recipes)} recipes")
        
        # Format for display
        display_recipes = filtered_recipes[["name", "calories", "protein", "carbs", "fat", "tags"]]
        display_recipes.columns = ["Recipe", "Calories", "Protein (g)", "Carbs (g)", "Fat (g)", "Tags"]
        
        st.table(display_recipes)
        
        # Option to add recipe to meal plan
        st.subheader("Add to Meal Plan")
        recipe_id = st.number_input("Enter Recipe ID to add:", min_value=1, max_value=max(recipes_df["id"]), step=1)
        client_name = st.selectbox("Select client for meal plan:", [client["name"] for client in clients])
        
        if st.button("Add to Meal Plan"):
            st.success(f"Added recipe to {client_name}'s meal plan!")
    else:
        st.info("No recipes found matching your criteria. Try adjusting your search or filter.")

# Nutrition Resources Section - Simple Table
st.header("Nutrition Resources")

resources = [
    {"title": "Diet-Specific Meal Planning Guide", "description": "Guidelines for creating meal plans for different diets (keto, vegan, paleo, etc.)"},
    {"title": "Allergen Substitution Chart", "description": "Reference for allergen-free substitutes in recipes"},
    {"title": "Nutrient Timing for Athletes", "description": "Optimal timing of nutrients for athletic performance"},
    {"title": "Meal Prep Templates", "description": "Printable templates for clients to track their meal preparations"}
]

# Convert to DataFrame
resources_df = pd.DataFrame(resources)
st.table(resources_df)
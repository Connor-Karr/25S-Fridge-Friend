import streamlit as st
import pandas as pd

# Basic page setup
st.title("🍽️ Athlete Meal Plans")
st.write("Optimize your nutrition with targeted meal plans for different training phases")

# Function to get meal plans (would connect to database in real app)
def get_meal_plans():
    # In a real app, you would fetch this from your database
    return [
        {"meal_id": 1, "recipe_id": 1, "recipe_name": "Pre-Run Oatmeal Bowl", "quantity": 1},
        {"meal_id": 2, "recipe_id": 2, "recipe_name": "Recovery Protein Smoothie", "quantity": 1},
        {"meal_id": 3, "recipe_id": 3, "recipe_name": "Salmon & Quinoa Dinner", "quantity": 1},
        {"meal_id": 4, "recipe_id": 4, "recipe_name": "Carb-Loading Pasta", "quantity": 2}
    ]

# Function to delete a meal plan (would connect to database in real app)
def delete_meal_plan(meal_id):
    # In a real app, you would call your API or database
    st.success(f"Meal plan {meal_id} deleted successfully!")
    return True

# Create a function to load recipes (would connect to database in real app)
def load_recipes():
    # In a real app, this would come from a database
    return {
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

# Load recipes
recipes = load_recipes()

# Initialize session state variables if they don't exist
if 'view_recipe' not in st.session_state:
    st.session_state.view_recipe = None

# Create tabs for different meal plan categories (keeping all four original tabs)
tab1, tab2, tab3, tab4 = st.tabs(["Current Plans", "Race Day", "Recovery", "Training Phases"])

# Tab 1: Current Plans
with tab1:
    st.subheader("Current Meal Plans")
    
    # Get existing meal plans
    meal_plans = get_meal_plans()
    
    # Group meals by phase
    phases = set(recipes[meal["recipe_id"]]["phase"] for meal in meal_plans)
    
    # Display meals by phase
    for phase in phases:
        st.write(f"### {phase} Meals")
        
        phase_meals = [meal for meal in meal_plans 
                      if recipes[meal["recipe_id"]]["phase"] == phase]
        
        for meal in phase_meals:
            recipe = recipes.get(meal["recipe_id"])
            
            # Create a simple expansion section for each meal
            with st.expander(f"{recipe['name']} - {recipe['calories']} calories"):
                st.write(f"**Description:** {recipe['description']}")
                st.write(f"**Nutrition:** Protein: {recipe['protein']}g | Carbs: {recipe['carbs']}g | Fat: {recipe['fat']}g")
                st.write(f"**Servings:** {meal['quantity']}")
                
                # Add buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"View Recipe", key=f"view_{meal['meal_id']}"):
                        st.session_state.view_recipe = meal['recipe_id']
                        st.rerun()
                
                with col2:
                    if st.button(f"Remove", key=f"remove_{meal['meal_id']}"):
                        delete_meal_plan(meal['meal_id'])
                        st.rerun()
    
    # Display recipe details if a recipe is selected
    if st.session_state.get('view_recipe'):
        recipe_id = st.session_state.view_recipe
        recipe = recipes.get(recipe_id)
        
        st.markdown("---")
        st.subheader(f"Recipe: {recipe['name']}")
        
        # Basic recipe details
        st.write(f"**Description:** {recipe['description']}")
        st.write(f"**Total Time:** 20 minutes")
        st.write(f"**Servings:** 1")
        
        st.write("**Nutrition (per serving):**")
        st.write(f"Calories: {recipe['calories']} | Protein: {recipe['protein']}g | Carbs: {recipe['carbs']}g | Fat: {recipe['fat']}g")
        
        # Sample ingredients and instructions that would come from a database
        st.write("**Ingredients:**")
        st.write("- Main ingredient 1")
        st.write("- Main ingredient 2")
        st.write("- Main ingredient 3")
        
        st.write("**Instructions:**")
        st.write("1. First preparation step")
        st.write("2. Second preparation step")
        st.write("3. Final preparation step")
        
        # Button to return to list
        if st.button("Back to Meal Plans"):
            st.session_state.view_recipe = None
            st.rerun()

# Tab 2: Race Day
with tab2:
    st.subheader("Race Day Nutrition")
    st.write("Specialized meal plans for before, during, and after races")
    
    # Simple race day timeline
    st.write("### Race Day Timeline")
    st.write("**Before Race:**")
    st.write("- **Night Before:** Carb-loading dinner")
    st.write("- **3 Hours Before:** Pre-race breakfast")
    st.write("- **30 Minutes Before:** Final fuel")
    
    st.write("**During Race:**")
    st.write("- Hydration and energy as needed")
    
    st.write("**After Race:**")
    st.write("- **Immediately:** Initial recovery nutrition")
    st.write("- **Within 2 Hours:** Complete recovery meal")
    
    # Simple race day calculator
    st.markdown("---")
    st.subheader("Race Day Carbs Calculator")
    
    weight = st.number_input("Weight (lbs):", value=150)
    race_distance = st.selectbox("Race Distance:", ["5K", "10K", "Half Marathon", "Marathon"])
    
    if st.button("Calculate Carb Needs"):
        # Convert weight to kg
        weight_kg = weight * 0.453592
        
        # Simple calculation based on race distance
        carb_multiplier = {
            "5K": 1.0,
            "10K": 1.5,
            "Half Marathon": 2.0,
            "Marathon": 3.0
        }
        
        carb_needs = weight_kg * carb_multiplier[race_distance]
        st.success(f"Pre-Race Carbohydrate Target: **{carb_needs:.0f} grams**")
        st.write(f"Consume {carb_needs:.0f}g of carbs 3-4 hours before your race.")

# Tab 3: Recovery
with tab3:
    st.subheader("Recovery Nutrition")
    st.write("Optimize your recovery with targeted nutrition strategies")
    
    # Simple recovery calculator
    st.subheader("Recovery Calculator")
    
    workout_type = st.selectbox("Workout Type:", ["Easy Run", "Tempo Run", "Long Run", "Interval Training", "Race"])
    duration = st.number_input("Duration (minutes):", value=60)
    weight = st.number_input("Weight (lbs):", value=150, key="recovery_weight")
    
    if st.button("Calculate Recovery Needs"):
        # Convert weight to kg
        weight_kg = weight * 0.453592
        
        # Simple calculation for recovery needs
        carb_needs = weight_kg * 0.5
        protein_needs = weight_kg * 0.2
        
        st.success("Recovery Nutrition Plan")
        st.write(f"**Carbohydrate Target:** {carb_needs:.0f}g")
        st.write(f"**Protein Target:** {protein_needs:.0f}g")
        
        # Simple recovery recommendations
        st.write("**Recovery Timeline:**")
        st.write("- 0-30 minutes: Consume a recovery drink or smoothie")
        st.write("- 1-2 hours: Eat a balanced meal with protein and carbs")
    
    # Simple recovery food suggestions
    st.markdown("---")
    st.subheader("Recovery Food Options")
    st.write("**Good options for recovery:**")
    st.write("1. Protein smoothie with banana and berries")
    st.write("2. Chocolate milk")
    st.write("3. Greek yogurt with fruit")
    st.write("4. Turkey sandwich")

# Tab 4: Training Phases
with tab4:
    st.subheader("Training Phase Nutrition")
    st.write("Adjust your nutrition strategy for different training phases")
    
    # Simple phase selector
    current_phase = st.radio(
        "Current Training Phase:",
        ["Base Building", "Build Phase", "Peaking", "Taper", "Race Week", "Recovery"]
    )
    
    # Define simple nutritional strategies for each phase
    phase_nutrition = {
        "Base Building": {
            "calories": "Maintenance",
            "carbs": "Moderate (5-6g/kg/day)",
            "protein": "Moderate (1.6g/kg/day)",
            "fat": "Moderate (1g/kg/day)",
            "emphasis": "Building good nutritional habits",
            "meals": ["Oatmeal with yogurt and berries", "Chicken with rice and vegetables"]
        },
        "Build Phase": {
            "calories": "Slight surplus",
            "carbs": "Moderate-high (6-8g/kg/day)",
            "protein": "High (1.8g/kg/day)",
            "fat": "Moderate (1g/kg/day)",
            "emphasis": "Fueling harder workouts",
            "meals": ["Protein pancakes with banana", "Turkey wrap with vegetables"]
        },
        "Peaking": {
            "calories": "Maintenance",
            "carbs": "High (8-10g/kg/day)",
            "protein": "High (1.8g/kg/day)", 
            "fat": "Low-moderate (0.8g/kg/day)",
            "emphasis": "Maximum glycogen storage",
            "meals": ["Oatmeal with honey", "Pasta with lean meat sauce"]
        },
        "Taper": {
            "calories": "Slightly reduced",
            "carbs": "Moderate-high (7-8g/kg/day)",
            "protein": "Moderate (1.6g/kg/day)",
            "fat": "Low-moderate (0.8g/kg/day)",
            "emphasis": "Maintaining glycogen while reducing volume",
            "meals": ["Greek yogurt with granola", "Fish with potatoes"]
        },
        "Race Week": {
            "calories": "Maintenance",
            "carbs": "High (8-12g/kg/day)",
            "protein": "Moderate (1.5g/kg/day)",
            "fat": "Low (0.5g/kg/day)",
            "emphasis": "Carb-loading, easy digestion",
            "meals": ["Toast with honey", "Plain pasta with light sauce"] 
        },
        "Recovery": {
            "calories": "Maintenance",
            "carbs": "Moderate (5-6g/kg/day)",
            "protein": "High (2.0g/kg/day)",
            "fat": "Moderate (1g/kg/day)",
            "emphasis": "Tissue repair, inflammation reduction",
            "meals": ["Protein smoothie with berries", "Salmon with vegetables"]
        }
    }
    
    # Display selected phase information
    if current_phase in phase_nutrition:
        phase_data = phase_nutrition[current_phase]
        
        st.subheader("Nutrition Strategy")
        st.write(f"**Calories:** {phase_data['calories']}")
        st.write(f"**Carbohydrates:** {phase_data['carbs']}")
        st.write(f"**Protein:** {phase_data['protein']}")
        st.write(f"**Fat:** {phase_data['fat']}")
        st.write(f"**Emphasis:** {phase_data['emphasis']}")
        
        st.subheader("Sample Meals")
        for meal in phase_data['meals']:
            st.write(f"- {meal}")
        
        # Simple button to create a meal plan
        if st.button("Create Meal Plan for This Phase"):
            st.success(f"Meal plan created for {current_phase}!")
            st.info("Your meal plan has been saved.")
    
    # Simple phase transition information
    st.markdown("---")
    st.subheader("Phase Transition Tips")
    
    st.write(f"When moving to {current_phase}, remember to:")
    
    transition_tips = {
        "Base Building": ["Focus on establishing good eating habits", "Balance your macronutrients"],
        "Build Phase": ["Increase carbs to fuel harder workouts", "Add more protein for recovery"],
        "Peaking": ["Maximize carbohydrate intake", "Focus on recovery between hard workouts"],
        "Taper": ["Maintain carb intake as training decreases", "Watch overall calories to avoid weight gain"],
        "Race Week": ["Implement carb-loading strategy", "Reduce fiber intake before race day"],
        "Recovery": ["Focus on anti-inflammatory foods", "Prioritize protein for tissue repair"]
    }
    
    for tip in transition_tips.get(current_phase, ["Adjust nutrition based on training needs"]):
        st.write(f"- {tip}")
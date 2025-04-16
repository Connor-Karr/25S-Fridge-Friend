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

# Check if viewing a recipe
        if st.session_state.get('view_recipe'):
            recipe_id = st.session_state.view_recipe
            recipe = recipes.get(recipe_id)
            
            if recipe:
                st.markdown("---")
                st.subheader(f"Recipe: {recipe['name']}")
                
                # Mock recipe details
                st.write(f"**Description:** {recipe['description']}")
                st.write(f"**Total Time:** 20 minutes")
                st.write(f"**Servings:** 1")
                
                st.write("**Nutrition (per serving):**")
                st.write(f"Calories: {recipe['calories']} | Protein: {recipe['protein']}g | Carbs: {recipe['carbs']}g | Fat: {recipe['fat']}g")
                
                st.write("**Ingredients:**")
                
                # Mock ingredients based on the recipe
                if recipe['name'] == "Pre-Run Oatmeal Bowl":
                    st.write("- 1 cup rolled oats")
                    st.write("- 1 ripe banana, sliced")
                    st.write("- 1 tbsp honey")
                    st.write("- 1 tbsp almond butter")
                    st.write("- 1 cup almond milk")
                    st.write("- Pinch of cinnamon")
                elif recipe['name'] == "Recovery Protein Smoothie":
                    st.write("- 1 scoop protein powder")
                    st.write("- 1 banana")
                    st.write("- 1 cup mixed berries")
                    st.write("- 1 cup almond milk")
                    st.write("- 1 tbsp honey")
                    st.write("- Ice cubes")
                elif recipe['name'] == "Salmon & Quinoa Dinner":
                    st.write("- 5 oz salmon fillet")
                    st.write("- 1/2 cup cooked quinoa")
                    st.write("- 1 cup roasted vegetables")
                    st.write("- 1 tbsp olive oil")
                    st.write("- Lemon and herbs to taste")
                elif recipe['name'] == "Carb-Loading Pasta":
                    st.write("- 2 cups pasta")
                    st.write("- 1/2 cup marinara sauce")
                    st.write("- 2 tbsp olive oil")
                    st.write("- 1/4 cup parmesan cheese")
                    st.write("- Fresh basil")
                
                st.write("**Instructions:**")
                
                # Mock instructions based on the recipe
                if recipe['name'] == "Pre-Run Oatmeal Bowl":
                    st.write("1. Cook oats with almond milk according to package directions")
                    st.write("2. Stir in honey and almond butter")
                    st.write("3. Top with sliced banana and cinnamon")
                    st.write("4. Eat 1-2 hours before your run")
                elif recipe['name'] == "Recovery Protein Smoothie":
                    st.write("1. Add all ingredients to a blender")
                    st.write("2. Blend until smooth")
                    st.write("3. Consume within 30 minutes after your workout")
                elif recipe['name'] == "Salmon & Quinoa Dinner":
                    st.write("1. Cook salmon fillet in the oven at 400°F for 12-15 minutes")
                    st.write("2. Prepare quinoa according to package directions")
                    st.write("3. Toss vegetables with olive oil and roast at 425°F for 20 minutes")
                    st.write("4. Plate quinoa, top with salmon and vegetables")
                    st.write("5. Season with lemon and herbs")
                elif recipe['name'] == "Carb-Loading Pasta":
                    st.write("1. Cook pasta according to package directions")
                    st.write("2. Heat marinara sauce in a pan")
                    st.write("3. Toss pasta with sauce and olive oil")
                    st.write("4. Top with parmesan and fresh basil")
                    st.write("5. Consume 12-24 hours before race day")
                
                # Button to return to list
                if st.button("Back to Meal Plans"):
                    if 'view_recipe' in st.session_state:
                        del st.session_state.view_recipe
                    st.rerun()
    else:
        st.info("No meal plans found. Add some meal plans for different training phases!")

# Race Day Tab
with tab2:
    st.subheader("Race Day Nutrition")
    st.write("Specialized meal plans for before, during, and after races")
    
    # Create race day timeline visualization
    timeline_data = [
        {"time": "-12 hours", "meal": "Carb-loading dinner", "description": "High-carb, moderate protein, low fat, low fiber"},
        {"time": "-3 hours", "meal": "Pre-race breakfast", "description": "Easy-to-digest carbs, low fiber, low fat"},
        {"time": "-30 minutes", "meal": "Final fuel", "description": "Simple carbs, electrolytes"},
        {"time": "During Race", "meal": "Race nutrition", "description": "Carbs, electrolytes, fluids"},
        {"time": "+0-30 minutes", "meal": "Immediate recovery", "description": "Quick carbs + protein, fluids"},
        {"time": "+1-2 hours", "meal": "Recovery meal", "description": "Balanced meal with protein, carbs, and antioxidants"}
    ]
    
    # Create a visual timeline
    for i, item in enumerate(timeline_data):
        with st.container(border=True):
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.subheader(item["time"])
            
            with col2:
                st.write(f"**{item['meal']}**")
                st.write(item["description"])
                
                # Add example button
                if st.button("See Examples", key=f"example_{i}"):
                    if item["time"] == "-12 hours":
                        st.info("**Examples:** Pasta with tomato sauce, bread, baked potato, rice bowl, pancakes with maple syrup")
                    elif item["time"] == "-3 hours":
                        st.info("**Examples:** Oatmeal with banana, toast with honey, sports drink, white rice with a small amount of protein")
                    elif item["time"] == "-30 minutes":
                        st.info("**Examples:** Sports gel, banana, energy chews, sports drink")
                    elif item["time"] == "During Race":
                        st.info("**Examples:** Sports gels (every 45-60 minutes), sports drink, energy chews")
                    elif item["time"] == "+0-30 minutes":
                        st.info("**Examples:** Recovery drink, chocolate milk, banana with protein shake")
                    elif item["time"] == "+1-2 hours":
                        st.info("**Examples:** Turkey or chicken sandwich, recovery smoothie, rice bowl with lean protein")
    
    # Race day carbs calculator
    st.markdown("---")
    st.subheader("Race Day Carbs Calculator")
    
    with st.form("carb_calculator"):
        col1, col2 = st.columns(2)
        
        with col1:
            weight = st.number_input("Weight (lbs):", min_value=80, max_value=300, value=150)
            race_duration = st.selectbox(
                "Race Duration:",
                ["5K (20-30 min)", "10K (40-60 min)", "Half Marathon (1:30-2:30)", "Marathon (3:00-5:00)"]
            )
        
        with col2:
            timing = st.radio(
                "Timing:",
                ["Night Before Race", "Race Morning", "During Race", "Post-Race Recovery"]
            )
        
        calculate_button = st.form_submit_button("Calculate Needs")
        
        if calculate_button:
            # Convert weight to kg
            weight_kg = weight * 0.453592
            
            # Calculate carb needs based on timing and race
            if timing == "Night Before Race":
                carb_factor = 8  # g/kg
                carb_needs = weight_kg * carb_factor
                st.success(f"Carbohydrate Target: **{carb_needs:.0f} grams**")
                st.write(f"Aim for {carb_needs:.0f}g of carbs with your dinner and evening snacks. Focus on easy-to-digest sources like pasta, rice, potatoes, and bread.")
            
            elif timing == "Race Morning":
                # Calculate based on race distance
                if "5K" in race_duration:
                    carb_factor = 1  # g/kg
                elif "10K" in race_duration:
                    carb_factor = 1.5  # g/kg
                elif "Half" in race_duration:
                    carb_factor = 2  # g/kg
                else:  # Marathon
                    carb_factor = 3  # g/kg
                
                carb_needs = weight_kg * carb_factor
                st.success(f"Pre-Race Carbohydrate Target: **{carb_needs:.0f} grams**")
                st.write(f"Consume {carb_needs:.0f}g of carbs 3-4 hours before your race. Choose low-fiber, low-fat options that are easy to digest.")
            
            elif timing == "During Race":
                # Calculate based on race distance
                if "5K" in race_duration:
                    carb_factor = 0  # No need for 5K
                    st.info("Carbohydrate supplementation is generally not necessary for a 5K race.")
                elif "10K" in race_duration:
                    carb_factor = 30  # g/hour
                    st.success(f"Carbohydrate Target: **30 grams/hour**")
                    st.write("For a 10K, a small amount of carbs from a sports drink or gel may help, especially in the latter half of the race.")
                elif "Half" in race_duration:
                    carb_factor = 60  # g/hour
                    st.success(f"Carbohydrate Target: **60 grams/hour**")
                    st.write("Aim for 60g of carbs per hour from sports drinks, gels, or chews. Start fueling early and maintain a consistent schedule.")
                else:  # Marathon
                    carb_factor = 90  # g/hour
                    st.success(f"Carbohydrate Target: **60-90 grams/hour**")
                    st.write("For a marathon, aim for 60-90g of carbs per hour. Use a mix of sports drinks, gels, and solid foods if your stomach allows.")
            
            else:  # Post-Race Recovery
                # Calculate based on weight
                carb_factor = 1  # g/kg
                protein_factor = 0.3  # g/kg
                
                carb_needs = weight_kg * carb_factor
                protein_needs = weight_kg * protein_factor
                
                st.success(f"Recovery Targets: **{carb_needs:.0f}g carbs and {protein_needs:.0f}g protein**")
                st.write(f"Within 30 minutes post-race, consume {carb_needs:.0f}g of carbs and {protein_needs:.0f}g of protein. Follow with a complete meal within 2 hours.")
    
    # Race day meal plan templates
    st.markdown("---")
    st.subheader("Race Day Meal Plan Templates")
    
    race_plans = [
        {
            "name": "5K/10K Race Plan", 
            "description": "Optimized for shorter, higher-intensity races",
            "meals": [
                {"time": "Night Before", "meal": "Pasta with tomato sauce, garlic bread, and a small side salad"},
                {"time": "3h Before", "meal": "Oatmeal with banana and honey, white toast with jam"},
                {"time": "During", "meal": "Sports drink only (5K) or sports drink + 1 gel at halfway mark (10K)"},
                {"time": "After", "meal": "Recovery shake, followed by sandwich and fruit in 1-2 hours"}
            ]
        },
        {
            "name": "Half Marathon Plan",
            "description": "Balanced fueling for sustained energy over 13.1 miles",
            "meals": [
                {"time": "Night Before", "meal": "Rice bowl with lean protein, cooked vegetables, and dinner roll"},
                {"time": "3h Before", "meal": "Bagel with honey, banana, and sports drink"},
                {"time": "During", "meal": "Sports drink + gels every 40-45 minutes (2-3 total)"},
                {"time": "After", "meal": "Recovery shake, followed by balanced meal with chicken, rice, and vegetables"}
            ]
        },
        {
            "name": "Marathon Plan",
            "description": "Comprehensive fueling for maximum endurance",
            "meals": [
                {"time": "2 Days Before", "meal": "Begin carb-loading with high-carb meals throughout the day"},
                {"time": "Night Before", "meal": "Large pasta dinner with bread, light protein, and minimal fat/fiber"},
                {"time": "3h Before", "meal": "Oatmeal with banana and honey, white bread with jam, sports drink"},
                {"time": "During", "meal": "Sports drink + gel every 30 minutes, salt tabs for hot weather"},
                {"time": "After", "meal": "Recovery shake immediately, light meal in 1-2 hours, feast the next day"}
            ]
        }
    ]
    
    # Create columns for race plans
    cols = st.columns(len(race_plans))
    
    for i, plan in enumerate(race_plans):
        with cols[i]:
            st.subheader(plan["name"])
            st.write(plan["description"])
            
            # Show meals as a list
            for meal in plan["meals"]:
                st.markdown(f"**{meal['time']}:** {meal['meal']}")
            
            # Add button to save plan
            if st.button("Use This Template", key=f"use_plan_{i}"):
                st.success(f"Race day template selected: {plan['name']}")
                st.info("This would create personalized meal plans based on the template in a real app.")

# Recovery Tab
with tab3:
    st.subheader("Recovery Nutrition")
    st.write("Optimize your recovery with targeted nutrition strategies")
    
    # Recovery nutrition calculator
    st.write("### Recovery Nutrition Calculator")
    
    with st.form("recovery_calculator"):
        col1, col2 = st.columns(2)
        
        with col1:
            workout_type = st.selectbox(
                "Workout Type:",
                ["Easy Run", "Tempo Run", "Long Run", "Interval Training", "Race", "Cross-Training"]
            )
            
            duration = st.slider("Duration (minutes):", min_value=15, max_value=240, value=60)
        
        with col2:
            intensity = st.select_slider("Intensity:", options=["Low", "Moderate", "High", "Very High"])
            
            weight = st.number_input("Weight (lbs):", min_value=80, max_value=300, value=150)
        
        calculate_button = st.form_submit_button("Calculate Recovery Needs")
        
        if calculate_button:
            # Convert weight to kg
            weight_kg = weight * 0.453592
            
            # Calculate calorie burn (very simplified)
            intensity_factor = {
                "Low": 6,
                "Moderate": 8,
                "High": 10,
                "Very High": 12
            }
            
            calories_per_min_per_kg = intensity_factor[intensity]
            calories_burned = calories_per_min_per_kg * weight_kg * duration / 60
            
            # Calculate macros for recovery
            carb_factor = 0
            protein_factor = 0
            
            if intensity in ["High", "Very High"] or duration > 90:
                carb_factor = 1.0  # g/kg
                protein_factor = 0.3  # g/kg
            elif intensity == "Moderate" or duration > 60:
                carb_factor = 0.7  # g/kg
                protein_factor = 0.25  # g/kg
            else:
                carb_factor = 0.5  # g/kg
                protein_factor = 0.2  # g/kg
            
            carb_needs = weight_kg * carb_factor
            protein_needs = weight_kg * protein_factor
            
            # Display results
            st.markdown("### Recovery Nutrition Plan")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Calories Burned", f"{calories_burned:.0f} kcal")
            
            with col2:
                st.metric("Carbohydrate Target", f"{carb_needs:.0f}g")
            
            with col3:
                st.metric("Protein Target", f"{protein_needs:.0f}g")
            
            # Recovery timing recommendations
            st.subheader("Recovery Timeline")
            
            st.write("**0-30 minutes post-workout:**")
            st.write(f"- Consume {carb_needs:.0f}g carbs and {protein_needs:.0f}g protein")
            st.write("- Focus on fast-digesting options")
            st.write(f"- Drink 16-24 oz fluid per pound of weight lost")
            
            st.write("**1-2 hours post-workout:**")
            st.write("- Complete balanced meal with protein, carbs, and vegetables")
            st.write("- Continue hydrating")
            
            st.write("**Throughout day:**")
            st.write("- Ensure total daily protein intake of 1.6-2.0g/kg body weight")
            st.write(f"- Maintain at least {weight_kg * 6:.0f}g total daily carbs for glycogen replenishment")
            
            # Example recovery meals
            st.subheader("Example Recovery Options")
            
            if intensity in ["High", "Very High"] or duration > 90:
                st.info("**High-Intensity Recovery Options:**")
                st.write("1. Protein smoothie with banana, berries, and protein powder")
                st.write("2. Chocolate milk and a banana")
                st.write("3. Greek yogurt with honey and fruit")
                st.write("4. Turkey sandwich on white bread")
            else:
                st.info("**Moderate-Intensity Recovery Options:**")
                st.write("1. Greek yogurt with berries")
                st.write("2. Apple with nut butter")
                st.write("3. Tuna on whole grain crackers")
                st.write("4. Small protein shake")
    
    # Recovery nutrition science
    st.markdown("---")
    st.subheader("Recovery Nutrition Science")
    
    # Create tabs for different aspects of recovery
    recovery_tabs = st.tabs(["Timing", "Protein Quality", "Hydration", "Micronutrients"])
    
    with recovery_tabs[0]:
        st.write("### The Recovery Window")
        
        st.write("""
        The ideal window for post-workout nutrition:
        
        - **The 30-Minute Window**: Research shows enhanced glycogen synthesis when carbs are consumed 
          immediately after exercise.
          
        - **Extended Recovery**: While the 30-minute window is important, studies show recovery continues 
          for 24+ hours after hard workouts.
          
        - **Practical Approach**: Consume fast-digesting carbs and protein within 30 minutes, followed by a 
          complete meal within 2 hours.
        """)
        
        # Create timeline visualization
        timeline = pd.DataFrame({
            'Time': ['0 min', '30 min', '2 hours', '24 hours'],
            'Glycogen Synthesis Rate': [100, 80, 50, 30],
            'Protein Synthesis Rate': [90, 100, 80, 60]
        })
        
        fig = px.line(
            timeline, 
            x='Time', 
            y=['Glycogen Synthesis Rate', 'Protein Synthesis Rate'],
            title='Recovery Rates After Exercise',
            markers=True
        )
        
        fig.update_layout(height=350, yaxis_title='Relative Rate (%)')
        
        st.plotly_chart(fig, use_container_width=True)
    
    with recovery_tabs[1]:
        st.write("### Protein Quality for Recovery")
        
        # Protein quality data
        protein_data = pd.DataFrame({
            'Protein Source': ['Whey', 'Casein', 'Egg', 'Soy', 'Pea', 'Rice', 'Collagen'],
            'Leucine Content (g/25g protein)': [2.7, 2.3, 2.2, 1.8, 1.7, 1.4, 0.8],
            'Digestion Rate (relative)': [95, 65, 80, 75, 70, 65, 60],
            'PDCAAS Score (%)': [100, 100, 100, 91, 85, 65, 50]
        })
        
        # Create bar chart for leucine content
        fig = px.bar(
            protein_data,
            x='Protein Source',
            y='Leucine Content (g/25g protein)',
            title='Leucine Content by Protein Source (per 25g protein)',
            color='PDCAAS Score (%)',
            color_continuous_scale=px.colors.sequential.Viridis
        )
        
        fig.update_layout(height=350)
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("""
        **Why Protein Quality Matters:**
        
        1. **Leucine Content**: Leucine is the primary amino acid that triggers muscle protein synthesis.
        
        2. **Digestion Rate**: Fast-digesting proteins like whey are ideal post-workout, while slow-digesting 
           proteins like casein are better before bed.
        
        3. **Complete Amino Acid Profile**: PDCAAS score indicates how complete a protein's amino acid profile is 
           relative to human needs.
        
        **Recommendation**: For optimal recovery, use a fast-digesting, high-leucine protein source immediately 
        post-workout, followed by complete meals with mixed protein sources.
        """)
    
    with recovery_tabs[2]:
        st.write("### Hydration for Recovery")
        
        st.write("""
        Proper hydration is critical for recovery because:
        
        - **Nutrient Transport**: Fluids help transport nutrients to muscles
        - **Waste Removal**: Helps flush metabolic waste products
        - **Temperature Regulation**: Supports continued cooling after exercise
        - **Enzymatic Activity**: Optimal hydration improves recovery enzyme function
**Hydration Guidelines:**
        """)

# Hydration guidelines
        hydration_data = pd.DataFrame({
            'Sweat Loss': ['1 pound (16 oz)', '2 pounds (32 oz)', '3+ pounds (48+ oz)'],
            'Water Requirement': ['20-24 oz', '40-48 oz', '60-72+ oz'],
            'Electrolyte Need': ['Low', 'Medium', 'High']
        })
        
        st.dataframe(
            hydration_data,
            column_config={
                "Sweat Loss": st.column_config.TextColumn("Sweat Loss"),
                "Water Requirement": st.column_config.TextColumn("Water to Drink"),
                "Electrolyte Need": st.column_config.TextColumn("Electrolyte Need")
            },
            use_container_width=True
        )
        
        # Hydration calculator
        st.subheader("Quick Hydration Calculator")
        
        weight_before = st.number_input("Pre-workout weight (lbs):", min_value=80.0, max_value=300.0, value=150.0, step=0.1)
        weight_after = st.number_input("Post-workout weight (lbs):", min_value=80.0, max_value=300.0, value=148.5, step=0.1)
        fluid_consumed = st.number_input("Fluid consumed during workout (oz):", min_value=0.0, max_value=100.0, value=16.0, step=1.0)
        
        if st.button("Calculate Hydration Needs"):
            weight_loss = weight_before - weight_after
            actual_sweat_loss = weight_loss * 16 + fluid_consumed  # 16 oz per pound
            
            # Calculate recommended fluid intake
            fluid_to_consume = actual_sweat_loss * 1.5  # Replace 150% of losses
            
            st.success(f"You lost approximately {weight_loss:.1f} lbs ({actual_sweat_loss:.0f} oz) of sweat")
            st.info(f"**Recommendation:** Drink {fluid_to_consume:.0f} oz of fluid to fully rehydrate")
            
            # Electrolyte recommendations
            if actual_sweat_loss > 48:
                st.warning("Consider a high-electrolyte drink to replace lost minerals")
            elif actual_sweat_loss > 32:
                st.info("Include moderate electrolytes in your recovery drinks")
    
    with recovery_tabs[3]:
        st.write("### Recovery Micronutrients")
        
        st.write("""
        Beyond proteins and carbs, specific micronutrients play crucial roles in recovery:
        """)
        
        # Create micronutrient info
        micronutrient_data = [
            {
                "nutrient": "Vitamin D",
                "benefits": "Reduces inflammation, supports protein synthesis",
                "sources": "Fatty fish, egg yolks, sunlight exposure, fortified foods"
            },
            {
                "nutrient": "Magnesium",
                "benefits": "Reduces muscle soreness, supports energy production",
                "sources": "Dark leafy greens, nuts, seeds, whole grains"
            },
            {
                "nutrient": "Antioxidants (Vit C & E)",
                "benefits": "Combats oxidative stress, reduces inflammation",
                "sources": "Berries, citrus fruits, bell peppers, nuts, seeds"
            },
            {
                "nutrient": "Zinc",
                "benefits": "Supports immune function and protein synthesis",
                "sources": "Meat, shellfish, legumes, seeds"
            },
            {
                "nutrient": "Omega-3 Fatty Acids",
                "benefits": "Reduces inflammation, improves recovery rate",
                "sources": "Fatty fish, walnuts, flaxseeds, chia seeds"
            }
        ]
        
        # Display micronutrients in expandable sections
        for data in micronutrient_data:
            with st.expander(data["nutrient"]):
                st.write(f"**Benefits:** {data['benefits']}")
                st.write(f"**Food Sources:** {data['sources']}")
        
        # Anti-inflammatory foods
        st.subheader("Anti-inflammatory Recovery Foods")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Tart Cherries**")
            st.write("- Reduces muscle soreness")
            st.write("- Improves sleep quality")
            st.write("- Speeds recovery time")
        
        with col2:
            st.write("**Turmeric**")
            st.write("- Contains curcumin")
            st.write("- Powerful anti-inflammatory")
            st.write("- Reduces joint pain")
        
        with col3:
            st.write("**Fatty Fish**")
            st.write("- Rich in omega-3s")
            st.write("- Reduces inflammation")
            st.write("- Supports muscle repair")

# Training Phases Tab
with tab4:
    st.subheader("Training Phase Nutrition")
    st.write("Adjust your nutrition strategy for different training phases")
    
    # Create training phase selector
    current_phase = st.radio(
        "Current Training Phase:",
        ["Base Building", "Build Phase", "Peaking", "Taper", "Race Week", "Recovery"],
        horizontal=True
    )
    
    # Define nutritional strategies for each phase
    phase_nutrition = {
        "Base Building": {
            "calories": "Maintenance to slight surplus",
            "carbs": "Moderate (5-6g/kg/day)",
            "protein": "Moderate-high (1.6-1.8g/kg/day)",
            "fat": "Moderate (1g/kg/day)",
            "emphasis": "Building good nutritional habits, establishing baseline",
            "priority_nutrients": ["Protein", "Iron", "Calcium", "Vitamin D"],
            "sample_meals": [
                "Overnight oats with Greek yogurt and berries", 
                "Chicken and vegetable stir fry with brown rice",
                "Salmon with sweet potato and green vegetables"
            ]
        },
        "Build Phase": {
            "calories": "Maintenance to moderate surplus (+200-300 cals)",
            "carbs": "Moderate-high (6-8g/kg/day)",
            "protein": "High (1.8-2.0g/kg/day)",
            "fat": "Moderate (1g/kg/day)",
            "emphasis": "Fueling increasingly intense workouts, enhanced recovery",
            "priority_nutrients": ["Carbohydrates", "Protein", "Magnesium", "B Vitamins"],
            "sample_meals": [
                "Protein pancakes with banana and maple syrup",
                "Turkey wrap with hummus and vegetables", 
                "Beef and vegetable bowl with rice and avocado"
            ]
        },
        "Peaking": {
            "calories": "Maintenance to slight surplus",
            "carbs": "High (8-10g/kg/day)",
            "protein": "High (1.8-2.0g/kg/day)",
            "fat": "Low-moderate (0.8g/kg/day)",
            "emphasis": "Maximum glycogen storage, intense workout fueling",
            "priority_nutrients": ["Carbohydrates", "Sodium", "Potassium", "Antioxidants"],
            "sample_meals": [
                "Oatmeal with banana, honey, and protein powder",
                "Pasta with lean meat sauce and vegetables", 
                "Rice bowl with chicken, vegetables, and teriyaki sauce"
            ]
        },
        "Taper": {
            "calories": "Slightly reduced (-100-200 cals)",
            "carbs": "Moderate-high (7-8g/kg/day)",
            "protein": "Moderate (1.6-1.8g/kg/day)",
            "fat": "Low-moderate (0.8g/kg/day)",
            "emphasis": "Maintaining glycogen while reducing volume, avoiding weight gain",
            "priority_nutrients": ["Carbohydrates", "Protein", "Zinc", "Antioxidants"],
            "sample_meals": [
                "Greek yogurt with granola and fruit",
                "Quinoa salad with grilled chicken and vegetables", 
                "Fish with roasted potatoes and green beans"
            ]
        },
        "Race Week": {
            "calories": "Maintenance",
            "carbs": "High, increasing to very high (8-12g/kg/day)",
            "protein": "Moderate (1.5-1.6g/kg/day)",
            "fat": "Low (0.5-0.8g/kg/day)",
            "emphasis": "Carb-loading, reducing fiber, easy digestion",
            "priority_nutrients": ["Carbohydrates", "Sodium", "Magnesium", "Potassium"],
            "sample_meals": [
                "White toast with honey and banana",
                "Plain pasta with small amount of sauce", 
                "White rice with lean protein and minimal fiber"
            ]
        },
        "Recovery": {
            "calories": "Maintenance to slight deficit (-100-200 cals)",
            "carbs": "Moderate (5-6g/kg/day)",
            "protein": "High (1.8-2.0g/kg/day)",
            "fat": "Moderate (1g/kg/day)",
            "emphasis": "Tissue repair, inflammation reduction, immune support",
            "priority_nutrients": ["Protein", "Omega-3s", "Antioxidants", "Zinc"],
            "sample_meals": [
                "Protein smoothie with berries and spinach",
                "Salmon with quinoa and roasted vegetables", 
                "Chicken and vegetable soup with whole grain bread"
            ]
        }
    }
    
    # Display selected phase information
    if current_phase in phase_nutrition:
        phase_data = phase_nutrition[current_phase]
        
        # Create columns for data display
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Nutrition Strategy")
            
            # Create nutrition summary
            st.write(f"**Calories:** {phase_data['calories']}")
            st.write(f"**Carbohydrates:** {phase_data['carbs']}")
            st.write(f"**Protein:** {phase_data['protein']}")
            st.write(f"**Fat:** {phase_data['fat']}")
            st.write(f"**Emphasis:** {phase_data['emphasis']}")
            
            # Create nutrition visualization
            carb_pct = 60 if "high" in phase_data['carbs'].lower() else 50 if "moderate" in phase_data['carbs'].lower() else 40
            protein_pct = 30 if "high" in phase_data['protein'].lower() else 25 if "moderate" in phase_data['protein'].lower() else 20
            fat_pct = 100 - carb_pct - protein_pct
            
            # Create donut chart for macro ratio
            macro_data = pd.DataFrame({
                'Macronutrient': ['Carbs', 'Protein', 'Fat'],
                'Percentage': [carb_pct, protein_pct, fat_pct]
            })
            
            fig = px.pie(
                macro_data,
                values='Percentage',
                names='Macronutrient',
                title=f'{current_phase} Macro Ratio',
                color_discrete_sequence=px.colors.qualitative.Set2,
                hole=0.4
            )
            
            fig.update_layout(height=300)
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Key Recommendations")
            
            # Priority nutrients
            st.write("**Priority Nutrients:**")
            for nutrient in phase_data['priority_nutrients']:
                st.write(f"- {nutrient}")
            
            # Sample meals
            st.write("**Sample Meals:**")
            for meal in phase_data['sample_meals']:
                st.write(f"- {meal}")
            
            # Create a meal plan button
            if st.button("Create Meal Plan for This Phase"):
                with st.spinner("Creating personalized meal plan..."):
                    time.sleep(2)
                    st.success(f"Meal plan created for {current_phase}!")
                    
                    # Mock create a meal plan in the database
                    plan_data = {
                        "pc_id": 1,  # Mock personal constraints ID
                        "recipe_id": 1 if current_phase == "Base Building" else 2 if current_phase == "Recovery" else 3 if current_phase == "Build Phase" else 4,
                        "quantity": 1
                    }
                    
                    result, success = create_meal_plan(plan_data)
                    
                    if success:
                        st.success("Meal plan saved to your account!")
                    else:
                        # Mock success for demo
                        st.success("Meal plan saved to your account! (Mock)")
    
    # Phase transition guidelines
    st.markdown("---")
    st.subheader("Phase Transition Guidelines")
    
    st.write("""
    When transitioning between training phases, make these nutrition adjustments:
    """)
    
    # Create expandable sections for each transition
    with st.expander("Base → Build"):
        st.write("""
        - Gradually increase carbohydrate intake by 1-2g/kg/day
        - Add ~200 calories daily to support increased training load
        - Slightly increase protein intake to support muscle adaptation
        - Time carbs strategically around harder workouts
        """)
    
    with st.expander("Build → Peak"):
        st.write("""
        - Further increase carbohydrates by 1-2g/kg/day
        - Maintain protein at high levels (1.8-2.0g/kg/day)
        - Decrease fat intake slightly to accommodate more carbs
        - Prioritize recovery nutrition after intense sessions
        - Consider adding intra-workout carbs for longer sessions
        """)
    
    with st.expander("Peak → Taper"):
        st.write("""
        - Reduce calories slightly as training volume decreases
        - Maintain carbohydrate intake to ensure full glycogen stores
        - Slightly reduce protein intake (1.6-1.8g/kg/day)
        - Monitor body weight to avoid unwanted gains
        - Begin reducing fiber intake in final days before race
        """)
    
    with st.expander("Taper → Race"):
        st.write("""
        - Implement carb-loading protocol 1-3 days before race
        - Dramatically reduce fiber intake 24-48 hours pre-race
        - Maintain adequate hydration and electrolyte balance
        - Reduce fat and protein to accommodate higher carbs
        - Test race-day nutrition strategy during final workouts
        """)
    
    with st.expander("Race → Recovery"):
        st.write("""
        - Focus on rehydration and glycogen replenishment immediately post-race
        - Gradually return to normal eating patterns over 24-48 hours
        - Emphasize protein intake for tissue repair
        - Include anti-inflammatory foods (berries, fatty fish, turmeric)
        - Don't restrict calories too much; support recovery before resuming training
        """)
    
    # Personal phase tracking
    st.markdown("---")
    st.subheader("Personal Phase Tracking")
    
    # Create simple mock phase tracking visualization
    # Generate data for the past 6 months and next 2 months
    months = 8
    month_labels = [(datetime.now() - timedelta(days=30*(months-3-i))).strftime('%b') for i in range(months)]
    
    # Define phases for each month
    phases = ["Base Building", "Base Building", "Build Phase", "Build Phase", 
              "Peaking", "Taper", "Race Week", "Recovery"]
    
    # Create DataFrame
    phase_df = pd.DataFrame({
        'Month': month_labels,
        'Phase': phases,
        'Current': [i == 5 for i in range(months)]  # Mark current month
    })
    
    # Create figure
    fig = go.Figure()
    
    # Add bars for each phase with different colors
    colors = {
        "Base Building": "#91e5ff",
        "Build Phase": "#4cb5ff",
        "Peaking": "#1e88e5",
        "Taper": "#ff9800",
        "Race Week": "#f44336",
        "Recovery": "#4caf50"
    }
    
    # Add phase bars
    for phase in set(phases):
        mask = phase_df['Phase'] == phase
        fig.add_trace(go.Bar(
            x=phase_df[mask]['Month'],
            y=[1] * sum(mask),
            name=phase,
            marker_color=colors[phase],
            width=0.6
        ))
    
    # Add current month indicator
    current_month = phase_df[phase_df['Current']]['Month'].values[0]
    
    fig.add_shape(
        type="line",
        x0=current_month,
        y0=0,
        x1=current_month,
        y1=1,
        line=dict(color="Black", width=3)
    )
    
    fig.add_annotation(
        x=current_month,
        y=1.05,
        text="You are here",
        showarrow=False,
        font=dict(color="black", size=14)
    )
    
    # Update layout
    fig.update_layout(
        title="Training Phase Timeline",
        xaxis_title="Month",
        yaxis_visible=False,
        height=300,
        barmode='stack',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add button to update phase
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if st.button("Update Current Phase"):
            st.session_state.update_phase = True
    
    # Phase update form
    if st.session_state.get("update_phase", False):
        with st.form("update_phase_form"):
            st.subheader("Update Training Phase")
            
            new_phase = st.selectbox(
                "Select current training phase:",
                ["Base Building", "Build Phase", "Peaking", "Taper", "Race Week", "Recovery"]
            )
            
            next_race = st.date_input(
                "Next race date:",
                value=datetime.now().date() + timedelta(days=30)
            )
            
            submit = st.form_submit_button("Save Phase Update")
            
            if submit:
                st.success(f"Training phase updated to {new_phase}")
                st.info(f"Nutritional recommendations updated for {new_phase} phase")
                
                # Clear update state
                if "update_phase" in st.session_state:
                    del st.session_state.update_phase
                
                st.rerun()

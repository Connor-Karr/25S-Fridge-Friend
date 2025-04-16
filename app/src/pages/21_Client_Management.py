import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from modules.nav import SideBarLinks

if not st.session_state.get('authenticated', False) or st.session_state.role != "nutritionist":
    st.warning("Please log in as Nancy to access this page")
    st.stop()

SideBarLinks(st.session_state.role)

@st.cache_data(ttl=300)
def get_users():
    try:
        response = requests.get("http://web-api:4000/users")
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
        response = requests.get("http://web-api:4000/users/{user_id}")
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
        response = requests.put("http://web-api:4000/users/constraints/{pc_id}", json=data)
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
        response = requests.post("http://web-api:4000/users/constraints", json=data)
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
        # Allergy Management Tab
        with tab3:
            st.subheader("Allergy & Dietary Restriction Management")
            
            current_allergies = client['allergies']
            current_diet = client['diet']
            st.write(f"**Current Allergies/Intolerances:** {current_allergies}")
            st.write(f"**Current Diet Type:** {current_diet}")
            
            # Update restrictions form
            with st.form("edit_restrictions_form"):
                st.subheader("Update Dietary Restrictions")
                all_allergens = ["Dairy", "Eggs", "Peanuts", "Tree Nuts", "Shellfish", "Fish", "Soy", "Wheat", "Gluten"]
                current_allergen_list = [a.strip() for a in current_allergies.split(",")]
                selected_allergens = []
                for allergen in all_allergens:
                    if any(a.lower() == allergen.lower() for a in current_allergen_list):
                        selected_allergens.append(allergen)
                
                new_allergens = st.multiselect(
                    "Select Allergies/Intolerances:",
                    all_allergens,
                    default=selected_allergens
                )
                
                diet_types = ["Low Carb", "High Protein", "Balanced", "Keto", "Mediterranean", "Vegan", "Vegetarian"]
                new_diet = st.selectbox(
                    "Diet Type:",
                    diet_types,
                    index=diet_types.index(current_diet) if current_diet in diet_types else 0
                )
                
                special_instructions = st.text_area(
                    "Special Instructions:",
                    placeholder="Enter any additional dietary considerations or notes..."
                )
                
                submit_button = st.form_submit_button("Update Restrictions")
                
                if submit_button:
                    new_allergies_string = ", ".join(new_allergens) if new_allergens else "None"
                    st.success(f"Dietary restrictions updated successfully!")
                    st.write(f"New allergies: {new_allergies_string}")
                    st.write(f"New diet type: {new_diet}")
                    
                    client['allergies'] = new_allergies_string
                    client['diet'] = new_diet
                    
                    constraints_data = {
                        'dietary_restrictions': new_allergies_string.lower(),
                        'personal_diet': new_diet.lower().replace(' ', '-')
                    }
                    
                    pc_id = client['constraints']['pc_id']
                    time.sleep(1)
                    st.rerun()
            
            # Substitution chart
            st.markdown("---")
            st.subheader("Substitution Chart")
            allergen_substitutes = {
                "Dairy": ["Almond milk", "Coconut milk", "Cashew cheese", "Nutritional yeast"],
                "Eggs": ["Flax egg (1 tbsp ground flax + 3 tbsp water)", "Chia egg", "Applesauce", "Mashed banana"],
                "Gluten": ["Rice flour", "Almond flour", "Gluten-free oats", "Quinoa"],
                "Peanuts": ["Sunflower seed butter", "Almond butter", "Pumpkin seeds", "Cashews"],
                "Shellfish": ["White fish", "Tofu", "Tempeh", "Jackfruit"]
            }
            
            relevant_allergens = []
            for allergen in client['allergies'].split(','):
                allergen = allergen.strip().capitalize()
                if allergen in allergen_substitutes:
                    relevant_allergens.append(allergen)
            
            if relevant_allergens:
                substitute_data = []
                for allergen in relevant_allergens:
                    for substitute in allergen_substitutes.get(allergen, []):
                        substitute_data.append({"Allergen": allergen, "Substitute": substitute})
                if substitute_data:
                    substitute_df = pd.DataFrame(substitute_data)
                    st.dataframe(substitute_df, use_container_width=True)
            else:
                st.info("No specific allergens requiring substitution.")
            
            # Food label guide
            st.markdown("---")
            st.subheader("Food Label Guide")
            st.write("""
            Help your client look for these alternative names on food labels:
            
            **Dairy:** Casein, Whey, Lactose, Lactalbumin, Ghee
            
            **Eggs:** Albumin, Globulin, Ovoglobulin, Livetin, Vitellin
            
            **Gluten:** Wheat, Barley, Rye, Malt, Semolina, Farina
            
            **Peanuts:** Arachis oil, Beer nuts, Artificial nuts
            
            **Shellfish:** Scampi, Surimi, Crevette, Bouillabaisse
            """)
            
            if st.button("Download Complete Food Label Guide"):
                with st.spinner("Preparing download..."):
                    time.sleep(1)
                    st.download_button(
                        label="Download Guide",
                        data="This would be a complete guide to food labeling for allergens.",
                        file_name="allergen_food_label_guide.txt",
                        mime="text/plain"
                    )
        # Progress Tab
        with tab4:
            st.subheader("Client Progress")
            
            # Time period selection
            progress_period = st.selectbox(
                "View progress for:",
                ["Last 30 Days", "Last 3 Months", "Last 6 Months", "Last Year", "All Time"]
            )
            
            if progress_period == "Last 30 Days":
                days = 30
            elif progress_period == "Last 3 Months":
                days = 90
            elif progress_period == "Last 6 Months":
                days = 180
            elif progress_period == "Last Year":
                days = 365
            else:
                days = 365
            
            dates = [(datetime.now() - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(days)]
            dates.reverse()
            
            start_weight = float(client['weight'].split()[0])
            if client['goal'] == "Weight Loss":
                weekly_change = -np.random.uniform(0.8, 1.5)
            elif client['goal'] == "Muscle Gain":
                weekly_change = np.random.uniform(0.4, 0.8)
            else:
                weekly_change = np.random.uniform(-0.2, 0.2)
            
            daily_change = weekly_change / 7
            np.random.seed(42)
            weights = []
            current_weight = start_weight
            for i in range(days):
                fluctuation = np.random.normal(0, 0.5)
                current_weight += daily_change + fluctuation
                weights.append(max(current_weight, start_weight * 0.7))
            
            weight_data = pd.DataFrame({
                'Date': dates,
                'Weight (lbs)': weights
            })
            
            fig = px.line(
                weight_data,
                x='Date',
                y='Weight (lbs)',
                title=f'Weight Progress ({progress_period})',
                markers=True
            )
            
            if client['goal'] in ["Weight Loss", "Muscle Gain"]:
                goal_weight = start_weight * 0.85 if client['goal'] == "Weight Loss" else start_weight * 1.1
                fig.add_hline(
                    y=goal_weight,
                    line_dash="dash",
                    line_color="red",
                    annotation_text="Goal Weight",
                    annotation_position="bottom right"
                )
            
            fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig, use_container_width=True)
            
            if client['goal'] in ["Weight Loss", "Muscle Gain"]:
                st.subheader("Body Composition Changes")
                if client['goal'] == "Weight Loss":
                    initial_fat, final_fat = 28, 22
                    initial_muscle, final_muscle = 30, 33
                else:
                    initial_fat, final_fat = 18, 19
                    initial_muscle, final_muscle = 35, 42
                
                fat_daily_change = (final_fat - initial_fat) / days
                muscle_daily_change = (final_muscle - initial_muscle) / days
                
                fat_percentages, muscle_percentages = [], []
                current_fat, current_muscle = initial_fat, initial_muscle
                for i in range(days):
                    current_fat += fat_daily_change + np.random.normal(0, 0.2)
                    current_muscle += muscle_daily_change + np.random.normal(0, 0.1)
                    fat_percentages.append(current_fat)
                    muscle_percentages.append(current_muscle)
                
                composition_data = pd.DataFrame({
                    'Date': dates,
                    'Body Fat %': fat_percentages,
                    'Muscle %': muscle_percentages
                })
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=composition_data['Date'], y=composition_data['Body Fat %'],
                                         mode='lines', name='Body Fat %', line=dict(color='orange')))
                fig.add_trace(go.Scatter(x=composition_data['Date'], y=composition_data['Muscle %'],
                                         mode='lines', name='Muscle %', line=dict(color='blue')))
                fig.update_layout(
                    title='Body Composition Changes',
                    xaxis_title='Date',
                    yaxis_title='Percentage',
                    height=400,
                    margin=dict(l=20, r=20, t=40, b=20),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig, use_container_width=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Starting Metrics:**")
                    st.write(f"Weight: {start_weight} lbs")
                    st.write(f"Body Fat: {initial_fat:.1f}%")
                    st.write(f"Muscle Mass: {initial_muscle:.1f}%")
                with col2:
                    st.write("**Current Metrics:**")
                    st.write(f"Weight: {weights[-1]:.1f} lbs")
                    st.write(f"Body Fat: {fat_percentages[-1]:.1f}%")
                    st.write(f"Muscle Mass: {muscle_percentages[-1]:.1f}%")
                
                st.write("**Changes:**")
                weight_change = weights[-1] - start_weight
                fat_change = fat_percentages[-1] - initial_fat
                muscle_change = muscle_percentages[-1] - initial_muscle
                st.write(f"Weight: {'+' if weight_change > 0 else ''}{weight_change:.1f} lbs")
                st.write(f"Body Fat: {'+' if fat_change > 0 else ''}{fat_change:.1f}%")
                st.write(f"Muscle Mass: {'+' if muscle_change > 0 else ''}{muscle_change:.1f}%")
            
            st.subheader("Key Metrics")
            metric_tabs = st.tabs(["Adherence", "Nutrition", "Outcomes"])
            
            with metric_tabs[0]:
                adherence_data = {
                    "Meal Logging": 85,
                    "Following Meal Plan": 78,
                    "Meeting Protein Goals": 82,
                    "Staying Within Calorie Range": 75,
                    "Avoiding Restricted Foods": 95
                }
                adherence_df = pd.DataFrame({
                    'Metric': list(adherence_data.keys()),
                    'Adherence (%)': list(adherence_data.values())
                })
                fig = px.bar(
                    adherence_df,
                    y='Metric',
                    x='Adherence (%)',
                    orientation='h',
                    title='Client Adherence Metrics',
                    color='Adherence (%)',
                    color_continuous_scale=px.colors.sequential.Viridis,
                    range_x=[0, 100]
                )
                fig.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20),
                                  yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
            
            with metric_tabs[1]:
                np.random.seed(43)
                protein_compliance = np.clip(np.random.normal(85, 10, days), 0, 100)
                calorie_compliance = np.clip(np.random.normal(80, 15, days), 0, 100)
                carb_compliance = np.clip(np.random.normal(75, 20, days), 0, 100)
                nutrition_df = pd.DataFrame({
                    'Date': dates,
                    'Protein': protein_compliance,
                    'Calories': calorie_compliance,
                    'Carbs': carb_compliance
                })
                fig = px.line(
                    nutrition_df,
                    x='Date',
                    y=['Protein', 'Calories', 'Carbs'],
                    title='Daily Nutrition Target Compliance (%)',
                    labels={'value': 'Compliance (%)'}
                )
                fig.add_hline(y=80, line_dash="dash", line_color="green",
                              annotation_text="Target Compliance Level", annotation_position="bottom right")
                fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20),
                                  legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                                  yaxis_range=[0, 100])
                st.plotly_chart(fig, use_container_width=True)
            
            with metric_tabs[2]:
                st.write("**Progress Towards Goals:**")
                if client['goal'] == "Weight Loss":
                    outcomes = {"Weight Loss": 68, "Body Fat Reduction": 72, "Energy Levels": 85, "Fitness Improvement": 60}
                elif client['goal'] == "Muscle Gain":
                    outcomes = {"Muscle Gain": 75, "Strength Increase": 80, "Recovery Time": 65, "Protein Intake": 90}
                elif client['goal'] == "Performance":
                    outcomes = {"Endurance": 82, "Energy During Workouts": 75, "Recovery Time": 70, "Performance Metrics": 78}
                else:
                    outcomes = {"Overall Wellness": 85, "Energy Levels": 80, "Diet Sustainability": 90, "Health Markers": 75}
                outcome_cols = st.columns(2)
                for i, (outcome, value) in enumerate(outcomes.items()):
                    with outcome_cols[i % 2]:
                        fig = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=value,
                            title={'text': outcome},
                            gauge={
                                'axis': {'range': [0, 100]},
                                'bar': {'color': "darkblue"},
                                'steps': [
                                    {'range': [0, 50], 'color': "lightgray"},
                                    {'range': [50, 75], 'color': "gray"},
                                    {'range': [75, 100], 'color': "lightblue"}
                                ],
                                'threshold': {
                                    'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75,
                                    'value': 90
                                }
                            }
                        ))
                        fig.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=20))
                        st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("Progress Notes")
            notes = [
                {"date": "2025-04-01", "note": "Client has been consistent with protein intake. Energy levels improved."},
                {"date": "2025-03-15", "note": "Missed several tracking days due to travel. Getting back on track now."},
                {"date": "2025-03-01", "note": "Adjusted meal plan to accommodate new work schedule."},
                {"date": "2025-02-15", "note": "Client reports improved sleep quality and morning energy."}
            ]
            for note in notes:
                st.write(f"**{note['date']}:** {note['note']}")
            
            with st.form("add_note_form"):
                st.subheader("Add Progress Note")
                new_note = st.text_area("Note:", placeholder="Enter progress note...")
                submit_button = st.form_submit_button("Add Note")
                if submit_button and new_note:
                    today = datetime.now().strftime('%Y-%m-%d')
                    st.success("Progress note added successfully!")
                    st.write(f"**{today}:** {new_note}")
            
            if st.button("Generate Progress Report"):
                with st.spinner("Generating report..."):
                    time.sleep(2)
                    report_text = f"# Progress Report for {client['name']}\n\n"
                    report_text += f"**Report Period:** {progress_period}\n"
                    report_text += f"**Generated on:** {datetime.now().strftime('%Y-%m-%d')}\n\n"
                    report_text += f"## Weight Progress\n"
                    report_text += f"Starting Weight: {start_weight} lbs\n"
                    report_text += f"Current Weight: {weights[-1]:.1f} lbs\n"
                    report_text += f"Change: {weights[-1] - start_weight:.1f} lbs\n\n"
                    report_text += f"## Adherence Metrics\n"
                    for metric, value in adherence_data.items():
                        report_text += f"- {metric}: {value}%\n"
                    report_text += "\n"
                    report_text += f"## Progress Notes\n"
                    for note in notes:
                        report_text += f"**{note['date']}:** {note['note']}\n"
                    report_text += "\n"
                    report_text += f"## Recommendations\n"
                    report_text += "1. Continue focusing on protein intake consistency\n"
                    report_text += "2. Increase water intake to support metabolism\n"
                    report_text += "3. Consider adding one additional strength training session per week\n"
                    
                    st.download_button(
                        label="Download Progress Report",
                        data=report_text,
                        file_name=f"progress_report_{client['name'].replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
else:
    st.title("Client Management")
    
    search_term = st.text_input("Search clients:", placeholder="Enter name, goal, or diet type...")
    
    col1, col2 = st.columns(2)
    with col1:
        goal_filter = st.selectbox(
            "Filter by goal:",
            ["All Goals", "Weight Loss", "Muscle Gain", "Maintenance", "Performance", "Health"]
        )
    with col2:
        diet_filter = st.selectbox(
            "Filter by diet type:",
            ["All Diets", "Low Carb", "High Protein", "Balanced", "Keto", "Mediterranean", "Vegan", "Vegetarian"]
        )
    
    filtered_clients = clients
    if search_term:
        filtered_clients = [
            client for client in filtered_clients 
            if search_term.lower() in client['name'].lower() or 
               search_term.lower() in client['goal'].lower() or 
               search_term.lower() in client['diet'].lower()
        ]
    if goal_filter != "All Goals":
        filtered_clients = [
            client for client in filtered_clients 
            if client['goal'] == goal_filter
        ]
    if diet_filter != "All Diets":
        filtered_clients = [
            client for client in filtered_clients 
            if client['diet'] == diet_filter
        ]
    
    if filtered_clients:
        st.write(f"Showing {len(filtered_clients)} clients")
        for client in filtered_clients:
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    st.subheader(client['name'])
                    st.write(f"**Goal:** {client['goal']}")
                    st.write(f"**Diet:** {client['diet']}")
                with col2:
                    st.write(f"**Age:** {client['age']}")
                    st.write(f"**Allergies:** {client['allergies']}")
                    st.write(f"**Activity Level:** {client['activity_level']}")
                with col3:
                    st.write("")
                    if st.button("View Profile", key=f"view_{client['id']}"):
                        st.session_state.selected_client_id = client['id']
                        st.session_state.selected_client_name = client['name']
                        st.rerun()
    else:
        st.info("No clients match your search criteria.")
    
    st.markdown("---")
    if st.button("+ Add New Client"):
        st.session_state.add_client = True
    
    if st.session_state.get('add_client', False):
        st.subheader("Add New Client")
        with st.form("add_client_form"):
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name:")
                last_name = st.text_input("Last Name:")
                age = st.number_input("Age:", min_value=16, max_value=100, value=30)
                email = st.text_input("Email:")
            with col2:
                phone = st.text_input("Phone:")
                height = st.text_input("Height (e.g., 5'10\"):")
                weight = st.text_input("Weight (lbs):")
                activity_level = st.selectbox(
                    "Activity Level:",
                    ["Sedentary", "Light", "Moderate", "Active", "Very Active"]
                )
            col1, col2 = st.columns(2)
            with col1:
                goal = st.selectbox(
                    "Primary Goal:",
                    ["Weight Loss", "Muscle Gain", "Maintenance", "Performance", "Health"]
                )
                diet = st.selectbox(
                    "Diet Type:",
                    ["Low Carb", "High Protein", "Balanced", "Keto", "Mediterranean", "Vegan", "Vegetarian"]
                )
            with col2:
                allergies = st.text_input("Allergies/Intolerances (comma-separated):")
                budget = st.number_input("Weekly Budget ($):", min_value=50.0, max_value=500.0, value=100.0, step=10.0)
            submit_button = st.form_submit_button("Add Client")
            if submit_button and first_name and last_name and email:
                st.success(f"Client {first_name} {last_name} added successfully!")
                if 'add_client' in st.session_state:
                    del st.session_state.add_client
                time.sleep(1)
                st.rerun()

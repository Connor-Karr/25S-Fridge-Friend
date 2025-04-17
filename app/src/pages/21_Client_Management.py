import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from modules.nav import SideBarLinks

# Authentication check
if not st.session_state.get('authenticated', False) or st.session_state.role != "nutritionist":
    st.warning("Please log in as Nancy to access this page")
    st.stop()

SideBarLinks(st.session_state.role)

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
        "status": "On Track"
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
        "status": "Needs Review"
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
        "status": "On Track"
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
        "status": "Needs Review"
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
        "status": "On Track"
    }
]

# Get selected client ID from session state
selected_client_id = st.session_state.get('selected_client_id', None)

# Main page content
if selected_client_id:
    # Find the selected client in our mock data
    client = next((c for c in clients if c["id"] == selected_client_id), None)
    
    if client:
        st.title(f"Client Profile: {client['name']}")
        
        # Create tabs for different sections
        tab1, tab2, tab3 = st.tabs(["Basic Info", "Nutrition Plan", "Progress"])
        
        # Basic Info Tab
        with tab1:
            st.header("Client Information")
            
            # Create a simple table with client details
            client_info = {
                "Field": ["Age", "Email", "Phone", "Height", "Weight", "Goal", "Diet Type", "Allergies", "Status"],
                "Value": [
                    client['age'],
                    client['email'],
                    client['phone'],
                    client['height'],
                    client['weight'],
                    client['goal'],
                    client['diet'],
                    client['allergies'],
                    client['status']
                ]
            }
            
            client_df = pd.DataFrame(client_info)
            st.table(client_df)
            
            # Calculate basic nutrition targets
            weight_lbs = float(client['weight'].split()[0])
            weight_kg = weight_lbs * 0.453592
            
            # Simple calculation based on weight and goal
            if client['goal'] == "Weight Loss":
                calorie_target = int(weight_kg * 30)
                protein_target = int(weight_kg * 2.0)
                carb_target = int(weight_kg * 2.5)
                fat_target = int(weight_kg * 1.0)
            elif client['goal'] == "Muscle Gain":
                calorie_target = int(weight_kg * 35)
                protein_target = int(weight_kg * 2.5)
                carb_target = int(weight_kg * 4.0)
                fat_target = int(weight_kg * 1.0)
            else:
                calorie_target = int(weight_kg * 33)
                protein_target = int(weight_kg * 1.8)
                carb_target = int(weight_kg * 3.5)
                fat_target = int(weight_kg * 1.0)
            
            # Display nutrition targets
            st.header("Nutrition Targets")
            targets_data = {
                "Target": ["Calories", "Protein", "Carbohydrates", "Fat"],
                "Daily Amount": [
                    f"{calorie_target} kcal",
                    f"{protein_target} g",
                    f"{carb_target} g",
                    f"{fat_target} g"
                ]
            }
            
            targets_df = pd.DataFrame(targets_data)
            st.table(targets_df)
        
        # Nutrition Plan Tab
        with tab2:
            st.header("Daily Meal Plan")
            
            # Mock meal plan data
            meals = [
                {"name": "Breakfast", "description": "Greek yogurt with berries and granola", "calories": 350, "protein": 20, "carbs": 40, "fat": 10},
                {"name": "Snack", "description": "Apple with almond butter", "calories": 200, "protein": 5, "carbs": 25, "fat": 10},
                {"name": "Lunch", "description": "Grilled chicken salad with olive oil dressing", "calories": 450, "protein": 35, "carbs": 20, "fat": 25},
                {"name": "Snack", "description": "Protein shake with banana", "calories": 250, "protein": 25, "carbs": 30, "fat": 3},
                {"name": "Dinner", "description": "Salmon with quinoa and roasted vegetables", "calories": 550, "protein": 40, "carbs": 45, "fat": 22}
            ]
            
            # Create a table for the meal plan
            meal_data = []
            for meal in meals:
                meal_data.append({
                    "Meal": meal["name"],
                    "Description": meal["description"],
                    "Calories": meal["calories"],
                    "Protein (g)": meal["protein"],
                    "Carbs (g)": meal["carbs"],
                    "Fat (g)": meal["fat"]
                })
            
            meal_df = pd.DataFrame(meal_data)
            st.table(meal_df)
            
            # Calculate daily totals
            total_calories = sum(meal["calories"] for meal in meals)
            total_protein = sum(meal["protein"] for meal in meals)
            total_carbs = sum(meal["carbs"] for meal in meals)
            total_fat = sum(meal["fat"] for meal in meals)
            
            st.subheader("Daily Totals")
            totals_data = {
                "Nutrient": ["Calories", "Protein", "Carbohydrates", "Fat"],
                "Amount": [
                    f"{total_calories} kcal",
                    f"{total_protein} g",
                    f"{total_carbs} g",
                    f"{total_fat} g"
                ],
                "% of Target": [
                    f"{int(total_calories / calorie_target * 100)}%",
                    f"{int(total_protein / protein_target * 100)}%",
                    f"{int(total_carbs / carb_target * 100)}%",
                    f"{int(total_fat / fat_target * 100)}%"
                ]
            }
            
            totals_df = pd.DataFrame(totals_data)
            st.table(totals_df)
            
            # Check for allergies in meals
            if client["allergies"] != "None":
                st.subheader("Allergy Check")
                st.info(f"Remember to check meals for {client['allergies']} allergens.")
        
        # Progress Tab
        with tab3:
            st.header("Client Progress")
            
            # Create mock weekly progress data
            progress_data = []
            
            # Start date (6 weeks ago)
            start_date = datetime.now() - timedelta(weeks=6)
            
            # Generate weekly data
            for i in range(6):
                week_date = (start_date + timedelta(weeks=i)).strftime('%Y-%m-%d')
                
                # Set weight based on client goal
                start_weight = float(client['weight'].split()[0])
                if client['goal'] == "Weight Loss":
                    weight = start_weight - (i * 1.2)
                elif client['goal'] == "Muscle Gain":
                    weight = start_weight + (i * 0.5)
                else:
                    weight = start_weight + (i * 0.1) - (i * 0.1)  # Small fluctuations
                
                progress_data.append({
                    "Week": week_date,
                    "Weight (lbs)": round(weight, 1),
                    "Plan Adherence": f"{80 + i * 3}%",
                    "Notes": [
                        "Started program",
                        "Adjusted protein intake",
                        "Increased water consumption",
                        "Added strength training",
                        "Improved meal timing",
                        "Meeting all targets"
                    ][i]
                })
            
            # Create DataFrame and display
            progress_df = pd.DataFrame(progress_data)
            st.table(progress_df)
            
            # Current stats
            st.subheader("Current Status")
            st.info(f"Current weight: {progress_data[-1]['Weight (lbs)']} lbs")
            st.info(f"Plan adherence: {progress_data[-1]['Plan Adherence']}")
            st.info(f"Total weight change: {round(progress_data[-1]['Weight (lbs)'] - progress_data[0]['Weight (lbs)'], 1)} lbs")
        
        # Go back to client list button
        if st.button("← Back to Client List"):
            st.session_state.selected_client_id = None
            st.rerun()
else:
    # Display the client list
    st.title("Client Management")
    
    # Simple client search
    search_term = st.text_input("Search by name:", placeholder="Enter client name...")
    
    # Apply search filter
    filtered_clients = clients.copy()
    if search_term:
        filtered_clients = [c for c in filtered_clients if search_term.lower() in c['name'].lower()]
    
    # Show filtered client list
    if filtered_clients:
        st.subheader(f"Showing {len(filtered_clients)} clients")
        
        # Convert clients to DataFrame for table display
        clients_for_display = []
        for client in filtered_clients:
            clients_for_display.append({
                "ID": client["id"],
                "Name": client["name"],
                "Age": client["age"],
                "Goal": client["goal"],
                "Diet": client["diet"],
                "Status": client["status"]
            })
        
        clients_df = pd.DataFrame(clients_for_display)
        st.table(clients_df)
        
        # Client selection input
        selected_id = st.selectbox(
            "Select Client to View:",
            options=[client["id"] for client in filtered_clients],
            format_func=lambda x: next((client["name"] for client in filtered_clients if client["id"] == x), "")
        )
        
        if st.button("View Client"):
            st.session_state.selected_client_id = selected_id
            st.rerun()
    else:
        st.info("No clients match your search criteria.")
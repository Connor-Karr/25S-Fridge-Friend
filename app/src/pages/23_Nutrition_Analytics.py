import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
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
NUTRITION_TRACKING_ENDPOINT = f"{API_BASE_URL}/logs/nutrition"

# Page header
st.title("Nutrition Analytics")
st.write("Analyze client nutrition data and identify trends")

# Simple time period selection
time_period = st.selectbox(
    "Analysis Period:",
    ["Last 30 Days", "Last 3 Months", "Last 6 Months", "Year to Date"]
)

# Calculate date range based on selection
if time_period == "Last 30 Days":
    days = 30
elif time_period == "Last 3 Months":
    days = 90
elif time_period == "Last 6 Months":
    days = 180
else:  # Year to Date
    start_of_year = datetime(datetime.now().year, 1, 1).date()
    days = (datetime.now().date() - start_of_year).days

start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
end_date = datetime.now().strftime('%Y-%m-%d')

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

# Function to get nutrition tracking data
def get_nutrition_data(client_id=None):
    try:
        endpoint = NUTRITION_TRACKING_ENDPOINT
        if client_id:
            endpoint += f"/{client_id}"
        response = requests.get(endpoint)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching nutrition data: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"API connection error: {str(e)}")
        return []

# Get users from API
users = get_all_users()

# Create tabs for different analysis types
tab1, tab2, tab3 = st.tabs(["Diet Compliance", "Nutrient Analysis", "Allergies"])

# Diet Compliance Tab
with tab1:
    st.header("Diet Compliance Analysis")
    
    # Simple filter for diet type
    diet_filter = st.selectbox(
        "Filter by diet type:",
        ["All Diets", "low-carb", "high-protein", "balanced", "keto", "mediterranean"]
    )
    
    # Get constraints for all users to determine diet types
    compliance_data = []
    
    for user in users:
        pc_id = user.get("pc_id")
        if pc_id:
            # Get user constraints to determine diet type
            constraints = get_user_constraints(pc_id)
            if constraints:
                diet_type = constraints.get("personal_diet", "Not specified")
                
                # Get nutrition data for compliance calculation
                nutrition_data = get_nutrition_data(user.get("user_id"))
                
                # Calculate compliance based on diet type and nutrition data
                # In a real app, this would be a complex calculation based on actual tracking data
                compliance = 0
                if nutrition_data:
                    # Simple placeholder calculation
                    # In a real app, this would analyze if the user met their macro targets
                    compliance = 80  # Default placeholder value
                else:
                    # No nutrition data, assume medium compliance
                    compliance = 70
                
                # Only include if it matches the filter
                if diet_filter == "All Diets" or diet_filter.lower() in diet_type.lower():
                    compliance_data.append({
                        "Client": f"{user.get('f_name', '')} {user.get('l_name', '')}",
                        "Diet Type": diet_type,
                        "Compliance (%)": compliance,
                        "Status": "On Track" if compliance >= 80 else "Needs Attention"
                    })
    
    # Create DataFrame and display
    if compliance_data:
        compliance_df = pd.DataFrame(compliance_data)
        st.table(compliance_df)
        
        # Calculate and show average compliance
        avg_compliance = sum(item["Compliance (%)"] for item in compliance_data) / len(compliance_data)
        st.info(f"Average compliance: {avg_compliance:.1f}%")
    else:
        st.info(f"No clients found with {diet_filter if diet_filter != 'All Diets' else 'any'} diet plan.")
    
    # Key factors affecting compliance
    st.subheader("Key Compliance Factors")
    
    factors_data = {
        "Factor": ["Meal Tracking Frequency", "Using Recommended Foods", "Following Portion Sizes", "Meal Timing", "Following Macronutrient Ratios"],
        "Adherence (%)": [85, 72, 68, 76, 64]
    }
    
    factors_df = pd.DataFrame(factors_data)
    st.table(factors_df)
    
    # Simple recommendations based on data
    st.subheader("Recommendations to Improve Compliance")
    st.write("1. Simplify meal plans for clients struggling with adherence")
    st.write("2. Focus on portion control education - this is a common challenge area")
    st.write("3. Provide visual guides for macronutrient ratios")
    st.write("4. Encourage use of meal tracking app with reminders")

# Nutrient Analysis Tab
with tab2:
    st.header("Nutrient Analysis")
    
    # Nutrient selection
    nutrient = st.selectbox(
        "Select nutrient to analyze:",
        ["Protein", "Carbohydrates", "Fat", "Fiber", "Sodium", "Calories"]
    )
    
    # Group by selection
    group_by = st.selectbox(
        "Group analysis by:",
        ["Diet Type", "Age Group"]
    )
    
    # Get nutrition data
    all_nutrition_data = []
    for user in users:
        user_id = user.get("user_id")
        if user_id:
            # Get user's nutrition tracking data
            user_nutrition = get_nutrition_data(user_id)
            
            # Get user's constraints to determine diet type and age group
            pc_id = user.get("pc_id")
            constraints = None
            if pc_id:
                constraints = get_user_constraints(pc_id)
            
            # Add to collection with grouping info
            if user_nutrition and constraints:
                for entry in user_nutrition:
                    entry["user_name"] = f"{user.get('f_name', '')} {user.get('l_name', '')}"
                    entry["diet_type"] = constraints.get("personal_diet", "Not specified")
                    entry["age_group"] = constraints.get("age_group", "adult")
                    all_nutrition_data.append(entry)
    
    # Process nutrition data based on grouping
    if all_nutrition_data:
        # Analyze based on selected nutrient and grouping
        nutrient_to_key = {
            "Protein": "protein",
            "Carbohydrates": "carbs", 
            "Fat": "fat",
            "Fiber": "fiber",
            "Sodium": "sodium",
            "Calories": "calories"
        }
        
        nutrient_key = nutrient_to_key.get(nutrient, "protein")
        
        # Group data
        grouped_data = {}
        for entry in all_nutrition_data:
            group = entry.get("diet_type" if group_by == "Diet Type" else "age_group", "Unknown")
            if group not in grouped_data:
                grouped_data[group] = []
            
            # Add nutrient value to the group
            value = entry.get(nutrient_key, 0)
            if value is not None:
                grouped_data[group].append(value)
        
        # Calculate averages for each group
        analysis_data = []
        for group, values in grouped_data.items():
            if values:
                avg_value = sum(values) / len(values)
                # Determine target based on group
                target = 0
                if nutrient == "Protein":
                    target = 100 if group == "high-protein" else 80
                elif nutrient == "Carbohydrates":
                    target = 100 if group == "low-carb" else 250
                elif nutrient == "Fat":
                    target = 50 if group == "low-fat" else 70
                elif nutrient == "Fiber":
                    target = 25
                elif nutrient == "Sodium":
                    target = 2300
                elif nutrient == "Calories":
                    target = 2000
                
                # Calculate percentage of target
                pct_of_target = (avg_value / target * 100) if target > 0 else 0
                
                analysis_data.append({
                    "Group": group,
                    "Current Intake": round(avg_value, 1),
                    "Target Intake": target,
                    "% of Target": round(pct_of_target, 1)
                })
        
        # Create DataFrame and display
        if analysis_data:
            nutrient_df = pd.DataFrame(analysis_data)
            st.subheader(f"{nutrient} Analysis by {group_by}")
            st.table(nutrient_df)
        else:
            st.info(f"No nutrition data available for {nutrient} analysis.")
    else:
        st.info("No nutrition tracking data available. Please check your API connection.")
    
    # Show insights based on nutrient
    st.subheader("Nutrient Insights")
    
    if nutrient == "Protein":
        st.info("• High-protein diet clients are typically meeting protein targets")
        st.info("• Most clients need additional protein education for optimal intake")
    elif nutrient == "Carbohydrates":
        st.info("• Low-carb diet clients are generally staying within their carb limits")
        st.info("• Reminder: weekend carb intake is often higher than weekdays")
    elif nutrient == "Fat":
        st.info("• Most clients need education on healthy fat sources")
        st.info("• Mediterranean diet followers typically have better fat quality intake")
    elif nutrient == "Fiber":
        st.warning("• Fiber intake is below target for most clients")
        st.info("• Recommend increasing vegetable and whole grain consumption")
    elif nutrient == "Sodium":
        st.warning("• Sodium intake often exceeds recommendations")
        st.info("• Focus on reducing processed food consumption")
    else:  # Calories
        st.info("• Calorie targets are generally being met by most clients")
        st.info("• Adjust individual targets based on activity level and goals")

# Allergies Tab
with tab3:
    st.header("Allergy & Dietary Restriction Analysis")
    
    # Get dietary restrictions from all user constraints
    allergies_count = {}
    
    for user in users:
        pc_id = user.get("pc_id")
        if pc_id:
            constraints = get_user_constraints(pc_id)
            if constraints and constraints.get("dietary_restrictions"):
                restrictions = constraints.get("dietary_restrictions").lower().split(",")
                for restriction in restrictions:
                    restriction = restriction.strip()
                    if restriction and restriction != "none":
                        allergies_count[restriction] = allergies_count.get(restriction, 0) + 1
    
    # Create table of allergies
    if allergies_count:
        total_users = sum(allergies_count.values())
        allergy_data = []
        for allergen, count in allergies_count.items():
            allergy_data.append({
                "Allergen": allergen.capitalize(),
                "Client Count": count,
                "Percentage": f"{round(count / len(users) * 100)}%"
            })
        
        allergy_df = pd.DataFrame(allergy_data)
        st.table(allergy_df)
    else:
        st.info("No dietary restrictions or allergies found among clients.")
    
    # Substitution recommendations
    st.subheader("Common Substitutions")
    
    substitution_data = {
        "Allergen": ["Dairy", "Dairy", "Gluten", "Gluten", "Nuts", "Eggs", "Soy"],
        "Food Item": ["Milk", "Cheese", "Wheat Flour", "Bread", "Peanut Butter", "Eggs in Baking", "Soy Sauce"],
        "Substitution": ["Almond Milk", "Nutritional Yeast", "Rice Flour", "Gluten-Free Bread", "Sunflower Seed Butter", "Flax Egg", "Coconut Aminos"]
    }
    
    substitution_df = pd.DataFrame(substitution_data)
    st.table(substitution_df)
    
    # Impact of allergies on nutrition
    st.subheader("Nutritional Impact of Allergies")
    
    impact_data = {
        "Allergen": ["Dairy", "Dairy", "Gluten", "Gluten", "Nuts"],
        "Affected Nutrient": ["Calcium", "Vitamin D", "Fiber", "B Vitamins", "Healthy Fats"],
        "Impact": ["High", "High", "Medium", "Medium", "Medium"],
        "Alternative Sources": ["Fortified Plant Milks, Leafy Greens", "Supplements, Sunlight", "Vegetables, Fruits", "Supplements, Meat", "Avocado, Seeds, Olive Oil"]
    }
    
    impact_df = pd.DataFrame(impact_data)
    st.table(impact_df)
    
    # Recommendations section
    st.subheader("Key Recommendations")
    
    st.write("1. **Dairy Allergies**: Focus on non-dairy calcium sources (fortified plant milks, leafy greens) and consider vitamin D supplementation.")
    st.write("2. **Gluten Allergies**: Increase fiber from non-grain sources (vegetables, fruits) and consider B vitamin supplementation.")
    st.write("3. **Nut Allergies**: Incorporate more seeds and avocados for healthy fats.")
    st.write("4. **Overall Strategy**: Create specialized meal plans for clients with specific allergens.")

# Report Generation Section
st.header("Generate Nutrition Reports")

with st.form("generate_report_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        report_type = st.selectbox(
            "Report Type:",
            ["Client Summary", "Diet Compliance", "Nutrition Analysis"]
        )
        
        # Client selection from actual users
        client_options = [f"{user.get('f_name', '')} {user.get('l_name', '')}" for user in users]
        client_selection = st.multiselect(
            "Select clients:",
            client_options,
            default=[client_options[0]] if client_options else []
        )
    
    with col2:
        include_tables = st.checkbox("Include tables", value=True)
        include_recommendations = st.checkbox("Include recommendations", value=True)
        report_format = st.selectbox(
            "Report format:",
            ["PDF", "Excel", "Text"]
        )
    
    submit = st.form_submit_button("Generate Report")
    
    if submit:
        if client_selection:
            st.success("Report generated successfully!")
            
            report_content = f"""
            # Nutrition Analysis Report
            Report Type: {report_type}
            Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
            
            ## Clients Included
            {', '.join(client_selection)}
            
            ## Summary
            This report provides analysis of nutritional data for the selected clients over the {time_period}.
            
            ## Key Findings
            - Diet compliance analysis shows varying levels of adherence across clients
            - Key areas for improvement include portion control and meal timing
            """
            
            st.download_button(
                label="Download Report",
                data=report_content,
                file_name=f"nutrition_report_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
        else:
            st.warning("Please select at least one client for the report.")
import streamlit as st
import pandas as pd
from modules.nav import SideBarLinks

# Authentication check
if not st.session_state.get('authenticated', False) or st.session_state.role != "athlete":
    st.warning("Please log in as Riley to access this page")
    st.stop()

# Set up navigation
SideBarLinks(st.session_state.role)

st.title("🍽️ Athlete Meal Plans")
st.write("Optimize your nutrition with targeted meal plans for different training phases")

# Static meal plans data
meal_plans = [
    {"Meal": "Pre-Run Oatmeal Bowl", "Phase": "Pre-Workout", "Calories": 380, "Protein": 12, "Carbs": 68, "Fat": 8, "Servings": 1},
    {"Meal": "Recovery Protein Smoothie", "Phase": "Recovery", "Calories": 320, "Protein": 30, "Carbs": 42, "Fat": 5, "Servings": 1},
    {"Meal": "Salmon & Quinoa Dinner", "Phase": "Maintenance", "Calories": 450, "Protein": 35, "Carbs": 40, "Fat": 18, "Servings": 1},
    {"Meal": "Carb-Loading Pasta", "Phase": "Race Day", "Calories": 580, "Protein": 20, "Carbs": 95, "Fat": 12, "Servings": 2}
]

# Nutrition strategies for training phases
phase_nutrition = {
    "Base Building": {
        "Calories": "Maintenance",
        "Carbs": "Moderate (5-6g/kg/day)",
        "Protein": "Moderate (1.6g/kg/day)",
        "Fat": "Moderate (1g/kg/day)",
        "Emphasis": "Building good nutritional habits",
        "Meals": ["Oatmeal with yogurt and berries", "Chicken with rice and vegetables"]
    },
    "Build Phase": {
        "Calories": "Slight surplus",
        "Carbs": "Moderate-high (6-8g/kg/day)",
        "Protein": "High (1.8g/kg/day)",
        "Fat": "Moderate (1g/kg/day)",
        "Emphasis": "Fueling harder workouts",
        "Meals": ["Protein pancakes with banana", "Turkey wrap with vegetables"]
    },
    "Peaking": {
        "Calories": "Maintenance",
        "Carbs": "High (8-10g/kg/day)",
        "Protein": "High (1.8g/kg/day)",
        "Fat": "Low-moderate (0.8g/kg/day)",
        "Emphasis": "Maximum glycogen storage",
        "Meals": ["Oatmeal with honey", "Pasta with lean meat sauce"]
    },
    "Taper": {
        "Calories": "Slightly reduced",
        "Carbs": "Moderate-high (7-8g/kg/day)",
        "Protein": "Moderate (1.6g/kg/day)",
        "Fat": "Low-moderate (0.8g/kg/day)",
        "Emphasis": "Maintaining glycogen while reducing volume",
        "Meals": ["Greek yogurt with granola", "Fish with potatoes"]
    },
    "Race Week": {
        "Calories": "Maintenance",
        "Carbs": "High (8-12g/kg/day)",
        "Protein": "Moderate (1.5g/kg/day)",
        "Fat": "Low (0.5g/kg/day)",
        "Emphasis": "Carb-loading, easy digestion",
        "Meals": ["Toast with honey", "Plain pasta with light sauce"]
    },
    "Recovery": {
        "Calories": "Maintenance",
        "Carbs": "Moderate (5-6g/kg/day)",
        "Protein": "High (2.0g/kg/day)",
        "Fat": "Moderate (1g/kg/day)",
        "Emphasis": "Tissue repair, inflammation reduction",
        "Meals": ["Protein smoothie with berries", "Salmon with vegetables"]
    }
}

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Current Plans", "Race Day", "Recovery", "Training Phases"])

with tab1:
    st.subheader("Current Meal Plans")
    st.dataframe(pd.DataFrame(meal_plans))

with tab2:
    st.subheader("Race Day Nutrition")
    st.write("Specialized meal plans for before, during, and after races")
    st.markdown("### Race Day Timeline")
    st.markdown("""
**Before Race:**
- Night Before: Carb-loading dinner
- 3 Hours Before: Pre-race breakfast
- 30 Minutes Before: Final fuel

**During Race:**
- Hydration and energy as needed

**After Race:**
- Immediately: Initial recovery nutrition
- Within 2 Hours: Complete recovery meal
""")
    st.markdown("### Sample Carb Needs Table")
    carb_table = pd.DataFrame({
        "Race Distance": ["5K", "10K", "Half Marathon", "Marathon"],
        "Carb Multiplier (g/kg)": [1.0, 1.5, 2.0, 3.0]
    })
    st.dataframe(carb_table)

with tab3:
    st.subheader("Recovery Nutrition")
    st.write("Optimize your recovery with targeted nutrition strategies")
    st.markdown("### Recovery Timeline")
    st.markdown("""
- 0-30 minutes: Consume a recovery drink or smoothie
- 1-2 hours: Eat a balanced meal with protein and carbs
""")
    st.markdown("### Good Options for Recovery")
    st.write(pd.DataFrame({
        "Food": [
            "Protein smoothie with banana and berries",
            "Chocolate milk",
            "Greek yogurt with fruit",
            "Turkey sandwich"
        ]
    }))

with tab4:
    st.subheader("Training Phase Nutrition")
    st.write("Adjust your nutrition strategy for different training phases")
    for phase, data in phase_nutrition.items():
        st.markdown(f"#### {phase}")
        st.write(pd.DataFrame({
            "Calories": [data["Calories"]],
            "Carbs": [data["Carbs"]],
            "Protein": [data["Protein"]],
            "Fat": [data["Fat"]],
            "Emphasis": [data["Emphasis"]]
        }))
        st.markdown("**Sample Meals:**")
        st.write(pd.DataFrame({"Meal": data["Meals"]}))
        st.markdown("---")

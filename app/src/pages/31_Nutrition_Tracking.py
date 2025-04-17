import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from modules.nav import SideBarLinks

# --- Authentication check ---
if not st.session_state.get('authenticated', False) or st.session_state.role != "athlete":
    st.warning("Please log in as Riley to access this page")
    st.stop()

# --- Sidebar navigation ---
SideBarLinks(st.session_state.role)

# --- Page header ---
st.title("📊 Nutrition Tracking")
st.write("Track and analyze your nutrition to optimize performance")

# --- Mock nutrition data for demonstration ---
nutrition_logs = [
    {"tracking_id": 1, "client_id": 1, "protein": 89, "fat": 38, "fiber": 18, "sodium": 1200, "vitamins": 80, "calories": 1241, "carbs": 135},
    {"tracking_id": 2, "client_id": 1, "protein": 120, "fat": 45, "fiber": 22, "sodium": 1500, "vitamins": 90, "calories": 1650, "carbs": 180},
    {"tracking_id": 3, "client_id": 1, "protein": 105, "fat": 42, "fiber": 25, "sodium": 1350, "vitamins": 85, "calories": 1450, "carbs": 160}
]

targets = {
    "Protein": 135,
    "Carbs": 225, 
    "Fat": 55,
    "Fiber": 30,
    "Sodium": 2000,
    "Calories": 1900
}

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["Daily Tracker", "Log Meal", "Nutrition Analysis"])

# --- Tab 1: Daily Tracker ---
with tab1:
    st.subheader("Today's Nutrition")
    today_log = nutrition_logs[0]

    consumed = {
        "Protein": today_log.get("protein", 0),
        "Carbs": today_log.get("carbs", 0),
        "Fat": today_log.get("fat", 0),
        "Fiber": today_log.get("fiber", 0),
        "Sodium": today_log.get("sodium", 0),
        "Calories": today_log.get("calories", 0)
    }

    df = pd.DataFrame({
        "Target": targets,
        "Consumed": consumed
    })
    st.dataframe(df)

    st.subheader("Macro Ratios (Calories from Macros)")
    protein_calories = consumed["Protein"] * 4
    carb_calories = consumed["Carbs"] * 4
    fat_calories = consumed["Fat"] * 9
    total_macro_calories = protein_calories + carb_calories + fat_calories

    if total_macro_calories > 0:
        macro_ratio_df = pd.DataFrame({
            "Macronutrient": ["Protein", "Carbs", "Fat"],
            "Calories": [protein_calories, carb_calories, fat_calories],
            "Percent": [
                round(protein_calories / total_macro_calories * 100, 1),
                round(carb_calories / total_macro_calories * 100, 1),
                round(fat_calories / total_macro_calories * 100, 1)
            ]
        })
        st.dataframe(macro_ratio_df)

    st.subheader("Water Intake (Example)")
    st.write("Water Consumed: 1.8L / 3.0L")

# --- Tab 2: Log Meal ---
with tab2:
    st.subheader("Recent Meals (Example)")
    # Show the same nutrition logs as a table
    st.dataframe(pd.DataFrame(nutrition_logs))

    st.subheader("Meal Templates (Example)")
    templates = [
        {"name": "Pre-run Breakfast", "protein": 20, "carbs": 50, "fat": 10, "calories": 370},
        {"name": "Post-workout Recovery", "protein": 30, "carbs": 45, "fat": 8, "calories": 372},
        {"name": "Light Pre-race Dinner", "protein": 25, "carbs": 60, "fat": 12, "calories": 448},
        {"name": "Protein-focused Lunch", "protein": 35, "carbs": 35, "fat": 15, "calories": 415}
    ]
    st.dataframe(pd.DataFrame(templates))

# --- Tab 3: Nutrition Analysis ---
with tab3:
    st.subheader("Nutrition Analysis (Last 7 Days Example)")
    # Generate mock data for 7 days
    analysis_dates = [(datetime.now().date() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
    np.random.seed(42)
    nutrition_data = []
    for date in analysis_dates:
        protein = np.random.normal(120, 15)
        carbs = np.random.normal(200, 30)
        fat = np.random.normal(50, 8)
        calories = (protein * 4) + (carbs * 4) + (fat * 9) + np.random.normal(0, 50)
        nutrition_data.append({
            'date': date,
            'protein': max(0, round(protein)),
            'carbs': max(0, round(carbs)),
            'fat': max(0, round(fat)),
            'calories': max(0, round(calories))
        })
    df = pd.DataFrame(nutrition_data)
    st.dataframe(df)

    st.subheader("Average Metrics (Last 7 Days)")
    avg_protein = df['protein'].mean()
    avg_carbs = df['carbs'].mean()
    avg_fat = df['fat'].mean()
    avg_calories = df['calories'].mean()
    avg_df = pd.DataFrame({
        "Avg. Protein (g)": [f"{avg_protein:.1f}"],
        "Avg. Carbs (g)": [f"{avg_carbs:.1f}"],
        "Avg. Fat (g)": [f"{avg_fat:.1f}"],
        "Avg. Calories": [f"{avg_calories:.0f}"]
    })
    st.dataframe(avg_df)

    st.subheader("Insights (Example)")
    st.write("- Protein intake is well-balanced.")
    st.write("- Carbohydrate intake is aligned with training needs.")
    st.write("- Fat intake is in the optimal range.")
    st.write("- Calorie intake is supporting your training needs.")

    st.subheader("Recommendations (Example)")
    st.write("1. Add a post-workout protein shake if protein is low.")
    st.write("2. Include more whole grains and fruits if carbs are low.")
    st.write("3. Add healthy fats if fat intake is low.")
    st.write("4. Increase portion sizes if calorie intake is low.")

    st.markdown("---")
    st.subheader("📚 Nutrition Resources for Runners")
    st.write("Race Day Nutrition Guide, Runner's Recipe Book, Training Phase Nutrition Calculator, Hydration Calculator (see app resources).")

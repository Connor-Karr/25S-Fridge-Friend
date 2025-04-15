import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime, timedelta
from PIL import Image
import base64
from modules.nav import SideBarLinks
import plotly.express as px

# page configuration
st.set_page_config(
    page_title="FridgeFriend",
    page_icon="🍏",
    layout="wide",
    initial_sidebar_state="expanded"
)


if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'role' not in st.session_state:
    st.session_state.role = None
if 'first_name' not in st.session_state:
    st.session_state.first_name = None

# sidebar navigation
SideBarLinks(st.session_state.role)

#App header
col1, col2 = st.columns([1, 5])

with col1:
    st.image("https://via.placeholder.com/150x150.png?text=FridgeFriend", width=120)

with col2:
    st.title("FridgeFriend")
    st.subheader("Smart Food Management & Nutrition Tracking")


# Main page content
st.markdown("""
## Welcome to FridgeFriend!

FridgeFriend is a data-driven application designed to streamline healthy eating by intelligently combining real-time fridge inventory management, personalized nutrition tracking, and dynamic meal suggestions.

### Key Features:
- **Smart Inventory Tracking**: Monitor what's in your fridge and get alerts for expiring items
- **Personalized Nutrition**: Track your macros and nutrition based on your goals
- **Recipe Suggestions**: Get meal ideas based on what's in your fridge
- **Budget Planning**: Stay within your grocery budget with smart planning
- **Allergen Management**: Track dietary restrictions and allergies
""")


st.markdown("### Select Your Profile")
st.write("Choose a profile to log in and access personalized features.")


col1, col2, col3, col4 = st.columns(4)

#Ben
with col1:
    st.markdown("#### 🧑‍🎓 Student")
    st.write("Quick meals & budget tracking")
    if st.button("Login as Ben", key="student"):
        st.session_state.authenticated = True
        st.session_state.role = "busy_student"
        st.session_state.first_name = "Ben"
        st.switch_page("pages/00_Ben_Dashboard.py")

#Alvin
with col2:
    st.markdown("#### 👨‍💻 Administrator")
    st.write("System management & monitoring")
    if st.button("Login as Alvin", key="admin"):
        st.session_state.authenticated = True
        st.session_state.role = "admin"
        st.session_state.first_name = "Alvin"
        st.switch_page("pages/10_Admin_Dashboard.py")

#Nancy
with col3:
    st.markdown("#### 👩‍⚕️ Nutritionist")
    st.write("Client management & meal planning")
    if st.button("Login as Nancy", key="nutritionist"):
        st.session_state.authenticated = True
        st.session_state.role = "nutritionist"
        st.session_state.first_name = "Nancy"
        st.switch_page("pages/20_Nutritionist_Dashboard.py")

# Riley
with col4:
    st.markdown("#### 🏃‍♀️ Athlete")
    st.write("Performance nutrition & tracking")
    if st.button("Login as Riley", key="athlete"):
        st.session_state.authenticated = True
        st.session_state.role = "athlete"
        st.session_state.first_name = "Riley"
        st.switch_page("pages/30_Athlete_Dashboard.py")

# Feature showcase with tabs
st.markdown("---")
st.markdown("## Feature Showcase")

tabs = st.tabs(["Smart Inventory", "Recipe Suggestions", "Nutrition Tracking", "Budget Management"])

# Smart Inventory tab
with tabs[0]:
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.markdown("### Smart Inventory Tracking")
        st.markdown("""
        **Never waste food again!**
        - Real-time inventory tracking
        - Expiration alerts
        - Automatic update when items are used
        - Easy scanning of new groceries
        - Categorized storage system
        """)
    
    with col2:
        inventory_df = pd.DataFrame({
            'Category': ['Dairy', 'Produce', 'Meat', 'Grains', 'Snacks'],
            'Items': [4, 7, 3, 5, 6],
            'Expiring Soon': [1, 2, 1, 0, 0]
        })
        
        st.bar_chart(inventory_df.set_index('Category'))
        st.caption("Example of your inventory breakdown by category")


# Recipe Suggestions tab
with tabs[1]:
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### Intelligent Recipe Suggestions")
        st.markdown("""
        **Cook with what you have!**
        - Recipes based on available ingredients
        - Personalized to your dietary preferences
        - Quick-filter by prep time and difficulty
        - Budget-friendly options
        - Save favorite recipes for later
        """)
    
    with col2:
        st.info("**Quick Stir Fry** (15 mins)\n\n✓ Uses items in your fridge\n✓ Under your calorie goal\n✓ High protein")
        st.success("**Protein Smoothie** (5 mins)\n\n✓ Uses expiring items\n✓ Matches your macros\n✓ Pre-workout friendly")

    # Nutrition Tracking tab
with tabs[2]:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Personalized Nutrition Tracking")
        st.markdown("""
        **Meet your health goals!**
        - Track macro and micronutrients
        - Personalized targets based on goals
        - Visual progress tracking
        - Meal suggestions to meet targets
        - Integration with workout data
        """)
    
    with col2:
        st.write("**Daily Nutrition Progress**")
        st.progress(0.75, text="Protein: 75%")
        st.progress(0.60, text="Carbs: 60%")
        st.progress(0.90, text="Fat: 90%")
        st.progress(0.80, text="Calories: 80%")

# Budget Management tab
with tabs[3]:
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.markdown("### Smart Budget Management")
        st.markdown("""
        **Save money on groceries!**
        - Weekly grocery budget tracking
        - Cost-per-meal calculations
        - Budget-friendly recipe suggestions
        - Waste reduction savings
        - Smart shopping list generation
        """)
    
    with col2:
        budget_data = pd.DataFrame({
            'Category': ['Protein', 'Produce', 'Grains', 'Dairy', 'Snacks'],
            'Expense': [45, 30, 15, 20, 10]
        })
        
        fig = px.pie(
            budget_data, 
            values='Expense', 
            names='Category',
            title='Weekly Grocery Budget Breakdown',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        
        st.plotly_chart(fig, use_container_width=True)

# User testimonials
st.markdown("---")
st.markdown("## What Our Users Say")

testimonial_col1, testimonial_col2, testimonial_col3 = st.columns(3)

with testimonial_col1:
    st.markdown("#### *\"FridgeFriend has saved me over $200 per month on groceries, and I'm eating healthier than ever!\"*")
    st.markdown("**- Jamie, College Student**")

with testimonial_col2:
    st.markdown("#### *\"As a nutritionist, this app has revolutionized how I create meal plans for my clients. The data insights are invaluable.\"*")
    st.markdown("**- Dr. Rachel, Registered Dietitian**")

with testimonial_col3:
    st.markdown("#### *\"Training for marathons requires precise nutrition. FridgeFriend helps me hit my macros perfectly every day.\"*")
    st.markdown("**- Mark, Marathon Runner**")
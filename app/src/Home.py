import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Page configuration 
st.set_page_config(
    page_title="FridgeFriend",
    page_icon="🍏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# If a user is at this page, we assume they are not authenticated
st.session_state['authenticated'] = False

# Initialize session state variables if they don't exist
if 'role' not in st.session_state:
    st.session_state.role = None
if 'first_name' not in st.session_state:
    st.session_state.first_name = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

# Set up navigation
SideBarLinks(st.session_state.role)

# API base URL (would connect to your actual backend)
API_BASE_URL = "http://web-api:4000"

# App header
logger.info("Loading the Home page of the FridgeFriend app")
col1, col2 = st.columns([1, 5])

with col1:
        st.image("assets/logo.png", width=120)

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

# Make API calls for user data (simulated)
try:
    # Student (Ben) data
    student_response = requests.get(f"{API_BASE_URL}/users/auth/student/1")
    if student_response.status_code == 200:
        student_data = student_response.json()
        logger.info("Student API Response: %s", student_data)
        student_firstname = student_data["data"][0]["firstName"]
        student_lastname = student_data["data"][0]["lastName"]
        student_dietary_preferences = student_data["data"][0].get("dietaryPreferences", "Budget-friendly")
        student_id = 1
    else:
        st.error(f"Error: {student_response.status_code}")
        st.code(student_response.text)
        # Fallback data if API call fails
        student_firstname = "Busy"
        student_lastname = "Ben."
        student_dietary_preferences = "Budget-friendly"
        student_id = 1
except Exception as e:
    logger.error(f"Failed to fetch student data: {str(e)}")
    # Fallback data if API call fails
    student_firstname = "Busy"
    student_lastname = "Ben."
    student_dietary_preferences = "Budget-friendly"
    student_id = 1

try:
    # Admin (Alvin) data
    admin_response = requests.get(f"{API_BASE_URL}/users/auth/admin/1")
    if admin_response.status_code == 200:
        admin_data = admin_response.json()
        admin_firstname = admin_data["data"][0]["firstName"]
        admin_lastname = admin_data["data"][0]["lastName"]
        admin_id = 1
    else:
        logger.error(f"Admin API Error: {admin_response.status_code}")
        # Fallback data
        admin_firstname = "Alvin"
        admin_lastname = "Admin."
        admin_id = 1
except Exception as e:
    logger.error(f"Failed to fetch admin data: {str(e)}")
    # Fallback data
    admin_firstname = "Alvin"
    admin_lastname = "Admin."
    admin_id = 1

try:
    # Nutritionist (Nancy) data
    nutritionist_response = requests.get(f"{API_BASE_URL}/users/auth/health/2")
    if nutritionist_response.status_code == 200:
        nutritionist_data = nutritionist_response.json()
        nutritionist_firstname = nutritionist_data["data"][0]["firstName"]
        nutritionist_lastname = nutritionist_data["data"][0]["lastName"]
        nutritionist_id = 1
    else:
        logger.error(f"Nutritionist API Error: {nutritionist_response.status_code}")
        # Fallback data
        nutritionist_firstname = "Nancy"
        nutritionist_lastname = "Nutritionist."
        nutritionist_id = 1
except Exception as e:
    logger.error(f"Failed to fetch nutritionist data: {str(e)}")
    # Fallback data
    nutritionist_firstname = "Nancy"
    nutritionist_lastname = "Nutritionist."
    nutritionist_id = 1

try:
    # Athlete (Riley) data
    athlete_response = requests.get(f"{API_BASE_URL}/users/auth/health/1")
    if athlete_response.status_code == 200:
        athlete_data = athlete_response.json()
        athlete_firstname = athlete_data["data"][0]["firstName"]
        athlete_lastname = athlete_data["data"][0]["lastName"]
        athlete_id = 1
    else:
        logger.error(f"Athlete API Error: {athlete_response.status_code}")
        # Fallback data
        athlete_firstname = "Riley"
        athlete_lastname = "Runner."
        athlete_id = 1
except Exception as e:
    logger.error(f"Failed to fetch athlete data: {str(e)}")
    # Fallback data
    athlete_firstname = "Riley"
    athlete_lastname = "Runner."
    athlete_id = 1
    
# User selection section  
st.markdown("### Select Your Profile")
st.write("Choose a profile to log in and access personalized features.")

col1, col2, col3, col4 = st.columns(4)

# Ben (Student)
with col1:
    st.markdown("#### 🧑‍🎓 Student")
    st.write(f"**Name:** {student_firstname} {student_lastname}")
    st.write("**Focus:** Quick meals & budget tracking")
    st.write(f"**Preferences:** {student_dietary_preferences}")
    
    if st.button("Login as Ben", key="student", use_container_width=True):
        st.session_state.authenticated = True
        st.session_state.role = "busy_student"
        st.session_state.first_name = student_firstname
        st.session_state.user_id = student_id
        logger.info("Logging in as a Student")
            
        st.switch_page("pages/00_Dashboard_Overview.py")

# Alvin (Admin)
with col2:
    st.markdown("#### 👨‍💻 Administrator")
    st.write(f"**Name:** {admin_firstname} {admin_lastname}")
    st.write("**Role:** System management & monitoring")
    st.write("**Access:** Full system access")
    
    if st.button("Login as Alvin", key="admin", use_container_width=True):
        st.session_state.authenticated = True
        st.session_state.role = "admin"
        st.session_state.first_name = admin_firstname
        st.session_state.user_id = admin_id
        logger.info("Logging in as Admin")

            
        st.switch_page("pages/10_Admin_Dashboard.py")

# Nancy (Nutritionist)
with col3:
    st.markdown("#### 👩‍⚕️ Nutritionist")
    st.write(f"**Name:** {nutritionist_firstname} {nutritionist_lastname}")
    st.write("**Role:** Client management & meal planning")
    st.write("**Expertise:** Clinical nutrition & meal planning")
    
    if st.button("Login as Nancy", key="nutritionist", use_container_width=True):
        st.session_state.authenticated = True
        st.session_state.role = "nutritionist"
        st.session_state.first_name = nutritionist_firstname
        st.session_state.user_id = nutritionist_id
        logger.info("Logging in as Nutritionist")
        

            
        st.switch_page("pages/20_Nutritionist_Dashboard.py")

# Riley (Athlete)
with col4:
    st.markdown("#### 🏃‍♀️ Athlete")
    st.write(f"**Name:** {athlete_firstname} {athlete_lastname}")
    st.write("**Focus:** Performance nutrition & tracking")
    st.write("**Goals:** Optimize nutrition for athletic performance")
    
    if st.button("Login as Riley", key="athlete", use_container_width=True):
        st.session_state.authenticated = True
        st.session_state.role = "athlete"
        st.session_state.first_name = athlete_firstname
        st.session_state.user_id = athlete_id
        logger.info("Logging in as Athlete")
        

        st.switch_page("pages/30_Athlete_Dashboard.py")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.caption("© 2025 FridgeFriend | A CS 3200 Project")

with col2:
    st.caption("Northeastern University")

with col3:
    st.caption("Version 2.3.1 | Last Updated: April 12, 2025")


    
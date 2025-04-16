import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from modules.nav import SideBarLinks

API_BASE_URL = "http://web-api:4000"

if not st.session_state.get('authenticated', False) or st.session_state.role != "nutritionist":
    st.warning("Please log in as Nancy to access this page")
    st.stop()

SideBarLinks(st.session_state.role)

@st.cache_data(ttl=300)
def get_users():
    try:
        response = requests.get(f"{API_BASE_URL}/users")
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
        response = requests.get(f"{API_BASE_URL}/users/{user_id}")
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
        response = requests.put(f"{API_BASE_URL}/users/constraints/{pc_id}", json=data)
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
        response = requests.post(f"{API_BASE_URL}/users/constraints", json=data)
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

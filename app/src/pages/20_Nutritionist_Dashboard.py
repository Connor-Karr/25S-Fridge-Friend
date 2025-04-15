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
if not st.session_state.get('authenticated', False) or st.session_state.role != "nutritionist":
    st.warning("Please log in as Nancy to access this page")
    st.stop()

# Set up navigation
SideBarLinks(st.session_state.role)

# Page header
st.title(f"Nutritionist Dashboard")
st.subheader(f"Welcome, {st.session_state.first_name}!")


# Mock client data
clients = [
    {"id": 1, "name": "John D.", "age": 27, "goal": "Weight Loss", "diet": "Low Carb", "allergies": "Peanuts"},
    {"id": 2, "name": "Sarah M.", "age": 34, "goal": "Muscle Gain", "diet": "High Protein", "allergies": "Dairy"},
    {"id": 3, "name": "Michael R.", "age": 42, "goal": "Maintenance", "diet": "Balanced", "allergies": "None"},
    {"id": 4, "name": "Emma L.", "age": 19, "goal": "Performance", "diet": "Keto", "allergies": "Gluten"},
    {"id": 5, "name": "David W.", "age": 55, "goal": "Health", "diet": "Mediterranean", "allergies": "Shellfish"}
]

# Create dashboard layout
col1, col2 = st.columns([2, 1])

# Client overview section
with col1:
    st.subheader("👥 Active Clients")

    for client in clients:
        with st.container():
            col_a, col_b, col_c, col_d, col_e = st.columns([3, 2, 2, 2, 1])

            with col_a:
                st.write(f"**{client['name']}**")
            with col_b:
                st.write(f"Age: {client['age']}")
            with col_c:
                st.write(f"Goal: {client['goal']}")
            with col_d:
                st.write(f"Diet: {client['diet']}")
            with col_e:
                if st.button("View", key=f"view_{client['id']}"):
                    st.session_state.selected_client_id = client['id']
                    st.session_state.selected_client_name = client['name']
                    st.switch_page("pages/21_Client_Management.py")

            st.write("---")

    if st.button("+ Add New Client"):
        st.switch_page("pages/21_Client_Management.py")


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

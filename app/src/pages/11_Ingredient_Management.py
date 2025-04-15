import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime, timedelta
import json
from modules.nav import SideBarLinks

# API base URL
API_BASE_URL = "http://web-api:4000"

# Authentication check
if not st.session_state.get('authenticated', False) or st.session_state.role != "admin":
    st.warning("Please log in as Alvin to access this page")
    st.stop()

# Set up navigation
SideBarLinks(st.session_state.role)

# Page header
st.title("🥕 Ingredient Management")
st.write("Add, update, and manage ingredients and their nutritional data")

# Create tabs for different functions
tab1, tab2, tab3 = st.tabs(["Ingredient Database", "Add New Ingredient", "Update Macros"])

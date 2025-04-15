import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime, timedelta
import json
from modules.nav import SideBarLinks

# API base URL
API_BASE_URL = "http://web-api:4000"

# Authentication check
if not st.session_state.get('authenticated', False) or st.session_state.role != "busy_student":
    st.warning("Please log in as Ben to access this page")
    st.stop()

# Set up navigation
SideBarLinks(st.session_state.role)

# Page header
st.title("🧊 Fridge Inventory")
st.write("Manage your fridge ingredients and keep track of what's in stock")

# Tabs for different views
tab1, tab2, tab3 = st.tabs(["Current Inventory", "Add Items", "Remove Expired"])

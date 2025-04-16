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

# Page header
st.title("📈 Nutrition Analytics")
st.write("Analyze nutritional data across clients and identify trends")

# Mock client data
clients = [
    {"id": 1, "name": "John D.", "age": 27, "goal": "Weight Loss", "diet": "Low Carb"},
    {"id": 2, "name": "Sarah M.", "age": 34, "goal": "Muscle Gain", "diet": "High Protein"},
    {"id": 3, "name": "Michael R.", "age": 42, "goal": "Maintenance", "diet": "Balanced"},
    {"id": 4, "name": "Emma L.", "age": 19, "goal": "Performance", "diet": "Keto"},
    {"id": 5, "name": "David W.", "age": 55, "goal": "Health", "diet": "Mediterranean"}
]

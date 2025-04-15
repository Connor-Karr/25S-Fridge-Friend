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
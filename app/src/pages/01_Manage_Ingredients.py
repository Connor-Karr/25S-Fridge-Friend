import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from modules.nav import SideBarLinks

# sidebar + auth
SideBarLinks(st.session_state.role)
if not st.session_state.get('authenticated', False) or st.session_state.role != "busy_student":
    st.warning("Please log in as Ben to access this page")
    st.stop()

API_BASE_URL = "http://web-api:4000"

st.title("Fridge Inventory")

# show all ingredients 
st.subheader("Your Ingredients")

try:
    response = requests.get(f"{API_BASE_URL}/ingredients")
    if response.status_code == 200:
        ingredients = response.json()
        df = pd.DataFrame(ingredients)
        st.dataframe(df)
    else:
        st.error("Failed to fetch ingredients.")
except Exception as e:
    st.error(f"Error: {str(e)}")


# form to add ingredient
st.subheader("Add New Ingredient")

with st.form("add_ingredient_form"):
    name = st.text_input("Ingredient Name")
    expiration_date = st.date_input("Expiration Date")
    submitted = st.form_submit_button("Add Ingredient")

    if submitted:
        try:
            payload = {
                "name": name,
                "expiration_date": expiration_date.strftime("%Y-%m-%d")
            }

            response = requests.post(f"{API_BASE_URL}/ingredients/add", json=payload)

            if response.status_code == 201:
                st.success("Ingredient added successfully!")
                st.rerun()
            else:
                st.error("Failed to add ingredient.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

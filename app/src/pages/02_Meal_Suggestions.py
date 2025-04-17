import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

# sidebar + auth
SideBarLinks(st.session_state.role)
if not st.session_state.get('authenticated', False) or st.session_state.role != "busy_student":
    st.warning("please log in as ben to access this page")
    st.stop()

API_BASE_URL = "http://web-api:4000"

st.title("macronutrient dashboard")

# full macro table 
st.subheader("all your ingredient macros")

try:
    response = requests.get(f"{API_BASE_URL}/macronutrients")
    if response.status_code == 200:
        macros = response.json()
        if macros:
            df = pd.DataFrame(macros)

            # reordering columns
            preferred_order = ['ingredient_id', 'ingredient_name'] + [col for col in df.columns if col not in ['ingredient_id', 'ingredient_name']]
            df = df[preferred_order]

            st.dataframe(df)

            # top protein 
            st.subheader("your highest protein ingredients")
            top_protein = df.sort_values(by='protein', ascending=False)
            st.dataframe(top_protein[['ingredient_name', 'protein']])

            # top fiber 
            st.subheader("your highest fiber ingredients")
            top_fiber = df.sort_values(by='fiber', ascending=False)
            st.dataframe(top_fiber[['ingredient_name', 'fiber']])

            # top vitamins
            st.subheader("your highest vitamin ingredients")
            top_vitamin = df.sort_values(by='vitamin', ascending=False)
            st.dataframe(top_vitamin[['ingredient_name', 'vitamin']])
        else:
            st.info("no macronutrient data found.")
    else:
        st.error(f"failed to fetch macronutrients: {response.status_code}")
except Exception as e:
    st.error(f"error: {str(e)}")

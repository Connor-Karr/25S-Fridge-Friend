import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
from modules.nav import SideBarLinks

# sidebar + auth
SideBarLinks(st.session_state.role)
if not st.session_state.get('authenticated', False) or st.session_state.role != "busy_student":
    st.warning("Please log in as Ben to access this page")
    st.stop()

API_BASE_URL = "http://web-api:4000"

st.title("Busy Ben's Dashboard")

# ----------- expiring soon (within 1 month) -----------
st.subheader("Expiring in the Next 30 Days!")

try:
    response = requests.get(f"{API_BASE_URL}/ingredients")
    if response.status_code == 200:
        items = response.json()
        df = pd.DataFrame(items)
        df['expiration_date'] = pd.to_datetime(df['expiration_date'])
        today = pd.to_datetime("2025-04-17")
        cutoff = today + timedelta(days=30)
        expiring = df[(df['expiration_date'] >= today) & (df['expiration_date'] <= cutoff)]
        expiring_sorted = expiring.sort_values(by='expiration_date')

        if not expiring_sorted.empty:
            st.dataframe(expiring_sorted[['name', 'expiration_date']], use_container_width=True)
        else:
            st.success("No ingredients expiring in the next 30 days!")
    else:
        st.error("Could not fetch expiring items.")
except Exception as e:
    st.error(f"Error fetching expiring items: {str(e)}")

# ----------- macro snapshot -----------
st.subheader("Macros Snapshot")

try:
    response = requests.get(f"{API_BASE_URL}/macronutrients")
    if response.status_code == 200:
        macros = response.json()
        df = pd.DataFrame(macros)

        # top 3 for each macro
        top_protein = df[['ingredient_name', 'protein']].sort_values(by='protein', ascending=False).head(3)
        top_fiber = df[['ingredient_name', 'fiber']].sort_values(by='fiber', ascending=False).head(3)
        top_vitamin = df[['ingredient_name', 'vitamin']].sort_values(by='vitamin', ascending=False).head(3)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.caption("Protein")
            st.dataframe(top_protein, hide_index=True, use_container_width=True)
        with col2:
            st.caption("Fiber")
            st.dataframe(top_fiber, hide_index=True, use_container_width=True)
        with col3:
            st.caption("Vitamin")
            st.dataframe(top_vitamin, hide_index=True, use_container_width=True)
    else:
        st.error("Failed to load macronutrients.")
except Exception as e:
    st.error(f"Error: {str(e)}")

# ----------- leftovers summary (counts only) -----------
st.subheader("Leftovers Snapshot")

try:
    response = requests.get(f"{API_BASE_URL}/leftovers")
    if response.status_code == 200:
        leftovers = response.json()
        df = pd.DataFrame(leftovers)
        fresh_count = df[df["is_expired"] == 0].shape[0]
        spoiled_count = df[df["is_expired"] == 1].shape[0]

        st.write(f"Fresh Leftovers: **{fresh_count}**")
        st.write(f"Spoiled Leftovers: **{spoiled_count}**")
    else:
        st.error("Failed to fetch leftovers.")
except Exception as e:
    st.error(f"Error: {str(e)}")

# ----------- budget overview (hardcoded) -----------
st.subheader("Budget Overview")

total_budget = 140.35
used = 27.45
remaining = total_budget - used

budget_df = pd.DataFrame({
    'Category': ['Total', 'Used', 'Remaining'],
    'Amount': [f"${total_budget:.2f}", f"${used:.2f}", f"${remaining:.2f}"]
})

st.dataframe(budget_df, hide_index=True, use_container_width=True)

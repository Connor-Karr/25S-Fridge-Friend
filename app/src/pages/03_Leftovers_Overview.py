import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

# sidebar + auth
SideBarLinks(st.session_state.role)
if not st.session_state.get('authenticated', False) or st.session_state.role != "busy_student":
    st.warning("Please log in as Ben to access this page")
    st.stop()

API_BASE_URL = "http://web-api:4000"

st.title("Leftovers Tracker")

try:
    response = requests.get(f"{API_BASE_URL}/leftovers")
    if response.status_code == 200:
        leftovers = response.json()

        if not leftovers:
            st.info("You have no leftovers right now.")
        else:
            df = pd.DataFrame(leftovers)
            df = df.rename(columns={"recipe_name": "name"}) if "recipe_name" in df.columns else df
            df_filtered = df[["is_expired", "name", "quantity"]]

            # Still Good
            still_good = df_filtered[df_filtered["is_expired"] == 0]
            st.subheader("Still Good to Eat!")
            if not still_good.empty:
                st.dataframe(still_good)
            else:
                st.success("You have no fresh leftovers.")

            # Time to Toss
            expired = df_filtered[df_filtered["is_expired"] == 1]
            st.subheader("Time to Throw Away!")
            if not expired.empty:
                st.dataframe(expired)
            else:
                st.info("No spoiled leftovers. Nice job!")
    else:
        st.error("Failed to fetch leftovers.")
except Exception as e:
    st.error(f"Error: {str(e)}")

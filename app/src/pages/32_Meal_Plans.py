import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

# Auth check
if not st.session_state.get('authenticated', False) or st.session_state.role != "athlete":
    st.warning("Please log in as Riley to access this page")
    st.stop()

SideBarLinks(st.session_state.role)

st.title("🍽️ Athlete Meal Plans")
st.write("Manage and view your personalized meal plans")

API_BASE_URL = "http://localhost:4000"  # LOCAL testing only
CLIENT_ID = st.session_state.get("client_id", 11)

# Helpers
def get_data(endpoint, params=None):
    try:
        res = requests.get(f"{API_BASE_URL}/{endpoint}", params=params)
        if res.status_code == 200:
            return res.json()
        st.error(f"Failed to fetch {endpoint}: Status {res.status_code}")
        return []
    except Exception as e:
        st.error(f"Connection error for {endpoint}: {e}")
        return []

def send_data(method, endpoint, payload=None):
    try:
        url = f"{API_BASE_URL}/{endpoint}"
        if method == "POST":
            return requests.post(url, json=payload)
        elif method == "PUT":
            return requests.put(url, json=payload)
        elif method == "DELETE":
            return requests.delete(url)
    except Exception as e:
        st.error(f"{method} request failed: {e}")
        return None


meal_plans = get_data("meal-plans", {"client_id": CLIENT_ID})
leftovers = get_data("leftovers", {"client_id": CLIENT_ID})

# Tabs
tab1, tab2, tab3 = st.tabs(["Current Plans", "Leftovers", "Update/Delete"])

# === Tab 1: Current Plans ===
with tab1:
    st.subheader("📋 Current Meal Plans")
    if meal_plans:
        st.dataframe(pd.DataFrame(meal_plans), use_container_width=True)
    else:
        st.info("No meal plans found.")

# === Tab 2: Leftovers ===
with tab2:
    st.subheader("🥡 Available Leftovers")
    if leftovers:
        st.dataframe(pd.DataFrame(leftovers), use_container_width=True)

        st.markdown("**❌ Delete a Leftover**")
        leftover_ids = [str(l['leftover_id']) for l in leftovers]
        selected = st.selectbox("Choose a leftover ID to delete", leftover_ids)
        if st.button("Delete Leftover"):
            res = send_data("DELETE", f"leftovers/{selected}")
            if res and res.status_code == 200:
                st.success("Leftover deleted.")
                st.rerun()
            else:
                st.error("Failed to delete leftover.")
    else:
        st.info("No leftovers found.")

# === Tab 3: Update/Delete ===
with tab3:
    st.subheader("📝 Update or Delete a Meal Plan")
    if meal_plans:
        meal_ids = {f"{m['meal_id']} - {m['recipe_name']}": m["meal_id"] for m in meal_plans}
        selected_meal = st.selectbox("Select Meal Plan", list(meal_ids.keys()))

        col1, col2 = st.columns(2)

        with col1:
            new_quantity = st.number_input("New Quantity", min_value=1, value=1)
            if st.button("Update Quantity"):
                res = send_data("PUT", f"meal-plans/{meal_ids[selected_meal]}", {"quantity": new_quantity})
                if res and res.status_code == 200:
                    st.success("Meal plan updated.")
                    st.rerun()
                else:
                    st.error("Update failed.")

        with col2:
            if st.button("Delete Meal Plan"):
                res = send_data("DELETE", f"meal-plans/{meal_ids[selected_meal]}")
                if res and res.status_code == 200:
                    st.success("Meal plan deleted.")
                    st.rerun()
                else:
                    st.error("Deletion failed.")
    else:
        st.info("No meal plans found.")

import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime
from modules.nav import SideBarLinks

SideBarLinks(st.session_state.role)

st.title(f"Welcome, {st.session_state.first_name}! 👋")
st.write("Manage your fridge, plan meals, and stay on budget!")

col1, col2 = st.columns(2)

with col1:
    st.subheader("⚠️ Expiring Soon")

    @st.cache_data(ttl=300)
    def get_expiring_items():
        try:
            response = requests.get(f"{API_BASE_URL}/fridge?client_id=1")
            if response.status_code != 200:
                st.error(f"Error fetching data: {response.status_code}")
                return []

            data = response.json()
            today = datetime.now().date()
            expiring_soon = []

            for item in data:
                if item.get('expiration_date'):
                    exp_date = datetime.strptime(item['expiration_date'], '%Y-%m-%d').date()
                    days_left = (exp_date - today).days

                    if 0 <= days_left <= 5 and not item.get('is_expired', False):
                        expiring_soon.append({
                            'name': item['name'],
                            'days_left': days_left,
                            'quantity': item.get('quantity', 1)
                        })
            return expiring_soon
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return []

    expiring_items = get_expiring_items()

    if expiring_items:
        for item in expiring_items:
            msg = f"{item['name']} - Expires in {item['days_left']} days ({item['quantity']} remaining)"
            if item['days_left'] == 0:
                st.error(f"⚠️ {item['name']} - Expires today! ({item['quantity']} remaining)")
            elif item['days_left'] == 1:
                st.warning(f"⚠️ {item['name']} - Expires tomorrow ({item['quantity']} remaining)")
            else:
                st.info(f"ℹ️ {msg}")
    else:
        st.success("No items expiring soon! Your fridge is in good shape.")

    if st.button("Update Expired Status"):
        try:
            response = requests.put(f"{API_BASE_URL}/fridge/expired")
            if response.status_code == 200:
                st.success("Updated expired item status!")
                st.cache_data.clear()
                time.sleep(1)
                st.rerun()
            else:
                st.error(f"Error updating expired status: {response.status_code}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
            
with col2:
    st.subheader("🍲 Quick Meal Ideas")

    @st.cache_data(ttl=300)
    def get_meal_suggestions():
        try:
            response = requests.get(f"{API_BASE_URL}/meal-plans?client_id=1")
            if response.status_code != 200:
                st.error(f"Error fetching meal suggestions: {response.status_code}")
                return []
            data = response.json()
            return [
                {
                    'name': meal.get('recipe_name', 'Unknown Recipe'),
                    'meal_id': meal.get('meal_id'),
                    'quantity': meal.get('quantity', 1)
                } for meal in data
            ]
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return []

    meal_suggestions = get_meal_suggestions()

    if meal_suggestions:
        for i, meal in enumerate(meal_suggestions[:3]):
            st.write(f"**{meal['name']}** (makes {meal['quantity']} servings)")
            col1a, col1b = st.columns([3, 1])

            with col1a:
                if st.button(f"See Recipe #{i+1}", key=f"recipe_{i}"):
                    st.session_state.selected_meal_id = meal['meal_id']
                    st.switch_page("pages/02_Meal_Suggestions.py")

            with col1b:
                if st.button(f"Save as Leftover #{i+1}", key=f"leftover_{i}"):
                    try:
                        leftover_data = {'recipe_id': meal['meal_id'], 'quantity': 1}
                        response = requests.post(f"{API_BASE_URL}/leftovers", json=leftover_data)

                        if response.status_code == 201:
                            st.success(f"Saved {meal['name']} as leftover!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(f"Error saving leftover: {response.status_code}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    else:
        st.info("No meal suggestions available. Add ingredients to your fridge!")

    if st.button("See All Meal Suggestions"):
        st.switch_page("pages/02_Meal_Suggestions.py")

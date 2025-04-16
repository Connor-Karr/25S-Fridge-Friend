import streamlit as st
import requests
from datetime import datetime, timedelta
from modules.nav import SideBarLinks

# Set up navigation
SideBarLinks(st.session_state.role)

# Authentication check
if not st.session_state.get('authenticated', False) or st.session_state.role != "busy_student":
    st.warning("Please log in as Ben to access this page")
    st.stop()

st.title("Fridge Inventory")
st.write("Manage your fridge ingredients")

# Create tabs
tab1, tab2, tab3 = st.tabs(["Current Inventory", "Add Items", "Remove Expired"])

# Current Inventory Tab
with tab1:
    st.subheader("Current Fridge Contents")
    
    # Get inventory data
    try:
        response = requests.get("http://web-api:4000/fridge?client_id=1")
        if response.status_code == 200:
            items = response.json()
            
            if items:
                # Display items in simple format
                for item in items:
                    st.write(f"{item['name']} - Quantity: {item.get('quantity', 1)}")
                
                st.write(f"Total items: {len(items)}")
            else:
                st.info("Your fridge is empty!")
        else:
            st.error("Error loading inventory")
    except:
        st.error("Error loading inventory")
    
    if st.button("Refresh"):
        st.rerun()

# Add Items Tab
with tab2:
    st.subheader("Add New Items")
    
    # Get available ingredients
    try:
        response = requests.get("http://web-api:4000/ingredients")
        if response.status_code == 200:
            ingredients = response.json()
            
            # Create ingredient dropdown
            names = [ing.get('name', 'Unknown') for ing in ingredients]
            selected = st.selectbox("Select ingredient:", names)
            
            # Get ID of selected ingredient
            ingredient_id = None
            for ing in ingredients:
                if ing.get('name') == selected:
                    ingredient_id = ing.get('ingredient_id')
            
            # Quantity input
            quantity = st.number_input("Quantity:", min_value=0.1, value=1.0, step=0.1)
            
            # Add button
            if st.button("Add to Fridge"):
                if ingredient_id:
                    data = {'fridge_id': 1, 'quantity': quantity}
                    response = requests.post(f"http://web-api:4000/fridge/{ingredient_id}", json=data)
                    
                    if response.status_code == 201:
                        st.success(f"Added {selected} to fridge!")
                    else:
                        st.error("Error adding item")
        else:
            st.error("Error loading ingredients")
    except:
        st.error("Error loading ingredients")
    
    # Add custom ingredient
    st.subheader("Add Custom Ingredient")
    name = st.text_input("Name:")
    exp_date = st.date_input("Expiration date:", value=datetime.now().date() + timedelta(days=7))
    qty = st.number_input("Quantity:", min_value=0.1, value=1.0, step=0.1, key="custom_qty")
    
    if st.button("Add Custom"):
        if name:
            # Add new ingredient
            ingredient_data = {'name': name, 'expiration_date': exp_date.strftime('%Y-%m-%d')}
            resp1 = requests.post("http://web-api:4000/ingredients", json=ingredient_data)
            
            if resp1.status_code == 201:
                # Add to fridge
                ing_id = resp1.json().get('ingredient_id')
                fridge_data = {'fridge_id': 1, 'quantity': qty}
                resp2 = requests.post(f"http://web-api:4000/fridge/{ing_id}", json=fridge_data)
                
                if resp2.status_code == 201:
                    st.success(f"Added {name} to fridge!")
                else:
                    st.error("Error adding to fridge")
            else:
                st.error("Error creating ingredient")

# Remove Expired Tab
with tab3:
    st.subheader("Remove Expired Items")
    
    # Get expired items
    try:
        response = requests.get("http://web-api:4000/fridge?client_id=1")
        if response.status_code == 200:
            items = response.json()
            today = datetime.now().date()
            expired = []
            
            # Find expired items
            for item in items:
                if item.get('expiration_date'):
                    try:
                        exp_date = datetime.strptime(item['expiration_date'], '%Y-%m-%d').date()
                        if exp_date < today:
                            expired.append(item['name'])
                    except:
                        pass
            
            # Display expired items
            if expired:
                st.write(f"Expired items ({len(expired)}):")
                for name in expired:
                    st.write(f"• {name}")
                
                # Remove button
                if st.button("Remove All Expired"):
                    response = requests.delete("http://web-api:4000/fridge/expired")
                    if response.status_code == 200:
                        st.success("Expired items removed!")
                        st.rerun()
                    else:
                        st.error("Error removing items")
            else:
                st.success("No expired items!")
        else:
            st.error("Error loading inventory")
    except:
        st.error("Error loading inventory")
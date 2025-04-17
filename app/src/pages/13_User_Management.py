import streamlit as st
import pandas as pd
import requests
import time
from modules.nav import SideBarLinks

if not st.session_state.get('authenticated', False) or st.session_state.role != "admin":
    st.warning("Please log in as Alvin to access this page")
    st.stop()

SideBarLinks(st.session_state.role)

st.title("👤 User Management")
st.write("Manage user accounts and roles")

def get_users():
    try:
        response = requests.get("http://web-api:4000/users/")
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            st.error(f"Error fetching users: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []
    
def get_user_details(user_id):
    try:
        response = requests.get(f"http://web-api:4000/users/{user_id}")
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            st.error(f"Error fetching user details: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None
    
def update_user(user_id, data):
    try:
        response = requests.put(f"http://web-api:4000/users/{user_id}", json=data)
        
        if response.status_code == 200:
            return True
        else:
            st.error(f"Error updating user: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False
    
# Fetch users from the API
users = get_users()

# Determine role based on user_id ranges
for user in users:
    if "role" not in user:
        if user["user_id"] >= 1 and user["user_id"] <= 10:
            user["role"] = "client"
        elif user["user_id"] >= 11 and user["user_id"] <= 20:
            user["role"] = "admin"
        elif user["user_id"] >= 21:
            user["role"] = "health_advisor"

tab1, tab2 = st.tabs(["User Accounts", "Create User"])

with tab1:
    st.subheader("User Accounts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        search_term = st.text_input("Search users:", placeholder="Name, email, or username...")
    
    with col2:
        role_filter = st.selectbox(
            "Filter by role:",
            ["All", "client", "admin", "health_advisor"]
        )
    
    filtered_users = users
    
    if search_term:
        filtered_users = [
            user for user in filtered_users
            if (search_term.lower() in user.get('f_name', '').lower() or
                search_term.lower() in user.get('l_name', '').lower() or
                search_term.lower() in user.get('username', '').lower() or
                search_term.lower() in user.get('email', '').lower())
        ]
    
    if role_filter != "All":
        filtered_users = [
            user for user in filtered_users
            if user.get('role', '') == role_filter
        ]
    
    st.write(f"Showing {len(filtered_users)} users")
    
    if filtered_users:
        user_df = pd.DataFrame([
            {
                "ID": user.get('user_id'),
                "Name": f"{user.get('f_name', '')} {user.get('l_name', '')}",
                "Username": user.get('username', ''),
                "Email": user.get('email', ''),
                "Role": user.get('role', '')
            }
            for user in filtered_users
        ])
        
        st.table(user_df)

        selected_user_id = st.selectbox(
            "Select user to edit:",
            options=[user.get('user_id') for user in filtered_users],
            format_func=lambda x: f"{next((u['f_name'] + ' ' + u['l_name'] for u in filtered_users if u['user_id'] == x), '')} ({x})"
        )
        
        if selected_user_id:
            st.session_state.selected_user_id = selected_user_id
            selected_user = next((u for u in filtered_users if u['user_id'] == selected_user_id), None)
            
            if selected_user:
                with st.form("edit_user_form"):
                    st.subheader("Edit User")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        new_first_name = st.text_input("First Name:", value=selected_user.get('f_name', ''))
                        new_last_name = st.text_input("Last Name:", value=selected_user.get('l_name', ''))
                    
                    with col2:
                        new_email = st.text_input("Email:", value=selected_user.get('email', ''))
                        new_username = st.text_input("Username:", value=selected_user.get('username', ''))
                    
                    submit_button = st.form_submit_button("Update User")
                    
                    if submit_button:
                        update_data = {
                            'f_name': new_first_name,
                            'l_name': new_last_name,
                            'username': new_username,
                            'email': new_email
                        }
                        
                        success = update_user(selected_user_id, update_data)
                        
                        if success:
                            st.success("User updated successfully!")
                            st.cache_data.clear()
                            time.sleep(1)
                            st.rerun()
    else:
        st.info("No users found matching your search criteria.")

with tab2:
    st.subheader("Create New User")
    
    with st.form("create_user_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_first_name = st.text_input("First Name:")
            new_last_name = st.text_input("Last Name:")
            new_username = st.text_input("Username:")
        
        with col2:
            new_email = st.text_input("Email:")
            new_password = st.text_input("Password:", type="password")
        
        submit_button = st.form_submit_button("Create User")
        
        if submit_button and all([new_first_name, new_last_name, new_username, new_password, new_email]):
            new_user_data = {
                'f_name': new_first_name,
                'l_name': new_last_name,
                'username': new_username,
                'password': new_password,
                'email': new_email
            }
            
            try:
                response = requests.post("http://web-api:4000/users/", json=new_user_data)
                
                if response.status_code == 201:
                    st.success(f"User {new_username} created successfully!")
                    st.cache_data.clear()
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"Error creating user: {response.status_code}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Display simple user statistics
st.subheader("User Statistics")

role_counts = {}
for user in users:
    role = user.get('role', 'unknown')
    if role in role_counts:
        role_counts[role] += 1
    else:
        role_counts[role] = 1

stat_cols = st.columns(len(role_counts) + 1)
with stat_cols[0]:
    st.metric("Total Users", len(users))

idx = 1
for role, count in role_counts.items():
    with stat_cols[idx]:
        st.metric(f"{role.capitalize()}", count)
    idx += 1
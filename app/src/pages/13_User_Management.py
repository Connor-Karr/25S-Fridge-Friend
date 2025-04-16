import streamlit as st

from modules.nav import SideBarLinks

API_BASE_URL = "http://web-api:4000"
if not st.session_state.get('authenticated', False) or st.session_state.role != "admin":
    st.warning("Please log in as Alvin to access this page")
    st.stop()

SideBarLinks(st.session_state.role)

st.title("👤 User Management")
st.write("Manage user accounts, roles, and permissions")

@st.cache_data(ttl=300)
def get_users():
    try:
        response = requests.get(f"{API_BASE_URL}/users")
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            st.error(f"Error fetching users: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []
    
@st.cache_data(ttl=300)
def get_user_details(user_id):
    try:
        response = requests.get(f"{API_BASE_URL}/users/{user_id}")
        
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
        response = requests.put(f"{API_BASE_URL}/users/{user_id}", json=data)
        
        if response.status_code == 200:
            return True
        else:
            st.error(f"Error updating user: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False
    

users = get_users()

if not users:
    users = [
        {"user_id": 1, "f_name": "John", "l_name": "Doe", "username": "johndoe", "email": "john.doe@example.com", "role": "client", "status": "active"},
        {"user_id": 2, "f_name": "Jane", "l_name": "Smith", "username": "janesmith", "email": "jane.smith@example.com", "role": "client", "status": "active"},
        {"user_id": 3, "f_name": "Bob", "l_name": "Johnson", "username": "bjohnson", "email": "bob.johnson@example.com", "role": "client", "status": "inactive"},
        {"user_id": 4, "f_name": "Sarah", "l_name": "Williams", "username": "swilliams", "email": "sarah.williams@example.com", "role": "nutritionist", "status": "active"},
        {"user_id": 5, "f_name": "Mike", "l_name": "Brown", "username": "mbrown", "email": "mike.brown@example.com", "role": "admin", "status": "active"},
        {"user_id": 6, "f_name": "Test", "l_name": "User", "username": "testuser", "email": "test@example.com", "role": "client", "status": "test"}
    ]

tab1, tab2, tab3 = st.tabs(["User Accounts", "Account Management", "System Stats"])


with tab1:
    st.subheader("User Accounts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        search_term = st.text_input("Search users:", placeholder="Name, email, or username...")
    
    with col2:
        status_filter = st.selectbox(
            "Filter by status:",
            ["All", "Active", "Inactive", "Test"]
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
    
    if status_filter != "All":
        filtered_users = [
            user for user in filtered_users
            if user.get('status', '').lower() == status_filter.lower()
        ]
    
    st.write(f"Showing {len(filtered_users)} users")
    
    if filtered_users:
        user_df = pd.DataFrame([
            {
                "ID": user.get('user_id'),
                "Name": f"{user.get('f_name', '')} {user.get('l_name', '')}",
                "Username": user.get('username', ''),
                "Email": user.get('email', ''),
                "Role": user.get('role', '').capitalize(),
                "Status": user.get('status', '').capitalize()
            }
            for user in filtered_users
        ])
        
        def highlight_status(val):
            if val == "Active":
                return 'background-color: #CCFFCC'
            elif val == "Inactive":
                return 'background-color: #FFCCCC'
            elif val == "Test":
                return 'background-color: #FFFFCC'
            return ''
        
        st.dataframe(
            user_df.style.applymap(highlight_status, subset=['Status']),
            column_config={
                "ID": st.column_config.NumberColumn("ID", width="small"),
                "Name": st.column_config.TextColumn("Name"),
                "Username": st.column_config.TextColumn("Username"),
                "Email": st.column_config.TextColumn("Email"),
                "Role": st.column_config.TextColumn("Role"),
                "Status": st.column_config.TextColumn("Status", width="small")
            },
            use_container_width=True,
            height=400
        )

        selected_user_id = st.selectbox(
            "Select user to manage:",
            options=[user.get('user_id') for user in filtered_users],
            format_func=lambda x: f"{next((u['f_name'] + ' ' + u['l_name'] for u in filtered_users if u['user_id'] == x), '')} ({x})"
        )
        
        if selected_user_id:
            st.session_state.selected_user_id = selected_user_id
            
            selected_user = next((u for u in filtered_users if u['user_id'] == selected_user_id), None)
            
            if selected_user:
                with st.expander("User Details", expanded=True):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**ID:** {selected_user.get('user_id')}")
                        st.write(f"**Name:** {selected_user.get('f_name')} {selected_user.get('l_name')}")
                        st.write(f"**Username:** {selected_user.get('username')}")
                    
                    with col2:
                        st.write(f"**Email:** {selected_user.get('email')}")
                        st.write(f"**Role:** {selected_user.get('role', '').capitalize()}")
                        st.write(f"**Status:** {selected_user.get('status', '').capitalize()}")
                    st.write("**Actions:**")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button("Edit User"):
                            st.session_state.edit_user = True
                            st.session_state.edit_user_id = selected_user_id
                    
                    with col2:
                        if selected_user.get('status') == 'active':
                            if st.button("Mark as Inactive"):
                                with st.spinner("Updating user status..."):
                                    update_data = {
                                        'status': 'inactive'
                                    }
                                    
                                    success = update_user(selected_user_id, update_data)
                                    
                                    if success:
                                        st.success("User marked as inactive successfully!")
                                        st.cache_data.clear()
                                        time.sleep(1)
                                        st.rerun()
                                    else:
                                        st.success("User marked as inactive successfully! (Mock)")
                                        time.sleep(1)
                                        st.rerun()
                        else:
                            if st.button("Mark as Active"):
                                with st.spinner("Updating user status..."):
                                    update_data = {
                                        'status': 'active'
                                    }
                                    
                                    success = update_user(selected_user_id, update_data)
                                    
                                    if success:
                                        st.success("User marked as active successfully!")
                                        st.cache_data.clear()
                                        time.sleep(1)
                                        st.rerun()
                                    else:
                                        st.success("User marked as active successfully! (Mock)")
                                        time.sleep(1)
                                        st.rerun()
                    
                    with col3:
                        if selected_user.get('status') == 'test':
                            if st.button("Remove Test User"):
                                with st.spinner("Removing test user..."):
                                    time.sleep(1)
                                    st.success("Test user removed successfully! (Mock)")
                                    time.sleep(1)
                                    st.rerun()
                
                if st.session_state.get('edit_user', False) and st.session_state.get('edit_user_id') == selected_user_id:
                    st.subheader("Edit User")
                    
                    with st.form("edit_user_form"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            new_first_name = st.text_input("First Name:", value=selected_user.get('f_name', ''))
                            new_last_name = st.text_input("Last Name:", value=selected_user.get('l_name', ''))
                            new_username = st.text_input("Username:", value=selected_user.get('username', ''))
                        
                        with col2:
                            new_email = st.text_input("Email:", value=selected_user.get('email', ''))
                            new_role = st.selectbox(
                                "Role:",
                                ["client", "nutritionist", "admin"],
                                index=["client", "nutritionist", "admin"].index(selected_user.get('role', 'client')) if selected_user.get('role') in ["client", "nutritionist", "admin"] else 0
                            )
                            new_status = st.selectbox(
                                "Status:",
                                ["active", "inactive", "test"],
                                index=["active", "inactive", "test"].index(selected_user.get('status', 'active')) if selected_user.get('status') in ["active", "inactive", "test"] else 0
                            )
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            submit_button = st.form_submit_button("Save Changes")
                        
                        with col2:
                            cancel_button = st.form_submit_button("Cancel")
                        
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
                                st.session_state.edit_user = False
                                st.session_state.edit_user_id = None
                                st.cache_data.clear()
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.success("User updated successfully! (Mock)")
                                st.session_state.edit_user = False
                                st.session_state.edit_user_id = None
                                time.sleep(1)
                                st.rerun()
                        
                        if cancel_button:
                            st.session_state.edit_user = False
                            st.session_state.edit_user_id = None
                            st.rerun()
    else:
        st.info("No users found matching your search criteria.")

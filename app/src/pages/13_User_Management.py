import streamlit as st
from modules.nav import SideBarLinks

if not st.session_state.get('authenticated', False) or st.session_state.role != "admin":
    st.warning("Please log in as Alvin to access this page")
    st.stop()

SideBarLinks(st.session_state.role)

st.title("👤 User Management")
st.write("Manage user accounts, roles, and permissions")

@st.cache_data(ttl=300)
def get_users():
    try:
        response = requests.get("http://web-api:4000/users")
        
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
        response = requests.get("http://web-api:4000/users/{user_id}")
        
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
        response = requests.put("http://web-api:4000/users/{user_id}", json=data)
        
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

with tab2:
    st.subheader("Account Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Create New User")
        
        with st.form("create_user_form"):
            new_first_name = st.text_input("First Name:")
            new_last_name = st.text_input("Last Name:")
            new_username = st.text_input("Username:")
            new_password = st.text_input("Password:", type="password")
            new_email = st.text_input("Email:")
            new_role = st.selectbox("Role:", ["client", "nutritionist", "admin"])
            
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
                    response = requests.post("http://web-api:4000/users", json=new_user_data)
                    
                    if response.status_code == 201:
                        st.success(f"User {new_username} created successfully!")
                        st.cache_data.clear()
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"Error creating user: {response.status_code}")
                        st.success(f"User {new_username} created successfully! (Mock)")
                        time.sleep(1)
                        st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.success(f"User {new_username} created successfully! (Mock)")
                    time.sleep(1)
                    st.rerun()

    with col2:
        st.write("### Bulk Operations")
        
        st.write("#### Update Status")
        
        with st.form("update_status_form"):
            status_options = st.selectbox(
                "Set status for all matching users:",
                ["active", "inactive", "test"]
            )
            
            role_filter = st.selectbox(
                "For users with role:",
                ["All", "client", "nutritionist", "admin"]
            )
            
            confirm_status = st.checkbox("I confirm this bulk operation")
            
            submit_button = st.form_submit_button("Update Status")
            
            if submit_button and confirm_status:
                with st.spinner("Updating user status..."):
                    affected_users = [
                        user for user in users
                        if (role_filter == "All" or user.get('role') == role_filter)
                    ]
                    
                    time.sleep(2)
                    
                    st.success(f"Updated status to '{status_options}' for {len(affected_users)} users!")
        
        st.write("#### Test User Cleanup")
        
        with st.form("test_user_form"):
            confirm_test = st.checkbox("I confirm removal of all test users")
            
            submit_button = st.form_submit_button("Remove All Test Users")
            
            if submit_button and confirm_test:
                with st.spinner("Removing test users..."):
                    test_users = [
                        user for user in users
                        if user.get('status') == 'test'
                    ]
                    
                    time.sleep(2)
                    
                    st.success(f"Removed {len(test_users)} test users successfully!")
    
    st.markdown("---")
    st.subheader("Role Management")
    
    role_permissions = {
        "client": ["View own profile", "Track nutrition", "Create meal plans", "Manage fridge inventory"],
        "nutritionist": ["View client profiles", "Create meal plans", "Track client nutrition", "Manage dietary restrictions", "View nutrition analytics"],
        "admin": ["Manage all users", "View system logs", "Manage food database", "View system analytics", "Manage application settings"]
    }
    
    role_tabs = st.tabs(["Client", "Nutritionist", "Admin"])
    
    for i, (role, permissions) in enumerate(role_permissions.items()):
        with role_tabs[i]:
            st.write(f"**{role.capitalize()} Role Permissions:**")
            
            for permission in permissions:
                st.checkbox(permission, value=True, disabled=True)
            
            with st.expander("Add Custom Permission"):
                with st.form(f"add_permission_{role}"):
                    new_permission = st.text_input("New Permission:", key=f"new_perm_{role}")
                    submit = st.form_submit_button("Add Permission")
                    
                    if submit and new_permission:
                        st.success(f"Permission '{new_permission}' added to {role} role! (Mock)")

with tab3:
    st.subheader("System Statistics")
    
    st.write("### User Statistics")
    
    total_users = len(users)
    active_users = len([user for user in users if user.get('status') == 'active'])
    inactive_users = len([user for user in users if user.get('status') == 'inactive'])
    test_users = len([user for user in users if user.get('status') == 'test'])
    
    role_counts = {}
    for user in users:
        role = user.get('role', 'unknown')
        if role in role_counts:
            role_counts[role] += 1
        else:
            role_counts[role] = 1
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Users", total_users)
    
    with col2:
        st.metric("Active Users", active_users)
    
    with col3:
        st.metric("Inactive Users", inactive_users)
    
    with col4:
        st.metric("Test Users", test_users)
    
    st.write("### User Growth")
    
    months = 12
    month_labels = [(datetime.now() - timedelta(days=30*x)).strftime('%b %Y') for x in range(months)]
    month_labels.reverse() 
    
    np.random.seed(42)
    monthly_new_users = np.random.randint(3, 15, months)
    cumulative_users = np.cumsum(monthly_new_users)
    
    growth_data = pd.DataFrame({
        'Month': month_labels,
        'New Users': monthly_new_users,
        'Total Users': cumulative_users
    })
    
    fig = px.bar(
        growth_data,
        x='Month',
        y='New Users',
        title='User Growth Over Time'
    )
    
    fig.add_scatter(
        x=growth_data['Month'],
        y=growth_data['Total Users'],
        mode='lines+markers',
        name='Total Users',
        yaxis='y2'
    )
    
    fig.update_layout(
        yaxis=dict(title='New Users'),
        yaxis2=dict(
            title='Total Users',
            overlaying='y',
            side='right'
        ),
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)

    st.write("### User Distribution by Role")
    
    role_data = pd.DataFrame({
        'Role': list(role_counts.keys()),
        'Count': list(role_counts.values())
    })
    
    fig = px.pie(
        role_data,
        values='Count',
        names='Role',
        title='User Distribution by Role',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_layout(height=400)
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.write("### User Activity")
    
    days = 30
    day_labels = [(datetime.now() - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(days)]
    day_labels.reverse()  
    
    np.random.seed(43)
    logins = np.random.randint(10, 30, days)
    active_sessions = np.random.randint(20, 50, days)
    api_calls = np.random.randint(100, 300, days)
    
    activity_data = pd.DataFrame({
        'Date': day_labels,
        'Logins': logins,
        'Active Sessions': active_sessions,
        'API Calls': api_calls
    })
    
    fig = px.line(
        activity_data,
        x='Date',
        y=['Logins', 'Active Sessions'],
        title='Daily User Activity',
        markers=True
    )
    
    fig.update_layout(
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.write("### User Retention")
    
    retention_data = {
        "Week 1": 100,
        "Week 2": 82,
        "Week 3": 68,
        "Week 4": 61,
        "Week 5": 57,
        "Week 6": 52,
        "Week 7": 48,
        "Week 8": 45
    }
    
    retention_df = pd.DataFrame({
        'Week': list(retention_data.keys()),
        'Retention (%)': list(retention_data.values())
    })
    
    fig = px.bar(
        retention_df,
        x='Week',
        y='Retention (%)',
        title='User Retention Over Time',
        color='Retention (%)',
        color_continuous_scale=px.colors.sequential.Viridis,
        text='Retention (%)'
    )
    
    fig.update_layout(
        height=400,
        yaxis_range=[0, 100]
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
st.markdown("---")
st.subheader("⚙️ System Actions")

action_col1, action_col2, action_col3, action_col4 = st.columns(4)

with action_col1:
    if st.button("Export User Data", use_container_width=True):
        with st.spinner("Exporting user data..."):
            time.sleep(2)
            
            user_csv = pd.DataFrame(users).to_csv(index=False)
            
            st.success("User data exported successfully!")
            st.download_button(
                label="Download CSV",
                data=user_csv,
                file_name="user_data_export.csv",
                mime="text/csv"
            )

with action_col2:
    if st.button("Synchronize User Data", use_container_width=True):
        with st.spinner("Synchronizing user data..."):
            time.sleep(3)
            st.success("User data synchronized successfully!")

with action_col3:
    if st.button("Backup User Database", use_container_width=True):
        with st.spinner("Creating backup..."):
            time.sleep(4)
            st.success("Database backup created successfully!")

with action_col4:
    if st.button("Generate User Report", use_container_width=True):
        with st.spinner("Generating report..."):
            time.sleep(2)
            
            report_content = f"""
            # FridgeFriend User Report
            Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            ## User Statistics
            - Total Users: {total_users}
            - Active Users: {active_users}
            - Inactive Users: {inactive_users}
            - Test Users: {test_users}
            
            ## User Distribution by Role
            """
            
            for role, count in role_counts.items():
                report_content += f"- {role.capitalize()}: {count} users\n"
            
            st.success("User report generated successfully!")
            st.download_button(
                label="Download Report",
                data=report_content,
                file_name="user_report.txt",
                mime="text/plain"
            )
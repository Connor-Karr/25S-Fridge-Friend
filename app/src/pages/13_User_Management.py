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
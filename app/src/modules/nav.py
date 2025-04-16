import streamlit as st

def SideBarLinks(role=None):
    """
    Creates sidebar navigation links based on user role.
    Args:
        role: The user's role (busy_student, admin, nutritionist, athlete)
    """

# Add a home button
    st.sidebar.page_link("Home.py", label="🏠 Home")

# Add role-specific links
    if role == "busy_student":
        _add_student_links()
    elif role == "admin":
        _add_admin_links()
    elif role == "nutritionist":
        _add_nutritionist_links()
    elif role == "athlete":
        _add_athlete_links()
        
# Add logout button if authenticated
    if st.session_state.get('authenticated', False):
        st.sidebar.markdown("---")
        st.sidebar.write(f"Logged in as: **{st.session_state.first_name}**")
        
        if st.sidebar.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.role = None
            st.session_state.first_name = None
            st.rerun()

# Add footer to sidebar
    st.sidebar.markdown("---")
    st.sidebar.caption("FridgeFriend v1.0")
    st.sidebar.caption("© 2025 CS3200 Project")

def _add_student_links():
    """Add links for the Student role (Ben)"""
    st.sidebar.markdown("### Student Navigation")
    
    st.sidebar.page_link("pages/00_Fridge_Dashboard.py", label="📊 Dashboard")
    st.sidebar.page_link("pages/01_Fridge_Inventory.py", label="🧊 Fridge Inventory")
    st.sidebar.page_link("pages/02_Meal_Suggestions.py", label="🍲 Meal Suggestions")
    st.sidebar.page_link("pages/03_Leftovers_Tracker.py", label="🥡 Leftovers Tracker")

def _add_admin_links():
    """Add links for the Admin role (Alvin)"""
    st.sidebar.markdown("### Admin Navigation")
    
    st.sidebar.page_link("pages/10_Admin_Dashboard.py", label="📊 Admin Dashboard")
    st.sidebar.page_link("pages/11_Ingredient_Management.py", label="🥕 Ingredient Management")
    st.sidebar.page_link("pages/12_System_Logs.py", label="📝 System Logs")
    st.sidebar.page_link("pages/13_User_Management.py", label="👤 User Management")

def _add_nutritionist_links():
    """Add links for the Nutritionist role (Nancy)"""
    st.sidebar.markdown("### Nutritionist Navigation")
    
    st.sidebar.page_link("pages/20_Nutritionist_Dashboard.py", label="📊 Dashboard")
    st.sidebar.page_link("pages/21_Client_Management.py", label="👥 Client Management")
    st.sidebar.page_link("pages/22_Meal_Planning.py", label="🍽️ Meal Planning")
    st.sidebar.page_link("pages/23_Nutrition_Analytics.py", label="📈 Nutrition Analytics")

def _add_athlete_links():
    """Add links for the Athlete role (Riley)"""
    st.sidebar.markdown("### Athlete Navigation")
    
    st.sidebar.page_link("pages/30_Athlete_Dashboard.py", label="📊 Dashboard")
    st.sidebar.page_link("pages/31_Nutrition_Tracking.py", label="🥗 Nutrition Tracking")
    st.sidebar.page_link("pages/32_Meal_Plans.py", label="🍽️ Meal Plans")
    st.sidebar.page_link("pages/33_Performance_Analytics.py", label="📈 Performance Analytics")
       

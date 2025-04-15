import streamlit as st

def SideBarLinks(role=None):
    """
    Creates sidebar navigation links based on user role.
    Args:
        role: The user's role (busy_student, admin, nutritionist, athlete)
    """

# Add logo to sidebar
    # In a real app, replace with your logo file path
    st.sidebar.image("https://via.placeholder.com/150x150.png?text=FridgeFriend", width=120)

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
    
    st.sidebar.page_link("pages/00_Ben_Dashboard.py", label="📊 Dashboard")
    st.sidebar.page_link("pages/01_Fridge_Inventory.py", label="🧊 Fridge Inventory")
    st.sidebar.page_link("pages/02_Meal_Suggestions.py", label="🍲 Meal Suggestions")
    st.sidebar.page_link("pages/03_Leftovers_Tracker.py", label="🥡 Leftovers Tracker")


        

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

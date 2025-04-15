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

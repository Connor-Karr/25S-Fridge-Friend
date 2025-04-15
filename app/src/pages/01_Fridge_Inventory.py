import streamlit as st

SideBarLinks(st.session_state.role)

st.title(f"Welcome, {st.session_state.first_name}! 👋")
st.write("Manage your fridge, plan meals, and stay on budget!")

col1, col2 = st.columns(2)
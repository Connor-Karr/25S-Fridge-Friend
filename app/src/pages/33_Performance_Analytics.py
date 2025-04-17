import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

# API base URL
API_BASE_URL = "http://web-api:4000"

# Authentication check
if not st.session_state.get('authenticated', False) or st.session_state.role != "athlete":
    st.warning("Please log in as an athlete to access this page")
    st.stop()

# Set up navigation
SideBarLinks(st.session_state.role)

# Page header
st.title("📈 Performance Analytics")
st.write("Track and analyze your workouts")

# API helper functions
def get_api_data(endpoint):
    """Get data from API with error handling"""
    try:
        response = requests.get(f"{API_BASE_URL}/{endpoint}")
        if response.status_code == 200:
            return response.json()
        else:
            # Don't show error for 404s
            if response.status_code != 404:
                st.error(f"Error fetching data from {endpoint}: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []

def post_api_data(endpoint, data):
    """Post data to API with error handling"""
    try:
        response = requests.post(f"{API_BASE_URL}/{endpoint}", json=data)
        if response.status_code in [200, 201]:
            return response.json(), True
        else:
            st.error(f"Error posting to {endpoint}: {response.status_code}")
            return None, False
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None, False

def put_api_data(endpoint, data):
    """Put data to API with error handling"""
    try:
        response = requests.put(f"{API_BASE_URL}/{endpoint}", json=data)
        if response.status_code == 200:
            return True
        else:
            st.error(f"Error updating {endpoint}: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

def delete_api_data(endpoint):
    """Delete data via API with error handling"""
    try:
        response = requests.delete(f"{API_BASE_URL}/{endpoint}")
        if response.status_code == 200:
            return True
        else:
            st.error(f"Error deleting from {endpoint}: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

# Get user data
client_id = st.session_state.get('user_id', 1)

# Create tabs for different views
tab1, tab2 = st.tabs(["Workout History", "Add Workout"])

# Workout History Tab
with tab1:
    st.subheader("Your Workout History")
    
    # Get workout data
    workout_data = get_api_data(f"users/client/{client_id}/workouts")
    
    if workout_data:
        # Convert to DataFrame
        workout_df = pd.DataFrame(workout_data)
        
        # Display full workout history
        st.dataframe(
            workout_df,
            column_config={
                "workout_id": "ID", 
                "name": "Workout Type", 
                "quantity": "Duration (min)", 
                "weight": "Weight (lbs)",
                "calories_burnt": "Calories Burned"
            },
            use_container_width=True
        )
        
        # Option to select and manage a workout
        if 'workout_id' in workout_df.columns and not workout_df.empty:
            workout_ids = workout_df['workout_id'].tolist()
            selected_workout_id = st.selectbox("Select workout to manage:", workout_ids)
            
            # Get the selected workout
            selected_workout = workout_df[workout_df['workout_id'] == selected_workout_id].iloc[0]
            
            # Display workout details
            st.subheader("Workout Details")
            
            # Create form for updating
            with st.form("update_workout_form"):
                workout_name = st.text_input("Workout Type:", value=selected_workout.get('name', ''))
                duration = st.number_input("Duration (minutes):", min_value=0, value=int(selected_workout.get('quantity', 0)))
                weight = st.number_input("Weight (if applicable, lbs):", min_value=0.0, value=float(selected_workout.get('weight', 0) or 0))
                calories = st.number_input("Calories Burned:", min_value=0, value=int(selected_workout.get('calories_burnt', 0) or 0))
                
                col1, col2 = st.columns(2)
                with col1:
                    update_button = st.form_submit_button("Update Workout")
                with col2:
                    delete_button = st.form_submit_button("Delete Workout")
                
                if update_button:
                    workout_data = {
                        'name': workout_name,
                        'quantity': duration,
                        'weight': weight if weight > 0 else None,
                        'calories_burnt': calories
                    }
                    if put_api_data(f"users/workouts/{selected_workout_id}", workout_data):
                        st.success("Workout updated successfully!")
                        st.rerun()
                
                if delete_button:
                    if delete_api_data(f"users/workouts/{selected_workout_id}"):
                        st.success("Workout deleted successfully!")
                        st.rerun()
        
        # Workout summary statistics
        if len(workout_df) > 0:
            st.subheader("Workout Summary")
            
            # Group by workout type
            if 'name' in workout_df.columns:
                workout_summary = workout_df['name'].value_counts().reset_index()
                workout_summary.columns = ['Workout Type', 'Count']
                
                st.dataframe(workout_summary, use_container_width=True)
            
            # Show total stats if available
            metrics_cols = st.columns(3)
            
            with metrics_cols[0]:
                if 'quantity' in workout_df.columns:
                    total_duration = workout_df['quantity'].sum()
                    st.metric("Total Duration", f"{total_duration} minutes")
            
            with metrics_cols[1]:
                if 'calories_burnt' in workout_df.columns:
                    total_calories = workout_df['calories_burnt'].sum()
                    st.metric("Total Calories", f"{total_calories} kcal")
            
            with metrics_cols[2]:
                st.metric("Workouts Recorded", f"{len(workout_df)}")
    else:
        st.info("No workout data found. Add your first workout using the 'Add Workout' tab.")

# Add Workout Tab
with tab2:
    st.subheader("Log New Workout")
    
    with st.form("add_workout_form"):
        workout_name = st.text_input("Workout Type:")
        duration = st.number_input("Duration (minutes):", min_value=0, value=30)
        weight = st.number_input("Weight (if applicable, lbs):", min_value=0.0, value=0.0)
        calories = st.number_input("Calories Burned:", min_value=0, value=0)
        
        submit_button = st.form_submit_button("Add Workout")
        
        if submit_button and workout_name:
            # Prepare workout data
            workout_data = {
                'name': workout_name,
                'quantity': duration,
                'weight': weight if weight > 0 else None,
                'calories_burnt': calories,
                'client_id': client_id
            }
            
            # Post to API
            result, success = post_api_data("users/workouts", workout_data)
            
            if success:
                st.success(f"Added {workout_name} to your workout history!")
                st.rerun()


# Refresh button
if st.button("Refresh Data"):
    st.rerun()
import streamlit as st
import pandas as pd
import requests
import logging
from datetime import datetime
from modules.nav import SideBarLinks

# Set up logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# API base URL
API_BASE_URL = "http://web-api:4000"

# Authentication check
if not st.session_state.get('authenticated', False) or st.session_state.role != "nutritionist":
    st.warning("Please log in as a nutritionist to access this page")
    st.stop()

# Set up navigation
SideBarLinks(st.session_state.role)

# Page header
st.title("👩‍⚕️ Nutritionist Dashboard")
st.markdown(f"**Welcome, {st.session_state.first_name}!**")
st.markdown("---")

# We know from the Home.py file that Nancy is advisor_id=2
advisor_id = 2

logger.info(f"Using advisor_id={advisor_id} for nutritionist dashboard")

# Function to get clients for the nutritionist
def get_clients(advisor_id):
    try:
        logger.info(f"Fetching clients for advisor_id={advisor_id}")
        response = requests.get(f"{API_BASE_URL}/users/nutritionist/{advisor_id}/clients")
        if response.status_code == 200:
            return response.json()
        logger.error(f"Error fetching clients: {response.status_code}, {response.text}")
        return []
    except Exception as e:
        logger.error(f"Exception fetching clients: {str(e)}")
        return []

# Function to get dietary alerts
def get_dietary_alerts(advisor_id):
    try:
        logger.info(f"Fetching dietary alerts for advisor_id={advisor_id}")
        response = requests.get(f"{API_BASE_URL}/users/nutritionist/{advisor_id}/dietary-alerts")
        if response.status_code == 200:
            return response.json()
        logger.error(f"Error fetching dietary alerts: {response.status_code}, {response.text}")
        return []
    except Exception as e:
        logger.error(f"Exception fetching dietary alerts: {str(e)}")
        return []

# Function to get nutrition summary
def get_nutrition_summary(advisor_id):
    try:
        logger.info(f"Fetching nutrition summary for advisor_id={advisor_id}")
        response = requests.get(f"{API_BASE_URL}/users/nutritionist/{advisor_id}/nutrition-summary")
        if response.status_code == 200:
            return response.json()
        logger.error(f"Error fetching nutrition summary: {response.status_code}, {response.text}")
        return []
    except Exception as e:
        logger.error(f"Exception fetching nutrition summary: {str(e)}")
        return []

# Get data
clients = get_clients(advisor_id)
dietary_alerts = get_dietary_alerts(advisor_id)
nutrition_summary = get_nutrition_summary(advisor_id)

# Client overview section
st.markdown("### 👥 Active Clients")

if clients:
    # Create DataFrame for display
    clients_df = pd.DataFrame(clients)
    
    # Rename columns for better display
    if 'f_name' in clients_df.columns and 'l_name' in clients_df.columns:
        clients_df['client_name'] = clients_df['f_name'] + ' ' + clients_df['l_name']
    
    display_cols = ['client_name', 'age_group', 'personal_diet', 'dietary_restrictions']
    
    if all(col in clients_df.columns for col in display_cols):
        renamed_df = clients_df[display_cols].copy()
        renamed_df.columns = ['Client Name', 'Age Group', 'Diet Type', 'Restrictions']
        st.table(renamed_df)
    else:
        # If we don't have all expected columns, show what we have
        logger.info(f"Client data columns: {clients_df.columns.tolist()}")
        st.table(clients_df)
else:
    st.info("No clients found. You will see your clients here once assigned.")

# Dietary Alerts section
st.markdown("### ⚠️ Dietary Alerts")

if dietary_alerts:
    # Create DataFrame for display
    alerts_df = pd.DataFrame(dietary_alerts)
    
    # Rename columns for better display
    if 'f_name' in alerts_df.columns and 'l_name' in alerts_df.columns:
        alerts_df['client_name'] = alerts_df['f_name'] + ' ' + alerts_df['l_name']
    
    if 'alert_message' in alerts_df.columns and 'priority' in alerts_df.columns:
        display_cols = ['client_name', 'alert_message', 'priority']
        
        if all(col in alerts_df.columns for col in display_cols):
            renamed_df = alerts_df[display_cols].copy()
            renamed_df.columns = ['Client', 'Alert', 'Priority']
            st.table(renamed_df)
        else:
            # If we don't have all expected columns, show what we have
            logger.info(f"Alert data columns: {alerts_df.columns.tolist()}")
            st.table(alerts_df)
    else:
        # If we don't have expected columns, show what we have
        logger.info(f"Alert data columns: {alerts_df.columns.tolist()}")
        st.table(alerts_df)
else:
    st.info("No dietary alerts at this time.")

# Nutrition distribution section
st.markdown("### 📊 Nutrition Distribution by Diet Type")

if nutrition_summary:
    nutrition_df = pd.DataFrame(nutrition_summary)
    logger.info(f"Nutrition summary data types: {nutrition_df.dtypes}")
    
    if all(col in nutrition_df.columns for col in ['diet_type', 'avg_protein', 'avg_carbs', 'avg_fat']):
        # Convert string values to float for calculations
        try:
            # Convert numeric columns to float
            for col in ['avg_protein', 'avg_carbs', 'avg_fat']:
                nutrition_df[col] = pd.to_numeric(nutrition_df[col], errors='coerce')
            
            # Calculate total and percentages
            nutrition_df['total'] = nutrition_df['avg_protein'] + nutrition_df['avg_carbs'] + nutrition_df['avg_fat']
            nutrition_df['protein_pct'] = (nutrition_df['avg_protein'] / nutrition_df['total'] * 100).round(1)
            nutrition_df['carbs_pct'] = (nutrition_df['avg_carbs'] / nutrition_df['total'] * 100).round(1)
            nutrition_df['fat_pct'] = (nutrition_df['avg_fat'] / nutrition_df['total'] * 100).round(1)
            
            # Display a summary table with all diet types
            summary_table = []
            
            for _, row in nutrition_df.iterrows():
                summary_table.append({
                    'Diet Type': row['diet_type'],
                    'Protein (g)': round(row['avg_protein'], 1),
                    'Carbs (g)': round(row['avg_carbs'], 1),
                    'Fat (g)': round(row['avg_fat'], 1),
                    'Protein (%)': f"{row['protein_pct']}%",
                    'Carbs (%)': f"{row['carbs_pct']}%",
                    'Fat (%)': f"{row['fat_pct']}%"
                })
            
            summary_df = pd.DataFrame(summary_table)
            st.table(summary_df)
        except Exception as e:
            logger.error(f"Error processing nutrition data: {str(e)}")
            # Just display the raw data if we encounter calculation errors
            st.write("Raw nutrition data:")
            st.table(nutrition_df)
    else:
        # If we don't have all expected columns, show what we have
        logger.info(f"Nutrition summary columns: {nutrition_df.columns.tolist()}")
        st.table(nutrition_df)
else:
    st.info("No nutrition data available for analysis.")


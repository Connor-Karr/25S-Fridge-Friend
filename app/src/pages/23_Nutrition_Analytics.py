import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from modules.nav import SideBarLinks

API_BASE_URL = "http://web-api:4000"

if not st.session_state.get('authenticated', False) or st.session_state.role != "nutritionist":
    st.warning("Please log in as Nancy to access this page")
    st.stop()

SideBarLinks(st.session_state.role)

# Page header
st.title("📈 Nutrition Analytics")
st.write("Analyze nutritional data across clients and identify trends")

# Mock client data
clients = [
    {"id": 1, "name": "John D.", "age": 27, "goal": "Weight Loss", "diet": "Low Carb"},
    {"id": 2, "name": "Sarah M.", "age": 34, "goal": "Muscle Gain", "diet": "High Protein"},
    {"id": 3, "name": "Michael R.", "age": 42, "goal": "Maintenance", "diet": "Balanced"},
    {"id": 4, "name": "Emma L.", "age": 19, "goal": "Performance", "diet": "Keto"},
    {"id": 5, "name": "David W.", "age": 55, "goal": "Health", "diet": "Mediterranean"}
]
# Time period selection
time_period = st.selectbox(
    "Analysis Period:",
    ["Last 30 Days", "Last 3 Months", "Last 6 Months", "Year to Date", "Custom Range"]
)

if time_period == "Custom Range":
    date_range = st.date_input(
        "Select date range:",
        value=(datetime.now().date() - timedelta(days=30), datetime.now().date()),
        max_value=datetime.now().date()
    )
else:
    if time_period == "Last 30 Days":
        days = 30
    elif time_period == "Last 3 Months":
        days = 90
    elif time_period == "Last 6 Months":
        days = 180
    else:  # Year to Date
        start_of_year = datetime(datetime.now().year, 1, 1).date()
        days = (datetime.now().date() - start_of_year).days

    date_range = (datetime.now().date() - timedelta(days=days), datetime.now().date())
# Create different tabs
tab1, tab2, tab3, tab4 = st.tabs(["Diet Compliance", "Nutrient Analysis", "Client Comparisons", "Allergy Insights"])
# Diet Compliance Tab
with tab1:
    st.subheader("Diet Compliance Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        goal_filter = st.multiselect(
            "Filter by goal:",
            ["Weight Loss", "Muscle Gain", "Maintenance", "Performance", "Health"],
            default=["Weight Loss", "Muscle Gain"]
        )
    with col2:
        diet_filter = st.multiselect(
            "Filter by diet type:",
            ["Low Carb", "High Protein", "Balanced", "Keto", "Mediterranean"],
            default=["Low Carb", "High Protein", "Keto"]
        )
    
    # Filter clients based on selections
    filtered_clients = [
        client for client in clients
        if (not goal_filter or client["goal"] in goal_filter) and
           (not diet_filter or client["diet"] in diet_filter)
    ]
    
    if filtered_clients:
        # Create mock compliance data
        np.random.seed(42)
        compliance_data = []
        for client in filtered_clients:
            diet_bias = {"Low Carb": 5, "High Protein": 10, "Balanced": 15, "Keto": 0, "Mediterranean": 12}
            base_compliance = np.random.normal(75, 10)
            diet_boost = diet_bias.get(client["diet"], 0)
            compliance_data.append({
                "Client Name": client["name"],
                "Diet Type": client["diet"],
                "Goal": client["goal"],
                "Compliance (%)": min(max(base_compliance + diet_boost, 40), 98)
            })
        
        compliance_df = pd.DataFrame(compliance_data)
        avg_compliance = compliance_df["Compliance (%)"].mean()
        st.metric("Average Compliance", f"{avg_compliance:.1f}%")
        
        fig = px.bar(
            compliance_df,
            x="Client Name",
            y="Compliance (%)",
            color="Diet Type",
            title="Diet Compliance by Client",
            hover_data=["Goal"],
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.add_hline(
            y=80,
            line_dash="dash",
            line_color="red",
            annotation_text="Target Compliance",
            annotation_position="bottom right"
        )
        fig.update_layout(
            height=400,
            xaxis_title="Client",
            yaxis_title="Compliance (%)",
            yaxis=dict(range=[0, 100])
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Compliance by Diet Type")
        diet_compliance = compliance_df.groupby("Diet Type")["Compliance (%)"].mean().reset_index()
        fig = px.bar(
            diet_compliance,
            y="Diet Type",
            x="Compliance (%)",
            orientation='h',
            title="Average Compliance by Diet Type",
            color="Compliance (%)",
            color_continuous_scale=px.colors.sequential.Viridis,
            text="Compliance (%)"
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(height=350, xaxis=dict(range=[0, 100]), xaxis_title="Compliance (%)", yaxis_title="Diet Type")
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Key Compliance Factors")
        factors = {
            "Meal Tracking Frequency": 85,
            "Using Recommended Foods": 72,
            "Following Portion Sizes": 68,
            "Meal Timing Adherence": 76,
            "Following Macronutrient Ratios": 64
        }
        factor_df = pd.DataFrame({"Factor": list(factors.keys()), "Adherence (%)": list(factors.values())})
        fig = px.bar(
            factor_df,
            y="Factor",
            x="Adherence (%)",
            orientation='h',
            title="Key Compliance Factors",
            color="Adherence (%)",
            color_continuous_scale=px.colors.sequential.Viridis,
            text="Adherence (%)"
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(height=350, xaxis=dict(range=[0, 100]), xaxis_title="Adherence (%)", yaxis_title="Factor")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No clients match the selected filters.")

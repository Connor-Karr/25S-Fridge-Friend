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
# Nutrient Analysis Tab
with tab2:
    st.subheader("Nutrient Analysis")
    
    # Controls for nutrient, analysis type, and grouping
    control_col1, control_col2, control_col3 = st.columns(3)
    with control_col1:
        nutrient = st.selectbox(
            "Select nutrient:",
            ["Protein", "Carbs", "Fat", "Fiber", "Sodium", "Vitamin D", "Calcium", "Iron"]
        )
    with control_col2:
        analysis_type = st.selectbox(
            "Analysis type:",
            ["Average Intake", "% of Target", "Trend Over Time"]
        )
    with control_col3:
        grouping = st.selectbox(
            "Group by:",
            ["Diet Type", "Goal", "Age Group", "Individual"]
        )
    
    if grouping == "Diet Type":
        groups = ["Low Carb", "High Protein", "Balanced", "Keto", "Mediterranean"]
    elif grouping == "Goal":
        groups = ["Weight Loss", "Muscle Gain", "Maintenance", "Performance", "Health"]
    elif grouping == "Age Group":
        groups = ["18-24", "25-34", "35-44", "45-54", "55+"]
    else:
        groups = [client["name"] for client in clients]
    
    np.random.seed(44)
    nutrient_data = []
    
    if analysis_type == "Trend Over Time":
        days = 30
        dates = [(datetime.now() - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(days)]
        dates.reverse()
        
        for group in groups:
            if nutrient == "Protein":
                base, std_dev = 100, 15
            elif nutrient == "Carbs":
                base, std_dev = 180, 25
            elif nutrient == "Fat":
                base, std_dev = 60, 10
            else:
                base, std_dev = 50, 8
            
            trend = np.linspace(-5, 5, days)
            values = np.clip(np.random.normal(base, std_dev, days) + trend, 0, None)
            for i, date in enumerate(dates):
                nutrient_data.append({"Date": date, "Group": group, "Value": values[i]})
        
        nutrient_df = pd.DataFrame(nutrient_data)
        fig = px.line(
            nutrient_df,
            x="Date",
            y="Value",
            color="Group",
            title=f"{nutrient} Trend Over Time by {grouping}",
            markers=True
        )
        fig.update_layout(height=500, xaxis_title="Date", yaxis_title=f"{nutrient} (g)" if nutrient not in ["Sodium", "Vitamin D", "Calcium", "Iron"] else f"{nutrient} (mg)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        # Generate average or % of target data per group
        for group in groups:
            if nutrient == "Protein":
                base, std_dev, target = 100, 15, 120
            elif nutrient == "Carbs":
                base, std_dev, target = 180, 25, 200
            elif nutrient == "Fat":
                base, std_dev, target = 60, 10, 65
            elif nutrient == "Fiber":
                base, std_dev, target = 25, 5, 30
            elif nutrient == "Sodium":
                base, std_dev, target = 2000, 300, 2300
            else:
                base, std_dev, target = 50, 10, 60
            
            if group in ["High Protein", "Muscle Gain", "25-34", "John D."]:
                base_adj = base * 1.1
            elif group in ["Low Carb", "Keto", "Weight Loss"]:
                base_adj = base * 0.8 if nutrient == "Carbs" else base * 1.05
            else:
                base_adj = base
            
            value = np.clip(np.random.normal(base_adj, std_dev), 0, None)
            if analysis_type == "% of Target":
                value = (value / target) * 100
            
            nutrient_data.append({"Group": group, "Value": value})
        
        nutrient_df = pd.DataFrame(nutrient_data)
        if analysis_type == "% of Target":
            fig = px.bar(
                nutrient_df,
                x="Group",
                y="Value",
                title=f"{nutrient} Intake (% of Target) by {grouping}",
                color="Value",
                color_continuous_scale=px.colors.sequential.Viridis,
                text="Value"
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.add_hline(
                y=100,
                line_dash="dash",
                line_color="red",
                annotation_text="Target (100%)",
                annotation_position="bottom right"
            )
            fig.update_layout(height=400, xaxis_title=grouping, yaxis_title="% of Target", yaxis=dict(range=[0, max(150, nutrient_df["Value"].max() * 1.1)]))
        else:
            fig = px.bar(
                nutrient_df,
                x="Group",
                y="Value",
                title=f"Average {nutrient} Intake by {grouping}",
                color="Group",
                text="Value"
            )
            fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
            fig.update_layout(height=400, xaxis_title=grouping, yaxis_title=f"{nutrient} (g)" if nutrient not in ["Sodium", "Vitamin D", "Calcium", "Iron"] else f"{nutrient} (mg)")
        st.plotly_chart(fig, use_container_width=True)
    
    # Nutrient insights based on selected nutrient
    st.subheader("Nutrient Insights")
    if nutrient == "Protein":
        st.info("High-protein diet clients are consistently meeting protein targets (94% compliance), while low-carb dieters show more variability.")
        st.info("Consider increasing protein targets for performance-focused clients as they consistently exceed their current levels.")
    elif nutrient == "Carbs":
        st.warning("Keto diet clients occasionally exceed their carb limits on weekends, leading to a 23% drop in compliance.")
        st.info("Offer guidance on hidden carb sources and weekend meal strategies for keto clients.")
    elif nutrient == "Fat":
        st.info("Mediterranean diet clients have the most consistent healthy fat intake, achieving 92% compliance.")
        st.info("Share Mediterranean fat sourcing techniques with other groups to promote better fat profiles.")
    elif nutrient == "Fiber":
        st.warning("Fiber intake is below target for 72% of clients, regardless of diet type.")
        st.info("Implement targeted fiber education programs and recommend more high-fiber foods.")
    else:
        st.info("Select different nutrients to view specific insights.")

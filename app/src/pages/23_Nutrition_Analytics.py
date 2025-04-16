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
# Client Comparisons Tab
with tab3:
    st.subheader("Client Comparisons")
    
    selected_clients = st.multiselect(
        "Select clients to compare:",
        [client["name"] for client in clients],
        default=[clients[0]["name"], clients[1]["name"]] if len(clients) >= 2 else []
    )
    
    if selected_clients:
        metrics = st.multiselect(
            "Select metrics to compare:",
            ["Calories", "Protein", "Carbs", "Fat", "Diet Compliance", "Meal Logging Consistency", "Progress Rate"],
            default=["Calories", "Protein", "Diet Compliance"]
        )
        
        if metrics:
            comparison_data = []
            for client_name in selected_clients:
                client = next((c for c in clients if c["name"] == client_name), None)
                if client:
                    client_row = {"Client": client_name}
                    diet_bias = {
                        "Low Carb": {"Calories": -100, "Protein": 20, "Carbs": -50, "Fat": 10},
                        "High Protein": {"Calories": 100, "Protein": 40, "Carbs": -20, "Fat": -5},
                        "Keto": {"Calories": -50, "Protein": 30, "Carbs": -80, "Fat": 30},
                        "Balanced": {"Calories": 0, "Protein": 0, "Carbs": 0, "Fat": 0},
                        "Mediterranean": {"Calories": -30, "Protein": -10, "Carbs": 20, "Fat": 5}
                    }
                    goal_bias = {
                        "Weight Loss": {"Diet Compliance": 5, "Meal Logging Consistency": 10, "Progress Rate": 8},
                        "Muscle Gain": {"Diet Compliance": 8, "Meal Logging Consistency": 5, "Progress Rate": 7},
                        "Maintenance": {"Diet Compliance": 10, "Meal Logging Consistency": 0, "Progress Rate": 6},
                        "Performance": {"Diet Compliance": 12, "Meal Logging Consistency": 15, "Progress Rate": 9},
                        "Health": {"Diet Compliance": 5, "Meal Logging Consistency": -5, "Progress Rate": 4}
                    }
                    
                    diet = client["diet"]
                    goal = client["goal"]
                    
                    for metric in metrics:
                        np.random.seed(hash(client_name + metric) % 10000)
                        if metric in ["Calories", "Protein", "Carbs", "Fat"]:
                            base_values = {"Calories": 2000, "Protein": 100, "Carbs": 200, "Fat": 65}
                            base = base_values[metric] + diet_bias.get(diet, {}).get(metric, 0)
                            value = np.clip(np.random.normal(base, base * 0.1), 0, None)
                            client_row[metric] = round(value, 1)
                        else:
                            base_values = {"Diet Compliance": 75, "Meal Logging Consistency": 70, "Progress Rate": 65}
                            base = base_values[metric] + goal_bias.get(goal, {}).get(metric, 0)
                            value = np.clip(np.random.normal(base, 5), 0, 100)
                            client_row[metric] = round(value, 1)
                    comparison_data.append(client_row)
            
            comparison_df = pd.DataFrame(comparison_data)
            st.dataframe(comparison_df, use_container_width=True)
            
            if len(selected_clients) <= 5:
                fig = go.Figure()
                for data in comparison_data:
                    values = [data[metric] for metric in metrics]
                    normalized_values = []
                    for j, metric in enumerate(metrics):
                        if metric in ["Diet Compliance", "Meal Logging Consistency", "Progress Rate"]:
                            normalized_values.append(values[j])
                        elif metric == "Calories":
                            normalized_values.append((values[j] / 2000) * 100)
                        elif metric == "Protein":
                            normalized_values.append((values[j] / 100) * 100)
                        elif metric == "Carbs":
                            normalized_values.append((values[j] / 200) * 100)
                        elif metric == "Fat":
                            normalized_values.append((values[j] / 65) * 100)
                    fig.add_trace(go.Scatterpolar(
                        r=normalized_values,
                        theta=metrics,
                        fill='toself',
                        name=data["Client"]
                    ))
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 150])),
                    title="Client Comparison (Normalized %)",
                    height=500
                )
                st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("Key Differences")
            if len(selected_clients) >= 2:
                max_diff_metric, max_diff_value, max_diff_clients = None, 0, (None, None)
                for metric in metrics:
                    for i, client1 in enumerate(comparison_data):
                        for j, client2 in enumerate(comparison_data):
                            if i < j:
                                diff = abs(client1[metric] - client2[metric])
                                if diff > max_diff_value:
                                    max_diff_value = diff
                                    max_diff_metric = metric
                                    max_diff_clients = (client1["Client"], client2["Client"])
                if max_diff_metric:
                    st.info(f"**Biggest difference:** {max_diff_clients[0]} and {max_diff_clients[1]} differ most in {max_diff_metric} ({max_diff_value:.1f} units difference).")
                
                min_diff_metric, min_diff_value, min_diff_clients = None, float('inf'), (None, None)
                for metric in metrics:
                    for i, client1 in enumerate(comparison_data):
                        for j, client2 in enumerate(comparison_data):
                            if i < j:
                                diff = abs(client1[metric] - client2[metric])
                                if diff < min_diff_value:
                                    min_diff_value = diff
                                    min_diff_metric = metric
                                    min_diff_clients = (client1["Client"], client2["Client"])
                if min_diff_metric:
                    st.info(f"**Most similar:** {min_diff_clients[0]} and {min_diff_clients[1]} are most similar in {min_diff_metric} (only {min_diff_value:.1f} units difference).")
            
            st.subheader("Suggested Interventions")
            for client in comparison_data:
                client_name = client["Client"]
                weakest_metric, weakest_value = None, float('inf')
                for metric in metrics:
                    if metric == "Calories":
                        normalized_value = (client[metric] / 2000) * 100
                    elif metric == "Protein":
                        normalized_value = (client[metric] / 100) * 100
                    elif metric == "Carbs":
                        normalized_value = (client[metric] / 200) * 100
                    elif metric == "Fat":
                        normalized_value = (client[metric] / 65) * 100
                    else:
                        normalized_value = client[metric]
                    if normalized_value < weakest_value:
                        weakest_value = normalized_value
                        weakest_metric = metric
                if weakest_metric:
                    st.write(f"**{client_name}:** Focus on improving {weakest_metric}")
                    if weakest_metric == "Diet Compliance":
                        st.write("  - Simplify meal plan to increase adherence")
                        st.write("  - Set up more frequent check-ins")
                        st.write("  - Provide easier alternatives for challenging meals")
                    elif weakest_metric == "Meal Logging Consistency":
                        st.write("  - Send daily reminders at meal times")
                        st.write("  - Simplify logging process with quick-add options")
                        st.write("  - Provide positive reinforcement for consistent logging")
                    elif weakest_metric == "Progress Rate":
                        st.write("  - Adjust targets for achievable short-term goals")
                        st.write("  - Increase check-in frequency")
                        st.write("  - Review and adjust nutrition plan")
                    elif weakest_metric == "Protein":
                        st.write("  - Add protein-rich snacks between meals")
                        st.write("  - Consider protein supplementation")
                        st.write("  - Provide high-protein recipe alternatives")
        else:
            st.info("Please select at least one metric to compare.")
    else:
        st.info("Please select at least one client to analyze.")
# Allergy Insights Tab
with tab4:
    st.subheader("Allergy & Restriction Analytics")
    
    # Mock allergy data and pie chart
    allergies = {"Dairy": 28, "Gluten": 22, "Nuts": 18, "Shellfish": 12, "Eggs": 10, "Soy": 8, "Fish": 5, "Other": 15}
    allergy_df = pd.DataFrame({"Allergen": list(allergies.keys()), "Count": list(allergies.values())})
    fig = px.pie(
        allergy_df,
        values="Count",
        names="Allergen",
        title="Distribution of Common Allergens",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Substitution Compliance
    st.subheader("Substitution Compliance")
    substitutions = {"Dairy to Plant Milk": 85, "Gluten to GF Grains": 72, "Eggs to Flax Eggs": 64, "Nuts to Seeds": 78, "Wheat to Almond Flour": 62}
    subst_df = pd.DataFrame({"Substitution": list(substitutions.keys()), "Compliance (%)": list(substitutions.values())})
    fig = px.bar(
        subst_df,
        y="Substitution",
        x="Compliance (%)",
        orientation='h',
        title="Substitution Compliance",
        color="Compliance (%)",
        color_continuous_scale=px.colors.sequential.Viridis,
        text="Compliance (%)"
    )
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(height=350, xaxis=dict(range=[0, 100]), xaxis_title="Compliance (%)", yaxis_title="Substitution Type")
    st.plotly_chart(fig, use_container_width=True)
    
    # Allergy Impact on Nutrition
    st.subheader("Allergy Impact on Nutrition")
    allergen_impacts = {
        "Dairy Allergy": {"Calcium": -35, "Vitamin D": -28, "Protein": -12, "Calories": -8},
        "Gluten Allergy": {"Fiber": -25, "B Vitamins": -30, "Calories": -15, "Protein": -10},
        "Nut Allergy": {"Healthy Fats": -32, "Protein": -15, "Fiber": -18, "Calories": -12}
    }
    impact_data = []
    for allergen, impacts in allergen_impacts.items():
        for nutrient, impact in impacts.items():
            impact_data.append({"Allergen": allergen, "Nutrient": nutrient, "Impact (%)": impact})
    impact_df = pd.DataFrame(impact_data)
    fig = px.bar(
        impact_df,
        x="Allergen",
        y="Impact (%)",
        color="Nutrient",
        barmode="group",
        title="Nutritional Impact of Allergies",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(height=400, xaxis_title="Allergen", yaxis_title="Impact (%)")
    st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    st.subheader("Key Recommendations")
    st.write("""
    Based on the allergy analysis, here are some key recommendations:
    
    1. **Dairy Allergies**: Focus on non-dairy calcium sources (fortified plant milks, leafy greens) and consider vitamin D supplementation.
    2. **Gluten Allergies**: Increase fiber from non-grain sources (vegetables, fruits) and consider B vitamin supplementation.
    3. **Nut Allergies**: Incorporate more seeds and avocados for healthy fats.
    4. **Overall Strategy**: Create specialized meal plans for common allergen combinations.
    """)
    
    with st.expander("Allergen Substitution Resources"):
        st.write("**Downloadable Resources:**")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Dairy Substitution Guide**")
            if st.button("Download Dairy Guide"):
                st.download_button(
                    label="Download Guide",
                    data="This would be a comprehensive guide to dairy substitutions.",
                    file_name="dairy_substitution_guide.txt",
                    mime="text/plain"
                )
        with col2:
            st.write("**Gluten-Free Alternatives Guide**")
            if st.button("Download Gluten Guide"):
                st.download_button(
                    label="Download Guide",
                    data="This would be a comprehensive guide to gluten-free alternatives.",
                    file_name="gluten_free_guide.txt",
                    mime="text/plain"
                )
# Generate report section
st.markdown("---")
st.subheader("🔄 Generate Nutrition Reports")

with st.form("generate_report_form"):
    col1, col2 = st.columns(2)
    with col1:
        report_type = st.selectbox(
            "Report Type:",
            ["Client Summary", "Diet Compliance", "Nutrition Analysis", "Allergy Management"]
        )
        client_selection = st.multiselect(
            "Select clients:",
            [client["name"] for client in clients],
            default=[clients[0]["name"]] if clients else []
        )
    with col2:
        include_charts = st.checkbox("Include charts", value=True)
        include_recommendations = st.checkbox("Include recommendations", value=True)
        report_format = st.selectbox(
            "Report format:",
            ["PDF", "Excel", "Text"]
        )
    
    submit = st.form_submit_button("Generate Report")
    
    if submit:
        if client_selection:
            with st.spinner("Generating report..."):
                time.sleep(2)
                report_content = f"""
                # Nutrition Analysis Report
                Report Type: {report_type}
                Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
                
                ## Clients Included
                {', '.join(client_selection)}
                
                ## Summary
                This report provides a detailed analysis of nutritional data for the selected clients over the specified time period.
                
                ## Key Findings
                - Diet compliance averages 78% across all clients
                - Protein intake is consistently below target for 60% of clients
                """
                st.download_button(
                    label="Download Report",
                    data=report_content,
                    file_name=f"nutrition_report_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )

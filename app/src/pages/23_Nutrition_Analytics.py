import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from modules.nav import SideBarLinks

# Authentication check
if not st.session_state.get('authenticated', False) or st.session_state.role != "nutritionist":
    st.warning("Please log in as Nancy to access this page")
    st.stop()

SideBarLinks(st.session_state.role)

# Page header
st.title("Nutrition Analytics")
st.write("Analyze nutritional data across clients and identify trends")

# Simple time period selection
time_period = st.selectbox(
    "Analysis Period:",
    ["Last 30 Days", "Last 3 Months", "Last 6 Months", "Year to Date"]
)

# Create tabs for different analysis views
tab1, tab2, tab3, tab4 = st.tabs(["Diet Compliance", "Nutrient Analysis", "Client Comparisons", "Allergies"])

# Diet Compliance Tab
with tab1:
    st.header("Diet Compliance Analysis")
    
    # Simple filter options
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
            default=["Low Carb", "High Protein"]
        )
    
    # Mock compliance data
    compliance_data = [
        {"Client": "John D.", "Diet Type": "Low Carb", "Goal": "Weight Loss", "Compliance (%)": 85},
        {"Client": "Sarah M.", "Diet Type": "High Protein", "Goal": "Muscle Gain", "Compliance (%)": 92},
        {"Client": "Michael R.", "Diet Type": "Balanced", "Goal": "Maintenance", "Compliance (%)": 78},
        {"Client": "Emma L.", "Diet Type": "Keto", "Goal": "Performance", "Compliance (%)": 88},
        {"Client": "David W.", "Diet Type": "Mediterranean", "Goal": "Health", "Compliance (%)": 76}
    ]
    
    # Filter based on selections
    filtered_data = []
    for client in compliance_data:
        if (not goal_filter or client["Goal"] in goal_filter) and (not diet_filter or client["Diet Type"] in diet_filter):
            filtered_data.append(client)
    
    # Display as a table
    if filtered_data:
        st.subheader("Client Compliance Table")
        compliance_df = pd.DataFrame(filtered_data)
        st.table(compliance_df)
        
        # Calculate and show average compliance
        avg_compliance = sum(client["Compliance (%)"] for client in filtered_data) / len(filtered_data)
        st.success(f"Average compliance: {avg_compliance:.1f}%")
    else:
        st.info("No clients match the selected filters.")
    
    # Compliance factors table
    st.subheader("Key Compliance Factors")
    
    factors_data = [
        {"Factor": "Meal Tracking Frequency", "Adherence (%)": 85},
        {"Factor": "Using Recommended Foods", "Adherence (%)": 72},
        {"Factor": "Following Portion Sizes", "Adherence (%)": 68},
        {"Factor": "Meal Timing Adherence", "Adherence (%)": 76},
        {"Factor": "Following Macronutrient Ratios", "Adherence (%)": 64}
    ]
    
    factors_df = pd.DataFrame(factors_data)
    st.table(factors_df)

# Nutrient Analysis Tab
with tab2:
    st.header("Nutrient Analysis")
    
    # Simplified controls
    control_col1, control_col2 = st.columns(2)
    
    with control_col1:
        nutrient = st.selectbox(
            "Select nutrient:",
            ["Protein", "Carbs", "Fat", "Fiber", "Sodium", "Vitamin D"]
        )
    
    with control_col2:
        grouping = st.selectbox(
            "Group by:",
            ["Diet Type", "Goal", "Age Group", "Individual"]
        )
    
    # Mock nutrient data based on selection
    if grouping == "Diet Type":
        nutrient_data = [
            {"Group": "Low Carb", "Value": 120, "Target": 100, "% of Target": 120},
            {"Group": "High Protein", "Value": 155, "Target": 130, "% of Target": 119},
            {"Group": "Balanced", "Value": 90, "Target": 100, "% of Target": 90},
            {"Group": "Keto", "Value": 130, "Target": 110, "% of Target": 118},
            {"Group": "Mediterranean", "Value": 85, "Target": 100, "% of Target": 85}
        ]
    elif grouping == "Goal":
        nutrient_data = [
            {"Group": "Weight Loss", "Value": 110, "Target": 100, "% of Target": 110},
            {"Group": "Muscle Gain", "Value": 150, "Target": 140, "% of Target": 107},
            {"Group": "Maintenance", "Value": 95, "Target": 100, "% of Target": 95},
            {"Group": "Performance", "Value": 125, "Target": 120, "% of Target": 104},
            {"Group": "Health", "Value": 90, "Target": 100, "% of Target": 90}
        ]
    elif grouping == "Age Group":
        nutrient_data = [
            {"Group": "18-24", "Value": 105, "Target": 100, "% of Target": 105},
            {"Group": "25-34", "Value": 115, "Target": 100, "% of Target": 115},
            {"Group": "35-44", "Value": 95, "Target": 100, "% of Target": 95},
            {"Group": "45-54", "Value": 85, "Target": 100, "% of Target": 85},
            {"Group": "55+", "Value": 80, "Target": 100, "% of Target": 80}
        ]
    else:  # Individual
        nutrient_data = [
            {"Group": "John D.", "Value": 125, "Target": 100, "% of Target": 125},
            {"Group": "Sarah M.", "Value": 145, "Target": 130, "% of Target": 112},
            {"Group": "Michael R.", "Value": 98, "Target": 100, "% of Target": 98},
            {"Group": "Emma L.", "Value": 115, "Target": 110, "% of Target": 105},
            {"Group": "David W.", "Value": 85, "Target": 100, "% of Target": 85}
        ]
    
    # Convert to DataFrame and display as table
    nutrient_df = pd.DataFrame(nutrient_data)
    st.subheader(f"{nutrient} Analysis by {grouping}")
    st.table(nutrient_df)
    
    # Add insights based on selected nutrient
    st.subheader("Nutrient Insights")
    
    if nutrient == "Protein":
        st.info("High-protein diet clients are consistently meeting protein targets (94% compliance), while low-carb dieters show more variability.")
    elif nutrient == "Carbs":
        st.warning("Keto diet clients occasionally exceed their carb limits on weekends, leading to a 23% drop in compliance.")
    elif nutrient == "Fat":
        st.info("Mediterranean diet clients have the most consistent healthy fat intake, achieving 92% compliance.")
    elif nutrient == "Fiber":
        st.warning("Fiber intake is below target for 72% of clients, regardless of diet type.")
    else:
        st.info("Select different nutrients to view specific insights.")

# Client Comparisons Tab
with tab3:
    st.header("Client Comparisons")
    
    # Client selection
    selected_clients = st.multiselect(
        "Select clients to compare:",
        ["John D.", "Sarah M.", "Michael R.", "Emma L.", "David W."],
        default=["John D.", "Sarah M."]
    )
    
    # Metrics selection
    selected_metrics = st.multiselect(
        "Select metrics to compare:",
        ["Calories", "Protein", "Carbs", "Fat", "Diet Compliance", "Meal Logging", "Progress Rate"],
        default=["Calories", "Protein", "Diet Compliance"]
    )
    
    # Create comparison table if selections are made
    if selected_clients and selected_metrics:
        # Mock data for comparison
        comparison_data = []
        
        for client in selected_clients:
            client_row = {"Client": client}
            
            # Add mock data for each selected metric
            if "Calories" in selected_metrics:
                if client == "John D.":
                    client_row["Calories"] = 1850
                elif client == "Sarah M.":
                    client_row["Calories"] = 2100
                elif client == "Michael R.":
                    client_row["Calories"] = 2300
                elif client == "Emma L.":
                    client_row["Calories"] = 1950
                else:
                    client_row["Calories"] = 2050
            
            if "Protein" in selected_metrics:
                if client == "John D.":
                    client_row["Protein"] = 120
                elif client == "Sarah M.":
                    client_row["Protein"] = 140
                elif client == "Michael R.":
                    client_row["Protein"] = 110
                elif client == "Emma L.":
                    client_row["Protein"] = 105
                else:
                    client_row["Protein"] = 95
            
            if "Carbs" in selected_metrics:
                if client == "John D.":
                    client_row["Carbs"] = 150
                elif client == "Sarah M.":
                    client_row["Carbs"] = 190
                elif client == "Michael R.":
                    client_row["Carbs"] = 240
                elif client == "Emma L.":
                    client_row["Carbs"] = 120
                else:
                    client_row["Carbs"] = 220
            
            if "Fat" in selected_metrics:
                if client == "John D.":
                    client_row["Fat"] = 65
                elif client == "Sarah M.":
                    client_row["Fat"] = 60
                elif client == "Michael R.":
                    client_row["Fat"] = 75
                elif client == "Emma L.":
                    client_row["Fat"] = 95
                else:
                    client_row["Fat"] = 70
            
            if "Diet Compliance" in selected_metrics:
                if client == "John D.":
                    client_row["Diet Compliance"] = 85
                elif client == "Sarah M.":
                    client_row["Diet Compliance"] = 92
                elif client == "Michael R.":
                    client_row["Diet Compliance"] = 78
                elif client == "Emma L.":
                    client_row["Diet Compliance"] = 88
                else:
                    client_row["Diet Compliance"] = 76
            
            if "Meal Logging" in selected_metrics:
                if client == "John D.":
                    client_row["Meal Logging"] = 92
                elif client == "Sarah M.":
                    client_row["Meal Logging"] = 85
                elif client == "Michael R.":
                    client_row["Meal Logging"] = 65
                elif client == "Emma L.":
                    client_row["Meal Logging"] = 94
                else:
                    client_row["Meal Logging"] = 72
            
            if "Progress Rate" in selected_metrics:
                if client == "John D.":
                    client_row["Progress Rate"] = 78
                elif client == "Sarah M.":
                    client_row["Progress Rate"] = 86
                elif client == "Michael R.":
                    client_row["Progress Rate"] = 72
                elif client == "Emma L.":
                    client_row["Progress Rate"] = 82
                else:
                    client_row["Progress Rate"] = 70
            
            comparison_data.append(client_row)
        
        # Convert to DataFrame and display as table
        comparison_df = pd.DataFrame(comparison_data)
        st.subheader("Client Comparison")
        st.table(comparison_df)
        
        # Add simple analysis
        if len(selected_clients) >= 2 and len(selected_metrics) >= 1:
            st.subheader("Key Insights")
            
            # Find biggest difference
            for metric in selected_metrics:
                if metric in comparison_df.columns:
                    max_val = comparison_df[metric].max()
                    min_val = comparison_df[metric].min()
                    max_client = comparison_df.loc[comparison_df[metric].idxmax(), "Client"]
                    min_client = comparison_df.loc[comparison_df[metric].idxmin(), "Client"]
                    
                    if max_val - min_val > 0:
                        st.info(f"**{metric}:** {max_client} has the highest value ({max_val}) and {min_client} has the lowest ({min_val}). Difference: {max_val - min_val}.")
    else:
        st.info("Please select at least one client and one metric to compare.")

# Allergies Tab
with tab4:
    st.header("Allergy & Restriction Analysis")
    
    # Mock allergy data
    allergy_data = [
        {"Allergen": "Dairy", "Count": 28, "Percentage": "28%"},
        {"Allergen": "Gluten", "Count": 22, "Percentage": "22%"},
        {"Allergen": "Nuts", "Count": 18, "Percentage": "18%"},
        {"Allergen": "Shellfish", "Count": 12, "Percentage": "12%"},
        {"Allergen": "Eggs", "Count": 10, "Percentage": "10%"},
        {"Allergen": "Soy", "Count": 8, "Percentage": "8%"},
        {"Allergen": "Fish", "Count": 5, "Percentage": "5%"},
        {"Allergen": "Other", "Count": 15, "Percentage": "15%"}
    ]
    
    # Display as table
    allergy_df = pd.DataFrame(allergy_data)
    st.subheader("Common Allergens")
    st.table(allergy_df)
    
    # Substitution compliance
    st.subheader("Substitution Compliance")
    
    substitution_data = [
        {"Substitution": "Dairy to Plant Milk", "Compliance (%)": 85},
        {"Substitution": "Gluten to GF Grains", "Compliance (%)": 72},
        {"Substitution": "Eggs to Flax Eggs", "Compliance (%)": 64},
        {"Substitution": "Nuts to Seeds", "Compliance (%)": 78},
        {"Substitution": "Wheat to Almond Flour", "Compliance (%)": 62}
    ]
    
    substitution_df = pd.DataFrame(substitution_data)
    st.table(substitution_df)
    
    # Nutritional impact
    st.subheader("Nutritional Impact of Allergies")
    
    impact_data = [
        {"Allergen": "Dairy Allergy", "Nutrient": "Calcium", "Impact (%)": -35},
        {"Allergen": "Dairy Allergy", "Nutrient": "Vitamin D", "Impact (%)": -28},
        {"Allergen": "Dairy Allergy", "Nutrient": "Protein", "Impact (%)": -12},
        {"Allergen": "Gluten Allergy", "Nutrient": "Fiber", "Impact (%)": -25},
        {"Allergen": "Gluten Allergy", "Nutrient": "B Vitamins", "Impact (%)": -30},
        {"Allergen": "Gluten Allergy", "Nutrient": "Calories", "Impact (%)": -15},
        {"Allergen": "Nut Allergy", "Nutrient": "Healthy Fats", "Impact (%)": -32},
        {"Allergen": "Nut Allergy", "Nutrient": "Protein", "Impact (%)": -15},
        {"Allergen": "Nut Allergy", "Nutrient": "Fiber", "Impact (%)": -18}
    ]
    
    impact_df = pd.DataFrame(impact_data)
    st.table(impact_df)
    
    # Recommendations
    st.subheader("Key Recommendations")
    
    recommendations = [
        "1. **Dairy Allergies**: Focus on non-dairy calcium sources (fortified plant milks, leafy greens) and consider vitamin D supplementation.",
        "2. **Gluten Allergies**: Increase fiber from non-grain sources (vegetables, fruits) and consider B vitamin supplementation.",
        "3. **Nut Allergies**: Incorporate more seeds and avocados for healthy fats.",
        "4. **Overall Strategy**: Create specialized meal plans for common allergen combinations."
    ]
    
    for recommendation in recommendations:
        st.write(recommendation)

# Report Generation Section
st.header("Generate Nutrition Reports")

with st.form("generate_report_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        report_type = st.selectbox(
            "Report Type:",
            ["Client Summary", "Diet Compliance", "Nutrition Analysis", "Allergy Management"]
        )
        
        client_selection = st.multiselect(
            "Select clients:",
            ["John D.", "Sarah M.", "Michael R.", "Emma L.", "David W."],
            default=["John D."]
        )
    
    with col2:
        include_charts = st.checkbox("Include tables", value=True)
        include_recommendations = st.checkbox("Include recommendations", value=True)
        report_format = st.selectbox(
            "Report format:",
            ["PDF", "Excel", "Text"]
        )
    
    submit = st.form_submit_button("Generate Report")
    
    if submit:
        if client_selection:
            st.success("Report generated successfully!")
            
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
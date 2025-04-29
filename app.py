import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import base64
from io import BytesIO

from kpi_analyzer import (
    calculate_metric_scores,
    classify_metrics,
    get_top_metrics,
    detect_redundant_metrics,
    get_metrics_by_impact
)

from utils import (
    load_sample_data,
    export_to_excel,
    generate_recommendations
)

def main():
    st.set_page_config(
        page_title="KPI Audit Tool",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("🔍 KPI Audit Tool")
    st.markdown("""
    ### Identify redundant metrics and focus on what really matters for business outcomes
    Upload your KPI data to analyze which metrics are truly valuable and which ones might be creating noise.
    """)
    
    # File uploader
    uploaded_file = st.file_uploader("Upload your metrics CSV file", type=["csv"])
    
    use_sample = st.checkbox("Use sample data instead")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        analyze_data(df)
    elif use_sample:
        st.info("Using sample data from the provided Vanity Metrics dashboard.")
        df = load_sample_data()
        analyze_data(df)
    else:
        st.info("Please upload a CSV file with your metrics data or use our sample data.")
        st.markdown("""
        ### Expected CSV format:
        Your CSV should include the following columns:
        - Department
        - Metric_Name
        - Visible_in_Dashboard
        - Used_in_Decision_Making
        - Executive_Requested
        - Last_Reviewed
        - Metric_Last_Used_For_Decision
        - Interpretation_Notes
        """)

def analyze_data(df):
    st.subheader("Data Overview")
    
    # Display the raw data
    with st.expander("View Raw Data"):
        st.dataframe(df)
    
    # Calculate metric scores and classify them
    df_with_scores = calculate_metric_scores(df)
    df_classified = classify_metrics(df_with_scores)
    
    # Get redundant metrics
    redundant_metrics = detect_redundant_metrics(df_classified)
    
    # Metrics Dashboard
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Metric Health by Department")
        dept_metrics = df_classified.groupby('Department')['impact_score'].mean().reset_index()
        dept_metrics = dept_metrics.sort_values('impact_score', ascending=False)
        
        fig = px.bar(
            dept_metrics, 
            x='Department', 
            y='impact_score',
            color='impact_score',
            color_continuous_scale='RdYlGn',
            title="Average Metric Impact by Department"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Metric Categories")
        
        categories = df_classified['category'].value_counts().reset_index()
        categories.columns = ['Category', 'Count']
        
        fig = px.pie(
            categories, 
            values='Count', 
            names='Category',
            color='Category',
            color_discrete_map={
                'High Impact': '#4CAF50',
                'Medium Impact': '#FFC107',
                'Low Impact': '#FF5722',
            },
            title="Distribution of Metric Categories"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Top metrics recommendations
    st.subheader("Top Recommended Metrics")
    top_metrics = get_top_metrics(df_classified, n=3)
    
    col1, col2, col3 = st.columns(3)
    
    for i, (idx, metric) in enumerate(top_metrics.iterrows()):
        with [col1, col2, col3][i]:
            st.markdown(f"### {i+1}. {metric['Metric_Name']}")
            st.markdown(f"**Department:** {metric['Department']}")
            st.markdown(f"**Impact Score:** {metric['impact_score']:.2f}")
            st.markdown(f"**Used in Decision Making:** {metric['Used_in_Decision_Making']}")
            st.markdown(f"**Last Used:** {metric['Metric_Last_Used_For_Decision']}")
            if not pd.isna(metric['Interpretation_Notes']):
                st.markdown(f"**Notes:** {metric['Interpretation_Notes']}")
    
    # Recommendations based on analysis
    st.subheader("AI Recommendations")
    recommendations = generate_recommendations(df_classified, redundant_metrics)
    st.markdown(recommendations)
    
    # Detailed Metric Analysis
    st.subheader("Detailed Metric Analysis")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_department = st.selectbox(
            "Filter by Department",
            options=["All"] + sorted(df['Department'].unique().tolist())
        )
    
    with col2:
        selected_category = st.selectbox(
            "Filter by Impact Category",
            options=["All", "High Impact", "Medium Impact", "Low Impact"]
        )
    
    with col3:
        sort_by = st.selectbox(
            "Sort by",
            options=["Impact Score (High to Low)", "Impact Score (Low to High)", "Department"]
        )
    
    # Apply filters
    filtered_df = df_classified.copy()
    
    if selected_department != "All":
        filtered_df = filtered_df[filtered_df['Department'] == selected_department]
    
    if selected_category != "All":
        filtered_df = filtered_df[filtered_df['category'] == selected_category]
    
    # Apply sorting
    if sort_by == "Impact Score (High to Low)":
        filtered_df = filtered_df.sort_values('impact_score', ascending=False)
    elif sort_by == "Impact Score (Low to High)":
        filtered_df = filtered_df.sort_values('impact_score', ascending=True)
    elif sort_by == "Department":
        filtered_df = filtered_df.sort_values('Department')
    
    # Display metrics table with scores
    display_cols = ['Department', 'Metric_Name', 'impact_score', 'category', 'Used_in_Decision_Making', 
                   'Visible_in_Dashboard', 'Last_Reviewed', 'redundant', 'Interpretation_Notes']
    
    # Rename columns for better display
    display_df = filtered_df[display_cols].copy()
    display_df.columns = ['Department', 'Metric Name', 'Impact Score', 'Category', 'Used in Decisions', 
                         'In Dashboard', 'Last Reviewed', 'Redundant', 'Notes']
    
    st.dataframe(display_df, use_container_width=True)
    
    # Redundant Metrics Section
    if len(redundant_metrics) > 0:
        st.subheader("Redundant Metrics")
        st.markdown("These metrics may be redundant or overlapping with others. Consider consolidating or removing them:")
        
        redundant_df = df_classified[df_classified['redundant'] == True]
        
        # Group by redundant groups
        redundant_groups = {}
        for _, row in redundant_df.iterrows():
            key = f"{row['Department']}_{row['Metric_Name']}"
            if key not in redundant_groups:
                redundant_groups[key] = []
            
            redundant_groups[key].append({
                'Department': row['Department'],
                'Metric_Name': row['Metric_Name'],
                'impact_score': row['impact_score'],
                'Notes': row['Interpretation_Notes']
            })
        
        for i, (key, group) in enumerate(redundant_groups.items()):
            st.markdown(f"**Group {i+1}:** {key.split('_')[1]} ({key.split('_')[0]})")
            
            for item in group:
                st.markdown(f"- **{item['Metric_Name']}** (Impact: {item['impact_score']:.2f}) - {item['Notes']}")
            
            st.markdown("---")
    
    # Export Options
    st.subheader("Export Analysis")
    
    if st.button("Export to Excel"):
        excel_file = export_to_excel(df_classified)
        
        # Create a download link
        b64 = base64.b64encode(excel_file.getvalue()).decode()
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="kpi_analysis.xlsx">Download Excel file</a>'
        st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

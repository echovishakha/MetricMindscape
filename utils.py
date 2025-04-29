import pandas as pd
import io
import os
import base64
import streamlit as st

def load_sample_data():
    """
    Load sample data for demonstration
    """
    # Try to load the sample data from the file
    try:
        df = pd.read_csv("sample_data/week2_vanity_metrics.csv")
        return df
    except:
        # If file doesn't exist, load from the attached CSV
        try:
            df = pd.read_csv("attached_assets/week 2 - Problem_4_-_Vanity_Metrics_Dashboard__Revised_.csv")
            
            # Ensure the directory exists
            os.makedirs("sample_data", exist_ok=True)
            
            # Save it to the sample_data directory for future use
            df.to_csv("sample_data/week2_vanity_metrics.csv", index=False)
            
            return df
        except Exception as e:
            # If both methods fail, create a minimal dataset
            st.error(f"Failed to load sample data: {e}")
            # Return an empty DataFrame with the expected columns
            return pd.DataFrame(columns=[
                "Department", "Metric_Name", "Visible_in_Dashboard", 
                "Used_in_Decision_Making", "Executive_Requested", 
                "Last_Reviewed", "Metric_Last_Used_For_Decision", "Interpretation_Notes"
            ])

def export_to_excel(df):
    """
    Export the analysis results to Excel
    """
    output = io.BytesIO()
    
    # Create a Pandas Excel writer using the BytesIO object
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    
    # Create sheets for different categories
    df.to_excel(writer, sheet_name='All Metrics', index=False)
    
    # Add sheets for different impact categories
    for category in ['High Impact', 'Medium Impact', 'Low Impact']:
        category_df = df[df['category'] == category]
        if not category_df.empty:
            category_df.to_excel(writer, sheet_name=category, index=False)
    
    # Add a sheet for redundant metrics
    redundant_df = df[df['redundant'] == True]
    if not redundant_df.empty:
        redundant_df.to_excel(writer, sheet_name='Redundant Metrics', index=False)
    
    # Add recommendations sheet
    recommendations = generate_recommendations(df, redundant_df.index.tolist())
    recommendations_df = pd.DataFrame({
        'Recommendations': [recommendations]
    })
    recommendations_df.to_excel(writer, sheet_name='Recommendations', index=False)
    
    writer.close()
    
    # Reset the buffer position to the beginning
    output.seek(0)
    
    return output

def generate_recommendations(df, redundant_metrics):
    """
    Generate AI recommendations based on the metric analysis
    """
    # Count metrics by category
    high_impact = len(df[df['category'] == 'High Impact'])
    medium_impact = len(df[df['category'] == 'Medium Impact'])
    low_impact = len(df[df['category'] == 'Low Impact'])
    
    # Count metrics by department
    dept_counts = df.groupby('Department').size()
    most_metrics_dept = dept_counts.idxmax()
    
    # Calculate percentage of metrics actually used in decision making
    decision_making_pct = (df['Used_in_Decision_Making'].sum() / len(df)) * 100
    
    # Count redundant metrics
    redundant_count = len(redundant_metrics)
    
    # Generate recommendations
    recommendations = f"""
    ### Key Findings:
    
    - **{high_impact} high-impact** metrics identified that drive business outcomes
    - **{low_impact} low-impact** metrics that could be considered for removal
    - **{redundant_count} redundant** metrics that overlap or duplicate information
    - Only **{decision_making_pct:.1f}%** of your metrics are actively used for decision making
    
    ### Recommendations:
    
    1. **Consolidate Redundant Metrics**: {redundant_count} metrics appear to measure similar things across departments.
       Consider centralizing these for consistency and reduced overhead.
    
    2. **Review Low-Impact Metrics**: {low_impact} metrics were classified as low-impact. These should be evaluated
       for removal from dashboards to reduce noise and focus attention on what matters.
    
    3. **Department Focus**: The {most_metrics_dept} department has the most metrics. Consider reviewing which
       ones truly align with strategic goals and eliminating the rest.
    
    4. **Decision-Making Alignment**: Consider removing dashboard metrics that aren't actively used in decision-making
       processes to improve dashboard focus.
    
    ### Next Steps:
    
    1. Review the top recommended metrics and ensure they are given visibility across the organization
    2. Schedule a metric review workshop to discuss the low-impact metrics with stakeholders
    3. Create a metric governance process to regularly evaluate metric relevance and impact
    """
    
    return recommendations

# File comments for documentation only
# This sample data is used for the KPI Audit Tool

import pandas as pd
import io
import os
import base64

def load_sample_data():
    """
    Load sample data for demonstration
    """
    # Try to load the sample data from the file
    try:
        df = pd.read_csv("sample_data/week2_vanity_metrics.csv")
        return df
    except:
        # If file doesn't exist, create data from the attached CSV
        data = """Department,Metric_Name,Visible_in_Dashboard,Used_in_Decision_Making,Executive_Requested,Last_Reviewed,Metric_Last_Used_For_Decision,Interpretation_Notes
Marketing,OKR Progress,No,No,No,This week,2 weeks ago,Drives vanity OKRs
Finance,Leads Generated,Yes,No,No,Last month,Used in QBR,Tied to real goals
Engineering,OKR Progress,Yes,Yes,Yes,Last month,Recently,Auto-synced from tool
Engineering,Daily Active Users,Yes,No,No,Last quarter,Last quarter,Auto-synced from tool
Finance,Code Commits,Yes,No,No,Unknown,Recently,Updated manually
Operations,Email Open Rate,Yes,No,Yes,Unknown,Don't know,Updated manually
Operations,Net Revenue Retention,Yes,No,No,Last quarter,Don't know,Tied to real goals
Marketing,Demo Requests,No,Yes,No,Last month,2 weeks ago,Tied to real goals
Engineering,Revenue,Yes,Yes,No,Last quarter,Last quarter,Used for optics only
Finance,Customer Churn,No,No,No,This week,Used in QBR,Drives vanity OKRs
Sales,Ticket Resolution Time,Yes,No,No,Unknown,Last quarter,Auto-synced from tool
Finance,Ticket Resolution Time,Yes,No,No,Last quarter,Last quarter,Frequently discussed
Sales,Slack Messages Sent,Yes,Yes,No,Last quarter,Don't know,Tied to real goals
Support,New Signups,Yes,No,No,Last quarter,2 weeks ago,Updated manually
Engineering,Customer Escalations,No,No,No,Last month,2 weeks ago,Updated manually
Product,Bug Count,Yes,No,No,Unknown,Last quarter,Tied to real goals
Operations,Ticket Resolution Time,Yes,No,No,Last month,Used in QBR,Unclear ownership
Support,Demo Requests,Yes,Yes,Yes,Last month,2 weeks ago,Tied to real goals
Marketing,Test Coverage,Yes,No,No,This week,2 weeks ago,Drives vanity OKRs
Engineering,Deployment Frequency,No,No,No,Unknown,Never,Tied to real goals
Product,Internal NPS,Yes,Yes,No,This week,Recently,Drives vanity OKRs
Operations,Deployment Frequency,Yes,No,No,Last month,2 weeks ago,Updated manually
Marketing,Internal NPS,Yes,No,No,Unknown,Last quarter,Frequently discussed
Operations,Customer Touchpoints,No,No,No,This week,Last quarter,Auto-synced from tool
Support,Daily Active Users,Yes,No,No,This week,Never,Auto-synced from tool
Engineering,Customer Escalations,Yes,Yes,No,Unknown,2 weeks ago,Auto-synced from tool
Finance,Customer Escalations,Yes,Yes,No,Unknown,Last quarter,Auto-synced from tool
Marketing,Slack Messages Sent,No,Yes,No,Last quarter,Never,Auto-synced from tool
Engineering,Demo Requests,Yes,No,No,Last month,Don't know,Often misinterpreted
Marketing,Daily Active Users,Yes,Yes,No,Last quarter,Don't know,Unclear ownership
Product,Leads Generated,Yes,Yes,No,Unknown,Recently,Drives vanity OKRs
Support,Code Commits,Yes,No,No,Last month,Don't know,Tied to real goals
Operations,Code Commits,Yes,No,No,Last quarter,Used in QBR,Unclear ownership
Marketing,Meetings Booked,Yes,No,No,Last month,Used in QBR,Auto-synced from tool
Finance,Revenue,Yes,No,No,This week,2 weeks ago,Frequently discussed
Finance,App Crashes,No,No,Yes,Unknown,Don't know,Updated manually
Marketing,OKR Progress,Yes,Yes,No,This week,Recently,Often misinterpreted
Product,Bug Count,Yes,Yes,No,This week,Recently,Updated manually
Sales,App Crashes,No,No,No,Unknown,Recently,Used for optics only
Marketing,Customer Escalations,Yes,No,No,This week,Used in QBR,Drives vanity OKRs
Finance,Customer Touchpoints,Yes,No,No,This week,Never,Often misinterpreted
Finance,Customer Escalations,No,No,No,Last month,Recently,Tied to real goals
Product,App Crashes,Yes,Yes,Yes,This week,Used in QBR,Used for optics only
Operations,Email Open Rate,Yes,Yes,Yes,This week,Recently,Often misinterpreted
Engineering,Customer Escalations,Yes,Yes,Yes,Unknown,Last quarter,Frequently discussed
Engineering,Customer Churn,Yes,Yes,No,Last month,Used in QBR,Auto-synced from tool
Engineering,Customer Escalations,Yes,Yes,No,Last month,Recently,Tied to real goals
Product,Slack Messages Sent,Yes,No,No,Unknown,2 weeks ago,Frequently discussed
Product,Net Revenue Retention,No,No,No,Unknown,Last quarter,Used for optics only
Product,OKR Progress,Yes,No,No,Last month,Never,Tied to real goals
Operations,App Crashes,No,Yes,No,Unknown,Recently,Drives vanity OKRs
Sales,Slack Messages Sent,Yes,No,Yes,Unknown,2 weeks ago,Auto-synced from tool
Engineering,Customer Churn,Yes,No,No,This week,Last quarter,Unclear ownership
Operations,Demo Requests,Yes,No,No,Last quarter,2 weeks ago,Updated manually
Sales,Customer Churn,Yes,No,No,Last month,Recently,Tied to real goals
Sales,Ticket Resolution Time,Yes,No,No,Unknown,Never,Auto-synced from tool
Product,Leads Generated,No,No,Yes,Unknown,Last quarter,Auto-synced from tool
Product,Time on Site,No,Yes,No,Last month,Never,Often misinterpreted
Engineering,Demo Requests,No,No,No,Last month,Last quarter,Auto-synced from tool
Finance,Demo Requests,Yes,No,No,Last quarter,Don't know,Frequently discussed"""
        
        # Ensure the directory exists
        os.makedirs("sample_data", exist_ok=True)
        
        # Write data to file
        with open("sample_data/week2_vanity_metrics.csv", "w") as f:
            f.write(data)
        
        # Return dataframe
        df = pd.read_csv(io.StringIO(data))
        return df

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

## file_path: sample_data/week2_vanity_metrics.csv
```csv
Department,Metric_Name,Visible_in_Dashboard,Used_in_Decision_Making,Executive_Requested,Last_Reviewed,Metric_Last_Used_For_Decision,Interpretation_Notes
Marketing,OKR Progress,No,No,No,This week,2 weeks ago,Drives vanity OKRs
Finance,Leads Generated,Yes,No,No,Last month,Used in QBR,Tied to real goals
Engineering,OKR Progress,Yes,Yes,Yes,Last month,Recently,Auto-synced from tool
Engineering,Daily Active Users,Yes,No,No,Last quarter,Last quarter,Auto-synced from tool
Finance,Code Commits,Yes,No,No,Unknown,Recently,Updated manually
Operations,Email Open Rate,Yes,No,Yes,Unknown,Don't know,Updated manually
Operations,Net Revenue Retention,Yes,No,No,Last quarter,Don't know,Tied to real goals
Marketing,Demo Requests,No,Yes,No,Last month,2 weeks ago,Tied to real goals
Engineering,Revenue,Yes,Yes,No,Last quarter,Last quarter,Used for optics only
Finance,Customer Churn,No,No,No,This week,Used in QBR,Drives vanity OKRs
Sales,Ticket Resolution Time,Yes,No,No,Unknown,Last quarter,Auto-synced from tool
Finance,Ticket Resolution Time,Yes,No,No,Last quarter,Last quarter,Frequently discussed
Sales,Slack Messages Sent,Yes,Yes,No,Last quarter,Don't know,Tied to real goals
Support,New Signups,Yes,No,No,Last quarter,2 weeks ago,Updated manually
Engineering,Customer Escalations,No,No,No,Last month,2 weeks ago,Updated manually
Product,Bug Count,Yes,No,No,Unknown,Last quarter,Tied to real goals
Operations,Ticket Resolution Time,Yes,No,No,Last month,Used in QBR,Unclear ownership
Support,Demo Requests,Yes,Yes,Yes,Last month,2 weeks ago,Tied to real goals
Marketing,Test Coverage,Yes,No,No,This week,2 weeks ago,Drives vanity OKRs
Engineering,Deployment Frequency,No,No,No,Unknown,Never,Tied to real goals
Product,Internal NPS,Yes,Yes,No,This week,Recently,Drives vanity OKRs
Operations,Deployment Frequency,Yes,No,No,Last month,2 weeks ago,Updated manually
Marketing,Internal NPS,Yes,No,No,Unknown,Last quarter,Frequently discussed
Operations,Customer Touchpoints,No,No,No,This week,Last quarter,Auto-synced from tool
Support,Daily Active Users,Yes,No,No,This week,Never,Auto-synced from tool
Engineering,Customer Escalations,Yes,Yes,No,Unknown,2 weeks ago,Auto-synced from tool
Finance,Customer Escalations,Yes,Yes,No,Unknown,Last quarter,Auto-synced from tool
Marketing,Slack Messages Sent,No,Yes,No,Last quarter,Never,Auto-synced from tool
Engineering,Demo Requests,Yes,No,No,Last month,Don't know,Often misinterpreted
Marketing,Daily Active Users,Yes,Yes,No,Last quarter,Don't know,Unclear ownership
Product,Leads Generated,Yes,Yes,No,Unknown,Recently,Drives vanity OKRs
Support,Code Commits,Yes,No,No,Last month,Don't know,Tied to real goals
Operations,Code Commits,Yes,No,No,Last quarter,Used in QBR,Unclear ownership
Marketing,Meetings Booked,Yes,No,No,Last month,Used in QBR,Auto-synced from tool
Finance,Revenue,Yes,No,No,This week,2 weeks ago,Frequently discussed
Finance,App Crashes,No,No,Yes,Unknown,Don't know,Updated manually
Marketing,OKR Progress,Yes,Yes,No,This week,Recently,Often misinterpreted
Product,Bug Count,Yes,Yes,No,This week,Recently,Updated manually
Sales,App Crashes,No,No,No,Unknown,Recently,Used for optics only
Marketing,Customer Escalations,Yes,No,No,This week,Used in QBR,Drives vanity OKRs
Finance,Customer Touchpoints,Yes,No,No,This week,Never,Often misinterpreted
Finance,Customer Escalations,No,No,No,Last month,Recently,Tied to real goals
Product,App Crashes,Yes,Yes,Yes,This week,Used in QBR,Used for optics only
Operations,Email Open Rate,Yes,Yes,Yes,This week,Recently,Often misinterpreted
Engineering,Customer Escalations,Yes,Yes,Yes,Unknown,Last quarter,Frequently discussed
Engineering,Customer Churn,Yes,Yes,No,Last month,Used in QBR,Auto-synced from tool
Engineering,Customer Escalations,Yes,Yes,No,Last month,Recently,Tied to real goals
Product,Slack Messages Sent,Yes,No,No,Unknown,2 weeks ago,Frequently discussed
Product,Net Revenue Retention,No,No,No,Unknown,Last quarter,Used for optics only
Product,OKR Progress,Yes,No,No,Last month,Never,Tied to real goals
Operations,App Crashes,No,Yes,No,Unknown,Recently,Drives vanity OKRs
Sales,Slack Messages Sent,Yes,No,Yes,Unknown,2 weeks ago,Auto-synced from tool
Engineering,Customer Churn,Yes,No,No,This week,Last quarter,Unclear ownership
Operations,Demo Requests,Yes,No,No,Last quarter,2 weeks ago,Updated manually
Sales,Customer Churn,Yes,No,No,Last month,Recently,Tied to real goals
Sales,Ticket Resolution Time,Yes,No,No,Unknown,Never,Auto-synced from tool
Product,Leads Generated,No,No,Yes,Unknown,Last quarter,Auto-synced from tool
Product,Time on Site,No,Yes,No,Last month,Never,Often misinterpreted
Engineering,Demo Requests,No,No,No,Last month,Last quarter,Auto-synced from tool
Finance,Demo Requests,Yes,No,No,Last quarter,Don't know,Frequently discussed

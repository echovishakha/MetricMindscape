import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import datetime

def calculate_metric_scores(df):
    """
    Calculate impact scores for each metric based on various factors
    """
    # Create a copy of the dataframe
    df_scored = df.copy()
    
    # Convert boolean columns
    bool_columns = ['Visible_in_Dashboard', 'Used_in_Decision_Making', 'Executive_Requested']
    for col in bool_columns:
        df_scored[col] = df_scored[col].map({'Yes': 1, 'No': 0})
    
    # Convert review frequency to numerical values
    review_map = {
        'This week': 5,
        'Last month': 4,
        'Last quarter': 3,
        'Unknown': 1
    }
    df_scored['review_score'] = df_scored['Last_Reviewed'].map(review_map)
    df_scored['review_score'] = df_scored['review_score'].fillna(1)
    
    # Convert last used for decision to numerical values
    usage_map = {
        'Recently': 5,
        '2 weeks ago': 4,
        'Last quarter': 3,
        'Used in QBR': 3,
        'Never': 0,
        "Don't know": 1
    }
    df_scored['usage_score'] = df_scored['Metric_Last_Used_For_Decision'].map(usage_map)
    df_scored['usage_score'] = df_scored['usage_score'].fillna(1)
    
    # Create interpretation quality score
    interpretation_map = {
        'Tied to real goals': 5,
        'Auto-synced from tool': 4,
        'Frequently discussed': 3,
        'Updated manually': 2,
        'Used for optics only': 1,
        'Drives vanity OKRs': 0,
        'Often misinterpreted': 0,
        'Unclear ownership': 1
    }
    df_scored['interpretation_score'] = df_scored['Interpretation_Notes'].map(interpretation_map)
    df_scored['interpretation_score'] = df_scored['interpretation_score'].fillna(2)
    
    # Calculate the impact score
    # Weight factors: decision usage (highest), review frequency, interpretation quality, executive requested
    df_scored['impact_score'] = (
        (df_scored['Used_in_Decision_Making'] * 3) +  # Highest weight
        (df_scored['review_score'] * 0.5) + 
        (df_scored['usage_score'] * 1.5) +
        (df_scored['interpretation_score'] * 2) +
        (df_scored['Executive_Requested'] * 0.5)  # Lower weight since executives might request vanity metrics
    )
    
    # Normalize the score to 0-10 scale
    max_possible = 3 + 0.5*5 + 1.5*5 + 2*5 + 0.5
    df_scored['impact_score'] = df_scored['impact_score'] * 10 / max_possible
    
    # Flag potentially redundant metrics (for now just initialize the column)
    df_scored['redundant'] = False
    
    return df_scored

def classify_metrics(df):
    """
    Classify metrics into categories based on their impact scores
    """
    df_classified = df.copy()
    
    # Define thresholds for classification
    high_threshold = 7.0
    medium_threshold = 4.0
    
    # Classify metrics
    conditions = [
        (df_classified['impact_score'] >= high_threshold),
        (df_classified['impact_score'] >= medium_threshold) & (df_classified['impact_score'] < high_threshold),
        (df_classified['impact_score'] < medium_threshold)
    ]
    categories = ['High Impact', 'Medium Impact', 'Low Impact']
    
    df_classified['category'] = np.select(conditions, categories, default='Uncategorized')
    
    return df_classified

def get_top_metrics(df, n=3):
    """
    Get the top n most impactful metrics
    """
    # Get metrics that are used in decision making and have high impact
    decision_metrics = df[df['Used_in_Decision_Making'] == 1]
    
    # If we don't have enough decision-making metrics, just get the top by impact score
    if len(decision_metrics) < n:
        return df.sort_values('impact_score', ascending=False).head(n)
    
    # Otherwise, get the top metrics from those used in decision making
    return decision_metrics.sort_values('impact_score', ascending=False).head(n)

def detect_redundant_metrics(df):
    """
    Detect potentially redundant metrics based on similarities
    """
    df_redundant = df.copy()
    
    # Group by department and metric name to find duplicates
    grouped = df_redundant.groupby(['Department', 'Metric_Name'])
    
    redundant_metrics = []
    
    # For each metric, check if there are multiple instances or similar metrics
    for department in df_redundant['Department'].unique():
        dept_metrics = df_redundant[df_redundant['Department'] == department]
        
        # If a department has the same metric name multiple times, mark as redundant
        metric_counts = dept_metrics['Metric_Name'].value_counts()
        duplicate_metrics = metric_counts[metric_counts > 1].index.tolist()
        
        for metric in duplicate_metrics:
            duplicate_rows = dept_metrics[dept_metrics['Metric_Name'] == metric].index.tolist()
            redundant_metrics.extend(duplicate_rows)
    
    # Cross-department redundancy detection
    # For each metric name, check if it appears in multiple departments
    for metric_name in df_redundant['Metric_Name'].unique():
        metric_depts = df_redundant[df_redundant['Metric_Name'] == metric_name]['Department'].unique()
        
        if len(metric_depts) > 1:
            # This metric appears in multiple departments, potentially redundant
            cross_dept_redundant = df_redundant[df_redundant['Metric_Name'] == metric_name].index.tolist()
            redundant_metrics.extend(cross_dept_redundant)
    
    # Mark redundant metrics in the dataframe
    df_redundant.loc[redundant_metrics, 'redundant'] = True
    
    return redundant_metrics

def get_metrics_by_impact(df, category):
    """
    Get metrics filtered by impact category
    """
    return df[df['category'] == category]

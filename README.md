# KPI Audit Tool

## Overview
The KPI Audit Tool is an AI-powered application that helps businesses identify which metrics truly matter for business outcomes and which ones are creating unnecessary noise. It analyzes your current KPIs, detects redundancies, and recommends the most impactful metrics for your organization.

## Problem Statement
Many organizations track dozens of metrics but only a few actually drive business outcomes. This tool helps you cut through the noise:

- **Sales teams** tracking "calls made per day" where reps call voicemails just to hit numbers
- **Design teams** hitting 100% "feedback resolution rate" by auto-responding "thanks!" 
- **Dashboards with 27 KPIs** where only 2-3 actually matter

## Features

### 🔍 Comprehensive Metric Analysis
- Calculate impact scores for each metric based on multiple factors
- Classify metrics into high, medium, and low impact categories
- Visualize metric health by department

### 🔄 Redundancy Detection
- Identify metrics that duplicate information across departments
- Detect metrics measuring the same things in different ways
- Provide recommendations for consolidation

### 📊 Visual Insights
- Interactive charts and graphs to visualize impact scores
- Department-specific metric health analysis
- Categorized view of metrics by importance

### 💡 AI Recommendations
- Get specific recommendations on which metrics to keep, modify, or eliminate
- Identify which departments have metric overload
- Suggest governance processes for future metric management

## Technical Implementation

- **Frontend**: Streamlit web application
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **Analysis**: Scikit-learn for advanced metric classification
- **Export Capabilities**: Excel export with XlsxWriter

## How to Use

1. **Upload Data**: Upload your metrics CSV file or use the sample data
2. **Review Analysis**: Examine the generated dashboards and visualizations
3. **Explore Recommendations**: Review the AI-generated recommendations
4. **Filter Results**: Use the filtering options to focus on specific departments or impact categories
5. **Export**: Export the complete analysis to Excel for further review

## CSV Format
Your CSV should include the following columns:
- Department
- Metric_Name
- Visible_in_Dashboard (Yes/No)
- Used_in_Decision_Making (Yes/No)
- Executive_Requested (Yes/No)
- Last_Reviewed (This week/Last month/Last quarter/Unknown)
- Metric_Last_Used_For_Decision (Recently/2 weeks ago/Last quarter/Never/Don't know/Used in QBR)
- Interpretation_Notes (Text describing metric quality, such as "Tied to real goals", "Auto-synced from tool", etc.)

### Template Available
The tool includes a downloadable CSV template that you can use as a starting point for your own metrics data.

## Development

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/kpi-audit-tool.git

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### Dependencies
- streamlit
- pandas
- numpy
- plotly
- scikit-learn
- xlsxwriter

## License
MIT License

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

---

Developed for better data-driven decision making.
"""
Functions for analyzing birth patterns by decade and gender
"""
import pandas as pd

def births_by_decade_analysis(data):
    """Analyze births by decade and gender"""
    # Group by decade for easier analysis
    data['decade'] = (data['year'] // 10) * 10
    
    # Create summary table
    summary_table = data.groupby(['decade', 'gender'])['births'].sum().unstack(fill_value=0)
    
    # Calculate totals for each decade
    decade_totals = {}
    for decade in sorted(data['decade'].unique()):
        decade_subset = data[data['decade'] == decade]
        females = decade_subset[decade_subset['gender'] == 'F']['births'].sum()
        males = decade_subset[decade_subset['gender'] == 'M']['births'].sum()
        total = females + males
        decade_totals[decade] = {'female': females, 'male': males, 'total': total}
    
    return data
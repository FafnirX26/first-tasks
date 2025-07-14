"""
Analysis of yearly birth trends and visualization
"""
import pandas as pd
import matplotlib.pyplot as plt

def yearly_birth_trends(data):
    """Look at how birth rates changed over time"""
    
    # Group births by year 
    births_per_year = data.groupby('year')['births'].sum()
    
    # Make a simple line plot
    plt.figure(figsize=(12, 6))
    plt.plot(births_per_year.index, births_per_year.values, 'o-', linewidth=2)
    plt.title('Total Births by Year')
    plt.xlabel('Year')
    plt.ylabel('Total Births')
    plt.grid(True, alpha=0.3)
    
    # Format y-axis labels 
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
    
    # Calculate basic stats
    min_year = births_per_year.idxmin()
    max_year = births_per_year.idxmax()
    
    # Look at decade changes
    data_copy = data.copy()
    data_copy['decade'] = (data_copy['year'] // 10) * 10
    decade_totals = data_copy.groupby('decade')['births'].sum()
    decade_years = data_copy.groupby('decade')['year'].nunique()
    decade_averages = decade_totals / decade_years
    
    # Calculate decade changes for analysis
    decade_changes = []
    for i in range(1, len(decade_averages)):
        current_decade = decade_averages.index[i]
        previous_decade = decade_averages.index[i-1]
        current_avg = decade_averages.iloc[i]
        previous_avg = decade_averages.iloc[i-1]
        
        pct_change = ((current_avg - previous_avg) / previous_avg) * 100
        decade_changes.append((previous_decade, current_decade, pct_change))
    
    plt.tight_layout()
    plt.savefig('births_by_year.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    return births_per_year
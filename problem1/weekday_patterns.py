"""
Analysis of birth patterns by day of the week
"""
import pandas as pd
import matplotlib.pyplot as plt

def weekday_birth_patterns(data):
    """Check if births vary by day of week for 1960s, 1970s, 1980s"""
    
    # Need to create actual dates to get weekdays
    clean_data = data.dropna(subset=['day']).copy()
    clean_data['day'] = clean_data['day'].astype(int)
    
    # Build date strings and convert to datetime
    clean_data['date_str'] = (clean_data['year'].astype(str) + '-' + 
                             clean_data['month'].astype(str).str.zfill(2) + '-' + 
                             clean_data['day'].astype(str).str.zfill(2))
    
    clean_data['actual_date'] = pd.to_datetime(clean_data['date_str'], errors='coerce')
    clean_data = clean_data.dropna(subset=['actual_date'])
    
    clean_data['weekday'] = clean_data['actual_date'].dt.day_name()
    clean_data['decade'] = (clean_data['year'] // 10) * 10
    
    # Focus on three decades as requested
    decades_to_check = [1960, 1970, 1980]
    subset = clean_data[clean_data['decade'].isin(decades_to_check)]
    
    # Sum up births by weekday for each decade
    weekday_summary = subset.groupby(['decade', 'weekday'])['births'].sum().reset_index()
    
    # Create comparison charts
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    for i, decade in enumerate(decades_to_check):
        decade_data = weekday_summary[weekday_summary['decade'] == decade]
        decade_data = decade_data.set_index('weekday').reindex(days)
        
        # Color weekends differently
        bar_colors = ['lightblue' if day in ['Saturday', 'Sunday'] else 'salmon' for day in days]
        axes[i].bar(range(len(days)), decade_data['births'], color=bar_colors)
        axes[i].set_title(f'{decade}s')
        axes[i].set_xlabel('Day')
        axes[i].set_ylabel('Total Births')
        axes[i].set_xticks(range(len(days)))
        axes[i].set_xticklabels([day[:3] for day in days], rotation=45)
        axes[i].grid(True, alpha=0.3)
        
        # Format numbers
        axes[i].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
        
        # Store the numbers for analysis
        decade_breakdown = {}
        for day in days:
            count = decade_data.loc[day, 'births'] if day in decade_data.index else 0
            decade_breakdown[day] = count
    
    plt.suptitle('Birth Patterns by Day of Week')
    plt.tight_layout()
    plt.savefig('births_by_weekday.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    return weekday_summary
"""
Analysis of seasonal birth patterns throughout the year
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def seasonal_birth_analysis(data):
    """Examine seasonal patterns in births throughout the year"""
    
    # Work with clean data
    clean_data = data.dropna(subset=['day']).copy()
    clean_data['day'] = clean_data['day'].astype(int)
    
    # Get average births for each date (month-day combo)
    daily_averages = clean_data.groupby(['month', 'day'])['births'].mean().reset_index()
    daily_averages['date_label'] = (daily_averages['month'].astype(str).str.zfill(2) + '-' + 
                                   daily_averages['day'].astype(str).str.zfill(2))
    
    # Use 2000 as a dummy year for plotting
    daily_averages['plotting_date'] = pd.to_datetime('2000-' + daily_averages['date_label'], errors='coerce')
    daily_averages = daily_averages.dropna(subset=['plotting_date']).sort_values('plotting_date')
    
    # Create the time series plot
    plt.figure(figsize=(14, 7))
    plt.plot(daily_averages['plotting_date'], daily_averages['births'], linewidth=1.2, color='navy')
    
    # Overlay monthly averages 
    monthly_data = clean_data.groupby('month')['births'].mean()
    month_midpoints = pd.to_datetime([f'2000-{m:02d}-15' for m in range(1, 13)])
    plt.plot(month_midpoints, monthly_data.values, 'ro-', linewidth=2, markersize=5, 
             label='Monthly averages', alpha=0.8)
    
    plt.title('Average Births Throughout the Year')
    plt.xlabel('Month')
    plt.ylabel('Average Daily Births')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Format x-axis nicely
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('births_by_date_of_year.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Find interesting dates
    peak_day = daily_averages.loc[daily_averages['births'].idxmax()]
    low_day = daily_averages.loc[daily_averages['births'].idxmin()]
    
    # Store key findings
    key_findings = {
        'highest_births': {'date': peak_day['date_label'], 'count': peak_day['births']},
        'lowest_births': {'date': low_day['date_label'], 'count': low_day['births']}
    }
    
    # Calculate monthly breakdown
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    monthly_breakdown = {}
    for i, (month_num, avg) in enumerate(monthly_data.items()):
        monthly_breakdown[months[i]] = avg
    
    # Compare seasons
    spring = monthly_data[3:6].mean()  # Mar-May
    summer = monthly_data[6:9].mean()  # Jun-Aug  
    fall = monthly_data[9:12].mean()   # Sep-Nov
    winter = monthly_data[[12, 1, 2]].mean()  # Dec, Jan, Feb
    
    # Store seasonal comparison
    seasonal_comparison = {
        'Spring': spring,
        'Summer': summer, 
        'Fall': fall,
        'Winter': winter
    }
    
    return daily_averages
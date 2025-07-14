"""
Configuration settings for the CDC births analysis
"""

# Data file settings
DATA_FILE = 'CDCbirths.csv'

# Plot settings
PLOT_STYLE = {
    'figure_size': (12, 6),
    'line_width': 2,
    'grid_alpha': 0.3,
    'dpi': 150
}

# Analysis settings
WEEKDAY_DECADES = [1960, 1970, 1980]  # Decades to analyze for weekday patterns
WEEKDAY_ORDER = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Color schemes
WEEKDAY_COLORS = {
    'weekday': 'salmon',
    'weekend': 'lightblue'
}

SEASONAL_COLORS = {
    'daily_line': 'navy',
    'monthly_points': 'red'
}

# Month names for display
MONTH_NAMES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
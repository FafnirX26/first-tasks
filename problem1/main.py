"""
Main script to run all CDC births data analyses

This script coordinates the different analysis modules to provide
a comprehensive look at birth patterns in the CDC dataset.
"""
import sys
import os

# Add the current directory to path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_loader import load_and_explore_data
from decade_analysis import births_by_decade_analysis
from yearly_trends import yearly_birth_trends
from weekday_patterns import weekday_birth_patterns
from seasonal_analysis import seasonal_birth_analysis

def main():
    """Run the complete analysis pipeline"""
    # Load and explore the dataset
    birth_data = load_and_explore_data('CDCbirths.csv')
    
    # Run each analysis module
    birth_data = births_by_decade_analysis(birth_data)
    yearly_trends = yearly_birth_trends(birth_data)  
    weekday_patterns = weekday_birth_patterns(birth_data)
    seasonal_patterns = seasonal_birth_analysis(birth_data)
    
    # Analysis complete - visualizations saved to PNG files
    return birth_data, yearly_trends, weekday_patterns, seasonal_patterns

if __name__ == "__main__":
    main()
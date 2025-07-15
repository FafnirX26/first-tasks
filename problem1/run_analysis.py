import argparse
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_loader import load_and_explore_data
from decade_analysis import births_by_decade_analysis
from yearly_trends import yearly_birth_trends
from weekday_patterns import weekday_birth_patterns
from seasonal_analysis import seasonal_birth_analysis

def run_selected_analyses(args):
    """Run only the selected analysis components"""
    
    # Always load data first
    data = load_and_explore_data('CDCbirths.csv')
    
    if args.all or args.decade:
        print("\n" + "="*60)
        print("RUNNING DECADE ANALYSIS")
        print("="*60)
        data = births_by_decade_analysis(data)
    
    if args.all or args.yearly:
        print("\n" + "="*60)
        print("RUNNING YEARLY TRENDS ANALYSIS")
        print("="*60)
        yearly_birth_trends(data)
    
    if args.all or args.weekday:
        print("\n" + "="*60)
        print("RUNNING WEEKDAY PATTERNS ANALYSIS")
        print("="*60)
        weekday_birth_patterns(data)
    
    if args.all or args.seasonal:
        print("\n" + "="*60)
        print("RUNNING SEASONAL ANALYSIS")
        print("="*60)
        seasonal_birth_analysis(data)

def main():
    parser = argparse.ArgumentParser(description='Run CDC births data analysis')
    parser.add_argument('--all', action='store_true', help='Run all analyses')
    parser.add_argument('--decade', action='store_true', help='Run decade analysis')
    parser.add_argument('--yearly', action='store_true', help='Run yearly trends analysis')
    parser.add_argument('--weekday', action='store_true', help='Run weekday patterns analysis')
    parser.add_argument('--seasonal', action='store_true', help='Run seasonal analysis')
    
    args = parser.parse_args()
    
    # If no specific analysis is chosen, run all
    if not any([args.decade, args.yearly, args.weekday, args.seasonal]):
        args.all = True
    
    run_selected_analyses(args)

if __name__ == "__main__":
    main()

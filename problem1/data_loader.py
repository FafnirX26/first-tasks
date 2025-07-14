"""
Data loading and basic exploration functions for CDC births dataset
"""
import pandas as pd

def load_and_explore_data(filename='CDCbirths.csv'):
    """Load the CDC births dataset and return basic information"""
    data = pd.read_csv(filename)
    
    # Store basic information for reporting
    dataset_info = {
        'columns': list(data.columns),
        'shape': data.shape,
        'first_five_rows': data.head(),
        'data_types': data.dtypes
    }
    
    return data

def prepare_data_with_decades(data):
    """Add decade column for easier decade-based analysis"""
    data_copy = data.copy()
    data_copy['decade'] = (data_copy['year'] // 10) * 10
    return data_copy
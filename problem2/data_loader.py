"""
Data loading utilities for ICU dataset from Physionet 2012 challenge
"""
import numpy as np
import pandas as pd

def load_icu_data():
    """Load the ICU training and testing datasets from npz files"""
    
    # Load training data
    train_data = np.load('hw1_train.data.npz')
    train_features = train_data['X_train']
    train_labels = train_data['y_train']
    
    # Load testing data  
    test_data = np.load('hw1_test.data.npz')
    test_features = test_data['X_test']
    test_labels = test_data['y_test']
    
    return train_features, train_labels, test_features, test_labels

def explore_dataset(train_features, train_labels, test_features, test_labels):
    """Explore the dataset structure and characteristics"""
    
    dataset_info = {
        'train_samples': train_features.shape[0],
        'test_samples': test_features.shape[0],
        'n_features': train_features.shape[1],
        'train_positive_ratio': np.mean(train_labels),
        'test_positive_ratio': np.mean(test_labels),
        'feature_stats': {
            'train_mean': np.mean(train_features, axis=0),
            'train_std': np.std(train_features, axis=0),
            'test_mean': np.mean(test_features, axis=0),
            'test_std': np.std(test_features, axis=0)
        }
    }
    
    return dataset_info
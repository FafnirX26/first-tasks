"""
Main script to run ICU mortality prediction analysis with multiple classifiers
"""
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_loader import load_icu_data, explore_dataset
from classifiers import ICUClassifiers

def main():
    """Run the complete classification analysis pipeline"""
    
    # Load ICU dataset
    X_train, y_train, X_test, y_test = load_icu_data()
    
    # Explore dataset characteristics
    dataset_info = explore_dataset(X_train, y_train, X_test, y_test)
    
    # Initialize classifier container
    classifiers = ICUClassifiers()
    
    # Prepare scaled data for SVM
    X_train_scaled, X_test_scaled = classifiers.prepare_data(X_train, y_train, X_test, y_test)
    
    # Train Logistic Regression
    lr_results = classifiers.train_logistic_regression(X_train, y_train, X_test, y_test)
    
    # Train Random Forest with different parameters
    rf_results = classifiers.train_random_forest(X_train, y_train, X_test, y_test)
    
    # Train SVM with different parameters
    svm_results = classifiers.train_svm(X_train_scaled, y_train, X_test_scaled, y_test)
    
    # Get all results
    all_results = classifiers.get_all_results()
    best_models = classifiers.get_best_models()
    
    return all_results, best_models, dataset_info

if __name__ == "__main__":
    all_results, best_models, dataset_info = main()
"""
Classification models for ICU mortality prediction
"""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.preprocessing import StandardScaler

class ICUClassifiers:
    """Container for different classification models"""
    
    def __init__(self):
        self.models = {}
        self.results = {}
        self.scaler = StandardScaler()
    
    def prepare_data(self, X_train, y_train, X_test, y_test):
        """Standardize features for SVM"""
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        return X_train_scaled, X_test_scaled
    
    def train_logistic_regression(self, X_train, y_train, X_test, y_test):
        """Train Logistic Regression with default parameters"""
        
        # Use default parameters as specified
        model = LogisticRegression(random_state=42, max_iter=1000)
        model.fit(X_train, y_train)
        
        # Predictions
        train_pred = model.predict(X_train)
        test_pred = model.predict(X_test)
        train_pred_proba = model.predict_proba(X_train)[:, 1]
        test_pred_proba = model.predict_proba(X_test)[:, 1]
        
        # Metrics
        results = {
            'train_accuracy': accuracy_score(y_train, train_pred),
            'test_accuracy': accuracy_score(y_test, test_pred),
            'train_auroc': roc_auc_score(y_train, train_pred_proba),
            'test_auroc': roc_auc_score(y_test, test_pred_proba)
        }
        
        self.models['logistic_regression'] = model
        self.results['logistic_regression'] = results
        return results
    
    def train_random_forest(self, X_train, y_train, X_test, y_test):
        """Train Random Forest with different parameter combinations"""
        
        # Parameter combinations as specified
        param_combinations = [
            {'max_depth': 3, 'n_estimators': 100},
            {'max_depth': 3, 'n_estimators': 500},
            {'max_depth': 5, 'n_estimators': 100},
            {'max_depth': 5, 'n_estimators': 500}
        ]
        
        rf_results = {}
        
        for i, params in enumerate(param_combinations):
            model_name = f"random_forest_depth{params['max_depth']}_est{params['n_estimators']}"
            
            model = RandomForestClassifier(
                max_depth=params['max_depth'],
                n_estimators=params['n_estimators'],
                random_state=42
            )
            model.fit(X_train, y_train)
            
            # Predictions
            train_pred = model.predict(X_train)
            test_pred = model.predict(X_test)
            train_pred_proba = model.predict_proba(X_train)[:, 1]
            test_pred_proba = model.predict_proba(X_test)[:, 1]
            
            # Metrics
            results = {
                'params': params,
                'train_accuracy': accuracy_score(y_train, train_pred),
                'test_accuracy': accuracy_score(y_test, test_pred),
                'train_auroc': roc_auc_score(y_train, train_pred_proba),
                'test_auroc': roc_auc_score(y_test, test_pred_proba)
            }
            
            self.models[model_name] = model
            rf_results[model_name] = results
        
        self.results.update(rf_results)
        return rf_results
    
    def train_svm(self, X_train_scaled, y_train, X_test_scaled, y_test):
        """Train SVM with different parameter combinations"""
        
        # Parameter combinations for C and kernel
        param_combinations = [
            {'C': 0.1, 'kernel': 'linear'},
            {'C': 0.1, 'kernel': 'rbf'},
            {'C': 1.0, 'kernel': 'linear'}, 
            {'C': 1.0, 'kernel': 'rbf'},
            {'C': 10.0, 'kernel': 'linear'},
            {'C': 10.0, 'kernel': 'rbf'}
        ]
        
        svm_results = {}
        
        for i, params in enumerate(param_combinations):
            model_name = f"svm_C{params['C']}_kernel{params['kernel']}"
            
            model = SVC(
                C=params['C'],
                kernel=params['kernel'],
                probability=True,  # Enable probability estimates for AUROC
                random_state=42
            )
            model.fit(X_train_scaled, y_train)
            
            # Predictions
            train_pred = model.predict(X_train_scaled)
            test_pred = model.predict(X_test_scaled)
            train_pred_proba = model.predict_proba(X_train_scaled)[:, 1]
            test_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
            
            # Metrics
            results = {
                'params': params,
                'train_accuracy': accuracy_score(y_train, train_pred),
                'test_accuracy': accuracy_score(y_test, test_pred),
                'train_auroc': roc_auc_score(y_train, train_pred_proba),
                'test_auroc': roc_auc_score(y_test, test_pred_proba)
            }
            
            self.models[model_name] = model
            svm_results[model_name] = results
        
        self.results.update(svm_results)
        return svm_results
    
    def get_all_results(self):
        """Return all model results"""
        return self.results
    
    def get_best_models(self):
        """Find best model for each algorithm type based on test AUROC"""
        best_models = {}
        
        # Best Logistic Regression (only one)
        if 'logistic_regression' in self.results:
            best_models['logistic_regression'] = self.results['logistic_regression']
        
        # Best Random Forest
        rf_models = {k: v for k, v in self.results.items() if k.startswith('random_forest')}
        if rf_models:
            best_rf_name = max(rf_models.keys(), key=lambda x: rf_models[x]['test_auroc'])
            best_models['best_random_forest'] = rf_models[best_rf_name]
            best_models['best_random_forest']['model_name'] = best_rf_name
        
        # Best SVM
        svm_models = {k: v for k, v in self.results.items() if k.startswith('svm')}
        if svm_models:
            best_svm_name = max(svm_models.keys(), key=lambda x: svm_models[x]['test_auroc'])
            best_models['best_svm'] = svm_models[best_svm_name]
            best_models['best_svm']['model_name'] = best_svm_name
        
        return best_models
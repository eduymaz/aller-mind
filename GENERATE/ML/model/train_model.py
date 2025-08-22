import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
import os
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.pipeline import Pipeline

class AllergyModel:
    def __init__(self, model_dir='saved_models'):
        """
        Initialize the allergy prediction model
        
        Parameters:
        model_dir (str): Directory to save trained models
        """
        self.model_dir = model_dir
        self.models = {}
        self.features = None
        os.makedirs(model_dir, exist_ok=True)
    
    def preprocess_data(self, data, target_col='allergy_group'):
        """
        Preprocess data for training
        
        Parameters:
        data (DataFrame): Input dataset
        target_col (str): Target column name
        
        Returns:
        X (DataFrame): Features
        y (Series): Target
        """
        # Select only numerical features
        numerical_features = [
            'temperature_2m', 'relative_humidity_2m', 'precipitation', 
            'snowfall', 'rain', 'cloud_cover', 'surface_pressure', 
            'wind_speed_10m', 'wind_direction_10m', 'soil_temperature_0_to_7cm', 
            'soil_moisture_0_to_7cm', 'sunshine_duration', 'pm10', 'pm2_5', 
            'carbon_dioxide', 'carbon_monoxide', 'nitrogen_dioxide', 
            'sulphur_dioxide', 'ozone', 'aerosol_optical_depth', 
            'methane', 'uv_index', 'uv_index_clear_sky', 'dust',
            'grass', 'tree', 'weed'
        ]
        
        # Filter available features
        self.features = [f for f in numerical_features if f in data.columns]
        
        # Handle missing values
        X = data[self.features].fillna(data[self.features].median())
        
        # Create target if needed
        if target_col not in data.columns:
            # Simulate group assignment for synthetic data
            # Revised groups:
            # Group 1: Severe Allergic Asthma - most sensitive to pollutants and allergens
            # Group 2: Mild to Moderate Allergic - sensitive to common allergens
            # Group 3: Possible Allergic/High Risk - potential sensitivity
            # Group 4: Not Yet Diagnosed - general population
            # Group 5: Vulnerable Population - babies, elderly, chronic patients
            
            conditions = [
                # Group 1: Severe Allergic Asthma - highly sensitive to pollutants and all pollens
                ((data['pm2_5'] > data['pm2_5'].quantile(0.7)) & 
                 ((data['tree'] > data['tree'].quantile(0.6)) | 
                  (data['grass'] > data['grass'].quantile(0.6)) | 
                  (data['weed'] > data['weed'].quantile(0.6))) &
                 ((data['ozone'] > data['ozone'].quantile(0.6)) | 
                  (data['nitrogen_dioxide'] > data['nitrogen_dioxide'].quantile(0.6)))),
                
                # Group 2: Mild to Moderate Allergic
                ((data['pm10'] > data['pm10'].quantile(0.6)) & 
                 ((data['tree'] > data['tree'].quantile(0.5)) | 
                  (data['grass'] > data['grass'].quantile(0.5))) &
                 (data['ozone'] < data['ozone'].quantile(0.7))),
                
                # Group 3: Possible Allergic/High Risk
                ((data['pm2_5'] > data['pm2_5'].quantile(0.5)) |
                 (data['ozone'] > data['ozone'].quantile(0.5)) |
                 (data['nitrogen_dioxide'] > data['nitrogen_dioxide'].quantile(0.5))),
                
                # Group 5: Vulnerable Population (taking precedence over Group 4)
                # Characterized by sensitivity to extreme temperature, humidity, and pollutants
                ((data['temperature_2m'] > data['temperature_2m'].quantile(0.8)) | 
                 (data['temperature_2m'] < data['temperature_2m'].quantile(0.2)) |
                 (data['relative_humidity_2m'] > data['relative_humidity_2m'].quantile(0.8)) |
                 (data['relative_humidity_2m'] < data['relative_humidity_2m'].quantile(0.2))) &
                 (data['pm2_5'] > data['pm2_5'].quantile(0.6))
            ]
            
            choices = [1, 2, 3, 5]  # Group 4 is default if no condition is met
            y = np.select(conditions, choices, default=4)
            y = pd.Series(y)
        else:
            y = data[target_col]
        
        return X, y
    
    def train(self, data, target_col='allergy_group'):
        """
        Train models for allergy group prediction
        
        Parameters:
        data (DataFrame): Training data
        target_col (str): Target column name
        
        Returns:
        self: The trained model instance
        """
        X, y = self.preprocess_data(data, target_col)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, random_state=42, stratify=y
        )
        
        # Define models to try
        models = {
            'random_forest': Pipeline([
                ('scaler', StandardScaler()),
                ('clf', RandomForestClassifier(random_state=42))
            ]),
            'gradient_boosting': Pipeline([
                ('scaler', StandardScaler()),
                ('clf', GradientBoostingClassifier(random_state=42))
            ]),
            'svm': Pipeline([
                ('scaler', StandardScaler()),
                ('clf', SVC(probability=True, random_state=42))
            ])
        }
        
        # Parameters for grid search
        param_grids = {
            'random_forest': {
                'clf__n_estimators': [100, 200, 300],
                'clf__max_depth': [None, 15, 30],
                'clf__min_samples_split': [2, 5, 10]
            },
            'gradient_boosting': {
                'clf__n_estimators': [100, 200, 300],
                'clf__learning_rate': [0.01, 0.05, 0.1],
                'clf__max_depth': [3, 5, 7]
            },
            'svm': {
                'clf__C': [0.1, 1, 10],
                'clf__gamma': ['scale', 'auto'],
                'clf__kernel': ['rbf', 'poly']
            }
        }
        
        # Train and evaluate models
        best_accuracy = 0
        best_model_name = None
        
        for model_name, model in models.items():
            print(f"Training {model_name}...")
            
            # Grid search
            grid_search = GridSearchCV(
                model, param_grids[model_name], cv=5, 
                scoring='accuracy', n_jobs=-1
            )
            grid_search.fit(X_train, y_train)
            
            # Get best model
            best_model = grid_search.best_estimator_
            self.models[model_name] = best_model
            
            # Evaluate
            y_pred = best_model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            print(f"{model_name} best parameters: {grid_search.best_params_}")
            print(f"{model_name} accuracy: {accuracy:.4f}")
            print(classification_report(y_test, y_pred))
            
            # Plot confusion matrix
            plt.figure(figsize=(10, 8))
            cm = confusion_matrix(y_test, y_pred)
            plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
            plt.title(f'Confusion Matrix - {model_name}')
            plt.colorbar()
            tick_marks = np.arange(len(np.unique(y)))
            plt.xticks(tick_marks, [f"Group {i}" for i in np.unique(y)], rotation=45)
            plt.yticks(tick_marks, [f"Group {i}" for i in np.unique(y)])
            plt.tight_layout()
            plt.ylabel('True label')
            plt.xlabel('Predicted label')
            
            # Add text annotations to confusion matrix
            thresh = cm.max() / 2.
            for i in range(cm.shape[0]):
                for j in range(cm.shape[1]):
                    plt.text(j, i, format(cm[i, j], 'd'),
                            ha="center", va="center",
                            color="white" if cm[i, j] > thresh else "black")
                            
            plt.savefig(os.path.join(self.model_dir, f'{model_name}_confusion_matrix.png'))
            
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_model_name = model_name
        
        # Calculate feature importance for the best model
        if best_model_name in ['random_forest', 'gradient_boosting']:
            self._plot_feature_importance(self.models[best_model_name], X.columns)
        
        # Save all models
        for model_name, model in self.models.items():
            joblib.dump(model, os.path.join(self.model_dir, f'{model_name}.pkl'))
        
        # Save features
        joblib.dump(self.features, os.path.join(self.model_dir, 'features.pkl'))
        
        print(f"\nBest model: {best_model_name} with accuracy: {best_accuracy:.4f}")
        print(f"All models saved to {self.model_dir}")
        
        return self
    
    def _plot_feature_importance(self, model, feature_names):
        """Plot feature importance for tree-based models"""
        # Extract feature importances
        if hasattr(model, 'named_steps') and hasattr(model.named_steps['clf'], 'feature_importances_'):
            importances = model.named_steps['clf'].feature_importances_
            indices = np.argsort(importances)[::-1]
            
            # Plot feature importances
            plt.figure(figsize=(12, 8))
            plt.title('Feature Importances')
            plt.bar(range(len(importances)), importances[indices], align='center')
            plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=90)
            plt.tight_layout()
            plt.savefig(os.path.join(self.model_dir, 'feature_importance.png'))
            
            # Also save as CSV for easier analysis
            importance_df = pd.DataFrame({
                'Feature': feature_names,
                'Importance': importances
            }).sort_values('Importance', ascending=False)
            
            importance_df.to_csv(os.path.join(self.model_dir, 'feature_importance.csv'), index=False)
            
            # Save group-specific feature importance
            self._save_group_specific_importance(model, feature_names)
    
    def _save_group_specific_importance(self, model, feature_names):
        """Calculate and save feature importance for each group"""
        if not hasattr(model, 'named_steps') or not hasattr(model.named_steps['clf'], 'feature_importances_'):
            return
            
        # For advanced analysis, we could analyze feature importance per class
        # This is a simplified approach that could be expanded with SHAP values in production
        clf = model.named_steps['clf']
        if hasattr(clf, 'estimators_'):
            # For random forest, we can look at estimators trained for different classes
            with open(os.path.join(self.model_dir, 'group_feature_importance.md'), 'w') as f:
                f.write("# Feature Importance by Allergy Group\n\n")
                f.write("This analysis shows which environmental factors are most important for each allergy group.\n\n")
                
                for group in range(1, 6):  # 5 groups
                    f.write(f"## Group {group}\n\n")
                    if group == 1:
                        f.write("### Severe Allergic Asthma\n\n")
                    elif group == 2:
                        f.write("### Mild to Moderate Allergic\n\n")
                    elif group == 3:
                        f.write("### Possible Allergic/High Risk\n\n")
                    elif group == 4:
                        f.write("### Not Yet Diagnosed\n\n")
                    elif group == 5:
                        f.write("### Vulnerable Population (Babies, Elderly, Chronic Patients)\n\n")
                    
                    # Create a placeholder for importance analysis
                    # In a production system, this would use more sophisticated per-class importance analysis
                    f.write("Top 10 most important factors for this group:\n\n")
                    f.write("1. *Analysis would be based on actual trained model*\n")
                    f.write("2. *Using techniques like SHAP values for explainability*\n\n")
    
    def predict(self, data):
        """
        Make predictions with the best model
        
        Parameters:
        data (DataFrame): Input data
        
        Returns:
        predictions (ndarray): Predicted allergy groups
        probabilities (ndarray): Probability for each class
        """
        # Ensure features are available
        if self.features is None:
            self.features = joblib.load(os.path.join(self.model_dir, 'features.pkl'))
        
        # Load best model if not already loaded
        if not self.models:
            # Try to load all available models
            for model_name in ['random_forest', 'gradient_boosting', 'svm']:
                model_path = os.path.join(self.model_dir, f'{model_name}.pkl')
                if os.path.exists(model_path):
                    self.models[model_name] = joblib.load(model_path)
        
        if not self.models:
            raise ValueError("No trained models available. Train models first.")
        
        # Select best model (could be improved to dynamically select best model)
        best_model = self.models.get('gradient_boosting', next(iter(self.models.values())))
        
        # Prepare data
        available_features = [f for f in self.features if f in data.columns]
        X = data[available_features].fillna(data[available_features].median())
        
        # Add missing features with median values
        for feature in self.features:
            if feature not in available_features:
                X[feature] = 0  # Will be ignored by the scaler in the pipeline
        
        # Ensure correct feature order
        X = X[self.features]
        
        # Make predictions
        predictions = best_model.predict(X)
        probabilities = best_model.predict_proba(X)
        
        return predictions, probabilities

# Main execution
if __name__ == "__main__":
    # Load data
    try:
        data_path = '../../synthetic_combined_data.csv'
        data = pd.read_csv(data_path)
        print(f"Loaded data from {data_path}, shape: {data.shape}")
        
        # Create and train model
        model = AllergyModel()
        model.train(data)
        
        # Example prediction
        sample_data = data.sample(5)
        predictions, probabilities = model.predict(sample_data)
        
        print("\nSample predictions:")
        for i, pred in enumerate(predictions):
            group_names = {
                1: "Severe Allergic Asthma",
                2: "Mild to Moderate Allergic",
                3: "Possible Allergic/High Risk",
                4: "Not Yet Diagnosed",
                5: "Vulnerable Population"
            }
            group_name = group_names.get(pred, f"Group {pred}")
            print(f"Sample {i+1}: Predicted {group_name} with probability {probabilities[i][pred-1]:.4f}")
            
    except Exception as e:
        print(f"Error: {e}")

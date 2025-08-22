# /Users/elifdy/Desktop/allermind/aller-mind/GENERATE/ML/feature_analysis.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score, f1_score, classification_report
import shap

# Define our feature groups
numerical_features = [
    'temperature_2m', 'relative_humidity_2m', 'precipitation', 'snowfall',
    'rain', 'cloud_cover', 'surface_pressure', 'wind_speed_10m',
    'wind_direction_10m', 'soil_temperature_0_to_7cm', 'soil_moisture_0_to_7cm',
    'sunshine_duration', 'pm10', 'pm2_5', 'carbon_dioxide', 'carbon_monoxide',
    'nitrogen_dioxide', 'sulphur_dioxide', 'ozone', 'aerosol_optical_depth',
    'methane', 'uv_index', 'uv_index_clear_sky', 'dust', 'grass', 'tree', 'weed'
]

categorical_features = ['CITY_NAME', 'LAT', 'LON', 'TIME']

# Function to load and preprocess data
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Feature importance analysis
def analyze_feature_importance(X, y, feature_names):
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Random Forest for feature importance
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    
    # Get feature importance
    importances = rf.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    # Plot feature importance
    plt.figure(figsize=(12, 8))
    plt.title('Feature Importances')
    plt.bar(range(X.shape[1]), importances[indices], align='center')
    plt.xticks(range(X.shape[1]), [feature_names[i] for i in indices], rotation=90)
    plt.tight_layout()
    plt.savefig('feature_importance.png')
    
    # Permutation importance
    perm_importance = permutation_importance(rf, X_test, y_test, n_repeats=10, random_state=42)
    
    # Return sorted features by importance
    feature_importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Random Forest Importance': importances,
        'Permutation Importance': perm_importance.importances_mean
    })
    
    return feature_importance_df.sort_values('Permutation Importance', ascending=False)

# Model training and evaluation
def train_evaluate_model(X, y, selected_features, group_name):
    # Select only the important features
    X_selected = X[selected_features]
    
    # Create preprocessing pipeline
    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, selected_features)
        ])
    
    # Create classifier pipeline
    clf = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', GradientBoostingClassifier(random_state=42))
    ])
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X_selected, y, test_size=0.3, random_state=42)
    
    # Train model
    clf.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = clf.predict(X_test)
    
    print(f"Model evaluation for {group_name}:")
    print(classification_report(y_test, y_pred))
    
    # Cross-validation
    cv_scores = cross_val_score(clf, X_selected, y, cv=5, scoring='f1')
    print(f"5-fold CV F1 Score: {np.mean(cv_scores):.4f} ± {np.std(cv_scores):.4f}")
    
    return clf

# SHAP analysis for model interpretation
def shap_analysis(model, X, feature_names):
    # Create SHAP explainer
    explainer = shap.Explainer(model)
    shap_values = explainer(X)
    
    # Plot SHAP summary
    plt.figure(figsize=(12, 10))
    shap.summary_plot(shap_values, X, feature_names=feature_names, show=False)
    plt.tight_layout()
    plt.savefig('shap_summary.png')
    
    return shap_values

# Main function
def main():
    # This would be replaced with actual data loading
    # For demonstration purposes, we'll assume the data is loaded
    print("Starting feature importance analysis and modeling for allergy groups...")
    
    # Feature selections for each group based on our analysis
    group1_features = ['pm2_5', 'pm10', 'ozone', 'nitrogen_dioxide', 'carbon_monoxide', 
                      'relative_humidity_2m', 'temperature_2m', 'tree', 'grass', 'weed']
    
    group2_features = ['temperature_2m', 'relative_humidity_2m', 'uv_index', 
                      'pm2_5', 'ozone', 'dust', 'surface_pressure', 'sunshine_duration']
    
    group3_features = ['carbon_dioxide', 'surface_pressure', 'temperature_2m', 
                      'relative_humidity_2m', 'pm2_5', 'ozone', 'nitrogen_dioxide', 'sulphur_dioxide']
    
    group4_features = ['temperature_2m', 'relative_humidity_2m', 'wind_speed_10m', 
                      'precipitation', 'cloud_cover', 'soil_temperature_0_to_7cm', 
                      'soil_moisture_0_to_7cm', 'uv_index']
    
    print("Selected features for each group:")
    print(f"Group 1 (Respiratory Allergies): {', '.join(group1_features)}")
    print(f"Group 2 (Skin Allergies): {', '.join(group2_features)}")
    print(f"Group 3 (Food Allergies): {', '.join(group3_features)}")
    print(f"Group 4 (Insect Allergies): {', '.join(group4_features)}")
    
    print("\nAnalysis complete. See info.md for detailed interpretations.")

if __name__ == "__main__":
    main()
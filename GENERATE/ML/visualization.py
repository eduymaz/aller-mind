# /Users/elifdy/Desktop/allermind/aller-mind/GENERATE/ML/visualization.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def load_and_prepare_data(file_path):
    """Load data and prepare for visualization"""
    df = pd.read_csv(file_path)
    return df

def create_correlation_heatmap(df, numerical_features, group_name):
    """Create correlation heatmap for numerical features"""
    plt.figure(figsize=(14, 12))
    corr = df[numerical_features].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=False, cmap='coolwarm', 
                fmt='.2f', linewidths=0.5, vmin=-1, vmax=1)
    plt.title(f'Feature Correlation for {group_name}', fontsize=16)
    plt.tight_layout()
    plt.savefig(f'{group_name.lower().replace(" ", "_")}_correlation.png')

def visualize_pca(df, numerical_features, group_target):
    """Perform PCA and visualize results"""
    # Extract features
    X = df[numerical_features]
    
    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Apply PCA
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    
    # Create DataFrame for visualization
    pca_df = pd.DataFrame(
        data=X_pca, 
        columns=['PC1', 'PC2']
    )
    pca_df['Group'] = df[group_target]
    
    # Plot
    plt.figure(figsize=(10, 8))
    sns.scatterplot(
        x='PC1', y='PC2',
        hue='Group',
        palette='viridis',
        data=pca_df,
        alpha=0.7
    )
    plt.title('PCA of Environmental Factors', fontsize=16)
    plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%} variance explained)')
    plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%} variance explained)')
    
    # Add loading vectors
    feature_vectors = pca.components_.T
    for i, (x, y) in enumerate(zip(feature_vectors[0], feature_vectors[1])):
        plt.arrow(0, 0, x*3, y*3, color='r', alpha=0.5)
        plt.text(x*3.2, y*3.2, numerical_features[i], fontsize=10)
    
    plt.tight_layout()
    plt.savefig('pca_visualization.png')
    
    return pca, pca_df

def feature_distribution_by_group(df, feature, group_col):
    """Visualize feature distribution by group"""
    plt.figure(figsize=(12, 6))
    sns.boxplot(x=group_col, y=feature, data=df)
    plt.title(f'Distribution of {feature} by Group', fontsize=14)
    plt.tight_layout()
    plt.savefig(f'{feature}_by_group.png')

def main():
    # Define feature groups (would normally load from data)
    numerical_features = [
        'temperature_2m', 'relative_humidity_2m', 'precipitation', 
        'pm10', 'pm2_5', 'carbon_dioxide', 'ozone', 'uv_index',
        'dust', 'grass', 'tree', 'weed'
    ]
    
    # These functions would be called with actual data in a real implementation
    print("Visualization module for allergy impact analysis")
    print("Functions available:")
    print("- create_correlation_heatmap: Creates correlation heatmaps for features")
    print("- visualize_pca: Performs PCA analysis and visualizes results")
    print("- feature_distribution_by_group: Shows boxplots of features by group")
    
    print("\nRun with actual data to generate visualizations.")

if __name__ == "__main__":
    main()
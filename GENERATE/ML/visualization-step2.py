# /Users/elifdy/Desktop/allermind/aller-mind/visualization.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
import numpy as np

def create_correlation_heatmap(data, title='Correlation Heatmap', figsize=(12, 10)):
    """
    Creates a correlation heatmap for the given dataset
    
    Parameters:
    data (pandas.DataFrame): Dataset to analyze
    title (str): Title of the heatmap
    figsize (tuple): Size of the figure (width, height)
    
    Returns:
    matplotlib.figure.Figure: The resulting heatmap figure
    """
    # Calculate correlation matrix
    numeric_data = data.select_dtypes(include=[np.number])
    corr_matrix = numeric_data.corr()
    
    # Create figure
    plt.figure(figsize=figsize)
    
    # Create heatmap
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", 
                linewidths=0.5, vmin=-1, vmax=1)
    
    plt.title(title, fontsize=16)
    plt.tight_layout()
    
    return plt.gcf()

def visualize_pca(data, target_column=None, n_components=2, figsize=(10, 8)):
    """
    Performs PCA and visualizes the results
    
    Parameters:
    data (pandas.DataFrame): Dataset to analyze
    target_column (str): Column name for color coding points
    n_components (int): Number of PCA components to calculate
    figsize (tuple): Size of the figure (width, height)
    
    Returns:
    matplotlib.figure.Figure: The resulting PCA plot
    """
    # Get numeric features only
    numeric_data = data.select_dtypes(include=[np.number])
    
    # Remove target column from features if present
    features = numeric_data.drop(columns=[target_column]) if target_column in numeric_data else numeric_data
    
    # Standardize the features
    scaled_features = (features - features.mean()) / features.std()
    
    # Perform PCA
    pca = PCA(n_components=n_components)
    pca_result = pca.fit_transform(scaled_features)
    
    # Create DataFrame for visualization
    pca_df = pd.DataFrame(data=pca_result, columns=[f'PC{i+1}' for i in range(n_components)])
    
    # Add target column if provided
    if target_column and target_column in data.columns:
        pca_df[target_column] = data[target_column].values
    
    # Create plot
    plt.figure(figsize=figsize)
    
    if target_column and target_column in data.columns:
        # Color-code by target
        sns.scatterplot(x='PC1', y='PC2', hue=target_column, data=pca_df, palette='viridis')
    else:
        # Simple scatter plot if no target
        sns.scatterplot(x='PC1', y='PC2', data=pca_df)
    
    # Add variance explained labels
    explained_var = pca.explained_variance_ratio_
    plt.xlabel(f'PC1 ({explained_var[0]:.2%} variance explained)')
    plt.ylabel(f'PC2 ({explained_var[1]:.2%} variance explained)')
    
    plt.title('PCA Visualization', fontsize=16)
    plt.tight_layout()
    
    return plt.gcf()

def feature_distribution_by_group(data, feature, group_column, figsize=(12, 8)):
    """
    Creates boxplots showing distribution of a feature across groups
    
    Parameters:
    data (pandas.DataFrame): Dataset to analyze
    feature (str): Feature to analyze
    group_column (str): Column to group by
    figsize (tuple): Size of the figure (width, height)
    
    Returns:
    matplotlib.figure.Figure: The resulting boxplot figure
    """
    plt.figure(figsize=figsize)
    
    sns.boxplot(x=group_column, y=feature, data=data)
    
    plt.title(f'Distribution of {feature} by {group_column}', fontsize=16)
    plt.xlabel(group_column, fontsize=12)
    plt.ylabel(feature, fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return plt.gcf()

# Main execution
if __name__ == "__main__":
    print("Visualization module for allergy impact analysis")
    print("Functions available:")
    print("- create_correlation_heatmap: Creates correlation heatmaps for features")
    print("- visualize_pca: Performs PCA analysis and visualizes results")
    print("- feature_distribution_by_group: Shows boxplots of features by group")
    
    # Load actual data
    data_path = '/Users/elifdy/Desktop/allermind/aller-mind/GENERATE/synthetic_combined_data.csv'
    try:
        data = pd.read_csv(data_path)
        print(f"\nLoaded dataset from {data_path}")
        print(f"Dataset shape: {data.shape}")
        
        # Create and save visualizations
        print("\nGenerating visualizations...")
        
        # 1. Correlation heatmap
        corr_fig = create_correlation_heatmap(data, title='Feature Correlation in Allergy Data')
        corr_fig.savefig('correlation_heatmap.png')
        print("- Saved correlation heatmap to 'correlation_heatmap.png'")
        
        # 2. PCA visualization (assuming there's an 'Allergy_Status' column)
        target_col = 'Allergy_Status' if 'Allergy_Status' in data.columns else None
        if target_col:
            pca_fig = visualize_pca(data, target_column=target_col)
            pca_fig.savefig('pca_visualization.png')
            print(f"- Saved PCA visualization to 'pca_visualization.png'")
        
        # 3. Feature distributions for some key features (modify as needed)
        key_features = ['IgE_Level', 'Eosinophil_Count'] 
        key_features = [f for f in key_features if f in data.columns]
        
        for feature in key_features:
            if target_col:
                dist_fig = feature_distribution_by_group(data, feature, target_col)
                dist_fig.savefig(f'{feature}_distribution.png')
                print(f"- Saved {feature} distribution to '{feature}_distribution.png'")
        
        print("\nVisualization complete!")
        
    except Exception as e:
        print(f"Error: {e}")
        print(f"Make sure the file exists at: {data_path}")
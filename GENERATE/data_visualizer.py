# /Users/elifdy/Desktop/allermind/aller-mind/GENERATE/data_visualizer.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def load_data(file_path):
    """Load the synthetic data from a CSV file."""
    return pd.read_csv(file_path)

def visualize_pollen_data(df):
    """Create visualizations for pollen data."""
    # Convert TIME to datetime
    df['TIME'] = pd.to_datetime(df['TIME'])
    df['month'] = df['TIME'].dt.month
    
    # Set up the plot style
    sns.set(style="whitegrid")
    plt.figure(figsize=(16, 12))
    
    # Plot 1: Pollen levels by month
    plt.subplot(2, 2, 1)
    monthly_pollen = df.groupby('month')[['grass', 'tree', 'weed']].mean().reset_index()
    monthly_pollen = pd.melt(monthly_pollen, id_vars=['month'], 
                             value_vars=['grass', 'tree', 'weed'],
                             var_name='Pollen Type', value_name='Level')
    sns.lineplot(data=monthly_pollen, x='month', y='Level', hue='Pollen Type', marker='o')
    plt.title('Average Pollen Levels by Month')
    plt.xlabel('Month')
    plt.ylabel('Pollen Level')
    plt.xticks(range(1, 13))
    
    # Plot 2: Pollen levels vs temperature
    plt.subplot(2, 2, 2)
    sns.scatterplot(data=df, x='temperature_2m', y='grass', alpha=0.3, label='Grass')
    sns.scatterplot(data=df, x='temperature_2m', y='tree', alpha=0.3, label='Tree')
    sns.scatterplot(data=df, x='temperature_2m', y='weed', alpha=0.3, label='Weed')
    plt.title('Pollen Levels vs Temperature')
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Pollen Level')
    
    # Plot 3: Pollen levels by city (boxplot)
    plt.subplot(2, 2, 3)
    city_pollen = pd.melt(df, id_vars=['CITY_NAME'], 
                         value_vars=['grass', 'tree', 'weed'],
                         var_name='Pollen Type', value_name='Level')
    sns.boxplot(data=city_pollen, x='CITY_NAME', y='Level', hue='Pollen Type')
    plt.title('Pollen Levels by City')
    plt.xlabel('City')
    plt.ylabel('Pollen Level')
    plt.xticks(rotation=45)
    
    # Plot 4: Correlation between pollen and air quality
    plt.subplot(2, 2, 4)
    corr_cols = ['grass', 'tree', 'weed', 'pm10', 'pm2_5', 
                'carbon_monoxide', 'nitrogen_dioxide', 'temperature_2m']
    corr = df[corr_cols].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Correlation between Pollen and Air Quality')
    
    plt.tight_layout()
    
    # Save the figure
    output_path = os.path.join(os.path.dirname(__file__), 'pollen_visualizations.png')
    plt.savefig(output_path)
    print(f"Visualizations saved to {output_path}")
    plt.show()

def main():
    # Load the data
    data_path = os.path.join(os.path.dirname(__file__), 'synthetic_combined_data.csv')
    if not os.path.exists(data_path):
        print(f"Data file not found at {data_path}. Please run main.py first.")
        return
    
    df = load_data(data_path)
    visualize_pollen_data(df)

if __name__ == "__main__":
    main()
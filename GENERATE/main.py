# /Users/elifdy/Desktop/allermind/aller-mind/GENERATE/main.py

import os
from datetime import datetime, timedelta
from synthetic_data_generator import generate_city_data, save_synthetic_data

def main():
    print("Generating synthetic combined weather, pollution, and pollen data...")
    
    # Generate data for the last 90 days
    start_date = datetime.now() - timedelta(days=90)
    end_date = datetime.now()
    
    # Generate 1000 data points per city across the date range
    df = generate_city_data(
        num_samples=1000, 
        start_date=start_date,
        end_date=end_date
    )
    
    # Save to the GENERATE directory
    output_path = os.path.join(os.path.dirname(__file__), 'synthetic_combined_data.csv')
    save_synthetic_data(df, output_path)
    
    # Display sample of the data
    print("\nSample of generated data:")
    print(df.head())
    
    # Display statistics
    print("\nData statistics:")
    print(df.describe())

if __name__ == "__main__":
    main()
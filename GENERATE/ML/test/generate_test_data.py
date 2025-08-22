import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_test_data(n_samples=500, random_seed=42):
    """
    Generate synthetic test data for allergy prediction model
    
    Parameters:
    n_samples (int): Number of samples to generate
    random_seed (int): Random seed for reproducibility
    
    Returns:
    DataFrame: Synthetic test dataset
    """
    np.random.seed(random_seed)
    
    # Generate random date ranges covering all seasons
    start_date = datetime(2025, 1, 1)
    dates = [start_date + timedelta(days=np.random.randint(0, 365)) for _ in range(n_samples)]
    
    # Determine season for each date
    def get_season(date):
        month = date.month
        if 3 <= month <= 5:
            return 'spring'
        elif 6 <= month <= 8:
            return 'summer'
        elif 9 <= month <= 11:
            return 'fall'
        else:
            return 'winter'
    
    seasons = [get_season(date) for date in dates]
    
    # Create base dataframe
    df = pd.DataFrame({
        'date': dates,
        'season': seasons
    })
    
    # Generate weather data based on seasons
    df['temperature_2m'] = df['season'].apply(lambda s: 
        np.random.normal(25, 5) if s == 'summer' 
        else np.random.normal(15, 5) if s in ['spring', 'fall'] 
        else np.random.normal(5, 8)
    )
    
    df['relative_humidity_2m'] = np.random.normal(65, 15, n_samples)
    # Ensure humidity is between 0 and 100
    df['relative_humidity_2m'] = df['relative_humidity_2m'].clip(10, 100)
    
    # More rain in spring/fall, less in summer/winter
    df['precipitation'] = df['season'].apply(lambda s: 
        np.random.exponential(5) if s in ['spring', 'fall'] 
        else np.random.exponential(2)
    )
    
    # Snowfall only in winter
    df['snowfall'] = df.apply(lambda row: 
        np.random.exponential(3) if row['season'] == 'winter' and row['temperature_2m'] < 2 
        else 0, axis=1
    )
    
    # Rain is precipitation minus snowfall (snow water equivalent)
    df['rain'] = (df['precipitation'] - df['snowfall'] * 0.1).clip(0)
    
    # Cloud cover - more in winter and rainy days
    df['cloud_cover'] = df.apply(lambda row: 
        min(100, np.random.normal(70, 20) + row['precipitation'] * 5) if row['season'] == 'winter'
        else min(100, np.random.normal(40, 30) + row['precipitation'] * 5), axis=1
    )
    
    # Surface pressure - normal distribution around standard pressure
    df['surface_pressure'] = np.random.normal(1013, 10, n_samples)
    
    # Wind - higher in winter/spring
    df['wind_speed_10m'] = df['season'].apply(lambda s: 
        np.random.gamma(3, 3) if s in ['winter', 'spring'] 
        else np.random.gamma(2, 2)
    )
    
    df['wind_direction_10m'] = np.random.uniform(0, 360, n_samples)
    
    # Soil temperature - correlated with air temperature
    df['soil_temperature_0_to_7cm'] = df['temperature_2m'] - np.random.normal(1, 2, n_samples)
    
    # Soil moisture - correlated with precipitation
    df['soil_moisture_0_to_7cm'] = 0.2 + 0.05 * np.log1p(df['precipitation']) + np.random.normal(0, 0.05, n_samples)
    df['soil_moisture_0_to_7cm'] = df['soil_moisture_0_to_7cm'].clip(0.05, 0.9)
    
    # Sunshine duration - inverse of cloud cover (in seconds, max 3600 for an hour)
    df['sunshine_duration'] = (3600 * (1 - df['cloud_cover'] / 100) * np.random.uniform(0.8, 1, n_samples)).clip(0, 3600)
    
    # Air quality data
    
    # PM10 - higher in urban areas, winter, and dry conditions
    df['pm10'] = df.apply(lambda row:
        np.random.gamma(3, 7) if row['season'] == 'winter' or row['precipitation'] < 1
        else np.random.gamma(2, 5), axis=1
    )
    
    # PM2.5 - correlated with PM10 but with specific variations
    df['pm2_5'] = df['pm10'] * np.random.uniform(0.4, 0.7, n_samples) + np.random.normal(2, 1, n_samples)
    
    # Various gas pollutants
    df['carbon_dioxide'] = np.random.normal(410, 20, n_samples)
    
    df['carbon_monoxide'] = df.apply(lambda row:
        np.random.gamma(4, 40) if row['season'] == 'winter' 
        else np.random.gamma(3, 30), axis=1
    )
    
    df['nitrogen_dioxide'] = df.apply(lambda row:
        np.random.gamma(2, 15) if row['season'] == 'winter' or row['wind_speed_10m'] < 5
        else np.random.gamma(1, 10), axis=1
    )
    
    df['sulphur_dioxide'] = df.apply(lambda row:
        np.random.gamma(1.5, 10) if row['season'] == 'winter'
        else np.random.gamma(1, 5), axis=1
    )
    
    # Ozone - higher in summer with sunlight
    df['ozone'] = df.apply(lambda row:
        np.random.normal(100, 20) if row['season'] == 'summer' and row['sunshine_duration'] > 1800
        else np.random.normal(70, 15), axis=1
    )
    
    # Other air quality metrics
    df['aerosol_optical_depth'] = np.random.gamma(3, 0.1, n_samples)
    df['methane'] = np.random.normal(1500, 100, n_samples)
    
    # UV index - higher in summer, correlated with sunshine
    df['uv_index'] = df.apply(lambda row:
        np.random.gamma(3, 3) if row['season'] == 'summer' and row['sunshine_duration'] > 1800
        else np.random.gamma(1.5, 1.5) if row['season'] in ['spring', 'fall'] and row['sunshine_duration'] > 1000
        else np.random.gamma(1, 0.5), axis=1
    )
    
    df['uv_index_clear_sky'] = df['uv_index'] + np.random.uniform(0, 2, n_samples)
    
    # Dust - higher in dry conditions
    df['dust'] = df.apply(lambda row:
        np.random.gamma(2, 1) if row['precipitation'] < 1 and row['wind_speed_10m'] > 10
        else np.random.gamma(1, 0.5), axis=1
    )
    
    # Pollen data
    # Pollen - seasonal patterns: tree in spring, grass in late spring/summer, weed in fall
    df['tree'] = df.apply(lambda row:
        np.random.gamma(5, 1.5) if row['season'] == 'spring' 
        else np.random.gamma(1, 0.5), axis=1
    )
    
    df['grass'] = df.apply(lambda row:
        np.random.gamma(5, 1.5) if row['season'] in ['spring', 'summer']
        else np.random.gamma(1, 0.5), axis=1
    )
    
    df['weed'] = df.apply(lambda row:
        np.random.gamma(5, 1.5) if row['season'] in ['summer', 'fall']
        else np.random.gamma(1, 0.5), axis=1
    )
    
    # Reduce pollen when raining
    rain_mask = df['precipitation'] > 2
    df.loc[rain_mask, ['tree', 'grass', 'weed']] = df.loc[rain_mask, ['tree', 'grass', 'weed']] * 0.3
    
    # Generate allergy group based on environmental conditions
    # Now using the new classification:
    # Group 1: Severe Allergic Asthma
    # Group 2: Mild to Moderate Allergic
    # Group 3: Possible Allergic/High Risk
    # Group 4: Not Yet Diagnosed
    # Group 5: Vulnerable Population (babies, elderly, chronic patients)
    
    # Create conditions for each group
    conditions = [
        # Group 1: Severe Allergic Asthma - highly sensitive to pollutants and all pollens
        ((df['pm2_5'] > np.percentile(df['pm2_5'], 70)) & 
         ((df['tree'] > np.percentile(df['tree'], 60)) | 
          (df['grass'] > np.percentile(df['grass'], 60)) | 
          (df['weed'] > np.percentile(df['weed'], 60))) &
         ((df['ozone'] > np.percentile(df['ozone'], 60)) | 
          (df['nitrogen_dioxide'] > np.percentile(df['nitrogen_dioxide'], 60)))),
        
        # Group 2: Mild to Moderate Allergic
        ((df['pm10'] > np.percentile(df['pm10'], 60)) & 
         ((df['tree'] > np.percentile(df['tree'], 50)) | 
          (df['grass'] > np.percentile(df['grass'], 50))) &
         (df['ozone'] < np.percentile(df['ozone'], 70))),
        
        # Group 3: Possible Allergic/High Risk
        ((df['pm2_5'] > np.percentile(df['pm2_5'], 50)) |
         (df['ozone'] > np.percentile(df['ozone'], 50)) |
         (df['nitrogen_dioxide'] > np.percentile(df['nitrogen_dioxide'], 50))),
        
        # Group 5: Vulnerable Population (taking precedence over Group 4)
        # Characterized by sensitivity to extreme temperature, humidity, and pollutants
        ((df['temperature_2m'] > np.percentile(df['temperature_2m'], 80)) | 
         (df['temperature_2m'] < np.percentile(df['temperature_2m'], 20)) |
         (df['relative_humidity_2m'] > np.percentile(df['relative_humidity_2m'], 80)) |
         (df['relative_humidity_2m'] < np.percentile(df['relative_humidity_2m'], 20))) &
         (df['pm2_5'] > np.percentile(df['pm2_5'], 60))
    ]
    
    choices = [1, 2, 3, 5]  # Group 4 is default if no condition is met
    df['allergy_group'] = np.select(conditions, choices, default=4)
    
    # Add some noise to simulate real-world complexity
    # Randomly change 5% of the classifications to simulate the unpredictable nature of allergies
    random_indices = np.random.choice(df.index, size=int(0.05 * n_samples), replace=False)
    df.loc[random_indices, 'allergy_group'] = np.random.choice([1, 2, 3, 4, 5], size=len(random_indices))
    
    # Drop the date and season columns as they won't be available in real predictions
    df = df.drop(['date', 'season'], axis=1)
    
    return df

if __name__ == "__main__":
    # Generate a sample dataset and save it
    data = generate_test_data(1000)
    data.to_csv("synthetic_test_data.csv", index=False)
    print(f"Generated dataset with {len(data)} samples")
    print(f"Group distribution:")
    print(data['allergy_group'].value_counts())

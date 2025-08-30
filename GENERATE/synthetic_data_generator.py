import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_city_data(num_samples=100, start_date=None, end_date=None):
    """
    Generate synthetic data for multiple cities, combining weather, air pollution, and pollen information.
    
    Args:
        num_samples (int): Number of data points to generate per city
        start_date: Start date for time series data (default: 30 days ago)
        end_date: End date for time series data (default: today)
    
    Returns:
        DataFrame with combined weather, pollution and pollen data
    """
    if start_date is None:
        start_date = datetime.now() - timedelta(days=30)
    if end_date is None:
        end_date = datetime.now()
    
    # Define cities with their coordinates
    cities = {
        'Istanbul': {'lat': 41.0082, 'lon': 28.9784},
        'Ankara': {'lat': 39.9334, 'lon': 32.8597},
        'Izmir': {'lat': 38.4237, 'lon': 27.1428},
        'Antalya': {'lat': 36.8969, 'lon': 30.7133},
        'Bursa': {'lat': 40.1885, 'lon': 29.0610},
        'Adana': {'lat': 37.0000, 'lon': 35.3213}
    }
    
    all_data = []
    
    date_range = pd.date_range(start=start_date, end=end_date, periods=num_samples)
    
    for city_name, coords in cities.items():
        for timestamp in date_range:
            # Add some randomness to coordinates to simulate different locations in the same city
            lat_variation = random.uniform(-0.02, 0.02)
            lon_variation = random.uniform(-0.02, 0.02)
            
            # Create a data point
            data_point = {
                'CITY_NAME': city_name,
                'LAT': coords['lat'] + lat_variation,
                'LON': coords['lon'] + lon_variation,
                'TIME': timestamp
            }
            
            # Generate weather data
            data_point.update({
                'temperature_2m': round(random.uniform(5, 35), 1),  # Temperature in Celsius
                'relative_humidity_2m': round(random.uniform(30, 95), 1),  # Humidity in %
                'precipitation': round(random.uniform(0, 15), 2),  # Precipitation in mm
                'snowfall': round(max(0, random.uniform(-2, 5)), 2),  # Snowfall in cm
                'rain': round(max(0, random.uniform(-1, 15)), 2),  # Rain in mm
                'cloud_cover': round(random.uniform(0, 100), 1),  # Cloud cover in %
                'surface_pressure': round(random.uniform(990, 1030), 1),  # Pressure in hPa
                'wind_speed_10m': round(random.uniform(0, 20), 1),  # Wind speed in m/s
                'wind_direction_10m': round(random.uniform(0, 360), 1),  # Wind direction in degrees
                'soil_temperature_0_to_7cm': round(random.uniform(0, 30), 1),  # Soil temperature in Celsius
                'soil_moisture_0_to_7cm': round(random.uniform(0, 100), 2),  # Soil moisture in %
                'sunshine_duration': round(random.uniform(0, 12), 1),  # Sunshine duration in hours
            })
            
            # Generate air pollution data (repeated columns as in the requirements)
            pollution_data = {
                'pm10': round(random.uniform(5, 80), 2),  # PM10 in μg/m³
                'pm2_5': round(random.uniform(2, 50), 2),  # PM2.5 in μg/m³
                'carbon_dioxide': round(random.uniform(350, 500), 2),  # CO2 in ppm
                'carbon_monoxide': round(random.uniform(0.1, 2), 3),  # CO in ppm
                'nitrogen_dioxide': round(random.uniform(5, 60), 2),  # NO2 in μg/m³
                'sulphur_dioxide': round(random.uniform(1, 30), 2),  # SO2 in μg/m³
                'ozone': round(random.uniform(20, 120), 2),  # O3 in μg/m³
                'aerosol_optical_depth': round(random.uniform(0.01, 0.8), 3),  # AOD dimensionless
                'methane': round(random.uniform(1800, 2000), 2),  # Methane in ppb
                'uv_index': round(random.uniform(0, 12), 1),  # UV index
                'uv_index_clear_sky': round(random.uniform(0, 12), 1),  # Clear sky UV index
                'dust': round(random.uniform(0, 100), 2),  # Dust in μg/m³
            }
            
            # Add pollution data (duplicated as per requirements)
            data_point.update(pollution_data)
            data_point.update(pollution_data)  # Adding these keys again as they are repeated in the requirements
            
            # Generate pollen data - seasonal patterns
            season = get_season(timestamp)
            temp = data_point['temperature_2m']
            humidity = data_point['relative_humidity_2m']
            
            # Pollen levels are affected by season, temperature, and humidity
            pollen_multiplier = calculate_pollen_multiplier(season, temp, humidity)
            
            data_point.update({
                'grass': round(random.uniform(0, 80) * pollen_multiplier['grass'], 2),
                'tree': round(random.uniform(0, 120) * pollen_multiplier['tree'], 2),
                'weed': round(random.uniform(0, 60) * pollen_multiplier['weed'], 2)
            })
            
            all_data.append(data_point)
    
    # Convert to DataFrame
    df = pd.DataFrame(all_data)
    
    return df

def get_season(date):
    """Determine season based on month."""
    month = date.month
    if month in [3, 4, 5]:
        return 'spring'
    elif month in [6, 7, 8]:
        return 'summer'
    elif month in [9, 10, 11]:
        return 'autumn'
    else:
        return 'winter'

def calculate_pollen_multiplier(season, temperature, humidity):
    """Calculate pollen level multipliers based on season, temperature, and humidity."""
    multipliers = {
        'grass': 0.1,
        'tree': 0.1,
        'weed': 0.1
    }
    
    # Season effects
    if season == 'spring':
        multipliers['tree'] = 1.5
        multipliers['grass'] = 0.8
        multipliers['weed'] = 0.4
    elif season == 'summer':
        multipliers['tree'] = 0.3
        multipliers['grass'] = 1.5
        multipliers['weed'] = 1.2
    elif season == 'autumn':
        multipliers['tree'] = 0.1
        multipliers['grass'] = 0.3
        multipliers['weed'] = 1.0
    else:  # winter
        multipliers['tree'] = 0.0
        multipliers['grass'] = 0.0
        multipliers['weed'] = 0.0
    
    # Temperature effect: pollen increases with temperature until about 30°C
    temp_factor = min(temperature / 30, 1) if temperature > 0 else 0
    
    # Humidity effect: moderate humidity is best for pollen, very low or high reduces it
    humidity_factor = 1 - abs((humidity - 60) / 60)
    humidity_factor = max(0.1, humidity_factor)
    
    # Apply environmental factors
    for pollen_type in multipliers:
        multipliers[pollen_type] *= temp_factor * humidity_factor
    
    return multipliers

def save_synthetic_data(df, output_path='synthetic_data.csv'):
    """Save the generated data to a CSV file."""
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Synthetic data saved to {output_path}")
    
    # Print data summary
    print(f"Generated {len(df)} records for {df['CITY_NAME'].nunique()} cities")
    print(f"Date range: {df['TIME'].min()} to {df['TIME'].max()}")
    
    return output_path
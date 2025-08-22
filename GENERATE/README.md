# Synthetic Data Generator for Weather, Air Pollution and Pollen

This directory contains tools to generate synthetic data that combines weather, air pollution, and pollen information for multiple cities.

## Files

- `synthetic_data_generator.py`: Core functionality for generating synthetic data
- `main.py`: Script to generate synthetic data and save it as a CSV
- `data_visualizer.py`: Tool to create visualizations from the generated data

## Data Structure

The generated data includes the following columns:

- `CITY_NAME`: Name of the city
- `LAT`, `LON`: Geographical coordinates
- `TIME`: Timestamp of the measurement
- Weather data: temperature_2m, relative_humidity_2m, precipitation, etc.
- Air pollution data: pm10, pm2_5, carbon_dioxide, etc.
- Pollen data: grass, tree, weed

## How to Use

1. Run the data generator:

```python main.py```


2. Visualize the generated data:

```python data_visualizer.py```



## Data Generation Logic

The synthetic data generator creates realistic values by:

1. Using proper ranges for each environmental metric
2. Implementing seasonal patterns for pollen types
3. Creating correlations between related variables (e.g., temperature affects pollen levels)
4. Varying pollution and pollen levels based on city characteristics
5. Adding randomness to simulate natural variations

## Pollen Data Characteristics

- Tree pollen: Peaks in spring, minimal in winter
- Grass pollen: Highest in summer, low in winter
- Weed pollen: Peaks in late summer/autumn

All pollen types are affected by temperature, humidity, and precipitation in realistic ways.

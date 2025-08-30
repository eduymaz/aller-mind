from db.db_connection import DatabaseConnectionManager
from config import config


class SchemaManager:
    def __init__(self):
        self.db_manager = DatabaseConnectionManager()
        # Use the schema from config instead of trying to get it from connection info
        self.schema = config.db_config.schema

    def create_tables_if_not_exists(self):
        """Create all required tables if they don't exist."""
        self._create_weather_table()
        self._create_air_quality_table()
        self._create_processing_status_table()

    def _create_weather_table(self):
        """Create the weather data table."""
        with self.db_manager.get_cursor() as cursor:
            # Ensure schema exists
            cursor.execute(f'CREATE SCHEMA IF NOT EXISTS "{self.schema}"')
            
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS "{self.schema}"."weather_data" (
                    lat NUMERIC NOT NULL,
                    lon NUMERIC NOT NULL,
                    time TIMESTAMP NOT NULL,
                    temperature_2m NUMERIC,
                    relative_humidity_2m INTEGER,
                    precipitation NUMERIC,
                    snowfall NUMERIC,
                    rain NUMERIC,
                    cloud_cover INTEGER,
                    surface_pressure NUMERIC,
                    wind_speed_10m NUMERIC,
                    wind_direction_10m INTEGER,
                    soil_temperature_0_to_7cm NUMERIC,
                    soil_moisture_0_to_7cm NUMERIC,
                    sunshine_duration NUMERIC,
                    PRIMARY KEY (lat, lon, time)
                )
            """)

    def _create_air_quality_table(self):
        """Create the air quality data table."""
        with self.db_manager.get_cursor() as cursor:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS "{self.schema}"."air_quality_data" (
                    lat NUMERIC NOT NULL,
                    lon NUMERIC NOT NULL,
                    time TIMESTAMP NOT NULL,
                    pm10 NUMERIC,
                    pm2_5 NUMERIC,
                    carbon_dioxide INTEGER,
                    carbon_monoxide NUMERIC,
                    nitrogen_dioxide NUMERIC,
                    sulphur_dioxide NUMERIC,
                    ozone NUMERIC,
                    aerosol_optical_depth NUMERIC,
                    methane NUMERIC,
                    uv_index NUMERIC,
                    uv_index_clear_sky NUMERIC,
                    dust INTEGER,
                    PRIMARY KEY (lat, lon, time)
                )
            """)

    def _create_processing_status_table(self):
        """Create the processing status table for daily execution tracking."""
        with self.db_manager.get_cursor() as cursor:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS "{self.schema}"."processing_status" (
                    date DATE PRIMARY KEY,
                    isprocessed BOOLEAN NOT NULL
                )
            """)

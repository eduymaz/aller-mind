from typing import List

from db.db_connection import DatabaseConnectionManager
from domain.entities import WeatherRecord
from config import config


class WeatherDAO:
    def __init__(self):
        self.db_manager = DatabaseConnectionManager()
        self.schema = config.db_config.schema

    def bulk_insert(self, records: List[WeatherRecord]) -> int:
        """Insert multiple weather records, ignoring conflicts.
        
        Returns:
            The number of records inserted.
        """
        if not records:
            return 0
            
        with self.db_manager.get_cursor() as cursor:
            args = []
            for record in records:
                args.extend([
                    record.lat, record.lon, record.time, 
                    record.temperature_2m, record.relative_humidity_2m,
                    record.precipitation, record.snowfall, record.rain,
                    record.cloud_cover, record.surface_pressure,
                    record.wind_speed_10m, record.wind_direction_10m,
                    record.soil_temperature_0_to_7cm, record.soil_moisture_0_to_7cm,
                    record.sunshine_duration
                ])
            
            placeholders = ", ".join([
                "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                for _ in records
            ])
            
            query = f"""
                INSERT INTO "{self.schema}"."weather_data" (
                    lat, lon, time, temperature_2m, relative_humidity_2m, 
                    precipitation, snowfall, rain, cloud_cover, surface_pressure,
                    wind_speed_10m, wind_direction_10m, soil_temperature_0_to_7cm,
                    soil_moisture_0_to_7cm, sunshine_duration
                ) VALUES {placeholders}
                ON CONFLICT (lat, lon, time) DO NOTHING
            """
            
            cursor.execute(query, args)
            return cursor.rowcount

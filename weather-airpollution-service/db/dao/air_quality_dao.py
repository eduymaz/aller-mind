from typing import List

from db.db_connection import DatabaseConnectionManager
from domain.entities import AirQualityRecord
from config import config


class AirQualityDAO:
    def __init__(self):
        self.db_manager = DatabaseConnectionManager()
        self.schema = config.db_config.schema

    def bulk_insert(self, records: List[AirQualityRecord]) -> int:
        """Insert multiple air quality records, ignoring conflicts.
        
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
                    record.pm10, record.pm2_5, record.carbon_dioxide,
                    record.carbon_monoxide, record.nitrogen_dioxide, 
                    record.sulphur_dioxide, record.ozone, 
                    record.aerosol_optical_depth, record.methane,
                    record.uv_index, record.uv_index_clear_sky, record.dust
                ])
            
            placeholders = ", ".join([
                "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                for _ in records
            ])
            
            query = f"""
                INSERT INTO "{self.schema}"."air_quality_data" (
                    lat, lon, time, pm10, pm2_5, carbon_dioxide,
                    carbon_monoxide, nitrogen_dioxide, sulphur_dioxide,
                    ozone, aerosol_optical_depth, methane, uv_index,
                    uv_index_clear_sky, dust
                ) VALUES {placeholders}
                ON CONFLICT (lat, lon, time) DO NOTHING
            """
            
            cursor.execute(query, args)
            return cursor.rowcount

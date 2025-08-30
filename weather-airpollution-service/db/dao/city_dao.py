from typing import List

from db.db_connection import DatabaseConnectionManager
from domain.entities import City
from config import config


class CityDAO:
    def __init__(self):
        self.db_manager = DatabaseConnectionManager()
        self.schema = config.db_config.schema

    def get_all_cities(self) -> List[City]:
        """Fetch all cities from the database."""
        cities = []
        with self.db_manager.get_cursor() as cursor:
            cursor.execute(f'SELECT plaka, il_adi, lat, lon, northeast_lat, northeast_lon, southwest_lat, southwest_lon FROM "{self.schema}"."city"')
            for row in cursor.fetchall():
                cities.append(City(
                    plaka=row[0],
                    il_adi=row[1],
                    lat=row[2],
                    lon=row[3],
                    northeast_lat=row[4],
                    northeast_lon=row[5],
                    southwest_lat=row[6],
                    southwest_lon=row[7]
                ))
        return cities

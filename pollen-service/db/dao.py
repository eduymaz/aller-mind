import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Optional
from .entities import City, PollenData, PlantData
import logging

logger = logging.getLogger(__name__)

class DatabaseConnection:
    def __init__(self, host, port, dbname, user, password, schema):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self.schema = schema
        self.conn = None
        
    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.dbname,
                user=self.user,
                password=self.password
            )
            return self.conn
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            raise
            
    def close(self):
        if self.conn:
            self.conn.close()

class CityDAO:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        
    def get_all_cities(self) -> List[City]:
        conn = self.db_connection.connect()
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            # Updated SQL query with proper schema quoting and column names
            cursor.execute(f'SELECT plaka, il_adi, lat, lon, northeast_lat, northeast_lon, southwest_lat, southwest_lon FROM "{self.db_connection.schema}"."city"')
            rows = cursor.fetchall()
            cities = [City(**row) for row in rows]
            return cities
        finally:
            self.db_connection.close()

class PollenDataDAO:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        
    def create_tables(self):
        conn = self.db_connection.connect()
        try:
            cursor = conn.cursor()
            # Create pollen_data table with proper schema quoting
            cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS "{self.db_connection.schema}"."pollen_data" (
                id SERIAL PRIMARY KEY,
                lat FLOAT NOT NULL,
                lon FLOAT NOT NULL,
                date DATE NOT NULL,
                pollen_code VARCHAR(50) NOT NULL,
                in_season BOOLEAN NOT NULL,
                upi_value FLOAT NOT NULL,
                health_recommendations TEXT
            )
            """)
            
            # Create plant_data table with proper schema quoting
            cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS "{self.db_connection.schema}"."plant_data" (
                id SERIAL PRIMARY KEY,
                pollen_data_id INTEGER NOT NULL REFERENCES "{self.db_connection.schema}"."pollen_data"(id),
                plant_code VARCHAR(50) NOT NULL,
                plant_in_season BOOLEAN NOT NULL,
                plant_upi_value FLOAT NOT NULL,
                upi_description TEXT,
                picture_url TEXT,
                picture_closeup_url TEXT
            )
            """)
            
            conn.commit()
            logger.info("Tables created successfully")
        except Exception as e:
            conn.rollback()
            logger.error(f"Error creating tables: {e}")
            raise
        finally:
            self.db_connection.close()
            
    def insert_pollen_data(self, pollen_data: PollenData) -> int:
        conn = self.db_connection.connect()
        try:
            cursor = conn.cursor()
            # Updated SQL query with proper schema quoting
            cursor.execute(f"""
            INSERT INTO "{self.db_connection.schema}"."pollen_data"
            (lat, lon, date, pollen_code, in_season, upi_value, health_recommendations)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """, (
                pollen_data.lat,
                pollen_data.lon,
                pollen_data.date,
                pollen_data.pollen_code,
                pollen_data.in_season,
                pollen_data.upi_value,
                pollen_data.health_recommendations
            ))
            pollen_id = cursor.fetchone()[0]
            conn.commit()
            return pollen_id
        except Exception as e:
            conn.rollback()
            logger.error(f"Error inserting pollen data: {e}")
            raise
        finally:
            self.db_connection.close()

class PlantDataDAO:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        
    def insert_plant_data(self, plant_data: PlantData):
        conn = self.db_connection.connect()
        try:
            cursor = conn.cursor()
            # Updated SQL query with proper schema quoting
            cursor.execute(f"""
            INSERT INTO "{self.db_connection.schema}"."plant_data"
            (pollen_data_id, plant_code, plant_in_season, plant_upi_value, 
             upi_description, picture_url, picture_closeup_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                plant_data.pollen_data_id,
                plant_data.plant_code,
                plant_data.plant_in_season,
                plant_data.plant_upi_value,
                plant_data.upi_description,
                plant_data.picture_url,
                plant_data.picture_closeup_url
            ))
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Error inserting plant data: {e}")
            raise
        finally:
            self.db_connection.close()

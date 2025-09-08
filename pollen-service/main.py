import logging
import json
import os
from db.dao import DatabaseConnection, CityDAO, PollenDataDAO, PlantDataDAO
from service.pollen_service import PollenService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Database configuration
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "allermind"
DB_USER = "postgres"
DB_PASSWORD = "123456"
SCHEMA_NAME = "POLLEN"

def main():
    try:
        # Create database connection
        db_connection = DatabaseConnection(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            schema=SCHEMA_NAME
        )
        
        # Create DAOs
        pollen_dao = PollenDataDAO(db_connection)
        plant_dao = PlantDataDAO(db_connection)
        city_dao = CityDAO(db_connection)
        
        # Create service
        pollen_service = PollenService(pollen_dao, plant_dao)
        
        # Step 1: Create tables (only needs to be done once)
        logger.info("Creating tables...")
        pollen_dao.create_tables()
        
        # Step 2: Get all cities
        logger.info("Fetching cities...")
        cities = city_dao.get_all_cities()
        
        # Step 3: Process each city
        for city in cities:
            logger.info(f"Processing city: {city.il_adi}")
            try:
                # Fetch pollen data for the city
                response_data = pollen_service.fetch_pollen_data(city.lat, city.lon)
                
                # Process and store the data
                pollen_service.process_pollen_response(response_data, city.lat, city.lon)
                
                logger.info(f"Successfully processed data for {city.il_adi}")
            except Exception as e:
                logger.error(f"Error processing city {city.il_adi}: {e}")
                continue
                
        logger.info("Pollen data processing completed")
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

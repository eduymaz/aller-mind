import logging
import sys
from datetime import date

from config import config
from db.schema import SchemaManager
from services.data_service import DataService
from db.db_connection import DatabaseConnectionManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def main():
    try:
        logger.info("Starting weather and air pollution data service")
        logger.info(f"Processing date: {date.today().isoformat()}")
        
        # Initialize schema manager and create tables if needed
        if config.create_tables_if_not_exists:
            logger.info("Checking and creating database tables if needed")
            schema_manager = SchemaManager()
            schema_manager.create_tables_if_not_exists()
            
        # Run data processing
        logger.info("Starting data processing for all cities")
        data_service = DataService()
        weather_count, air_quality_count = data_service.fetch_and_store_data_for_all_cities()
        
        logger.info(f"Data processing completed. Weather records: {weather_count}, Air quality records: {air_quality_count}")
        
    except Exception as e:
        logger.exception(f"An error occurred during execution: {str(e)}")
        sys.exit(1)
    finally:
        # Close database connection
        DatabaseConnectionManager().close_connection()
        

if __name__ == "__main__":
    main()

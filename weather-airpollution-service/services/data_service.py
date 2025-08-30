from datetime import date, datetime
import logging
from typing import List, Tuple

from domain.entities import City, ProcessingStatus, WeatherRecord, AirQualityRecord
from domain.converters import weather_data_to_records, air_quality_data_to_records
from db.dao.city_dao import CityDAO
from db.dao.weather_dao import WeatherDAO
from db.dao.air_quality_dao import AirQualityDAO
from db.dao.processing_status_dao import ProcessingStatusDAO
from service import WeatherService, AirQualityService

logger = logging.getLogger(__name__)


class DataService:
    def __init__(self):
        self.city_dao = CityDAO()
        self.weather_dao = WeatherDAO()
        self.air_quality_dao = AirQualityDAO()
        self.processing_status_dao = ProcessingStatusDAO()
        self.weather_service = WeatherService()
        self.air_quality_service = AirQualityService()
    
    def should_process_today(self) -> bool:
        """Check if data should be processed for today based on processing status."""
        today = date.today()
        status = self.processing_status_dao.get_status_for_date(today)
        
        if status is None or not status.isprocessed:
            return True
        
        logger.info(f"Data for today ({today}) has already been processed. Skipping.")
        return False
    
    def mark_today_as_processed(self) -> None:
        """Mark today as processed in the database."""
        today = date.today()
        status = ProcessingStatus(date=today, isprocessed=True)
        self.processing_status_dao.create_or_update_status(status)
        logger.info(f"Marked {today} as processed.")
    
    def fetch_and_store_data_for_all_cities(self) -> Tuple[int, int]:
        """Fetch and store weather and air quality data for all cities.
        
        Returns:
            Tuple containing (weather_records_stored, air_quality_records_stored)
        """
        if not self.should_process_today():
            return 0, 0
            
        cities = self.city_dao.get_all_cities()
        today_str = date.today().isoformat()
        
        total_weather_records = 0
        total_air_quality_records = 0
        
        for city in cities:
            try:
                # Fetch weather data
                weather_data = self.weather_service.fetch(
                    city.lat, city.lon, today_str, today_str
                )
                weather_records = weather_data_to_records(weather_data)
                weather_stored = self.weather_dao.bulk_insert(weather_records)
                total_weather_records += weather_stored
                
                # Fetch air quality data
                air_quality_data = self.air_quality_service.fetch(
                    city.lat, city.lon, today_str, today_str
                )
                air_quality_records = air_quality_data_to_records(air_quality_data)
                air_quality_stored = self.air_quality_dao.bulk_insert(air_quality_records)
                total_air_quality_records += air_quality_stored
                
                logger.info(
                    f"Processed city {city.il_adi}: "
                    f"Weather records: {weather_stored}, "
                    f"Air quality records: {air_quality_stored}"
                )
            
            except Exception as e:
                logger.error(f"Error processing city {city.il_adi}: {str(e)}")
        
        # Mark today as processed after all cities are done
        self.mark_today_as_processed()
        
        return total_weather_records, total_air_quality_records

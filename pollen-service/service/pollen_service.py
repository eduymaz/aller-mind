import requests
import logging
import json
from datetime import datetime, date
from typing import Dict, List, Any
from db.entities import PollenData, PlantData
from db.dao import PollenDataDAO, PlantDataDAO

logger = logging.getLogger(__name__)

class PollenService:
    def __init__(self, pollen_dao: PollenDataDAO, plant_dao: PlantDataDAO):
        self.pollen_dao = pollen_dao
        self.plant_dao = plant_dao
        self.BASE_URL = "https://pollen.googleapis.com/v1/forecast:lookup?key=AIzaSyBBu4qaSpo8kTpJlRYZNKjZIqo-JLdMmIc"
        
    def fetch_pollen_data(self, lat: float, lon: float) -> Dict[str, Any]:
        """Fetch pollen data from the API for a given location"""
        url = f"{self.BASE_URL}&location.longitude={lon}&location.latitude={lat}&days=1"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request error for lat={lat}, lon={lon}: {e}")
            raise
            
    def process_pollen_response(self, response_data: Dict[str, Any], lat: float, lon: float):
        """Process the API response and store data in the database"""
        
        # Extract date from the response - updated for the actual JSON format
        forecast_date = None
        if 'dailyInfo' in response_data and response_data['dailyInfo']:
            date_obj = response_data['dailyInfo'][0].get('date', {})
            if date_obj and isinstance(date_obj, dict):
                year = date_obj.get('year')
                month = date_obj.get('month')
                day = date_obj.get('day')
                if year and month and day:
                    try:
                        forecast_date = date(year, month, day)
                    except ValueError:
                        logger.error(f"Invalid date: year={year}, month={month}, day={day}")
                        forecast_date = datetime.now().date()
                else:
                    forecast_date = datetime.now().date()
            else:
                forecast_date = datetime.now().date()
        else:
            forecast_date = datetime.now().date()
            
        # Process each pollen type
        if 'dailyInfo' in response_data and response_data['dailyInfo']:
            daily_info = response_data['dailyInfo'][0]
            
            if 'pollenTypeInfo' in daily_info:
                for pollen_info in daily_info['pollenTypeInfo']:
                    # Skip if essential data is missing
                    if not pollen_info.get('code'):
                        continue
                        
                    # Extract health recommendations as a string (it's an array in the actual response)
                    health_recommendations = None
                    if 'healthRecommendations' in pollen_info and pollen_info['healthRecommendations']:
                        health_recommendations = '\n'.join(pollen_info['healthRecommendations'])
                    
                    # Get UPI value if available, otherwise default to 0
                    upi_value = 0.0
                    in_season = False
                    
                    if 'indexInfo' in pollen_info and pollen_info['indexInfo']:
                        upi_value = pollen_info['indexInfo'].get('value', 0.0)
                    
                    # Check if inSeason key exists and use its value
                    if 'inSeason' in pollen_info:
                        in_season = pollen_info['inSeason']
                    
                    # Create and save pollen data
                    pollen_data = PollenData(
                        lat=lat,
                        lon=lon,
                        date=forecast_date,
                        pollen_code=pollen_info.get('code', ''),
                        in_season=in_season,
                        upi_value=upi_value,
                        health_recommendations=health_recommendations
                    )
                    
                    # Insert pollen data and get the ID
                    pollen_id = self.pollen_dao.insert_pollen_data(pollen_data)
                    
                    # Process related plant info
                    if 'plantInfo' in daily_info:
                        for plant_info in daily_info['plantInfo']:
                            # Check if this plant has the necessary data
                            if not plant_info.get('code') or 'plantDescription' not in plant_info:
                                continue
                                
                            # Match plant with pollen type
                            plant_type = plant_info.get('plantDescription', {}).get('type', '')
                            if plant_type == pollen_data.pollen_code:
                                # Extract UPI value and description if available
                                plant_upi_value = 0.0
                                upi_description = None
                                plant_in_season = False
                                
                                if 'indexInfo' in plant_info and plant_info['indexInfo']:
                                    plant_upi_value = plant_info['indexInfo'].get('value', 0.0)
                                    upi_description = plant_info['indexInfo'].get('indexDescription', None)
                                
                                if 'inSeason' in plant_info:
                                    plant_in_season = plant_info['inSeason']
                                
                                plant_data = PlantData(
                                    pollen_data_id=pollen_id,
                                    plant_code=plant_info.get('code', ''),
                                    plant_in_season=plant_in_season,
                                    plant_upi_value=plant_upi_value,
                                    upi_description=upi_description,
                                    picture_url=plant_info.get('plantDescription', {}).get('picture', None),
                                    picture_closeup_url=plant_info.get('plantDescription', {}).get('pictureCloseup', None)
                                )
                                self.plant_dao.insert_plant_data(plant_data)

import sys
import os

# Add the Aller-mind directory to sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import methods from CityService, ComponentService, StationService, Request, and Mapper
from domain.city.CityService import create_city
from domain.station.StationService import create_station
from domain.component.ComponentService import create_component
from domain.airpollution.AirpollutionRestClient import fetch_constants
from domain.airpollution.AirpollutionMapper import map_constants_to_entities
from config.dbconnector import close_db_connection

if __name__ == "__main__":
    try:
        # Fetch constants
        constants = fetch_constants()

        # Map constants to entities
        entities = map_constants_to_entities(constants)

        # Save mapped entities to the database
        print("Saving Cities to the database...")
        for city in entities["cities"]:
            create_city(city)

        print("\nSaving Components to the database...")
        for component in entities["components"]:
            create_component(component)

        print("\nSaving Stations to the database...")
        for station in entities["stations"]:
            create_station(station)

        print("\nAll entities saved successfully.")
    finally:
        # Close the database connection after all operations
        close_db_connection()

import sys
import os

# Add the Aller-mind directory to sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import methods from CityService, ComponentService, MeasurementService, and StationService
from domain.city.CityService import create_city, fetch_all_cities
from domain.city.CityEntity import CityEntity
from domain.component.ComponentService import create_component, fetch_all_components
from domain.component.ComponentEntity import ComponentEntity
from domain.measurement.MeasurementService import create_measurement, fetch_all_measurements
from domain.measurement.MeasurementEntity import MeasurementEntity
from domain.station.StationService import create_station, fetch_all_stations
from domain.station.StationEntity import StationEntity
from config.dbconnector import close_db_connection

if __name__ == "__main__":
    try:
        # CityService operations
        city_entity = CityEntity(id=1, external_id="EXT123", name="Sample City")
        create_city(city_entity)
        fetch_all_cities()

        # ComponentService operations
        component_entity = ComponentEntity(id=1, symbol="CO2")
        create_component(component_entity)
        fetch_all_components()

        # MeasurementService operations
        measurement_entity = MeasurementEntity(id=1, station_id="ST123", component_id="CO2", date="2023-01-01", value=42.5)
        create_measurement(measurement_entity)
        fetch_all_measurements()

        # StationService operations
        station_entity = StationEntity(id=1, external_id="EXT456", city_id="CITY123", name="Sample Station", lat="40.7128", lon="-74.0060")
        create_station(station_entity)
        fetch_all_stations()
    finally:
        # Close the database connection after all operations
        close_db_connection()

# Import methods from CityService, ComponentService, StationService, Request, and Mapper
from domain.city.CityService import create_city
from domain.station.StationService import create_station
from domain.component.ComponentService import create_component
from domain.airpollution.AirpollutionRestClient import fetch_constants
from domain.airpollution.AirpollutionMapper import map_constants_to_entities


def seed_database():

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


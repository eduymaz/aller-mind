# Import dbconnector from config
from domain.city.CityRepository import CityRepository

def create_city(city_entity):
    city_repository = CityRepository()
    try:
        city_repository.create(city_entity)
        print("CityEntity instance saved successfully.")
    except Exception as e:
        print(f"Error saving CityEntity instance: {e}")

def fetch_all_cities():
    city_repository = CityRepository()
    try:
        cities = city_repository.select_all()
        print("All cities fetched from the database:")
        for city in cities:
            print(city)
    except Exception as e:
        print(f"Error fetching cities: {e}")
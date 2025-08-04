from domain.station.StationRepository import StationRepository

def create_station(station_entity):
    station_repository = StationRepository()
    try:
        station_repository.create(station_entity)
        print("StationEntity instance saved successfully.")
    except Exception as e:
        print(f"Error saving StationEntity instance: {e}")

def fetch_all_stations():
    station_repository = StationRepository()
    try:
        stations = station_repository.select_all()
        print("All stations fetched from the database:")
        for station in stations:
            print(station)
    except Exception as e:
        print(f"Error fetching stations: {e}")

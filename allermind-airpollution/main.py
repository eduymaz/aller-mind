import sys
import os
from datetime import datetime, timedelta
import time

# Add the Aller-mind directory to sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import necessary functions
from seed_data import seed_database
from domain.airpollution.AirpollutionRestClient import fetch_station_data
from domain.airpollution.AirpollutionMapper import map_station_data_to_measurements
from domain.measurement.MeasurementService import create_measurement
from domain.component.ComponentService import fetch_all_components
from domain.station.StationService import fetch_all_stations
from config.dbconnector import close_db_connection

def prepare_data(station_id=None, start_date=None, end_date=None):
    # Default values for start_date and end_date
    if end_date is None:
        end_date = datetime.now().strftime("%d.%m.%Y %H:%M")
    if start_date is None:
        start_date = (datetime.now() - timedelta(hours=1)).strftime("%d.%m.%Y %H:%M")

    # Fetch station IDs from the database if not provided
    if station_id is None:
        stations = fetch_all_stations()
        station_ids = [station.external_id for station in stations]
    else:
        station_ids = [station_id]

    return station_ids, start_date, end_date

def send_requests_in_batches(station_ids, parameters, start_date, end_date):
    batch_size = 70

    # Split station IDs into batches of 5
    for i in range(0, len(station_ids), batch_size):
        batch = station_ids[i:i + batch_size]
        print(f"\nSending request for batch: {batch}")

        data = {
            "__RequestVerificationToken": "bs2QsnIBFgNzO4uRac1D46SfEunVsuTnT8wYzvxOrTlrn1LWlLCi7wiKgf5eJsrdq3Xx9ZdIb0ixvRvnsZu0ze8ynGq4xka0SOn9SAZsA9o1",
            "StationIds": batch,
            "Parameters": parameters,
            "DataPeriods": "8",
            "StartDateTime": start_date,
            "EndDateTime": end_date
        }

        # Fetch station data
        station_data = fetch_station_data(data)
        print("Station Data:", station_data)

        # Map station data to MeasurementEntity objects
        measurements = map_station_data_to_measurements(station_data)

        # Save measurements to the database immediately
        print("\nSaving measurements to the database...")
        for measurement in measurements:
            create_measurement(measurement)

        # Add a 3-second delay between REST calls
        time.sleep(3)

if __name__ == "__main__":
    try:
        print("Starting the program...")

        # Seed the database
        # seed_database()

        # Prepare parameters for fetch_station_data
        print("\nPreparing parameters for fetch_station_data...")
        components = fetch_all_components()
        parameters = [component.symbol for component in components]

        # Prepare data dynamically
        station_ids, start_date, end_date = prepare_data()

        # Send requests in batches and save measurements
        print("\nSending requests in batches...")
        send_requests_in_batches(station_ids, parameters, start_date, end_date)

        print("\nProgram finished.")

    finally:
        close_db_connection()

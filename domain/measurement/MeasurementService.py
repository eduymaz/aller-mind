from domain.measurement.MeasurementRepository import MeasurementRepository

def create_measurement(measurement_entity):
    measurement_repository = MeasurementRepository()
    try:
        measurement_repository.create(measurement_entity)
        print("MeasurementEntity instance saved successfully.")
    except Exception as e:
        print(f"Error saving MeasurementEntity instance: {e}")

def fetch_all_measurements():
    measurement_repository = MeasurementRepository()
    try:
        measurements = measurement_repository.select_all()
        print("All measurements fetched from the database:")
        for measurement in measurements:
            print(measurement)
    except Exception as e:
        print(f"Error fetching measurements: {e}")
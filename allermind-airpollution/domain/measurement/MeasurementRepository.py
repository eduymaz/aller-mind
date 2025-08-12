from config.dbconnector import cursor
from domain.measurement.MeasurementEntity import MeasurementEntity

class MeasurementRepository:
    @staticmethod
    def create(measurement: MeasurementEntity):
        try:
            # Update the ID using get_next_id
            measurement.id = MeasurementRepository.get_next_id()

            query = "INSERT INTO \"AIRPOLLUTION\".\"MEASUREMENT\" (\"ID\", \"STATION_ID\", \"COMPONENT_ID\", \"DATE\", \"VALUE\") VALUES (%s, %s, %s, %s, %s);"
            cursor.execute(query, (measurement.id, measurement.station_id, measurement.component_id, measurement.date, measurement.value))
            print(f"Measurement {measurement.id} inserted successfully.")
        except Exception as e:
            print(f"Error inserting measurement: {e}")

    @staticmethod
    def select_all():
        try:
            query = "SELECT \"ID\", \"STATION_ID\", \"COMPONENT_ID\", \"DATE\", \"VALUE\" FROM \"AIRPOLLUTION\".\"MEASUREMENT\";"
            cursor.execute(query)
            rows = cursor.fetchall()
            measurements = [MeasurementEntity(id=row[0], station_id=row[1], component_id=row[2], date=row[3], value=row[4]) for row in rows]
            return measurements
        except Exception as e:
            print(f"Error fetching measurements: {e}")
            return []

    @staticmethod
    def get_next_id():
        """Get the next available ID for the MEASUREMENT table."""
        try:
            query = "SELECT MAX(\"ID\") FROM \"AIRPOLLUTION\".\"MEASUREMENT\";"
            cursor.execute(query)
            max_id = cursor.fetchone()[0]
            return (max_id + 1) if max_id is not None else 1
        except Exception as e:
            print(f"Error fetching next ID: {e}")
            return 1

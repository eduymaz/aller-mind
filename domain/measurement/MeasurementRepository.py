from config.dbconnector import cursor
from domain.measurement.MeasurementEntity import MeasurementEntity

class MeasurementRepository:
    @staticmethod
    def create(measurement: MeasurementEntity):
        try:
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

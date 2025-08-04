from config.dbconnector import cursor
from domain.station.StationEntity import StationEntity

class StationRepository:
    @staticmethod
    def create(station: StationEntity):
        try:
            query = "INSERT INTO \"AIRPOLLUTION\".\"STATION\" (\"ID\", \"EXTERNAL_ID\", \"CITY_ID\", \"NAME\", \"LAT\", \"LON\") VALUES (%s, %s, %s, %s, %s, %s);"
            cursor.execute(query, (station.id, station.external_id, station.city_id, station.name, station.lat, station.lon))
            print(f"Station {station.name} inserted successfully.")
        except Exception as e:
            print(f"Error inserting station: {e}")

    @staticmethod
    def select_all():
        try:
            query = "SELECT \"ID\", \"EXTERNAL_ID\", \"CITY_ID\", \"NAME\", \"LAT\", \"LON\" FROM \"AIRPOLLUTION\".\"STATION\";"
            cursor.execute(query)
            rows = cursor.fetchall()
            stations = [StationEntity(id=row[0], external_id=row[1], city_id=row[2], name=row[3], lat=row[4], lon=row[5]) for row in rows]
            return stations
        except Exception as e:
            print(f"Error fetching stations: {e}")
            return []

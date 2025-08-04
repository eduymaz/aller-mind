from config.dbconnector import cursor
from domain.city.CityEntity import CityEntity

class CityRepository:
    @staticmethod
    def create(city: CityEntity):
        try:
            query = "INSERT INTO \"AIRPOLLUTION\".\"CITY\" (\"ID\", \"EXTERNAL_ID\", \"NAME\") VALUES (%s, %s, %s);"
            cursor.execute(query, (city.id, city.external_id, city.name))
            print(f"City {city.name} inserted successfully.")
        except Exception as e:
            print(f"Error inserting city: {e}")

    @staticmethod
    def select_all():
        try:
            query = "SELECT \"ID\", \"EXTERNAL_ID\", \"NAME\" FROM \"AIRPOLLUTION\".\"CITY\";"
            cursor.execute(query)
            rows = cursor.fetchall()
            cities = [CityEntity(id=row[0], external_id=row[1], name=row[2]) for row in rows]
            return cities
        except Exception as e:
            print(f"Error fetching cities: {e}")
            return []
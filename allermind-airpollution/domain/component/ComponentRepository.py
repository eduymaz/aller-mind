from config.dbconnector import cursor
from domain.component.ComponentEntity import ComponentEntity

class ComponentRepository:
    @staticmethod
    def create(component: ComponentEntity):
        try:
            query = "INSERT INTO \"AIRPOLLUTION\".\"COMPONENT\" (\"ID\", \"SYMBOL\") VALUES (%s, %s);"
            cursor.execute(query, (component.id, component.symbol))
            print(f"Component {component.symbol} inserted successfully.")
        except Exception as e:
            print(f"Error inserting component: {e}")

    @staticmethod
    def select_all():
        try:
            query = "SELECT \"ID\", \"SYMBOL\" FROM \"AIRPOLLUTION\".\"COMPONENT\";"
            cursor.execute(query)
            rows = cursor.fetchall()
            components = [ComponentEntity(id=row[0], symbol=row[1]) for row in rows]
            return components
        except Exception as e:
            print(f"Error fetching components: {e}")
            return []

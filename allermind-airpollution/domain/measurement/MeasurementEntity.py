class MeasurementEntity:
    def __init__(self, station_id: str, component_id: str, date: str, value: float):
        self.id = None
        self.station_id = station_id
        self.component_id = component_id
        self.date = date
        self.value = value

    def __repr__(self):
        return f"MeasurementEntity(id={self.id}, station_id='{self.station_id}', component_id='{self.component_id}', date='{self.date}', value={self.value})"

    def to_dict(self):
        return {
            "ID": self.id,
            "STATION_ID": self.station_id,
            "COMPONENT_ID": self.component_id,
            "DATE": self.date,
            "VALUE": self.value
        }

    @staticmethod
    def from_dict(data: dict):
        return MeasurementEntity(
            id=data.get("ID"),
            station_id=data.get("STATION_ID"),
            component_id=data.get("COMPONENT_ID"),
            date=data.get("DATE"),
            value=data.get("VALUE")
        )

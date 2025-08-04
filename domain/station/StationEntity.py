class StationEntity:
    def __init__(self, id: int, external_id: str, city_id: str, name: str, lat: str, lon: str):
        self.id = id
        self.external_id = external_id
        self.city_id = city_id
        self.name = name
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return f"StationEntity(id={self.id}, external_id='{self.external_id}', city_id='{self.city_id}', name='{self.name}', lat='{self.lat}', lon='{self.lon}')"

    def to_dict(self):
        return {
            "ID": self.id,
            "EXTERNAL_ID": self.external_id,
            "CITY_ID": self.city_id,
            "NAME": self.name,
            "LAT": self.lat,
            "LON": self.lon
        }

    @staticmethod
    def from_dict(data: dict):
        return StationEntity(
            id=data.get("ID"),
            external_id=data.get("EXTERNAL_ID"),
            city_id=data.get("CITY_ID"),
            name=data.get("NAME"),
            lat=data.get("LAT"),
            lon=data.get("LON")
        )

class CityEntity:
    def __init__(self, id: int, external_id: str, name: str):
        self.id = id
        self.external_id = external_id
        self.name = name

    def __repr__(self):
        return f"CityEntity(id={self.id}, external_id='{self.external_id}', name='{self.name}')"

    def to_dict(self):
        return {
            "ID": self.id,
            "EXTERNAL_ID": self.external_id,
            "NAME": self.name
        }

    @staticmethod
    def from_dict(data: dict):
        return CityEntity(
            id=data.get("ID"),
            external_id=data.get("EXTERNAL_ID"),
            name=data.get("NAME")
        )
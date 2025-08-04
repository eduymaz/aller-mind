class ComponentEntity:
    def __init__(self, id: int, symbol: str):
        self.id = id
        self.symbol = symbol

    def __repr__(self):
        return f"ComponentEntity(id={self.id}, symbol='{self.symbol}')"

    def to_dict(self):
        return {
            "ID": self.id,
            "SYMBOL": self.symbol
        }

    @staticmethod
    def from_dict(data: dict):
        return ComponentEntity(
            id=data.get("ID"),
            symbol=data.get("SYMBOL")
        )

import requests

class PollenTypeInfo:
    def __init__(self, code, value, category, color):
        self.code = code
        self.value = value
        self.category = category
        self.color = color

class PollenResponse:
    def __init__(self, city, lat, lon, pollen_types):
        self.city = city
        self.lat = lat
        self.lon = lon
        self.pollen_types = pollen_types  # List[PollenTypeInfo]

class PollenService:
    BASE_URL = "https://pollen.googleapis.com/v1/forecast:lookup?key=AIzaSyBBu4qaSpo8kTpJlRYZNKjZIqo-JLdMmIc"

    def fetch(self, city, lat, lon):
        url = f"{self.BASE_URL}&location.longitude={lon}&location.latitude={lat}&days=1"
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        pollen_types = []
        daily_info = data.get("dailyInfo", [])
        if daily_info:
            for pollen in daily_info[0].get("pollenTypeInfo", []):
                code = pollen.get("code")
                index_info = pollen.get("indexInfo", {})
                value = index_info.get("value")
                category = index_info.get("category")
                color = index_info.get("color", {})
                pollen_types.append(PollenTypeInfo(code, value, category, color))
        return PollenResponse(city, lat, lon, pollen_types)

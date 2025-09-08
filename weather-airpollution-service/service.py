import requests
from domain.entities import WeatherData, AirQualityData

class WeatherService:
    def fetch(self, latitude: str, longitude: str, start_date: str, end_date: str) -> WeatherData:
        url = (
            #f"https://archive-api.open-meteo.com/v1/archive?"
            "https://api.open-meteo.com/v1/forecast?"
            f"latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}"
            "&hourly=temperature_2m,relative_humidity_2m,precipitation,snowfall,rain,cloud_cover,"
            "surface_pressure,wind_speed_10m,wind_direction_10m,soil_temperature_0_to_7cm,"
            "soil_moisture_0_to_7cm,sunshine_duration"
        )
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        return WeatherData(latitude, longitude, hourly=data['hourly'])

class AirQualityService:
    def fetch(self, latitude: str, longitude: str, start_date: str, end_date: str) -> AirQualityData:
        url = (
            f"https://air-quality-api.open-meteo.com/v1/air-quality?"
            f"latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}"
            "&hourly=pm10,pm2_5,carbon_dioxide,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,"
            "ozone,aerosol_optical_depth,methane,uv_index,uv_index_clear_sky,dust"
        )
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        return AirQualityData(latitude, longitude, hourly=data['hourly'])

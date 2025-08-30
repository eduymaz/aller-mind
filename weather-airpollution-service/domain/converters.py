from datetime import datetime
from typing import List

from domain.entities import WeatherData, AirQualityData, WeatherRecord, AirQualityRecord


def parse_datetime(time_str: str) -> datetime:
    """Parse datetime string from API response to Python datetime object."""
    return datetime.fromisoformat(time_str)


def weather_data_to_records(data: WeatherData) -> List[WeatherRecord]:
    """Convert WeatherData response to list of WeatherRecord objects."""
    records = []
    time_values = data.hourly["time"]
    
    for i in range(len(time_values)):
        record = WeatherRecord(
            lat=data.latitude,
            lon=data.longitude,
            time=parse_datetime(data.hourly["time"][i]),
            temperature_2m=data.hourly["temperature_2m"][i],
            relative_humidity_2m=data.hourly["relative_humidity_2m"][i],
            precipitation=data.hourly["precipitation"][i],
            snowfall=data.hourly["snowfall"][i],
            rain=data.hourly["rain"][i],
            cloud_cover=data.hourly["cloud_cover"][i],
            surface_pressure=data.hourly["surface_pressure"][i],
            wind_speed_10m=data.hourly["wind_speed_10m"][i],
            wind_direction_10m=data.hourly["wind_direction_10m"][i],
            soil_temperature_0_to_7cm=data.hourly["soil_temperature_0_to_7cm"][i],
            soil_moisture_0_to_7cm=data.hourly["soil_moisture_0_to_7cm"][i],
            sunshine_duration=data.hourly["sunshine_duration"][i]
        )
        records.append(record)
    
    return records


def air_quality_data_to_records(data: AirQualityData) -> List[AirQualityRecord]:
    """Convert AirQualityData response to list of AirQualityRecord objects."""
    records = []
    time_values = data.hourly["time"]
    
    for i in range(len(time_values)):
        record = AirQualityRecord(
            lat=data.latitude,
            lon=data.longitude,
            time=parse_datetime(data.hourly["time"][i]),
            pm10=data.hourly["pm10"][i],
            pm2_5=data.hourly["pm2_5"][i],
            carbon_dioxide=data.hourly["carbon_dioxide"][i],
            carbon_monoxide=data.hourly["carbon_monoxide"][i],
            nitrogen_dioxide=data.hourly["nitrogen_dioxide"][i],
            sulphur_dioxide=data.hourly["sulphur_dioxide"][i],
            ozone=data.hourly["ozone"][i],
            aerosol_optical_depth=data.hourly["aerosol_optical_depth"][i],
            methane=data.hourly["methane"][i],
            uv_index=data.hourly["uv_index"][i],
            uv_index_clear_sky=data.hourly["uv_index_clear_sky"][i],
            dust=data.hourly["dust"][i]
        )
        records.append(record)
    
    return records

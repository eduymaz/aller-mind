from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional, List, Dict, Any


@dataclass
class City:
    plaka: int
    il_adi: str
    lat: str
    lon: str
    northeast_lat: Optional[float] = None
    northeast_lon: Optional[float] = None
    southwest_lat: Optional[float] = None
    southwest_lon: Optional[float] = None


@dataclass
class WeatherData:
    latitude: str
    longitude: str
    hourly: Dict[str, List[Any]]


@dataclass
class AirQualityData:
    latitude: str
    longitude: str
    hourly: Dict[str, List[Any]]


@dataclass
class WeatherRecord:
    lat: str
    lon: str
    time: datetime
    temperature_2m: float
    relative_humidity_2m: int
    precipitation: float
    snowfall: float
    rain: float
    cloud_cover: int
    surface_pressure: float
    wind_speed_10m: float
    wind_direction_10m: int
    soil_temperature_0_to_7cm: float
    soil_moisture_0_to_7cm: float
    sunshine_duration: float


@dataclass
class AirQualityRecord:
    lat: str
    lon: str
    time: datetime
    pm10: float
    pm2_5: float
    carbon_dioxide: int
    carbon_monoxide: float
    nitrogen_dioxide: float
    sulphur_dioxide: float
    ozone: float
    aerosol_optical_depth: float
    methane: float
    uv_index: float
    uv_index_clear_sky: float
    dust: int


@dataclass
class ProcessingStatus:
    date: date
    isprocessed: bool

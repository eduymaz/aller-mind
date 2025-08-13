from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class City:
    plaka: int
    name: str

@dataclass
class Country:
    ilce_id: int
    il_plaka: int
    ilce_adi: str
    lat: float
    lon: float

@dataclass
class WeatherData:
    latitude: float
    longitude: float
    hourly: Dict[str, Any]

@dataclass
class AirQualityData:
    latitude: float
    longitude: float
    hourly: Dict[str, Any]

@dataclass
class CombinedData:
    city_name: str
    country: str
    lat: float
    lon: float
    time: str
    values: Dict[str, Any] = field(default_factory=dict)

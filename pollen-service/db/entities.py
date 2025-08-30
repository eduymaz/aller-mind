from dataclasses import dataclass
from datetime import date
from typing import Optional, List

@dataclass
class City:
    plaka: int
    il_adi: str
    lat: float
    lon: float
    northeast_lat: Optional[float] = None
    northeast_lon: Optional[float] = None
    southwest_lat: Optional[float] = None
    southwest_lon: Optional[float] = None

@dataclass
class PollenData:
    id: Optional[int] = None
    lat: float = 0.0
    lon: float = 0.0
    date: date = None
    pollen_code: str = ""
    in_season: bool = False
    upi_value: float = 0.0
    health_recommendations: Optional[str] = None

@dataclass
class PlantData:
    id: Optional[int] = None
    pollen_data_id: int = 0
    plant_code: str = ""
    plant_in_season: bool = False
    plant_upi_value: float = 0.0
    upi_description: Optional[str] = None
    picture_url: Optional[str] = None
    picture_closeup_url: Optional[str] = None

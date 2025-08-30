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


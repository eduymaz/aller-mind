import csv
from typing import Dict, List
from domain import City, Country

class CityRepository:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def get_city_by_plaka(self, plaka: int) -> City:
        with open(self.filepath, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if int(row['plaka']) == plaka:
                    return City(plaka=int(row['plaka']), name=row['il_adi'])
        return None

class CountryRepository:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def get_country_by_il_plaka(self, il_plaka: int) -> List[Country]:
        countries = []
        with open(self.filepath, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if int(row['il_plaka']) == il_plaka:
                    countries.append(Country(
                        ilce_id=int(row['ilce_id']),
                        il_plaka=int(row['il_plaka']),
                        ilce_adi=row['ilce_adi'],
                        lat=float(row['lat']),
                        lon=float(row['lon'])
                    ))
        return countries

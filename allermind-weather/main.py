from datetime import datetime, timezone
from repository import CityRepository, CountryRepository
from service import WeatherService, AirQualityService
from merge import merge_hourly_data
from exporter import export_to_csv


def run(plaka: int, ilce_adi: str, start_date: str, end_date: str):
    city_repo = CityRepository('city.csv')
    country_repo = CountryRepository('country.csv')
    city = city_repo.get_city_by_plaka(plaka)
    countries = country_repo.get_country_by_il_plaka(plaka)
    # ilce_adi ile eşleşen country bul
    country = next((c for c in countries if c.ilce_adi == ilce_adi), None)
    if not city or not country:
        print("City or Country not found")
        return
    lat, lon = country.lat, country.lon
    weather_service = WeatherService()
    air_service = AirQualityService()
    weather = weather_service.fetch(lat, lon, start_date, end_date)
    air = air_service.fetch(lat, lon, start_date, end_date)
    combined = merge_hourly_data(city.name, country.ilce_adi, lat, lon, weather, air)
    export_to_csv('output.csv', combined)

if __name__ == "__main__":
    # Örnek parametreler
    run(plaka=35, ilce_adi="MENEMEN", start_date="2025-08-06", end_date="2025-08-07")
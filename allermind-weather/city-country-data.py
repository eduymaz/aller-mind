from datetime import datetime, timezone
from repository import CityRepository, CountryRepository
from service import WeatherService, AirQualityService
from merge import merge_hourly_data
from exporter import export_to_csv
import csv
import os


def run_all(start_date: str, end_date: str, output_file: str = 'output.csv'):
    # Dosya yollarını script'in bulunduğu dizinden al
    base_dir = os.path.dirname(os.path.abspath(__file__))
    city_csv = os.path.join(base_dir, 'city.csv')
    country_csv = os.path.join(base_dir, 'country.csv')
    output_csv = os.path.join(base_dir, output_file)

    city_repo = CityRepository(city_csv)
    country_repo = CountryRepository(country_csv)
    weather_service = WeatherService()
    air_service = AirQualityService()

    # Eğer dosya varsa sil, baştan oluştur
    if os.path.exists(output_csv):
        os.remove(output_csv)

    header_written = False

    with open(country_csv, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            plaka = int(row['il_plaka'])
            ilce_adi = row['ilce_adi']
            lat = float(row['lat'])
            lon = float(row['lon'])
            city = city_repo.get_city_by_plaka(plaka)
            if not city:
                print(f"City not found for plaka={plaka}")
                continue
            try:
                weather = weather_service.fetch(lat, lon, start_date, end_date)
                air = air_service.fetch(lat, lon, start_date, end_date)
            except Exception as e:
                print(f"API error for {city.name}, {ilce_adi}: {e}")
                continue
            combined = merge_hourly_data(city.name, ilce_adi, lat, lon, weather, air)
            # İlk yazımda header, sonrakilerde append modunda sadece veri
            export_to_csv(output_csv, combined, write_header=not header_written)
            header_written = True

if __name__ == "__main__":
    run_all(start_date="2025-08-07", end_date="2025-08-08")
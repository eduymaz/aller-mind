from datetime import datetime, timezone
from repository import CityRepository
from service import WeatherService, AirQualityService
from merge import merge_hourly_data
from exporter import export_to_csv
import csv
import os


def run_all_cities(start_date: str, end_date: str, output_file: str = 'city_output.csv'):
    # Dosya yollarını script'in bulunduğu dizinden al
    base_dir = os.path.dirname(os.path.abspath(__file__))
    city_csv = os.path.join(base_dir, 'city.csv')
    output_csv = os.path.join(base_dir, output_file)

    city_repo = CityRepository(city_csv)
    weather_service = WeatherService()
    air_service = AirQualityService()

    # Eğer dosya varsa sil, baştan oluştur
    if os.path.exists(output_csv):
        os.remove(output_csv)

    header_written = False

    with open(city_csv, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            city_name = row['il_adi']
            lat = float(row['lat'])
            lon = float(row['lon'])
            try:
                weather = weather_service.fetch(lat, lon, start_date, end_date)
                air = air_service.fetch(lat, lon, start_date, end_date)
            except Exception as e:
                print(f"API error for {city_name}: {e}")
                continue
            combined = merge_hourly_data(city_name, "", lat, lon, weather, air)
            # İlk yazımda header, sonrakilerde append modunda sadece veri
            export_to_csv(output_csv, combined, write_header=not header_written, exclude_country=True)
            header_written = True

if __name__ == "__main__":
    run_all_cities(start_date="2024-08-01", end_date="2025-08-01")
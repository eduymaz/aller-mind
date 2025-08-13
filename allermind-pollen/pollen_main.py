import os
import csv
from pollen_service import PollenService
from pollen_exporter import export_pollen_csv

def run(city_csv_path, output_csv_path):
    pollen_service = PollenService()
    pollen_responses = []
    with open(city_csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            city = row['il_adi']
            lat = float(row['lat'])
            lon = float(row['lon'])
            try:
                resp = pollen_service.fetch(city, lat, lon)
                pollen_responses.append(resp)
            except Exception as e:
                print(f"API error for {city}: {e}")
    export_pollen_csv(output_csv_path, pollen_responses)

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    city_csv = os.path.join(base_dir, "city.csv")
    output_csv = os.path.join(base_dir, "pollen_output.csv")
    run(city_csv, output_csv)

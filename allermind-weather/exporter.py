import csv
from domain import CombinedData

def export_to_csv(filepath: str, combined_data: list):
    if not combined_data:
        return
    # Kolonlar: CITY_NAME, COUNTRY, LAT, LON, TIME + tüm values keyleri
    fieldnames = ['CITY_NAME', 'COUNTRY', 'LAT', 'LON', 'TIME'] + list(combined_data[0].values.keys())
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for data in combined_data:
            row = {
                'CITY_NAME': data.city_name,
                'COUNTRY': data.country,
                'LAT': data.lat,
                'LON': data.lon,
                'TIME': data.time,
                **data.values
            }
            writer.writerow(row)

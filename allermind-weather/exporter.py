import csv
from domain import CombinedData

def export_to_csv(filepath: str, combined_data: list, write_header: bool = True, exclude_country: bool = False):
    if not combined_data:
        return
    value_keys = [k for k in combined_data[0].values.keys() if k != 'TIME']
    fieldnames = ['CITY_NAME', 'LAT', 'LON', 'TIME'] + value_keys if exclude_country else ['CITY_NAME', 'COUNTRY', 'LAT', 'LON', 'TIME'] + value_keys
    mode = 'a' if not write_header else 'w'
    with open(filepath, mode, newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        for data in combined_data:
            row = {
                'CITY_NAME': data.city_name,
                'LAT': data.lat,
                'LON': data.lon,
                'TIME': data.time,
                **{k: v for k, v in data.values.items() if k != 'TIME'}
            }
            if not exclude_country:
                row['COUNTRY'] = data.country
            writer.writerow(row)

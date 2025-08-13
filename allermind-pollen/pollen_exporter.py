import csv

def export_pollen_csv(filepath, pollen_responses):
    # Kolonlar: CITY, LAT, LON, POLLEN_CODE, VALUE, CATEGORY, COLOR_RED, COLOR_GREEN, COLOR_BLUE
    fieldnames = [
        "CITY", "LAT", "LON", "POLLEN_CODE", "VALUE", "CATEGORY", "COLOR_RED", "COLOR_GREEN", "COLOR_BLUE"
    ]
    with open(filepath, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for resp in pollen_responses:
            for pollen in resp.pollen_types:
                row = {
                    "CITY": resp.city,
                    "LAT": resp.lat,
                    "LON": resp.lon,
                    "POLLEN_CODE": pollen.code,
                    "VALUE": pollen.value,
                    "CATEGORY": pollen.category,
                    "COLOR_RED": pollen.color.get("red", ""),
                    "COLOR_GREEN": pollen.color.get("green", ""),
                    "COLOR_BLUE": pollen.color.get("blue", "")
                }
                writer.writerow(row)

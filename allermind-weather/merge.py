from domain import WeatherData, AirQualityData, CombinedData

def merge_hourly_data(city_name, country_name, lat, lon, weather: WeatherData, air: AirQualityData):
    times = weather.hourly['time']
    combined = []
    for idx, time in enumerate(times):
        values = {}
        # Weather hourly values
        for key, arr in weather.hourly.items():
            if key == 'time': continue
            values[key] = arr[idx] if idx < len(arr) else None
        # AirQuality hourly values
        for key, arr in air.hourly.items():
            if key == 'time': continue
            values[key] = arr[idx] if idx < len(arr) else None
        combined.append(CombinedData(
            city_name=city_name,
            country=country_name,
            lat=lat,
            lon=lon,
            time=time,
            values=values
        ))
    return combined

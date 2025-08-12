from domain.city.CityEntity import CityEntity
from domain.component.ComponentEntity import ComponentEntity
from domain.station.StationEntity import StationEntity
from domain.measurement.MeasurementEntity import MeasurementEntity

def map_constants_to_entities(constants):
    entities = {
        "cities": [],
        "components": [],
        "stations": []
    }

    # Map CityEntity
    for index, city in enumerate(constants["Object"]["CityId"], start=1):
        entities["cities"].append(CityEntity(
            id=index,
            external_id=city["Id"],
            name=city["Name"]
        ))

    # Map ComponentEntity
    for index, parameter in enumerate(constants["Object"]["Parameters"], start=1):
        entities["components"].append(ComponentEntity(
            id=index,
            symbol=parameter["Id"]
        ))

    # Map StationEntity
    for index, station in enumerate(constants["Object"]["StationIds"], start=1):
        location = station["Location"].replace("POINT (", "").replace(")", "").split()
        entities["stations"].append(StationEntity(
            id=index,
            external_id=station["id"],
            city_id=station["CityId"],
            name=station["Name"],
            lat=location[0],
            lon=location[1]
        ))

    return entities

def map_station_data_to_measurements(response_data):
    measurements = []

    for data_entry in response_data["Object"]["Data"]:
        station_id = data_entry["Stationid"]
        read_time = data_entry["ReadTime"]

        for component_id, value in data_entry.items():
            if component_id not in ["Stationid", "ReadTime"] and value is not None:
                measurements.append(MeasurementEntity(
                    station_id=station_id,
                    component_id=component_id,
                    date=read_time,
                    value=value
                ))
    return measurements

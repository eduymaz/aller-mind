package com.allermind.model.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class WeatherAirQualityResponse {
    private String cityName;
    private String latitude;
    private String longitude;
    private WeatherRecord weatherRecord;
    private AirQualityRecord airQualityRecord;
}

package com.allermind.weather.application.dto;

import com.allermind.weather.domain.entity.AirQualityRecord;
import com.allermind.weather.domain.entity.WeatherRecord;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class WeatherAirQualityResponse {
    
    private String cityName;
    private WeatherRecord weatherRecord;
    private AirQualityRecord airQualityRecord;
}

package com.allermind.weather.application.dto.external;

import java.util.List;
import java.util.Map;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * DTO for Weather API response from Open-Meteo
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class WeatherApiResponse {
    
    private String latitude;
    private String longitude;
    private Map<String, List<Object>> hourly;
}

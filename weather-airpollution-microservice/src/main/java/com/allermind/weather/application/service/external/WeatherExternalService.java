package com.allermind.weather.application.service.external;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import com.allermind.weather.application.dto.external.WeatherApiResponse;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

/**
 * Service for fetching weather data from Open-Meteo API
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class WeatherExternalService {
    
    private final RestTemplate restTemplate;
    private static final String WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast";
    
    public WeatherApiResponse fetchWeatherData(String latitude, String longitude, LocalDate date) {
        String dateStr = date.format(DateTimeFormatter.ISO_DATE);
        
        String url = UriComponentsBuilder.fromUriString(WEATHER_API_URL)
                .queryParam("latitude", latitude)
                .queryParam("longitude", longitude)
                .queryParam("start_date", dateStr)
                .queryParam("end_date", dateStr)
                .queryParam("hourly", String.join(",",
                        "temperature_2m",
                        "relative_humidity_2m",
                        "precipitation",
                        "snowfall",
                        "rain",
                        "cloud_cover",
                        "surface_pressure",
                        "wind_speed_10m",
                        "wind_direction_10m",
                        "soil_temperature_0_to_7cm",
                        "soil_moisture_0_to_7cm",
                        "sunshine_duration"
                ))
                .toUriString();
        
        log.debug("Fetching weather data from: {}", url);
        
        try {
            WeatherApiResponse response = restTemplate.getForObject(url, WeatherApiResponse.class);
            log.info("Successfully fetched weather data for lat={}, lon={}, date={}", 
                    latitude, longitude, dateStr);
            return response;
        } catch (Exception e) {
            log.error("Error fetching weather data for lat={}, lon={}, date={}: {}", 
                    latitude, longitude, dateStr, e.getMessage());
            throw new RuntimeException("Failed to fetch weather data", e);
        }
    }
}

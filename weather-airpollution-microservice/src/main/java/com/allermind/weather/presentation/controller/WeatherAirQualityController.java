package com.allermind.weather.presentation.controller;

import com.allermind.weather.application.dto.WeatherAirQualityResponse;
import com.allermind.weather.application.service.WeatherAirQualityService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/weather-air-quality")
@RequiredArgsConstructor
public class WeatherAirQualityController {
    
    private final WeatherAirQualityService weatherAirQualityService;
    
    @GetMapping("/{cityName}")
    public ResponseEntity<WeatherAirQualityResponse> getWeatherAndAirQuality(
            @PathVariable String cityName) {
        
        WeatherAirQualityResponse response = weatherAirQualityService
                .getWeatherAndAirQualityByCityName(cityName);
        
        return ResponseEntity.ok(response);
    }
}

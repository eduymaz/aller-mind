package com.allermind.weather.presentation.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.allermind.weather.application.dto.WeatherAirQualityResponse;
import com.allermind.weather.application.service.WeatherAirQualityService;

import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/api/v1/weather-air-quality")
@RequiredArgsConstructor
public class WeatherAirQualityController {
    
    private final WeatherAirQualityService weatherAirQualityService;
    
    @GetMapping
    public ResponseEntity<WeatherAirQualityResponse> getWeatherAndAirQuality(
            @RequestParam String lat,
            @RequestParam String lon) {
        
        WeatherAirQualityResponse response = weatherAirQualityService
                .getWeatherAndAirQualityByCoordinates(lat, lon);
        
        return ResponseEntity.ok(response);
    }
}

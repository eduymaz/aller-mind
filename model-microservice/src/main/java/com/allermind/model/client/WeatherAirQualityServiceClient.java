package com.allermind.model.client;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import com.allermind.model.dto.WeatherAirQualityResponse;

import lombok.extern.slf4j.Slf4j;

@Component
@Slf4j
public class WeatherAirQualityServiceClient {

    private final RestTemplate restTemplate;
    private final String weatherServiceBaseUrl;

    public WeatherAirQualityServiceClient(RestTemplate restTemplate,
                                         @Value("${weather.service.base-url:http://localhost:8383}") String weatherServiceBaseUrl) {
        this.restTemplate = restTemplate;
        this.weatherServiceBaseUrl = weatherServiceBaseUrl;
    }

    public WeatherAirQualityResponse getWeatherAirQualityData(String lat, String lon) {
        try {
            String url = UriComponentsBuilder.fromUriString(weatherServiceBaseUrl)
                    .path("/api/v1/weather-air-quality")
                    .queryParam("lat", lat)
                    .queryParam("lon", lon)
                    .toUriString();

            log.info("Calling weather air quality service with URL: {}", url);

            ResponseEntity<WeatherAirQualityResponse> response = restTemplate.exchange(
                    url,
                    HttpMethod.GET,
                    null,
                    WeatherAirQualityResponse.class
            );

            return response.getBody();
        } catch (Exception e) {
            log.error("Error calling weather air quality service: {}", e.getMessage(), e);
            throw new RuntimeException("Failed to fetch weather air quality data", e);
        }
    }
}

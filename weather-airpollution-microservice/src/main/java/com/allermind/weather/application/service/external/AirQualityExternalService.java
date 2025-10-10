package com.allermind.weather.application.service.external;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import com.allermind.weather.application.dto.external.AirQualityApiResponse;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

/**
 * Service for fetching air quality data from Open-Meteo API
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class AirQualityExternalService {
    
    private final RestTemplate restTemplate;
    private static final String AIR_QUALITY_API_URL = "https://air-quality-api.open-meteo.com/v1/air-quality";
    
    public AirQualityApiResponse fetchAirQualityData(String latitude, String longitude, LocalDate date) {
        String dateStr = date.format(DateTimeFormatter.ISO_DATE);
        
        String url = UriComponentsBuilder.fromUriString(AIR_QUALITY_API_URL)
                .queryParam("latitude", latitude)
                .queryParam("longitude", longitude)
                .queryParam("start_date", dateStr)
                .queryParam("end_date", dateStr)
                .queryParam("hourly", String.join(",",
                        "pm10",
                        "pm2_5",
                        "carbon_dioxide",
                        "carbon_monoxide",
                        "nitrogen_dioxide",
                        "sulphur_dioxide",
                        "ozone",
                        "aerosol_optical_depth",
                        "methane",
                        "uv_index",
                        "uv_index_clear_sky",
                        "dust"
                ))
                .toUriString();
        
        log.debug("Fetching air quality data from: {}", url);
        
        try {
            AirQualityApiResponse response = restTemplate.getForObject(url, AirQualityApiResponse.class);
            log.info("Successfully fetched air quality data for lat={}, lon={}, date={}", 
                    latitude, longitude, dateStr);
            return response;
        } catch (Exception e) {
            log.error("Error fetching air quality data for lat={}, lon={}, date={}: {}", 
                    latitude, longitude, dateStr, e.getMessage());
            throw new RuntimeException("Failed to fetch air quality data", e);
        }
    }
}

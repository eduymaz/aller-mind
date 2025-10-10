package com.allermind.pollen.service.external;

import java.time.LocalDate;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import com.allermind.pollen.dto.external.GooglePollenApiResponse;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

/**
 * Service for fetching pollen data from Google Pollen API
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class GooglePollenExternalService {
    
    private final RestTemplate restTemplate;
    
    @Value("${google.pollen.api.key:AIzaSyBBu4qaSpo8kTpJlRYZNKjZIqo-JLdMmIc}")
    private String apiKey;
    
    private static final String POLLEN_API_URL = "https://pollen.googleapis.com/v1/forecast:lookup";
    
    /**
     * Fetch pollen data from Google Pollen API for given coordinates
     * 
     * @param latitude Location latitude
     * @param longitude Location longitude
     * @return GooglePollenApiResponse containing pollen data
     */
    public GooglePollenApiResponse fetchPollenData(String latitude, String longitude) {
        String url = UriComponentsBuilder.fromUriString(POLLEN_API_URL)
                .queryParam("key", apiKey)
                .queryParam("location.latitude", latitude)
                .queryParam("location.longitude", longitude)
                .queryParam("days", 2)
                .toUriString();
        
        log.debug("Fetching pollen data from: {}", url.replace(apiKey, "***"));
        
        try {
            GooglePollenApiResponse response = restTemplate.getForObject(url, GooglePollenApiResponse.class);
            
            // Filter dailyInfo to keep only today's data
            if (response != null && response.getDailyInfo() != null) {
                LocalDate today = LocalDate.now();
                response.setDailyInfo(
                    response.getDailyInfo().stream()
                        .filter(dailyInfo -> {
                            if (dailyInfo.getDate() != null) {
                                LocalDate dailyDate = LocalDate.of(
                                    dailyInfo.getDate().getYear(),
                                    dailyInfo.getDate().getMonth(),
                                    dailyInfo.getDate().getDay()
                                );
                                return dailyDate.isEqual(today);
                            }
                            return false;
                        })
                        .toList()
                );
            }
            
            log.info("Successfully fetched pollen data for lat={}, lon={}", latitude, longitude);
            return response;
        } catch (Exception e) {
            log.error("Error fetching pollen data for lat={}, lon={}: {}", 
                    latitude, longitude, e.getMessage());
            throw new RuntimeException("Failed to fetch pollen data", e);
        }
    }
}

package com.allermind.model.client;

import java.util.UUID;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import com.allermind.model.dto.AllergyClassificationResponse;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Component
@RequiredArgsConstructor
@Slf4j
public class UserPreferenceServiceClient {
    
    private final RestTemplate restTemplate;
    
    @Value("${user.preference.service.base-url:http://localhost:9191}")
    private String userPreferenceServiceUrl;
    
    public AllergyClassificationResponse getUserPreference(UUID userId) {
        try {
            String url = userPreferenceServiceUrl + "/api/v1/allergy-classification/user/" + userId;
            log.info("Calling user preference service: {}", url);
            
            AllergyClassificationResponse response = restTemplate.getForObject(url, AllergyClassificationResponse.class);
            log.info("Successfully retrieved user preference for user: {}", userId);
            
            return response;
        } catch (Exception e) {
            log.error("Error calling user preference service for user {}: {}", userId, e.getMessage(), e);
            throw new RuntimeException("Failed to retrieve user preference", e);
        }
    }
}
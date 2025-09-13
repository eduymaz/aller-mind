package com.allermind.model.client;

import java.util.List;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import com.allermind.model.dto.PollenResponse;

import lombok.extern.slf4j.Slf4j;

@Component
@Slf4j
public class PollenServiceClient {

    private final RestTemplate restTemplate;
    private final String pollenServiceBaseUrl;

    public PollenServiceClient(RestTemplate restTemplate,
                              @Value("${pollen.service.base-url:http://localhost:8282}") String pollenServiceBaseUrl) {
        this.restTemplate = restTemplate;
        this.pollenServiceBaseUrl = pollenServiceBaseUrl;
    }

    public List<PollenResponse> getPollenData(String lat, String lon) {
        try {
            String url = UriComponentsBuilder.fromUriString(pollenServiceBaseUrl)
                    .path("/api/pollen")
                    .queryParam("lat", lat)
                    .queryParam("lon", lon)
                    .toUriString();

            log.info("Calling pollen service with URL: {}", url);

            ResponseEntity<List<PollenResponse>> response = restTemplate.exchange(
                    url,
                    HttpMethod.GET,
                    null,
                    new ParameterizedTypeReference<List<PollenResponse>>() {}
            );

            return response.getBody();
        } catch (Exception e) {
            log.error("Error calling pollen service: {}", e.getMessage(), e);
            throw new RuntimeException("Failed to fetch pollen data", e);
        }
    }
}

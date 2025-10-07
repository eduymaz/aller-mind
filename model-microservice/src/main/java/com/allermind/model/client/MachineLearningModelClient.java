package com.allermind.model.client;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import com.allermind.model.dto.ModelPredictionRequest;
import com.allermind.model.dto.ModelPredictionResponse;

import lombok.extern.slf4j.Slf4j;

@Component
@Slf4j
public class MachineLearningModelClient {

    private final RestTemplate restTemplate;
    private final String mlModelServiceBaseUrl;

    public MachineLearningModelClient(RestTemplate restTemplate,
                                     @Value("${ml.model.service.base-url:http://localhost:8000}") String mlModelServiceBaseUrl) {
        this.restTemplate = restTemplate;
        this.mlModelServiceBaseUrl = mlModelServiceBaseUrl;
    }

    public ModelPredictionResponse getPrediction(ModelPredictionRequest request) {
        try {
            String url = mlModelServiceBaseUrl + "/api/v1/predict";

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            HttpEntity<ModelPredictionRequest> entity = new HttpEntity<>(request, headers);

            log.info("Calling ML model service with URL: {}", url);
            log.debug("Request body: {}", request);

            ResponseEntity<ModelPredictionResponse> response = restTemplate.exchange(
                    url,
                    HttpMethod.POST,
                    entity,
                    ModelPredictionResponse.class
            );

            ModelPredictionResponse mlResponse = response.getBody();
            
            log.debug("Raw response status: {}", response.getStatusCode());
            log.debug("Raw response body: {}", mlResponse);
            
            if (mlResponse != null && !Boolean.TRUE.equals(mlResponse.getSuccess())) {
                log.error("ML model returned error: {}", mlResponse.getMessage());
                throw new RuntimeException("ML model error: " + mlResponse.getMessage());
            }
            
            if (mlResponse != null) {
                log.info("ML model response received successfully - Risk Score: {}, Risk Level: {}, User Group: {} (ID: {})", 
                    mlResponse.getRiskScore(), 
                    mlResponse.getRiskLevel(),
                    mlResponse.getUserGroup() != null ? mlResponse.getUserGroup().getGroupName() : "null",
                    mlResponse.getUserGroup() != null ? mlResponse.getUserGroup().getGroupId() : "null");
                
                if (mlResponse.getPredictions() != null) {
                    log.info("Legacy predictions count: {}", mlResponse.getPredictions().size());
                }
                
                // Log additional fields for debugging
                log.debug("Confidence: {}, Model Version: {}, Data Quality Score: {}", 
                    mlResponse.getConfidence(), 
                    mlResponse.getModelVersion(), 
                    mlResponse.getDataQualityScore());
                    
                if (mlResponse.getPollenSpecificRisks() != null) {
                    log.debug("High risk pollens: {}", mlResponse.getPollenSpecificRisks().getHighRiskPollens());
                    log.debug("Cross reactive foods: {}", mlResponse.getPollenSpecificRisks().getCrossReactiveFoods());
                }
            } else {
                log.warn("Received null response from ML model service");
            }

            return mlResponse;
        } catch (Exception e) {
            log.error("Error calling ML model service: {}", e.getMessage(), e);
            throw new RuntimeException("Failed to get prediction from ML model", e);
        }
    }
}

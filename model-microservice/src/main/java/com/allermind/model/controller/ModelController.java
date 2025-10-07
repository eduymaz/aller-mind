package com.allermind.model.controller;

import java.util.UUID;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.allermind.model.dto.AllerMindResponse;
import com.allermind.model.service.AllerMindModelService;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@RestController
@RequestMapping("/api/v1/model")
@RequiredArgsConstructor
@Slf4j
public class ModelController {

    private final AllerMindModelService allerMindModelService;

    @GetMapping("/prediction")
    public ResponseEntity<AllerMindResponse> getPrediction(
            @RequestParam String lat,
            @RequestParam String lon,
            @RequestParam String userId) {
        
        log.info("Received prediction request for coordinates: {}, {} and user: {}", 
                lat, lon, userId);

        AllerMindResponse response = allerMindModelService.processAllerMindRequest(lat, lon, UUID.fromString(userId));
        
        log.info("Returning prediction response with risk level: {}", response.getOverallRiskLevel());
        
        return ResponseEntity.ok(response);
    }

    @PostMapping("/prediction")
    public ResponseEntity<AllerMindResponse> getPredictionPost(
            @RequestParam String lat,
            @RequestParam String lon,
            @RequestParam String userId) {
        
        log.info("Received POST prediction request for coordinates: {}, {} and user: {}", 
                lat, lon, userId);

        AllerMindResponse response = allerMindModelService.processAllerMindRequest(lat, lon, UUID.fromString(userId));
        
        log.info("Returning prediction response with risk level: {}", response.getOverallRiskLevel());
        
        return ResponseEntity.ok(response);
    }

    @GetMapping("/health")
    public ResponseEntity<String> health() {
        return ResponseEntity.ok("Model Service is healthy");
    }
}

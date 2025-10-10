package com.allermind.pollen.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.allermind.pollen.service.scheduled.PollenDataProcessingService;

import lombok.RequiredArgsConstructor;

/**
 * Admin controller for manual pollen data processing operations
 * This should be secured in production
 */
@RestController
@RequestMapping("/api/v1/admin/pollen-processing")
@RequiredArgsConstructor
public class PollenDataProcessingController {
    
    private final PollenDataProcessingService pollenDataProcessingService;
    
    /**
     * Manual trigger endpoint for testing
     * POST /api/v1/admin/pollen-processing/trigger
     */
    @PostMapping("/trigger")
    public ResponseEntity<PollenDataProcessingService.PollenProcessingSummary> triggerPollenDataProcessing() {
        PollenDataProcessingService.PollenProcessingSummary summary = 
                pollenDataProcessingService.fetchAndStoreDataForAllCities();
        return ResponseEntity.ok(summary);
    }
}

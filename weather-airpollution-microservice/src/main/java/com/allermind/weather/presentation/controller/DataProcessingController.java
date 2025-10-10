package com.allermind.weather.presentation.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.allermind.weather.application.service.scheduled.DataProcessingService;

import lombok.RequiredArgsConstructor;

/**
 * Admin controller for manual data processing operations
 * This should be secured in production
 */
@RestController
@RequestMapping("/api/v1/admin/data-processing")
@RequiredArgsConstructor
public class DataProcessingController {
    
    private final DataProcessingService dataProcessingService;
    
    /**
     * Manual trigger endpoint for testing
     * POST /api/v1/admin/data-processing/trigger
     */
    @PostMapping("/trigger")
    public ResponseEntity<DataProcessingService.DataProcessingSummary> triggerDataProcessing() {
        DataProcessingService.DataProcessingSummary summary = 
                dataProcessingService.fetchAndStoreDataForAllCities();
        return ResponseEntity.ok(summary);
    }
}

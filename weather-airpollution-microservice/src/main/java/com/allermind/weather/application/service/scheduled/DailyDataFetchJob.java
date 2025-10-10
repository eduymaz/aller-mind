package com.allermind.weather.application.service.scheduled;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

/**
 * Scheduled job that runs daily at midnight (00:00) to fetch and store
 * weather and air quality data for all cities
 */
@Component
@RequiredArgsConstructor
@Slf4j
public class DailyDataFetchJob {
    
    private final DataProcessingService dataProcessingService;
    
    /**
     * Scheduled to run daily at 00:00
     * Cron expression: "0 0 0 * * *" = second minute hour day month weekday
     */
    @Scheduled(cron = "0 0/5 * * * *")
    public void fetchDailyData() {
        log.info("===== Starting daily data fetch job =====");
        
        try {
            DataProcessingService.DataProcessingSummary summary = 
                    dataProcessingService.fetchAndStoreDataForAllCities();
            
            log.info("===== Daily data fetch job completed successfully =====");
            log.info("Summary: Cities: {}, Weather: {}, Air Quality: {}, Status: {}",
                    summary.citiesProcessed(),
                    summary.weatherRecordsStored(),
                    summary.airQualityRecordsStored(),
                    summary.status());
            
        } catch (Exception e) {
            log.error("===== Daily data fetch job failed =====", e);
        }
    }
    
    /**
     * Optional: Manual trigger for testing purposes
     * Can be removed in production or exposed via admin endpoint
     */
    public void triggerManually() {
        log.info("Manual trigger initiated");
        fetchDailyData();
    }
}

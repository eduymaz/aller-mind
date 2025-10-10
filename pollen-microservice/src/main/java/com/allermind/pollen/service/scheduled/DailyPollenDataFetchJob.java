package com.allermind.pollen.service.scheduled;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

/**
 * Scheduled job that runs daily at midnight (00:00) to fetch and store
 * pollen data for all cities from Google Pollen API
 */
@Component
@RequiredArgsConstructor
@Slf4j
public class DailyPollenDataFetchJob {
    
    private final PollenDataProcessingService pollenDataProcessingService;
    
    /**
     * Scheduled to run daily at 00:00
     * Cron expression: "0 0 0 * * *" = second minute hour day month weekday
     */
    @Scheduled(cron = "0 0/5 * * * *")
    public void fetchDailyPollenData() {
        log.info("===== Starting daily pollen data fetch job =====");
        
        try {
            PollenDataProcessingService.PollenProcessingSummary summary = 
                    pollenDataProcessingService.fetchAndStoreDataForAllCities();
            
            log.info("===== Daily pollen data fetch job completed successfully =====");
            log.info("Summary: Cities: {}, Pollen records: {}, Plant records: {}, Status: {}",
                    summary.citiesProcessed(),
                    summary.pollenRecordsStored(),
                    summary.plantRecordsStored(),
                    summary.status());
            
        } catch (Exception e) {
            log.error("===== Daily pollen data fetch job failed =====", e);
        }
    }
    
    /**
     * Optional: Manual trigger for testing purposes
     * Can be removed in production or exposed via admin endpoint
     */
    public void triggerManually() {
        log.info("Manual trigger initiated for pollen data fetch");
        fetchDailyPollenData();
    }
}

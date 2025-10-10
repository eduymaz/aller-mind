package com.allermind.pollen.service.scheduled;

import java.time.LocalDate;
import java.util.List;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.allermind.pollen.dto.external.GooglePollenApiResponse;
import com.allermind.pollen.model.City;
import com.allermind.pollen.model.PollenData;
import com.allermind.pollen.model.ProcessingStatus;
import com.allermind.pollen.repository.CityRepository;
import com.allermind.pollen.repository.PollenDataRepository;
import com.allermind.pollen.repository.ProcessingStatusRepository;
import com.allermind.pollen.service.external.GooglePollenExternalService;
import com.allermind.pollen.service.mapper.PollenDataMapper;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

/**
 * Service for processing pollen data for all cities
 * This service is called by the scheduled job daily at midnight
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class PollenDataProcessingService {
    
    private final CityRepository cityRepository;
    private final PollenDataRepository pollenDataRepository;
    private final ProcessingStatusRepository processingStatusRepository;
    
    private final GooglePollenExternalService googlePollenExternalService;
    private final PollenDataMapper pollenDataMapper;
    
    /**
     * Check if data should be processed for today
     */
    public boolean shouldProcessToday() {
        LocalDate today = LocalDate.now();
        return processingStatusRepository.findByDate(today)
                .map(status -> !status.getIsprocessed())
                .orElse(true);
    }
    
    /**
     * Mark today as processed in the database
     */
    @Transactional
    public void markTodayAsProcessed() {
        LocalDate today = LocalDate.now();
        ProcessingStatus status = new ProcessingStatus(today, true);
        processingStatusRepository.save(status);
        log.info("Marked {} as processed", today);
    }
    
    /**
     * Fetch and store pollen data for all cities
     * Returns a summary of processed records
     */
    //@Transactional
    public PollenProcessingSummary fetchAndStoreDataForAllCities() {
        if (!shouldProcessToday()) {
            log.info("Pollen data for today has already been processed. Skipping.");
            return new PollenProcessingSummary(0, 0, 0, "Already processed");
        }
        
        List<City> cities = cityRepository.findAll();
        
        int totalPollenRecords = 0;
        int totalPlantRecords = 0;
        int citiesProcessed = 0;
        
        log.info("Starting pollen data processing for {} cities", cities.size());
        
        for (City city : cities) {
            try {
                // Fetch pollen data from Google API
                GooglePollenApiResponse response = googlePollenExternalService.fetchPollenData(
                        city.getLat(), city.getLon()
                );
                
                // Map response to entities
                List<PollenData> pollenDataList = pollenDataMapper.mapToPollenDataList(
                        response, city.getLat(), city.getLon()
                );
                
                // Save to database (cascade will save plant data too)
                List<PollenData> savedPollenData = pollenDataRepository.saveAll(pollenDataList);
                
                int pollenCount = savedPollenData.size();
                int plantCount = savedPollenData.stream()
                        .mapToInt(pd -> pd.getPlants() != null ? pd.getPlants().size() : 0)
                        .sum();
                
                totalPollenRecords += pollenCount;
                totalPlantRecords += plantCount;
                citiesProcessed++;
                
                log.info("Processed city {}: Pollen records: {}, Plant records: {}",
                        city.getIlAdi(), pollenCount, plantCount);
                
            } catch (Exception e) {
                log.error("Error processing city {}: {}", city.getIlAdi(), e.getMessage(), e);
            }
        }
        
        // Mark today as processed after all cities are done
        markTodayAsProcessed();
        
        log.info("Pollen data processing completed. Cities: {}, Pollen records: {}, Plant records: {}",
                citiesProcessed, totalPollenRecords, totalPlantRecords);
        
        return new PollenProcessingSummary(citiesProcessed, totalPollenRecords, totalPlantRecords, "Success");
    }
    
    /**
     * Summary of pollen data processing operation
     */
    public record PollenProcessingSummary(
            int citiesProcessed,
            int pollenRecordsStored,
            int plantRecordsStored,
            String status
    ) {}
}

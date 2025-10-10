package com.allermind.weather.application.service.scheduled;

import java.time.LocalDate;
import java.util.List;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.allermind.weather.application.dto.external.AirQualityApiResponse;
import com.allermind.weather.application.dto.external.WeatherApiResponse;
import com.allermind.weather.application.service.external.AirQualityExternalService;
import com.allermind.weather.application.service.external.WeatherExternalService;
import com.allermind.weather.application.service.mapper.DataMapper;
import com.allermind.weather.domain.entity.AirQualityRecord;
import com.allermind.weather.domain.entity.City;
import com.allermind.weather.domain.entity.ProcessingStatus;
import com.allermind.weather.domain.entity.WeatherRecord;
import com.allermind.weather.infrastructure.repository.AirQualityRecordRepository;
import com.allermind.weather.infrastructure.repository.CityRepository;
import com.allermind.weather.infrastructure.repository.ProcessingStatusRepository;
import com.allermind.weather.infrastructure.repository.WeatherRecordRepository;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

/**
 * Service for processing weather and air quality data for all cities
 * This service is called by the scheduled job daily at midnight
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class DataProcessingService {
    
    private final CityRepository cityRepository;
    private final WeatherRecordRepository weatherRecordRepository;
    private final AirQualityRecordRepository airQualityRecordRepository;
    private final ProcessingStatusRepository processingStatusRepository;
    
    private final WeatherExternalService weatherExternalService;
    private final AirQualityExternalService airQualityExternalService;
    private final DataMapper dataMapper;
    
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
     * Fetch and store weather and air quality data for all cities
     * Returns a summary of processed records
     */
    @Transactional
    public DataProcessingSummary fetchAndStoreDataForAllCities() {
        if (!shouldProcessToday()) {
            log.info("Data for today has already been processed. Skipping.");
            return new DataProcessingSummary(0, 0, 0, "Already processed");
        }
        
        List<City> cities = cityRepository.findAll();
        LocalDate today = LocalDate.now();
        
        int totalWeatherRecords = 0;
        int totalAirQualityRecords = 0;
        int citiesProcessed = 0;
        
        log.info("Starting data processing for {} cities on {}", cities.size(), today);
        
        for (City city : cities) {
            try {
                // Fetch and store weather data
                WeatherApiResponse weatherResponse = weatherExternalService.fetchWeatherData(
                        city.getLat(), city.getLon(), today
                );
                List<WeatherRecord> weatherRecords = dataMapper.mapWeatherApiResponseToRecords(weatherResponse, city);
                weatherRecordRepository.saveAll(weatherRecords);
                totalWeatherRecords += weatherRecords.size();
                
                // Fetch and store air quality data
                AirQualityApiResponse airQualityResponse = airQualityExternalService.fetchAirQualityData(
                        city.getLat(), city.getLon(), today
                );
                List<AirQualityRecord> airQualityRecords = dataMapper.mapAirQualityApiResponseToRecords(airQualityResponse, city);
                airQualityRecordRepository.saveAll(airQualityRecords);
                totalAirQualityRecords += airQualityRecords.size();
                
                citiesProcessed++;
                
                log.info("Processed city {}: Weather records: {}, Air quality records: {}",
                        city.getIlAdi(), weatherRecords.size(), airQualityRecords.size());
                
            } catch (Exception e) {
                log.error("Error processing city {}: {}", city.getIlAdi(), e.getMessage(), e);
            }
        }
        
        // Mark today as processed after all cities are done
        markTodayAsProcessed();
        
        log.info("Data processing completed. Cities: {}, Weather records: {}, Air quality records: {}",
                citiesProcessed, totalWeatherRecords, totalAirQualityRecords);
        
        return new DataProcessingSummary(citiesProcessed, totalWeatherRecords, totalAirQualityRecords, "Success");
    }
    
    /**
     * Summary of data processing operation
     */
    public record DataProcessingSummary(
            int citiesProcessed,
            int weatherRecordsStored,
            int airQualityRecordsStored,
            String status
    ) {}
}

package com.allermind.weather.application.service;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.allermind.weather.application.dto.WeatherAirQualityResponse;
import com.allermind.weather.domain.entity.AirQualityRecord;
import com.allermind.weather.domain.entity.City;
import com.allermind.weather.domain.entity.WeatherRecord;
import com.allermind.weather.infrastructure.repository.AirQualityRecordRepository;
import com.allermind.weather.infrastructure.repository.CityRepository;
import com.allermind.weather.infrastructure.repository.WeatherRecordRepository;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Slf4j
@Transactional(readOnly = true)
public class WeatherAirQualityService {
    
    private final CityRepository cityRepository;
    private final WeatherRecordRepository weatherRecordRepository;
    private final AirQualityRecordRepository airQualityRecordRepository;
    
    public WeatherAirQualityResponse getWeatherAndAirQualityByCoordinates(String lat, String lon) {
        log.info("Fetching weather and air quality data for coordinates: lat={}, lon={}", lat, lon);
        
        // Önce tam eşleşme ara
        City city = cityRepository.findByLatAndLon(lat, lon).orElse(null);
        
        // Tam eşleşme bulunamazsa en yakın şehri bul
        if (city == null) {
            try {
                double latDouble = Double.parseDouble(lat);
                double lonDouble = Double.parseDouble(lon);
                city = cityRepository.findNearestCity(latDouble, lonDouble).orElse(null);
                log.info("Exact match not found, using nearest city: {}", 
                        city != null ? city.getIlAdi() : "Not found");
            } catch (NumberFormatException e) {
                log.warn("Invalid coordinates provided: lat={}, lon={}", lat, lon);
            }
        } else {
            log.info("Exact match found for city: {}", city.getIlAdi());
        }
        
        String cityName = city != null ? city.getIlAdi() : "Unknown Location";
        
        WeatherRecord weatherRecord = weatherRecordRepository
                .findLatestByLatAndLon(city.getLat(), city.getLon());
        
        AirQualityRecord airQualityRecord = airQualityRecordRepository
                .findLatestByLatAndLon(city.getLat(), city.getLon());
        
        return new WeatherAirQualityResponse(cityName, city.getLat(), city.getLon(), weatherRecord, airQualityRecord);
    }
}

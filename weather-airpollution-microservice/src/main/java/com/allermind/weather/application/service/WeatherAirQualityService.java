package com.allermind.weather.application.service;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.allermind.weather.application.dto.WeatherAirQualityResponse;
import com.allermind.weather.domain.entity.AirQualityRecord;
import com.allermind.weather.domain.entity.City;
import com.allermind.weather.domain.entity.WeatherRecord;
import com.allermind.weather.domain.exception.CityNotFoundException;
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
    
    public WeatherAirQualityResponse getWeatherAndAirQualityByCityName(String cityName) {
        log.info("Fetching weather and air quality data for city: {}", cityName);
        
        City city = cityRepository.findByIlAdiIgnoreCase(cityName)
                .orElseThrow(() -> new CityNotFoundException(cityName));
        
                final var x = weatherRecordRepository.findAll();
        WeatherRecord weatherRecord = weatherRecordRepository
                .findLatestByLatAndLon(37.812500, 27.937500);
        
        AirQualityRecord airQualityRecord = airQualityRecordRepository
                .findLatestByLatAndLon(city.getLat(), city.getLon());
        
        return new WeatherAirQualityResponse(city.getIlAdi(), weatherRecord, airQualityRecord);
    }
}

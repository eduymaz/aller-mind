package com.allermind.weather.application.service.mapper;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.springframework.stereotype.Component;

import com.allermind.weather.application.dto.external.AirQualityApiResponse;
import com.allermind.weather.application.dto.external.WeatherApiResponse;
import com.allermind.weather.domain.entity.AirQualityRecord;
import com.allermind.weather.domain.entity.City;
import com.allermind.weather.domain.entity.WeatherRecord;

import lombok.extern.slf4j.Slf4j;

/**
 * Mapper service for converting API responses to domain entities
 */
@Component
@Slf4j
public class DataMapper {
    
    private static final DateTimeFormatter DATE_TIME_FORMATTER = DateTimeFormatter.ISO_DATE_TIME;
    
    /**
     * Convert WeatherApiResponse to list of WeatherRecord entities
     */
    public List<WeatherRecord> mapWeatherApiResponseToRecords(WeatherApiResponse response, City city) {
        List<WeatherRecord> records = new ArrayList<>();
        
        if (response == null || response.getHourly() == null) {
            log.warn("Weather API response or hourly data is null");
            return records;
        }
        
        Map<String, List<Object>> hourly = response.getHourly();
        List<Object> timeValues = hourly.get("time");
        
        if (timeValues == null || timeValues.isEmpty()) {
            log.warn("No time values found in weather API response");
            return records;
        }
        
        int size = timeValues.size();
        
        for (int i = 0; i < size; i++) {
            try {
                WeatherRecord record = new WeatherRecord();
                record.setLat(city.getLat());
                record.setLon(city.getLon());
                record.setTime(LocalDateTime.parse(timeValues.get(i).toString(), DATE_TIME_FORMATTER));
                record.setTemperature2m(getDoubleValue(hourly.get("temperature_2m"), i));
                record.setRelativeHumidity2m(getIntegerValue(hourly.get("relative_humidity_2m"), i));
                record.setPrecipitation(getDoubleValue(hourly.get("precipitation"), i));
                record.setSnowfall(getDoubleValue(hourly.get("snowfall"), i));
                record.setRain(getDoubleValue(hourly.get("rain"), i));
                record.setCloudCover(getIntegerValue(hourly.get("cloud_cover"), i));
                record.setSurfacePressure(getDoubleValue(hourly.get("surface_pressure"), i));
                record.setWindSpeed10m(getDoubleValue(hourly.get("wind_speed_10m"), i));
                record.setWindDirection10m(getIntegerValue(hourly.get("wind_direction_10m"), i));
                record.setSoilTemperature0To7cm(getDoubleValue(hourly.get("soil_temperature_0_to_7cm"), i));
                record.setSoilMoisture0To7cm(getDoubleValue(hourly.get("soil_moisture_0_to_7cm"), i));
                record.setSunshineDuration(getDoubleValue(hourly.get("sunshine_duration"), i));
                
                records.add(record);
            } catch (Exception e) {
                log.error("Error mapping weather record at index {}: {}", i, e.getMessage());
            }
        }
        
        log.info("Mapped {} weather records", records.size());
        return records;
    }
    
    /**
     * Convert AirQualityApiResponse to list of AirQualityRecord entities
     */
    public List<AirQualityRecord> mapAirQualityApiResponseToRecords(AirQualityApiResponse response, City city) {
        List<AirQualityRecord> records = new ArrayList<>();
        
        if (response == null || response.getHourly() == null) {
            log.warn("Air quality API response or hourly data is null");
            return records;
        }
        
        Map<String, List<Object>> hourly = response.getHourly();
        List<Object> timeValues = hourly.get("time");
        
        if (timeValues == null || timeValues.isEmpty()) {
            log.warn("No time values found in air quality API response");
            return records;
        }
        
        int size = timeValues.size();
        
        for (int i = 0; i < size; i++) {
            try {
                AirQualityRecord record = new AirQualityRecord();
                record.setLat(city.getLat());
                record.setLon(city.getLon());
                record.setTime(LocalDateTime.parse(timeValues.get(i).toString(), DATE_TIME_FORMATTER));
                record.setPm10(getDoubleValue(hourly.get("pm10"), i));
                record.setPm25(getDoubleValue(hourly.get("pm2_5"), i));
                record.setCarbonDioxide(getIntegerValue(hourly.get("carbon_dioxide"), i));
                record.setCarbonMonoxide(getDoubleValue(hourly.get("carbon_monoxide"), i));
                record.setNitrogenDioxide(getDoubleValue(hourly.get("nitrogen_dioxide"), i));
                record.setSulphurDioxide(getDoubleValue(hourly.get("sulphur_dioxide"), i));
                record.setOzone(getDoubleValue(hourly.get("ozone"), i));
                record.setAerosolOpticalDepth(getDoubleValue(hourly.get("aerosol_optical_depth"), i));
                record.setMethane(getDoubleValue(hourly.get("methane"), i));
                record.setUvIndex(getDoubleValue(hourly.get("uv_index"), i));
                record.setUvIndexClearSky(getDoubleValue(hourly.get("uv_index_clear_sky"), i));
                record.setDust(getIntegerValue(hourly.get("dust"), i));
                
                records.add(record);
            } catch (Exception e) {
                log.error("Error mapping air quality record at index {}: {}", i, e.getMessage());
            }
        }
        
        log.info("Mapped {} air quality records", records.size());
        return records;
    }
    
    private Double getDoubleValue(List<Object> values, int index) {
        if (values == null || index >= values.size()) {
            return 0.0;
        }
        Object value = values.get(index);
        if (value == null) {
            return 0.0;
        }
        if (value instanceof Number) {
            return ((Number) value).doubleValue();
        }
        try {
            return Double.parseDouble(value.toString());
        } catch (NumberFormatException e) {
            log.warn("Failed to parse double value: {}", value);
            return 0.0;
        }
    }
    
    private Integer getIntegerValue(List<Object> values, int index) {
        if (values == null || index >= values.size()) {
            return 0;
        }
        Object value = values.get(index);
        if (value == null) {
            return 0;
        }
        if (value instanceof Number) {
            return ((Number) value).intValue();
        }
        try {
            return Integer.parseInt(value.toString());
        } catch (NumberFormatException e) {
            log.warn("Failed to parse integer value: {}", value);
            return 0;
        }
    }
}

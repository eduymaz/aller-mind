package com.allermind.model.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ModelPredictionRequest {
    @JsonProperty("userClassification")
    private AllergyClassificationResponse userClassification;
    
    @JsonProperty("environmentalData")
    private EnvironmentalData environmentalData;
    
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class EnvironmentalData {
        @JsonProperty("airQuality")
        private AirQualityData airQuality;
        
        @JsonProperty("pollen")
        private PollenData pollen;
        
        @JsonProperty("weather")
        private WeatherData weather;
    }
    
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class AirQualityData {
        private Double pm25;
        private Double pm10;
        private Double o3;
        private Double no2;
        private Double so2;
        private Double co;
    }
    
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class PollenData {
        private Double totalUpi;
        private Double treePollen;
        private Double grassPollen;
        private Double weedPollen;
        private Integer inSeasonCount;
        private Double diversityIndex;
    }
    
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class WeatherData {
        private Double temperature;
        private Double humidity;
        private Double windSpeed;
        private Double pressure;
    }
}

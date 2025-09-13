package com.allermind.model.service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import org.springframework.stereotype.Service;

import com.allermind.model.client.MachineLearningModelClient;
import com.allermind.model.client.PollenServiceClient;
import com.allermind.model.client.WeatherAirQualityServiceClient;
import com.allermind.model.dto.AirQualityRecord;
import com.allermind.model.dto.AllerMindResponse;
import com.allermind.model.dto.ModelPredictionRequest;
import com.allermind.model.dto.ModelPredictionResponse;
import com.allermind.model.dto.PollenResponse;
import com.allermind.model.dto.UserGroup;
import com.allermind.model.dto.UserSettings;
import com.allermind.model.dto.WeatherAirQualityResponse;
import com.allermind.model.dto.WeatherRecord;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Slf4j
public class AllerMindModelService {

    private final PollenServiceClient pollenServiceClient;
    private final WeatherAirQualityServiceClient weatherAirQualityServiceClient;
    private final MachineLearningModelClient mlModelClient;
    private final UserGroupingService userGroupingService;

    public AllerMindResponse processAllerMindRequest(String lat, String lon, UserSettings userSettings) {
        log.info("Processing AllerMind request for coordinates: {}, {}", lat, lon);

        try {
            // 1. User settings'i grup bilgisine dönüştür
            UserGroup userGroup = userGroupingService.determineUserGroup(userSettings);
            log.info("User group determined: {}", userGroup);

            // 2. Pollen verisi al
            List<PollenResponse> pollenData = pollenServiceClient.getPollenData(lat, lon);
            log.info("Pollen data retrieved: {} records", pollenData != null ? pollenData.size() : 0);

            // 3. Weather ve Air Quality verisi al
            WeatherAirQualityResponse weatherAirQualityData = 
                weatherAirQualityServiceClient.getWeatherAirQualityData(lat, lon);
            log.info("Weather air quality data retrieved for city: {}", 
                weatherAirQualityData != null ? weatherAirQualityData.getCityName() : "Unknown");

            // 4. ML modeli için request hazırla
            ModelPredictionRequest mlRequest = prepareMLRequest(userGroup, pollenData, weatherAirQualityData);

            // 5. ML modelinden prediction al
            ModelPredictionResponse mlResponse = mlModelClient.getPrediction(mlRequest);

            // 6. Final response hazırla
            return buildAllerMindResponse(lat, lon, userSettings.getUserId(), userGroup, mlResponse);

        } catch (Exception e) {
            log.error("Error processing AllerMind request: {}", e.getMessage(), e);
            throw new RuntimeException("Failed to process AllerMind request", e);
        }
    }

    private ModelPredictionRequest prepareMLRequest(UserGroup userGroup, 
                                                   List<PollenResponse> pollenData, 
                                                   WeatherAirQualityResponse weatherAirQualityData) {
        
        Map<String, Object> additionalFeatures = new HashMap<>();
        
        // Pollen verilerinden özellikler çıkar
        if (pollenData != null && !pollenData.isEmpty()) {
            double avgUpiValue = pollenData.stream()
                .filter(p -> p.getUpiValue() != null)
                .mapToDouble(PollenResponse::getUpiValue)
                .average()
                .orElse(0.0);
            additionalFeatures.put("avgPollenUpi", avgUpiValue);
            
            long inSeasonCount = pollenData.stream()
                .filter(p -> Boolean.TRUE.equals(p.getInSeason()))
                .count();
            additionalFeatures.put("inSeasonPollenCount", inSeasonCount);
        }

        // Hava durumu verilerinden özellikler çıkar
        if (weatherAirQualityData != null && weatherAirQualityData.getWeatherRecord() != null) {
            WeatherRecord weather = weatherAirQualityData.getWeatherRecord();
            additionalFeatures.put("temperature", weather.getTemperature2m());
            additionalFeatures.put("humidity", weather.getRelativeHumidity2m());
            additionalFeatures.put("windSpeed", weather.getWindSpeed10m());
        }

        // Hava kalitesi verilerinden özellikler çıkar
        if (weatherAirQualityData != null && weatherAirQualityData.getAirQualityRecord() != null) {
            AirQualityRecord airQuality = weatherAirQualityData.getAirQualityRecord();
            additionalFeatures.put("pm25", airQuality.getPm25());
            additionalFeatures.put("pm10", airQuality.getPm10());
            additionalFeatures.put("ozone", airQuality.getOzone());
            additionalFeatures.put("uvIndex", airQuality.getUvIndex());
        }

        return ModelPredictionRequest.builder()
                .userGroup(userGroup)
                .pollenData(pollenData)
                .weatherAirQualityData(weatherAirQualityData)
                .additionalFeatures(additionalFeatures)
                .build();
    }

    private AllerMindResponse buildAllerMindResponse(String lat, String lon, String userId,
                                                    UserGroup userGroup, ModelPredictionResponse mlResponse) {
        
        // En yüksek risk skoruna sahip grubu bul
        String overallRiskLevel = "LOW";
        String overallRiskEmoji = "🟢";
        Integer overallRiskCode = 1;
        Double overallRiskScore = 0.0;
        
        if (mlResponse.getPredictions() != null && !mlResponse.getPredictions().isEmpty()) {
            ModelPredictionResponse.GroupResult highestRiskGroup = mlResponse.getPredictions().stream()
                .max((g1, g2) -> Double.compare(g1.getPredictionValue(), g2.getPredictionValue()))
                .orElse(null);
                
            if (highestRiskGroup != null) {
                overallRiskLevel = highestRiskGroup.getRiskLevel();
                overallRiskEmoji = highestRiskGroup.getRiskEmoji();
                overallRiskCode = highestRiskGroup.getRiskCode();
                overallRiskScore = highestRiskGroup.getPredictionValue();
            }
        }
        
        return AllerMindResponse.builder()
                .predictionId(UUID.randomUUID().toString())
                .userId(userId)
                .lat(lat)
                .lon(lon)
                .success(Boolean.TRUE.equals(mlResponse.getSuccess()))
                .message(mlResponse.getMessage())
                .overallRiskScore(overallRiskScore)
                .overallRiskLevel(overallRiskLevel)
                .overallRiskEmoji(overallRiskEmoji)
                .overallRiskCode(overallRiskCode)
                .modelPrediction(mlResponse)
                .userGroup(userGroup)
                .build();
    }
}

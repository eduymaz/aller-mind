package com.allermind.model.service;

import java.util.List;
import java.util.UUID;

import org.springframework.stereotype.Service;

import com.allermind.model.client.MachineLearningModelClient;
import com.allermind.model.client.PollenServiceClient;
import com.allermind.model.client.UserPreferenceServiceClient;
import com.allermind.model.client.WeatherAirQualityServiceClient;
import com.allermind.model.dto.AirQualityRecord;
import com.allermind.model.dto.AllerMindResponse;
import com.allermind.model.dto.AllergyClassificationResponse;
import com.allermind.model.dto.ModelPredictionRequest;
import com.allermind.model.dto.ModelPredictionResponse;
import com.allermind.model.dto.PollenResponse;
import com.allermind.model.dto.UserGroup;
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
    private final UserPreferenceServiceClient userPreferenceServiceClient;

    public AllerMindResponse processAllerMindRequest(String lat, String lon, UUID userId) {
        log.info("Processing AllerMind request for coordinates: {}, {} and user: {}", lat, lon, userId);

        try {
            // 1. User preferences'i user preference service'den al
            AllergyClassificationResponse userPreferenceResponse = userPreferenceServiceClient.getUserPreference(userId);
            log.info("User preference retrieved for user: {} with group: {}", userId, userPreferenceResponse.getGroupName());
            
            // 2. User preference response'u UserGroup'a dönüştür
            UserGroup userGroup = convertToUserGroup(userPreferenceResponse);
            log.info("User group converted: {}", userGroup);

            // 3. Pollen verisi al
            List<PollenResponse> pollenData = pollenServiceClient.getPollenData(lat, lon);
            log.info("Pollen data retrieved: {} records", pollenData != null ? pollenData.size() : 0);

            // 4. Weather ve Air Quality verisi al
            WeatherAirQualityResponse weatherAirQualityData = 
                weatherAirQualityServiceClient.getWeatherAirQualityData(lat, lon);
            log.info("Weather air quality data retrieved for city: {}", 
                weatherAirQualityData != null ? weatherAirQualityData.getCityName() : "Unknown");

            // 5. ML modeli için request hazırla
            ModelPredictionRequest mlRequest = prepareMLRequest(userPreferenceResponse, pollenData, weatherAirQualityData);

            // 6. ML modelinden prediction al
            ModelPredictionResponse mlResponse = mlModelClient.getPrediction(mlRequest);

            // 7. Final response hazırla
            return buildAllerMindResponse(lat, lon, userId.toString(), userGroup, mlResponse);

        } catch (Exception e) {
            log.error("Error processing AllerMind request: {}", e.getMessage(), e);
            throw new RuntimeException("Failed to process AllerMind request", e);
        }
    }
    
    private UserGroup convertToUserGroup(AllergyClassificationResponse response) {
        // AllergyClassificationResponse'dan UserGroup'a dönüştürme
        String riskLevel = determineRiskLevel(response.getGroupId());
        
        return UserGroup.builder()
                .groupId(response.getGroupId().toString())
                .riskLevel(riskLevel)
                .riskScore(response.getModelWeight() != null ? response.getModelWeight().doubleValue() : 0.0)
                .groupDescription(response.getGroupDescription())
                .build();
    }
    
    private String determineRiskLevel(Integer groupId) {
        // Grup ID'ye göre risk seviyesi belirleme
        return switch (groupId) {
            case 1 -> "CRITICAL";  // Şiddetli Alerjik Grup
            case 2 -> "HIGH";      // Hafif-Orta Alerjik Grup
            case 3 -> "MEDIUM";    // Genetik Yatkınlık Grubu
            case 4 -> "MEDIUM";    // Teşhis Almamış Grup
            case 5 -> "HIGH";      // Hassas Çocuk/Yaşlı Grubu
            default -> "LOW";
        };
    }

    private ModelPredictionRequest prepareMLRequest(AllergyClassificationResponse userClassificationResponse, 
                                                   List<PollenResponse> pollenData, 
                                                   WeatherAirQualityResponse weatherAirQualityData) {
        
        // Environmental data hazırla
        ModelPredictionRequest.EnvironmentalData environmentalData = ModelPredictionRequest.EnvironmentalData.builder()
                .airQuality(buildAirQualityData(weatherAirQualityData))
                .pollen(buildPollenData(pollenData))
                .weather(buildWeatherData(weatherAirQualityData))
                .build();

        return ModelPredictionRequest.builder()
                .userClassification(userClassificationResponse)
                .environmentalData(environmentalData)
                .build();
    }
    
    private ModelPredictionRequest.AirQualityData buildAirQualityData(WeatherAirQualityResponse weatherAirQualityData) {
        if (weatherAirQualityData == null || weatherAirQualityData.getAirQualityRecord() == null) {
            return ModelPredictionRequest.AirQualityData.builder()
                    .pm25(0.0)
                    .pm10(0.0)  
                    .o3(0.0)
                    .no2(0.0)
                    .so2(0.0)
                    .co(0.0)
                    .build();
        }
        
        AirQualityRecord airQuality = weatherAirQualityData.getAirQualityRecord();
        return ModelPredictionRequest.AirQualityData.builder()
                .pm25(airQuality.getPm25() != null ? airQuality.getPm25().doubleValue() : 0.0)
                .pm10(airQuality.getPm10() != null ? airQuality.getPm10().doubleValue() : 0.0)
                .o3(airQuality.getOzone() != null ? airQuality.getOzone().doubleValue() : 0.0)
                .no2(airQuality.getNitrogenDioxide() != null ? airQuality.getNitrogenDioxide().doubleValue() : 0.0)
                .so2(airQuality.getSulphurDioxide() != null ? airQuality.getSulphurDioxide().doubleValue() : 0.0)
                .co(airQuality.getCarbonMonoxide() != null ? airQuality.getCarbonMonoxide().doubleValue() : 0.0)
                .co2(airQuality.getCarbonDioxide() != null ? airQuality.getCarbonDioxide() : 0)
                .dust(airQuality.getDust() != null ? airQuality.getDust() : 0)
                .methane(airQuality.getMethane() != null ? airQuality.getMethane() : 0)
                .uvIndex(airQuality.getUvIndex() != null ? airQuality.getUvIndex() : 0)
                .aerosolOpticalDepth(airQuality.getAerosolOpticalDepth() != null ? airQuality.getAerosolOpticalDepth() : 0)
                .build();
    }
    
    private ModelPredictionRequest.PollenData buildPollenData(List<PollenResponse> pollenData) {
        if (pollenData == null || pollenData.isEmpty()) {
            return ModelPredictionRequest.PollenData.builder()
                    .totalUpi(0.0)
                    .treePollen(0.0)
                    .grassPollen(0.0)
                    .weedPollen(0.0)
                    .inSeasonCount(0)
                    .diversityIndex(0.0)
                    .build();
        }
        
        double totalUpi = pollenData.stream()
                .filter(p -> p.getUpiValue() != null)
                .mapToDouble(p -> p.getUpiValue().doubleValue())
                .sum();
                
        long inSeasonCount = pollenData.stream()
                .filter(p -> Boolean.TRUE.equals(p.getInSeason()))
                .count();
                
        // Pollen kategorilerini pollen code'a göre belirle (basit kategorilendirme)
        double treePollen = pollenData.stream()
                .filter(p -> p.getUpiValue() != null && p.getPollenCode() != null && 
                            (p.getPollenCode().toLowerCase().contains("tree") || 
                             p.getPollenCode().toLowerCase().contains("birch") ||
                             p.getPollenCode().toLowerCase().contains("oak") ||
                             p.getPollenCode().toLowerCase().contains("pine")))
                .mapToDouble(p -> p.getUpiValue().doubleValue())
                .sum();
                
        double grassPollen = pollenData.stream()
                .filter(p -> p.getUpiValue() != null && p.getPollenCode() != null && 
                            (p.getPollenCode().toLowerCase().contains("grass") ||
                             p.getPollenCode().toLowerCase().contains("graminales")))
                .mapToDouble(p -> p.getUpiValue().doubleValue())
                .sum();
                
        double weedPollen = pollenData.stream()
                .filter(p -> p.getUpiValue() != null && p.getPollenCode() != null && 
                            (p.getPollenCode().toLowerCase().contains("weed") ||
                             p.getPollenCode().toLowerCase().contains("ragweed") ||
                             p.getPollenCode().toLowerCase().contains("mugwort")))
                .mapToDouble(p -> p.getUpiValue().doubleValue())
                .sum();
        
        double diversityIndex = !pollenData.isEmpty() ? (double) inSeasonCount / pollenData.size() : 0.0;
        
        return ModelPredictionRequest.PollenData.builder()
                .totalUpi(totalUpi)
                .treePollen(treePollen)
                .grassPollen(grassPollen)
                .weedPollen(weedPollen)
                .inSeasonCount((int) inSeasonCount)
                .diversityIndex(diversityIndex)
                .build();
    }
    
    private ModelPredictionRequest.WeatherData buildWeatherData(WeatherAirQualityResponse weatherAirQualityData) {
        if (weatherAirQualityData == null || weatherAirQualityData.getWeatherRecord() == null) {
            return ModelPredictionRequest.WeatherData.builder()
                    .temperature(0.0)
                    .humidity(0.0)
                    .windSpeed(0.0)
                    .pressure(0.0)
                    .precipitation(0.0)
                    .windDirection(0)
                    .sunshineDuration(0.0)
                    .cloudCover(0)
                    .build();
        }
        
        WeatherRecord weather = weatherAirQualityData.getWeatherRecord();
        return ModelPredictionRequest.WeatherData.builder()
                .temperature(weather.getTemperature2m() != null ? weather.getTemperature2m() : 0.0)
                .humidity(weather.getRelativeHumidity2m() != null ? weather.getRelativeHumidity2m().doubleValue() : 0.0)
                .windSpeed(weather.getWindSpeed10m() != null ? weather.getWindSpeed10m() : 0.0)
                .pressure(weather.getSurfacePressure() != null ? weather.getSurfacePressure() : 0.0)
                .precipitation(weather.getPrecipitation() != null ? weather.getPrecipitation() : 0.0)
                .windDirection(weather.getWindDirection10m() != null ? weather.getWindDirection10m().intValue() : 0)
                .sunshineDuration(weather.getSunshineDuration() != null ? weather.getSunshineDuration() : 0.0)
                .cloudCover(weather.getCloudCover() != null ? weather.getCloudCover() : 0)
                .build();
    }

    private AllerMindResponse buildAllerMindResponse(String lat, String lon, String userId,
                                                    UserGroup userGroup, ModelPredictionResponse mlResponse) {
        
        // Python API'den gelen yeni response formatını kullan
        String overallRiskLevel = mlResponse.getRiskLevel() != null ? mlResponse.getRiskLevel() : "LOW";
        String overallRiskEmoji = determineRiskEmoji(overallRiskLevel);
        Integer overallRiskCode = determineRiskCode(overallRiskLevel);
        Double overallRiskScore = mlResponse.getRiskScore() != null ? mlResponse.getRiskScore() : 0.0;
        
        // Backward compatibility için predictions oluştur
        if (mlResponse.getPredictions() == null && mlResponse.getRiskScore() != null) {
            ModelPredictionResponse.GroupResult groupResult = ModelPredictionResponse.GroupResult.builder()
                .groupId(Integer.valueOf(userGroup.getGroupId()))
                .groupName(userGroup.getGroupDescription())
                .predictionValue(mlResponse.getRiskScore())
                .riskLevel(overallRiskLevel)
                .riskEmoji(overallRiskEmoji)
                .riskCode(overallRiskCode)
                .build();
            mlResponse.setPredictions(List.of(groupResult));
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
    
    private String determineRiskEmoji(String riskLevel) {
        return switch (riskLevel.toUpperCase()) {
            case "CRITICAL" -> "🔴";
            case "HIGH" -> "🟠";
            case "MEDIUM" -> "🟡";
            case "LOW" -> "🟢";
            default -> "⚪";
        };
    }
    
    private Integer determineRiskCode(String riskLevel) {
        return switch (riskLevel.toUpperCase()) {
            case "CRITICAL" -> 4;
            case "HIGH" -> 3;
            case "MEDIUM" -> 2;
            case "LOW" -> 1;
            default -> 0;
        };
    }
}

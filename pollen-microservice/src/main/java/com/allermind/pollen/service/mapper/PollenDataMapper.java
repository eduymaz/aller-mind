package com.allermind.pollen.service.mapper;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Component;

import com.allermind.pollen.dto.external.GooglePollenApiResponse;
import com.allermind.pollen.model.PlantData;
import com.allermind.pollen.model.PollenData;

import lombok.extern.slf4j.Slf4j;

/**
 * Mapper service for converting Google Pollen API responses to domain entities
 */
@Component
@Slf4j
public class PollenDataMapper {
    
    /**
     * Extract date from API response
     */
    public LocalDate extractDate(GooglePollenApiResponse response) {
        if (response.getDailyInfo() != null && !response.getDailyInfo().isEmpty()) {
            GooglePollenApiResponse.DailyInfo.DateInfo dateInfo = 
                    response.getDailyInfo().get(0).getDate();
            
            if (dateInfo != null && dateInfo.getYear() != null && 
                dateInfo.getMonth() != null && dateInfo.getDay() != null) {
                try {
                    return LocalDate.of(dateInfo.getYear(), dateInfo.getMonth(), dateInfo.getDay());
                } catch (Exception e) {
                    log.warn("Invalid date from API: {}-{}-{}", 
                            dateInfo.getYear(), dateInfo.getMonth(), dateInfo.getDay());
                }
            }
        }
        return LocalDate.now();
    }
    
    /**
     * Map Google Pollen API response to PollenData entities with associated PlantData
     */
    public List<PollenData> mapToPollenDataList(GooglePollenApiResponse response, 
                                                  String latitude, String longitude) {
        List<PollenData> pollenDataList = new ArrayList<>();
        
        if (response == null || response.getDailyInfo() == null || response.getDailyInfo().isEmpty()) {
            log.warn("No daily info in pollen API response");
            return pollenDataList;
        }
        
        GooglePollenApiResponse.DailyInfo dailyInfo = response.getDailyInfo().get(0);
        LocalDate forecastDate = extractDate(response);
        
        if (dailyInfo.getPollenTypeInfo() == null) {
            log.warn("No pollen type info in API response");
            return pollenDataList;
        }
        
        // Process each pollen type
        for (GooglePollenApiResponse.DailyInfo.PollenTypeInfo pollenTypeInfo : dailyInfo.getPollenTypeInfo()) {
            if (pollenTypeInfo.getCode() == null || pollenTypeInfo.getCode().isEmpty()) {
                continue;
            }
            
            PollenData pollenData = new PollenData();
            pollenData.setLat(latitude);
            pollenData.setLon(longitude);
            pollenData.setDate(forecastDate);
            pollenData.setPollenCode(pollenTypeInfo.getCode());
            pollenData.setInSeason(pollenTypeInfo.getInSeason() != null ? pollenTypeInfo.getInSeason() : false);
            
            // Get UPI value
            Double upiValue = 0.0;
            if (pollenTypeInfo.getIndexInfo() != null && pollenTypeInfo.getIndexInfo().getValue() != null) {
                upiValue = pollenTypeInfo.getIndexInfo().getValue();
            }
            pollenData.setUpiValue(upiValue.floatValue());
            
            // Get health recommendations
            String healthRecommendations = null;
            if (pollenTypeInfo.getHealthRecommendations() != null && 
                !pollenTypeInfo.getHealthRecommendations().isEmpty()) {
                healthRecommendations = String.join("\n", pollenTypeInfo.getHealthRecommendations());
            }
            pollenData.setHealthRecommendations(healthRecommendations);
            
            // Map related plant info
            List<PlantData> plantDataList = mapPlantDataForPollenType(
                    dailyInfo, pollenTypeInfo.getCode(), pollenData);
            pollenData.setPlants(plantDataList);
            
            pollenDataList.add(pollenData);
        }
        
        log.info("Mapped {} pollen data entries", pollenDataList.size());
        return pollenDataList;
    }
    
    /**
     * Map plant data for a specific pollen type
     */
    private List<PlantData> mapPlantDataForPollenType(GooglePollenApiResponse.DailyInfo dailyInfo,
                                                       String pollenCode, PollenData pollenData) {
        List<PlantData> plantDataList = new ArrayList<>();
        
        if (dailyInfo.getPlantInfo() == null) {
            return plantDataList;
        }
        
        for (GooglePollenApiResponse.DailyInfo.PlantInfo plantInfo : dailyInfo.getPlantInfo()) {
            if (plantInfo.getCode() == null || plantInfo.getPlantDescription() == null) {
                continue;
            }
            
            // Match plant with pollen type
            String plantType = plantInfo.getPlantDescription().getType();
            if (plantType != null && plantType.equals(pollenCode)) {
                PlantData plantData = new PlantData();
                plantData.setPollenData(pollenData);
                plantData.setPlantCode(plantInfo.getCode());
                plantData.setPlantInSeason(plantInfo.getInSeason() != null ? plantInfo.getInSeason() : false);
                
                // Get UPI value
                Double plantUpiValue = 0.0;
                String upiDescription = null;
                if (plantInfo.getIndexInfo() != null) {
                    if (plantInfo.getIndexInfo().getValue() != null) {
                        plantUpiValue = plantInfo.getIndexInfo().getValue();
                    }
                    upiDescription = plantInfo.getIndexInfo().getIndexDescription();
                }
                plantData.setPlantUpiValue(plantUpiValue.floatValue());
                plantData.setUpiDescription(upiDescription);
                
                // Get picture URLs
                if (plantInfo.getPlantDescription() != null) {
                    plantData.setPictureUrl(plantInfo.getPlantDescription().getPicture());
                    plantData.setPictureCloseupUrl(plantInfo.getPlantDescription().getPictureCloseup());
                }
                
                plantDataList.add(plantData);
            }
        }
        
        return plantDataList;
    }
}

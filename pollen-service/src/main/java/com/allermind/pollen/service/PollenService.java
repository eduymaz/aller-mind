package com.allermind.pollen.service;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.allermind.pollen.dto.PlantDataDto;
import com.allermind.pollen.dto.PollenResponse;
import com.allermind.pollen.model.City;
import com.allermind.pollen.model.PlantData;
import com.allermind.pollen.model.PollenData;
import com.allermind.pollen.repository.CityRepository;
import com.allermind.pollen.repository.PlantDataRepository;
import com.allermind.pollen.repository.PollenDataRepository;

@Service
public class PollenService {

    @Autowired
    private CityRepository cityRepository;

    @Autowired
    private PollenDataRepository pollenDataRepository;

    @Autowired
    private PlantDataRepository plantDataRepository;

    public List<PollenResponse> getPollenDataByCityName(String cityName) {
        List<City> cities;

        // If cityName is provided, filter by city name, otherwise get all cities
        if (cityName != null && !cityName.isEmpty()) {
            cities = cityRepository.findByIlAdiIgnoreCase(cityName);
        } else {
            cities = cityRepository.findAll();
        }

        List<PollenResponse> responses = new ArrayList<>();
        
        // Process each city
        for (City city : cities) {
            // Get the latest pollen data for this city
            List<PollenData> pollenDataList = pollenDataRepository.findByLatAndLon(
                    city.getLat(), city.getLon());
            
            // Process each pollen data entry
            for (PollenData pollenData : pollenDataList) {
                List<PlantData> plantDataList = plantDataRepository.findByPollenData(pollenData);
                
                // Map plant data to DTOs
                List<PlantDataDto> plantDataDtos = plantDataList.stream()
                        .map(this::mapToPlantDataDto)
                        .collect(Collectors.toList());
                
                // Create response object
                PollenResponse response = PollenResponse.builder()
                        .cityName(city.getIlAdi())
                        .lat(pollenData.getLat())
                        .lon(pollenData.getLon())
                        .date(pollenData.getDate())
                        .pollenCode(pollenData.getPollenCode())
                        .inSeason(pollenData.getInSeason())
                        .upiValue(pollenData.getUpiValue())
                        .healthRecommendations(pollenData.getHealthRecommendations())
                        .plants(plantDataDtos)
                        .build();
                
                responses.add(response);
            }
        }
        
        return responses;
    }
    
    private PlantDataDto mapToPlantDataDto(PlantData plantData) {
        return PlantDataDto.builder()
                .plantCode(plantData.getPlantCode())
                .inSeason(plantData.getPlantInSeason())
                .upiValue(plantData.getPlantUpiValue())
                .upiDescription(plantData.getUpiDescription())
                .pictureUrl(plantData.getPictureUrl())
                .pictureCloseupUrl(plantData.getPictureCloseupUrl())
                .build();
    }
}

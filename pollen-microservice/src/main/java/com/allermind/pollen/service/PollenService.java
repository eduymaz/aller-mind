package com.allermind.pollen.service;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
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

    public List<PollenResponse> getPollenDataByLatLon(String lat, String lon) {
        // First try to find exact coordinates
        Optional<City> exactCity = cityRepository.findByLatAndLon(lat, lon);
        
        City targetCity;
        if (exactCity.isPresent()) {
            targetCity = exactCity.get();
        } else {
            // If exact coordinates not found, find nearest city
            Optional<City> nearestCity = cityRepository.findNearestCity(lat, lon);
            if (nearestCity.isPresent()) {
                targetCity = nearestCity.get();
            } else {
                return new ArrayList<>(); // No cities found
            }
        }
        
        return getPollenDataForCity(targetCity);
    }
    
    private List<PollenResponse> getPollenDataForCity(City city) {
        List<PollenResponse> responses = new ArrayList<>();
        
        // Get today's date
        LocalDate today = LocalDate.now();
        
        // Get pollen data for this city for today's date
        List<PollenData> pollenDataList = pollenDataRepository.findByLatAndLonAndDate(
                city.getLat(), city.getLon(), today);
        
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

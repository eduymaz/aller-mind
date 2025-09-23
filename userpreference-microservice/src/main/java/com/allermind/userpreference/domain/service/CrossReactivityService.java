package com.allermind.userpreference.domain.service;

import com.allermind.userpreference.domain.model.aggregate.UserPreference;
import com.allermind.userpreference.domain.model.enums.FoodType;
import com.allermind.userpreference.domain.model.enums.PollenType;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.*;

@Service
public class CrossReactivityService {
    
    private final Map<PollenType, List<FoodType>> crossReactivityMatrix;
    
    public CrossReactivityService() {
        this.crossReactivityMatrix = initializeCrossReactivityMatrix();
    }
    
    public BigDecimal calculateCrossReactivityRisk(UserPreference userPreference) {
        BigDecimal crossRisk = BigDecimal.ZERO;
        
        // Check pollen-food cross reactions
        for (Map.Entry<PollenType, List<FoodType>> entry : crossReactivityMatrix.entrySet()) {
            PollenType pollenType = entry.getKey();
            List<FoodType> relatedFoods = entry.getValue();
            
            // Check if user has pollen sensitivity
            boolean pollenSensitive = userPreference.hasPollenAllergy(pollenType);
            
            if (pollenSensitive) {
                // Check related food allergies
                for (FoodType food : relatedFoods) {
                    if (userPreference.hasFoodAllergy(food)) {
                        crossRisk = crossRisk.add(new BigDecimal("0.2")); // Cross-reaction risk bonus
                    }
                }
            }
        }
        
        return crossRisk.min(new BigDecimal("0.5")); // Maximum 50% bonus risk
    }
    
    public List<FoodType> getCrossReactiveFoods(PollenType pollenType) {
        return crossReactivityMatrix.getOrDefault(pollenType, Collections.emptyList());
    }
    
    public boolean hasCrossReactivity(PollenType pollenType, FoodType foodType) {
        List<FoodType> crossReactiveFoods = crossReactivityMatrix.get(pollenType);
        return crossReactiveFoods != null && crossReactiveFoods.contains(foodType);
    }
    
    private Map<PollenType, List<FoodType>> initializeCrossReactivityMatrix() {
        Map<PollenType, List<FoodType>> matrix = new EnumMap<>(PollenType.class);
        
        // Birch cross-reactive foods
        matrix.put(PollenType.BIRCH, Arrays.asList(
                FoodType.APPLE, FoodType.CHERRY, FoodType.PEAR, FoodType.ALMOND
        ));
        
        // Ragweed cross-reactive foods
        matrix.put(PollenType.RAGWEED, Arrays.asList(
                FoodType.MELON, FoodType.BANANA, FoodType.CUCUMBER
        ));
        
        // Mugwort cross-reactive foods
        matrix.put(PollenType.MUGWORT, Arrays.asList(
                FoodType.CELERY, FoodType.SPICES, FoodType.HERBS
        ));
        
        return Collections.unmodifiableMap(matrix);
    }
}
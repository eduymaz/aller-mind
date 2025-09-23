package com.allermind.userpreference.domain.service;

import com.allermind.userpreference.domain.model.aggregate.UserPreference;
import com.allermind.userpreference.domain.model.enums.PollenType;
import com.allermind.userpreference.domain.model.valueobject.RiskScore;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.EnumMap;
import java.util.Map;

@Service
public class RiskCalculationService {
    
    private final Map<PollenType, BigDecimal> pollenRiskWeights;
    private final CrossReactivityService crossReactivityService;
    
    public RiskCalculationService(CrossReactivityService crossReactivityService) {
        this.crossReactivityService = crossReactivityService;
        this.pollenRiskWeights = initializePollenRiskWeights();
    }
    
    public RiskScore calculatePollenRiskScore(UserPreference userPreference) {
        BigDecimal riskScore = BigDecimal.ZERO;
        
        // Tree pollen sensitivity (weight: 0.3)
        riskScore = riskScore.add(calculateCategoryRisk(userPreference.getTreePollenAllergies(), 
                PollenType.PollenCategory.TREE, new BigDecimal("0.3")));
        
        // Grass pollen sensitivity (weight: 0.4)
        riskScore = riskScore.add(calculateCategoryRisk(userPreference.getGrassPollenAllergies(), 
                PollenType.PollenCategory.GRASS, new BigDecimal("0.4")));
        
        // Weed pollen sensitivity (weight: 0.4)
        riskScore = riskScore.add(calculateCategoryRisk(userPreference.getWeedPollenAllergies(), 
                PollenType.PollenCategory.WEED, new BigDecimal("0.4")));
        
        // Cross-reactivity bonus
        BigDecimal crossReactionBonus = crossReactivityService.calculateCrossReactivityRisk(userPreference);
        riskScore = riskScore.add(crossReactionBonus);
        
        // Normalize to 0-1 range
        BigDecimal normalizedScore = riskScore.min(BigDecimal.ONE);
        
        return new RiskScore(normalizedScore);
    }
    
    private BigDecimal calculateCategoryRisk(Map<PollenType, Boolean> sensitivities, 
                                           PollenType.PollenCategory category, 
                                           BigDecimal categoryWeight) {
        if (sensitivities == null || sensitivities.isEmpty()) {
            return BigDecimal.ZERO;
        }
        
        BigDecimal categoryRisk = BigDecimal.ZERO;
        
        for (Map.Entry<PollenType, Boolean> entry : sensitivities.entrySet()) {
            PollenType pollenType = entry.getKey();
            Boolean isSensitive = entry.getValue();
            
            if (Boolean.TRUE.equals(isSensitive) && pollenType.getCategory() == category) {
                BigDecimal pollenWeight = pollenRiskWeights.getOrDefault(pollenType, new BigDecimal("0.5"));
                categoryRisk = categoryRisk.add(pollenWeight);
            }
        }
        
        return categoryRisk.multiply(categoryWeight).setScale(4, RoundingMode.HALF_UP);
    }
    
    private Map<PollenType, BigDecimal> initializePollenRiskWeights() {
        Map<PollenType, BigDecimal> weights = new EnumMap<>(PollenType.class);
        
        // Tree pollens
        weights.put(PollenType.BIRCH, new BigDecimal("0.9"));
        weights.put(PollenType.OLIVE, new BigDecimal("0.5"));
        weights.put(PollenType.PINE, new BigDecimal("0.6"));
        weights.put(PollenType.OAK, new BigDecimal("0.8"));
        weights.put(PollenType.CEDAR, new BigDecimal("0.7"));
        
        // Grass pollens
        weights.put(PollenType.GRAMINALES, new BigDecimal("1.0"));
        
        // Weed pollens
        weights.put(PollenType.RAGWEED, new BigDecimal("1.3"));
        weights.put(PollenType.MUGWORT, new BigDecimal("1.1"));
        weights.put(PollenType.PLANTAIN, new BigDecimal("1.0"));
        weights.put(PollenType.NETTLE, new BigDecimal("0.9"));
        
        return weights;
    }
}
package com.allermind.userpreference.domain.service;

import com.allermind.userpreference.domain.model.aggregate.UserPreference;
import com.allermind.userpreference.domain.model.enums.*;
import com.allermind.userpreference.domain.model.valueobject.AllergyClassificationResult;
import com.allermind.userpreference.domain.model.valueobject.RiskScore;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class AllergyGroupClassifierDomainService {
    
    private final RiskCalculationService riskCalculationService;
    private final CrossReactivityService crossReactivityService;
    
    public AllergyGroupClassifierDomainService(
            RiskCalculationService riskCalculationService,
            CrossReactivityService crossReactivityService) {
        this.riskCalculationService = riskCalculationService;
        this.crossReactivityService = crossReactivityService;
    }
    
    public AllergyClassificationResult classifyAllergyGroup(UserPreference userPreference) {
        // 1. Age vulnerability assessment
        boolean vulnerablePopulation = userPreference.hasVulnerableAge();
        
        // 2. Clinical status assessment
        AllergyGroupType clinicalGroup = assessClinicalStatus(userPreference.getClinicalDiagnosis());
        if (clinicalGroup != null) {
            return createClassificationResult(
                    clinicalGroup,
                    userPreference,
                    "Klinik tanı temelinde"
            );
        }
        
        // 3. Pollen sensitivity assessment
        RiskScore pollenRiskScore = riskCalculationService.calculatePollenRiskScore(userPreference);
        
        // 4. Genetic predisposition
        boolean familyHistory = userPreference.hasFamilyHistory();
        
        // Decision matrix
        if (familyHistory && pollenRiskScore.isModerate()) {
            return createClassificationResult(
                    AllergyGroupType.GENETIC_PREDISPOSITION,
                    userPreference,
                    String.format("Genetik yatkınlık + yüksek polen riski (%.2f)", pollenRiskScore.value().doubleValue())
            );
        }
        
        // Vulnerable population check
        if (vulnerablePopulation) {
            return createClassificationResult(
                    AllergyGroupType.VULNERABLE_POPULATION,
                    userPreference,
                    String.format("Yaş tabanlı vulnerabilite (%d yaş)", userPreference.getAge().value())
            );
        }
        
        // Default group (undiagnosed)
        return createClassificationResult(
                AllergyGroupType.UNDIAGNOSED,
                userPreference,
                String.format("Teşhis almamış, polen riski: %.2f", pollenRiskScore.value().doubleValue())
        );
    }
    
    private AllergyGroupType assessClinicalStatus(ClinicalDiagnosis diagnosis) {
        if (diagnosis == null) {
            return null;
        }
        return diagnosis.toAllergyGroupType();
    }
    
    private AllergyClassificationResult createClassificationResult(
            AllergyGroupType groupType,
            UserPreference userPreference,
            String reason) {
        
        return AllergyClassificationResult.builder()
                .groupType(groupType)
                .assignmentReason(reason)
                .modelWeight(groupType.getWeight())
                .personalRiskModifiers(calculatePersonalModifiers(userPreference, groupType))
                .immunologicProfile(getImmunologicProfile(groupType))
                .environmentalSensitivityFactors(getEnvironmentalFactors(userPreference))
                .pollenSpecificRisks(getPollenSpecificRisks(userPreference))
                .recommendationAdjustments(getRecommendationAdjustments(userPreference, groupType))
                .build();
    }
    
    private Map<String, Double> calculatePersonalModifiers(UserPreference userPreference, AllergyGroupType groupType) {
        Map<String, Double> modifiers = new HashMap<>();
        
        // Base sensitivity
        double baseSensitivity = 1.0;
        if (userPreference.getAge().isChild()) {
            baseSensitivity = 1.3;
        } else if (userPreference.getAge().isElderly()) {
            baseSensitivity = 1.2;
        }
        modifiers.put("base_sensitivity", baseSensitivity);
        
        // Environmental amplifier
        int triggerCount = userPreference.getEnvironmentalTriggerCount();
        double environmentalAmplifier = 1.0 + (triggerCount * 0.1);
        modifiers.put("environmental_amplifier", environmentalAmplifier);
        
        // Seasonal modifier
        double seasonalModifier = switch (groupType) {
            case SEVERE_ALLERGIC -> 1.5;
            case MILD_MODERATE_ALLERGIC -> 1.2;
            default -> 1.0;
        };
        modifiers.put("seasonal_modifier", seasonalModifier);
        
        // Comorbidity factor
        double comorbidityFactor = 1.0;
        if (userPreference.isOnMedication("asthma")) {
            comorbidityFactor = 1.4;
        } else if (userPreference.isOnMedication("bronchodilator")) {
            comorbidityFactor = 1.2;
        }
        modifiers.put("comorbidity_factor", comorbidityFactor);
        
        return modifiers;
    }
    
    private Map<String, Object> getImmunologicProfile(AllergyGroupType groupType) {
        Map<String, Object> profile = new HashMap<>();
        
        switch (groupType) {
            case SEVERE_ALLERGIC:
                profile.put("ige_level", "very_high");
                profile.put("th2_activation", "maximal");
                profile.put("mast_cell_degranulation", "rapid_widespread");
                profile.put("cytokine_profile", List.of("IL-4", "IL-5", "IL-13"));
                break;
                
            case MILD_MODERATE_ALLERGIC:
                profile.put("ige_level", "moderate_high");
                profile.put("inflammatory_response", "local");
                profile.put("antihistamine_response", "good");
                profile.put("seasonal_pattern", "rhinitis");
                break;
                
            case GENETIC_PREDISPOSITION:
                profile.put("atopic_structure", true);
                profile.put("family_loading", true);
                profile.put("ige_production_capacity", "increased");
                profile.put("th1_th2_imbalance", true);
                profile.put("sensitization_risk", "high");
                break;
                
            case UNDIAGNOSED:
                profile.put("ige_level", "normal_borderline");
                profile.put("sensitization", "unclear");
                profile.put("environmental_triggers", true);
                profile.put("inflammatory_response", "non_specific");
                break;
                
            case VULNERABLE_POPULATION:
                profile.put("immune_system", "immature_aged");
                profile.put("inflammatory_response", "increased");
                profile.put("immune_tolerance", "low");
                profile.put("multisystem_risk", "high");
                break;
        }
        
        return profile;
    }
    
    private Map<String, Boolean> getEnvironmentalFactors(UserPreference userPreference) {
        Map<String, Boolean> factors = new HashMap<>();
        factors.put("dust_mite_sensitivity", userPreference.hasEnvironmentalTrigger(EnvironmentalTrigger.DUST_MITES));
        factors.put("pet_dander_sensitivity", userPreference.hasEnvironmentalTrigger(EnvironmentalTrigger.PET_DANDER));
        factors.put("mold_sensitivity", userPreference.hasEnvironmentalTrigger(EnvironmentalTrigger.MOLD));
        factors.put("air_pollution_sensitivity", userPreference.hasEnvironmentalTrigger(EnvironmentalTrigger.AIR_POLLUTION));
        factors.put("smoke_sensitivity", userPreference.hasEnvironmentalTrigger(EnvironmentalTrigger.SMOKE));
        return factors;
    }
    
    private Map<String, List<String>> getPollenSpecificRisks(UserPreference userPreference) {
        Map<String, List<String>> risks = new HashMap<>();
        risks.put("high_risk_pollens", new ArrayList<>());
        risks.put("moderate_risk_pollens", new ArrayList<>());
        risks.put("cross_reactive_foods", new ArrayList<>());
        
        // Check all pollen types
        for (PollenType pollenType : PollenType.values()) {
            if (userPreference.hasPollenAllergy(pollenType)) {
                String riskLevel = getPollenRiskLevel(pollenType);
                if ("high".equals(riskLevel)) {
                    risks.get("high_risk_pollens").add(pollenType.getName());
                } else if ("moderate".equals(riskLevel)) {
                    risks.get("moderate_risk_pollens").add(pollenType.getName());
                }
                
                // Add cross-reactive foods
                List<FoodType> crossReactiveFoods = crossReactivityService.getCrossReactiveFoods(pollenType);
                for (FoodType food : crossReactiveFoods) {
                    risks.get("cross_reactive_foods").add(food.getName());
                }
            }
        }
        
        return risks;
    }
    
    private String getPollenRiskLevel(PollenType pollenType) {
        // Based on risk weights from RiskCalculationService
        return switch (pollenType) {
            case RAGWEED, MUGWORT -> "high";
            case BIRCH, OAK, GRAMINALES, PLANTAIN, NETTLE -> "moderate";
            case OLIVE, PINE, CEDAR -> "low";
        };
    }
    
    private Map<String, Object> getRecommendationAdjustments(UserPreference userPreference, AllergyGroupType groupType) {
        Map<String, Object> adjustments = new HashMap<>();
        
        // Default values
        adjustments.put("medication_priority", "standard");
        adjustments.put("environmental_control_level", "standard");
        adjustments.put("monitoring_frequency", "standard");
        adjustments.put("emergency_preparedness", false);
        
        // Group-specific adjustments
        switch (groupType) {
            case SEVERE_ALLERGIC:
                adjustments.put("medication_priority", "high");
                adjustments.put("environmental_control_level", "strict");
                adjustments.put("monitoring_frequency", "daily");
                adjustments.put("emergency_preparedness", true);
                break;
                
            case MILD_MODERATE_ALLERGIC:
                adjustments.put("medication_priority", "moderate");
                adjustments.put("environmental_control_level", "moderate");
                adjustments.put("monitoring_frequency", "weekly");
                break;
                
            case VULNERABLE_POPULATION:
                adjustments.put("medication_priority", "high");
                adjustments.put("environmental_control_level", "strict");
                adjustments.put("monitoring_frequency", "daily");
                break;
        }
        
        // Personal modifications
        if (userPreference.hasPreviousReaction(AllergyReactionType.ANAPHYLAXIS)) {
            adjustments.put("emergency_preparedness", true);
            adjustments.put("medication_priority", "critical");
        }
        
        return adjustments;
    }
}
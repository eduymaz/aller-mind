package com.allermind.userpreference.domain.model.valueobject;

import com.allermind.userpreference.domain.model.enums.AllergyGroupType;
import java.util.Map;
import java.util.List;

public class AllergyClassificationResult {
    
    private final AllergyGroupType groupType;
    private final String assignmentReason;
    private final double modelWeight;
    private final Map<String, Double> personalRiskModifiers;
    private final Map<String, Object> immunologicProfile;
    private final Map<String, Boolean> environmentalSensitivityFactors;
    private final Map<String, List<String>> pollenSpecificRisks;
    private final Map<String, Object> recommendationAdjustments;
    
    public AllergyClassificationResult(AllergyGroupType groupType, String assignmentReason, 
                                      double modelWeight, Map<String, Double> personalRiskModifiers,
                                      Map<String, Object> immunologicProfile,
                                      Map<String, Boolean> environmentalSensitivityFactors,
                                      Map<String, List<String>> pollenSpecificRisks,
                                      Map<String, Object> recommendationAdjustments) {
        this.groupType = groupType;
        this.assignmentReason = assignmentReason;
        this.modelWeight = modelWeight;
        this.personalRiskModifiers = personalRiskModifiers;
        this.immunologicProfile = immunologicProfile;
        this.environmentalSensitivityFactors = environmentalSensitivityFactors;
        this.pollenSpecificRisks = pollenSpecificRisks;
        this.recommendationAdjustments = recommendationAdjustments;
    }
    
    // Getters
    public AllergyGroupType getGroupType() {
        return groupType;
    }
    
    public String getAssignmentReason() {
        return assignmentReason;
    }
    
    public double getModelWeight() {
        return modelWeight;
    }
    
    public Map<String, Double> getPersonalRiskModifiers() {
        return personalRiskModifiers;
    }
    
    public Map<String, Object> getImmunologicProfile() {
        return immunologicProfile;
    }
    
    public Map<String, Boolean> getEnvironmentalSensitivityFactors() {
        return environmentalSensitivityFactors;
    }
    
    public Map<String, List<String>> getPollenSpecificRisks() {
        return pollenSpecificRisks;
    }
    
    public Map<String, Object> getRecommendationAdjustments() {
        return recommendationAdjustments;
    }
    
    public static Builder builder() {
        return new Builder();
    }
    
    public static class Builder {
        private AllergyGroupType groupType;
        private String assignmentReason;
        private double modelWeight;
        private Map<String, Double> personalRiskModifiers;
        private Map<String, Object> immunologicProfile;
        private Map<String, Boolean> environmentalSensitivityFactors;
        private Map<String, List<String>> pollenSpecificRisks;
        private Map<String, Object> recommendationAdjustments;
        
        public Builder groupType(AllergyGroupType groupType) {
            this.groupType = groupType;
            return this;
        }
        
        public Builder assignmentReason(String assignmentReason) {
            this.assignmentReason = assignmentReason;
            return this;
        }
        
        public Builder modelWeight(double modelWeight) {
            this.modelWeight = modelWeight;
            return this;
        }
        
        public Builder personalRiskModifiers(Map<String, Double> personalRiskModifiers) {
            this.personalRiskModifiers = personalRiskModifiers;
            return this;
        }
        
        public Builder immunologicProfile(Map<String, Object> immunologicProfile) {
            this.immunologicProfile = immunologicProfile;
            return this;
        }
        
        public Builder environmentalSensitivityFactors(Map<String, Boolean> environmentalSensitivityFactors) {
            this.environmentalSensitivityFactors = environmentalSensitivityFactors;
            return this;
        }
        
        public Builder pollenSpecificRisks(Map<String, List<String>> pollenSpecificRisks) {
            this.pollenSpecificRisks = pollenSpecificRisks;
            return this;
        }
        
        public Builder recommendationAdjustments(Map<String, Object> recommendationAdjustments) {
            this.recommendationAdjustments = recommendationAdjustments;
            return this;
        }
        
        public AllergyClassificationResult build() {
            return new AllergyClassificationResult(groupType, assignmentReason, modelWeight,
                    personalRiskModifiers, immunologicProfile, environmentalSensitivityFactors,
                    pollenSpecificRisks, recommendationAdjustments);
        }
    }
}
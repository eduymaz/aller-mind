package com.allermind.userpreference.application.dto;

import java.util.List;
import java.util.Map;
import java.util.UUID;

public class AllergyClassificationResponse {
    
    private UUID userPreferenceId;
    private Integer groupId;
    private String groupName;
    private String groupDescription;
    private String assignmentReason;
    private Double modelWeight;
    private Map<String, Double> personalRiskModifiers;
    private Map<String, Object> immunologicProfile;
    private Map<String, Boolean> environmentalSensitivityFactors;
    private Map<String, List<String>> pollenSpecificRisks;
    private Map<String, Object> recommendationAdjustments;
    
    // Default constructor
    public AllergyClassificationResponse() {}
    
    // Getters and setters
    public UUID getUserPreferenceId() {
        return userPreferenceId;
    }
    
    public void setUserPreferenceId(UUID userPreferenceId) {
        this.userPreferenceId = userPreferenceId;
    }
    
    public Integer getGroupId() {
        return groupId;
    }
    
    public void setGroupId(Integer groupId) {
        this.groupId = groupId;
    }
    
    public String getGroupName() {
        return groupName;
    }
    
    public void setGroupName(String groupName) {
        this.groupName = groupName;
    }
    
    public String getGroupDescription() {
        return groupDescription;
    }
    
    public void setGroupDescription(String groupDescription) {
        this.groupDescription = groupDescription;
    }
    
    public String getAssignmentReason() {
        return assignmentReason;
    }
    
    public void setAssignmentReason(String assignmentReason) {
        this.assignmentReason = assignmentReason;
    }
    
    public Double getModelWeight() {
        return modelWeight;
    }
    
    public void setModelWeight(Double modelWeight) {
        this.modelWeight = modelWeight;
    }
    
    public Map<String, Double> getPersonalRiskModifiers() {
        return personalRiskModifiers;
    }
    
    public void setPersonalRiskModifiers(Map<String, Double> personalRiskModifiers) {
        this.personalRiskModifiers = personalRiskModifiers;
    }
    
    public Map<String, Object> getImmunologicProfile() {
        return immunologicProfile;
    }
    
    public void setImmunologicProfile(Map<String, Object> immunologicProfile) {
        this.immunologicProfile = immunologicProfile;
    }
    
    public Map<String, Boolean> getEnvironmentalSensitivityFactors() {
        return environmentalSensitivityFactors;
    }
    
    public void setEnvironmentalSensitivityFactors(Map<String, Boolean> environmentalSensitivityFactors) {
        this.environmentalSensitivityFactors = environmentalSensitivityFactors;
    }
    
    public Map<String, List<String>> getPollenSpecificRisks() {
        return pollenSpecificRisks;
    }
    
    public void setPollenSpecificRisks(Map<String, List<String>> pollenSpecificRisks) {
        this.pollenSpecificRisks = pollenSpecificRisks;
    }
    
    public Map<String, Object> getRecommendationAdjustments() {
        return recommendationAdjustments;
    }
    
    public void setRecommendationAdjustments(Map<String, Object> recommendationAdjustments) {
        this.recommendationAdjustments = recommendationAdjustments;
    }
}
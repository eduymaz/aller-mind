package com.allermind.userpreference.application.dto;

import java.math.BigDecimal;
import java.util.List;
import java.util.Map;
import java.util.Set;
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
    
    // User preference details
    private Integer age;
    private String gender;
    private BigDecimal latitude;
    private BigDecimal longitude;
    private String clinicalDiagnosis;
    private Boolean familyAllergyHistory;
    private Map<String, Boolean> previousAllergicReactions;
    private Set<String> currentMedications;
    private Map<String, Boolean> treePollenAllergies;
    private Map<String, Boolean> grassPollenAllergies;
    private Map<String, Boolean> weedPollenAllergies;
    private Map<String, Boolean> foodAllergies;
    private Map<String, Boolean> environmentalTriggers;
    
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
    
    // User preference details getters and setters
    public Integer getAge() {
        return age;
    }
    
    public void setAge(Integer age) {
        this.age = age;
    }
    
    public String getGender() {
        return gender;
    }
    
    public void setGender(String gender) {
        this.gender = gender;
    }
    
    public BigDecimal getLatitude() {
        return latitude;
    }
    
    public void setLatitude(BigDecimal latitude) {
        this.latitude = latitude;
    }
    
    public BigDecimal getLongitude() {
        return longitude;
    }
    
    public void setLongitude(BigDecimal longitude) {
        this.longitude = longitude;
    }
    
    public String getClinicalDiagnosis() {
        return clinicalDiagnosis;
    }
    
    public void setClinicalDiagnosis(String clinicalDiagnosis) {
        this.clinicalDiagnosis = clinicalDiagnosis;
    }
    
    public Boolean getFamilyAllergyHistory() {
        return familyAllergyHistory;
    }
    
    public void setFamilyAllergyHistory(Boolean familyAllergyHistory) {
        this.familyAllergyHistory = familyAllergyHistory;
    }
    
    public Map<String, Boolean> getPreviousAllergicReactions() {
        return previousAllergicReactions;
    }
    
    public void setPreviousAllergicReactions(Map<String, Boolean> previousAllergicReactions) {
        this.previousAllergicReactions = previousAllergicReactions;
    }
    
    public Set<String> getCurrentMedications() {
        return currentMedications;
    }
    
    public void setCurrentMedications(Set<String> currentMedications) {
        this.currentMedications = currentMedications;
    }
    
    public Map<String, Boolean> getTreePollenAllergies() {
        return treePollenAllergies;
    }
    
    public void setTreePollenAllergies(Map<String, Boolean> treePollenAllergies) {
        this.treePollenAllergies = treePollenAllergies;
    }
    
    public Map<String, Boolean> getGrassPollenAllergies() {
        return grassPollenAllergies;
    }
    
    public void setGrassPollenAllergies(Map<String, Boolean> grassPollenAllergies) {
        this.grassPollenAllergies = grassPollenAllergies;
    }
    
    public Map<String, Boolean> getWeedPollenAllergies() {
        return weedPollenAllergies;
    }
    
    public void setWeedPollenAllergies(Map<String, Boolean> weedPollenAllergies) {
        this.weedPollenAllergies = weedPollenAllergies;
    }
    
    public Map<String, Boolean> getFoodAllergies() {
        return foodAllergies;
    }
    
    public void setFoodAllergies(Map<String, Boolean> foodAllergies) {
        this.foodAllergies = foodAllergies;
    }
    
    public Map<String, Boolean> getEnvironmentalTriggers() {
        return environmentalTriggers;
    }
    
    public void setEnvironmentalTriggers(Map<String, Boolean> environmentalTriggers) {
        this.environmentalTriggers = environmentalTriggers;
    }
}
package com.allermind.model.dto;

import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
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
    private String clinicalDiagnosis;
    private Boolean familyAllergyHistory;
    private Map<String, Boolean> previousAllergicReactions;
    private Set<String> currentMedications;
    private Map<String, Boolean> treePollenAllergies;
    private Map<String, Boolean> grassPollenAllergies;
    private Map<String, Boolean> weedPollenAllergies;
    private Map<String, Boolean> foodAllergies;
    private Map<String, Boolean> environmentalTriggers;
}
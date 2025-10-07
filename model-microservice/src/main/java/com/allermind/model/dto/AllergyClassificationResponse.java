package com.allermind.model.dto;

import java.util.List;
import java.util.Map;
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
}
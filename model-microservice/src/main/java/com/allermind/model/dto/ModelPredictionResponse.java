package com.allermind.model.dto;

import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ModelPredictionResponse {
    private Boolean success;
    private String message;
    private String error;
    private String timestamp;
    
    @JsonProperty("riskScore")
    private Double riskScore;
    
    @JsonProperty("riskLevel")
    private String riskLevel;
    
    private Double confidence;
    
    @JsonProperty("userGroup")
    private UserGroupInfo userGroup;
    
    @JsonProperty("contributingFactors")
    private Map<String, Object> contributingFactors;
    
    private List<String> recommendations;
    
    @JsonProperty("environmentalRisks")
    private Map<String, Object> environmentalRisks;
    
    @JsonProperty("personalModifiers")
    private Map<String, Object> personalModifiers;
    
    @JsonProperty("immunologicProfile")
    private Map<String, Object> immunologicProfile;
    
    @JsonProperty("environmentalSensitivityFactors")
    private Map<String, Boolean> environmentalSensitivityFactors;
    
    @JsonProperty("pollenSpecificRisks")
    private PollenSpecificRisks pollenSpecificRisks;
    
    @JsonProperty("dataQualityScore")
    private Double dataQualityScore;
    
    @JsonProperty("modelVersion")
    private String modelVersion;
    
    @JsonProperty("predictionTimestamp")
    private String predictionTimestamp;
    
    // Legacy fields for backward compatibility
    private List<GroupResult> predictions;
    
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class UserGroupInfo {
        @JsonProperty("groupId")
        private Integer groupId;
        
        @JsonProperty("groupName")
        private String groupName;
        
        @JsonProperty("description")
        private String description;
        
        @JsonProperty("assignmentReason")
        private String assignmentReason;
        
        @JsonProperty("modelWeight")
        private Double modelWeight;
    }
    
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class GroupResult {
        @JsonProperty("group_id")
        private Integer groupId;
        @JsonProperty("group_name")
        private String groupName;
        @JsonProperty("prediction_value")
        private Double predictionValue;
        @JsonProperty("risk_level")
        private String riskLevel;
        @JsonProperty("risk_emoji")
        private String riskEmoji;
        @JsonProperty("risk_code")
        private Integer riskCode;
    }
    
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class PredictionSummary {
        @JsonProperty("lowest_risk")
        private RiskGroup lowestRisk;
        @JsonProperty("highest_risk")
        private RiskGroup highestRisk;
        @JsonProperty("average_risk")
        private Double averageRisk;
    }
    
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class RiskGroup {
        @JsonProperty("group_id")
        private Integer groupId;
        @JsonProperty("group_name")
        private String groupName;
        private Double value;
    }
    
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class PollenSpecificRisks {
        @JsonProperty("high_risk_pollens")
        private List<String> highRiskPollens;
        
        @JsonProperty("cross_reactive_foods")
        private List<String> crossReactiveFoods;
        
        @JsonProperty("moderate_risk_pollens")
        private List<String> moderateRiskPollens;
    }
}

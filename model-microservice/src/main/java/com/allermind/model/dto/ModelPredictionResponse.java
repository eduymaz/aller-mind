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
    private LocationInfo location;
    @JsonProperty("user_group")
    private UserGroup userGroup;
    private List<GroupResult> predictions;
    private PredictionSummary summary;
    @JsonProperty("environmental_data")
    private Map<String, Object> environmentalData;
    private String timestamp;
    
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class LocationInfo {
        private Double latitude;
        private Double longitude;
        @JsonProperty("city_name")
        private String cityName;
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
}

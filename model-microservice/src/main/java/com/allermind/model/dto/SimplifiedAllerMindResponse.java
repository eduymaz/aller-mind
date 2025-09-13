package com.allermind.model.dto;

import java.util.List;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class SimplifiedAllerMindResponse {
    private String predictionId;
    private String userId;
    private String lat;
    private String lon;
    private Double overallRiskScore;
    private String overallRiskLevel;
    private String overallRiskEmoji;
    private String recommendation;
    private List<GroupPrediction> groupPredictions;
    private String cityName;
    private String timestamp;
    
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class GroupPrediction {
        private Integer groupId;
        private String groupName;
        private Double predictionValue;
        private String riskLevel;
        private String riskEmoji;
    }
}

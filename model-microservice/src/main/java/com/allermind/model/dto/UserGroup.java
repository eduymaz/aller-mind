package com.allermind.model.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserGroup {
    private String groupId;
    private String riskLevel; // LOW, MEDIUM, HIGH, CRITICAL
    private String groupDescription;
    private Double riskScore;
}

package com.allermind.model.dto;

import java.util.List;
import java.util.Map;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ModelPredictionRequest {
    private UserGroup userGroup;
    private List<PollenResponse> pollenData;
    private WeatherAirQualityResponse weatherAirQualityData;
    private Map<String, Object> additionalFeatures;
}

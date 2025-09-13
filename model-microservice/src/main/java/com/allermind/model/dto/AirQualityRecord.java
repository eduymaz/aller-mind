package com.allermind.model.dto;

import java.time.LocalDateTime;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class AirQualityRecord {
    private Long id;
    private String lat;
    private String lon;
    private LocalDateTime time;
    private Double pm10;
    private Double pm25;
    private Integer carbonDioxide;
    private Double carbonMonoxide;
    private Double nitrogenDioxide;
    private Double sulphurDioxide;
    private Double ozone;
    private Double aerosolOpticalDepth;
    private Double methane;
    private Double uvIndex;
    private Double uvIndexClearSky;
    private Integer dust;
}

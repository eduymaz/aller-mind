package com.allermind.model.dto;

import java.time.LocalDateTime;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class WeatherRecord {
    private Long id;
    private String lat;
    private String lon;
    private LocalDateTime time;
    private Double temperature2m;
    private Integer relativeHumidity2m;
    private Double precipitation;
    private Double snowfall;
    private Double rain;
    private Integer cloudCover;
    private Double surfacePressure;
    private Double windSpeed10m;
    private Integer windDirection10m;
    private Double soilTemperature0To7cm;
    private Double soilMoisture0To7cm;
    private Double sunshineDuration;
}

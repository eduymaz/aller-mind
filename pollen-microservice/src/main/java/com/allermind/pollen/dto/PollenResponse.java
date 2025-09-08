package com.allermind.pollen.dto;

import java.time.LocalDate;
import java.util.List;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PollenResponse {
    private String cityName;
    private String lat;
    private String lon;
    private LocalDate date;
    private String pollenCode;
    private Boolean inSeason;
    private Float upiValue;
    private String healthRecommendations;
    private List<PlantDataDto> plants;
}

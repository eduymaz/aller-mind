package com.allermind.pollen.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;
import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PollenResponse {
    private String cityName;
    private Float lat;
    private Float lon;
    private LocalDate date;
    private String pollenCode;
    private Boolean inSeason;
    private Float upiValue;
    private String healthRecommendations;
    private List<PlantDataDto> plants;
}

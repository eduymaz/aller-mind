package com.allermind.pollen.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PlantDataDto {
    private String plantCode;
    private Boolean inSeason;
    private Float upiValue;
    private String upiDescription;
    private String pictureUrl;
    private String pictureCloseupUrl;
}

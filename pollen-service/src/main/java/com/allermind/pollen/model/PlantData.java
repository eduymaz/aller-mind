package com.allermind.pollen.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "plant_data", schema = "POLLEN")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class PlantData {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "pollen_data_id", nullable = false)
    private PollenData pollenData;
    
    @Column(name = "plant_code", nullable = false)
    private String plantCode;
    
    @Column(name = "plant_in_season", nullable = false)
    private Boolean plantInSeason;
    
    @Column(name = "plant_upi_value", nullable = false)
    private Float plantUpiValue;
    
    @Column(name = "upi_description")
    private String upiDescription;
    
    @Column(name = "picture_url")
    private String pictureUrl;
    
    @Column(name = "picture_closeup_url")
    private String pictureCloseupUrl;
}

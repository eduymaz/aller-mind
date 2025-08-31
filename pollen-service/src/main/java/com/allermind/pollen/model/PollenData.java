package com.allermind.pollen.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "pollen_data", schema = "POLLEN")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class PollenData {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    
    @Column(name = "lat", nullable = false)
    private Float lat;
    
    @Column(name = "lon", nullable = false)
    private Float lon;
    
    @Column(name = "date", nullable = false)
    private LocalDate date;
    
    @Column(name = "pollen_code", nullable = false)
    private String pollenCode;
    
    @Column(name = "in_season", nullable = false)
    private Boolean inSeason;
    
    @Column(name = "upi_value", nullable = false)
    private Float upiValue;
    
    @Column(name = "health_recommendations")
    private String healthRecommendations;
    
    @OneToMany(mappedBy = "pollenData", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<PlantData> plants = new ArrayList<>();
}

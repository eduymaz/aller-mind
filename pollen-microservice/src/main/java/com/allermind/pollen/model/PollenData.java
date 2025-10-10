package com.allermind.pollen.model;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

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
    private String lat;
    
    @Column(name = "lon", nullable = false)
    private String lon;
    
    @Column(name = "date", nullable = false)
    private LocalDate date;
    
    @Column(name = "pollen_code", nullable = false)
    private String pollenCode;
    
    @Column(name = "in_season", nullable = false)
    private Boolean inSeason;
    
    @Column(name = "upi_value", nullable = false)
    private Float upiValue;
    
    @Column(name = "health_recommendations", length=100000)
    private String healthRecommendations;
    
    @OneToMany(mappedBy = "pollenData", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<PlantData> plants = new ArrayList<>();
}

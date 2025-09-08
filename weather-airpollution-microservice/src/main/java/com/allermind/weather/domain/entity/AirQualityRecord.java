package com.allermind.weather.domain.entity;

import java.time.LocalDateTime;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "air_quality_data")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class AirQualityRecord {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String lat;
    
    @Column(nullable = false)
    private String lon;
    
    @Column(nullable = false)
    private LocalDateTime time;
    
    @Column(nullable = false)
    private Double pm10;
    
    @Column(name = "pm2_5", nullable = false)
    private Double pm25;
    
    @Column(name = "carbon_dioxide", nullable = false)
    private Integer carbonDioxide;
    
    @Column(name = "carbon_monoxide", nullable = false)
    private Double carbonMonoxide;
    
    @Column(name = "nitrogen_dioxide", nullable = false)
    private Double nitrogenDioxide;
    
    @Column(name = "sulphur_dioxide", nullable = false)
    private Double sulphurDioxide;
    
    @Column(nullable = false)
    private Double ozone;
    
    @Column(name = "aerosol_optical_depth", nullable = false)
    private Double aerosolOpticalDepth;
    
    @Column(nullable = false)
    private Double methane;
    
    @Column(name = "uv_index", nullable = false)
    private Double uvIndex;
    
    @Column(name = "uv_index_clear_sky", nullable = false)
    private Double uvIndexClearSky;
    
    @Column(nullable = false)
    private Integer dust;
}

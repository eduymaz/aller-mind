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
@Table(name = "weather_data")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class WeatherRecord {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String lat;
    
    @Column(nullable = false)
    private String lon;
    
    @Column(nullable = false)
    private LocalDateTime time;
    
    @Column(name = "temperature_2m", nullable = false)
    private Double temperature2m;
    
    @Column(name = "relative_humidity_2m", nullable = false)
    private Integer relativeHumidity2m;
    
    @Column(nullable = false)
    private Double precipitation;
    
    @Column(nullable = false)
    private Double snowfall;
    
    @Column(nullable = false)
    private Double rain;
    
    @Column(name = "cloud_cover", nullable = false)
    private Integer cloudCover;
    
    @Column(name = "surface_pressure", nullable = false)
    private Double surfacePressure;
    
    @Column(name = "wind_speed_10m", nullable = false)
    private Double windSpeed10m;
    
    @Column(name = "wind_direction_10m", nullable = false)
    private Integer windDirection10m;
    
    @Column(name = "soil_temperature_0_to_7cm", nullable = false)
    private Double soilTemperature0To7cm;
    
    @Column(name = "soil_moisture_0_to_7cm", nullable = false)
    private Double soilMoisture0To7cm;
    
    @Column(name = "sunshine_duration", nullable = false)
    private Double sunshineDuration;
}

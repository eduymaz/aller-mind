package com.allermind.weather.domain.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "city")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class City {
    
    @Id
    private Integer plaka;
    
    @Column(name = "il_adi", nullable = false)
    private String ilAdi;
    
    @Column(nullable = false)
    private String lat;
    
    @Column(nullable = false)
    private String lon;
    
    @Column(name = "northeast_lat")
    private Double northeastLat;
    
    @Column(name = "northeast_lon")
    private Double northeastLon;
    
    @Column(name = "southwest_lat")
    private Double southwestLat;
    
    @Column(name = "southwest_lon")
    private Double southwestLon;
}

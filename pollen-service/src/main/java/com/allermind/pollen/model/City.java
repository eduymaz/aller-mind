package com.allermind.pollen.model;

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
    @Column(name = "plaka")
    private Integer plaka;
    
    @Column(name = "il_adi", nullable = false)
    private String ilAdi;
    
    @Column(name = "lat", nullable = false)
    private Float lat;
    
    @Column(name = "lon", nullable = false)
    private Float lon;
    
    @Column(name = "northeast_lat")
    private Float northeastLat;
    
    @Column(name = "northeast_lon")
    private Float northeastLon;
    
    @Column(name = "southwest_lat")
    private Float southwestLat;
    
    @Column(name = "southwest_lon")
    private Float southwestLon;
}

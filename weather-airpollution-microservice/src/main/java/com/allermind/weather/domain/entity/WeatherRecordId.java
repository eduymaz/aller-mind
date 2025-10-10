package com.allermind.weather.domain.entity;

import java.io.Serializable;
import java.time.LocalDateTime;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Composite primary key for WeatherRecord
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class WeatherRecordId implements Serializable {
    
    private static final long serialVersionUID = 1L;
    
    private String lat;
    private String lon;
    private LocalDateTime time;
}

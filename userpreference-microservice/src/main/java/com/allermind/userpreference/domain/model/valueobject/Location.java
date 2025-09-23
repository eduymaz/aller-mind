package com.allermind.userpreference.domain.model.valueobject;

import jakarta.persistence.Embeddable;
import java.math.BigDecimal;
import java.util.Objects;

@Embeddable
public record Location(BigDecimal latitude, BigDecimal longitude) {
    
    public Location {
        Objects.requireNonNull(latitude, "Latitude cannot be null");
        Objects.requireNonNull(longitude, "Longitude cannot be null");
        
        if (latitude.compareTo(new BigDecimal("90")) > 0 || latitude.compareTo(new BigDecimal("-90")) < 0) {
            throw new IllegalArgumentException("Latitude must be between -90 and 90, but was: " + latitude);
        }
        
        if (longitude.compareTo(new BigDecimal("180")) > 0 || longitude.compareTo(new BigDecimal("-180")) < 0) {
            throw new IllegalArgumentException("Longitude must be between -180 and 180, but was: " + longitude);
        }
    }
    
    public static Location of(double latitude, double longitude) {
        return new Location(BigDecimal.valueOf(latitude), BigDecimal.valueOf(longitude));
    }
}
package com.allermind.userpreference.domain.model.valueobject;

import jakarta.persistence.Embeddable;
import java.math.BigDecimal;

@Embeddable
public record RiskScore(BigDecimal value) {
    
    private static final BigDecimal MIN_SCORE = BigDecimal.ZERO;
    private static final BigDecimal MAX_SCORE = BigDecimal.ONE;
    
    public RiskScore {
        if (value.compareTo(MIN_SCORE) < 0 || value.compareTo(MAX_SCORE) > 0) {
            throw new IllegalArgumentException("Risk score must be between 0 and 1, but was: " + value);
        }
    }
    
    public boolean isHigh() {
        return value.compareTo(new BigDecimal("0.7")) >= 0;
    }
    
    public boolean isModerate() {
        return value.compareTo(new BigDecimal("0.4")) >= 0 && 
               value.compareTo(new BigDecimal("0.7")) < 0;
    }
    
    public boolean isLow() {
        return value.compareTo(new BigDecimal("0.4")) < 0;
    }
    
    public static RiskScore of(double value) {
        return new RiskScore(BigDecimal.valueOf(value));
    }
}
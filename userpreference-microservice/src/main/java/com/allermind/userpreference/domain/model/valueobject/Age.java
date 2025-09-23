package com.allermind.userpreference.domain.model.valueobject;

import jakarta.persistence.Embeddable;

@Embeddable
public record Age(int value) {
    
    public Age {
        if (value < 0 || value > 150) {
            throw new IllegalArgumentException("Age must be between 0 and 150, but was: " + value);
        }
    }
    
    public boolean isVulnerable() {
        return value <= 12 || value >= 65;
    }
    
    public boolean isChild() {
        return value <= 12;
    }
    
    public boolean isElderly() {
        return value >= 65;
    }
    
    public boolean isAdult() {
        return value > 12 && value < 65;
    }
}
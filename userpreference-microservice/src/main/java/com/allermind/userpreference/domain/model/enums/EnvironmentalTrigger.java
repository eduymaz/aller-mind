package com.allermind.userpreference.domain.model.enums;

public enum EnvironmentalTrigger {
    DUST_MITES("dust_mites"),
    PET_DANDER("pet_dander"),
    MOLD("mold"),
    AIR_POLLUTION("air_pollution"),
    SMOKE("smoke");
    
    private final String name;
    
    EnvironmentalTrigger(String name) {
        this.name = name;
    }
    
    public String getName() {
        return name;
    }
}
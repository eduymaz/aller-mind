package com.allermind.userpreference.domain.model.enums;

public enum AllergyReactionType {
    ANAPHYLAXIS("anaphylaxis"),
    SEVERE_ASTHMA("severe_asthma"),
    HOSPITALIZATION("hospitalization"),
    SKIN_REACTIONS("skin_reactions"),
    RESPIRATORY_SYMPTOMS("respiratory_symptoms");
    
    private final String name;
    
    AllergyReactionType(String name) {
        this.name = name;
    }
    
    public String getName() {
        return name;
    }
}
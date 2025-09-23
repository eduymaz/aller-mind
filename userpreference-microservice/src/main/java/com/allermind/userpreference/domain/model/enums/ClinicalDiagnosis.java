package com.allermind.userpreference.domain.model.enums;

public enum ClinicalDiagnosis {
    NONE("none"),
    MILD_MODERATE_ALLERGY("mild_moderate_allergy"),
    SEVERE_ALLERGY("severe_allergy"),
    ASTHMA("asthma");
    
    private final String value;
    
    ClinicalDiagnosis(String value) {
        this.value = value;
    }
    
    public String getValue() {
        return value;
    }
    
    public AllergyGroupType toAllergyGroupType() {
        return switch (this) {
            case SEVERE_ALLERGY -> AllergyGroupType.SEVERE_ALLERGIC;
            case MILD_MODERATE_ALLERGY -> AllergyGroupType.MILD_MODERATE_ALLERGIC;
            case ASTHMA -> AllergyGroupType.MILD_MODERATE_ALLERGIC;
            case NONE -> null;
        };
    }
}
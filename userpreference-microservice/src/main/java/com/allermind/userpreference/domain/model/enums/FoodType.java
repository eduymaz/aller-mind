package com.allermind.userpreference.domain.model.enums;

public enum FoodType {
    // Tree pollens cross-reactive foods
    APPLE("apple"),
    CHERRY("cherry"),
    PEAR("pear"),
    ALMOND("almond"),
    
    // Ragweed cross-reactive foods
    MELON("melon"),
    BANANA("banana"),
    CUCUMBER("cucumber"),
    
    // Mugwort cross-reactive foods
    CELERY("celery"),
    SPICES("spices"),
    HERBS("herbs"),
    
    // Common allergens
    NUTS("nuts"),
    SHELLFISH("shellfish"),
    MILK("milk"),
    EGGS("eggs"),
    SOY("soy"),
    WHEAT("wheat"),
    FISH("fish");
    
    private final String name;
    
    FoodType(String name) {
        this.name = name;
    }
    
    public String getName() {
        return name;
    }
}